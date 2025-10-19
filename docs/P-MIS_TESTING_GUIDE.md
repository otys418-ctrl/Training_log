# P-MIS Testing Guide
**Date:** October 17, 2025  
**Service:** Plan Management & Ingestion Service  
**Environment:** localhost:8000

---

## ✅ Pre-Test Verification

### Dependencies Check
All required dependencies are installed:
- ✅ Python 3.13.3
- ✅ FastAPI 0.118.0
- ✅ Uvicorn 0.37.0
- ✅ spaCy 3.8.7
- ✅ spaCy model: en_core_web_sm

**Status:** Environment is ready for testing!

---

## 🚀 Step 1: Initialize Database

**Purpose:** Create the SQLite database schema

**Command:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
python3 -c "from database.connection import init_db; init_db()"
```

**Expected Output:**
```
Database initialized successfully (or no output if successful)
```

**Verification:**
```bash
ls -lh pmis.db
```
You should see `pmis.db` file created (likely ~40-100KB)

---

## 🚀 Step 2: Start the P-MIS Server

**Command:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
python3 main.py
```

**Expected Output:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Important:**
- Keep this terminal window open (server is running)
- Open a **new terminal tab** for testing commands
- Server runs on port 8000

---

## 🧪 Step 3: Test API Endpoints

### Test 1: Health Check (Root Endpoint)

**Purpose:** Verify server is running

**Command (in new terminal):**
```bash
curl http://localhost:8000
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "P-MIS",
  "message": "Plan Management & Ingestion Service is running"
}
```

**Status:** ✅ Server is alive

---

### Test 2: API Documentation (Swagger UI)

**Purpose:** View interactive API documentation

**Method:** Open browser and navigate to:
```
http://localhost:8000/docs
```

**Expected:**
- Interactive Swagger UI interface
- List of all API endpoints
- Ability to test endpoints directly from browser

**Screenshot:** You should see:
- `GET /` - Root endpoint
- `POST /api/v1/plans/upload` - Upload PDF
- `GET /api/v1/plans/{user_id}` - Get full plan
- `GET /api/v1/plans/{user_id}/{day}` - Get daily workout
- `DELETE /api/v1/plans/{user_id}` - Delete plan

---

### Test 3: Upload Training Plan (PDF)

**Purpose:** Test PDF parsing and plan ingestion

**Prerequisites:** You need a sample training plan PDF

#### Option A: Create a Simple Test PDF

Create a text file `sample_plan.txt`:
```
Monday - Chest & Triceps
- Bench Press 3x10
- Incline Dumbbell Press 3x12
- Cable Flyes 3x15
- Tricep Pushdowns 3x12

Tuesday - Back & Biceps
- Pull-ups 3x10
- Barbell Rows 4x8
- Dumbbell Curls 3x12
- Hammer Curls 3x12

Wednesday - Rest

Thursday - Legs
- Squats 4x10
- Leg Press 3x12
- Leg Curls 3x15
- Calf Raises 4x20

Friday - Shoulders & Abs
- Overhead Press 4x10
- Lateral Raises 3x12
- Front Raises 3x12
- Planks 3x60sec

Saturday - Rest

Sunday - Full Body
- Deadlifts 3x8
- Bench Press 3x10
- Pull-ups 3x8
- Squats 3x10
```

Convert to PDF:
- macOS: Open in TextEdit → File → Export as PDF
- Or use online converter: https://smallpdf.com/txt-to-pdf

#### Option B: Upload via Curl

**Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/plans/upload?user_id=test_user_123" \
  -F "file=@/path/to/your/training_plan.pdf"
```

**Replace:** `/path/to/your/training_plan.pdf` with actual path

**Expected Response:**
```json
{
  "message": "Training plan uploaded successfully",
  "plan_id": "plan_xxxxxxxxxxxxx",
  "user_id": "test_user_123",
  "days_parsed": 7,
  "exercises_extracted": 25
}
```

#### Option C: Upload via Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `POST /api/v1/plans/upload`
3. Click "Try it out"
4. Enter `user_id`: `test_user_123`
5. Click "Choose File" and select your PDF
6. Click "Execute"
7. Check response below

---

### Test 4: Retrieve Full Training Plan

**Purpose:** Verify plan was stored correctly

**Command:**
```bash
curl http://localhost:8000/api/v1/plans/test_user_123
```

**Expected Response:**
```json
{
  "plan_id": "plan_xxxxxxxxxxxxx",
  "user_id": "test_user_123",
  "created_at": "2025-10-17T12:00:00",
  "updated_at": "2025-10-17T12:00:00",
  "workouts": [
    {
      "workout_id": 1,
      "day": "Monday",
      "target_body_parts": ["Chest", "Triceps"],
      "exercises": [
        {
          "exercise_id": 1,
          "name": "Bench Press",
          "sets": 3,
          "reps": 10
        },
        {
          "exercise_id": 2,
          "name": "Incline Dumbbell Press",
          "sets": 3,
          "reps": 12
        }
        // ... more exercises
      ]
    }
    // ... more days
  ]
}
```

**Validation:**
- ✅ All 7 days present
- ✅ Exercises correctly extracted
- ✅ Sets/reps parsed
- ✅ Body parts identified

---

### Test 5: Get Daily Workout

**Purpose:** Test day-specific workout retrieval

**Command:**
```bash
curl http://localhost:8000/api/v1/plans/test_user_123/Monday
```

**Expected Response:**
```json
{
  "day": "Monday",
  "target_body_parts": ["Chest", "Triceps"],
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 3,
      "reps": 10
    },
    {
      "name": "Incline Dumbbell Press",
      "sets": 3,
      "reps": 12
    }
    // ... more exercises for Monday
  ]
}
```

**Test all days:**
```bash
for day in Monday Tuesday Wednesday Thursday Friday Saturday Sunday; do
  echo "Testing $day..."
  curl http://localhost:8000/api/v1/plans/test_user_123/$day
  echo -e "\n---"
