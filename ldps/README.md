# L-DPS: Logbook & Data Persistence Service

**Version:** 1.0.0  
**Port:** 8001  
**Status:** ✅ Operational

---

## 📋 Overview

L-DPS is the **immutable, append-only ledger** for all workout performance data in the Progressive Overload Log application. It serves as the single source of truth for historical workout data, enabling users to track progressive overload by comparing current performance against previous sessions.

### Key Principles
- **Append-Only**: Log entries can only be created, never updated or deleted
- **Immutable**: Once logged, data becomes permanent historical record
- **Independent**: Zero coupling with P-MIS; runs on separate port and database
- **Session-Aware**: Intelligent clustering of sets into workout sessions

---

## 🏗️ Architecture

### PRD References
- **Section II.2**: L-DPS Module Definition
- **F.3.0**: Real-Time Logging
- **F.4.0**: Data Persistence
- **F.5.0**: Progressive Overload Reference (Critical Feature)

### Technology Stack
```
Framework: FastAPI 0.104.1
ORM: SQLAlchemy 2.0.23
Validation: Pydantic 2.5.0
Database: SQLite (dev) / PostgreSQL (prod)
Testing: pytest 7.4.3
Server: Uvicorn 0.24.0
```

### Directory Structure
```
ldps/
├── main.py                     # FastAPI application (port 8001)
├── requirements.txt            # Python dependencies
├── ldps.db                     # SQLite database (auto-generated)
├── api/
│   └── logs.py                 # API endpoints
├── database/
│   ├── connection.py           # DB engine & session management
│   └── crud.py                 # CRUD operations
├── models/
│   ├── db_models.py            # SQLAlchemy LogEntry model
│   └── schemas.py              # Pydantic request/response models
├── utils/
│   └── session_clustering.py  # Session detection algorithm
└── tests/
    └── test_session_clustering.py
```

---

## 🗄️ Database Schema

### LogEntry Table
```sql
CREATE TABLE log_entries (
    log_entry_id VARCHAR PRIMARY KEY,      -- UUID
    user_id VARCHAR NOT NULL,
    exercise_name VARCHAR NOT NULL,
    timestamp DATETIME NOT NULL,           -- Auto-generated (UTC)
    set_number INTEGER NOT NULL,
    weight_used FLOAT NOT NULL,            -- kg or lbs
    reps_completed INTEGER NOT NULL,
    
    -- Optional fields
    duration INTEGER NULL,                 -- seconds
    distance FLOAT NULL,                   -- meters/km
    rpe INTEGER NULL,                      -- Rate of Perceived Exertion (1-10)
    
    created_at DATETIME NOT NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_exercise_name (exercise_name),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_exercise_time (user_id, exercise_name, timestamp)
);
```

**Key Constraints:**
- No `updated_at` field (immutable)
- Composite index for fast session queries
- UUID primary keys for distributed compatibility

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8001/api/v1/logs
```

### 1. **POST /** - Create Log Entry
**PRD Requirement:** F.3.0, F.4.0

Creates a new log entry after a set is completed.

**Request:**
```json
{
  "user_id": "user_123",
  "exercise_name": "Leg Press",
  "set_number": 1,
  "weight_used": 110.0,
  "reps_completed": 8,
  "rpe": 7
}
```

**Response (201):**
```json
{
  "log_entry_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "exercise_name": "Leg Press",
  "timestamp": "2025-10-17T14:32:10.123Z",
  "set_number": 1,
  "weight_used": 110.0,
  "reps_completed": 8,
  "rpe": 7,
  "created_at": "2025-10-17T14:32:10.123Z"
}
```

---

### 2. **GET /{user_id}/{exercise_name}/latest-session** - Get Reference Data
**PRD Requirement:** F.5.0 (CRITICAL)

Retrieves ALL sets from the most recent session of a specific exercise. This is the core Progressive Overload feature.

**Request:**
```
GET /api/v1/logs/user_123/Leg%20Press/latest-session?session_threshold_hours=2.0
```

**Response (200):**
```json
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
```

**Response (404):**
```json
{
  "detail": "No previous session found for Leg Press"
}
```

**Query Parameters:**
- `session_threshold_hours` (optional, default: 2.0): Hours between sets indicating new session

---

### 3. **GET /{user_id}/history** - Get Exercise History
Optional endpoint for analytics.

**Request:**
```
GET /api/v1/logs/user_123/history?exercise_name=Leg%20Press&limit=50
```

---

## 🧠 Session Clustering Algorithm

### Problem Statement
A "session" is a cluster of log entries with close timestamps. The challenge is to identify session boundaries from a continuous stream of logs.

### Algorithm
```python
Input: Log entries sorted by timestamp DESC
Output: All sets from most recent session

