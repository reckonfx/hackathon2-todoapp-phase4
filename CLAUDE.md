# CLAUDE.md (Generation Guide)

This project was built entirely using **Spec-Driven Development (SDD)** with Claude Code.

## Generation Summary

- **Feature**: Todo AI Chatbot (Phase-I, Phase-II & Phase-III)
- **Methodology**: SpecKit Plus (Spec -> Plan -> Tasks -> Implement)
- **Tech Stack**:
  - **Backend**: Python 3.13+, FastAPI, SQLAlchemy, PostgreSQL, asyncpg, Alembic
  - **AI/Agent**: OpenAI Agents SDK, MCP Tools
  - **Frontend**: Next.js 15, React 19, Tailwind CSS, Web Speech API

## Claude Code Prompts

1. **/sp.constitution**: Ratified the Evolution of Todo project principles.
2. **/sp.specify**: Translated natural language requirements into a technical specification (`spec.md`).
3. **/sp.plan**: Designed the modular architecture (Models, Services, API Routes, Database) and documented in `plan.md`.
4. **/sp.tasks**: Decomposed the design into testable tasks organized by user story.
5. **/sp.implement**: Faithfully executed the tasks to produce the final application code with PostgreSQL backend support.
6. **/sp.adr**: Documented architecturally significant decisions as ADRs (Architecture Decision Records)

## Key Architecture Decisions

### Phase I-II (Backend Foundation)
- **Async Database Operations**: Uses async SQLAlchemy with PostgreSQL for scalable backend operations
- **Database Migration Strategy**: Alembic-based migration system for safe schema changes
- **Connection Pooling**: Configurable connection pooling for production-ready performance
- **Environment Configuration**: Multi-environment support (development, staging, production)
- **Separation of Concerns**: Models, Services, and API layers are properly separated

### Phase III (AI Chatbot)
- **Stateless Backend**: No in-memory conversation state; all context reconstructed from database per request
- **MCP-Only State Mutation**: All task operations performed via MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Per-Request Agent**: OpenAI agent instance created per request for stateless operation
- **Conversation Persistence**: New conversations and messages tables store chat history
- **Voice Input**: Web Speech API for browser-native speech-to-text
- **Chat Widget**: React component with real-time UI updates

## Regeneration Instructions

To regenerate or extend this project:
1. Refer to specifications in `specs/` directory:
   - Phase I-II: `specs/001-db-migration/spec.md`, `specs/002-xxx/spec.md`
   - Phase III: `specs/003-agent-mcp-tools/spec.md`, `specs/004-chat-api-db-contracts/spec.md`
2. Ensure checklist items pass in respective checklists directories
3. Follow the phase-based approach in corresponding `tasks.md` files
4. Use the Spec-Driven Development methodology for new features

## Phase III API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/{user_id}/chat` | POST | Send chat message and receive AI response |

## Phase III Database Entities

| Table | Purpose |
|-------|---------|
| `conversations` | Chat sessions between users and AI |
| `messages` | Individual messages within conversations |

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
- Backend: Copy `backend/.env.example` to `backend/.env` and configure
- Frontend: Copy `frontend/.env.example` to `frontend/.env.local` and configure
- Required: `OPENAI_API_KEY` for AI chat functionality
