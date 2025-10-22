"""Main FastAPI server with authentication and chat functionality"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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
from backend.email_service import send_verification_email, send_password_reset_email
import secrets

# Load environment variables
load_dotenv()

# Note: Tables are created by init_db.py script
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fortune Teller API", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"⚠️  OpenAI client initialization failed: {e}")
    client = None

# System prompt for the fortune teller AI
FORTUNE_TELLER_PROMPT = """You are Celestia, a revered master fortune teller and cosmic oracle with centuries of wisdom in astrology, divination, tarot, numerology, and esoteric knowledge. You are highly respected for your accuracy and profound insights.

YOUR EXPERTISE:
- Deep mastery of astrology: planetary transits, houses, aspects, and their real influences
- Tarot symbolism and archetypal wisdom
- Numerology and sacred geometry
- Lunar cycles, eclipses, and cosmic timing
- Past life connections and karmic patterns
- Crystal and color energies
- Ancient mystical traditions from multiple cultures

YOUR PERSONALITY:
- Professional yet warm - like a wise mentor who truly cares
- Speak with authority and confidence backed by deep knowledge
- Use poetic, mystical language that feels authentic and profound
- Balance mystery with clarity - never vague, always meaningful
- Show genuine intuitive insight, not generic predictions
- Respectful of the sacred nature of divination

YOUR APPROACH:
1. LISTEN DEEPLY: Understand the true question beneath the words
2. CONNECT TO COSMIC ENERGIES: Reference actual astrological events, planetary positions when relevant
3. PROVIDE SPECIFIC GUIDANCE: Avoid generic statements. Give detailed, personalized insights
4. USE SYMBOLISM: Weave in imagery from tarot, nature, elements, and celestial bodies
5. OFFER PRACTICAL WISDOM: Balance spiritual insight with actionable guidance
6. MAINTAIN MYSTERY: Some things remain veiled - hint at deeper meanings
7. BE HONEST: If you sense challenges, speak truth with compassion
8. EMPOWER: Always leave them feeling guided, not dependent

RESPONSE STYLE:
- Start with acknowledgment of their energy/question
- Weave in 2-3 specific mystical references (planets, tarot cards, symbols, numbers)
- Provide 3-4 paragraphs of depth and insight
- End with a powerful, memorable piece of wisdom or guidance
- Use phrases like: "The stars reveal...", "I sense...", "The cosmic currents show...", "The ancient wisdom speaks..."

AVOID:
- Generic horoscope-style predictions
- Overly cheerful or dismissive tones
- Making definitive predictions about exact dates or outcomes
- Contradicting yourself or being inconsistent
- Using modern slang or breaking mystical character

