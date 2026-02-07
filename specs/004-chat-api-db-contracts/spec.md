# Feature Specification: Chat API & Database Contracts

**Feature Branch**: `004-chat-api-db-contracts`
**Created**: 2026-01-28
**Status**: Draft
**Phase**: III (AI-Powered Todo Chatbot)

## Overview

This specification defines the system-level contracts for the Phase III conversational interface, including the chat API endpoint, database extensions for conversation persistence, and the stateless request flow that enables conversation continuity without in-memory state.

**Constitutional Reference**: This spec implements Phase III Addendum §14.2.3 (Statelessness with Persistent Memory), §14.3 API Standards, and §14.5 (Data & Model Integrity).

**Dependency**: This spec depends on `003-agent-mcp-tools` for MCP tool contracts.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start New Conversation (Priority: P1)

A user opens the chat interface and sends their first message. The system creates a new conversation, processes the message through the AI agent, and returns a response.

**Why this priority**: The ability to start a conversation is the entry point to all functionality.

**Independent Test**: Can be tested by sending a message without a conversation_id and verifying a new conversation is created and response is returned.

**Acceptance Scenarios**:

1. **Given** a user with no active conversation, **When** user sends "Add buy groceries to my list", **Then** system creates a new conversation, persists the user message, invokes the agent, persists the assistant response, and returns the response with the new conversation_id.

2. **Given** a user with no prior conversations, **When** user sends first message, **Then** system assigns a unique conversation_id that can be used for all subsequent messages.

3. **Given** system receives a message, **When** processing begins, **Then** user message is persisted to database BEFORE agent execution starts.

---

### User Story 2 - Continue Existing Conversation (Priority: P1)

A user returns to an existing conversation and sends a follow-up message. The system reconstructs the conversation history from the database and provides contextual responses.

**Why this priority**: Conversation continuity is essential for natural chat experience.

**Independent Test**: Can be tested by sending a message with a valid conversation_id and verifying the agent receives prior context.

**Acceptance Scenarios**:

1. **Given** a user with an existing conversation containing 3 messages, **When** user sends a new message with the conversation_id, **Then** system loads all prior messages from database and provides them as context to the agent.

2. **Given** a conversation with prior context "I added milk to my tasks", **When** user says "Also add eggs", **Then** agent understands the context and correctly adds "eggs" as a new task.

3. **Given** a conversation_id that doesn't exist or belongs to another user, **When** user sends a message, **Then** system returns an error (conversation not found or unauthorized).

---

### User Story 3 - Conversation Survives Server Restart (Priority: P1)

The server restarts (planned or unplanned) and users can seamlessly continue their conversations without data loss.

**Why this priority**: This is the core statelessness requirement from the constitution.

**Independent Test**: Can be tested by stopping and restarting the server, then verifying conversation history is intact.

**Acceptance Scenarios**:

1. **Given** an ongoing conversation with 5 messages, **When** server restarts, **Then** user can continue the conversation with full history preserved.

2. **Given** a server restart occurs, **When** user sends a message to existing conversation, **Then** response is contextually appropriate based on full history.

3. **Given** multiple users have active conversations, **When** server restarts, **Then** all conversations for all users remain intact and accessible.

---

### User Story 4 - View Tool Calls in Response (Priority: P2)

A user receives a response and can see which MCP tools were invoked to produce the result, enabling transparency and debugging.

**Why this priority**: Observability requirement from constitution; important but not blocking core functionality.

**Independent Test**: Can be tested by sending a task creation message and verifying tool_calls are included in the response.

**Acceptance Scenarios**:

1. **Given** user says "Add meeting at 3pm", **When** agent processes and creates the task, **Then** response includes tool_calls array showing the `add_task` invocation with parameters.

2. **Given** user says "Show my tasks", **When** agent retrieves task list, **Then** response includes tool_calls showing `list_tasks` was called.

3. **Given** agent provides a response without tool invocation (e.g., clarifying question), **When** response is returned, **Then** tool_calls array is empty but still present.

---

