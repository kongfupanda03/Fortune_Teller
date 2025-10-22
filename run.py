#!/usr/bin/env python3
"""
Main entry point for the Fortune Teller application.
Run this file to start the server.
"""

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    port = int(os.getenv("PORT", 3000))
    
    print("=" * 60)
    print("🔮 Constellation Fortune Teller - Starting Server")
    print("=" * 60)
    print(f"🚀 Server: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"📡 Health Check: http://localhost:{port}/api/health")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not found!")
        print("   Please add it to your .env file")
    
    if not os.getenv("DATABASE_URL"):
        print("⚠️  WARNING: Using default DATABASE_URL")
        print("   Set it in .env for production")
    
    print("\n✨ Press CTRL+C to stop the server\n")
    
    # Run the server
    uvicorn.run(
        "backend.server:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Auto-reload on code changes
    )

