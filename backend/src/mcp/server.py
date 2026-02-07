"""
MCP Server for the Phase III Chat API.
Provides tool registration and invocation for the AI agent.
Spec Reference: research.md R3 (in-process MCP server using stdio transport)
"""

from typing import Dict, Any, Optional, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from .tools import add_task, list_tasks, complete_task, delete_task, delete_all_tasks, update_task

logger = logging.getLogger(__name__)


# Tool registry mapping tool names to their implementations
TOOL_REGISTRY: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "delete_all_tasks": delete_all_tasks,
    "update_task": update_task
}

# Tool schemas for OpenAI function calling
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user. Use this when the user wants to add, create, or remember something as a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title or name of the task (1-500 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional extended description of the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level of the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get the user's tasks. Use this when the user wants to see, show, list, or view their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "completed": {
                        "type": "boolean",
                        "description": "Filter by completion status. True for completed, False for pending."
                    },
                    "search": {
                        "type": "string",
                        "description": "Search term to filter tasks by title or description"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return (default 50, max 100)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed. Use this when the user has finished a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The unique ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently delete a task. Use this when the user wants to remove a task from their list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The unique ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_all_tasks",
            "description": "Permanently delete ALL tasks for the user. Use this when the user wants to remove all tasks, clear their task list, or start fresh. Always set confirm=true when calling this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be set to true to confirm deletion of all tasks"
                    }
                },
                "required": ["confirm"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task. Use this when the user wants to change the title, description, or status of a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The unique ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Set completion status"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]


async def invoke_tool(
    db: AsyncSession,
    user_id: str,
    tool_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Invoke an MCP tool by name with parameters.

    Args:
        db: Database session
        user_id: The authenticated user's ID
        tool_name: Name of the tool to invoke
        parameters: Tool parameters

    Returns:
        Tool execution result

    Raises:
        ValueError: If tool_name is not registered
    """
    if tool_name not in TOOL_REGISTRY:
        logger.error(f"Unknown tool: {tool_name}")
        return {
            "success": False,
            "error": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' not found"
        }

    tool_func = TOOL_REGISTRY[tool_name]

    # Add user_id to parameters (all tools require it)
    parameters["user_id"] = user_id
    parameters["db"] = db

    logger.info(f"Invoking tool: {tool_name} with params: {list(parameters.keys())}")

    try:
        result = await tool_func(**parameters)
        logger.info(f"Tool {tool_name} completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"Tool {tool_name} failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": "TOOL_EXECUTION_ERROR",
            "message": f"Tool execution failed: {str(e)}"
        }


def get_tool_schemas() -> list:
    """
    Get the tool schemas for OpenAI function calling.

    Returns:
        List of tool schema dictionaries in OpenAI format
    """
    return TOOL_SCHEMAS


def get_available_tools() -> list:
    """
    Get list of available tool names.

    Returns:
        List of tool name strings
    """
    return list(TOOL_REGISTRY.keys())
