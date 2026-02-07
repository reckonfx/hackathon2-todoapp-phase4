"""
MCP Tool: complete_task
Marks a task as completed.
Spec Reference: 003-agent-mcp-tools spec - Tool 3
"""

from typing import Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
import uuid

from ...models.task import Task
from ...models.user import User


async def complete_task(
    db: AsyncSession,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        db: Database session
        user_id: Unique identifier of the task owner
        task_id: Unique identifier of the task

    Returns:
        Dict with success status, task details, and message

    Spec Reference: MTR-001 to MTR-006
    """
    # Validate user_id
    try:
        u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "Invalid user ID format"
        }

    # Validate task_id
    try:
        t_id = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
    except ValueError:
        return {
            "success": False,
            "error": "TASK_NOT_FOUND",
            "message": "Invalid task ID format"
        }

    # Validate user exists
    result = await db.execute(select(User).filter(User.id == u_id))
    user = result.scalar_one_or_none()

    if not user:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "User not found"
        }

    # Get the task
    result = await db.execute(select(Task).filter(Task.id == t_id))
    task = result.scalar_one_or_none()

    if not task:
        return {
            "success": False,
            "error": "TASK_NOT_FOUND",
            "message": "Task not found"
        }

    # Verify ownership
    if task.user_id != u_id:
        return {
            "success": False,
            "error": "UNAUTHORIZED",
            "message": "You don't have access to this task"
        }

    # Check if already completed (idempotent - MTR-006)
    if task.completed:
        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "completed": True,
                "completed_at": task.completed_at.isoformat() if task.completed_at else datetime.utcnow().isoformat()
            },
            "message": "Task is already completed"
        }

    # Mark as completed
    task.completed = True
    task.completed_at = func.now()

    await db.commit()
    await db.refresh(task)

    return {
        "success": True,
        "task": {
            "id": str(task.id),
            "title": task.title,
            "completed": True,
            "completed_at": task.completed_at.isoformat() if task.completed_at else datetime.utcnow().isoformat()
        },
        "message": "Task marked as completed"
    }
