# Quickstart: Chat API & Database Contracts

**Feature**: 004-chat-api-db-contracts
**Date**: 2026-01-28

## Prerequisites

- Phase II backend running and database migrated
- Python 3.13+
- PostgreSQL (Neon) connection configured
- OpenAI API key configured

## Setup Steps

### 1. Install New Dependencies

```bash
cd backend
pip install openai-agents mcp pytest-asyncio
```

### 2. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

This creates:
- `conversations` table
- `messages` table
- Required indexes and foreign keys

### 3. Configure Environment

Add to `.env`:
```
OPENAI_API_KEY=your-api-key
```

### 4. Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload
```

## Verification Steps

### V1: Database Tables Created

```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('conversations', 'messages');

-- Expected: 2 rows
```

### V2: Start New Conversation

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries to my list"}'
```

**Expected Response**:
```json
{
  "conversation_id": "uuid",
  "message_id": "uuid",
  "response": "I've added 'buy groceries' to your tasks.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"user_id": "...", "title": "buy groceries"},
      "result": {"success": true, "task": {...}}
    }
  ],
  "created_at": "2026-01-28T12:00:00Z"
}
```

### V3: Continue Conversation

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Also add milk", "conversation_id": "{conversation_id_from_v2}"}'
```

**Expected**: Agent understands context and adds "milk" as new task.

### V4: Verify Statelessness (Server Restart Test)

```bash
# 1. Note conversation_id from V2/V3
# 2. Stop server (Ctrl+C)
# 3. Start server again
uvicorn src.main:app --reload

# 4. Continue conversation
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "What tasks do I have?", "conversation_id": "{conversation_id}"}'
```

**Expected**: Full conversation history preserved, agent lists tasks including groceries and milk.

### V5: Verify Message Persistence

```sql
-- Check messages in database
SELECT m.id, m.role, m.content, m.tool_calls, m.created_at
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE c.id = '{conversation_id}'
ORDER BY m.created_at;

-- Expected: All user and assistant messages in order
```

### V6: Verify Tool Calls Recorded

```sql
-- Check tool_calls are stored
SELECT id, tool_calls
FROM messages
WHERE conversation_id = '{conversation_id}'
AND role = 'assistant'
AND tool_calls IS NOT NULL;

-- Expected: JSONB with tool invocation details
```

## Troubleshooting

### Issue: 401 Unauthorized
- Verify Better Auth token is valid
- Check token includes correct user_id

### Issue: 404 Conversation Not Found
- Verify conversation_id is correct UUID format
- Verify conversation belongs to authenticated user

### Issue: Agent Not Responding
- Check OPENAI_API_KEY is set
- Verify OpenAI API quota not exceeded
- Check backend logs for agent errors

### Issue: Database Connection Failed
- Verify DATABASE_URL in .env
- Check Neon database is accessible
- Verify migrations have run

## Test Commands

```bash
# Run all chat-related tests
cd backend
pytest tests/ -k "chat" -v

# Run specific test files
pytest tests/contract/test_chat_api.py -v
pytest tests/integration/test_conversation_flow.py -v
pytest tests/integration/test_stateless_recovery.py -v
```

## Frontend Verification Steps

### V7: Open Chat Interface

```bash
# Start frontend (if not already running)
cd frontend
npm run dev

# Open browser to chat page
open http://localhost:3000/chat
```

**Expected**: Chat interface displays with input box and send button.

### V8: Send Text Message

1. Type "Add buy groceries to my list" in input box
2. Click Send (or press Enter)

**Expected**:
- Your message appears in a chat bubble (right-aligned)
- Loading indicator shows while processing
- Assistant response appears in chat bubble (left-aligned)
- Tool call badge visible (if add_task was invoked)

### V9: Send Voice Message

1. Click the microphone button
2. Say "Show my tasks"
3. Wait for transcription

**Expected**:
- Mic button shows "listening" state (pulsing)
- Transcribed text appears in input field
- Message sends automatically (or click Send)
- Task list displayed in response

### V10: Verify Chat History Persists

1. Send several messages
2. Refresh the page (F5)
3. Observe chat interface

**Expected**:
- Chat history reloads from server
- All previous messages displayed in correct order
- Can continue conversation seamlessly

---

## Success Criteria Checklist

### Backend

- [ ] New conversation can be started (SC-001)
- [ ] Existing conversation continues with context (SC-002)
- [ ] Conversation survives server restart (SC-003)
- [ ] tool_calls included in response (SC-004)
- [ ] No orphaned messages in database (SC-005)
- [ ] No orphaned conversations in database (SC-006)
- [ ] Messages ordered correctly (SC-007)
- [ ] User message persisted before agent (SC-008)

### Frontend

- [ ] Text message flow works end-to-end (SC-009)
- [ ] Voice input converts speech to text (SC-010)
- [ ] Chat history displays after refresh (SC-011)
- [ ] Tool calls visually indicated (SC-012)
- [ ] Chat works on mobile (SC-013)
- [ ] Voice degrades gracefully in unsupported browsers (SC-014)
