# Feature Specification: AI Agent Behavior & MCP Tool Contracts

**Feature Branch**: `003-agent-mcp-tools`
**Created**: 2026-01-28
**Status**: Draft
**Phase**: III (AI-Powered Todo Chatbot)

## Overview

This specification defines the behavioral contract for the Todo AI Chatbot agent and the MCP (Model Context Protocol) server tools used for task management. The agent acts as the conversational interface while MCP tools provide the atomic operations for task manipulation.

**Constitutional Reference**: This spec implements Phase III Addendum §14.2.2 (Agent-Tool Determinism) and §14.3 (Phase III Standards).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation (Priority: P1)

A user sends a natural language message like "Add buy groceries to my list" and the agent correctly interprets the intent, invokes the appropriate MCP tool, and confirms the action.

**Why this priority**: Task creation is the most fundamental operation. Without it, no other functionality has meaning.

**Independent Test**: Can be fully tested by sending a create-intent message and verifying the tool is called with correct parameters and the response confirms creation.

**Acceptance Scenarios**:

1. **Given** a user with an active conversation, **When** user says "Add buy milk to my tasks", **Then** agent calls `add_task` with title "buy milk" and confirms "I've added 'buy milk' to your tasks."

2. **Given** a user message with additional details, **When** user says "Add call mom tomorrow, it's important", **Then** agent calls `add_task` with title "call mom", due_date "tomorrow", priority "high" and confirms with all details.

3. **Given** an ambiguous message, **When** user says "remember eggs", **Then** agent interprets as task creation and calls `add_task` with title "eggs" (inferred intent: add to list).

---

### User Story 2 - Task Listing and Querying (Priority: P1)

A user asks to see their tasks and the agent retrieves and presents them in a readable format.

**Why this priority**: Users must be able to view tasks to manage them. This is equally critical as creation.

**Independent Test**: Can be tested by requesting task list and verifying the `list_tasks` tool is called and results are presented clearly.

**Acceptance Scenarios**:

1. **Given** a user with existing tasks, **When** user says "Show my tasks", **Then** agent calls `list_tasks` and presents tasks in a numbered, readable format.

2. **Given** a user asking for filtered view, **When** user says "What tasks are due today?", **Then** agent calls `list_tasks` with appropriate filter and presents only matching tasks.

3. **Given** a user with no tasks, **When** user says "List my todos", **Then** agent calls `list_tasks`, receives empty result, and responds "You don't have any tasks yet."

---

### User Story 3 - Task Completion (Priority: P2)

A user marks a task as complete through natural language and the agent confirms the action.

**Why this priority**: Completing tasks is the core value proposition of a todo app, but depends on tasks existing first.

**Independent Test**: Can be tested by requesting completion of an existing task and verifying `complete_task` is called and confirmation is returned.

**Acceptance Scenarios**:

1. **Given** a user with a task "buy milk", **When** user says "I bought the milk", **Then** agent identifies the task, calls `complete_task` with the task ID, and confirms "Great! I've marked 'buy milk' as complete."

2. **Given** multiple similar tasks exist, **When** user says "Done with the meeting task", **Then** agent asks for clarification: "I found multiple tasks with 'meeting'. Which one did you complete?" and lists options.

3. **Given** no matching task exists, **When** user says "Complete the xyz task", **Then** agent responds "I couldn't find a task matching 'xyz'. Would you like to see your current tasks?"

---

### User Story 4 - Task Deletion (Priority: P2)

A user requests to delete a task and the agent confirms before executing the destructive action.

**Why this priority**: Deletion is important but less frequent than completion. Requires confirmation due to destructive nature.

**Independent Test**: Can be tested by requesting deletion and verifying confirmation prompt appears before `delete_task` is called.

**Acceptance Scenarios**:

1. **Given** a user with a task "old reminder", **When** user says "Delete old reminder", **Then** agent asks "Are you sure you want to delete 'old reminder'? This cannot be undone." and waits for confirmation.

2. **Given** user confirms deletion, **When** user says "Yes, delete it", **Then** agent calls `delete_task` and confirms "I've deleted 'old reminder' from your tasks."

