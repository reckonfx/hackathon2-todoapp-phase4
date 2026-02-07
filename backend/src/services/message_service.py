"""
Message service for the Phase III Chat API.
Handles business logic for message persistence with async database support.
Spec Reference: DER-011 to DER-018, SFR-003 to SFR-007
"""

from typing import Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.message import Message
import uuid


async def create_message(
    db: AsyncSession,
    conversation_id: str,
    role: str,
    content: str,
    tool_calls: Optional[List[Dict[str, Any]]] = None
) -> Message:
    """
    Create a new message within a conversation.

    Args:
        db: Database session
        conversation_id: UUID of the parent conversation
        role: Message sender ('user' or 'assistant')
        content: Message text content
        tool_calls: Optional list of MCP tool invocations (assistant only)

    Returns:
        The created Message object

    Spec Reference:
        - SFR-003: User message persisted BEFORE agent processing
        - SFR-004: Assistant message persisted AFTER agent processing
        - DER-014: Role must be 'user' or 'assistant'
        - DER-016: Content length 1-10000 characters
    """
    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id

    # Validate role
    if role not in ('user', 'assistant'):
        raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")

    # Validate content length
    if not content or len(content) < 1:
        raise ValueError("Message content cannot be empty")
    if len(content) > 10000:
        raise ValueError("Message content exceeds maximum length of 10000 characters")

    # tool_calls only valid for assistant messages
    if tool_calls and role != 'assistant':
        raise ValueError("tool_calls can only be set for assistant messages")

    db_message = Message(
        conversation_id=c_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )

    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    return db_message


async def get_messages_for_conversation(
    db: AsyncSession,
    conversation_id: str,
    limit: int = 50
) -> List[Message]:
    """
    Get messages for a conversation, ordered chronologically.

    Args:
        db: Database session
        conversation_id: UUID of the conversation
        limit: Maximum number of messages to return (default 50, per research.md R4)

    Returns:
        List of Message objects, ordered by created_at ASC

    Spec Reference:
        - SFR-006: Load conversation history from database
        - SFR-007: Messages ordered chronologically
        - research.md R4: Default limit of 50 messages
    """
    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id

    result = await db.execute(
        select(Message)
        .filter(Message.conversation_id == c_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )

    return list(result.scalars().all())


async def get_message_by_id(
    db: AsyncSession,
    message_id: str
) -> Optional[Message]:
    """
    Get a message by its ID.

    Args:
        db: Database session
        message_id: UUID of the message

    Returns:
        The Message object if found, None otherwise
    """
    m_id = uuid.UUID(message_id) if isinstance(message_id, str) else message_id

    result = await db.execute(
        select(Message).filter(Message.id == m_id)
    )

    return result.scalar_one_or_none()


async def get_message_count(
    db: AsyncSession,
    conversation_id: str
) -> int:
    """
    Get the count of messages in a conversation.

    Args:
        db: Database session
        conversation_id: UUID of the conversation

    Returns:
        Number of messages in the conversation
    """
    from sqlalchemy import func as sql_func

    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id

    result = await db.execute(
        select(sql_func.count(Message.id))
        .filter(Message.conversation_id == c_id)
    )

    return result.scalar() or 0


async def create_user_message(
    db: AsyncSession,
    conversation_id: str,
    content: str
) -> Message:
    """
    Convenience method to create a user message.

    Args:
        db: Database session
        conversation_id: UUID of the conversation
        content: User's message text

    Returns:
        The created Message object

    Spec Reference: SFR-003 (persist user message before agent)
    """
    return await create_message(
        db=db,
        conversation_id=conversation_id,
        role='user',
        content=content
    )


async def create_assistant_message(
    db: AsyncSession,
    conversation_id: str,
    content: str,
    tool_calls: Optional[List[Dict[str, Any]]] = None
) -> Message:
    """
    Convenience method to create an assistant message.

    Args:
        db: Database session
        conversation_id: UUID of the conversation
        content: Assistant's response text
        tool_calls: Optional list of MCP tool invocations

    Returns:
        The created Message object

    Spec Reference: SFR-004 (persist assistant message after agent)
    """
    return await create_message(
        db=db,
        conversation_id=conversation_id,
        role='assistant',
        content=content,
        tool_calls=tool_calls
    )
