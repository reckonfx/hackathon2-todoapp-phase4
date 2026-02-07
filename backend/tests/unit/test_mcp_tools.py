"""
Unit tests for MCP tools.
Spec Reference: 003-agent-mcp-tools spec (MTR-001 to MTR-006)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

# Mock the database models and session
pytestmark = pytest.mark.asyncio


class TestAddTask:
    """Tests for add_task MCP tool."""

    async def test_add_task_success(self):
        """Test successful task creation."""
        from src.mcp.tools.add_task import add_task

        # Mock database session
        mock_db = AsyncMock()
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()

        # Mock the select query for user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        result = await add_task(
            db=mock_db,
            user_id=str(mock_user.id),
            title="Test task",
            description="Test description",
            priority="high"
        )

        assert result["success"] is True
        assert result["message"] == "Task created successfully"
        assert "task" in result

    async def test_add_task_invalid_title_empty(self):
        """Test task creation with empty title fails."""
        from src.mcp.tools.add_task import add_task

        mock_db = AsyncMock()

        result = await add_task(
            db=mock_db,
            user_id=str(uuid.uuid4()),
            title=""
        )

        assert result["success"] is False
        assert result["error"] == "INVALID_TITLE"

    async def test_add_task_invalid_priority(self):
        """Test task creation with invalid priority fails."""
        from src.mcp.tools.add_task import add_task

        mock_db = AsyncMock()

        result = await add_task(
            db=mock_db,
            user_id=str(uuid.uuid4()),
            title="Test task",
            priority="invalid"
        )

        assert result["success"] is False
        assert result["error"] == "INVALID_PRIORITY"


class TestListTasks:
    """Tests for list_tasks MCP tool."""

    async def test_list_tasks_success(self):
        """Test successful task listing."""
        from src.mcp.tools.list_tasks import list_tasks

        mock_db = AsyncMock()
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()

        # Mock user query
        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_user

        # Mock tasks query
        mock_tasks_result = MagicMock()
        mock_tasks_result.scalars.return_value.all.return_value = []

        mock_db.execute.side_effect = [mock_user_result, mock_tasks_result]

        result = await list_tasks(
            db=mock_db,
            user_id=str(mock_user.id)
        )

        assert result["success"] is True
        assert "tasks" in result
        assert "count" in result


class TestCompleteTask:
    """Tests for complete_task MCP tool."""

    async def test_complete_task_not_found(self):
        """Test completing non-existent task."""
        from src.mcp.tools.complete_task import complete_task

        mock_db = AsyncMock()
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()

        # Mock user query
        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_user

        # Mock task query - not found
        mock_task_result = MagicMock()
        mock_task_result.scalar_one_or_none.return_value = None

        mock_db.execute.side_effect = [mock_user_result, mock_task_result]

        result = await complete_task(
            db=mock_db,
            user_id=str(mock_user.id),
            task_id=str(uuid.uuid4())
        )

        assert result["success"] is False
        assert result["error"] == "TASK_NOT_FOUND"


class TestDeleteTask:
    """Tests for delete_task MCP tool."""

    async def test_delete_task_unauthorized(self):
        """Test deleting another user's task."""
        from src.mcp.tools.delete_task import delete_task

        mock_db = AsyncMock()
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.id = uuid.uuid4()
        mock_task.user_id = uuid.uuid4()  # Different user

        # Mock user query
        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = mock_user

        # Mock task query
        mock_task_result = MagicMock()
        mock_task_result.scalar_one_or_none.return_value = mock_task

        mock_db.execute.side_effect = [mock_user_result, mock_task_result]

        result = await delete_task(
            db=mock_db,
            user_id=str(mock_user.id),
            task_id=str(mock_task.id)
        )

        assert result["success"] is False
        assert result["error"] == "UNAUTHORIZED"


class TestUpdateTask:
    """Tests for update_task MCP tool."""

    async def test_update_task_no_changes(self):
        """Test update with no changes specified."""
        from src.mcp.tools.update_task import update_task

        mock_db = AsyncMock()

        result = await update_task(
            db=mock_db,
            user_id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4())
            # No title, description, or completed specified
        )

        assert result["success"] is False
        assert result["error"] == "NO_CHANGES"
