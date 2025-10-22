#!/usr/bin/env python3
"""Simplified server for testing"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

# Import backend modules
from backend.database import get_db, engine, Base
from backend.models import User, ChatSession, ChatMessage, VerificationToken
from backend.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    ChatRequest, ChatResponse, ClearHistoryRequest, HealthResponse
)
from backend.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="Fortune Teller API", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    database_connected = False
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        database_connected = True
    except:
        pass
    
    return HealthResponse(
        status="ok",
        message="Fortune Teller API is running",
        hasApiKey=bool(os.getenv("OPENAI_API_KEY")),
        database_connected=database_connected
    )

@app.get("/")
async def read_root():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(backend_dir, "frontend")
    index_path = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_path)

@app.get("/{file_name}")
async def serve_frontend_files(file_name: str):
    if file_name not in ['style.css', 'script.js']:
        raise HTTPException(status_code=404, detail="File not found")
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(backend_dir, "frontend")
    file_path = os.path.join(frontend_dir, file_name)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    print(f"🔮 Fortune Teller server running on http://localhost:{port}")
    print(f"📡 API Health check: http://localhost:{port}/api/health")
    uvicorn.run(app, host="0.0.0.0", port=port)
