#!/usr/bin/env python3
"""
Simple test for Strands Agents implementation
"""

import asyncio
import os
from app.strands_agents import ProductHuntCoordinator


async def test_strands_agents():
    """Test Strands agents with simple requests"""
    print("🧪 Testing Strands Agents Implementation")
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
        print("✅ Strands coordinator initialized")
        
        # Test planning agent
        print("\n🔍 Testing Planning Agent...")
        planning_result = await coordinator.route_request("planning", {
            "product_name": "TestApp",
            "product_type": "SaaS",
            "launch_date": "next Friday",
            "additional_notes": "Focus on developer tools"
        })
        print(f"Planning result: {planning_result.get('success', False)}")
        if not planning_result.get('success'):
            print(f"Error: {planning_result.get('error')}")
        
        # Test asset prep agent
        print("\n✍️ Testing Asset Prep Agent...")
        asset_result = await coordinator.route_request("asset_prep", {
            "product_name": "TestApp",
            "elevator_pitch": "AI-powered development tool for modern teams",
            "target_audience": "Software developers",
            "tone": "professional"
        })
        print(f"Asset prep result: {asset_result.get('success', False)}")
        if not asset_result.get('success'):
            print(f"Error: {asset_result.get('error')}")
        
        # Test research agent
        print("\n🔍 Testing Research Agent...")
        research_result = await coordinator.route_request("research", {
            "product_category": "Developer Tools",
            "target_audience": "Software developers",
            "budget_range": "Under $500"
        })
        print(f"Research result: {research_result.get('success', False)}")
        if not research_result.get('success'):
            print(f"Error: {research_result.get('error')}")
        
        # Check all results
        all_success = all([
            planning_result.get('success', False),
            asset_result.get('success', False),
            research_result.get('success', False)
        ])
        
        if all_success:
            print("\n🎉 All Strands agents working correctly!")
            return True
        else:
            print("\n❌ Some agents failed. Check the results above.")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Main test function"""
    success = await test_strands_agents()
    
    if success:
        print("\n✅ Strands implementation is ready for your hackathon!")
        print("Run 'make run' to start the application.")
    else:
        print("\n❌ There are issues with the Strands implementation.")
        print("Check your AWS configuration and dependencies.")


if __name__ == "__main__":
    asyncio.run(main())
