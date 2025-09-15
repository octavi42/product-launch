#!/usr/bin/env python3
"""
Run the Product Hunt Launch Assistant web application.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    import uvicorn
    from api.main import app

    def main():
        print("🚀 Starting Product Hunt Launch Assistant Web App")
        print("=" * 50)
        print("📱 Web Interface: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("🔧 Admin Panel: http://localhost:8000/redoc")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print()

        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Please install requirements: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Failed to start web app: {e}")
    sys.exit(1)