done
```

---

### Test 6: Delete Training Plan

**Purpose:** Test plan deletion

**Command:**
```bash
curl -X DELETE http://localhost:8000/api/v1/plans/test_user_123
```

**Expected Response:**
```json
{
  "message": "Training plan deleted successfully",
  "user_id": "test_user_123"
}
```

**Verify deletion:**
```bash
curl http://localhost:8000/api/v1/plans/test_user_123
```

**Expected (after deletion):**
```json
{
  "detail": "Training plan not found for user: test_user_123"
}
```

---

## 🧪 Step 4: Run Unit Tests

**Purpose:** Verify all components work correctly

**Command:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
pytest tests/ -v
```

**Expected Output:**
```
tests/test_pdf_parser.py::test_parse_pdf PASSED
tests/test_pdf_parser.py::test_extract_exercises PASSED
...
======================== X passed in X.XXs ========================
```

**Note:** Some tests might fail if they require specific PDF fixtures

---

## 🧪 Step 5: Run API Integration Tests

**Purpose:** Test all endpoints programmatically

**Command:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
python3 test_api.py
```

**Expected Output:**
```
Testing P-MIS API Endpoints...
✅ Health check passed
✅ Upload plan passed
✅ Get plan passed
✅ Get daily workout passed
✅ Delete plan passed

All tests completed!
```

---

## 📊 Database Verification

### Check Database Contents

**Command:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
sqlite3 pmis.db
```

**SQLite Commands:**
```sql
-- Show all tables
.tables

-- Count plans
SELECT COUNT(*) FROM plans;

-- View all plans
SELECT * FROM plans;

-- Count workouts
SELECT COUNT(*) FROM daily_workouts;

-- Count exercises
SELECT COUNT(*) FROM exercises;

-- View sample workout
SELECT * FROM daily_workouts LIMIT 1;

-- Exit
.quit
```

---

## 🎯 Success Criteria

Your P-MIS is working correctly if:

- ✅ Server starts without errors
- ✅ Health check returns 200 OK
- ✅ Swagger UI loads at /docs
- ✅ PDF upload succeeds
- ✅ Plan retrieval returns correct data
- ✅ Daily workout queries work
- ✅ Plan deletion works
- ✅ Database is populated
- ✅ Unit tests pass

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
pip3 install -r requirements.txt
```

### Issue: "spaCy model not found"

**Solution:**
```bash
python3 -m spacy download en_core_web_sm
```

### Issue: "Port 8000 already in use"

**Check what's using the port:**
```bash
lsof -i :8000
```

**Kill the process:**
```bash
kill -9 <PID>
```

**Or use a different port:**
```bash
python3 main.py --port 8001
```

### Issue: "Database locked"

**Solution:**
```bash
rm pmis.db
python3 -c "from database.connection import init_db; init_db()"
```

### Issue: "PDF parsing errors"

**Check PDF format:**
- Ensure text is not scanned images (use OCR if needed)
- Follow format: "Day - Body Parts" then "- Exercise SetsxReps"
- Use plain text, not complex formatting

---

## 📝 Testing Checklist

Before proceeding to L-DPS:

- [ ] Database initialized
- [ ] Server starts successfully
- [ ] Health check works
- [ ] Swagger UI accessible
- [ ] PDF upload works
- [ ] Plan retrieval works
- [ ] Daily workout queries work
- [ ] Plan deletion works
- [ ] Database contains data
- [ ] Unit tests pass (if applicable)
- [ ] API test script runs (if applicable)

---

## 🚦 Next Steps

Once all tests pass:

1. **Stop the server:** Press `CTRL+C` in terminal
2. **Commit cleanup changes:**
   ```bash
   cd /Users/flxshh/Desktop/WARP/Training_log
   git commit -m "chore: Project cleanup - add .gitignore, track MCP server, fix requirements.txt"
   ```
3. **Ready for L-DPS:** Begin Phase 2 implementation

---

## 📞 Quick Reference

**Start server:**
```bash
cd pmis && python3 main.py
```

**Stop server:**
Press `CTRL+C`

**Test endpoints:**
- Health: `curl http://localhost:8000`
- Docs: http://localhost:8000/docs
- Upload: `curl -X POST "http://localhost:8000/api/v1/plans/upload?user_id=USER" -F "file=@plan.pdf"`
- Get: `curl http://localhost:8000/api/v1/plans/USER`
- Daily: `curl http://localhost:8000/api/v1/plans/USER/Monday`
- Delete: `curl -X DELETE http://localhost:8000/api/v1/plans/USER`

---

**Testing Guide Complete!** Follow the steps above to verify P-MIS functionality.
