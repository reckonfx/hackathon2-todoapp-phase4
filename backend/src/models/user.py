"""
User model for the Phase-2 Web-Based Todo Application.
Defines the User SQLAlchemy ORM model.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from ..database.connection import Base


class User(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships (Phase III)
    # conversations relationship defined here to avoid circular imports
    # conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"