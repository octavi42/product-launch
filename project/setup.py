#!/usr/bin/env python3
"""Setup script for AWS Bedrock customer support agent."""

import os
import sys
import subprocess
from pathlib import Path


def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_aws_config():
    """Check if AWS configuration is set up."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and add your credentials")
        return False

    print("✅ AWS configuration found in .env")
    return True


def test_aws_connection():
    """Test AWS connection with provided credentials."""
    print("🔗 Testing AWS connection...")
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()

        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()

        print(f"✅ AWS connection successful!")
        print(f"   Account: {identity['Account']}")
        print(f"   Region: {os.getenv('AWS_DEFAULT_REGION', 'us-west-2')}")
        return True

    except Exception as e:
        print(f"❌ AWS connection failed: {e}")
        print("Please check your credentials in .env file")
        return False


def check_bedrock_access():
    """Check if Claude 3.7 Sonnet is accessible in Bedrock."""
    print("🧠 Testing Bedrock model access...")
    try:
        from dotenv import load_dotenv
        load_dotenv()

        import boto3
        bedrock = boto3.client('bedrock', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'))

        # Try to list foundation models to check access
        response = bedrock.list_foundation_models()

        # Check if Claude 3.7 Sonnet is available
        claude_models = [
            model for model in response.get('modelSummaries', [])
            if 'claude-3' in model.get('modelId', '').lower() and 'sonnet' in model.get('modelId', '').lower()
        ]

        if claude_models:
            print("✅ Bedrock access confirmed!")
            print("✅ Claude models are available")
            return True
        else:
            print("⚠️  Bedrock access confirmed, but Claude models may not be enabled")
            print("   Please enable Claude 3.7 Sonnet in the AWS Bedrock console")
            return True

    except Exception as e:
        print(f"❌ Bedrock access failed: {e}")
        print("Please ensure you have Bedrock permissions and Claude 3.7 Sonnet is enabled")
        return False


def main():
    """Main setup function."""
    print("🤖 AWS Bedrock Customer Support Agent Setup")
    print("=" * 50)

    success = True

    # Check if .env file exists
    if not check_aws_config():
        success = False

    # Install dependencies
    if not install_dependencies():
        success = False

    # Test AWS connection
    if success and not test_aws_connection():
        success = False

    # Test Bedrock access
    if success and not check_bedrock_access():
        success = False

    print("\n" + "=" * 50)

    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Start chatting with your customer support agent!")
    else:
        print("❌ Setup failed. Please fix the issues above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()