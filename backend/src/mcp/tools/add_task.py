"""
MCP Tool: add_task
Creates a new task for a user.
Spec Reference: 003-agent-mcp-tools spec - Tool 1
"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from ...models.task import Task
from ...models.user import User


async def add_task(
    db: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Create a new task for the specified user.

    Args:
        db: Database session
        user_id: Unique identifier of the task owner
        title: Task title (1-500 characters)
        description: Extended task description (max 2000 characters)
        priority: "low", "medium", or "high" (default: "medium")

    Returns:
        Dict with success status, task details, and message

    Spec Reference: MTR-001 to MTR-006
    """
    # Validate title (MTR-002)
    if not title or len(title) < 1:
        return {
            "success": False,
            "error": "INVALID_TITLE",
            "message": "Task title must be 1-500 characters"
        }
    if len(title) > 500:
        return {
            "success": False,
            "error": "INVALID_TITLE",
            "message": "Task title must be 1-500 characters"
        }

    # Validate description
    if description and len(description) > 2000:
        return {
            "success": False,
            "error": "INVALID_DESCRIPTION",
            "message": "Description must be at most 2000 characters"
        }

    # Validate priority
    valid_priorities = ["low", "medium", "high"]
    if priority not in valid_priorities:
        return {
            "success": False,
            "error": "INVALID_PRIORITY",
            "message": "Priority must be low, medium, or high"
        }

    # Validate user exists
    try:
        u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "Invalid user ID format"
        }

    result = await db.execute(select(User).filter(User.id == u_id))
    user = result.scalar_one_or_none()

    if not user:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "User not found"
        }

    # Create task (MTR-005 - database layer only)
    task = Task(
        user_id=u_id,
        title=title,
        description=description,
        completed=False
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    # Return response with timestamp (MTR-004)
    return {
        "success": True,
        "task": {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": priority,  # Note: priority not in Phase II Task model
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if task.created_at else datetime.utcnow().isoformat()
        },
        "message": "Task created successfully"
    }
