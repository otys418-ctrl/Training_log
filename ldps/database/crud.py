"""
CRUD operations for L-DPS

CRITICAL: This module enforces the APPEND-ONLY, IMMUTABLE nature of L-DPS.
- CREATE operations only
- NO UPDATE operations
- NO DELETE operations
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import timedelta
from models.db_models import LogEntry
from models.schemas import LogEntryResponse, SessionReferenceResponse, SetData
from utils.session_clustering import get_latest_session_from_logs, DEFAULT_SESSION_THRESHOLD
import uuid


def create_log_entry(db: Session, log_data: Dict[str, Any]) -> LogEntry:
    """
    Create a new log entry (PRD F.3.0, F.4.0).
    
    This is the ONLY write operation allowed in L-DPS.
    Logs are immutable once created.
    
    Args:
        db: Database session
        log_data: Dictionary containing log entry data
    
    Returns:
        Created LogEntry object with auto-generated timestamp
    
    Raises:
        IntegrityError: If duplicate log_entry_id (extremely rare with UUIDs)
    """
    log_entry = LogEntry(
        log_entry_id=str(uuid.uuid4()),
        user_id=log_data["user_id"],
        exercise_name=log_data["exercise_name"],
        set_number=log_data["set_number"],
        weight_used=log_data["weight_used"],
        reps_completed=log_data["reps_completed"],
        duration=log_data.get("duration"),
        distance=log_data.get("distance"),
        rpe=log_data.get("rpe")
    )
    
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    return log_entry


def get_latest_session(
    db: Session,
    user_id: str,
    exercise_name: str,
    session_threshold_hours: float = 2.0
) -> Optional[SessionReferenceResponse]:
    """
    Retrieve the most recent session for a specific exercise (PRD F.5.0).
    
    This is THE CRITICAL QUERY for Progressive Overload tracking.
    Returns ALL sets from the single most recent session.
    
    Algorithm:
    1. Query all logs for user + exercise, ordered by timestamp DESC
    2. Apply session clustering algorithm
    3. Return the most recent complete session
    
    Args:
        db: Database session
        user_id: User identifier
        exercise_name: Exercise name (case-sensitive)
        session_threshold_hours: Hours between sets indicating new session
    
    Returns:
        SessionReferenceResponse with all sets from latest session
        None if no previous session found
    
    Example Response:
        {
            "user_id": "user_123",
            "exercise_name": "Leg Press",
            "session_timestamp": "2025-10-15T10:05:00Z",
            "sets": [
                {"set_number": 1, "weight_used": 100.0, "reps_completed": 10, ...},
                {"set_number": 2, "weight_used": 105.0, "reps_completed": 8, ...},
                {"set_number": 3, "weight_used": 100.0, "reps_completed": 10, ...}
            ],
            "total_sets": 3
        }
    """
    # Step 1: Get all logs for this user + exercise, ordered by timestamp DESC
    all_logs = db.query(LogEntry)\
        .filter(
            LogEntry.user_id == user_id,
            LogEntry.exercise_name == exercise_name
        )\
        .order_by(LogEntry.timestamp.desc())\
        .all()
    
    if not all_logs:
        return None
    
    # Step 2: Apply session clustering algorithm
    session_threshold = timedelta(hours=session_threshold_hours)
    latest_session_logs = get_latest_session_from_logs(all_logs, session_threshold)
    
    if not latest_session_logs:
        return None
    
    # Step 3: Build response
    sets = [
        SetData(
            set_number=log.set_number,
            weight_used=log.weight_used,
            reps_completed=log.reps_completed,
            duration=log.duration,
            distance=log.distance,
            rpe=log.rpe,
            timestamp=log.timestamp
        )
        for log in latest_session_logs
    ]
    
    return SessionReferenceResponse(
        user_id=user_id,
        exercise_name=exercise_name,
        session_timestamp=latest_session_logs[0].timestamp,  # First set timestamp
        sets=sets,
        total_sets=len(sets)
    )


def get_exercise_history(
    db: Session,
    user_id: str,
    exercise_name: Optional[str] = None,
    limit: int = 100
) -> List[LogEntryResponse]:
    """
    Retrieve complete exercise history for a user.
    
    Optional for analytics, not required for core MVP.
    
    Args:
        db: Database session
        user_id: User identifier
        exercise_name: Optional filter by exercise name
        limit: Maximum number of entries to return
    
    Returns:
        List of LogEntryResponse objects, ordered by timestamp DESC
    """
    query = db.query(LogEntry).filter(LogEntry.user_id == user_id)
    
    if exercise_name:
        query = query.filter(LogEntry.exercise_name == exercise_name)
    
    logs = query.order_by(LogEntry.timestamp.desc()).limit(limit).all()
    
    return [
        LogEntryResponse(
            log_entry_id=log.log_entry_id,
            user_id=log.user_id,
            exercise_name=log.exercise_name,
            set_number=log.set_number,
            weight_used=log.weight_used,
            reps_completed=log.reps_completed,
            duration=log.duration,
            distance=log.distance,
            rpe=log.rpe,
            timestamp=log.timestamp,
            created_at=log.created_at
        )
        for log in logs
    ]


# =============================================================================
# FORBIDDEN OPERATIONS - These enforce immutability
# =============================================================================

def update_log_entry(*args, **kwargs):
    """
    FORBIDDEN: Log entries are immutable.
    
    Raises:
        NotImplementedError: Always
    """
    raise NotImplementedError(
        "Log entries cannot be updated. L-DPS is append-only. "
        "To correct a mistake, delete and re-log the entry (future feature)."
    )


def delete_log_entry(*args, **kwargs):
    """
    FORBIDDEN: Log entries are immutable.
    
    Note: Future implementation may allow soft-deletes for user corrections,
    but this would be a separate audit-logged operation, not a direct delete.
    
    Raises:
        NotImplementedError: Always
    """
    raise NotImplementedError(
        "Log entries cannot be deleted. L-DPS is an immutable ledger. "
        "Contact system administrator if data correction is required."
    )
