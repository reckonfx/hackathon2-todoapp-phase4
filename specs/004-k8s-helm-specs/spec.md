# Feature Specification: Phase IV Kubernetes and Helm Deployment Architecture

**Feature Branch**: `004-k8s-helm-specs`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase IV Kubernetes and Helm deployment specification for local Minikube cluster"

## Overview

This specification defines the Kubernetes deployment architecture and Helm chart structure for the Todo AI Chatbot application. It establishes how containerized services are deployed, networked, configured, and scaled on a local Minikube cluster.

### Deployment Architecture Summary

| Component | Deployment Strategy | Helm Chart |
|-----------|---------------------|------------|
| Frontend | Kubernetes Deployment | `todo-frontend` |
| Backend + MCP | Kubernetes Deployment | `todo-backend` |
| Database | External (Neon PostgreSQL) | NOT in cluster |

### Key Architectural Decisions

1. **One Helm chart per service** (per H-002)
2. **External database** - PostgreSQL NOT deployed in cluster (per K-007)
3. **Namespace isolation** - Separate namespaces per environment (per K-004)
4. **ConfigMaps for non-sensitive config** - Environment variables via values.yaml
5. **Kubernetes Secrets for sensitive data** - API keys, database credentials

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Helm Chart Structure Definition (Priority: P1)

A DevOps engineer needs a clear specification of Helm chart structure and responsibilities so that charts can be created consistently for both frontend and backend services.

**Why this priority**: Chart structure must be defined before any Kubernetes resources can be specified.

**Independent Test**: Can be fully tested by verifying the specification includes chart directory structure, values.yaml schema, and template responsibilities.

**Acceptance Scenarios**:

1. **Given** the Helm chart specification, **When** reviewed by infrastructure team, **Then** chart structure is clear and follows H-001 to H-008 rules
2. **Given** the values.yaml schema, **When** environment-specific overrides are needed, **Then** all configurable values are documented and overridable
3. **Given** the chart specification, **When** release names are generated, **Then** they follow the `{service}-{environment}` pattern (per H-008)

---

### User Story 2 - Kubernetes Deployment Specification (Priority: P1)

A DevOps engineer needs complete Kubernetes Deployment specifications for frontend and backend services including resource limits, probes, and scaling behavior.

**Why this priority**: Deployments are the core Kubernetes workload; without them, nothing runs.

**Independent Test**: Can be fully tested by verifying specifications include all required fields for Kubernetes Deployment resources.

**Acceptance Scenarios**:

1. **Given** the Deployment specification, **When** backend pods start, **Then** they use the specified resource requests and limits
2. **Given** the Deployment specification, **When** a pod fails health checks, **Then** Kubernetes restarts it according to the specified policy
3. **Given** the Deployment specification, **When** multiple replicas are requested, **Then** pods are distributed and stateless

---

### User Story 3 - Service and Networking Specification (Priority: P2)

A DevOps engineer needs Kubernetes Service specifications that enable frontend-to-backend communication and external access within Minikube.

**Why this priority**: Services enable pod-to-pod communication and external access.

**Independent Test**: Can be fully tested by verifying Service specifications include type, ports, and selectors.

**Acceptance Scenarios**:

1. **Given** the Service specification, **When** frontend pods call backend, **Then** they use Kubernetes DNS naming (per K-008)
2. **Given** the Service specification, **When** external access is needed, **Then** Minikube NodePort or Ingress is specified

---

### User Story 4 - Configuration and Secrets Management (Priority: P2)

A DevOps engineer needs clear separation between ConfigMaps (non-sensitive) and Secrets (sensitive) with all values flowing through Helm values.yaml.

**Why this priority**: Proper secret management is critical for security compliance.

**Independent Test**: Can be fully tested by verifying no secrets appear in ConfigMaps and all configuration flows through values.yaml.

**Acceptance Scenarios**:

