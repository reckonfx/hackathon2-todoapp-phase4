"""
MCP Tool: delete_all_tasks
Permanently removes all tasks for a user.
Spec Reference: 003-agent-mcp-tools spec - Tool Extension
"""

from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid

from ...models.task import Task
from ...models.user import User


async def delete_all_tasks(
    db: AsyncSession,
    user_id: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Permanently remove all tasks for a user.

    Args:
        db: Database session
        user_id: Unique identifier of the task owner
        confirm: Must be True to confirm deletion

    Returns:
        Dict with success status, count of deleted tasks, and message
    """
    # Require confirmation
    if not confirm:
        return {
            "success": False,
            "error": "CONFIRMATION_REQUIRED",
            "message": "Please confirm deletion by setting confirm=true. This will permanently delete ALL tasks."
        }

    # Validate user_id
    try:
        u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        return {
            "success": False,
            "error": "INVALID_USER",
            "message": "Invalid user ID format"
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

    # Count tasks before deletion
    result = await db.execute(select(Task).filter(Task.user_id == u_id))
    tasks = result.scalars().all()
    count = len(tasks)

    if count == 0:
        return {
            "success": True,
            "deleted_count": 0,
            "message": "No tasks to delete"
        }

    # Delete all tasks for this user
    await db.execute(delete(Task).where(Task.user_id == u_id))
    await db.commit()

    return {
        "success": True,
        "deleted_count": count,
        "message": f"Successfully deleted {count} task(s)"
    }
