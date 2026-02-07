"""
Message model for the Phase III Chat API.
Defines the Message SQLAlchemy ORM model.
Spec Reference: DER-011 to DER-018
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Uuid, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..database.connection import Base


class Message(Base):
    """SQLAlchemy model for messages within conversations."""

    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name='ck_messages_role'),
        CheckConstraint("length(content) BETWEEN 1 AND 10000", name='ck_messages_content_length'),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    tool_calls = Column(JSONB, nullable=True)  # Only for assistant messages
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, role='{self.role}', content='{content_preview}')>"
