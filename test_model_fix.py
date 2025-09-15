#!/usr/bin/env python3
"""
Test the corrected Bedrock model configuration
"""

import asyncio
import os
from app.strands_agents import ProductHuntCoordinator


async def test_model_fix():
    """Test that the corrected model works"""
    print("🧪 Testing Corrected Bedrock Model")
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
        # Initialize coordinator
        coordinator = ProductHuntCoordinator()
        print("✅ Strands coordinator initialized with Claude 3.5 Sonnet")
        
        # Test planning agent with a simple request
        print("\n🔍 Testing Planning Agent...")
        planning_result = await coordinator.route_request("planning", {
            "product_name": "TestApp",
            "product_type": "SaaS",
            "launch_date": "next Friday",
            "additional_notes": "Simple test"
        })
        
        if planning_result.get('success'):
            print("✅ Planning agent working!")
            print(f"   Response length: {len(str(planning_result.get('data', '')))}")
        else:
            print(f"❌ Planning agent failed: {planning_result.get('error')}")
            return False
        
        print("\n🎉 Model fix successful!")
        print("✅ Claude 3.5 Sonnet is working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Main test function"""
    success = await test_model_fix()
    
    if success:
        print("\n✅ Your Product Hunt Launch Assistant is ready!")
        print("Run 'make run' to start the application.")
    else:
        print("\n❌ There are still issues with the model configuration.")


if __name__ == "__main__":
    asyncio.run(main())
