""" User schemas for the Phase-2 Web-Based Todo Application.Pydantic models for request/response validation."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """Schema for user data in database."""

    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """Public user schema without sensitive data."""

    id: UUID

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserRegister(UserCreate):
    """Schema for user registration."""

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""

    username: Optional[str] = None