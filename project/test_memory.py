#!/usr/bin/env python3
"""Test script for Agentcore Memory integration."""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import ProductHuntLaunchAgent

def test_memory_integration():
    """Test the memory integration with a simple conversation."""
    print("🧠 Testing Agentcore Memory Integration")
    print("=" * 50)
    
    try:
        # Create agent with memory
        agent = ProductHuntLaunchAgent()
        print(f"✅ Agent created with user ID: {agent.get_user_id()}")
        print(f"✅ Session ID: {agent.get_session_id()}")
        print(f"✅ Memory enabled: {agent.memory_hooks is not None}")
        
        # Test product memory seeding
        product_data = {
            "product_name": "TestApp",
            "product_type": "SaaS",
            "product_description": "A test application for Product Hunt launch",
            "target_audience": "developers",
            "launch_date": "next Tuesday",
            "additional_notes": "This is a test product"
        }
        
        print("\n📝 Seeding product memory...")
        success = agent.seed_product_memory(product_data)
        print(f"✅ Memory seeding: {'Success' if success else 'Failed'}")
        
        # Test memory summary
        print("\n🔍 Getting memory summary...")
        memory_summary = agent.get_memory_summary()
        print(f"✅ Total memories: {memory_summary.get('total_memories', 0)}")
        print(f"✅ Preferences: {len(memory_summary.get('preferences', []))}")
        print(f"✅ Semantic memories: {len(memory_summary.get('semantic', []))}")
        
        # Test conversation with memory
        print("\n💬 Testing conversation with memory...")
        response = agent.chat("What do you know about my product?")
        response_text = str(response) if hasattr(response, '__str__') else response
        print(f"✅ Agent response: {response_text[:100]}...")
        
        # Test follow-up conversation
        print("\n🔄 Testing follow-up conversation...")
        follow_up = agent.chat("Can you help me create a launch timeline?")
        follow_up_text = str(follow_up) if hasattr(follow_up, '__str__') else follow_up
        print(f"✅ Follow-up response: {follow_up_text[:100]}...")
        
        print("\n🎉 Memory integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during memory test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_integration()