3. **Given** user cancels deletion, **When** user says "No, keep it", **Then** agent responds "Okay, I'll keep 'old reminder' in your tasks." and does NOT call `delete_task`.

---

### User Story 5 - Task Updates (Priority: P3)

A user modifies an existing task's details through natural language.

**Why this priority**: Updates are valuable but less common than CRUD basics.

**Independent Test**: Can be tested by requesting a task update and verifying `update_task` is called with correct parameters.

**Acceptance Scenarios**:

1. **Given** a task "meeting at 3pm", **When** user says "Change meeting to 4pm", **Then** agent calls `update_task` with the task ID and new time, confirms "I've updated the meeting time to 4pm."

2. **Given** a task with no priority, **When** user says "Make the groceries task high priority", **Then** agent calls `update_task` with priority "high" and confirms the change.

---

### Edge Cases

- **Ambiguous intent**: User says "groceries" without verb - agent asks "Would you like me to add 'groceries' as a new task?"
- **Multiple matches**: User references task that matches multiple items - agent lists options and asks for clarification
- **Non-existent task**: User tries to complete/delete task that doesn't exist - agent informs user and offers alternatives
- **Empty task title**: User says "Add" without content - agent asks "What would you like to add?"
- **Server unavailable**: MCP tool fails - agent responds "I'm having trouble updating your tasks right now. Please try again."
- **Rate limiting**: Too many requests - agent responds gracefully without exposing system details

---

## Phase Context & Constraints *(Phase-III)*

- **Persistence**: Database-backed (all state in PostgreSQL via MCP tools)
- **Interface**: Conversational chat
- **Intelligence**: OpenAI Agents SDK with MCP tool integration
- **Statelessness**: Agent and MCP server are stateless; all state reconstructed from database
- **External Specs**: Constitution §14 (Phase III Addendum), API Spec (TBD)

---

## Requirements *(mandatory)*

### Agent Behavioral Requirements

#### Intent Recognition

- **ABR-001**: Agent MUST recognize task creation intents from phrases like "add", "create", "remember", "new task", "todo"
- **ABR-002**: Agent MUST recognize listing intents from phrases like "show", "list", "what are my", "display"
- **ABR-003**: Agent MUST recognize completion intents from phrases like "done", "complete", "finished", "mark as done"
- **ABR-004**: Agent MUST recognize deletion intents from phrases like "delete", "remove", "get rid of"
- **ABR-005**: Agent MUST recognize update intents from phrases like "change", "update", "modify", "rename"
- **ABR-006**: Agent MUST handle ambiguous messages by asking clarifying questions

#### Tool Selection Mapping

- **ABR-007**: Creation intent MUST map to `add_task` tool
- **ABR-008**: Listing intent MUST map to `list_tasks` tool
- **ABR-009**: Completion intent MUST map to `complete_task` tool
- **ABR-010**: Deletion intent MUST map to `delete_task` tool
- **ABR-011**: Update intent MUST map to `update_task` tool
- **ABR-012**: Agent MUST NOT perform task operations without invoking the corresponding MCP tool

#### Confirmation Behavior

- **ABR-013**: Agent MUST confirm all successful state-changing operations with human-readable response
- **ABR-014**: Agent MUST request explicit confirmation before destructive actions (delete)
- **ABR-015**: Agent MUST display task details in confirmation (title, due date, priority if set)
- **ABR-016**: Agent MUST handle user cancellation gracefully without executing the action

#### Error Handling

- **ABR-017**: Agent MUST inform user when a referenced task cannot be found
- **ABR-018**: Agent MUST offer alternatives when task matching is ambiguous
- **ABR-019**: Agent MUST provide user-friendly error messages (no technical details exposed)
- **ABR-020**: Agent MUST gracefully handle MCP tool failures without crashing conversation
- **ABR-021**: Agent MUST NOT retry failed operations without user consent

#### Prohibited Behaviors

- **ABR-022**: Agent MUST NOT store or reference any state internally between requests
- **ABR-023**: Agent MUST NOT fabricate task IDs, titles, or statuses not returned by tools
- **ABR-024**: Agent MUST NOT assume task existence without querying via `list_tasks`
- **ABR-025**: Agent MUST NOT perform implicit operations (e.g., auto-completing tasks)
- **ABR-026**: Agent MUST NOT bypass MCP tools for any task manipulation
- **ABR-027**: Agent MUST NOT hallucinate task details or conversation history

