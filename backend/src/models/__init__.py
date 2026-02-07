"""
Models package for the Phase-2/3 Web-Based Todo Application.
Contains SQLAlchemy ORM models for database entities.

Phase II (Frozen):
- User: User accounts and authentication
- Task: Todo items belonging to users

Phase III (New):
- Conversation: Chat sessions between users and AI assistant
- Message: Individual messages within conversations
"""

from .user import User
from .task import Task
from .conversation import Conversation
from .message import Message

# Add Phase III relationships to User model
# This avoids circular imports while maintaining proper relationship setup
User.conversations = __import__('sqlalchemy.orm', fromlist=['relationship']).relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan"
)

__all__ = ["User", "Task", "Conversation", "Message"]