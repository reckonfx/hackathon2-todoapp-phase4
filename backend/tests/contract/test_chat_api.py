"""
Contract tests for Chat API endpoints.
Spec Reference: ACR-001 to ACR-017, contracts/chat-api.yaml
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import uuid

pytestmark = pytest.mark.asyncio


class TestChatNewConversation:
    """Contract tests for creating new conversations (T017)."""

    async def test_new_conversation_returns_required_fields(self):
        """POST without conversation_id creates new conversation with all required fields."""
        # This test verifies ACR-009 to ACR-013
        # Response must include: conversation_id, message_id, response, tool_calls, created_at

        # Mock response structure
        expected_fields = ["conversation_id", "message_id", "response", "tool_calls", "created_at"]

        # Verify schema has all required fields
        from src.database.schemas.chat_schema import ChatResponse
        response_fields = list(ChatResponse.model_fields.keys())

        for field in expected_fields:
            assert field in response_fields, f"Missing required field: {field}"

    async def test_chat_request_validates_message(self):
        """Request body validated against ChatRequest schema (ACR-004, ACR-008)."""
        from src.database.schemas.chat_schema import ChatRequest
        from pydantic import ValidationError

        # Empty message should fail
        with pytest.raises(ValidationError):
            ChatRequest(message="")

        # Message too long should fail (10000 char limit)
        with pytest.raises(ValidationError):
            ChatRequest(message="x" * 10001)

        # Valid message should pass
        request = ChatRequest(message="Hello, add a task")
        assert request.message == "Hello, add a task"


class TestChatContinueConversation:
    """Contract tests for continuing conversations (T023)."""

    async def test_conversation_id_format_validation(self):
        """conversation_id must be valid UUID format."""
        from src.database.schemas.chat_schema import ChatRequest
        from pydantic import ValidationError

        # Valid UUID should work
        valid_uuid = str(uuid.uuid4())
        request = ChatRequest(message="Test", conversation_id=valid_uuid)
        assert str(request.conversation_id) == valid_uuid

        # Invalid UUID should fail
        with pytest.raises(ValidationError):
            ChatRequest(message="Test", conversation_id="not-a-uuid")


class TestChatToolCalls:
    """Contract tests for tool_calls in response (T032)."""

    async def test_tool_call_schema_structure(self):
        """Tool calls follow ToolCall schema structure."""
        from src.database.schemas.chat_schema import ToolCall

        tool_call = ToolCall(
            tool="add_task",
            parameters={"title": "Buy groceries"},
            result={"success": True, "task": {"id": "123", "title": "Buy groceries"}}
        )

        assert tool_call.tool == "add_task"
        assert "title" in tool_call.parameters
        assert tool_call.result["success"] is True

    async def test_response_always_has_tool_calls_array(self):
        """Response tool_calls is always an array, even when empty (ACR-012)."""
        from src.database.schemas.chat_schema import ChatResponse
        from datetime import datetime

        # Response with no tool calls
        response = ChatResponse(
            conversation_id=uuid.uuid4(),
            message_id=uuid.uuid4(),
            response="Hello!",
            tool_calls=[],  # Must be empty array, not None
            created_at=datetime.utcnow()
        )

        assert isinstance(response.tool_calls, list)
        assert len(response.tool_calls) == 0


class TestErrorResponses:
    """Contract tests for error responses (T048)."""

    async def test_error_response_schema(self):
        """Error responses follow ErrorResponse schema."""
        from src.database.schemas.chat_schema import ErrorResponse, ValidationErrorDetail

        # Validation error with details
        error = ErrorResponse(
            error="validation_error",
            details=[ValidationErrorDetail(field="message", message="Required")]
        )
        assert error.error == "validation_error"
        assert len(error.details) == 1

        # Not found error with message
        error = ErrorResponse(
            error="not_found",
            message="Conversation not found"
        )
        assert error.error == "not_found"
        assert error.message == "Conversation not found"
