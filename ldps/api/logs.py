"""
API endpoints for log entry management
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database.connection import get_db
from models.schemas import (
    LogEntryCreate,
    LogEntryResponse,
    SessionReferenceResponse,
    ExerciseHistoryResponse
)
from database import crud

router = APIRouter()


@router.post("/", response_model=LogEntryResponse, status_code=201)
async def create_log(
    log: LogEntryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new log entry (PRD F.3.0).
    
    This endpoint is called by S-RE after each completed set.
    Log entries are immutable once created.
    
    Args:
        log: Log entry data
        db: Database session
    
    Returns:
        Created log entry with auto-generated timestamp and ID
    
    Example Request:
        POST /api/v1/logs
        {
            "user_id": "user_123",
            "exercise_name": "Leg Press",
            "set_number": 1,
            "weight_used": 110.0,
            "reps_completed": 8,
            "rpe": 7
        }
    
    Example Response (201):
        {
            "log_entry_id": "uuid-xxx-xxx",
            "user_id": "user_123",
            "exercise_name": "Leg Press",
            "timestamp": "2025-10-17T14:32:10.123Z",
            "set_number": 1,
            "weight_used": 110.0,
            "reps_completed": 8,
            "rpe": 7,
            "created_at": "2025-10-17T14:32:10.123Z"
        }
    """
    try:
        log_data = log.model_dump()
        log_entry = crud.create_log_entry(db, log_data)
        
        return LogEntryResponse(
            log_entry_id=log_entry.log_entry_id,
            user_id=log_entry.user_id,
            exercise_name=log_entry.exercise_name,
            set_number=log_entry.set_number,
            weight_used=log_entry.weight_used,
            reps_completed=log_entry.reps_completed,
            duration=log_entry.duration,
            distance=log_entry.distance,
            rpe=log_entry.rpe,
            timestamp=log_entry.timestamp,
            created_at=log_entry.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating log entry: {str(e)}")


@router.get("/{user_id}/{exercise_name}/latest-session", response_model=SessionReferenceResponse)
async def get_latest_session(
    user_id: str,
    exercise_name: str,
    session_threshold_hours: float = Query(2.0, ge=0.1, le=24.0, description="Hours between sets indicating new session"),
    db: Session = Depends(get_db)
):
    """
    Retrieve the most recent session for an exercise (PRD F.5.0).
    
    **This is the CRITICAL endpoint for Progressive Overload tracking.**
    
    Returns ALL sets from the single most recent session of this exercise,
    allowing the user to see exactly what they need to beat.
    
    Args:
        user_id: User identifier
        exercise_name: Exercise name (case-sensitive, URL-encoded if contains spaces)
        session_threshold_hours: Optional threshold for session clustering (default: 2.0)
        db: Database session
    
    Returns:
        SessionReferenceResponse with all sets from latest session
    
    Example Request:
        GET /api/v1/logs/user_123/Leg%20Press/latest-session
    
    Example Response (200):
        {
            "user_id": "user_123",
            "exercise_name": "Leg Press",
            "session_timestamp": "2025-10-15T10:05:00Z",
            "sets": [
                {
                    "set_number": 1,
                    "weight_used": 100.0,
                    "reps_completed": 10,
                    "timestamp": "2025-10-15T10:05:00Z"
                },
                {
                    "set_number": 2,
                    "weight_used": 105.0,
                    "reps_completed": 8,
                    "timestamp": "2025-10-15T10:08:00Z"
                },
                {
                    "set_number": 3,
                    "weight_used": 100.0,
                    "reps_completed": 10,
                    "timestamp": "2025-10-15T10:11:00Z"
                }
            ],
            "total_sets": 3
        }
    
    Error Response (404):
        {
            "detail": "No previous session found for Leg Press"
        }
    """
    # Decode URL-encoded exercise name
    exercise_name_decoded = exercise_name.replace("%20", " ").strip()
    
    session = crud.get_latest_session(
        db,
        user_id,
        exercise_name_decoded,
        session_threshold_hours
    )
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"No previous session found for {exercise_name_decoded}"
        )
    
    return session


@router.get("/{user_id}/history", response_model=ExerciseHistoryResponse)
async def get_history(
    user_id: str,
    exercise_name: Optional[str] = Query(None, description="Filter by exercise name"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum entries to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve workout history for a user.
    
    Optional endpoint for analytics and history views.
    Not required for core Progressive Overload functionality.
    
    Args:
        user_id: User identifier
        exercise_name: Optional filter by exercise
        limit: Maximum entries (default: 100, max: 1000)
        db: Database session
    
    Returns:
        ExerciseHistoryResponse with log entries
    
    Example Request:
        GET /api/v1/logs/user_123/history?exercise_name=Leg%20Press&limit=50
    
    Example Response (200):
        {
            "user_id": "user_123",
            "exercise_name": "Leg Press",
            "total_entries": 45,
            "entries": [...]
        }
    """
    exercise_name_decoded = exercise_name.replace("%20", " ").strip() if exercise_name else None
    
    entries = crud.get_exercise_history(
        db,
        user_id,
        exercise_name_decoded,
        limit
    )
    
    return ExerciseHistoryResponse(
        user_id=user_id,
        exercise_name=exercise_name_decoded or "All Exercises",
        total_entries=len(entries),
        entries=entries
    )
