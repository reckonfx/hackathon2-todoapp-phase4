# Implementation Plan: Phase IV Kubernetes and Helm Deployment Architecture

**Branch**: `004-k8s-helm-specs` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-k8s-helm-specs/spec.md`

## Summary

This plan defines the implementation approach for creating Kubernetes and Helm deployment artifacts for the Todo AI Chatbot application. The specification establishes a 2-chart Helm architecture (`todo-frontend`, `todo-backend`) with 3-namespace environment isolation (`todo-dev`, `todo-staging`, `todo-prod`), deployed to local Minikube. All configurations flow through values.yaml with environment-specific overrides.

## Technical Context

**Language/Version**: YAML (Helm 3.x templates, Kubernetes 1.28+)
**Primary Dependencies**: Helm 3.x, Kubernetes (Minikube), Docker images from 003-container-specs
**Storage**: External Neon PostgreSQL (NOT in cluster per K-007)
**Testing**: Helm lint, Helm template validation, kubectl dry-run
**Target Platform**: Local Minikube cluster
**Project Type**: Infrastructure/Deployment (Helm charts)
**Performance Goals**: Pods ready within 60 seconds, health checks passing
**Constraints**: Resource limits per spec (Frontend: 100m-250m CPU, 128Mi-512Mi RAM; Backend: 250m-500m CPU, 256Mi-1Gi RAM)
**Scale/Scope**: 2 Helm charts, 3 namespaces, 2 Deployments, 2 Services, 2 ConfigMaps, 1 Secret reference template

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-First Development
- [x] Is there a corresponding feature specification in `specs/`?
- [x] Does this plan directly address the requirements in the spec?

### II. No Manual Coding
- [x] Is the implementation strategy designed for agent execution?
- [x] Are we avoiding any manual code generation?

### III. Reusable Intelligence
- [x] Are new capabilities abstracted into reusable skills? (helm-chart-design, kubernetes-deployment-skill)
- [x] Is behavior separated from execution tools?

### IV. Deterministic Architecture
- [x] Are the outputs and behaviors predictable and testable?
- [x] Is there any hidden or implicit logic? (No - all values flow through values.yaml)

### V. Progressive Evolution
- [x] Does this implementation build on the previous phase without skipping steps?
- [x] Is forward compatibility maintained for Phase-V and beyond?

### VI. Phase-Specific Constraints (Phase-IV)
- [x] Deployment-only scope? (No application code changes)
- [x] Database schema immutable? (External PostgreSQL, connection config only)
- [x] All infrastructure spec-driven? (Specification artifacts produced)
- [x] Helm as ONLY deployment mechanism? (per K-002, H-001)
- [x] No direct kubectl apply in production? (per K-003)
- [x] AI agents specification-only? (per A-006)

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-helm-specs/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Helm best practices
├── data-model.md        # Phase 1 output - Kubernetes resource relationships
├── quickstart.md        # Phase 1 output - Deployment quick reference
├── contracts/           # Phase 1 output - Helm chart interfaces
│   ├── todo-frontend-chart.md
│   └── todo-backend-chart.md
├── checklists/
│   └── requirements.md  # Specification checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Helm Charts (to be created via /sp.implement)
helm/
├── todo-frontend/
│   ├── Chart.yaml           # Chart metadata
│   ├── values.yaml          # Default configuration
│   ├── templates/
│   │   ├── _helpers.tpl     # Template helpers
│   │   ├── deployment.yaml  # Kubernetes Deployment
│   │   ├── service.yaml     # Kubernetes Service
│   │   ├── configmap.yaml   # Non-sensitive configuration
│   │   └── NOTES.txt        # Post-install instructions
│   └── values/
│       ├── dev.yaml         # Development overrides
│       ├── staging.yaml     # Staging overrides
│       └── prod.yaml        # Production overrides
│
└── todo-backend/
    ├── Chart.yaml           # Chart metadata
    ├── values.yaml          # Default configuration
    ├── templates/
    │   ├── _helpers.tpl     # Template helpers
    │   ├── deployment.yaml  # Kubernetes Deployment
    │   ├── service.yaml     # Kubernetes Service
    │   ├── configmap.yaml   # Non-sensitive configuration
    │   ├── secret.yaml      # Secret reference template
    │   └── NOTES.txt        # Post-install instructions
    └── values/
        ├── dev.yaml         # Development overrides
        ├── staging.yaml     # Staging overrides
        └── prod.yaml        # Production overrides
```

