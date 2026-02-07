"""Data models for the Todo application."""

from dataclasses import dataclass, field

@dataclass(kw_only=True)
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier.
        title: Short summary of the task.
        description: Detailed notes.
        completed: Whether the task is finished.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate fields after initialization."""
        self.title = self.title.strip()
        self.description = self.description.strip()

        if not self.title:
            raise ValueError("Task title cannot be empty")

        if len(self.title) > 100:
            self.title = self.title[:100]

        if len(self.description) > 500:
            self.description = self.description[:500]
