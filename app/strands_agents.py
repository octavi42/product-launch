"""
Product Hunt Launch Assistant using Strands Agents
"""

from typing import Dict, Any
from strands import Agent, tool
from strands.models import BedrockModel
from app.tools import generate_launch_timeline, generate_marketing_assets, research_top_launches

# Configure Bedrock model for all agents
BEDROCK_MODEL = BedrockModel(
    region_name="us-west-2",
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.3
)


class ProductHuntPlanningAgent(Agent):
    """Agent for generating launch timelines and checklists"""
    
    def __init__(self):
        super().__init__(
            model=BEDROCK_MODEL,
            name="planning_agent",
            description="Generate comprehensive launch timelines and checklists for Product Hunt launches",
            tools=[tool(generate_launch_timeline)],
            system_prompt="""
            You are a Product Hunt launch expert specializing in creating detailed timelines and checklists.
            When given a product name, type, and launch date, generate a comprehensive timeline with:
            - Specific tasks with deadlines
            - Priority levels (High/Medium/Low)
            - Time estimates
            - Dependencies
            - Success criteria
            
            Focus on actionable, specific tasks that founders can execute immediately.
            Consider industry-specific requirements and best practices.
            """
        )


class ProductHuntAssetAgent(Agent):
    """Agent for generating marketing assets"""
    
    def __init__(self):
        super().__init__(
            model=BEDROCK_MODEL,
            name="asset_prep_agent",
            description="Create compelling marketing assets like taglines, descriptions, and social media content",
            tools=[tool(generate_marketing_assets)],
            system_prompt="""
            You are a marketing expert specializing in Product Hunt launch content.
            Generate multiple options for:
            - Compelling taglines (3-8 words)
            - Short descriptions optimized for Product Hunt
            - Social media tweets with hashtags
            - A/B testing suggestions
            
            Ensure all content is engaging, shareable, and optimized for the target audience.
            Vary the approach (problem-focused, benefit-focused, feature-focused).
            """
        )


class ProductHuntResearchAgent(Agent):
    """Agent for researching top launches and finding hunters"""
    
    def __init__(self):
        super().__init__(
            model=BEDROCK_MODEL,
            name="research_agent",
            description="Research top Product Hunt launches and find relevant hunters for your domain",
            tools=[tool(research_top_launches)],
            system_prompt="""
            You are a Product Hunt research expert specializing in competitive analysis and hunter identification.
            Research and analyze:
            - Top launches in the product category
            - Success factors and patterns
            - Recommended hunters with relevant experience
            - Market insights and positioning strategies
            
            Provide actionable insights and specific recommendations for launch success.
            Focus on recent launches and current trends.
            """
        )


class ProductHuntCoordinator:
    """Coordinates all Product Hunt agents"""
    
    def __init__(self):
        self.planning_agent = ProductHuntPlanningAgent()
        self.asset_agent = ProductHuntAssetAgent()
        self.research_agent = ProductHuntResearchAgent()
    
    async def route_request(self, agent_type: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate agent"""
        try:
            if agent_type == "planning":
                result = await self.planning_agent.invoke_async(
                    f"Generate a launch timeline for {request_data.get('product_name', '')} "
                    f"({request_data.get('product_type', '')}) launching on {request_data.get('launch_date', '')}. "
                    f"Additional notes: {request_data.get('additional_notes', '')}"
                )
            elif agent_type == "asset_prep":
                result = await self.asset_agent.invoke_async(
                    f"Generate marketing assets for {request_data.get('product_name', '')} "
                    f"with elevator pitch: {request_data.get('elevator_pitch', '')} "
                    f"targeting {request_data.get('target_audience', '')} "
                    f"with {request_data.get('tone', 'professional')} tone"
                )
            elif agent_type == "research":
                result = await self.research_agent.invoke_async(
                    f"Research top launches in {request_data.get('product_category', '')} "
                    f"category targeting {request_data.get('target_audience', '')} "
                    f"with budget range: {request_data.get('budget_range', '')}"
                )
            else:
                return {
                    "success": False,
                    "error": f"Unknown agent type: {agent_type}",
                    "agent_type": agent_type
                }
            
            # Extract the actual response content from AgentResult
            if hasattr(result, 'message') and result.message:
                # Get the content from the message
                content = result.message.get('content', [])
                if content and len(content) > 0:
                    # Extract text from the first content item
                    response_text = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
                else:
                    response_text = str(result)
            else:
                response_text = str(result)
            
            return {
                "success": True,
                "data": response_text,
                "agent_type": agent_type
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Agent execution failed: {str(e)}",
                "agent_type": agent_type
            }
    
    def get_available_agents(self) -> Dict[str, str]:
        """Get list of available agents and their descriptions"""
        return {
            "planning": "Generate launch timeline and checklist",
            "asset_prep": "Create taglines, descriptions, and tweets",
            "research": "Find top launches and recommend hunters"
        }