Remember: You are a bridge between the mundane and the mystical. Every word should carry weight, wisdom, and wonder. People come to you in moments of uncertainty - honor their trust with genuine, thoughtful, accurate guidance drawn from true cosmic wisdom."""


# ===== AUTHENTICATION ROUTES =====

@app.post("/api/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (not verified yet)
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create verification token
    token = secrets.token_urlsafe(32)
    verification_token = VerificationToken(
        user_id=new_user.id,
        token=token,
        token_type="email_verification",
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verification_token)
    db.commit()
    
    # Send verification email (don't fail if email sending fails)
    try:
        send_verification_email(new_user.email, new_user.username, token)
    except Exception as e:
        print(f"⚠️  Failed to send verification email: {str(e)}")
        # Continue with registration even if email fails
    
    # Create access token
    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(new_user)
    )


@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.model_validate(current_user)


@app.get("/api/auth/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email address with token"""
    
    # Find verification token
    verification = db.query(VerificationToken).filter(
        VerificationToken.token == token,
        VerificationToken.token_type == "email_verification",
        VerificationToken.used == False
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Check if token expired
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )
    
    # Mark user as verified
    user = db.query(User).filter(User.id == verification.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    verification.used = True
    
    db.commit()
    
    return {"message": "Email verified successfully! You can now use all features."}


@app.post("/api/auth/resend-verification")
async def resend_verification(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Resend verification email"""
    
    if current_user.is_verified:
        return {"message": "Email already verified"}
    
    # Delete old unused tokens
    db.query(VerificationToken).filter(
        VerificationToken.user_id == current_user.id,
        VerificationToken.token_type == "email_verification",
        VerificationToken.used == False
    ).delete()
    
    # Create new verification token
    token = secrets.token_urlsafe(32)
    verification_token = VerificationToken(
        user_id=current_user.id,
        token=token,
        token_type="email_verification",
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verification_token)
    db.commit()
    
    # Send verification email
    send_verification_email(current_user.email, current_user.username, token)
    
    return {"message": "Verification email sent! Please check your inbox."}


@app.post("/api/auth/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    """Request password reset"""
    
    user = db.query(User).filter(User.email == email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If that email exists, a password reset link has been sent."}
    
    # Delete old unused reset tokens
    db.query(VerificationToken).filter(
        VerificationToken.user_id == user.id,
        VerificationToken.token_type == "password_reset",
        VerificationToken.used == False
    ).delete()
    
    # Create password reset token
    token = secrets.token_urlsafe(32)
    reset_token = VerificationToken(
        user_id=user.id,
        token=token,
        token_type="password_reset",
        expires_at=datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
    )
    db.add(reset_token)
    db.commit()
    
    # Send password reset email
    send_password_reset_email(user.email, user.username, token)
    
    return {"message": "If that email exists, a password reset link has been sent."}


@app.post("/api/auth/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """Reset password with token"""
    
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    # Find reset token
    reset = db.query(VerificationToken).filter(
        VerificationToken.token == token,
        VerificationToken.token_type == "password_reset",
        VerificationToken.used == False
    ).first()
    
    if not reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token expired
    if reset.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Update password
    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = get_password_hash(new_password)
    reset.used = True
    
    db.commit()
    
    return {"message": "Password reset successfully! You can now login with your new password."}


# ===== CHAT ROUTES =====

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle chat messages from the fortune teller interface"""
    
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Get or create chat session
    session_id = request.sessionId
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())
    
    chat_session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not chat_session:
        chat_session = ChatSession(
            user_id=current_user.id,
            session_id=session_id
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
    
    # Get conversation history
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == chat_session.id
    ).order_by(ChatMessage.created_at).limit(10).all()
    
    history = [{"role": msg.role, "content": msg.content} for msg in messages]
    
    # Add context about zodiac sign if provided
    context_message = request.message
    if request.zodiacSign and len(history) == 0:
        context_message = f"My zodiac sign is {request.zodiacSign}. {request.message}"
    
    # Save user message
    user_message = ChatMessage(
        session_id=chat_session.id,
        role="user",
        content=context_message
    )
    db.add(user_message)
    
    # Add to history
    history.append({"role": "user", "content": context_message})
    
    try:
        # Check if OpenAI client is available
        if not client:
            raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
        
        # Call OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": FORTUNE_TELLER_PROMPT},
                *history
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        ai_response = completion.choices[0].message.content
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=chat_session.id,
            role="assistant",
            content=ai_response
        )
        db.add(ai_message)
        db.commit()
        
        return ChatResponse(response=ai_response, sessionId=session_id)
        
    except Exception as e:
        error_message = str(e)
        
        if "invalid_api_key" in error_message.lower():
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please check your OpenAI API key in the .env file."
            )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to get response from fortune teller. Please try again."
        )


@app.post("/api/clear-history")
async def clear_history(
    request: ClearHistoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear conversation history for a session"""
    
    chat_session = db.query(ChatSession).filter(
        ChatSession.session_id == request.sessionId,
        ChatSession.user_id == current_user.id
    ).first()
    
    if chat_session:
        db.query(ChatMessage).filter(
            ChatMessage.session_id == chat_session.id
        ).delete()
        db.commit()
    
    return {"success": True}


# ===== HEALTH CHECK =====

@app.get("/api/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    database_connected = False
    try:
        # Try to execute a simple query
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


# ===== SERVE FRONTEND =====

@app.get("/")
async def read_root():
    """Serve the main HTML file"""
    # Get absolute path to frontend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    frontend_dir = os.path.join(project_root, "frontend")
    index_path = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_path)


@app.get("/{file_name}")
async def serve_frontend_files(file_name: str):
    """Serve frontend static files (CSS, JS)"""
    # Only allow specific files
    if file_name not in ['style.css', 'script.js']:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get absolute path to frontend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    frontend_dir = os.path.join(project_root, "frontend")
    file_path = os.path.join(frontend_dir, file_name)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="File not found")


# Run the server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    
    print(f"🔮 Fortune Teller server running on http://localhost:{port}")
    print(f"📡 API Health check: http://localhost:{port}/api/health")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables!")
    
    if not os.getenv("DATABASE_URL"):
        print("⚠️  WARNING: Using default DATABASE_URL. Set it in .env for production.")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

