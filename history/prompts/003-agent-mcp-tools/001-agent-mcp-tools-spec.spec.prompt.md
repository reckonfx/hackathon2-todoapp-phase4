---
id: PHR-SPEC-003-001
title: Agent MCP Tools Specification
stage: spec
date: 2026-01-28
surface: claude-code
model: claude-opus-4-5-20251101
feature: 003-agent-mcp-tools
branch: 003-agent-mcp-tools
user: AKE
command: /sp.specify
labels: [spec, agent, mcp, tools, phase3, contracts]
links:
  spec: specs/003-agent-mcp-tools/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/003-agent-mcp-tools/spec.md
    action: create
  - path: specs/003-agent-mcp-tools/checklists/requirements.md
    action: create
tests:
  - null
---

## Prompt

```text
Scope: AI agent behavior and MCP tool contracts

Task:
Specify the behavior of the Todo AI Chatbot agent and the MCP server tools
used for task management.

Agent Specification must define:
- Intent recognition rules
- Tool selection mapping
- Confirmation behavior
- Error handling behavior
- Prohibited behaviors (hallucinated state, implicit memory)

MCP Tool Specification must define:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task

For each tool include:
- Purpose
- Parameters (required vs optional)
- Return schema
- Error conditions

Constraints:
- No implementation code
- Output only specification documents
```

## Response snapshot

Created comprehensive specification for AI Agent Behavior & MCP Tool Contracts at `specs/003-agent-mcp-tools/spec.md`.

**Agent Specification includes:**
- 6 Intent Recognition rules (ABR-001 to ABR-006)
- 6 Tool Selection Mapping rules (ABR-007 to ABR-012)
- 4 Confirmation Behavior rules (ABR-013 to ABR-016)
- 5 Error Handling rules (ABR-017 to ABR-021)
- 6 Prohibited Behavior rules (ABR-022 to ABR-027)

**MCP Tool Contracts include:**
1. `add_task` - Create new task with title, description, due_date, priority
2. `list_tasks` - Retrieve tasks with filtering (completed, priority, date range, search)
3. `complete_task` - Mark task as completed
4. `delete_task` - Permanently remove task
5. `update_task` - Modify task properties

Each tool has complete parameter tables, return schemas, and error conditions documented.

**User Stories (P1-P3):**
- P1: Task Creation, Task Listing
- P2: Task Completion, Task Deletion
- P3: Task Updates

**Success Criteria:** 8 measurable outcomes defined.

## Outcome

- ✅ Impact: Complete behavioral and contract specification for Phase III agent and MCP tools
- 🧪 Tests: N/A (specification document)
- 📁 Files: spec.md, checklists/requirements.md created
- 🔁 Next prompts: /sp.plan to design implementation architecture
- 🧠 Reflection: Spec follows constitution requirements for agent-tool determinism and statelessness

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Checklist PASS (all items verified)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase
