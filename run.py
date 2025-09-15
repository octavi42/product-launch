#!/usr/bin/env python3
"""
Product Hunt Launch Assistant
Run script for the application
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))


def main():
    """Run the Product Hunt Launch Assistant"""

    # Check for AWS credentials
    if not os.getenv('AWS_ACCESS_KEY_ID'):
        print("⚠️  Warning: AWS_ACCESS_KEY_ID not set")
        print("   Set your AWS credentials to use the Bedrock agents")
        print("   export AWS_ACCESS_KEY_ID=your_key")
        print("   export AWS_SECRET_ACCESS_KEY=your_secret")
        print("   export AWS_REGION=us-west-2")
        print()

    print("🚀 Starting Product Hunt Launch Assistant...")
    print("   Web Interface: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop")
    print()

    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
