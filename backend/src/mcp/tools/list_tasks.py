"""
MCP Tool: list_tasks
Retrieves tasks for a user with optional filtering.
Spec Reference: 003-agent-mcp-tools spec - Tool 2
"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from ...models.task import Task
from ...models.user import User


async def list_tasks(
    db: AsyncSession,
    user_id: str,
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Retrieve tasks for the specified user with optional filtering.

    Args:
        db: Database session
        user_id: Unique identifier of the task owner
        completed: Filter by completion status
        search: Search term to match against title/description
        limit: Maximum results to return (default: 50, max: 100)

    Returns:
        Dict with success status, tasks list, count, and message

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

    # Validate limit
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 1

    # Validate user exists
    result = await db.execute(select(User).filter(User.id == u_id))
    user = result.scalar_one_or_none()

    if not user:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "User not found"
        }

    # Build query
    query = select(Task).filter(Task.user_id == u_id)

    # Apply filters
    if completed is not None:
        query = query.filter(Task.completed == completed)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_pattern)) |
            (Task.description.ilike(search_pattern))
        )

    # Order by created_at desc and apply limit
    query = query.order_by(Task.created_at.desc()).limit(limit)

    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Format tasks for response
    task_list = []
    for task in tasks:
        task_list.append({
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": "medium",  # Default priority (not in Phase II model)
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        })

    return {
        "success": True,
        "tasks": task_list,
        "count": len(task_list),
        "message": f"Found {len(task_list)} task(s)"
    }