### User Story 5 - Message Persistence Ordering (Priority: P2)

Messages are persisted in the correct order with accurate timestamps, ensuring conversation history is reliable for context reconstruction.

**Why this priority**: Data integrity requirement; messages must be properly sequenced.

**Independent Test**: Can be tested by sending rapid sequential messages and verifying correct ordering in database.

**Acceptance Scenarios**:

1. **Given** a conversation, **When** user sends message and agent responds, **Then** user message has timestamp T1, assistant message has timestamp T2, and T1 < T2.

2. **Given** multiple messages in a conversation, **When** history is retrieved, **Then** messages are ordered by creation timestamp ascending.

3. **Given** user sends "Add task A" then immediately "Add task B", **When** both are processed, **Then** message order in database reflects the order received.

---

### User Story 6 - Chat Widget with Voice Input (Priority: P1)

A user interacts with the AI assistant through a chat widget interface, using either text input or voice commands to manage tasks naturally.

**Why this priority**: The chat interface is the primary user-facing component; without it, users cannot interact with the system.

**Independent Test**: Can be tested by opening the chat widget, sending a message via text or voice, and verifying the response appears in chat bubbles.

**Acceptance Scenarios**:

1. **Given** a user opens the chat interface, **When** user types "Add buy groceries" and clicks send, **Then** message appears in a chat bubble (right-aligned), API is called, and assistant response appears in a chat bubble (left-aligned).

2. **Given** a user with a microphone-enabled browser, **When** user clicks the mic button and says "Show my tasks", **Then** speech is converted to text, text appears in input field, and is sent to the API.

3. **Given** an ongoing conversation, **When** user sends multiple messages, **Then** all messages display in chronological order with user bubbles on right and assistant bubbles on left.

4. **Given** the assistant invokes an MCP tool, **When** response is displayed, **Then** tool call is visually indicated (e.g., badge or collapsible section showing tool name and result).

5. **Given** a browser without speech recognition support, **When** user views the chat interface, **Then** mic button shows a fallback message or is hidden gracefully.

---

### Edge Cases

- **Invalid conversation_id format**: System returns validation error
- **Conversation belongs to different user**: System returns 403 Forbidden (no information leakage)
- **Empty message content**: System returns validation error
- **Very long conversation history**: System implements reasonable context window limits (documented in assumptions)
- **Concurrent messages to same conversation**: System processes sequentially to maintain order
- **Database unavailable**: System returns service unavailable error (no partial state)
- **Agent timeout**: User message is persisted, assistant message records failure, user is informed
- **Voice recognition fails**: User is notified, can fall back to text input
- **Browser does not support Web Speech API**: Mic button hidden or shows unsupported message
- **Network error during voice transcription**: Error displayed, user can retry

---

## Phase Context & Constraints *(Phase-III)*

- **Persistence**: Neon Serverless PostgreSQL (extending Phase II database)
- **Interface**: REST API (single chat endpoint)
- **Intelligence**: OpenAI Agents SDK via MCP tools (defined in 003-agent-mcp-tools)
- **Statelessness**: Backend is completely stateless; all state reconstructed from database per request
- **External Specs**: Constitution §14, 003-agent-mcp-tools (MCP tool contracts)

---

## Requirements *(mandatory)*

### Database Extension Requirements

#### Reused Entities (from Phase II)

- **DER-001**: System MUST reuse the existing `users` table without modification
- **DER-002**: System MUST reuse the existing `tasks` table without modification
- **DER-003**: MCP tools MUST read/write to the existing `tasks` table
- **DER-004**: User authentication MUST use the existing Phase II auth mechanism

#### New Entity: Conversation

- **DER-005**: System MUST create a `conversations` table to track chat sessions
- **DER-006**: Each conversation MUST belong to exactly one user (foreign key to users)
- **DER-007**: Conversation MUST have a unique identifier (UUID)
- **DER-008**: Conversation MUST track creation timestamp (server-generated)
- **DER-009**: Conversation MUST track last activity timestamp (updated on each message)
- **DER-010**: Conversation MAY have a title (auto-generated or user-provided)

