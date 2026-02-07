---
id: PHR-CONST-0002
title: Phase III Constitution Ratification
stage: constitution
date: 2026-01-28
surface: claude-code
model: claude-opus-4-5-20251101
feature: phase3-constitution
branch: main
user: AKE
command: /sp.constitution
labels: [constitution, phase3, ratification, mcp, agentic]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - path: .specify/memory/constitution.md
    action: overwrite
tests:
  - null
---

## Prompt

```text
/sp.constitution

Project: Todo AI Chatbot — Phase III (Spec-Driven, Agentic MCP System)

Purpose:
Phase III governs the design, implementation, and validation of a fully functional,
AI-driven conversational todo management system built using MCP architecture,
OpenAI Agents SDK, and a stateless FastAPI backend. This phase focuses on correctness,
traceability, agent-tool alignment, and reproducible behavior across stateless requests.

────────────────────────────────────────
CORE PRINCIPLES
────────────────────────────────────────

1. Spec-First Fidelity
- All system behavior must originate from written specifications.
- No implementation is permitted without an explicit spec definition.
- Specs are the single source of truth for agent behavior, MCP tools, and API flows.

2. Agent-Tool Determinism
- AI agents must act only through MCP tools for task manipulation.
- No hidden state, implicit memory, or side-channel logic is allowed.
- Every state change must be attributable to a tool invocation.

3. Statelessness with Persistent Memory
- Backend servers and MCP tools must remain stateless across requests.
- All conversational and task state must be persisted in the database.
- System behavior must be fully recoverable after server restart.

4. Observability & Traceability
- Every user action must map to:
  user message → agent decision → MCP tool call → database mutation → response.
- Tool calls must be explicitly returned in API responses for auditability.

5. Reproducibility
- Given the same database state and user input, agent behavior must be reproducible.
- Prompts, specs, and agent configuration must be version-controlled.

────────────────────────────────────────
KEY STANDARDS
────────────────────────────────────────

Specification Standards:
- Separate specs must exist for: Agent behavior, MCP tool contracts, API request/response lifecycle
- Specs must define: Trigger conditions, Expected tool usage, Error handling behavior

Agent Standards:
- Agents must use OpenAI Agents SDK exclusively.
- Agents must: Select tools based on intent classification, Confirm all state-changing actions, Gracefully handle missing or invalid tasks
- Free-form hallucinated responses that bypass tools are disallowed.

MCP Standards:
- MCP server must use the Official MCP SDK.
- Each tool must be: Stateless, Idempotent where applicable, Fully validated against input schema
- Tools may only read/write via the database layer.

API Standards:
- Single stateless endpoint: POST /api/{user_id}/chat
- Conversation context must be reconstructed from database on every request.
- API responses must include: conversation_id, assistant response, list of MCP tool calls (if any)

────────────────────────────────────────
CONSTRAINTS
────────────────────────────────────────

Implementation Constraints:
- No manual coding outside the Agentic Dev Stack workflow.
- All code must be generated through: spec → plan → tasks → Claude Code execution.
- Direct ad-hoc edits to generated code are prohibited.

Architecture Constraints:
- Backend: Python FastAPI
- AI Logic: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- Frontend: OpenAI ChatKit

Behavioral Constraints:
- Agents must not store memory internally.
- Agents must not fabricate task IDs or task states.
- Agents must query before destructive actions when ambiguity exists.

────────────────────────────────────────
DATA & MODEL INTEGRITY
────────────────────────────────────────

Database Integrity:
- Tasks, conversations, and messages must be normalized and linked by user_id.
- No orphaned messages or tasks are allowed.
- All timestamps must be server-generated.

Conversation Integrity:
- Every user message must be persisted before agent execution.
- Every assistant message must be persisted after agent execution.
- Conversation continuity must survive server restarts.
- Behavior is reproducible and auditable via logs and tool calls.
- The full spec-driven workflow is documented and reviewable.
- The application resumes seamlessly after backend restarts.
```

## Response snapshot

Created Phase III constitution v1.0.0 at `.specify/memory/constitution.md` with:
- 5 Core Principles (Spec-First Fidelity, Agent-Tool Determinism, Statelessness with Persistent Memory, Observability & Traceability, Reproducibility)
- Key Standards (Specification, Agent, MCP, API)
- Constraints (Implementation, Architecture, Behavioral)
- Data & Model Integrity (Database, Conversation)
- Governance section with amendment procedure, versioning policy, and compliance review

## Outcome

- ✅ Impact: Constitution ratified for Phase III with all principles and constraints documented
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (overwritten)
- 🔁 Next prompts: /sp.specify to create feature specification, update plan-template.md and tasks-template.md for Phase III
- 🧠 Reflection: Successfully converted user's natural language governance rules into formal MUST/MUST NOT constitutional language

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update dependent templates (plan-template.md, tasks-template.md) to align with Phase III constitution
