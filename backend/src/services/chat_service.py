"""
Chat service for the Phase III Chat API.
Orchestrates conversation flow between API, database, and AI agent.
Spec Reference: SFR-001 to SFR-013, research.md R2, R7
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import os

from . import conversation_service
from . import message_service
from ..models.conversation import Conversation
from ..models.message import Message

# Configure logging
logger = logging.getLogger(__name__)


class ChatService:
    """
    Stateless chat orchestration service.

    This service coordinates:
    1. Conversation creation/lookup
    2. Message persistence (user message BEFORE agent, assistant AFTER)
    3. Agent invocation with context reconstruction
    4. Response formatting

    Spec Reference:
        - SFR-001: Stateless operation (no in-memory state)
        - SFR-002: Context reconstruction from database
        - SFR-003: User message persisted before agent
        - SFR-004: Assistant message persisted after agent
    """

    def __init__(self, db: AsyncSession, user_id: str):
        """
        Initialize chat service for a specific request.

        Args:
            db: Database session
            user_id: Authenticated user's ID
        """
        self.db = db
        self.user_id = user_id

    async def process_message(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return assistant response.

        Args:
            message: User's message text
            conversation_id: Optional existing conversation ID

        Returns:
            Dict containing conversation_id, message_id, response, tool_calls, created_at

        Spec Reference:
            - ACR-006: New conversation created if conversation_id not provided
            - ACR-007: Existing conversation loaded if conversation_id provided
            - SFR-003: User message persisted BEFORE agent
            - SFR-004: Assistant message persisted AFTER agent
        """
        # Step 1: Get or create conversation
        if conversation_id:
            conversation = await self._get_existing_conversation(conversation_id)
        else:
            conversation = await self._create_new_conversation()

        # Step 2: Persist user message BEFORE agent (SFR-003)
        user_message = await message_service.create_user_message(
            db=self.db,
            conversation_id=str(conversation.id),
            content=message
        )
        logger.info(f"User message persisted: {user_message.id}")

        # Step 3: Load conversation history for context (SFR-002, SFR-006)
        history = await self._load_conversation_history(str(conversation.id))

        # Step 4: Invoke agent with context
        try:
            agent_response, tool_calls = await self._invoke_agent(message, history)
        except Exception as e:
            # Error recovery: record failure in assistant message (research.md R7)
            logger.error(f"Agent invocation failed: {e}")
            agent_response = "[System: Request failed. Please try again.]"
            tool_calls = []

        # Step 5: Persist assistant message AFTER agent (SFR-004)
        assistant_message = await message_service.create_assistant_message(
            db=self.db,
            conversation_id=str(conversation.id),
            content=agent_response,
            tool_calls=tool_calls if tool_calls else None
        )
        logger.info(f"Assistant message persisted: {assistant_message.id}")

        # Step 6: Update conversation timestamp
        await conversation_service.update_conversation_timestamp(
            db=self.db,
            conversation_id=str(conversation.id)
        )

        # Step 7: Return response
        return {
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "response": agent_response,
            "tool_calls": tool_calls or [],
            "created_at": assistant_message.created_at
        }

    async def _create_new_conversation(self) -> Conversation:
        """Create a new conversation for the user."""
        conversation = await conversation_service.create_conversation(
            db=self.db,
            user_id=self.user_id
        )
        logger.info(f"New conversation created: {conversation.id}")
        return conversation

    async def _get_existing_conversation(self, conversation_id: str) -> Conversation:
        """
        Get existing conversation, verifying user ownership.

        Raises:
            ValueError: If conversation not found or not owned by user
        """
        conversation = await conversation_service.get_conversation(
            db=self.db,
            conversation_id=conversation_id,
            user_id=self.user_id
        )

        if not conversation:
            raise ValueError("Conversation not found")

        logger.info(f"Existing conversation loaded: {conversation.id}")
        return conversation

    async def _load_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Load conversation history for agent context.

        Args:
            conversation_id: UUID of the conversation
            limit: Maximum messages to load (default 50 per research.md R4)

        Returns:
            List of message dicts with role and content

        Spec Reference: SFR-006, SFR-007
        """
        messages = await message_service.get_messages_for_conversation(
            db=self.db,
            conversation_id=conversation_id,
            limit=limit
        )

        # Format for agent context
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content
            })

        return history

    async def _invoke_agent(
        self,
        message: str,
        history: List[Dict[str, Any]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Invoke the AI agent with message and context.

        Args:
            message: Current user message
            history: Conversation history for context

        Returns:
            Tuple of (response_text, tool_calls_list)

        Spec Reference: research.md R2 (per-request agent instance)
        """
        # Import agent integration (will be implemented in T020)
        try:
            from .agent_integration import invoke_agent
            return await invoke_agent(
                user_id=self.user_id,
                message=message,
                history=history
            )
        except ImportError:
            # Fallback for development/testing before agent integration
            logger.warning("Agent integration not available, using mock response")
            return await self._mock_agent_response(message, history)

    async def _mock_agent_response(
        self,
        message: str,
        history: List[Dict[str, Any]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Mock agent response for testing before OpenAI integration.

        This will be replaced by actual agent integration in T020.
        """
        # Simple echo response for testing
        response = f"I received your message: '{message}'. Agent integration pending."
        tool_calls = []

        # Detect simple intents for basic testing
        message_lower = message.lower()

        if any(word in message_lower for word in ['add', 'create', 'new task']):
            # Extract task title (simple heuristic)
            title = message.replace('add', '').replace('create', '').replace('new task', '').strip()
            if not title:
                title = "New task"

            response = f"I would add '{title}' to your tasks. (Agent integration pending)"
            tool_calls = [{
                "tool": "add_task",
                "parameters": {"user_id": self.user_id, "title": title},
                "result": {"success": True, "message": "Mock - agent integration pending"}
            }]

        elif any(word in message_lower for word in ['show', 'list', 'my tasks']):
            response = "I would show your tasks here. (Agent integration pending)"
            tool_calls = [{
                "tool": "list_tasks",
                "parameters": {"user_id": self.user_id},
                "result": {"success": True, "tasks": [], "count": 0}
            }]

        return response, tool_calls


async def process_chat_message(
    db: AsyncSession,
    user_id: str,
    message: str,
    conversation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to process a chat message.

    This is the main entry point for the chat API route.

    Args:
        db: Database session
        user_id: Authenticated user's ID
        message: User's message text
        conversation_id: Optional existing conversation ID

    Returns:
        Dict containing conversation_id, message_id, response, tool_calls, created_at
    """
    service = ChatService(db=db, user_id=user_id)
    return await service.process_message(
        message=message,
        conversation_id=conversation_id
    )
