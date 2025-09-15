#!/usr/bin/env python3
"""Main entry point for the AWS Bedrock customer support agent."""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import CustomerSupportAgent


def main():
    """Main function to run the customer support agent."""
    print("🤖 AWS Bedrock Customer Support Agent")
    print("=" * 40)

    try:
        agent = CustomerSupportAgent()
        agent.start_interactive_chat()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        print("Please ensure AWS credentials are configured and Claude 3.7 Sonnet is enabled in Bedrock.")
        sys.exit(1)


if __name__ == "__main__":
    main()