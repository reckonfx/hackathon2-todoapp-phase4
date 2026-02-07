"""
MCP Tools package for the Phase III Chat API.
Contains individual tool implementations for task management.

Available Tools:
- add_task: Create a new task
- list_tasks: Retrieve tasks with optional filtering
- complete_task: Mark a task as completed
- delete_task: Remove a task
- delete_all_tasks: Remove all tasks
- update_task: Modify an existing task

Spec Reference: 003-agent-mcp-tools spec (MTR-001 to MTR-006)
"""

from .add_task import add_task
from .list_tasks import list_tasks
from .complete_task import complete_task
from .delete_task import delete_task
from .delete_all_tasks import delete_all_tasks
from .update_task import update_task

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "delete_all_tasks",
    "update_task"
]
