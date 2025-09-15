#!/usr/bin/env python3
"""Main entry point for the Product Hunt Launch Assistant."""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import ProductHuntLaunchAgent


def main():
    """Main function to run the Product Hunt launch assistant."""
    print("🚀 Product Hunt Launch Assistant")
    print("=" * 40)
    print("Your AI-powered guide to Product Hunt success!")
    print()

    try:
        agent = ProductHuntLaunchAgent()
        agent.start_interactive_chat()
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
        print("Please ensure AWS credentials are configured and Claude 3.5 Haiku is enabled in Bedrock.")
        sys.exit(1)


if __name__ == "__main__":
    main()