"""AgentCore Memory integration for Product Hunt Launch Assistant."""

import logging
import os
import sys
import uuid
from typing import Dict, Optional

import boto3
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.constants import StrategyType
from boto3.session import Session
from botocore.exceptions import ClientError
from strands.hooks import (
    AfterInvocationEvent,
    HookProvider,
    HookRegistry,
    MessageAddedEvent,
)

from .utils import get_ssm_parameter, put_ssm_parameter

# Initialize logging
logger = logging.getLogger(__name__)

# Get AWS session and region
boto_session = Session()
REGION = 'us-west-2'

# Initialize memory client
memory_client = MemoryClient(region_name=REGION)
memory_name = "ProductHuntLaunchMemory"


def create_or_get_memory_resource():
    """Create or retrieve existing AgentCore Memory resource for Product Hunt launches."""
    try:
        memory_id = get_ssm_parameter("/app/producthunt/agentcore/memory_id")
        memory_client.gmcp_client.get_memory(memoryId=memory_id)
        return memory_id
    except Exception as e:
        print(f"Could not retrieve existing memory resource: {e}")
        try:
            strategies = [
                {
                    StrategyType.USER_PREFERENCE.value: {
                        "name": "ProductLaunchPreferences",
                        "description": "Captures user's product launch preferences, communication style, and strategic approach",
                        "namespaces": ["producthunt/user/{actorId}/preferences"],
                    }
                },
                {
                    StrategyType.SEMANTIC.value: {
                        "name": "ProductLaunchSemantic",
                        "description": "Stores factual information about products, launch strategies, and recommendations",
                        "namespaces": ["producthunt/user/{actorId}/semantic"],
                    }
                },
            ]
            print("Creating AgentCore Memory resources for Product Hunt Launch Assistant...")
            print(f"Using AWS region: {REGION}")
            print("This will take 2-3 minutes as AWS sets up the managed services...")
            
            # Create memory resource with semantic and user_pref strategy
            response = memory_client.create_memory_and_wait(
                name=memory_name,
                description="Product Hunt launch assistant memory for user preferences and product context",
                strategies=strategies,
                event_expiry_days=90,  # Memories expire after 90 days
            )
            memory_id = response["id"]
            try:
                put_ssm_parameter("/app/producthunt/agentcore/memory_id", memory_id)
            except Exception as ssm_error:
                print(f"Warning: Could not save memory ID to SSM: {ssm_error}")
            return memory_id
        except Exception as e:
            print(f"Failed to create memory resource: {e}")
            print("Memory functionality will be disabled. Please check your AWS credentials and region.")
            return None


def delete_memory(memory_hook):
    """Delete the memory resource and SSM parameter."""
    try:
        ssm_client = boto3.client("ssm", region_name=REGION)
        memory_client.delete_memory(memory_id=memory_hook.memory_id)
        ssm_client.delete_parameter(Name="/app/producthunt/agentcore/memory_id")
    except Exception:
        pass