1. Iterate through logs (newest to oldest)
2. Calculate time gap between consecutive logs
3. If gap > threshold (default 2 hours):
     → Session boundary detected
     → Save current session
     → Start new session
4. Return first (most recent) session
5. Sort by set_number before return
```

### Examples
```
Scenario 1: Single session
Logs: [10:00, 10:05, 10:10]
Gaps: [5min, 5min]
Result: All 3 sets returned (same session)

Scenario 2: Multiple sessions
Logs: [10:00, 10:05, 07:00, 07:05]
Gaps: [5min, 3hours, 5min]
Result: First 2 sets returned (today's session)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/ldps
pip3 install -r requirements.txt
```

### 2. Initialize Database
```bash
python3 -c "from database.connection import init_db; init_db()"
```

### 3. Start Server
```bash
python3 main.py
```

Server will start on **http://localhost:8001**

### 4. Verify Health
```bash
curl http://localhost:8001
```

Expected response:
```json
{
  "service": "L-DPS",
  "status": "operational",
  "version": "1.0.0"
}
```

### 5. View API Docs
Open browser: http://localhost:8001/docs

---

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/test_session_clustering.py -v
```

### Manual Testing Examples

#### Create a log entry
```bash
curl -X POST "http://localhost:8001/api/v1/logs" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "exercise_name": "Squat",
    "set_number": 1,
    "weight_used": 100.0,
    "reps_completed": 10
  }'
```

#### Get latest session
```bash
curl "http://localhost:8001/api/v1/logs/test_user/Squat/latest-session"
```

#### Get exercise history
```bash
curl "http://localhost:8001/api/v1/logs/test_user/history?limit=20"
```

---

## 🔒 Immutability Enforcement

### Code-Level
```python
def update_log_entry(*args, **kwargs):
    raise NotImplementedError("Log entries cannot be updated")

def delete_log_entry(*args, **kwargs):
    raise NotImplementedError("Log entries cannot be deleted")
```

### Database-Level (Future)
For PostgreSQL production deployment, add trigger:
```sql
CREATE TRIGGER no_updates_on_logs
    BEFORE UPDATE ON log_entries
    FOR EACH ROW
    EXECUTE FUNCTION prevent_log_updates();
```

---

## 🔗 Integration with S-RE (Phase 3)

### Scenario: User starts "Leg Press"
```
S-RE → GET /api/v1/logs/user_123/Leg%20Press/latest-session
L-DPS → Apply session clustering algorithm
L-DPS → Return all sets from last session
S-RE → Display reference data to user
```

### Scenario: User completes Set 1
```
S-RE → POST /api/v1/logs
       Body: {user_id, exercise_name, set_number, weight, reps}
L-DPS → Validate & create log entry
L-DPS → Return confirmation with timestamp
S-RE → Update UI: "Set 1 Logged: 110kg x 8"
```

---

## 📊 Performance Considerations

### Query Optimization
- Composite index on (user_id, exercise_name, timestamp) ensures fast session retrieval
- Typical query time: <50ms for 1000+ log entries

### Scalability
- SQLite suitable for single-user development
- PostgreSQL recommended for production (multi-user)
- Consider partitioning by date for large datasets (1M+ entries)

---

## ⚠️ Edge Cases Handled

1. **No previous session**: Returns 404 with clear message
2. **Single set in session**: Returns that one set
3. **Unordered set numbers**: Sorted by set_number before return
4. **Timezone handling**: All timestamps stored as UTC
5. **Concurrent writes**: UUID primary keys prevent collisions

---

## 🔐 Security Notes

- No authentication in Phase 2 (S-RE will handle in Phase 3)
- Exercise names are case-sensitive
- Input validation via Pydantic schemas
- SQL injection protected by SQLAlchemy ORM

---

## 📝 Future Enhancements

- [ ] Soft-delete functionality with audit log
- [ ] Exercise name normalization/dictionary
- [ ] Batch log creation endpoint
- [ ] Export data as CSV/JSON
- [ ] Performance analytics (PR tracking, volume calculations)

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8001
lsof -i :8001
kill -9 <PID>
```

### Database Issues
```bash
# Reset database
rm ldps.db
python3 -c "from database.connection import init_db; init_db()"
```

### Import Errors
```bash
# Reinstall dependencies
pip3 install -r requirements.txt
```

---

## 📚 References

- **PRD:** `../docs/PRD.md`
- **Project Rules:** `../WARP.md`
- **P-MIS Reference:** `../pmis/`
- **Testing Guide:** `../docs/L-DPS_TESTING_GUIDE.md` (to be created)

---

**L-DPS Status:** ✅ Ready for Testing  
**Next Phase:** S-RE (Workout Session & Reference Engine)