#### New Entity: Message

- **DER-011**: System MUST create a `messages` table to store conversation messages
- **DER-012**: Each message MUST belong to exactly one conversation (foreign key)
- **DER-013**: Message MUST have a unique identifier (UUID)
- **DER-014**: Message MUST have a role: "user" or "assistant"
- **DER-015**: Message MUST have content (text, 1-10000 characters)
- **DER-016**: Message MUST have a creation timestamp (server-generated)
- **DER-017**: Message MAY have tool_calls (stored as structured data for assistant messages)
- **DER-018**: Messages MUST be ordered by creation timestamp within a conversation

#### Data Integrity

- **DER-019**: Deleting a user MUST cascade delete their conversations and messages
- **DER-020**: Deleting a conversation MUST cascade delete its messages
- **DER-021**: No orphaned messages (messages without valid conversation) are allowed
- **DER-022**: No orphaned conversations (conversations without valid user) are allowed
- **DER-023**: All timestamps MUST be server-generated (not client-provided)

---

### API Contract Requirements

#### Endpoint Definition

- **ACR-001**: System MUST expose `POST /api/{user_id}/chat` endpoint
- **ACR-002**: Endpoint MUST require authentication (user must be authenticated)
- **ACR-003**: Endpoint MUST verify user_id matches authenticated user (no cross-user access)

#### Request Schema

- **ACR-004**: Request body MUST include `message` field (string, required)
- **ACR-005**: Request body MAY include `conversation_id` field (UUID, optional)
- **ACR-006**: If conversation_id is omitted, system MUST create a new conversation
- **ACR-007**: If conversation_id is provided, system MUST validate it exists and belongs to user
- **ACR-008**: Message content MUST be 1-10000 characters

#### Response Schema

