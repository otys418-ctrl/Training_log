"""
SQLAlchemy database models for L-DPS

IMPORTANT: This is an APPEND-ONLY, IMMUTABLE ledger.
Log entries CANNOT be updated or deleted once created.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class LogEntry(Base):
    """
    Immutable log entry for workout performance data.
    
    This table represents the single source of truth for all historical
    workout performance. Each row represents one completed set.
    
    PRD Reference: Section II.2 - L-DPS Data Model
    
    Constraints:
    - NO UPDATES allowed (append-only)
    - NO DELETES allowed (permanent record)
    - Timestamp auto-generated at creation (UTC)
    """
    __tablename__ = "log_entries"
    
    # Primary Key (UUID for distributed compatibility)
    log_entry_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core Required Fields (PRD Section II.2)
    user_id = Column(String, nullable=False, index=True)
    exercise_name = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    set_number = Column(Integer, nullable=False)
    weight_used = Column(Float, nullable=False)  # kg or lbs
    reps_completed = Column(Integer, nullable=False)
    
    # Optional Fields (PRD Section II.2 - "Other measurable insights")
    duration = Column(Integer, nullable=True)  # seconds
    distance = Column(Float, nullable=True)    # meters/km
    rpe = Column(Integer, nullable=True)       # Rate of Perceived Exertion (1-10)
    
    # Metadata (created_at only, no updated_at for immutability)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Composite index for efficient session queries
    # This index is critical for the "get latest session" query (PRD F.5.0)
    __table_args__ = (
        Index('idx_user_exercise_time', 'user_id', 'exercise_name', 'timestamp'),
    )
    
    def __repr__(self):
        return (
            f"<LogEntry(id={self.log_entry_id[:8]}, "
            f"user={self.user_id}, exercise={self.exercise_name}, "
            f"set={self.set_number}, weight={self.weight_used}kg, "
            f"reps={self.reps_completed})>"
        )
