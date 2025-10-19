"""
Main FastAPI application for L-DPS (Logbook & Data Persistence Service)

IMPORTANT: This service is INDEPENDENT from P-MIS
- Runs on port 8001 (P-MIS is on 8000)
- Uses separate database (ldps.db)
- Zero coupling with P-MIS code
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import logs
from database.connection import init_db

app = FastAPI(
    title="L-DPS API",
    description="Logbook & Data Persistence Service - Immutable workout performance ledger",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on deployment needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup"""
    init_db()

# Include API routes
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "L-DPS",
        "status": "operational",
        "version": "1.0.0",
        "description": "Logbook & Data Persistence Service - Append-only workout log",
        "endpoints": {
            "create_log": "POST /api/v1/logs",
            "get_latest_session": "GET /api/v1/logs/{user_id}/{exercise_name}/latest-session",
            "get_history": "GET /api/v1/logs/{user_id}/history"
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Port 8001 to avoid conflict with P-MIS (8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
