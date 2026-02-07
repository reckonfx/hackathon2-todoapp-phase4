"""
Task model for the Phase-2 Web-Based Todo Application.
Defines the Task SQLAlchemy ORM model with PostgreSQL compatibility.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..database.connection import Base


class Task(Base):
    """SQLAlchemy model for tasks with PostgreSQL compatibility."""

    __tablename__ = "tasks"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)  # Explicit length for PostgreSQL
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, server_default="false")  # PostgreSQL boolean
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"


# Add relationship to User model after Task is defined
from .user import User  # Import here to avoid circular imports

User.tasks = relationship("Task", order_by=Task.id, back_populates="user", cascade="all, delete-orphan")