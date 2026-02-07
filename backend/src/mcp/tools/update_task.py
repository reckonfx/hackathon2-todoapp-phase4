"""
MCP Tool: update_task
Modifies one or more properties of an existing task.
Spec Reference: 003-agent-mcp-tools spec - Tool 5
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
import uuid

from ...models.task import Task
from ...models.user import User


async def update_task(
    db: AsyncSession,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Modify one or more properties of an existing task.

    Args:
        db: Database session
        user_id: Unique identifier of the task owner
        task_id: Unique identifier of the task
        title: New task title (1-500 characters)
        description: New description (max 2000 characters, None to clear)
        completed: Set completion status

    Returns:
        Dict with success status, updated task, changes list, and message

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

    # Check if any updates provided
    if title is None and description is None and completed is None:
        return {
            "success": False,
            "error": "NO_CHANGES",
            "message": "No changes specified"
        }

    # Validate title if provided
    if title is not None:
        if len(title) < 1 or len(title) > 500:
            return {
                "success": False,
                "error": "INVALID_TITLE",
                "message": "Task title must be 1-500 characters"
            }

    # Validate description if provided
    if description is not None and len(description) > 2000:
        return {
            "success": False,
            "error": "INVALID_DESCRIPTION",
            "message": "Description must be at most 2000 characters"
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

    # Track changes
    changes: List[str] = []

    # Apply updates
    if title is not None and title != task.title:
        task.title = title
        changes.append("title")

    if description is not None and description != task.description:
        task.description = description if description else None
        changes.append("description")

    if completed is not None and completed != task.completed:
        task.completed = completed
        if completed:
            task.completed_at = func.now()
        else:
            task.completed_at = None
        changes.append("completed")

    # If no actual changes were made
    if not changes:
        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": "medium",
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat() if task.updated_at else datetime.utcnow().isoformat()
            },
            "changes": [],
            "message": "No changes needed"
        }

    # Save changes
    await db.commit()
    await db.refresh(task)

    return {
        "success": True,
        "task": {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": "medium",
            "completed": task.completed,
            "updated_at": task.updated_at.isoformat() if task.updated_at else datetime.utcnow().isoformat()
        },
        "changes": changes,
        "message": f"Updated: {', '.join(changes)}"
    }
