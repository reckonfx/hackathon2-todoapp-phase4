"""
Schemas package for the Phase-2/3 Web-Based Todo Application.
Contains Pydantic models for API request/response validation.

Phase II:
- TaskCreate, TaskUpdate, TaskInDB, TaskPublic, TaskToggle
- UserCreate, UserUpdate, UserInDB

Phase III:
- ChatRequest, ChatResponse, ToolCall, ErrorResponse
"""

from .task_schema import TaskCreate, TaskUpdate, TaskInDB, TaskPublic, TaskToggle
from .user_schema import UserCreate, UserInDB
from .chat_schema import (
    ChatRequest,
    ChatResponse,
    ToolCall,
    ErrorResponse,
    ValidationErrorDetail,
    ConversationInfo,
    MessageInfo
)

__all__ = [
    # Phase II - Tasks
    "TaskCreate",
    "TaskUpdate",
    "TaskInDB",
    "TaskPublic",
    "TaskToggle",
    # Phase II - Users
    "UserCreate",
    "UserInDB",
    # Phase III - Chat
    "ChatRequest",
    "ChatResponse",
    "ToolCall",
    "ErrorResponse",
    "ValidationErrorDetail",
    "ConversationInfo",
    "MessageInfo",
]