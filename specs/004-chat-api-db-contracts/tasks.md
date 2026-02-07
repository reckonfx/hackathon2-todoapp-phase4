# Tasks: Chat API & Database Contracts

**Input**: Design documents from `/specs/004-chat-api-db-contracts/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.yaml, quickstart.md

**Tests**: Tests are included as this is a critical infrastructure feature requiring validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Structure based on plan.md project structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and database migrations

- [ ] T001 Install new dependencies: openai-agents, mcp, pytest-asyncio in backend/requirements.txt
- [ ] T002 Create Alembic migration for conversations table in backend/alembic/versions/
- [ ] T003 Create Alembic migration for messages table in backend/alembic/versions/
- [ ] T004 [P] Configure OpenAI API key in environment variables (.env.example)
- [ ] T005 [P] Update backend/src/models/__init__.py to export new models

**Checkpoint**: Database schema ready, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and services that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Constitution Check**:
- [ ] T006 Verify Phase II users table is reused without modification (DER-001)
- [ ] T007 Verify Phase II tasks table is reused without modification (DER-002)
- [ ] T008 Verify Phase II auth mechanism is reused (DER-004)

### Core Models

- [ ] T009 [P] Create Conversation model in backend/src/models/conversation.py per data-model.md
- [ ] T010 [P] Create Message model in backend/src/models/message.py per data-model.md
- [ ] T011 Create model relationships (User→Conversations, Conversation→Messages) in backend/src/models/

### Core Services

- [ ] T012 Create ConversationService in backend/src/services/conversation_service.py
  - create_conversation(user_id) → Conversation
  - get_conversation(conversation_id, user_id) → Conversation | None
  - update_conversation_timestamp(conversation_id) → None

- [ ] T013 Create MessageService in backend/src/services/message_service.py
  - create_message(conversation_id, role, content, tool_calls?) → Message
  - get_messages_for_conversation(conversation_id, limit=50) → List[Message]

### Request/Response Schemas

- [ ] T014 [P] Create ChatRequest schema in backend/src/api/schemas/chat.py per contracts/chat-api.yaml
- [ ] T015 [P] Create ChatResponse schema in backend/src/api/schemas/chat.py per contracts/chat-api.yaml
- [ ] T016 [P] Create ErrorResponse schema in backend/src/api/schemas/chat.py per contracts/chat-api.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Start New Conversation (Priority: P1) 🎯 MVP

**Goal**: User can send a message without conversation_id and receive a response with new conversation created

**Independent Test**: Send POST /api/{user_id}/chat with message only, verify conversation_id returned

### Tests for User Story 1

- [ ] T017 [P] [US1] Contract test for new conversation in backend/tests/contract/test_chat_new_conversation.py
  - Test: POST without conversation_id creates new conversation
  - Test: Response includes conversation_id, message_id, response, tool_calls, created_at

### Implementation for User Story 1

- [ ] T018 [US1] Create chat route POST /api/{user_id}/chat in backend/src/api/routes/chat.py
  - Implement auth verification (ACR-002, ACR-003)
  - Implement request validation (ACR-004, ACR-008)
  - Handle missing conversation_id → create new conversation (ACR-006)

- [ ] T019 [US1] Create ChatService.process_new_conversation() in backend/src/services/chat_service.py
  - Create conversation via ConversationService
  - Persist user message BEFORE agent execution (SFR-003)
  - Return conversation_id and message_id

- [ ] T020 [US1] Integrate OpenAI Agent invocation in backend/src/services/chat_service.py
  - Create agent instance per request (research.md R2)
  - Pass empty context for new conversation
  - Capture agent response and tool_calls

- [ ] T021 [US1] Persist assistant message after agent execution in backend/src/services/chat_service.py
  - Create message with role="assistant" (SFR-004)
  - Store tool_calls as JSONB (research.md R6)
  - Update conversation timestamp

- [ ] T022 [US1] Build ChatResponse from persisted data in backend/src/api/routes/chat.py
  - Return conversation_id, message_id, response, tool_calls, created_at (ACR-009 to ACR-013)

**Checkpoint**: User Story 1 complete - new conversations work independently

---

## Phase 4: User Story 2 - Continue Existing Conversation (Priority: P1)

**Goal**: User can continue conversation with full context from database

**Independent Test**: Send message with valid conversation_id, verify context-aware response

### Tests for User Story 2

- [ ] T023 [P] [US2] Contract test for continuing conversation in backend/tests/contract/test_chat_continue_conversation.py
  - Test: POST with valid conversation_id loads history
  - Test: Invalid conversation_id returns 404
  - Test: Other user's conversation_id returns 404 (no info leak)

### Implementation for User Story 2

- [ ] T024 [US2] Implement conversation lookup and validation in backend/src/api/routes/chat.py
  - Validate conversation_id format
  - Load conversation, verify user ownership (ACR-007)
  - Return 404 if not found or unauthorized (ACR-016)

- [ ] T025 [US2] Create ChatService.process_existing_conversation() in backend/src/services/chat_service.py
  - Load conversation history via MessageService (SFR-006)
  - Order messages chronologically (SFR-007)
  - Persist new user message

- [ ] T026 [US2] Implement context reconstruction for agent in backend/src/services/chat_service.py
  - Build message history for agent context (SFR-002)
  - Include user_id for MCP tool calls (SFR-008)
  - Limit to 50 messages (research.md R4)

- [ ] T027 [US2] Invoke agent with reconstructed context in backend/src/services/chat_service.py
  - Pass full message history to agent
  - Agent receives context and responds appropriately

**Checkpoint**: User Stories 1 AND 2 complete - conversations can be started and continued

---

## Phase 5: User Story 3 - Conversation Survives Server Restart (Priority: P1)

**Goal**: All conversation state persists in database, survives restarts

**Independent Test**: Stop server, restart, continue conversation with full history

### Tests for User Story 3

- [ ] T028 [P] [US3] Integration test for stateless recovery in backend/tests/integration/test_stateless_recovery.py
  - Test: Create conversation, stop/start, continue with history
  - Test: No in-memory state retained (SFR-001)
  - Test: Multiple users' conversations all survive

### Implementation for User Story 3

- [ ] T029 [US3] Audit ChatService for statelessness violations in backend/src/services/chat_service.py
  - Remove any class-level state
  - Ensure all state comes from database (PGR-002)
  - No caching of conversation state (PGR-003)

- [ ] T030 [US3] Implement error recovery for agent failures in backend/src/services/chat_service.py
  - User message preserved on failure (SFR-005)
  - Record error in assistant message (research.md R7)
  - No transaction rollback of user message

- [ ] T031 [US3] Add database transaction handling in backend/src/services/chat_service.py
  - Atomic operations where needed
  - No partial state on failures (PGR-004)

**Checkpoint**: User Stories 1-3 complete - core stateless functionality working

---

## Phase 6: User Story 4 - View Tool Calls in Response (Priority: P2)

**Goal**: API responses include tool_calls array showing MCP tool invocations

**Independent Test**: Send task creation message, verify tool_calls in response

### Tests for User Story 4

- [ ] T032 [P] [US4] Contract test for tool_calls in backend/tests/contract/test_chat_tool_calls.py
  - Test: add_task message returns tool_calls with add_task
  - Test: list_tasks message returns tool_calls with list_tasks
  - Test: No tool message returns empty tool_calls array

### Implementation for User Story 4

- [ ] T033 [US4] Capture tool_calls from agent response in backend/src/services/chat_service.py
  - Extract tool name, parameters, result from agent
  - Format per contracts/chat-api.yaml ToolCall schema

- [ ] T034 [US4] Store tool_calls in Message.tool_calls JSONB in backend/src/services/message_service.py
  - Only for role="assistant" messages
  - Validate against expected schema

- [ ] T035 [US4] Ensure tool_calls always present in response in backend/src/api/routes/chat.py
  - Return empty array [] when no tools called (ACR-012)
  - Never return null for tool_calls

**Checkpoint**: User Story 4 complete - observability achieved

---

## Phase 7: User Story 5 - Message Persistence Ordering (Priority: P2)

**Goal**: Messages persisted in correct order with accurate timestamps

**Independent Test**: Send rapid messages, verify database order matches request order

### Tests for User Story 5

- [ ] T036 [P] [US5] Integration test for message ordering in backend/tests/integration/test_message_ordering.py
  - Test: User message timestamp < assistant message timestamp
  - Test: Multiple messages maintain correct order
  - Test: Rapid sequential messages ordered correctly

### Implementation for User Story 5

- [ ] T037 [US5] Ensure server-generated timestamps in backend/src/models/message.py
  - created_at uses database NOW() (DER-023)
  - No client-provided timestamps accepted

- [ ] T038 [US5] Implement message ordering in MessageService in backend/src/services/message_service.py
  - get_messages_for_conversation orders by created_at ASC
  - Composite index for efficient ordering

- [ ] T039 [US5] Handle concurrent message serialization in backend/src/services/chat_service.py
  - Implement optimistic locking if needed (research.md R5)
  - Sequential processing for same conversation (PGR-005)

**Checkpoint**: All user stories complete

---

## Phase 8: MCP Tools Integration

**Purpose**: Connect MCP tools to database for task operations

- [ ] T040 [P] Create MCP server entry point in backend/src/mcp/server.py
- [ ] T041 [P] Implement add_task tool in backend/src/mcp/tools/add_task.py per 003-agent-mcp-tools spec
- [ ] T042 [P] Implement list_tasks tool in backend/src/mcp/tools/list_tasks.py per 003-agent-mcp-tools spec
- [ ] T043 [P] Implement complete_task tool in backend/src/mcp/tools/complete_task.py per 003-agent-mcp-tools spec
- [ ] T044 [P] Implement delete_task tool in backend/src/mcp/tools/delete_task.py per 003-agent-mcp-tools spec
- [ ] T045 [P] Implement update_task tool in backend/src/mcp/tools/update_task.py per 003-agent-mcp-tools spec
- [ ] T046 Register MCP tools with agent in backend/src/services/chat_service.py
- [ ] T047 [P] Create MCP tool tests in backend/tests/unit/test_mcp_tools.py

**Checkpoint**: MCP tools connected and functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, validation, documentation

- [ ] T048 [P] Implement comprehensive error handling in backend/src/api/routes/chat.py
  - 400 for validation errors (ACR-014)
  - 401 for auth failures (ACR-015)
  - 404 for not found (ACR-016)
  - 500 for server errors (ACR-017)

- [ ] T049 [P] Add request/response logging in backend/src/api/routes/chat.py
  - Log tool calls for audit (SFR-013)
  - Sufficient detail for debugging (Constitution §14.2.4)

- [ ] T050 [P] Implement input validation in backend/src/api/schemas/chat.py
  - Message length 1-10000 chars (ACR-008)
  - UUID format for conversation_id
  - Sanitize inputs

- [ ] T051 Run quickstart.md validation steps
  - V1: Database tables created
  - V2: Start new conversation
  - V3: Continue conversation
  - V4: Verify statelessness
  - V5: Verify message persistence
  - V6: Verify tool calls recorded

- [ ] T052 [P] Update CLAUDE.md with Phase III context

---

## Phase 10: Frontend Chat Interface (User Story 6)

**Purpose**: Chat widget UI with voice input for natural language task management

**Goal**: Users can interact with the AI assistant via text or voice through a chat bubble interface

**Independent Test**: Open chat widget, send message via text or voice, see response in chat bubbles

### User Story 6 - Chat Widget with Voice Input (Priority: P1)

**Acceptance Scenarios**:
1. User types message in input box → message appears in chat bubble → response appears
2. User clicks mic button → speaks command → speech converted to text → sent to API
3. Chat history displays user messages (right) and assistant messages (left)
4. Tool calls are visually indicated in assistant responses

### Frontend Setup

- [ ] T053 [P] [US6] Install frontend dependencies in frontend/package.json
  - @openai/chatkit (or equivalent chat UI library)
  - React hooks for state management

- [ ] T054 [P] [US6] Create frontend environment config in frontend/.env.example
  - NEXT_PUBLIC_API_URL for backend endpoint

### Chat Interface Components

- [ ] T055 [P] [US6] Create ChatContainer component in frontend/src/components/chat/ChatContainer.tsx
  - Main wrapper for chat interface
  - Manages conversation state (conversation_id)
  - Handles API communication with POST /api/{user_id}/chat

- [ ] T056 [P] [US6] Create ChatBubble component in frontend/src/components/chat/ChatBubble.tsx
  - User message bubble (right-aligned, primary color)
  - Assistant message bubble (left-aligned, secondary color)
  - Timestamp display
  - Tool call indicator badge (optional)

- [ ] T057 [US6] Create ChatMessageList component in frontend/src/components/chat/ChatMessageList.tsx
  - Scrollable message history
  - Auto-scroll to latest message
  - Loading indicator while waiting for response

- [ ] T058 [US6] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx
  - Text input field with send button
  - Enter key to send
  - Disabled state while processing
  - Character count (max 10000)

### Voice Input Feature

- [ ] T059 [P] [US6] Create VoiceInput component in frontend/src/components/chat/VoiceInput.tsx
  - Microphone button with visual states (idle, listening, processing)
  - Web Speech API integration (SpeechRecognition)
  - Browser compatibility check (Chrome, Edge, Safari)
  - Fallback message for unsupported browsers

- [ ] T060 [US6] Implement speech-to-text logic in frontend/src/hooks/useSpeechRecognition.ts
  - Start/stop recording
  - Continuous vs single utterance mode
  - Interim results display (optional)
  - Final transcript → send to ChatInput

- [ ] T061 [US6] Add voice input to ChatInput in frontend/src/components/chat/ChatInput.tsx
  - Mic button next to send button
  - Visual feedback during recording (pulsing indicator)
  - Transcribed text appears in input field before sending

### Chat Service Integration

- [ ] T062 [US6] Create chat API service in frontend/src/services/chatService.ts
  - sendMessage(userId, message, conversationId?) → ChatResponse
  - Handle auth token injection
  - Error handling and retry logic

- [ ] T063 [US6] Create chat state hook in frontend/src/hooks/useChat.ts
  - messages: Message[]
  - conversationId: string | null
  - isLoading: boolean
  - sendMessage(text: string) → void
  - Persist conversationId in localStorage for session continuity

### Styling and UX

- [ ] T064 [P] [US6] Create chat styles in frontend/src/components/chat/chat.module.css
  - Chat container (fixed position or embedded)
  - Bubble styles (user vs assistant)
  - Input area styling
  - Mic button animations
  - Responsive design (mobile-friendly)

- [ ] T065 [P] [US6] Add tool call visualization in ChatBubble
  - Collapsible section showing tool name and result
  - Icon indicators for different tool types (add, list, complete, delete)

### Frontend Tests

- [ ] T066 [P] [US6] Create ChatContainer test in frontend/src/components/chat/__tests__/ChatContainer.test.tsx
  - Test: Sends message to API on submit
  - Test: Displays response in chat bubbles
  - Test: Maintains conversation_id across messages

- [ ] T067 [P] [US6] Create VoiceInput test in frontend/src/components/chat/__tests__/VoiceInput.test.tsx
  - Test: Mic button triggers speech recognition
  - Test: Transcribed text sent to input
  - Test: Fallback shown for unsupported browsers

### Integration

- [ ] T068 [US6] Add ChatContainer to main page in frontend/src/app/chat/page.tsx
  - Protected route (requires auth)
  - Pass authenticated user_id to ChatContainer

- [ ] T069 [US6] Add chat navigation link in frontend/src/components/navigation
  - Link to /chat from main navigation
  - Chat icon indicator

**Checkpoint**: Frontend complete - users can chat via text or voice

---

## Phase 11: End-to-End Integration

**Purpose**: Verify full stack works together

- [ ] T070 End-to-end test: Text message flow
  - Type "Add buy groceries" in chat widget
  - Verify message appears in chat bubbles
  - Verify task created in database
  - Verify response shows tool_calls

- [ ] T071 End-to-end test: Voice message flow
  - Click mic, say "Show my tasks"
  - Verify speech converted to text
  - Verify text sent to API
  - Verify task list returned and displayed

- [ ] T072 End-to-end test: Conversation continuity
  - Send multiple messages
  - Refresh page
  - Verify conversation continues with context

- [ ] T073 Update quickstart.md with frontend verification steps
  - V7: Open chat interface
  - V8: Send text message
  - V9: Send voice message
  - V10: Verify chat history persists

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-7 (User Stories)**: All depend on Phase 2 completion
- **Phase 8 (MCP Tools)**: Can run in parallel with Phases 3-7
- **Phase 9 (Polish)**: Depends on Phases 3-8
- **Phase 10 (Frontend)**: Can start after Phase 2, requires Phase 3 (US1) for integration
- **Phase 11 (E2E)**: Depends on all prior phases

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (New Conversation) | Phase 2 only | US4, US5, MCP Tools, US6 |
| US2 (Continue Conversation) | US1 | US3, US4, US5, US6 |
| US3 (Stateless Recovery) | US2 | US4, US5, US6 |
| US4 (Tool Calls) | US1 | US2, US3, US5, US6 |
| US5 (Message Ordering) | US1 | US2, US3, US4, US6 |
| US6 (Chat Widget + Voice) | Phase 2, US1 for integration | US2-US5 |

### Within Each User Story

1. Tests written FIRST (fail before implementation)
2. Route/endpoint
3. Service logic
4. Integration with agent
5. Story complete before next priority

### Parallel Opportunities

**Phase 1**:
```
T001 → [T002, T003] → [T004, T005]
```

**Phase 2** (after T001-T005):
```
[T006, T007, T008] (constitution checks)
[T009, T010] → T011 (models)
T012, T013 (services - after models)
[T014, T015, T016] (schemas - parallel)
```

**User Stories** (after Phase 2):
```
US1: T017 → T018 → T019 → T020 → T021 → T022
US4: T032 → T033 → T034 → T035 (can parallel with US1 after T022)
US5: T036 → T037 → T038 → T039 (can parallel with US1 after T022)
```

**MCP Tools** (after Phase 2):
```
[T040, T041, T042, T043, T044, T045] → T046 → T047
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Can create new conversations
5. Deploy/demo if ready

