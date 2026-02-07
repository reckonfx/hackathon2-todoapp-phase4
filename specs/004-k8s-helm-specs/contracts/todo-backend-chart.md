# Helm Chart Contract: todo-backend

**Feature**: 004-k8s-helm-specs
**Date**: 2026-02-02
**Purpose**: Define the interface contract for the todo-backend Helm chart.

## Chart Metadata

| Field | Value |
|-------|-------|
| **Name** | `todo-backend` |
| **Type** | Application |
| **Version** | `1.0.0` (semantic versioning per H-005) |
| **AppVersion** | Matches container image tag |
| **Description** | Helm chart for Todo AI Chatbot backend service (includes MCP) |
| **Home** | N/A |
| **Maintainers** | Project team |

## values.yaml Contract

### Complete Schema

```yaml
# Replica configuration
replicaCount: 1

# Container image configuration
image:
  repository: "todo-backend"       # REQUIRED: Image repository
  tag: "latest"                    # REQUIRED: Image tag
  pullPolicy: "IfNotPresent"       # Optional: Always, IfNotPresent, Never

# Service configuration
service:
  type: "ClusterIP"                # Optional: ClusterIP only (internal service)
  port: 8000                       # Optional: Service port

# Resource limits (per K-005)
resources:
  requests:
    cpu: "250m"                    # Optional: CPU request
    memory: "256Mi"                # Optional: Memory request
  limits:
    cpu: "500m"                    # Optional: CPU limit
    memory: "1Gi"                  # Optional: Memory limit

# Environment variables (non-sensitive) via ConfigMap
env:
  BACKEND_ENV: "production"        # Optional: Backend environment
  BACKEND_HOST: "0.0.0.0"          # Optional: Listen host
  BACKEND_PORT: "8000"             # Optional: Listen port
  CORS_ORIGINS: ""                 # REQUIRED: Allowed CORS origins
  POOL_SIZE: "5"                   # Optional: DB connection pool size
  MAX_OVERFLOW: "10"               # Optional: DB pool overflow
  POOL_TIMEOUT: "30"               # Optional: DB pool timeout (seconds)
  CHAT_MAX_MESSAGES: "100"         # Optional: Max messages per conversation

# Secret configuration (references pre-created secrets)
secrets:
  existingSecret: "todo-backend-secrets"  # REQUIRED: Name of pre-created secret
  keys:
    databaseUrl: "DATABASE_URL"           # Key name in secret
    secretKey: "SECRET_KEY"               # Key name in secret
    openaiApiKey: "OPENAI_API_KEY"        # Key name in secret
    authSecret: "AUTH_SECRET"             # Key name in secret

# Health probes (per K-006)
probes:
  liveness:
    enabled: true                  # Optional: Enable liveness probe
    path: "/health"                # Optional: Probe path
    port: 8000                     # Optional: Probe port
    initialDelaySeconds: 15        # Optional: Initial delay (backend needs more startup time)
    periodSeconds: 30              # Optional: Check period
    timeoutSeconds: 10             # Optional: Timeout
    failureThreshold: 3            # Optional: Failures before restart
  readiness:
    enabled: true                  # Optional: Enable readiness probe
    path: "/health"                # Optional: Probe path
    port: 8000                     # Optional: Probe port
    initialDelaySeconds: 10        # Optional: Initial delay
    periodSeconds: 10              # Optional: Check period
    timeoutSeconds: 10             # Optional: Timeout
    failureThreshold: 3            # Optional: Failures before unhealthy

# Pod configuration
podAnnotations: {}                 # Optional: Additional pod annotations
podLabels: {}                      # Optional: Additional pod labels

# Security context
securityContext: {}                # Optional: Pod security context

# Node selection
nodeSelector: {}                   # Optional: Node selector labels
tolerations: []                    # Optional: Node tolerations
affinity: {}                       # Optional: Pod affinity rules
```

### Required Values

| Key | Type | Description | Validation |
|-----|------|-------------|------------|
| `image.repository` | string | Container image repository | Non-empty |
| `image.tag` | string | Container image tag | Non-empty |
| `env.CORS_ORIGINS` | string | Allowed CORS origins | Non-empty, comma-separated URLs |
| `secrets.existingSecret` | string | Pre-created Kubernetes Secret name | Must exist in namespace |

### Optional Values with Defaults

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `replicaCount` | integer | `1` | Number of pod replicas |
| `image.pullPolicy` | string | `IfNotPresent` | Image pull policy |
| `service.type` | string | `ClusterIP` | Kubernetes Service type |
| `service.port` | integer | `8000` | Service port |
| `resources.requests.cpu` | string | `250m` | CPU request |
| `resources.requests.memory` | string | `256Mi` | Memory request |
| `resources.limits.cpu` | string | `500m` | CPU limit |
| `resources.limits.memory` | string | `1Gi` | Memory limit |
| `env.BACKEND_ENV` | string | `production` | Backend environment |
| `env.POOL_SIZE` | string | `5` | Database pool size |

