# Data Model: Kubernetes Resource Relationships

**Feature**: 004-k8s-helm-specs
**Date**: 2026-02-02
**Purpose**: Document the relationships between Kubernetes resources, Helm charts, and external dependencies.

## 1. Resource Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KUBERNETES CLUSTER (Minikube)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    NAMESPACE: todo-dev                               │   │
│  │  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │   │
│  │  │   HELM RELEASE:             │  │   HELM RELEASE:             │   │   │
│  │  │   todo-frontend-dev         │  │   todo-backend-dev          │   │   │
│  │  │                             │  │                             │   │   │
│  │  │  ┌─────────────────────┐    │  │  ┌─────────────────────┐    │   │   │
│  │  │  │    Deployment       │    │  │  │    Deployment       │    │   │   │
│  │  │  │  todo-frontend-dev  │    │  │  │  todo-backend-dev   │    │   │   │
│  │  │  │        │            │    │  │  │        │            │    │   │   │
│  │  │  │        ▼            │    │  │  │        ▼            │    │   │   │
│  │  │  │  ┌──────────┐       │    │  │  │  ┌──────────┐       │    │   │   │
│  │  │  │  │   Pod    │       │    │  │  │  │   Pod    │       │    │   │   │
│  │  │  │  │ (replica)│       │    │  │  │  │ (replica)│       │    │   │   │
│  │  │  │  └──────────┘       │    │  │  │  └──────────┘       │    │   │   │
│  │  │  └─────────────────────┘    │  │  └─────────────────────┘    │   │   │
│  │  │                             │  │                             │   │   │
│  │  │  ┌─────────────────────┐    │  │  ┌─────────────────────┐    │   │   │
│  │  │  │      Service        │    │  │  │      Service        │    │   │   │
│  │  │  │  todo-frontend      │────┼──┼──│  todo-backend       │    │   │   │
│  │  │  │  (ClusterIP/NodePort)│   │  │  │  (ClusterIP)        │    │   │   │
│  │  │  └─────────────────────┘    │  │  └─────────────────────┘    │   │   │
│  │  │                             │  │            │                │   │   │
│  │  │  ┌─────────────────────┐    │  │            │                │   │   │
│  │  │  │    ConfigMap        │    │  │  ┌─────────────────────┐    │   │   │
│  │  │  │ todo-frontend-config│    │  │  │    ConfigMap        │    │   │   │
│  │  │  └─────────────────────┘    │  │  │ todo-backend-config │    │   │   │
│  │  │                             │  │  └─────────────────────┘    │   │   │
│  │  └─────────────────────────────┘  │                             │   │   │
│  │                                   │  ┌─────────────────────┐    │   │   │
│  │                                   │  │      Secret         │    │   │   │
│  │                                   │  │ todo-backend-secrets│    │   │   │
│  │                                   │  │   (pre-created)     │    │   │   │
│  │                                   │  └─────────────────────┘    │   │   │
│  │                                   └─────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    NAMESPACE: todo-staging                           │   │
│  │                         (same structure)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    NAMESPACE: todo-prod                              │   │
│  │                         (same structure)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ DATABASE_URL
                                      ▼
                    ┌─────────────────────────────────────┐
                    │      EXTERNAL SERVICE               │
                    │      Neon PostgreSQL                │
                    │   (NOT in cluster - per K-007)      │
                    └─────────────────────────────────────┘
```

## 2. Helm Chart to Kubernetes Mapping

### 2.1 todo-frontend Chart

| Helm Template | Kubernetes Resource | Resource Name Pattern |
|---------------|--------------------|-----------------------|
| `deployment.yaml` | Deployment | `{release-name}` |
| `service.yaml` | Service | `{release-name}` |
| `configmap.yaml` | ConfigMap | `{release-name}-config` |
| `_helpers.tpl` | (template helpers) | N/A |
| `NOTES.txt` | (post-install output) | N/A |

### 2.2 todo-backend Chart

| Helm Template | Kubernetes Resource | Resource Name Pattern |
|---------------|--------------------|-----------------------|
| `deployment.yaml` | Deployment | `{release-name}` |
| `service.yaml` | Service | `{release-name}` |
| `configmap.yaml` | ConfigMap | `{release-name}-config` |
| `secret.yaml` | Secret reference | `{release-name}-secrets` (pre-created) |
| `_helpers.tpl` | (template helpers) | N/A |
| `NOTES.txt` | (post-install output) | N/A |

## 3. Resource Dependencies

### 3.1 Deployment Dependencies

```
┌──────────────────────┐
│     Deployment       │
│   (todo-frontend)    │
└──────────┬───────────┘
           │ requires
           ▼
