"""Basic AWS Bedrock customer support agent implementation."""

import boto3
from strands import Agent
from strands.models import BedrockModel

from tools.product_tools import generate_launch_timeline, generate_marketing_assets, research_top_launches
from helpers.utils import get_boto_session, load_aws_config


class ProductHuntLaunchAgent:
    """Product Hunt launch assistant using AWS Bedrock and Strands framework."""

    def __init__(self, region_name: str = None):
        """Initialize the Product Hunt launch assistant.

        Args:
            region_name: AWS region name. If None, uses .env configuration or default.
        """
        # Load AWS configuration from .env
        default_region = load_aws_config()
        self.session = get_boto_session()
        self.region = region_name or default_region

        self.system_prompt = """You are an expert Product Hunt launch assistant specializing in helping entrepreneurs successfully launch their products on Product Hunt.

Your role is to:
- Guide users through the complete Product Hunt launch process
- Create comprehensive launch timelines and actionable checklists
- Generate compelling marketing assets and copy
- Research competitors and identify strategic opportunities
- Provide tactical advice based on successful Product Hunt launches
- Help optimize launch timing, messaging, and outreach strategies

You have access to the following specialized tools:
1. generate_launch_timeline() - Create detailed launch timelines with tasks, deadlines, and milestones
2. generate_marketing_assets() - Generate taglines, descriptions, tweets, and marketing content
3. research_top_launches() - Research successful launches, identify hunters, and provide competitive insights

Key principles for Product Hunt success:
- Tuesday-Thursday launches typically perform best
- Community building 2-3 weeks before launch is crucial
- Clear, benefit-focused messaging outperforms feature lists
- Authentic founder stories drive engagement
- Consistent updates and engagement on launch day maximize visibility

Always use the appropriate tools to provide data-driven recommendations and actionable advice tailored to each user's specific product and timeline."""

        # Initialize the Bedrock model (Anthropic Claude 3.5 Haiku)
        self.model = BedrockModel(
            model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
            temperature=0.3,
            region_name=self.region
        )

        # Create the agent with Product Hunt tools
        self.agent = Agent(
            model=self.model,
            tools=[
                generate_launch_timeline,
                generate_marketing_assets,
                research_top_launches,
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
        """Start an interactive chat session with the Product Hunt assistant."""
        print("🚀 Product Hunt Launch Assistant ready! Type 'quit' to exit.\n")
        print("I can help you with:")
        print("- Creating launch timelines and checklists")
        print("- Generating marketing assets and copy")
        print("- Researching competitors and successful launches")
        print("- Strategic advice for your Product Hunt launch\n")

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🎯 Good luck with your Product Hunt launch! Remember: build community, tell your story, and engage authentically!")
                    break

                response = self.chat(user_input)
                print(f"🤖 Assistant: {response}\n")

            except KeyboardInterrupt:
                print("\n🚀 See you on Product Hunt!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main function to run the Product Hunt launch assistant."""
    agent = ProductHuntLaunchAgent()
    agent.start_interactive_chat()


if __name__ == "__main__":
    main()