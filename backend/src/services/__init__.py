"""
Services package for the Phase-2/3 Web-Based Todo Application.
Contains business logic and service layer implementations.

Phase II:
- task_service: Task CRUD operations
- auth_service: Authentication operations

Phase III:
- conversation_service: Conversation CRUD operations
- message_service: Message persistence operations
- chat_service: Chat orchestration (agent integration)
"""

from . import task_service
from . import auth_service
from . import conversation_service
from . import message_service