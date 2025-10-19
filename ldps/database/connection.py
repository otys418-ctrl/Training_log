"""
Database connection and session management for L-DPS

IMPORTANT: This is INDEPENDENT from P-MIS.
- Separate database file (ldps.db)
- No shared connections
- Can run on different port
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.db_models import Base
import os
from pathlib import Path

# Database URL - using SQLite for development, PostgreSQL-ready for production
# Use absolute path to avoid issues with working directory changes
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/ldps.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize database tables.
    
    Creates the log_entries table with all indexes.
    Safe to call multiple times (idempotent).
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Dependency for getting database sessions.
    
    Usage in FastAPI:
        @app.post("/logs")
        def create_log(log: LogEntryCreate, db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