## Template Contracts

### deployment.yaml

**Input Values**:
- `replicaCount`
- `image.*`
- `resources.*`
- `env.*`
- `secrets.*`
- `probes.*`
- `podAnnotations`, `podLabels`
- `securityContext`, `nodeSelector`, `tolerations`, `affinity`

**Output Resource**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
    # Standard Kubernetes labels
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      # Selector labels
  template:
    metadata:
      labels:
        # Pod labels
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          envFrom:
            - configMapRef:
                name: {{ .Release.Name }}-config
          env:
            # Secret references (per C-007 - not baked into image)
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ .Values.secrets.existingSecret }}
                  key: {{ .Values.secrets.keys.databaseUrl }}
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: {{ .Values.secrets.existingSecret }}
                  key: {{ .Values.secrets.keys.secretKey }}
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: {{ .Values.secrets.existingSecret }}
                  key: {{ .Values.secrets.keys.openaiApiKey }}
            - name: AUTH_SECRET
              valueFrom:
                secretKeyRef:
                  name: {{ .Values.secrets.existingSecret }}
                  key: {{ .Values.secrets.keys.authSecret }}
          resources:
            # Resource specifications
          livenessProbe:
            # Liveness probe configuration
          readinessProbe:
            # Readiness probe configuration
```

### service.yaml

**Input Values**:
- `service.type`
- `service.port`

**Output Resource**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
  labels:
    # Standard Kubernetes labels
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
      protocol: TCP
  selector:
    # Selector labels matching deployment
```

### configmap.yaml

**Input Values**:
- `env.*` (non-sensitive environment variables only)

**Output Resource**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
  labels:
    # Standard Kubernetes labels
data:
  BACKEND_ENV: {{ .Values.env.BACKEND_ENV | quote }}
  BACKEND_HOST: {{ .Values.env.BACKEND_HOST | quote }}
  BACKEND_PORT: {{ .Values.env.BACKEND_PORT | quote }}
  CORS_ORIGINS: {{ .Values.env.CORS_ORIGINS | quote }}
  POOL_SIZE: {{ .Values.env.POOL_SIZE | quote }}
  MAX_OVERFLOW: {{ .Values.env.MAX_OVERFLOW | quote }}
  POOL_TIMEOUT: {{ .Values.env.POOL_TIMEOUT | quote }}
  CHAT_MAX_MESSAGES: {{ .Values.env.CHAT_MAX_MESSAGES | quote }}
```

### secret.yaml

**Purpose**: Template for documenting required secret structure. Does NOT create secrets (per C-007).

**Output** (informational only):
```yaml
# This template documents the required secret structure.
# Secrets MUST be pre-created using kubectl before Helm install.
#
# Required secret: {{ .Values.secrets.existingSecret }}
# Required keys:
#   - {{ .Values.secrets.keys.databaseUrl }}: PostgreSQL connection string
#   - {{ .Values.secrets.keys.secretKey }}: JWT signing key
#   - {{ .Values.secrets.keys.openaiApiKey }}: OpenAI API key
#   - {{ .Values.secrets.keys.authSecret }}: Authentication secret
#
# Create with:
#   kubectl create secret generic {{ .Values.secrets.existingSecret }} \
#     --from-literal={{ .Values.secrets.keys.databaseUrl }}='postgresql://...' \
#     --from-literal={{ .Values.secrets.keys.secretKey }}='...' \
#     --from-literal={{ .Values.secrets.keys.openaiApiKey }}='sk-...' \
#     --from-literal={{ .Values.secrets.keys.authSecret }}='...' \
#     -n {{ .Release.Namespace }}
```

### NOTES.txt

**Output** (displayed after helm install/upgrade):
```
Thank you for installing {{ .Chart.Name }}!

Release: {{ .Release.Name }}
Namespace: {{ .Release.Namespace }}

IMPORTANT: This chart requires a pre-created Kubernetes Secret.
Secret name: {{ .Values.secrets.existingSecret }}

To create the required secret:
  kubectl create secret generic {{ .Values.secrets.existingSecret }} \
    --from-literal=DATABASE_URL='your-database-url' \
    --from-literal=SECRET_KEY='your-secret-key' \
    --from-literal=OPENAI_API_KEY='your-openai-key' \
    --from-literal=AUTH_SECRET='your-auth-secret' \
    -n {{ .Release.Namespace }}

To access the backend (for testing):
  kubectl port-forward svc/{{ .Release.Name }} {{ .Values.service.port }}:{{ .Values.service.port }} -n {{ .Release.Namespace }}
  echo "http://127.0.0.1:{{ .Values.service.port }}/health"

To check pod status:
  kubectl get pods -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Release.Namespace }}

To view logs:
  kubectl logs -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Release.Namespace }}

Service DNS (for frontend):
  http://{{ .Release.Name }}:{{ .Values.service.port }}
```

## Environment-Specific Overrides

### values/dev.yaml

```yaml
replicaCount: 1

image:
  tag: "dev"
  pullPolicy: "Never"  # Use locally loaded images

