"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class LogEntryBase(BaseModel):
    """Base schema for log entry data"""
    user_id: str = Field(..., description="User identifier")
    exercise_name: str = Field(..., description="Exercise name (case-sensitive)")
    set_number: int = Field(..., ge=1, description="Set number (1-based)")
    weight_used: float = Field(..., ge=0, description="Weight used in kg or lbs")
    reps_completed: int = Field(..., ge=0, description="Number of reps completed")
    duration: Optional[int] = Field(None, ge=0, description="Duration in seconds")
    distance: Optional[float] = Field(None, ge=0, description="Distance in meters/km")
    rpe: Optional[int] = Field(None, ge=1, le=10, description="Rate of Perceived Exertion (1-10)")


class LogEntryCreate(LogEntryBase):
    """Schema for creating a log entry (PRD F.3.0)"""
    pass


class LogEntryResponse(LogEntryBase):
    """Schema for log entry response"""
    log_entry_id: str
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class SetData(BaseModel):
    """Individual set data for session reference"""
    set_number: int
    weight_used: float
    reps_completed: int
    duration: Optional[int] = None
    distance: Optional[float] = None
    rpe: Optional[int] = None
    timestamp: datetime


class SessionReferenceResponse(BaseModel):
    """
    Response for the 'latest session' query (PRD F.5.0)
    
    This contains ALL sets from the single most recent session
    of a specific exercise, enabling Progressive Overload tracking.
    """
    user_id: str
    exercise_name: str
    session_timestamp: datetime = Field(..., description="Timestamp of first set in session")
    sets: List[SetData] = Field(default=[], description="All sets from the session, ordered by set_number")
    total_sets: int
    
    class Config:
        from_attributes = True


class ExerciseHistoryResponse(BaseModel):
    """Response for complete exercise history"""
    user_id: str
    exercise_name: str
    total_entries: int
    entries: List[LogEntryResponse]
