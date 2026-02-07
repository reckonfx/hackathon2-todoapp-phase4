"""
Task service for the Phase-2 Web-Based Todo Application.
Handles business logic for task operations with async database support.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, func
from ..models.task import Task
from ..models.user import User
from ..database.schemas.task_schema import TaskCreate, TaskUpdate, TaskInDB
import uuid


async def get_user_tasks(db: AsyncSession, user_id: str) -> List[TaskInDB]:
    """Get all tasks for a specific user."""
    # Convert string to UUID object for SQLAlchemy
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    result = await db.execute(select(Task).filter(Task.user_id == u_id))
    tasks = result.scalars().all()
    return [TaskInDB.model_validate(task) for task in tasks]


async def get_task_by_id(db: AsyncSession, task_id: str, user_id: str) -> Optional[TaskInDB]:
    """Get a specific task by ID for a user."""
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    t_id = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
    result = await db.execute(select(Task).filter(Task.id == t_id, Task.user_id == u_id))
    task = result.scalar_one_or_none()
    if not task:
        return None
    return TaskInDB.model_validate(task)


async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: str) -> TaskInDB:
    """Create a new task for a user."""
    # Pass the user_id directly - SQLAlchemy will handle the UUID conversion
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    )

    try:
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return TaskInDB.model_validate(db_task)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating task"
        )


async def update_task(db: AsyncSession, task_id: str, task_data: TaskUpdate, user_id: str) -> Optional[TaskInDB]:
    """Update an existing task."""
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    t_id = uuid.UUID(task_id) if isinstance(task_id, str) else task_id

    # Query for the existing task
    result = await db.execute(select(Task).filter(Task.id == t_id, Task.user_id == u_id))
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Update fields that are provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
        if task_data.completed:
            task.completed_at = func.now()
        else:
            task.completed_at = None

    try:
        await db.commit()
        await db.refresh(task)
        return TaskInDB.model_validate(task)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating task"
        )


async def delete_task(db: AsyncSession, task_id: str, user_id: str) -> bool:
    """Delete a task."""
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    t_id = uuid.UUID(task_id) if isinstance(task_id, str) else task_id

    result = await db.execute(
        delete(Task).filter(Task.id == t_id, Task.user_id == u_id).returning(Task.id)
    )
    deleted_row = result.fetchone()

    if not deleted_row:
        return False

    await db.commit()
    return True


async def toggle_task_completion(db: AsyncSession, task_id: str, user_id: str) -> Optional[TaskInDB]:
    """Toggle the completion status of a task."""
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    t_id = uuid.UUID(task_id) if isinstance(task_id, str) else task_id

    result = await db.execute(select(Task).filter(Task.id == t_id, Task.user_id == u_id))
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Toggle the completion status
    task.completed = not task.completed
    if task.completed:
        task.completed_at = func.now()
    else:
        task.completed_at = None

    try:
        await db.commit()
        await db.refresh(task)
        return TaskInDB.model_validate(task)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating task completion status"
        )