1. **Given** the configuration specification, **When** non-sensitive values are needed, **Then** they are provided via ConfigMap
2. **Given** the configuration specification, **When** API keys or passwords are needed, **Then** they are provided via Kubernetes Secret
3. **Given** the values.yaml schema, **When** secrets are specified, **Then** they reference Secret objects (not plaintext values)

---

### Edge Cases

- What happens when external database is unreachable? Pods start but report unhealthy; Kubernetes does not restart (database is external).
- What happens when Helm release already exists? Upgrade behavior is defined; duplicate installs fail cleanly.
- What happens when resource limits are exceeded? Pod is OOMKilled and restarted according to restart policy.
- What happens when Minikube runs out of resources? Pods remain Pending; clear error messages in pod status.

---

## Namespace Architecture

### Environment Separation (per K-004)

| Environment | Namespace | Purpose |
|-------------|-----------|---------|
| Development | `todo-dev` | Local development and testing |
| Staging | `todo-staging` | Pre-production validation |
| Production | `todo-prod` | Production deployment |

### Namespace Isolation Rules

- Each namespace contains complete application stack (frontend + backend)
- No cross-namespace resource references (except external database)
- Resource quotas applied per namespace (recommended)
- Network policies optional for Minikube (recommended for production)

---

## Helm Chart Specifications

### Chart 1: `todo-frontend`

#### Chart Metadata

| Field | Value |
|-------|-------|
| Chart Name | `todo-frontend` |
| Version | Semantic versioning (e.g., 1.0.0) |
| App Version | Matches container image tag |
| Description | Helm chart for Todo AI Chatbot frontend service |

#### Directory Structure

```
todo-frontend/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration
├── templates/
│   ├── _helpers.tpl     # Template helpers
│   ├── deployment.yaml  # Kubernetes Deployment
│   ├── service.yaml     # Kubernetes Service
│   ├── configmap.yaml   # Non-sensitive configuration
│   └── NOTES.txt        # Post-install instructions (per H-006)
└── values/
    ├── dev.yaml         # Development overrides
    ├── staging.yaml     # Staging overrides
    └── prod.yaml        # Production overrides
```

#### values.yaml Schema

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `replicaCount` | integer | No | 1 | Number of pod replicas |
| `image.repository` | string | Yes | - | Container image repository |
| `image.tag` | string | Yes | - | Container image tag |
| `image.pullPolicy` | string | No | `IfNotPresent` | Image pull policy |
| `service.type` | string | No | `ClusterIP` | Kubernetes Service type |
| `service.port` | integer | No | 3000 | Service port |
| `resources.requests.cpu` | string | No | `100m` | CPU request |
| `resources.requests.memory` | string | No | `128Mi` | Memory request |
| `resources.limits.cpu` | string | No | `250m` | CPU limit |
| `resources.limits.memory` | string | No | `512Mi` | Memory limit |
| `env.NEXT_PUBLIC_API_URL` | string | Yes | - | Backend API URL |
| `env.NODE_ENV` | string | No | `production` | Node environment |
| `probes.liveness.path` | string | No | `/` | Liveness probe path |
| `probes.readiness.path` | string | No | `/` | Readiness probe path |

---

### Chart 2: `todo-backend`

#### Chart Metadata

| Field | Value |
|-------|-------|
| Chart Name | `todo-backend` |
| Version | Semantic versioning (e.g., 1.0.0) |
| App Version | Matches container image tag |
| Description | Helm chart for Todo AI Chatbot backend service (includes MCP) |

#### Directory Structure

```
todo-backend/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration
├── templates/
│   ├── _helpers.tpl     # Template helpers
│   ├── deployment.yaml  # Kubernetes Deployment
│   ├── service.yaml     # Kubernetes Service
│   ├── configmap.yaml   # Non-sensitive configuration
│   ├── secret.yaml      # Secret reference template
│   └── NOTES.txt        # Post-install instructions (per H-006)
└── values/
    ├── dev.yaml         # Development overrides
    ├── staging.yaml     # Staging overrides
    └── prod.yaml        # Production overrides
```

#### values.yaml Schema

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `replicaCount` | integer | No | 1 | Number of pod replicas |
| `image.repository` | string | Yes | - | Container image repository |
| `image.tag` | string | Yes | - | Container image tag |
| `image.pullPolicy` | string | No | `IfNotPresent` | Image pull policy |
| `service.type` | string | No | `ClusterIP` | Kubernetes Service type |
| `service.port` | integer | No | 8000 | Service port |
| `resources.requests.cpu` | string | No | `250m` | CPU request |
| `resources.requests.memory` | string | No | `256Mi` | Memory request |
| `resources.limits.cpu` | string | No | `500m` | CPU limit |
| `resources.limits.memory` | string | No | `1Gi` | Memory limit |
| `env.BACKEND_ENV` | string | No | `production` | Backend environment |
| `env.CORS_ORIGINS` | string | Yes | - | Allowed CORS origins |
| `secrets.databaseUrl` | secretRef | Yes | - | Reference to DATABASE_URL secret |
| `secrets.secretKey` | secretRef | Yes | - | Reference to SECRET_KEY secret |
| `secrets.openaiApiKey` | secretRef | Yes | - | Reference to OPENAI_API_KEY secret |
| `secrets.authSecret` | secretRef | Yes | - | Reference to AUTH_SECRET secret |
| `probes.liveness.path` | string | No | `/health` | Liveness probe path |
| `probes.readiness.path` | string | No | `/health` | Readiness probe path |
| `probes.liveness.initialDelaySeconds` | integer | No | 10 | Initial delay |
| `probes.readiness.initialDelaySeconds` | integer | No | 5 | Initial delay |

---

## Kubernetes Deployment Specifications

### Frontend Deployment

| Field | Specification |
|-------|---------------|
| **Kind** | Deployment |
| **Replicas** | 1 (configurable via values.yaml) |
| **Strategy** | RollingUpdate (default) |
| **Container Image** | `todo-frontend:{tag}` |
| **Container Port** | 3000 |

#### Resource Specifications

| Resource | Request | Limit |
|----------|---------|-------|
| CPU | 100m | 250m |
| Memory | 128Mi | 512Mi |

#### Liveness Probe

| Field | Value |
|-------|-------|
| Type | HTTP GET |
| Path | `/` |
| Port | 3000 |
| Initial Delay | 10 seconds |
| Period | 30 seconds |
| Timeout | 5 seconds |
| Failure Threshold | 3 |

#### Readiness Probe

| Field | Value |
|-------|-------|
| Type | HTTP GET |
| Path | `/` |
| Port | 3000 |
| Initial Delay | 5 seconds |
| Period | 10 seconds |
| Timeout | 5 seconds |
| Failure Threshold | 3 |

---

### Backend Deployment

| Field | Specification |
|-------|---------------|
| **Kind** | Deployment |
| **Replicas** | 1 (configurable via values.yaml) |
| **Strategy** | RollingUpdate (default) |
| **Container Image** | `todo-backend:{tag}` |
| **Container Port** | 8000 |

#### Resource Specifications

| Resource | Request | Limit |
|----------|---------|-------|
| CPU | 250m | 500m |
| Memory | 256Mi | 1Gi |

#### Liveness Probe

| Field | Value |
|-------|-------|
| Type | HTTP GET |
| Path | `/health` |
| Port | 8000 |
| Initial Delay | 15 seconds |
| Period | 30 seconds |
| Timeout | 10 seconds |
| Failure Threshold | 3 |

#### Readiness Probe

| Field | Value |
|-------|-------|
| Type | HTTP GET |
| Path | `/health` |
| Port | 8000 |
| Initial Delay | 10 seconds |
| Period | 10 seconds |
| Timeout | 10 seconds |
| Failure Threshold | 3 |