### Incremental Delivery

| Milestone | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP Backend | US1 | New conversations work (API only) |
| Alpha | US1 + US2 | Conversations continue |
| Beta Backend | US1-3 | Stateless, production-ready |
| MVP Full Stack | US1-3 + US6 | **Chat widget with voice!** |
| v1.0 | US1-6 + MCP + E2E | Full observability, tested |

### Suggested Execution Order

1. T001-T005 (Setup)
2. T006-T016 (Foundational)
3. T017-T022 (US1 - MVP Backend)
4. T040-T047 (MCP Tools - parallel with US2-5)
5. T023-T027 (US2)
6. T028-T031 (US3)
7. T053-T069 (US6 - Frontend with Voice) ← **Can start after T022**
8. T032-T035 (US4)
9. T036-T039 (US5)
10. T048-T052 (Polish)
11. T070-T073 (E2E Integration)

---

## Summary

| Category | Count |
|----------|-------|
| Setup Tasks | 5 |
| Foundational Tasks | 11 |
| US1 Tasks | 6 |
| US2 Tasks | 5 |
| US3 Tasks | 4 |
| US4 Tasks | 4 |
| US5 Tasks | 4 |
| MCP Tools Tasks | 8 |
| Polish Tasks | 5 |
| **US6 Frontend Tasks** | **17** |
| **E2E Integration Tasks** | **4** |
| **Total** | **73** |

| Parallel Opportunities | Description |
|------------------------|-------------|
| Models | T009, T010 can run in parallel |
| Schemas | T014, T015, T016 can run in parallel |
| MCP Tools | T041-T045 can run in parallel |
| User Stories | US4, US5 can parallel with US2, US3 |
| Frontend Components | T055, T056 can run in parallel |
| Frontend Tests | T066, T067 can run in parallel |
| Backend + Frontend | Phase 10 can start while Phase 4-9 in progress |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story independently completable and testable
- Tests written FIRST, must FAIL before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