**Structure Decision**: Two independent Helm charts in `helm/` directory at repository root. Each chart is self-contained with environment-specific value overrides in `values/` subdirectory. This follows H-002 (one chart per service) and enables independent versioning and deployment.

## Implementation Phases

### Phase 0: Research (Complete)

See [research.md](./research.md) for Helm chart best practices, Kubernetes deployment patterns, and Minikube-specific considerations.

### Phase 1: Design Artifacts

| Artifact | Purpose | Location |
|----------|---------|----------|
| Data Model | Kubernetes resource relationships | [data-model.md](./data-model.md) |
| Frontend Chart Contract | Helm interface specification | [contracts/todo-frontend-chart.md](./contracts/todo-frontend-chart.md) |
| Backend Chart Contract | Helm interface specification | [contracts/todo-backend-chart.md](./contracts/todo-backend-chart.md) |
| Quickstart | Deployment reference guide | [quickstart.md](./quickstart.md) |

### Phase 2: Task Generation

Tasks will be generated via `/sp.tasks` command after design artifacts are complete.

**Expected Task Groups**:
1. Namespace Setup (create todo-dev, todo-staging, todo-prod)
2. Secret Pre-creation (DATABASE_URL, SECRET_KEY, OPENAI_API_KEY, AUTH_SECRET)
3. Frontend Helm Chart Implementation
4. Backend Helm Chart Implementation
5. Chart Validation (helm lint, helm template)
6. Deployment Verification (health checks, connectivity)

## Dependencies

### From Previous Specifications

| Dependency | Source | Status |
|------------|--------|--------|
| Container specifications | specs/003-container-specs/spec.md | Complete |
| Frontend Docker image | Dockerfile (to be created) | Pending |
| Backend Docker image | Dockerfile (to be created) | Pending |
| Phase III Application | backend/, frontend/ | Frozen |

### External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Minikube | Latest | Local Kubernetes cluster |
| Helm | 3.x | Package manager |
| kubectl | 1.28+ | Kubernetes CLI |
| External PostgreSQL | Neon | Database (connection only) |

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| Minikube resource constraints | Specify minimum 4GB RAM, 2 CPUs in quickstart |
| External database connectivity | Document Minikube tunnel/port-forward for external access |
| Secret management complexity | Pre-created secrets with kubectl, document in quickstart |
| Image pull failures | Use Minikube's built-in registry or local image loading |

## Compliance Matrix

### Phase IV Rules Coverage

| Category | Rules | Status |
|----------|-------|--------|
| Containerization | C-001 to C-008 | Addressed in 003-container-specs |
| Kubernetes | K-001 to K-008 | Fully addressed in this spec |
| Helm | H-001 to H-008 | Fully addressed in this spec |
| AI DevOps | A-001 to A-008 | Specification artifacts only |

### Success Criteria Mapping

| Criteria | Implementation | Validation |
|----------|----------------|------------|
| SC-001: K-001 to K-008 compliance | All Kubernetes rules followed | Checklist verification |
| SC-002: H-001 to H-008 compliance | All Helm rules followed | Checklist verification |
| SC-003: Complete values.yaml schemas | Both charts have documented schemas | Schema review |
| SC-004: Resource limits specified | Deployment templates include limits | Template inspection |
| SC-005: Probes defined | Liveness/readiness in deployments | Template inspection |
| SC-006: No secrets in ConfigMaps | Secrets via secretKeyRef only | Template audit |
| SC-007: Three namespaces | dev/staging/prod defined | Namespace verification |
| SC-008: Infrastructure team review | Specification-only artifacts | Process verification |

## Complexity Tracking

> No constitution violations identified. Implementation follows spec-driven approach with AI-generated artifacts.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| 2 Helm charts | Appropriate | H-002 requires one chart per service |
| 3 namespaces | Appropriate | K-004 requires namespace isolation |
| Environment overrides | Appropriate | H-004 requires environment-specific values |