---

## Kubernetes Service Specifications

### Frontend Service

| Field | Specification |
|-------|---------------|
| **Kind** | Service |
| **Type** | ClusterIP (internal), NodePort (external access) |
| **Port** | 3000 |
| **Target Port** | 3000 |
| **Protocol** | TCP |
| **Selector** | `app: todo-frontend` |

#### DNS Name (per K-008)

- Internal: `todo-frontend.{namespace}.svc.cluster.local`
- Short: `todo-frontend` (within same namespace)

### Backend Service

| Field | Specification |
|-------|---------------|
| **Kind** | Service |
| **Type** | ClusterIP |
| **Port** | 8000 |
| **Target Port** | 8000 |
| **Protocol** | TCP |
| **Selector** | `app: todo-backend` |

#### DNS Name (per K-008)

- Internal: `todo-backend.{namespace}.svc.cluster.local`
- Short: `todo-backend` (within same namespace)

---

## ConfigMap and Secret Specifications

### ConfigMap: `todo-frontend-config`

Contains non-sensitive environment variables for frontend.

| Key | Source | Description |
|-----|--------|-------------|
| `NODE_ENV` | values.yaml | Runtime environment |

### ConfigMap: `todo-backend-config`

Contains non-sensitive environment variables for backend.

| Key | Source | Description |
|-----|--------|-------------|
| `BACKEND_ENV` | values.yaml | Runtime environment |
| `BACKEND_HOST` | values.yaml | Listen host |
| `BACKEND_PORT` | values.yaml | Listen port |
| `CORS_ORIGINS` | values.yaml | Allowed CORS origins |
| `POOL_SIZE` | values.yaml | DB connection pool size |
| `MAX_OVERFLOW` | values.yaml | DB pool overflow |
| `POOL_TIMEOUT` | values.yaml | DB pool timeout |
| `CHAT_MAX_MESSAGES` | values.yaml | Max messages per conversation |

### Secret: `todo-backend-secrets`

Contains sensitive credentials. **Values are NOT in Helm chart** - referenced from pre-created Kubernetes Secrets or external secret management.

| Key | Type | Description |
|-----|------|-------------|
| `DATABASE_URL` | secretKeyRef | PostgreSQL connection string |
| `SECRET_KEY` | secretKeyRef | JWT signing key |
| `OPENAI_API_KEY` | secretKeyRef | OpenAI API key |
| `AUTH_SECRET` | secretKeyRef | Authentication secret |

#### Secret Management Options

1. **Pre-created Secrets**: Create Kubernetes Secrets manually before Helm install
2. **External Secrets Operator**: Reference secrets from external vault (future)
3. **Sealed Secrets**: Encrypt secrets in Git (future)

**Recommendation for Minikube**: Pre-created Secrets with kubectl

---

## Scaling and Restart Behavior

### Scaling Specification

| Service | Min Replicas | Max Replicas | Scaling Trigger |
|---------|--------------|--------------|-----------------|
| Frontend | 1 | 3 | Manual (HPA optional) |
| Backend | 1 | 3 | Manual (HPA optional) |

#### Horizontal Pod Autoscaler (Optional)

For future production use:
- Target CPU utilization: 70%
- Scale-up stabilization: 60 seconds
- Scale-down stabilization: 300 seconds

### Restart Policy

| Scenario | Behavior |
|----------|----------|
| Container crash | Restart immediately (RestartPolicy: Always) |
| Liveness probe failure | Kill and restart container |
| Readiness probe failure | Remove from Service endpoints (no restart) |
| Node failure | Reschedule pods to healthy nodes |
| OOMKilled | Restart with potential backoff |

### Pod Disruption Budget (Recommended)

| Service | Min Available | Max Unavailable |
|---------|---------------|-----------------|
| Frontend | 1 | 1 |
| Backend | 1 | 1 |

---

## Phase IV Compliance Matrix

