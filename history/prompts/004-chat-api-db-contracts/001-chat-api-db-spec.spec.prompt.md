---
id: PHR-SPEC-004-001
title: Chat API Database Contracts Spec
stage: spec
date: 2026-01-28
surface: claude-code
model: claude-opus-4-5-20251101
feature: 004-chat-api-db-contracts
branch: 004-chat-api-db-contracts
user: AKE
command: /sp.specify
labels: [spec, api, database, contracts, phase3, stateless, conversations]
links:
  spec: specs/004-chat-api-db-contracts/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/004-chat-api-db-contracts/spec.md
    action: create
  - path: specs/004-chat-api-db-contracts/checklists/requirements.md
    action: create
tests:
  - null
---

## Prompt

```text
Scope: API contract, database extensions, and stateless conversation flow

Context:
A Neon Serverless PostgreSQL database already exists from Phase II.
It currently stores user and task data.
Phase III must reuse this database and extend it only where necessary
to support conversational task management.

Task:
Specify system-level contracts for:

1. Database usage:
   - Reuse existing Neon PostgreSQL database
   - Identify existing models that will be reused (e.g., users, tasks)
   - Specify any new tables or fields required for:
     - conversations
     - messages
   - Define relationships between existing and new models

2. API contract:
   - POST /api/{user_id}/chat endpoint
   - Request and response schemas
   - Conversation ID lifecycle

3. Stateless request flow:
   - How conversation history is reconstructed per request
   - How user and assistant messages are persisted
   - How MCP tool calls read/write task state via the database

4. Persistence guarantees:
   - Resume conversations after server restart
   - No in-memory session state
   - Database as single source of truth

Requirements:
- Backend and MCP tools must remain stateless
- No duplication of existing Phase II database logic
- All task mutations occur through MCP tools
- Tool calls must be traceable to database changes

Constraints:
- No implementation code
- Focus on contracts, invariants, and data flow
```

## Response snapshot

Created comprehensive specification for Chat API & Database Contracts at `specs/004-chat-api-db-contracts/spec.md`.

**Database Extension Requirements (23 rules):**
- DER-001 to DER-004: Reuse Phase II users and tasks tables
- DER-005 to DER-010: New Conversation entity
- DER-011 to DER-018: New Message entity
- DER-019 to DER-023: Data integrity constraints

**API Contract Requirements (17 rules):**
- ACR-001 to ACR-003: Endpoint definition and auth
- ACR-004 to ACR-008: Request schema
- ACR-009 to ACR-013: Response schema
- ACR-014 to ACR-017: Error responses

**Stateless Flow Requirements (13 rules):**
- SFR-001 to SFR-005: Request processing
- SFR-006 to SFR-009: Context reconstruction
- SFR-010 to SFR-013: Tool call flow

**Persistence Guarantees (5 rules):**
- PGR-001 to PGR-005: State recovery and consistency

**New Entities:**
- Conversation: id, user_id, title, created_at, updated_at
- Message: id, conversation_id, role, content, tool_calls, created_at

**User Stories (P1-P2):**
- P1: Start new conversation, continue existing, survive restart
- P2: View tool calls, message ordering

## Outcome

- ✅ Impact: Complete system contracts for Phase III chat API and database extensions
- 🧪 Tests: N/A (specification document)
- 📁 Files: spec.md, checklists/requirements.md created
- 🔁 Next prompts: /sp.plan to design implementation architecture
- 🧠 Reflection: Spec maintains strict separation from Phase II while extending database schema minimally

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Checklist PASS (all 58 requirements validated)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase
