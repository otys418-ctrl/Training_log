"""
API endpoints for training plan management
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database.connection import get_db
from models.schemas import PlanResponse, DailyWorkoutResponse
from parsers.pdf_parser import PDFParser
from extractors.plan_extractor import PlanExtractor
from database import crud

router = APIRouter()


@router.post("/upload", response_model=dict, status_code=201)
async def upload_plan(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and parse a training plan PDF
    
    Args:
        user_id: Unique identifier for the user
        file: PDF file containing the training plan
        db: Database session
    
    Returns:
        Confirmation message with plan_id
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read PDF content
        pdf_content = await file.read()
        
        # Parse PDF to extract text
        parser = PDFParser()
        raw_text = parser.parse(pdf_content)
        
        # Extract structured data from text
        extractor = PlanExtractor()
        plan_data = extractor.extract(raw_text, user_id)
        
        # Store in database
        plan = crud.create_plan(db, plan_data)
        
        return {
            "message": "Plan uploaded successfully",
            "plan_id": plan.plan_id,
            "user_id": user_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing plan: {str(e)}")


@router.get("/{user_id}/{day}", response_model=DailyWorkoutResponse)
async def get_daily_workout(
    user_id: str,
    day: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve the scheduled workout for a specific day
    
    Args:
        user_id: Unique identifier for the user
        day: Day of the week (Monday, Tuesday, etc.)
        db: Database session
    
    Returns:
        DailyWorkoutResponse containing exercises for the specified day
    """
    # Validate day - accept both "Day 1" format and standard day names
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    valid_day_numbers = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    
    day_formatted = day.replace("%20", " ").strip()
    if day_formatted.capitalize() not in valid_days and day_formatted not in valid_day_numbers:
        raise HTTPException(status_code=400, detail=f"Invalid day. Must be one of: {', '.join(valid_days)} or Day 1-7")
    
    # Fetch plan from database
    workout = crud.get_daily_workout(db, user_id, day_formatted)
    
    if not workout:
        raise HTTPException(status_code=404, detail=f"No workout found for {user_id} on {day}")
    
    return workout


@router.get("/{user_id}", response_model=PlanResponse)
async def get_full_plan(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve the complete training plan for a user
    
    Args:
        user_id: Unique identifier for the user
        db: Database session
    
    Returns:
        Complete PlanResponse for the user
    """
    plan = crud.get_plan_by_user(db, user_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail=f"No plan found for user {user_id}")
    
    return plan


@router.delete("/{user_id}")
async def delete_plan(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a user's training plan
    
    Args:
        user_id: Unique identifier for the user
        db: Database session
    
    Returns:
        Confirmation message
    """
    success = crud.delete_plan(db, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"No plan found for user {user_id}")
    
    return {"message": f"Plan for user {user_id} deleted successfully"}