┌──────────────────────┐     ┌──────────────────────┐
│     ConfigMap        │     │   Container Image    │
│ (todo-frontend-config)│     │  (todo-frontend:tag) │
└──────────────────────┘     └──────────────────────┘


┌──────────────────────┐
│     Deployment       │
│   (todo-backend)     │
└──────────┬───────────┘
           │ requires
           ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│     ConfigMap        │  │       Secret         │  │   Container Image    │
│ (todo-backend-config)│  │ (todo-backend-secrets)│  │  (todo-backend:tag)  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
                                    │
                                    │ contains
                                    ▼
                          ┌──────────────────────┐
                          │  - DATABASE_URL      │
                          │  - SECRET_KEY        │
                          │  - OPENAI_API_KEY    │
                          │  - AUTH_SECRET       │
                          └──────────────────────┘
```

### 3.2 Service Dependencies

```
┌──────────────────────┐
│       Service        │
│   (todo-frontend)    │──────────┐
└──────────────────────┘          │
                                  │ routes traffic to
                                  ▼
                          ┌──────────────────────┐
                          │     Pods matching    │
                          │  selector labels     │
                          │ app: todo-frontend   │
                          └──────────────────────┘


┌──────────────────────┐
│       Service        │
│   (todo-backend)     │──────────┐
└──────────────────────┘          │
                                  │ routes traffic to
                                  ▼
                          ┌──────────────────────┐
                          │     Pods matching    │
                          │  selector labels     │
                          │  app: todo-backend   │
                          └──────────────────────┘
```

## 4. Label Selectors

### 4.1 Standard Labels (per Kubernetes conventions)

| Label | Value Pattern | Purpose |
|-------|---------------|---------|
| `app.kubernetes.io/name` | `todo-frontend` or `todo-backend` | Application name |
| `app.kubernetes.io/instance` | `{release-name}` | Helm release instance |
| `app.kubernetes.io/version` | `{app-version}` | Application version |
| `app.kubernetes.io/managed-by` | `Helm` | Management tool |
| `helm.sh/chart` | `{chart-name}-{chart-version}` | Chart identification |

### 4.2 Selector Labels (for Service matching)

| Label | Value Pattern | Used By |
|-------|---------------|---------|
| `app.kubernetes.io/name` | `todo-frontend` | Frontend Service selector |
| `app.kubernetes.io/instance` | `{release-name}` | Frontend Service selector |
| `app.kubernetes.io/name` | `todo-backend` | Backend Service selector |
| `app.kubernetes.io/instance` | `{release-name}` | Backend Service selector |

## 5. Network Communication Paths

### 5.1 Internal Communication

```
┌─────────────────┐    HTTP :8000    ┌─────────────────┐
│                 │  ───────────────▶│                 │
│  Frontend Pod   │                  │  Backend Pod    │
│  (Next.js)      │                  │  (FastAPI+MCP)  │
│                 │◀─────────────────│                 │
└─────────────────┘    JSON Response └─────────────────┘
        │                                    │
        │ DNS: todo-backend                  │ DATABASE_URL
        │      (short name)                  │ (from Secret)
        │                                    │
        ▼                                    ▼
┌─────────────────┐               ┌─────────────────┐
│     Service     │               │  External DB    │
│  todo-backend   │               │  (Neon PG)      │
│  :8000          │               │                 │
└─────────────────┘               └─────────────────┘
```

### 5.2 External Access Paths

```
                                    ┌─────────────────────────┐
                                    │      Minikube Node      │
                                    │                         │
┌──────────┐    NodePort :30XXX     │  ┌─────────────────┐    │
│  User    │  ─────────────────────▶│  │    Service      │    │
│ Browser  │                        │  │  todo-frontend  │    │
│          │◀─────────────────────  │  │  (NodePort)     │    │
└──────────┘                        │  └─────────────────┘    │
                                    │          │              │
            OR                      │          ▼              │
                                    │  ┌─────────────────┐    │
