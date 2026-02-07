"""
Chat schemas for the Phase III Chat API.
Pydantic models for request/response validation.
Spec Reference: ACR-004 to ACR-013, contracts/chat-api.yaml
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID


class ToolCall(BaseModel):
    """
    Schema for MCP tool invocation details.
    Spec Reference: ACR-012, contracts/chat-api.yaml ToolCall
    """
    tool: str = Field(
        ...,
        description="Name of the MCP tool invoked",
        examples=["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    )
    parameters: Dict[str, Any] = Field(
        ...,
        description="Parameters passed to the tool"
    )
    result: Dict[str, Any] = Field(
        ...,
        description="Result returned by the tool"
    )


class ChatRequest(BaseModel):
    """
    Schema for chat request payload.
    Spec Reference: ACR-004 to ACR-008
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User's message content"
    )
    conversation_id: Optional[UUID] = Field(
        default=None,
        description="UUID of existing conversation to continue. If omitted, a new conversation is created."
    )

    @field_validator('message')
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        """Validate message is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "message": "Add buy groceries to my list"
                },
                {
                    "message": "Also add milk",
                    "conversation_id": "660e8400-e29b-41d4-a716-446655440001"
                }
            ]
        }


class ChatResponse(BaseModel):
    """
    Schema for chat response payload.
    Spec Reference: ACR-009 to ACR-013
    """
    conversation_id: UUID = Field(
        ...,
        description="UUID of the conversation"
    )
    message_id: UUID = Field(
        ...,
        description="UUID of the assistant's response message"
    )
    response: str = Field(
        ...,
        description="Assistant's text response"
    )
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="List of MCP tool invocations (may be empty)"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp of the assistant's message"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
                "message_id": "770e8400-e29b-41d4-a716-446655440002",
                "response": "I've added 'buy groceries' to your tasks.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "parameters": {
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "buy groceries"
                        },
                        "result": {
                            "success": True,
                            "task": {
                                "id": "880e8400-e29b-41d4-a716-446655440003",
                                "title": "buy groceries"
                            }
                        }
                    }
                ],
                "created_at": "2026-01-28T12:00:00Z"
            }
        }


class ValidationErrorDetail(BaseModel):
    """Schema for individual validation error."""
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Validation failure reason")


class ErrorResponse(BaseModel):
    """
    Schema for error response payload.
    Spec Reference: ACR-014 to ACR-017
    """
    error: str = Field(
        ...,
        description="Error code",
        examples=["validation_error", "unauthorized", "not_found", "internal_error"]
    )
    message: Optional[str] = Field(
        default=None,
        description="Human-readable error message"
    )
    details: Optional[List[ValidationErrorDetail]] = Field(
        default=None,
        description="Detailed validation errors (for validation_error only)"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "error": "validation_error",
                    "details": [
                        {"field": "message", "message": "Message content is required"}
                    ]
                },
                {
                    "error": "not_found",
                    "message": "Conversation not found"
                },
                {
                    "error": "unauthorized",
                    "message": "Authentication required"
                }
            ]
        }


class ConversationInfo(BaseModel):
    """
    Schema for conversation info in lists.
    """
    id: UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageInfo(BaseModel):
    """
    Schema for message info.
    """
    id: UUID
    role: str
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    created_at: datetime

    class Config:
        from_attributes = True
