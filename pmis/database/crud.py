"""
CRUD operations for database models
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from models.db_models import Plan, DailyWorkout, Exercise
from models.schemas import DailyWorkoutResponse, PlanResponse, ExerciseResponse
import uuid


def create_plan(db: Session, plan_data: Dict[str, Any]) -> Plan:
    """
    Create a new training plan with workouts and exercises
    
    Args:
        db: Database session
        plan_data: Dictionary containing plan data with workouts
    
    Returns:
        Created Plan object
    """
    # Create plan
    plan = Plan(
        plan_id=str(uuid.uuid4()),
        user_id=plan_data["user_id"]
    )
    db.add(plan)
    db.flush()  # Get the plan_id
    
    # Create workouts and exercises
    for workout_data in plan_data.get("workouts", []):
        workout = DailyWorkout(
            plan_id=plan.plan_id,
            day=workout_data["day"],
            target_body_parts=workout_data.get("target_body_parts", [])
        )
        db.add(workout)
        db.flush()  # Get the workout_id
        
        # Create exercises
        for exercise_data in workout_data.get("exercises", []):
            exercise = Exercise(
                workout_id=workout.workout_id,
                name=exercise_data["name"],
                sets=exercise_data.get("sets"),
                reps=exercise_data.get("reps")
            )
            db.add(exercise)
    
    db.commit()
    db.refresh(plan)
    return plan


def get_plan_by_user(db: Session, user_id: str) -> Optional[PlanResponse]:
    """
    Retrieve the most recent plan for a user
    
    Args:
        db: Database session
        user_id: User identifier
    
    Returns:
        PlanResponse or None if not found
    """
    plan = db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.created_at.desc()).first()
    
    if not plan:
        return None
    
    # Build response
    workouts = []
    for workout in plan.workouts:
        exercises = [
            {"name": ex.name, "sets": ex.sets, "reps": ex.reps}
            for ex in workout.exercises
        ]
        workouts.append({
            "day": workout.day,
            "target_body_parts": workout.target_body_parts,
            "exercises": exercises
        })
    
    return PlanResponse(
        plan_id=plan.plan_id,
        user_id=plan.user_id,
        created_at=plan.created_at.isoformat(),
        workouts=workouts
    )


def get_daily_workout(db: Session, user_id: str, day: str) -> Optional[DailyWorkoutResponse]:
    """
    Retrieve the workout for a specific day
    
    Args:
        db: Database session
        user_id: User identifier
        day: Day of the week
    
    Returns:
        DailyWorkoutResponse or None if not found
    """
    # Get the most recent plan for the user
    plan = db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.created_at.desc()).first()
    
    if not plan:
        return None
    
    # Get the workout for the specified day
    workout = db.query(DailyWorkout).filter(
        DailyWorkout.plan_id == plan.plan_id,
        DailyWorkout.day == day
    ).first()
    
    if not workout:
        return None
    
    # Build exercises list
    exercises = [
        {"name": ex.name, "sets": ex.sets, "reps": ex.reps}
        for ex in workout.exercises
    ]
    
    return DailyWorkoutResponse(
        workout_id=workout.workout_id,
        plan_id=plan.plan_id,
        day=workout.day,
        target_body_parts=workout.target_body_parts,
        exercises=exercises
    )


def delete_plan(db: Session, user_id: str) -> bool:
    """
    Delete a user's training plan
    
    Args:
        db: Database session
        user_id: User identifier
    
    Returns:
        True if deleted, False if not found
    """
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    
    if not plan:
        return False
    
    db.delete(plan)
    db.commit()
    return True
