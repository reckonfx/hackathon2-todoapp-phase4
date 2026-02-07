"""
Conversation service for the Phase III Chat API.
Handles business logic for conversation operations with async database support.
Spec Reference: DER-005 to DER-010, PGR-001 to PGR-005
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from sqlalchemy.sql import func
from ..models.conversation import Conversation
import uuid


async def create_conversation(
    db: AsyncSession,
    user_id: str,
    title: Optional[str] = None
) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        db: Database session
        user_id: UUID of the user
        title: Optional title for the conversation

    Returns:
        The created Conversation object

    Spec Reference: DER-005, DER-006
    """
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

    db_conversation = Conversation(
        user_id=u_id,
        title=title
    )

    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)

    return db_conversation


async def get_conversation(
    db: AsyncSession,
    conversation_id: str,
    user_id: str
) -> Optional[Conversation]:
    """
    Get a conversation by ID, verifying user ownership.

    Args:
        db: Database session
        conversation_id: UUID of the conversation
        user_id: UUID of the user (for ownership verification)

    Returns:
        The Conversation object if found and owned by user, None otherwise

    Spec Reference: ACR-007 (user can only access own conversations)
    """
    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

    result = await db.execute(
        select(Conversation).filter(
            Conversation.id == c_id,
            Conversation.user_id == u_id
        )
    )

    return result.scalar_one_or_none()


async def get_conversation_by_id(
    db: AsyncSession,
    conversation_id: str
) -> Optional[Conversation]:
    """
    Get a conversation by ID without user verification.
    Use only for internal operations where user is already verified.

    Args:
        db: Database session
        conversation_id: UUID of the conversation

    Returns:
        The Conversation object if found, None otherwise
    """
    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id

    result = await db.execute(
        select(Conversation).filter(Conversation.id == c_id)
    )

    return result.scalar_one_or_none()


async def update_conversation_timestamp(
    db: AsyncSession,
    conversation_id: str
) -> None:
    """
    Update the conversation's updated_at timestamp.
    Called after adding new messages.

    Args:
        db: Database session
        conversation_id: UUID of the conversation

    Spec Reference: DER-010
    """
    c_id = uuid.UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id

    await db.execute(
        update(Conversation)
        .where(Conversation.id == c_id)
        .values(updated_at=func.now())
    )
    await db.commit()


async def get_user_conversations(
    db: AsyncSession,
    user_id: str,
    limit: int = 50
) -> List[Conversation]:
    """
    Get all conversations for a user, ordered by most recent.

    Args:
        db: Database session
        user_id: UUID of the user
        limit: Maximum number of conversations to return

    Returns:
        List of Conversation objects
    """
    u_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

    result = await db.execute(
        select(Conversation)
        .filter(Conversation.user_id == u_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )

    return list(result.scalars().all())


async def delete_conversation(
    db: AsyncSession,
    conversation_id: str,
    user_id: str
) -> bool:
    """
    Delete a conversation and all its messages (cascade).

    Args:
        db: Database session
        conversation_id: UUID of the conversation
        user_id: UUID of the user (for ownership verification)

    Returns:
        True if deleted, False if not found or not owned by user

    Spec Reference: DER-020, DER-021 (cascade delete)
    """
    conversation = await get_conversation(db, conversation_id, user_id)

    if not conversation:
        return False

    await db.delete(conversation)
    await db.commit()

    return True
