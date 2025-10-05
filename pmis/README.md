# P-MIS (Plan Management & Ingestion Service)

A service for ingesting, parsing, and managing training plans from PDF documents.

## Features

- **PDF Parsing**: Extract text from PDF training plans using PyMuPDF
- **NLP Data Extraction**: Automatically extract exercises, sets, reps, and body parts using spaCy
- **RESTful API**: FastAPI-based API for plan management
- **SQLite Database**: Local database storage with SQLAlchemy ORM
- **Daily Workout Retrieval**: Query workouts by day of the week
- **CRUD Operations**: Full create, read, update, delete support

## Project Structure

```
pmis/
├── api/              # API routes and endpoints
├── database/         # Database connection and CRUD operations
├── extractors/       # NLP-based data extraction logic
├── models/           # Pydantic schemas and SQLAlchemy models
├── parsers/          # PDF parsing utilities
├── tests/            # Unit tests
├── utils/            # Helper utilities
├── main.py           # FastAPI application entry point
├── .env              # Environment configuration
└── pmis.db           # SQLite database file
```

## Installation

### Prerequisites
- Python 3.13+
- pip

### Setup

1. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

2. **Download spaCy language model:**
```bash
python3 -m spacy download en_core_web_sm
```

3. **Create environment file:**
```bash
cp .env.example .env
```

4. **Initialize database:**
```bash
python3 -c "from database.connection import init_db; init_db()"
```

## Usage

### Start the API Server

```bash
python3 main.py
```

The API will be available at `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

### API Endpoints

#### 1. Health Check
```bash
GET /
```

#### 2. Upload Training Plan PDF
```bash
POST /api/v1/plans/upload?user_id=user123
Content-Type: multipart/form-data

Body: file=@training_plan.pdf
```

Example with curl:
```bash
curl -X POST "http://localhost:8000/api/v1/plans/upload?user_id=user123" \
  -F "file=@/path/to/training_plan.pdf"
```

#### 3. Get Full Training Plan
```bash
GET /api/v1/plans/{user_id}
```

Example:
```bash
curl http://localhost:8000/api/v1/plans/user123
```

#### 4. Get Daily Workout
```bash
GET /api/v1/plans/{user_id}/{day}
```

Example:
```bash
curl http://localhost:8000/api/v1/plans/user123/Monday
```

#### 5. Delete Training Plan
```bash
DELETE /api/v1/plans/{user_id}
```

Example:
```bash
curl -X DELETE http://localhost:8000/api/v1/plans/user123
```

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test API Endpoints
```bash
python3 test_api.py
```

## PDF Format Requirements

For best results, training plan PDFs should follow this structure:

```
Monday - Chest & Triceps
- Bench Press 3x10
- Incline Dumbbell Press 3x12
- Cable Flyes 3x15

Tuesday - Back & Biceps
- Pull-ups 3x10
- Barbell Rows 4x8
- Dumbbell Curls 3x12
...
```

### Supported Formats:
- **Days**: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
- **Sets/Reps**: "3x10", "3 x 10", "3 sets of 10"
- **Body Parts**: chest, back, shoulders, legs, arms, biceps, triceps, etc.

## Dependencies

### Core Dependencies
- **FastAPI** 0.118.0 - Web framework
- **Uvicorn** 0.37.0 - ASGI server
- **SQLAlchemy** 2.0.43 - Database ORM
- **Pydantic** 2.11.10 - Data validation
- **PyMuPDF** 1.26.4 - PDF parsing
- **spaCy** 3.8.7 - NLP processing

### Development Dependencies
- **Pytest** 8.4.2 - Testing framework
- **HTTPX** 0.28.1 - HTTP client for testing
- **Alembic** 1.16.5 - Database migrations (future use)

## Database Schema

### Tables

**plans**
- `plan_id` (String, Primary Key)
- `user_id` (String, Indexed)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**daily_workouts**
- `workout_id` (Integer, Primary Key)
- `plan_id` (String, Foreign Key)
- `day` (String)
- `target_body_parts` (JSON Array)

**exercises**
- `exercise_id` (Integer, Primary Key)
- `workout_id` (Integer, Foreign Key)
- `name` (String)
- `sets` (Integer, Nullable)
- `reps` (Integer, Nullable)

## Development Status

✅ **Completed:**
- Project scaffolding
- PDF parsing implementation
- NLP-based data extraction
- Database models and CRUD operations
- API endpoints
- Unit tests
- Database initialization
- API testing

🚧 **Future Enhancements:**
- Image-based PDF OCR support
- Advanced exercise recognition
- Multi-user authentication
- Progress tracking integration
- Mobile app API endpoints
- Database migrations with Alembic

## Troubleshooting

### Common Issues

**spaCy model not found:**
```bash
python3 -m spacy download en_core_web_sm
```

**Import errors:**
Make sure you're running commands from the project root directory:
```bash
cd /Users/flxshh/Desktop/WARP/Training_log/pmis
```

**Database not found:**
```bash
python3 -c "from database.connection import init_db; init_db()"
```

## License

This project is part of the Progressive Overload Training Log system.
