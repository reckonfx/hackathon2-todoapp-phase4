"""
Task routes for the Phase-2 Web-Based Todo Application.
Defines API endpoints for task management with async PostgreSQL database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import jwt
from datetime import timedelta

from ...database.deps import get_db
from ...database.schemas.task_schema import (
    TaskCreate, TaskUpdate, TaskInDB, TaskToggle
)
from ...services.task_service import (
    get_user_tasks, get_task_by_id, create_task, update_task,
    delete_task, toggle_task_completion
)
from ...models.user import User
from ...database.connection import settings
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tasks", tags=["tasks"], redirect_slashes=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get the current user from the token (async PostgreSQL)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    from sqlalchemy import select

    # Async execution for PostgreSQL
    result = await db.execute(select(User).filter(User.email == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


@router.get("", response_model=dict)
async def get_all_tasks(
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Get all tasks for the current user (async PostgreSQL)."""
    tasks = await get_user_tasks(db, str(current_user.id))
    return {
        "success": True,
        "tasks": tasks,
        "count": len(tasks)
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate,
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Create a new task for the current user (async PostgreSQL)."""
    created_task = await create_task(db, task_data, str(current_user.id))
    return {
        "success": True,
        "task": created_task,
        "message": "Task created successfully"
    }


@router.get("/{task_id}", response_model=dict)
async def get_single_task(
    task_id: str,
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific task by ID (async PostgreSQL)."""
    task = await get_task_by_id(db, task_id, str(current_user.id))
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "success": True,
        "task": task
    }


@router.put("/{task_id}", response_model=dict)
async def update_existing_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing task (async PostgreSQL)."""
    updated_task = await update_task(db, task_id, task_data, str(current_user.id))
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "success": True,
        "task": updated_task,
        "message": "Task updated successfully"
    }


@router.delete("/{task_id}", response_model=dict)
async def delete_existing_task(
    task_id: str,
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Delete an existing task (async PostgreSQL)."""
    success = await delete_task(db, task_id, str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "success": True,
        "message": "Task deleted successfully"
    }


@router.patch("/{task_id}/toggle", response_model=dict)
async def toggle_task_completion_status(
    task_id: str,
    current_user=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Toggle the completion status of a task (async PostgreSQL)."""
    updated_task = await toggle_task_completion(db, task_id, str(current_user.id))
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "success": True,
        "task": updated_task,
        "message": "Task completion status updated"
    }