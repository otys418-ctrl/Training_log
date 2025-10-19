"""
Session clustering utility for identifying workout sessions.

PRD Reference: F.5.0 - Progressive Overload Reference
A "session" is defined as a cluster of log entries with close timestamps.
"""

from datetime import timedelta
from typing import List
from models.db_models import LogEntry

# Default threshold: 2 hours between sets indicates new session
DEFAULT_SESSION_THRESHOLD = timedelta(hours=2)


def get_latest_session_from_logs(
    all_logs: List[LogEntry],
    session_threshold: timedelta = DEFAULT_SESSION_THRESHOLD
) -> List[LogEntry]:
    """
    Extract the most recent session from a list of log entries.
    
    Algorithm:
    1. Logs must be sorted by timestamp DESC (newest first)
    2. Iterate through logs, detecting session boundaries
    3. A gap > threshold indicates a new session boundary
    4. Return the first (most recent) complete session
    
    Args:
        all_logs: List of LogEntry objects, ordered by timestamp DESC
        session_threshold: Maximum time gap between sets in same session
    
    Returns:
        List of LogEntry objects from most recent session, sorted by set_number
        Empty list if no logs provided
    
    Example:
        Logs at: [10:00, 10:05, 10:10] -> Same session (5-min gaps)
        Logs at: [10:00, 10:05, 13:00] -> Two sessions (3-hour gap)
        
        Latest session would be the first cluster: [10:00, 10:05]
    """
    if not all_logs:
        return []
    
    # Session clustering algorithm
    sessions = []
    current_session = [all_logs[0]]
    
    for i in range(1, len(all_logs)):
        prev_log = all_logs[i - 1]
        curr_log = all_logs[i]
        
        # Calculate time gap between consecutive logs
        # Note: all_logs is DESC order, so prev_log.timestamp > curr_log.timestamp
        time_gap = prev_log.timestamp - curr_log.timestamp
        
        if time_gap <= session_threshold:
            # Still in the same session
            current_session.append(curr_log)
        else:
            # Session boundary detected - save current session and start new one
            sessions.append(current_session)
            current_session = [curr_log]
    
    # Don't forget the last session
    sessions.append(current_session)
    
    # Return the most recent session (first in list), sorted by set number
    latest_session = sessions[0]
    return sorted(latest_session, key=lambda x: x.set_number)


def cluster_logs_into_sessions(
    all_logs: List[LogEntry],
    session_threshold: timedelta = DEFAULT_SESSION_THRESHOLD
) -> List[List[LogEntry]]:
    """
    Cluster all logs into distinct sessions.
    
    Useful for analytics and history views showing multiple sessions.
    
    Args:
        all_logs: List of LogEntry objects, ordered by timestamp DESC
        session_threshold: Maximum time gap between sets in same session
    
    Returns:
        List of sessions, each session is a list of LogEntry objects
        Sessions ordered newest to oldest
    """
    if not all_logs:
        return []
    
    sessions = []
    current_session = [all_logs[0]]
    
    for i in range(1, len(all_logs)):
        prev_log = all_logs[i - 1]
        curr_log = all_logs[i]
        
        time_gap = prev_log.timestamp - curr_log.timestamp
        
        if time_gap <= session_threshold:
            current_session.append(curr_log)
        else:
            # Sort this session by set number before saving
            sessions.append(sorted(current_session, key=lambda x: x.set_number))
            current_session = [curr_log]
    
    # Add the last session
    sessions.append(sorted(current_session, key=lambda x: x.set_number))
    
    return sessions