env:
  BACKEND_ENV: "development"
  CORS_ORIGINS: "http://localhost:3000,http://todo-frontend:3000"
  POOL_SIZE: "2"
  MAX_OVERFLOW: "5"

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "250m"
    memory: "512Mi"

secrets:
  existingSecret: "todo-backend-secrets"
```

### values/staging.yaml

```yaml
replicaCount: 1

image:
  tag: "staging"
  pullPolicy: "IfNotPresent"

env:
  BACKEND_ENV: "staging"
  CORS_ORIGINS: "http://todo-frontend:3000"
  POOL_SIZE: "5"
  MAX_OVERFLOW: "10"

resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "1Gi"

secrets:
  existingSecret: "todo-backend-secrets"
```

### values/prod.yaml

```yaml
replicaCount: 2

image:
  tag: "prod"
  pullPolicy: "IfNotPresent"

env:
  BACKEND_ENV: "production"
  CORS_ORIGINS: "http://todo-frontend:3000"
  POOL_SIZE: "10"
  MAX_OVERFLOW: "20"

resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "1Gi"

secrets:
  existingSecret: "todo-backend-secrets"
```

## Pre-Installation Requirements

### Secret Creation (REQUIRED before Helm install)

```bash
# Development namespace
kubectl create namespace todo-dev
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@neon-host:5432/db' \
  --from-literal=SECRET_KEY='dev-secret-key-minimum-32-chars!' \
  --from-literal=OPENAI_API_KEY='sk-dev-openai-key' \
  --from-literal=AUTH_SECRET='dev-auth-secret-minimum-32-chars' \
  -n todo-dev

# Staging namespace
kubectl create namespace todo-staging
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@neon-host:5432/db' \
  --from-literal=SECRET_KEY='staging-secret-key-min-32-chars!' \
  --from-literal=OPENAI_API_KEY='sk-staging-openai-key' \
  --from-literal=AUTH_SECRET='staging-auth-secret-min-32-chars' \
  -n todo-staging

# Production namespace
kubectl create namespace todo-prod
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@neon-host:5432/db' \
  --from-literal=SECRET_KEY='production-secret-key-32-chars!!' \
  --from-literal=OPENAI_API_KEY='sk-prod-openai-key' \
  --from-literal=AUTH_SECRET='production-auth-secret-32-chars' \
  -n todo-prod
```

## Helm Commands

### Installation

```bash
# Development (AFTER creating secrets)
helm install todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev

# Staging
helm install todo-backend-staging ./helm/todo-backend \
  -f ./helm/todo-backend/values/staging.yaml \
  -n todo-staging

# Production
helm install todo-backend-prod ./helm/todo-backend \
  -f ./helm/todo-backend/values/prod.yaml \
  -n todo-prod
```

### Upgrade

```bash
helm upgrade todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev
```

### Uninstall

```bash
helm uninstall todo-backend-dev -n todo-dev
# Note: Secrets are NOT deleted with uninstall
```

## Validation

### Pre-Installation

```bash
# Lint chart
helm lint ./helm/todo-backend

# Template rendering
helm template todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev

# Dry run (requires namespace and secrets to exist)
helm install todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev \
  --dry-run --debug
```

### Post-Installation

```bash
# Check release status
helm status todo-backend-dev -n todo-dev

# Verify pods
kubectl get pods -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev

# Check health endpoint
kubectl port-forward svc/todo-backend-dev 8000:8000 -n todo-dev &
curl http://localhost:8000/health

# Check logs
kubectl logs -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev
```

### Secret Verification

```bash
# Verify secret exists
kubectl get secret todo-backend-secrets -n todo-dev

# Verify secret keys (base64 encoded)
kubectl get secret todo-backend-secrets -n todo-dev -o jsonpath='{.data}'
```

## Compliance

| Rule | Status | Evidence |
|------|--------|----------|
| H-001 | Compliant | Helm is deployment mechanism |
| H-002 | Compliant | Dedicated chart for backend |
| H-003 | Compliant | All values in values.yaml |
| H-004 | Compliant | Environment overrides in values/ |
| H-005 | Compliant | Semantic versioning |
| H-006 | Compliant | NOTES.txt included |
| H-007 | Compliant | No hardcoded env values |
| H-008 | Compliant | Release pattern: todo-backend-{env} |
| K-005 | Compliant | Resource limits specified |
| K-006 | Compliant | Probes configured |
| K-007 | Compliant | External PostgreSQL via DATABASE_URL |
| K-008 | Compliant | Service uses DNS naming |
| C-007 | Compliant | Secrets via secretKeyRef, not baked |

## Security Considerations

1. **Secrets are NOT in version control** - Pre-created manually
2. **Secrets are NOT in Helm values** - Referenced via secretKeyRef
3. **Environment-specific secrets** - Each namespace has own secret
4. **Secret rotation** - Update secret, then restart pods
5. **Audit trail** - Kubernetes audit logs capture secret access
