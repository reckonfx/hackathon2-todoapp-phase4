"""
Chat routes for the Phase III Chat API.
Defines API endpoint for conversational task management.
Spec Reference: ACR-001 to ACR-017
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from uuid import UUID
import logging

from ...database.deps import get_db
from ...database.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    ToolCall
)
from ...services.chat_service import process_chat_message
from ...models.user import User
from ...database.connection import settings

router = APIRouter(tags=["chat"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger(__name__)


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current user from the JWT token.

    Spec Reference: ACR-002, ACR-003 (authentication required)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.email == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def verify_user_id_matches(
    user_id: str = Path(..., description="User ID from path"),
    current_user: User = Depends(get_current_user_from_token)
) -> User:
    """
    Verify that the path user_id matches the authenticated user.

    Spec Reference: ACR-003 (user_id in path must match authenticated user)
    """
    try:
        path_user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    if path_user_uuid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID does not match authenticated user"
        )

    return current_user


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Send a chat message",
    description="""
    Process a user message through the AI agent and return the assistant's response.

    **Stateless Operation**:
    - Conversation context is reconstructed from database on each request
    - User message is persisted before agent execution
    - Assistant message is persisted after agent execution

    **Spec References**: ACR-001 to ACR-017
    """
)
async def send_chat_message(
    request: ChatRequest,
    current_user: User = Depends(verify_user_id_matches),
    db: AsyncSession = Depends(get_db)
) -> ChatResponse:
    """
    Send a chat message and receive assistant response.

    Spec Reference:
        - ACR-001: Endpoint accepts POST requests
        - ACR-004: Request body validated against ChatRequest schema
        - ACR-006: New conversation created if conversation_id not provided
        - ACR-007: Existing conversation validated if conversation_id provided
        - ACR-009 to ACR-013: Response includes all required fields
    """
    logger.info(f"Chat request from user {current_user.id}: message_length={len(request.message)}")

    try:
        # Process the message through chat service
        result = await process_chat_message(
            db=db,
            user_id=str(current_user.id),
            message=request.message,
            conversation_id=str(request.conversation_id) if request.conversation_id else None
        )

        # Convert tool_calls to proper schema
        tool_calls = [
            ToolCall(
                tool=tc["tool"],
                parameters=tc["parameters"],
                result=tc["result"]
            )
            for tc in result.get("tool_calls", [])
        ]

        logger.info(
            f"Chat response: conversation_id={result['conversation_id']}, "
            f"tool_calls_count={len(tool_calls)}"
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            message_id=result["message_id"],
            response=result["response"],
            tool_calls=tool_calls,
            created_at=result["created_at"]
        )

    except ValueError as e:
        # Conversation not found or validation error
        error_message = str(e)
        if "not found" in error_message.lower():
            logger.warning(f"Conversation not found: {request.conversation_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        else:
            logger.warning(f"Validation error: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

    except Exception as e:
        # Server error - log and return generic message
        logger.error(f"Chat processing error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your message"
        )
