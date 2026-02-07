---
id: 001
title: Phase IV Containerization Contracts Specification
stage: spec
date: 2026-02-02
surface: claude-code
model: claude-opus-4-5-20251101
feature: 003-container-specs
branch: 003-container-specs
user: AKE
command: /sp.specify
labels: [phase-iv, containers, docker, frontend, backend, mcp]
links:
  spec: specs/003-container-specs/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/003-container-specs/spec.md
  - specs/003-container-specs/checklists/requirements.md
tests:
  - N/A (specification only)
---

## Prompt

/sp.specify Scope: Phase IV containerization specification

Context:
The Todo AI Chatbot application has been fully implemented in Phase III.
Phase IV introduces containerization ONLY, with no application logic or
database schema changes permitted.

The system includes:
- Frontend: OpenAI ChatKit UI
- Backend: FastAPI + OpenAI Agents SDK
- MCP Server: Official MCP SDK (may be co-located or separate)
- Database: External Neon PostgreSQL (must NOT be containerized)

Task:
Specify containerization contracts for each deployable service. For EACH container, define:
- Container purpose
- Included components
- Excluded components
- Runtime assumptions
- Required environment variables
- Exposed ports
- Health check expectations
- Statelessness guarantees

## Response snapshot

Created containerization contracts for 2 containers (MCP co-located with backend):

**Deployment Topology**:
- `todo-frontend`: Next.js 15 application, port 3000
- `todo-backend`: FastAPI + MCP Server (co-located), port 8000
- Database: External Neon PostgreSQL (NOT containerized)

**MCP Co-Location Justification** (5 reasons):
1. In-process module sharing database session
2. No separate runtime required
3. Same async database session as API routes
4. Statelessness preserved without network overhead
5. Phase III design mandates in-process MCP

**Key Specifications**:
- Frontend: 3 required env vars, health check at `/`
- Backend: 13 env vars (4 required secrets), health check at `/health`
- All secrets marked "not baked" per C-007
- Base images: Node 20.x LTS, Python 3.13 (pinned per C-003)

**Phase IV Compliance**:
- 100% compliance with C-001 to C-008
- Compliance matrix included in specification

## Outcome

- Success Impact: Complete containerization contracts ready for Dockerfile implementation
- Tests: N/A (specification only)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: /sp.plan for implementation planning
- Reflection: MCP co-location decision well-justified by Phase III architecture

## Evaluation notes (flywheel)

- Failure modes observed: None - requirements were clear and specific
- Graders run and results (PASS/FAIL): Manual checklist validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add resource limit recommendations to spec
