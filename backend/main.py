#!/usr/bin/env python3
"""
Resume Scanner Backend - Development Server
For production, use: uvicorn src.infrastructure.web.fastapi_app:app
"""

import os
import sys
import uvicorn

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
try:
    from src.infrastructure.web.fastapi_app import app
    print("✅ FastAPI app imported successfully")
except ImportError as e:
    print(f"❌ Failed to import FastAPI app: {e}")
    print("Note: This is expected in WebContainer environment")
    print("In production, install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Resume Scanner Backend Server")
    print("📋 Hexagonal Architecture Implementation")
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print()
    
    # Run with uvicorn
    uvicorn.run(
        "src.infrastructure.web.fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )