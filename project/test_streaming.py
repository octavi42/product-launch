#!/usr/bin/env python3
"""Test streaming functionality to debug the issue."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

try:
    from src.agent import ProductHuntLaunchAgent

    print("🧪 Testing streaming functionality...")

    agent = ProductHuntLaunchAgent()

    print("🤖 Testing regular chat...")
    response = agent.chat("Hello, tell me about Product Hunt in one sentence.")
    print(f"Regular response type: {type(response)}")
    print(f"Regular response: {str(response)[:200]}...")

    print("\n🌊 Testing streaming chat...")
    try:
        chunks = []
        for chunk in agent.chat_stream("Hello, tell me about Product Hunt in one sentence."):
            chunk_str = str(chunk)
            chunks.append(chunk_str)
            print(f"Chunk type: {type(chunk)}, Content: {chunk_str[:50]}...")

        print(f"\nTotal chunks received: {len(chunks)}")

    except Exception as e:
        print(f"Streaming error: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()