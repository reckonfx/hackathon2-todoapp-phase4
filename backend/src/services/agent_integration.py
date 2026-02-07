"""
Agent Integration service for the Phase III Chat API.
Connects to OpenAI for AI-powered conversation and tool execution.
Spec Reference: research.md R2 (per-request agent instance)
"""

from typing import Dict, Any, List, Optional
import os
import logging
import json

logger = logging.getLogger(__name__)


async def invoke_agent(
    user_id: str,
    message: str,
    history: List[Dict[str, Any]]
) -> tuple[str, List[Dict[str, Any]]]:
    """
    Invoke the AI agent with a message and conversation history.

    Args:
        user_id: The authenticated user's ID
        message: Current user message
        history: Previous conversation messages

    Returns:
        Tuple of (response_text, tool_calls_list)

    Spec Reference:
        - research.md R2: Create agent instance per request
        - ABR-022: Agent stores no internal state between requests
    """
    try:
        # Try to use OpenAI API
        from openai import AsyncOpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set, using mock response")
            return _mock_response(message, history)

        client = AsyncOpenAI(api_key=api_key)

        # Import tool schemas
        from ..mcp.server import get_tool_schemas

        # Build messages for OpenAI
        messages = _build_messages(message, history, user_id)
        tools = get_tool_schemas()

        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Process response
        assistant_message = response.choices[0].message
        response_text = assistant_message.content or ""
        tool_calls = []

        # Handle tool calls in a loop until the AI is done
        all_tool_calls = []
        current_messages = messages.copy()
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        while assistant_message.tool_calls and iteration < max_iterations:
            iteration += 1
            logger.info(f"Processing tool calls, iteration {iteration}")

            # Execute tool calls
            new_tool_calls = await _handle_tool_calls(
                user_id=user_id,
                tool_calls=assistant_message.tool_calls
            )
            all_tool_calls.extend(new_tool_calls)

            # Add assistant message with tool calls to conversation
            current_messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })

            # Add tool results
            for i, tc in enumerate(assistant_message.tool_calls):
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(new_tool_calls[i]["result"])
                })

            # Get next response - still allow tool calls
            next_response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=current_messages,
                tools=tools,
                tool_choice="auto"
            )

            assistant_message = next_response.choices[0].message
            response_text = assistant_message.content or ""

        return response_text, all_tool_calls

    except ImportError:
        logger.warning("OpenAI package not available, using mock response")
        return _mock_response(message, history)
    except Exception as e:
        logger.error(f"Agent invocation failed: {e}", exc_info=True)
        raise


def _build_messages(
    message: str,
    history: List[Dict[str, Any]],
    user_id: str
) -> List[Dict[str, str]]:
    """Build the messages array for OpenAI API."""
    messages = [
        {
            "role": "system",
            "content": f"""You are a helpful task management assistant. Your job is to help users manage their todo list.

You have access to these tools:
- add_task: Create a new task
- list_tasks: Show the user's tasks
- complete_task: Mark a task as done
- delete_task: Remove a task
- update_task: Modify a task

Guidelines:
- Always use tools to perform task operations - never pretend or make up task information
- Be concise but friendly in your responses
- When listing tasks, format them nicely with numbers
- Confirm actions after completing them
- If a user's intent is unclear, ask for clarification
- The user's ID is: {user_id}

Important: When calling tools that require a task_id, you must first use list_tasks to find the correct ID."""
        }
    ]

    # Add conversation history
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current message
    messages.append({
        "role": "user",
        "content": message
    })

    return messages


async def _handle_tool_calls(
    user_id: str,
    tool_calls: list
) -> List[Dict[str, Any]]:
    """
    Execute tool calls and return results.

    Args:
        user_id: The authenticated user's ID
        tool_calls: List of tool calls from OpenAI

    Returns:
        List of tool call results in our format
    """
    from ..mcp.server import invoke_tool
    from ..database.connection import get_session_makers

    results = []

    # Get database session
    async_session_maker, _, _ = get_session_makers()

    async with async_session_maker() as db:
        for tc in tool_calls:
            tool_name = tc.function.name
            try:
                parameters = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                parameters = {}

            # Save a copy of parameters before invoke_tool modifies it
            saved_parameters = parameters.copy()

            # Execute tool (this modifies parameters by adding db, user_id)
            result = await invoke_tool(
                db=db,
                user_id=user_id,
                tool_name=tool_name,
                parameters=parameters
            )

            # Use saved_parameters (without db) for storage
            results.append({
                "tool": tool_name,
                "parameters": saved_parameters,
                "result": result
            })

    return results


def _mock_response(
    message: str,
    history: List[Dict[str, Any]]
) -> tuple[str, List[Dict[str, Any]]]:
    """
    Generate a mock response for testing when OpenAI is not available.

    This is used during development/testing before OpenAI integration.
    """
    message_lower = message.lower()
    tool_calls = []

    if any(word in message_lower for word in ['add', 'create', 'new task', 'remember']):
        # Extract potential task title
        title = message
        for word in ['add', 'create', 'new task', 'remember', 'to my list', 'to my tasks']:
            title = title.lower().replace(word, '').strip()

        if not title:
            title = "New task"

        return (
            f"I'd add '{title}' to your tasks. (OpenAI integration pending - set OPENAI_API_KEY)",
            [{
                "tool": "add_task",
                "parameters": {"title": title},
                "result": {"success": True, "message": "Mock response"}
            }]
        )

    elif any(word in message_lower for word in ['show', 'list', 'my tasks', 'what tasks']):
        return (
            "I'd show your tasks here. (OpenAI integration pending - set OPENAI_API_KEY)",
            [{
                "tool": "list_tasks",
                "parameters": {},
                "result": {"success": True, "tasks": [], "count": 0}
            }]
        )

    elif any(word in message_lower for word in ['done', 'complete', 'finished']):
        return (
            "I'd mark that task as complete. (OpenAI integration pending - set OPENAI_API_KEY)",
            [{
                "tool": "complete_task",
                "parameters": {"task_id": "mock"},
                "result": {"success": True, "message": "Mock response"}
            }]
        )

    elif any(word in message_lower for word in ['delete', 'remove']):
        return (
            "I'd delete that task. (OpenAI integration pending - set OPENAI_API_KEY)",
            [{
                "tool": "delete_task",
                "parameters": {"task_id": "mock"},
                "result": {"success": True, "message": "Mock response"}
            }]
        )

    else:
        return (
            f"I received: '{message}'. How can I help you manage your tasks? (OpenAI integration pending - set OPENAI_API_KEY)",
            []
        )
