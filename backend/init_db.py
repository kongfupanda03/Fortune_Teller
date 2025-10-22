"""Initialize the database - create all tables"""

from backend.database import engine, Base
from backend.models import User, ChatSession, ChatMessage

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_database()