┌──────────┐   port-forward :3000   │  │  Frontend Pod   │    │
│  User    │  ─────────────────────▶│  │                 │    │
│ Browser  │                        │  └─────────────────┘    │
│          │◀─────────────────────  │                         │
└──────────┘                        └─────────────────────────┘
```

## 6. Environment Variable Flow

### 6.1 Frontend Environment Variables

| Variable | Source | Flow Path |
|----------|--------|-----------|
| `NODE_ENV` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `NEXT_PUBLIC_API_URL` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |

### 6.2 Backend Environment Variables

| Variable | Source | Flow Path |
|----------|--------|-----------|
| `BACKEND_ENV` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `BACKEND_HOST` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `BACKEND_PORT` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `CORS_ORIGINS` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `POOL_SIZE` | values.yaml → ConfigMap | ConfigMap → Pod envFrom |
| `DATABASE_URL` | Pre-created Secret | Secret → Pod env secretKeyRef |
| `SECRET_KEY` | Pre-created Secret | Secret → Pod env secretKeyRef |
| `OPENAI_API_KEY` | Pre-created Secret | Secret → Pod env secretKeyRef |
| `AUTH_SECRET` | Pre-created Secret | Secret → Pod env secretKeyRef |

## 7. Namespace Isolation Model

### 7.1 Resource Boundaries

| Namespace | Contains | Isolation Level |
|-----------|----------|-----------------|
| `todo-dev` | Full app stack (frontend + backend) | Complete |
| `todo-staging` | Full app stack (frontend + backend) | Complete |
| `todo-prod` | Full app stack (frontend + backend) | Complete |

### 7.2 Cross-Namespace Access

| Access Type | Allowed | Reason |
|-------------|---------|--------|
| Pod-to-Pod (same namespace) | Yes | Same-namespace communication |
| Pod-to-Pod (different namespace) | No | Namespace isolation |
| Pod-to-External DB | Yes | External to cluster |
| Service DNS cross-namespace | Not used | Each namespace has own stack |

## 8. Resource Scaling Model

### 8.1 Horizontal Scaling

```
┌────────────────────────────────────────────────────────┐
│                   Deployment                           │
│                  (replicaCount=2)                      │
│                                                        │
│    ┌──────────┐    ┌──────────┐                       │
│    │   Pod    │    │   Pod    │                       │
│    │ replica-1│    │ replica-2│                       │
│    └────┬─────┘    └────┬─────┘                       │
│         │               │                              │
│         └───────┬───────┘                              │
│                 ▼                                      │
│         ┌─────────────┐                                │
│         │   Service   │                                │
│         │ (load bal.) │                                │
│         └─────────────┘                                │
└────────────────────────────────────────────────────────┘
```

### 8.2 Scaling Limits (per spec)

| Service | Min | Max | Scaling Trigger |
|---------|-----|-----|-----------------|
| Frontend | 1 | 3 | Manual or HPA (optional) |
| Backend | 1 | 3 | Manual or HPA (optional) |

## 9. Health Check Model

### 9.1 Probe Flow

```
                    ┌───────────────────────────┐
                    │      Kubernetes           │
                    │   Probe Controller        │
                    └─────────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │ Liveness     │      │ Readiness    │      │ Startup      │
   │ HTTP GET /   │      │ HTTP GET /   │      │ (optional)   │
   │              │      │              │      │              │
   │ Period: 30s  │      │ Period: 10s  │      │              │
   │ Failure: 3   │      │ Failure: 3   │      │              │
   └──────────────┘      └──────────────┘      └──────────────┘
          │                       │
          ▼                       ▼
   ┌──────────────┐      ┌──────────────┐
   │ On Failure:  │      │ On Failure:  │
   │ Restart Pod  │      │ Remove from  │
   │              │      │ Service      │
   └──────────────┘      └──────────────┘
```

### 9.2 Probe Endpoints

| Service | Liveness Path | Readiness Path | Port |
|---------|---------------|----------------|------|
| Frontend | `/` | `/` | 3000 |
| Backend | `/health` | `/health` | 8000 |
