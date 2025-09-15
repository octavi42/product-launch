"""Basic AWS Bedrock customer support agent implementation."""

import boto3
from strands import Agent
from strands.models import BedrockModel

from tools.product_tools import get_return_policy, get_product_info, web_search
from helpers.utils import get_boto_session, load_aws_config


class CustomerSupportAgent:
    """Customer support agent using AWS Bedrock and Strands framework."""

    def __init__(self, region_name: str = None):
        """Initialize the customer support agent.

        Args:
            region_name: AWS region name. If None, uses .env configuration or default.
        """
        # Load AWS configuration from .env
        default_region = load_aws_config()
        self.session = get_boto_session()
        self.region = region_name or default_region

        self.system_prompt = """You are a helpful and professional customer support assistant for an electronics e-commerce company.
Your role is to:
- Provide accurate information using the tools available to you
- Support the customer with technical information and product specifications, and maintenance questions
- Be friendly, patient, and understanding with customers
- Always offer additional help after answering questions
- If you can't help with something, direct customers to the appropriate contact

You have access to the following tools:
1. get_return_policy() - For warranty and return policy questions
2. get_product_info() - To get information about a specific product
3. web_search() - To access current technical documentation, or for updated information

Always use the appropriate tool to get accurate, up-to-date information rather than making assumptions about electronic products or specifications."""

        # Initialize the Bedrock model (Anthropic Claude 3.7 Sonnet)
        self.model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            temperature=0.3,
            region_name=self.region
        )

        # Create the agent with tools
        self.agent = Agent(
            model=self.model,
            tools=[
                get_product_info,
                get_return_policy,
                web_search,
            ],
            system_prompt=self.system_prompt,
        )

    def chat(self, message: str) -> str:
        """Send a message to the agent and get response.

        Args:
            message: User's message

        Returns:
            Agent's response
        """
        return self.agent(message)

    def start_interactive_chat(self):
        """Start an interactive chat session with the agent."""
        print("Customer Support Agent initialized! Type 'quit' to exit.\n")

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Thank you for contacting customer support!")
                    break

                response = self.chat(user_input)
                print(f"Agent: {response}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main function to run the customer support agent."""
    agent = CustomerSupportAgent()
    agent.start_interactive_chat()


if __name__ == "__main__":
    main()