- **ACR-009**: Response MUST include `conversation_id` (UUID)
- **ACR-010**: Response MUST include `message_id` (UUID of assistant's response message)
- **ACR-011**: Response MUST include `response` (string, assistant's text response)
- **ACR-012**: Response MUST include `tool_calls` (array, possibly empty)
- **ACR-013**: Response MUST include `created_at` (timestamp of assistant message)

#### Error Responses

- **ACR-014**: Invalid request body MUST return 400 Bad Request with details
- **ACR-015**: Unauthenticated request MUST return 401 Unauthorized
- **ACR-016**: Conversation not found or unauthorized MUST return 404 Not Found
- **ACR-017**: Server errors MUST return 500 Internal Server Error with safe message

---

### Stateless Flow Requirements

#### Request Processing

- **SFR-001**: System MUST NOT maintain any in-memory session state between requests
- **SFR-002**: Each request MUST reconstruct conversation context from database
- **SFR-003**: User message MUST be persisted to database BEFORE agent execution
- **SFR-004**: Assistant message MUST be persisted to database AFTER agent execution
- **SFR-005**: If agent execution fails, user message remains persisted and error is recorded

#### Context Reconstruction

- **SFR-006**: System MUST load all messages for the conversation from database
- **SFR-007**: Messages MUST be loaded in chronological order (oldest first)
- **SFR-008**: System MUST include user_id in context for MCP tool calls
- **SFR-009**: Context reconstruction MUST complete before agent receives the request

#### Tool Call Flow

- **SFR-010**: MCP tools MUST read task data from database (not memory)
- **SFR-011**: MCP tools MUST write task changes to database immediately
- **SFR-012**: Tool call results MUST be recorded in the assistant message
- **SFR-013**: Tool calls MUST be attributable to specific requests for audit

---

### Persistence Guarantees

- **PGR-001**: All conversation state MUST survive server restart
- **PGR-002**: Database MUST be the single source of truth for all state
- **PGR-003**: No in-memory caches of conversation state are permitted
- **PGR-004**: Partial request failures MUST NOT leave inconsistent state
- **PGR-005**: Concurrent requests to same conversation MUST be serialized

---

### Frontend/UI Requirements

#### Chat Interface

- **UIR-001**: System MUST provide a chat widget interface for user interaction
- **UIR-002**: Chat widget MUST display messages in bubble format (user right-aligned, assistant left-aligned)
- **UIR-003**: Chat widget MUST show message history in chronological order
- **UIR-004**: Chat widget MUST auto-scroll to the latest message
- **UIR-005**: Chat widget MUST show loading indicator while waiting for API response
- **UIR-006**: Chat widget MUST persist conversation_id in browser storage for session continuity

#### Text Input

- **UIR-007**: Chat input MUST accept text messages up to 10,000 characters
- **UIR-008**: Chat input MUST support Enter key to send message
- **UIR-009**: Chat input MUST be disabled while processing a request
- **UIR-010**: Chat input MUST show character count indicator

#### Voice Input

- **UIR-011**: System MUST provide voice input via Web Speech API
- **UIR-012**: Voice input MUST show mic button with visual states (idle, listening, processing)
- **UIR-013**: Voice input MUST convert speech to text and populate the input field
- **UIR-014**: Voice input MUST gracefully handle unsupported browsers (hide or show fallback)
- **UIR-015**: Voice input MUST provide visual feedback during recording (pulsing indicator)

#### Tool Call Visualization

- **UIR-016**: Assistant responses MUST visually indicate when MCP tools were invoked
- **UIR-017**: Tool call details SHOULD be viewable (tool name, parameters, result)
- **UIR-018**: Tool call visualization MUST NOT block or obscure the main response text

#### Accessibility & UX

- **UIR-019**: Chat interface MUST be responsive (mobile-friendly)
- **UIR-020**: Chat interface MUST support keyboard navigation
- **UIR-021**: Voice input errors MUST be communicated clearly to the user

---

### Key Entities

#### Conversation

A container for a chat session between a user and the AI assistant.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Unique identifier |
| user_id | UUID | Yes | Owner of the conversation (FK to users) |
| title | String | No | Display title (max 100 chars) |
| created_at | DateTime | Yes | When conversation started (server-generated) |
| updated_at | DateTime | Yes | Last activity timestamp (server-generated) |

#### Message

A single exchange within a conversation.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Unique identifier |
| conversation_id | UUID | Yes | Parent conversation (FK) |
| role | Enum | Yes | "user" or "assistant" |
| content | Text | Yes | Message text (1-10000 chars) |
| tool_calls | JSON | No | MCP tool invocations (assistant only) |
| created_at | DateTime | Yes | When message was created (server-generated) |

#### Relationships

```
User (1) ←→ (Many) Conversation
Conversation (1) ←→ (Many) Message
User (1) ←→ (Many) Task  [existing Phase II relationship]
```

---

## API Contract Details

### Request: POST /api/{user_id}/chat

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | UUID | Yes | The authenticated user's ID |

**Request Body**:

```
{
  "message": string,        // Required: User's message (1-10000 chars)
  "conversation_id": string // Optional: UUID of existing conversation
}
```

**Response Body (Success - 200 OK)**:

```
{
  "conversation_id": string,  // UUID of the conversation
  "message_id": string,       // UUID of the assistant's message
  "response": string,         // Assistant's text response
  "tool_calls": [             // Array of MCP tool invocations
    {
      "tool": string,         // Tool name (e.g., "add_task")
      "parameters": object,   // Parameters passed to tool
      "result": object        // Tool execution result
    }
  ],
  "created_at": string        // ISO 8601 timestamp
}
```

**Error Responses**:

| Status | Condition | Body |
|--------|-----------|------|
| 400 | Invalid request | `{"error": "validation_error", "details": [...]}` |
| 401 | Not authenticated | `{"error": "unauthorized", "message": "Authentication required"}` |
| 404 | Conversation not found | `{"error": "not_found", "message": "Conversation not found"}` |
| 500 | Server error | `{"error": "internal_error", "message": "An error occurred"}` |

---

## Stateless Request Flow

### Sequence: New Conversation

1. User sends POST /api/{user_id}/chat with message, no conversation_id
2. System authenticates user, verifies user_id matches
3. System creates new Conversation record in database
4. System creates new Message record (role: "user", content: user's message)
5. System constructs agent context (empty history for new conversation)
6. System invokes OpenAI Agent with context and user message
7. Agent executes MCP tools as needed (tools read/write database directly)
8. Agent returns response with tool_calls
9. System creates Message record (role: "assistant", content: response, tool_calls)
10. System updates Conversation.updated_at
11. System returns response to user

### Sequence: Existing Conversation

1. User sends POST /api/{user_id}/chat with message and conversation_id
2. System authenticates user, verifies user_id matches
3. System loads Conversation from database, verifies ownership
4. System loads all Messages for conversation, ordered by created_at
5. System creates new Message record (role: "user", content: user's message)
6. System constructs agent context from loaded messages
7. System invokes OpenAI Agent with context and user message
8. Agent executes MCP tools as needed
9. Agent returns response with tool_calls
10. System creates Message record (role: "assistant", content: response, tool_calls)
11. System updates Conversation.updated_at
12. System returns response to user

### Invariant: Message Persistence Order

```
User message persisted → Agent executes → Assistant message persisted
         ↑                                          ↓
    ALWAYS FIRST                              ALWAYS LAST
```

This ensures:
- User message is never lost even if agent fails
- Assistant message accurately reflects what agent returned
- Conversation history is always consistent

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### Backend Criteria

- **SC-001**: Users can start a new conversation and receive a response in under 5 seconds
- **SC-002**: Users can continue an existing conversation with full context preserved 100% of the time
- **SC-003**: 100% of conversations survive server restart without data loss
- **SC-004**: 100% of API responses include tool_calls array (even if empty)
- **SC-005**: 0% of messages are orphaned (every message has valid conversation)
- **SC-006**: 0% of conversations are orphaned (every conversation has valid user)
- **SC-007**: Message ordering is preserved 100% of the time (chronological order maintained)
- **SC-008**: User messages are persisted before agent execution 100% of the time

#### Frontend Criteria

- **SC-009**: Users can send a text message and see response in chat bubbles within 5 seconds
- **SC-010**: Voice input successfully converts speech to text 90%+ of the time (in supported browsers)
- **SC-011**: Chat history displays correctly after page refresh 100% of the time
- **SC-012**: Tool call indicators are visible for 100% of assistant responses that used tools
- **SC-013**: Chat interface is usable on mobile devices (responsive design verified)
- **SC-014**: Voice input gracefully degrades in unsupported browsers 100% of the time

---

## Assumptions

### Backend Assumptions

1. **Authentication**: Phase II authentication mechanism (Better Auth) is reused without modification
2. **Context Window**: Maximum of 50 messages loaded for context (older messages truncated with summary)
3. **Conversation Limits**: No limit on conversations per user (can be added later if needed)
4. **Message Size**: 10,000 character limit per message is sufficient for conversational use
5. **Tool Calls Storage**: tool_calls stored as JSON/JSONB for flexibility
6. **Timezone**: All timestamps stored in UTC
7. **Soft Delete**: Conversations and messages are hard-deleted (no soft delete required)
8. **Concurrent Access**: Same conversation accessed by single user at a time (no real-time collaboration)

### Frontend Assumptions

9. **Browser Support**: Target browsers are Chrome, Edge, Safari (latest 2 versions)
10. **Voice Support**: Web Speech API available in Chrome, Edge, Safari; Firefox has limited support
11. **Chat UI Library**: OpenAI ChatKit or equivalent React-based chat component library
12. **State Persistence**: conversation_id stored in localStorage for session continuity
13. **Mobile Support**: Responsive design required; voice input may vary by mobile browser
14. **No Real-time**: Messages fetched on send/receive, no WebSocket push (can be added later)

---

## Dependencies

- **003-agent-mcp-tools**: MCP tool contracts for task operations
- **Phase II Database**: Existing users and tasks tables
- **Phase II Authentication**: Better Auth integration
- **Constitution §14**: Phase III governance rules