### Kubernetes Rules (K-001 to K-008)

| Rule ID | Rule | Status |
|---------|------|--------|
| K-001 | Minikube is the required local environment | Compliant |
| K-002 | All deployments MUST use Helm | Compliant |
| K-003 | No direct kubectl apply in production | Compliant |
| K-004 | Namespace isolation specified | Compliant (todo-dev/staging/prod) |
| K-005 | Resource limits specified | Compliant |
| K-006 | Liveness and readiness probes configured | Compliant |
| K-007 | PostgreSQL remains external | Compliant |
| K-008 | Kubernetes DNS naming | Compliant |

### Helm Rules (H-001 to H-008)

| Rule ID | Rule | Status |
|---------|------|--------|
| H-001 | Helm is ONLY deployment unit | Compliant |
| H-002 | Each service has own chart | Compliant (2 charts) |
| H-003 | Values exposed via values.yaml | Compliant |
| H-004 | Environment-specific overrides | Compliant (values/*.yaml) |
| H-005 | Semantic versioning | Compliant |
| H-006 | NOTES.txt included | Compliant |
| H-007 | No hardcoded env values | Compliant |
| H-008 | Release name pattern | Compliant (`{service}-{env}`) |

---

## Phase Context & Constraints *(Phase-IV)*

- **Scope**: Kubernetes and Helm specification ONLY — no YAML generation
- **Target**: Local Minikube cluster
- **Database**: External Neon PostgreSQL (NOT in cluster per K-007)
- **Deployment**: Helm is the ONLY deployment mechanism (per K-002, H-001)
- **Configuration**: All values flow through values.yaml (per H-003)
- **Secrets**: Referenced from Kubernetes Secrets, not embedded (per C-007)
- **External Specs**: Container specs at `specs/003-container-specs/spec.md`

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Two Helm charts MUST be specified: `todo-frontend` and `todo-backend`
- **FR-002**: Each chart MUST include complete values.yaml schema documentation
- **FR-003**: Kubernetes Deployments MUST specify resource requests and limits
- **FR-004**: All pods MUST have liveness and readiness probes configured
- **FR-005**: Services MUST use Kubernetes DNS naming conventions
- **FR-006**: ConfigMaps MUST contain only non-sensitive configuration
- **FR-007**: Secrets MUST be referenced (not embedded) from Kubernetes Secrets
- **FR-008**: Namespace isolation MUST be specified for dev/staging/prod
- **FR-009**: Chart directory structures MUST include NOTES.txt
- **FR-010**: All specifications MUST comply with K-001 to K-008 and H-001 to H-008

### Key Entities

- **Helm Chart**: A package of Kubernetes resources with templated configuration
- **Kubernetes Deployment**: A workload controller managing pod replicas
- **Kubernetes Service**: A network abstraction for pod-to-pod communication
- **ConfigMap**: A Kubernetes resource for non-sensitive configuration
- **Secret**: A Kubernetes resource for sensitive credentials
- **Namespace**: A Kubernetes resource for environment isolation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% compliance with Kubernetes rules K-001 to K-008
- **SC-002**: 100% compliance with Helm rules H-001 to H-008
- **SC-003**: Both Helm charts have complete values.yaml schema documentation
- **SC-004**: All Deployments have resource requests and limits specified
- **SC-005**: All pods have liveness and readiness probes defined
- **SC-006**: No secrets appear in ConfigMaps or chart templates
- **SC-007**: Three namespaces are defined (dev, staging, prod)
- **SC-008**: Infrastructure team can review and approve specifications without YAML

## Assumptions

- Minikube has sufficient resources (4GB RAM, 2 CPUs recommended)
- External Neon PostgreSQL is accessible from Minikube cluster
- OpenAI API is accessible from Minikube cluster
- Secrets are pre-created in Kubernetes before Helm install
- Docker images are available in a registry accessible to Minikube
- Helm 3.x is installed on the deployment workstation
