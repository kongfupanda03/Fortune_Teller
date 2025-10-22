"""Database configuration and connection management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - supports both SQLite and MySQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Default to SQLite if no DATABASE_URL is set
if not DATABASE_URL:
    # Get the absolute path to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(backend_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    
    # SQLite database file in backend/db/
    db_path = os.path.join(db_dir, "fortune_teller.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    print(f"📦 Using SQLite database at: {db_path}")
elif DATABASE_URL.startswith("mysql"):
    print(f"🐬 Using MySQL database")
else:
    print(f"🗄️ Using database: {DATABASE_URL}")

# Create engine with appropriate settings
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

