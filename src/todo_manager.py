"""Business logic for managing todo tasks."""

from typing import List, Tuple, Optional
from models import Task

class TodoManager:
    """Manages a collection of tasks in-memory."""

    def __init__(self):
        """Initialize an empty task list."""
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Tuple[bool, str, Optional[Task]]:
        """Add a new task to the list.

        Args:
            title: The task title.
            description: Detailed notes.

        Returns:
            Tuple of (success, message, task).
        """
        try:
            task = Task(id=self._next_id, title=title, description=description)
            self.tasks.append(task)
            self._next_id += 1
            return True, f"Task added successfully! ID: {task.id}", task
        except ValueError as e:
            return False, str(e), None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks.

        Returns:
            List of Task objects.
        """
        return self.tasks

    def toggle_complete(self, task_id: int) -> Tuple[bool, str, Optional[Task]]:
        """Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle.

        Returns:
            Tuple of (success, message, task).
        """
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                status = "complete" if task.completed else "incomplete"
                return True, f"Task #{task_id} marked as {status}", task
        return False, f"Task with ID {task_id} not found", None

    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        """Remove a task from the list.

        Args:
            task_id: ID of the task to delete.

        Returns:
            Tuple of (success, message).
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True, f"Task #{task_id} deleted"
        return False, f"Task with ID {task_id} not found"

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Tuple[bool, str, Optional[Task]]:
        """Update an existing task's fields.

        Args:
            task_id: ID of the task to update.
            title: New title (optional).
            description: New description (optional).

        Returns:
            Tuple of (success, message, task).
        """
        for task in self.tasks:
            if task.id == task_id:
                changes_made = False
                if title is not None and title.strip():
                    task.title = title.strip()
                    changes_made = True
                if description is not None:
                    task.description = description.strip()
                    changes_made = True

                if not changes_made:
                    return True, "No changes made", task
                return True, f"Task #{task_id} updated", task
        return False, f"Task with ID {task_id} not found", None
