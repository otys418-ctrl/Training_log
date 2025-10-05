"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ExerciseBase(BaseModel):
    """Base schema for exercise data"""
    name: str = Field(..., description="Exercise name")
    sets: Optional[int] = Field(None, description="Number of sets")
    reps: Optional[int] = Field(None, description="Number of reps per set")


class ExerciseCreate(ExerciseBase):
    """Schema for creating an exercise"""
    pass


class ExerciseResponse(ExerciseBase):
    """Schema for exercise response"""
    exercise_id: int
    
    class Config:
        from_attributes = True


class DailyWorkoutBase(BaseModel):
    """Base schema for daily workout data"""
    day: str = Field(..., description="Day of the week")
    target_body_parts: List[str] = Field(default=[], description="Target body parts")
    exercises: List[ExerciseBase] = Field(default=[], description="List of exercises")


class DailyWorkoutCreate(DailyWorkoutBase):
    """Schema for creating a daily workout"""
    pass


class DailyWorkoutResponse(DailyWorkoutBase):
    """Schema for daily workout response"""
    workout_id: int
    plan_id: str
    
    class Config:
        from_attributes = True


class PlanBase(BaseModel):
    """Base schema for training plan data"""
    user_id: str = Field(..., description="User identifier")
    workouts: List[DailyWorkoutBase] = Field(default=[], description="List of daily workouts")


class PlanCreate(PlanBase):
    """Schema for creating a plan"""
    pass


class PlanResponse(PlanBase):
    """Schema for plan response"""
    plan_id: str
    created_at: str
    
    class Config:
        from_attributes = True
