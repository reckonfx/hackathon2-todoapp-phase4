---
id: 003
title: Phase IV Kubernetes and Helm Task Generation
stage: tasks
date: 2026-02-02
surface: claude-code
model: claude-opus-4-5-20251101
feature: 004-k8s-helm-specs
branch: 004-k8s-helm-specs
user: AKE
command: /sp.tasks
labels: [phase-iv, kubernetes, helm, task-generation, minikube]
links:
  spec: specs/004-k8s-helm-specs/spec.md
  plan: specs/004-k8s-helm-specs/plan.md
  ticket:
  adr:
  pr:
files:
  - specs/004-k8s-helm-specs/tasks.md
tests:
  - N/A (task generation only)
---

## Prompt

/sp.tasks

Context:
Continuing from the K8s/Helm implementation plan (002-k8s-helm-plan.plan.prompt.md), this command generates the implementation task list organized by user story.

Task:
Generate tasks.md with:
- Setup phase (directory structure)
- Foundational phase (Chart.yaml, _helpers.tpl)
- User story phases (P1: Chart Structure, P1: Deployments, P2: Services, P2: Config/Secrets)
- Validation phase (helm lint, helm template)
- Polish phase (documentation, quickstart validation)

## Response snapshot

Generated comprehensive tasks.md with 56 tasks organized by user story:

**Phase 1: Setup (7 tasks)**
- Create helm directory structure
- Create chart directories (todo-frontend, todo-backend)
- Create templates and values subdirectories

**Phase 2: Foundational (6 tasks)**
- Constitution check for Phase IV constraints
- Create Chart.yaml for both charts
- Create _helpers.tpl for both charts

**Phase 3: User Story 1 - Helm Chart Structure (10 tasks, P1)**
- Create values.yaml for both charts
- Create environment-specific overrides (dev, staging, prod)
- Create NOTES.txt for both charts

**Phase 4: User Story 2 - Kubernetes Deployments (8 tasks, P1)**
- Create deployment.yaml templates
- Verify resource limits (CPU, memory)
- Verify liveness and readiness probes

**Phase 5: User Story 3 - Services and Networking (6 tasks, P2)**
- Create service.yaml templates
- Verify port configuration and selectors
- Document Kubernetes DNS naming

**Phase 6: User Story 4 - Configuration and Secrets (7 tasks, P2)**
- Create configmap.yaml templates
- Create secret.yaml reference documentation
- Verify secret separation (no secrets in ConfigMaps)

**Phase 7: Chart Validation (7 tasks)**
- Run helm lint for both charts
- Run helm template for both charts
- Verify H-001 to H-008 and K-001 to K-008 compliance

**Phase 8: Polish (5 tasks)**
- Update quickstart.md
- Verify namespace and secret instructions
- Run full Minikube deployment validation

**Summary**:
- Total: 56 tasks
- Parallel tasks: 24 (can run concurrently)
- MVP scope: 31 tasks (Phases 1-4)
- Full scope: 56 tasks

## Outcome

- Success Impact: Complete task list ready for implementation via /sp.implement
- Tests: N/A (task generation only, validation via helm lint/template)
- Files: 1 file created (tasks.md)
- Next prompts: /sp.implement for execution
- Reflection: Tasks well-organized by user story enabling incremental delivery

## Evaluation notes (flywheel)

- Failure modes observed: Script returned wrong feature directory (004-chat-api-db-contracts instead of 004-k8s-helm-specs); manually used correct directory
- Graders run and results (PASS/FAIL): Manual format validation PASS (all tasks follow checklist format)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add task duration estimates for planning