---

### MCP Tool Requirements

#### General Tool Requirements

- **MTR-001**: All tools MUST be stateless (no internal state between calls)
- **MTR-002**: All tools MUST validate input parameters against schema before execution
- **MTR-003**: All tools MUST return consistent response schemas
- **MTR-004**: All tools MUST include operation timestamp in responses
- **MTR-005**: All tools MUST operate only via database layer (no direct memory manipulation)
- **MTR-006**: All tools MUST be idempotent where semantically appropriate

---

### Key Entities

- **Task**: A todo item belonging to a user with title, optional description, optional due date, priority level, and completion status
- **User**: The owner of tasks, identified by user_id passed to each tool
- **Conversation**: The chat session context (managed separately, not by MCP tools)

---

## MCP Tool Contracts

### Tool 1: `add_task`

**Purpose**: Creates a new task for the specified user.

**Parameters**:

| Parameter   | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| user_id     | string | Yes      | Unique identifier of the task owner              |
| title       | string | Yes      | Task title (1-500 characters)                    |
| description | string | No       | Extended task description (max 2000 characters)  |
| due_date    | string | No       | ISO 8601 date or relative ("tomorrow", "next week") |
| priority    | string | No       | "low", "medium", "high" (default: "medium")      |

**Return Schema**:

```
{
  "success": boolean,
  "task": {
    "id": string,
    "title": string,
    "description": string | null,
    "due_date": string | null,
    "priority": string,
    "completed": false,
    "created_at": string (ISO 8601)
  },
  "message": string
}
```

**Error Conditions**:

| Error Code | Condition                    | Message                              |
|------------|------------------------------|--------------------------------------|
| INVALID_TITLE | Title empty or too long   | "Task title must be 1-500 characters" |
| INVALID_USER  | User ID not found         | "User not found"                     |
| INVALID_DATE  | Date format unrecognized  | "Could not parse date"               |
| INVALID_PRIORITY | Priority not in allowed values | "Priority must be low, medium, or high" |

---

### Tool 2: `list_tasks`

**Purpose**: Retrieves tasks for the specified user with optional filtering.

**Parameters**:

| Parameter  | Type    | Required | Description                                      |
|------------|---------|----------|--------------------------------------------------|
| user_id    | string  | Yes      | Unique identifier of the task owner              |
| completed  | boolean | No       | Filter by completion status                      |
| priority   | string  | No       | Filter by priority level                         |
| due_before | string  | No       | Filter tasks due before this date (ISO 8601)     |
| due_after  | string  | No       | Filter tasks due after this date (ISO 8601)      |
| search     | string  | No       | Search term to match against title/description   |
| limit      | integer | No       | Maximum results to return (default: 50, max: 100)|

**Return Schema**:

```
{
  "success": boolean,
  "tasks": [
    {
      "id": string,
      "title": string,
      "description": string | null,
      "due_date": string | null,
      "priority": string,
      "completed": boolean,
      "created_at": string,
      "completed_at": string | null
    }
  ],
  "count": integer,
  "message": string
}
```

**Error Conditions**:

| Error Code     | Condition                | Message                    |
|----------------|--------------------------|----------------------------|
| INVALID_USER   | User ID not found        | "User not found"           |
| INVALID_FILTER | Invalid filter parameter | "Invalid filter: {detail}" |

---

### Tool 3: `complete_task`

**Purpose**: Marks a task as completed.

**Parameters**:

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| user_id   | string | Yes      | Unique identifier of the task owner |
| task_id   | string | Yes      | Unique identifier of the task       |

**Return Schema**:

```
{
  "success": boolean,
  "task": {
    "id": string,
    "title": string,
    "completed": true,
    "completed_at": string (ISO 8601)
  },
  "message": string
}
```

**Error Conditions**:

| Error Code        | Condition                      | Message                              |
|-------------------|--------------------------------|--------------------------------------|
| INVALID_USER      | User ID not found              | "User not found"                     |
| TASK_NOT_FOUND    | Task ID does not exist         | "Task not found"                     |
| UNAUTHORIZED      | Task belongs to different user | "You don't have access to this task" |
| ALREADY_COMPLETED | Task already marked complete   | "Task is already completed"          |

---

### Tool 4: `delete_task`

**Purpose**: Permanently removes a task.

**Parameters**:

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| user_id   | string | Yes      | Unique identifier of the task owner |
| task_id   | string | Yes      | Unique identifier of the task       |

**Return Schema**:

```
{
  "success": boolean,
  "deleted_task": {
    "id": string,
    "title": string
  },
  "message": string
}
```

**Error Conditions**:

| Error Code     | Condition                      | Message                              |
|----------------|--------------------------------|--------------------------------------|
| INVALID_USER   | User ID not found              | "User not found"                     |
| TASK_NOT_FOUND | Task ID does not exist         | "Task not found"                     |
| UNAUTHORIZED   | Task belongs to different user | "You don't have access to this task" |

---

### Tool 5: `update_task`

**Purpose**: Modifies one or more properties of an existing task.

**Parameters**:

| Parameter   | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| user_id     | string | Yes      | Unique identifier of the task owner              |
| task_id     | string | Yes      | Unique identifier of the task                    |
| title       | string | No       | New task title (1-500 characters)                |
| description | string | No       | New description (max 2000 characters, null to clear) |
| due_date    | string | No       | New due date (ISO 8601, null to clear)           |
| priority    | string | No       | New priority: "low", "medium", "high"            |
| completed   | boolean| No       | Set completion status                            |

**Return Schema**:

```
{
  "success": boolean,
  "task": {
    "id": string,
    "title": string,
    "description": string | null,
    "due_date": string | null,
    "priority": string,
    "completed": boolean,
    "updated_at": string (ISO 8601)
  },
  "changes": [string],  // List of fields that were modified
  "message": string
}
```

**Error Conditions**:

| Error Code       | Condition                      | Message                              |
|------------------|--------------------------------|--------------------------------------|
| INVALID_USER     | User ID not found              | "User not found"                     |
| TASK_NOT_FOUND   | Task ID does not exist         | "Task not found"                     |
| UNAUTHORIZED     | Task belongs to different user | "You don't have access to this task" |
| NO_CHANGES       | No update parameters provided  | "No changes specified"               |
| INVALID_TITLE    | Title empty or too long        | "Task title must be 1-500 characters"|
| INVALID_PRIORITY | Priority not in allowed values | "Priority must be low, medium, or high" |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task via natural language in under 5 seconds end-to-end
- **SC-002**: 95% of user intents are correctly classified on the first attempt
- **SC-003**: Agent provides confirmation for 100% of successful state-changing operations
- **SC-004**: Agent requests confirmation for 100% of destructive operations before execution
- **SC-005**: 0% of agent responses contain fabricated/hallucinated task information
- **SC-006**: System recovers gracefully from 100% of MCP tool failures with user-friendly messages
- **SC-007**: Users can complete a full task lifecycle (create → list → complete → delete) in under 2 minutes
- **SC-008**: Agent correctly handles ambiguous queries by asking clarification 100% of the time

---

## Assumptions

1. **User Authentication**: User identity (user_id) is established before agent interaction begins
2. **Conversation Context**: Conversation history is provided to the agent for context (managed by API layer)
3. **Date Parsing**: Natural language dates ("tomorrow", "next week") are parsed to ISO 8601 by the MCP tool
4. **Task Matching**: When user references a task by name, the system searches by title substring match
5. **Priority Default**: Tasks created without explicit priority default to "medium"
6. **Idempotency**: `complete_task` is idempotent - calling on already-completed task returns success with note
7. **Soft Delete**: Deletion is permanent (no soft delete) - this is intentional per user expectations for todo apps

---

## Dependencies

- **Constitution**: Phase III Addendum (§14) defines architectural constraints
- **API Specification**: Chat endpoint spec (TBD) defines how agent is invoked
- **Data Model**: Task and User schemas defined in database model spec (TBD)
