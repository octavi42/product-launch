#!/usr/bin/env python3
"""Test script to verify agent functionality."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

try:
    print("🧪 Testing Product Hunt Launch Agent...")

    # Test imports
    print("📦 Testing imports...")
    from src.agent import ProductHuntLaunchAgent
    print("✅ Agent import successful")

    from src.tools.product_tools import generate_launch_timeline, generate_marketing_assets, research_top_launches
    print("✅ Tools import successful")

    # Test agent initialization
    print("🤖 Testing agent initialization...")
    agent = ProductHuntLaunchAgent()
    print("✅ Agent initialized successfully")

    # Test simple chat
    print("💬 Testing simple chat...")
    response = agent.chat("Hello! Can you help me with Product Hunt?")
    print(f"✅ Chat response: {response[:100]}...")

    print("\n🎉 All tests passed! Agent is working correctly.")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)