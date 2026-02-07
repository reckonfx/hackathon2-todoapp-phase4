---
id: 001
title: Phase IV Deployment Governance Specification
stage: spec
date: 2026-02-02
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-deployment-governance
branch: 002-deployment-governance
user: AKE
command: /sp.specify
labels: [phase-iv, constitution, governance, deployment, kubernetes, helm]
links:
  spec: specs/002-deployment-governance/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/002-deployment-governance/spec.md
  - specs/002-deployment-governance/checklists/requirements.md
tests:
  - N/A (constitutional specification only)
---

## Prompt

/sp.specify Scope: Phase IV deployment governance

Task:
Extend the existing project constitution with a Phase IV addendum
that governs deployment and infrastructure work.

Phase IV must define:
- Deployment-only scope (no application feature or logic changes)
- Containerization rules
- Kubernetes deployment rules using Minikube
- Helm as the required deployment unit
- AI-assisted DevOps tool usage boundaries

Requirements:
- Preserve all Phase I-III rules
- Phase IV rules override earlier phases where applicable
- Explicitly prohibit database schema changes

Constraints:
- No code generation
- Output ONLY the Phase IV addendum text

## Response snapshot

Created Phase IV Deployment Governance constitutional addendum (Section 15) with:

**Core Principles**:
- 15.2.1 Deployment-Only Scope - no application logic changes
- 15.2.2 Database Schema Immutability - ABSOLUTE prohibition
- 15.2.3 Specification-Only Infrastructure
- 15.2.4 Stateless Application Preservation

**Standards Defined** (32 rules total):
- Containerization Standards: C-001 to C-008 (multi-stage builds, pinned versions, health checks)
- Kubernetes Deployment Standards: K-001 to K-008 (Minikube, Helm-only, external PostgreSQL)
- Helm Standards: H-001 to H-008 (required deployment unit, values.yaml, semantic versioning)
- AI-Assisted DevOps Standards: A-001 to A-008 (spec-only outputs, no autonomous execution)

**Override Precedence** (highest to lowest):
1. Database Schema Immutability
2. Deployment-Only Scope
3. Phase IV Addendum Rules
4. Phase III Addendum Rules
5. Core Principles
6. Technology Stack Governance

## Outcome

- Success Impact: Comprehensive governance addendum ready for constitutional ratification
- Tests: N/A (constitutional specification)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: /sp.constitution to ratify into main constitution
- Reflection: Clear separation maintained between deployment concerns and application logic

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements with explicit constraints
- Graders run and results (PASS/FAIL): Manual checklist validation PASS (all items checked)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding rollback governance rules in future iteration
