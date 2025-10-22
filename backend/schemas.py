"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Chat schemas
class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None
    zodiacSign: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sessionId: str


class ClearHistoryRequest(BaseModel):
    sessionId: str


# Health check
class HealthResponse(BaseModel):
    status: str
    message: str
    hasApiKey: bool
    database_connected: bool

