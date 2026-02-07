---
id: 001
title: Phase IV Kubernetes Helm Specification
stage: spec
date: 2026-02-02
surface: claude-code
model: claude-opus-4-5-20251101
feature: 004-k8s-helm-specs
branch: 004-k8s-helm-specs
user: AKE
command: /sp.specify
labels: [phase-iv, kubernetes, helm, minikube, deployment]
links:
  spec: specs/004-k8s-helm-specs/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/004-k8s-helm-specs/spec.md
  - specs/004-k8s-helm-specs/checklists/requirements.md
tests:
  - N/A (specification only)
---

## Prompt

/sp.specify Scope: Phase IV Kubernetes and Helm specification

Context:
The Todo AI Chatbot services have containerization specifications defined.
Phase IV now defines how these containers are deployed to a local
Kubernetes cluster using Helm.

Target environment:
- Local Kubernetes via Minikube
- External Neon PostgreSQL (no database in cluster)

Task:
Specify Kubernetes and Helm deployment architecture.

Define:
1. Namespaces and environment separation
2. Helm chart structure and responsibilities
3. Kubernetes Deployments for each containerized service
4. Kubernetes Services and networking assumptions
5. ConfigMap and Secret usage
6. Resource requests and limits
7. Liveness and readiness probe expectations
8. Scaling and restart behavior

## Response snapshot

Created comprehensive Kubernetes and Helm deployment specification:

**Deployment Architecture**:
- 2 Helm charts: `todo-frontend`, `todo-backend`
- 3 namespaces: `todo-dev`, `todo-staging`, `todo-prod`
- External PostgreSQL (NOT in cluster per K-007)

**Helm Chart Structure** (per chart):
- Chart.yaml, values.yaml
- templates/: deployment.yaml, service.yaml, configmap.yaml, NOTES.txt
- values/: dev.yaml, staging.yaml, prod.yaml

**Kubernetes Deployments**:
- Frontend: 100m-250m CPU, 128Mi-512Mi RAM, probes at `/`
- Backend: 250m-500m CPU, 256Mi-1Gi RAM, probes at `/health`

**Services**:
- Frontend: ClusterIP/NodePort on port 3000
- Backend: ClusterIP on port 8000
- DNS: `{service}.{namespace}.svc.cluster.local`

**Configuration**:
- ConfigMaps: Non-sensitive env vars
- Secrets: DATABASE_URL, SECRET_KEY, OPENAI_API_KEY, AUTH_SECRET

**Compliance**:
- 100% K-001 to K-008
- 100% H-001 to H-008

## Outcome

- Success Impact: Complete K8s/Helm architecture ready for chart implementation
- Tests: N/A (specification only)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: /sp.plan for Helm chart implementation
- Reflection: Comprehensive specification covering all deployment aspects

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements provided
- Graders run and results (PASS/FAIL): Manual checklist validation PASS (all items checked)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding Ingress specification for external access
