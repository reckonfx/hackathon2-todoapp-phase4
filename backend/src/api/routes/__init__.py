"""
Routes package for the Phase-2/3 Web-Based Todo Application.
Contains individual route modules for different API sections.

Phase II:
- auth: Authentication routes (register, login, logout)
- tasks: Task CRUD routes

Phase III:
- chat: Conversational chat endpoint for AI-powered task management
"""

from . import auth
from . import tasks
from . import chat

__all__ = ["auth", "tasks", "chat"]