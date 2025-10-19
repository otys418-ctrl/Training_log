"""
Unit tests for session clustering algorithm

Tests the critical F.5.0 requirement: identifying the most recent session
"""

import pytest
from datetime import datetime, timedelta
from models.db_models import LogEntry
from utils.session_clustering import get_latest_session_from_logs, cluster_logs_into_sessions


def create_mock_log(user_id, exercise, set_num, timestamp, weight=100, reps=10):
    """Helper to create mock LogEntry objects"""
    log = LogEntry(
        log_entry_id=f"log-{set_num}-{timestamp.timestamp()}",
        user_id=user_id,
        exercise_name=exercise,
        set_number=set_num,
        weight_used=weight,
        reps_completed=reps,
        timestamp=timestamp
    )
    return log


class TestGetLatestSession:
    """Tests for get_latest_session_from_logs function"""
    
    def test_empty_logs(self):
        """Should return empty list when no logs provided"""
        result = get_latest_session_from_logs([])
        assert result == []
    
    def test_single_set(self):
        """Should return single set when only one log exists"""
        now = datetime.utcnow()
        logs = [create_mock_log("user1", "Squat", 1, now)]
        
        result = get_latest_session_from_logs(logs)
        
        assert len(result) == 1
        assert result[0].set_number == 1
    
    def test_multiple_sets_same_session(self):
        """Should return all sets from a single session"""
        now = datetime.utcnow()
        logs = [
            create_mock_log("user1", "Squat", 3, now - timedelta(minutes=10)),
            create_mock_log("user1", "Squat", 2, now - timedelta(minutes=15)),
            create_mock_log("user1", "Squat", 1, now - timedelta(minutes=20)),
        ]
        # Note: logs must be DESC order (newest first)
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        result = get_latest_session_from_logs(logs_desc)
        
        assert len(result) == 3
        # Should be sorted by set_number
        assert result[0].set_number == 1
        assert result[1].set_number == 2
        assert result[2].set_number == 3
    
    def test_two_sessions_different_days(self):
        """Should return only most recent session"""
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        
        logs = [
            # Today's session (most recent)
            create_mock_log("user1", "Squat", 2, now - timedelta(minutes=5), weight=110),
            create_mock_log("user1", "Squat", 1, now - timedelta(minutes=10), weight=110),
            # Yesterday's session (should NOT be returned)
            create_mock_log("user1", "Squat", 3, yesterday - timedelta(minutes=5), weight=100),
            create_mock_log("user1", "Squat", 2, yesterday - timedelta(minutes=10), weight=100),
            create_mock_log("user1", "Squat", 1, yesterday - timedelta(minutes=15), weight=100),
        ]
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        result = get_latest_session_from_logs(logs_desc)
        
        # Should only get today's session (2 sets)
        assert len(result) == 2
        assert result[0].weight_used == 110  # Today's weight
        assert result[1].weight_used == 110
    
    def test_session_boundary_detection(self):
        """Should correctly identify session boundary with 2-hour gap"""
        now = datetime.utcnow()
        
        logs = [
            # Session 1 (most recent) - 10:00-10:15
            create_mock_log("user1", "Bench", 2, now - timedelta(hours=0, minutes=0)),
            create_mock_log("user1", "Bench", 1, now - timedelta(hours=0, minutes=15)),
            # 3-hour gap here (exceeds 2-hour threshold)
            # Session 2 (older) - 7:00-7:10
            create_mock_log("user1", "Bench", 2, now - timedelta(hours=3, minutes=15)),
            create_mock_log("user1", "Bench", 1, now - timedelta(hours=3, minutes=25)),
        ]
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        result = get_latest_session_from_logs(logs_desc, timedelta(hours=2))
        
        # Should only get Session 1 (2 sets)
        assert len(result) == 2
        assert result[0].set_number == 1
        assert result[1].set_number == 2
    
    def test_exactly_two_hour_gap(self):
        """Should treat exactly 2-hour gap as same session"""
        now = datetime.utcnow()
        
        logs = [
            create_mock_log("user1", "Deadlift", 2, now),
            create_mock_log("user1", "Deadlift", 1, now - timedelta(hours=2)),  # Exactly 2 hours
        ]
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        result = get_latest_session_from_logs(logs_desc, timedelta(hours=2))
        
        # Should be considered same session
        assert len(result) == 2
    
    def test_custom_threshold(self):
        """Should respect custom session threshold"""
        now = datetime.utcnow()
        
        logs = [
            create_mock_log("user1", "Press", 2, now),
            create_mock_log("user1", "Press", 1, now - timedelta(minutes=45)),  # 45-min gap
        ]
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        # With 30-min threshold, should be 2 sessions
        result_30min = get_latest_session_from_logs(logs_desc, timedelta(minutes=30))
        assert len(result_30min) == 1  # Only most recent set
        
        # With 60-min threshold, should be 1 session
        result_60min = get_latest_session_from_logs(logs_desc, timedelta(minutes=60))
        assert len(result_60min) == 2  # Both sets


class TestClusterLogsIntoSessions:
    """Tests for cluster_logs_into_sessions function"""
    
    def test_multiple_sessions(self):
        """Should correctly cluster logs into multiple sessions"""
        now = datetime.utcnow()
        
        logs = [
            # Session 1 (most recent)
            create_mock_log("user1", "Squat", 2, now),
            create_mock_log("user1", "Squat", 1, now - timedelta(minutes=10)),
            # Session 2 (yesterday)
            create_mock_log("user1", "Squat", 3, now - timedelta(days=1)),
            create_mock_log("user1", "Squat", 2, now - timedelta(days=1, minutes=5)),
            create_mock_log("user1", "Squat", 1, now - timedelta(days=1, minutes=10)),
        ]
        logs_desc = sorted(logs, key=lambda x: x.timestamp, reverse=True)
        
        sessions = cluster_logs_into_sessions(logs_desc)
        
        assert len(sessions) == 2
        assert len(sessions[0]) == 2  # Most recent session: 2 sets
        assert len(sessions[1]) == 3  # Older session: 3 sets


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
