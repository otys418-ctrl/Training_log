"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Plan(Base):
    """Training plan model"""
    __tablename__ = "plans"
    
    plan_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = relationship("DailyWorkout", back_populates="plan", cascade="all, delete-orphan")


class DailyWorkout(Base):
    """Daily workout model"""
    __tablename__ = "daily_workouts"
    
    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String, ForeignKey("plans.plan_id"), nullable=False)
    day = Column(String, nullable=False)
    target_body_parts = Column(JSON, default=[])
    
    # Relationships
    plan = relationship("Plan", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")


class Exercise(Base):
    """Exercise model"""
    __tablename__ = "exercises"
    
    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("daily_workouts.workout_id"), nullable=False)
    name = Column(String, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    
    # Relationships
    workout = relationship("DailyWorkout", back_populates="exercises")
