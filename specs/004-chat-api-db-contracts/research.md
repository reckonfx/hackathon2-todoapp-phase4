# Research: Chat API & Database Contracts

**Feature**: 004-chat-api-db-contracts
**Date**: 2026-01-28
**Status**: Complete

## Research Questions

### R1: SQLModel Schema Extension Pattern

**Question**: How to extend existing Phase II SQLModel tables without migration conflicts?

**Decision**: Use Alembic migrations with careful foreign key ordering

**Rationale**:
- Phase II already uses Alembic for migrations
- New tables (conversations, messages) reference existing users table
- Migration order: conversations first (FK to users), then messages (FK to conversations)
- No modification to existing users/tasks tables required

**Alternatives Considered**:
- Manual SQL scripts: Rejected (violates spec-driven workflow)
- Recreate all tables: Rejected (data loss, violates Phase II freeze)

---

### R2: OpenAI Agents SDK Integration Pattern

**Question**: How to integrate OpenAI Agents SDK with FastAPI for stateless operation?

**Decision**: Create agent instance per request, pass conversation history as context

**Rationale**:
- OpenAI Agents SDK supports passing message history to `Runner.run()`
- Agent instance is lightweight, can be created per request
- No agent state persists between requests (satisfies SFR-001)
- MCP tools registered once at startup, shared across requests

**Alternatives Considered**:
- Singleton agent with session management: Rejected (violates statelessness)
- Agent pooling: Rejected (premature optimization, adds complexity)

---

### R3: MCP SDK Server Pattern

**Question**: How to run MCP server alongside FastAPI?

**Decision**: In-process MCP server using stdio transport with agent

**Rationale**:
- MCP SDK supports in-process stdio transport
- Agent and MCP server run in same process
- No network overhead for tool calls
- Tools access database via same connection pool as API

**Alternatives Considered**:
- Separate MCP server process: Rejected (adds deployment complexity)
- HTTP-based MCP transport: Rejected (unnecessary network hop)

---

### R4: Conversation Context Window Management

**Question**: How to handle long conversation histories exceeding context window?

**Decision**: Load last 50 messages, older messages summarized or truncated

**Rationale**:
- 50 messages provides sufficient context for most interactions
- OpenAI models have token limits; truncation prevents errors
- Summary of older messages preserves essential context
- Configurable limit allows future tuning

**Alternatives Considered**:
- Load all messages always: Rejected (token limit issues)
- Sliding window without summary: Rejected (loses important context)

---

### R5: Concurrent Request Handling

**Question**: How to handle concurrent requests to same conversation?

**Decision**: Optimistic locking with conversation version field

**Rationale**:
- Spec requires serialization (PGR-005)
- Optimistic locking simpler than distributed locks
- Conflict detected at database level, retry with fresh state
- Low concurrency expected (single user per conversation)

**Alternatives Considered**:
- Database-level row locking: Considered, may use as fallback
- Redis distributed lock: Rejected (adds infrastructure)

---

### R6: Tool Call Recording Format

**Question**: How to store tool_calls in messages table?

**Decision**: JSONB column with structured schema

**Rationale**:
- JSONB provides flexibility for varying tool parameters
- PostgreSQL JSONB supports indexing if needed
- Schema matches API response format for consistency
- Easy to query and audit

**Schema**:
```json
{
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"user_id": "...", "title": "..."},
      "result": {"success": true, "task": {...}}
    }
  ]
}
```

**Alternatives Considered**:
- Separate tool_calls table: Rejected (over-normalized for this use case)
- Plain JSON (not JSONB): Rejected (no indexing capability)

---

### R7: Error Recovery Pattern

**Question**: How to handle partial failures (user message persisted, agent fails)?

**Decision**: Record failure in assistant message, allow retry

**Rationale**:
- User message persisted first (SFR-003) - never lost
- If agent fails, create assistant message with error indicator
- User can retry, new request sees error message in history
- No transaction rollback needed (user message intentionally preserved)

**Failure Message Format**:
```json
{
  "role": "assistant",
  "content": "[System: Request failed. Please try again.]",
  "tool_calls": null,
  "error": true
}
```

**Alternatives Considered**:
- Transaction rollback: Rejected (loses user message, violates spec)
- Silent retry: Rejected (user doesn't know what happened)

---

## Technology Decisions Summary

| Area | Decision | Reference |
|------|----------|-----------|
| Database Extension | Alembic migrations, FK ordering | R1 |
| Agent Integration | Per-request agent, history as context | R2 |
| MCP Transport | In-process stdio | R3 |
| Context Window | 50 messages, truncate older | R4 |
| Concurrency | Optimistic locking | R5 |
| Tool Storage | JSONB column | R6 |
| Error Recovery | Preserve user message, record failure | R7 |

---

### R8: Chat UI Component Library

**Question**: Which chat UI library to use for the frontend?

**Decision**: Use OpenAI ChatKit or build custom with React components

**Rationale**:
- OpenAI ChatKit designed for AI chat interfaces
- Provides chat bubble styling out of the box
- Integrates well with OpenAI-style responses
- If not available, custom React components are straightforward

**Alternatives Considered**:
- Stream Chat SDK: Rejected (overkill, real-time features not needed)
- Plain HTML/CSS: Rejected (reinventing the wheel)

---

### R9: Voice Input Implementation

**Question**: How to implement voice input for task commands?

**Decision**: Use browser-native Web Speech API (SpeechRecognition)

**Rationale**:
- No additional API costs (browser handles transcription)
- Works offline in some browsers
- Good accuracy for short commands
- Simple integration - just converts speech to text
- Backend API unchanged (receives text regardless of input method)

**Browser Support**:
- Chrome: Full support
- Edge: Full support
- Safari: Full support (iOS 14.5+)
- Firefox: Limited support (may need flag)

**Alternatives Considered**:
- OpenAI Whisper API: Rejected (adds cost, latency, complexity)
- Google Cloud Speech: Rejected (adds cost and API dependency)
- Assembly AI: Rejected (unnecessary for simple commands)

---

### R10: Chat State Persistence

**Question**: How to persist chat state across page refreshes?

**Decision**: Store conversation_id in localStorage, fetch messages from API

**Rationale**:
- conversation_id in localStorage allows resuming conversation
- Messages fetched fresh from API (source of truth is database)
- No need to cache full message history in browser
- Simple and consistent with stateless architecture

**Alternatives Considered**:
- Session storage: Rejected (clears on tab close)
- IndexedDB: Rejected (overkill for just conversation_id)
- Cookie: Rejected (conversation_id is user-specific, not auth)

---

## Dependencies Confirmed

### Backend

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.100 | API framework |
| sqlmodel | >=0.0.14 | ORM with Pydantic |
| openai-agents | >=0.1.0 | Agent SDK |
| mcp | >=1.0.0 | MCP SDK |
| asyncpg | >=0.29 | Async PostgreSQL driver |
| alembic | >=1.13 | Database migrations |
| pytest | >=8.0 | Testing |
| pytest-asyncio | >=0.23 | Async test support |

### Frontend

| Package | Version | Purpose |
|---------|---------|---------|
| react | >=18.0 | Component framework |
| next | >=14.0 | App framework |
| @openai/chatkit | >=0.1.0 | Chat UI (or custom) |
| Web Speech API | Browser native | Speech recognition |
