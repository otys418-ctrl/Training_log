"""
Main FastAPI application for P-MIS (Plan Management & Ingestion Service)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import plans
from database.connection import init_db

app = FastAPI(
    title="P-MIS API",
    description="Plan Management & Ingestion Service for Progressive Overload Log",
    version="0.1.0"
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
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "P-MIS",
        "status": "operational",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
