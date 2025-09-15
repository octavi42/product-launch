#!/usr/bin/env python3
"""
Test the Bedrock model connection
"""

import os
from app.utils import BedrockClient


def test_model():
    """Test the Bedrock model"""
    print("🧪 Testing Bedrock Model Connection")
    print("=" * 50)
    
    # Check AWS credentials
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("❌ AWS_ACCESS_KEY_ID not set")
        print("Set your AWS credentials first:")
        print("export AWS_ACCESS_KEY_ID=your_key")
        print("export AWS_SECRET_ACCESS_KEY=your_secret")
        print("export AWS_REGION=us-west-2")
        return False
    
    try:
        # Initialize the client
        client = BedrockClient()
        print("✅ Bedrock client initialized")
        print(f"   Model ID: {client.model_id}")
        print(f"   Temperature: {client.temperature}")
        print(f"   Region: {os.getenv('AWS_REGION', 'us-west-2')}")
        
        # Test with a simple prompt
        print("\n🔍 Testing model with simple prompt...")
        response = client.invoke_model("Hello, can you respond with 'Model is working!'?")
        
        print("✅ Model response received:")
        print(f"   {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_model()
    if success:
        print("\n🎉 Model test successful! Your Product Hunt Launch Assistant should work now.")
    else:
        print("\n❌ Model test failed. Check your AWS configuration.")
