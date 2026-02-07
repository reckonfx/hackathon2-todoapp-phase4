"""
Task schemas for the Phase-2 Web-Based Todo Application.
Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class TaskBase(BaseModel):
    """Base task model with common fields."""

    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    title: str

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True


class TaskInDB(TaskBase):
    """Schema for task data in database."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskPublic(TaskBase):
    """Public task schema."""

    id: UUID

    class Config:
        from_attributes = True


class TaskToggle(BaseModel):
    """Schema for toggling task completion."""

    completed: bool

    class Config:
        from_attributes = True