class ProductHuntMemoryHooks(HookProvider):
    """Memory hooks for Product Hunt Launch Assistant."""

    def __init__(
        self, memory_id: str, client: MemoryClient, actor_id: str, session_id: str
    ):
        self.memory_id = memory_id
        self.client = client
        self.actor_id = actor_id
        self.session_id = session_id
        self.namespaces = {
            i["type"]: i["namespaces"][0]
            for i in self.client.get_memory_strategies(self.memory_id)
        }

    def retrieve_product_context(self, event: MessageAddedEvent):
        """Retrieve product and user context before processing launch query."""
        messages = event.agent.messages
        if (
            messages[-1]["role"] == "user"
            and "toolResult" not in messages[-1]["content"][0]
        ):
            user_query = messages[-1]["content"][0]["text"]

            try:
                all_context = []

                for context_type, namespace in self.namespaces.items():
                    # Retrieve user context from each namespace
                    memories = self.client.retrieve_memories(
                        memory_id=self.memory_id,
                        namespace=namespace.format(actorId=self.actor_id),
                        query=user_query,
                        top_k=3,
                    )
                    # Post-processing: Format memories into context strings
                    for memory in memories:
                        if isinstance(memory, dict):
                            content = memory.get("content", {})
                            if isinstance(content, dict):
                                text = content.get("text", "").strip()
                                if text:
                                    all_context.append(
                                        f"[{context_type.upper()}] {text}"
                                    )

                # Inject product context into the query
                if all_context:
                    context_text = "\n".join(all_context)
                    original_text = messages[-1]["content"][0]["text"]
                    messages[-1]["content"][0][
                        "text"
                    ] = f"Product Launch Context:\n{context_text}\n\n{original_text}"
                    logger.info(f"Retrieved {len(all_context)} product context items")

            except Exception as e:
                logger.error(f"Failed to retrieve product context: {e}")

    def save_launch_interaction(self, event: AfterInvocationEvent):
        """Save product launch interaction after agent response."""
        try:
            messages = event.agent.messages
            if len(messages) >= 2 and messages[-1]["role"] == "assistant":
                # Get last user query and agent response
                user_query = None
                agent_response = None

                for msg in reversed(messages):
                    if msg["role"] == "assistant" and not agent_response:
                        agent_response = msg["content"][0]["text"]
                    elif (
                        msg["role"] == "user"
                        and not user_query
                        and "toolResult" not in msg["content"][0]
                    ):
                        user_query = msg["content"][0]["text"]
                        break

                if user_query and agent_response:
                    # Save the launch interaction to memory
                    self.client.create_event(
                        memory_id=self.memory_id,
                        actor_id=self.actor_id,
                        session_id=self.session_id,
                        messages=[
                            (user_query, "USER"),
                            (agent_response, "ASSISTANT"),
                        ],
                    )
                    logger.info("Saved product launch interaction to memory")

        except Exception as e:
            logger.error(f"Failed to save launch interaction: {e}")

    def register_hooks(self, registry: HookRegistry) -> None:
        """Register product launch memory hooks."""
        registry.add_callback(MessageAddedEvent, self.retrieve_product_context)
        registry.add_callback(AfterInvocationEvent, self.save_launch_interaction)
        logger.info("Product Hunt launch memory hooks registered")


def get_memory_hooks(actor_id: str = None, session_id: str = None):
    """Setup memory resource and return Memory hooks for agent."""
    memory_id = create_or_get_memory_resource()
    if not memory_id:
        return None
        
    # Use provided IDs or generate defaults
    if not actor_id:
        actor_id = f"user_{uuid.uuid4().hex[:8]}"
    if not session_id:
        session_id = str(uuid.uuid4())
    
    memory_hooks = ProductHuntMemoryHooks(
        memory_id=memory_id,
        client=memory_client,
        actor_id=actor_id,
        session_id=session_id,
    )

    return memory_hooks


def seed_product_memory(memory_id: str, actor_id: str, product_data: Dict):
    """Seed memory with initial product information."""
    try:
        # Create initial product context
        product_context = f"""
        Product Information:
        - Name: {product_data.get('product_name', 'Not specified')}
        - Type: {product_data.get('product_type', 'SaaS')}
        - Description: {product_data.get('product_description', 'Not provided')}
        - Target Audience: {product_data.get('target_audience', 'Not specified')}
        - Launch Date: {product_data.get('launch_date', 'Not specified')}
        - Additional Notes: {product_data.get('additional_notes', 'None')}
        - GitHub Repository: {product_data.get('github_repo', 'Not provided')}
        """
        
        # Save initial product context
        memory_client.create_event(
            memory_id=memory_id,
            actor_id=actor_id,
            session_id="initial_setup",
            messages=[
                (f"I'm launching a product: {product_data.get('product_name', 'my product')}", "USER"),
                (product_context, "ASSISTANT"),
            ],
        )
        logger.info("Seeded product memory with initial context")
        return True
        
    except Exception as e:
        logger.error(f"Failed to seed product memory: {e}")
        return False


def get_user_memory_summary(memory_id: str, actor_id: str) -> Dict:
    """Get a summary of user's stored memories."""
    try:
        summary = {
            "preferences": [],
            "semantic": [],
            "total_memories": 0
        }
        
        for context_type, namespace in {
            "preferences": f"producthunt/user/{actor_id}/preferences",
            "semantic": f"producthunt/user/{actor_id}/semantic"
        }.items():
            memories = memory_client.retrieve_memories(
                memory_id=memory_id,
                namespace=namespace,
                query="product launch context",
                top_k=5,
            )
            
            for memory in memories:
                if isinstance(memory, dict):
                    content = memory.get("content", {})
                    if isinstance(content, dict):
                        text = content.get("text", "").strip()
                        if text:
                            summary[context_type].append(text)
            
            summary["total_memories"] += len(memories)
        
        return summary
        
    except Exception as e:
        logger.error(f"Failed to get memory summary: {e}")
        return {"preferences": [], "semantic": [], "total_memories": 0}
