# Helm Chart Contract: todo-frontend

**Feature**: 004-k8s-helm-specs
**Date**: 2026-02-02
**Purpose**: Define the interface contract for the todo-frontend Helm chart.

## Chart Metadata

| Field | Value |
|-------|-------|
| **Name** | `todo-frontend` |
| **Type** | Application |
| **Version** | `1.0.0` (semantic versioning per H-005) |
| **AppVersion** | Matches container image tag |
| **Description** | Helm chart for Todo AI Chatbot frontend service |
| **Home** | N/A |
| **Maintainers** | Project team |

## values.yaml Contract

### Complete Schema

```yaml
# Replica configuration
replicaCount: 1

# Container image configuration
image:
  repository: "todo-frontend"      # REQUIRED: Image repository
  tag: "latest"                    # REQUIRED: Image tag
  pullPolicy: "IfNotPresent"       # Optional: Always, IfNotPresent, Never

# Service configuration
service:
  type: "ClusterIP"                # Optional: ClusterIP, NodePort, LoadBalancer
  port: 3000                       # Optional: Service port
  nodePort: null                   # Optional: Only used when type=NodePort

# Resource limits (per K-005)
resources:
  requests:
    cpu: "100m"                    # Optional: CPU request
    memory: "128Mi"                # Optional: Memory request
  limits:
    cpu: "250m"                    # Optional: CPU limit
    memory: "512Mi"                # Optional: Memory limit

# Environment variables (non-sensitive)
env:
  NODE_ENV: "production"           # Optional: Node environment
  NEXT_PUBLIC_API_URL: ""          # REQUIRED: Backend API URL

# Health probes (per K-006)
probes:
  liveness:
    enabled: true                  # Optional: Enable liveness probe
    path: "/"                      # Optional: Probe path
    port: 3000                     # Optional: Probe port
    initialDelaySeconds: 10        # Optional: Initial delay
    periodSeconds: 30              # Optional: Check period
    timeoutSeconds: 5              # Optional: Timeout
    failureThreshold: 3            # Optional: Failures before restart
  readiness:
    enabled: true                  # Optional: Enable readiness probe
    path: "/"                      # Optional: Probe path
    port: 3000                     # Optional: Probe port
    initialDelaySeconds: 5         # Optional: Initial delay
    periodSeconds: 10              # Optional: Check period
    timeoutSeconds: 5              # Optional: Timeout
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
| `env.NEXT_PUBLIC_API_URL` | string | Backend API URL | Valid URL format |

### Optional Values with Defaults

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `replicaCount` | integer | `1` | Number of pod replicas |
| `image.pullPolicy` | string | `IfNotPresent` | Image pull policy |
| `service.type` | string | `ClusterIP` | Kubernetes Service type |
| `service.port` | integer | `3000` | Service port |
| `resources.requests.cpu` | string | `100m` | CPU request |
| `resources.requests.memory` | string | `128Mi` | Memory request |
| `resources.limits.cpu` | string | `250m` | CPU limit |
| `resources.limits.memory` | string | `512Mi` | Memory limit |
| `env.NODE_ENV` | string | `production` | Node environment |

## Template Contracts

### deployment.yaml

**Input Values**:
- `replicaCount`
- `image.*`
- `resources.*`
- `env.*`
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
- `service.nodePort` (optional)

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
- `env.*` (all non-sensitive environment variables)

**Output Resource**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
  labels:
    # Standard Kubernetes labels
data:
  NODE_ENV: {{ .Values.env.NODE_ENV | quote }}
  NEXT_PUBLIC_API_URL: {{ .Values.env.NEXT_PUBLIC_API_URL | quote }}
```

### NOTES.txt

**Output** (displayed after helm install/upgrade):
```
Thank you for installing {{ .Chart.Name }}!

Release: {{ .Release.Name }}
Namespace: {{ .Release.Namespace }}

To access the frontend:
{{- if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get -n {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" svc {{ .Release.Name }})
  echo "http://$(minikube ip):$NODE_PORT"
{{- else if contains "ClusterIP" .Values.service.type }}
  kubectl port-forward svc/{{ .Release.Name }} {{ .Values.service.port }}:{{ .Values.service.port }} -n {{ .Release.Namespace }}
  echo "http://127.0.0.1:{{ .Values.service.port }}"
{{- end }}

To check pod status:
  kubectl get pods -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Release.Namespace }}
```

## Environment-Specific Overrides

### values/dev.yaml

```yaml
replicaCount: 1

image:
  tag: "dev"
  pullPolicy: "Never"  # Use locally loaded images

service:
  type: "NodePort"  # Enable external access for development

env:
  NODE_ENV: "development"
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"

resources:
  requests:
    cpu: "50m"
    memory: "64Mi"
  limits:
    cpu: "100m"
    memory: "256Mi"
```

### values/staging.yaml

```yaml
replicaCount: 1

image:
  tag: "staging"
  pullPolicy: "IfNotPresent"

service:
  type: "ClusterIP"

env:
  NODE_ENV: "staging"
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "250m"
    memory: "512Mi"
```

### values/prod.yaml

```yaml
replicaCount: 2

image:
  tag: "prod"
  pullPolicy: "IfNotPresent"

service:
  type: "ClusterIP"

env:
  NODE_ENV: "production"
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "250m"
    memory: "512Mi"
```

## Helm Commands

### Installation

```bash
# Development
helm install todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev

# Staging
helm install todo-frontend-staging ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/staging.yaml \
  -n todo-staging

# Production
helm install todo-frontend-prod ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/prod.yaml \
  -n todo-prod
```

### Upgrade

```bash
helm upgrade todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev
```

### Uninstall

```bash
helm uninstall todo-frontend-dev -n todo-dev
```

## Validation

### Pre-Installation

```bash
# Lint chart
helm lint ./helm/todo-frontend

# Template rendering
helm template todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev

# Dry run
helm install todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev \
  --dry-run --debug
```

### Post-Installation

```bash
# Check release status
helm status todo-frontend-dev -n todo-dev

# Verify pods
kubectl get pods -l app.kubernetes.io/instance=todo-frontend-dev -n todo-dev

# Check logs
kubectl logs -l app.kubernetes.io/instance=todo-frontend-dev -n todo-dev
```

## Compliance

| Rule | Status | Evidence |
|------|--------|----------|
| H-001 | Compliant | Helm is deployment mechanism |
| H-002 | Compliant | Dedicated chart for frontend |
| H-003 | Compliant | All values in values.yaml |
| H-004 | Compliant | Environment overrides in values/ |
| H-005 | Compliant | Semantic versioning |
| H-006 | Compliant | NOTES.txt included |
| H-007 | Compliant | No hardcoded env values |
| H-008 | Compliant | Release pattern: todo-frontend-{env} |
| K-005 | Compliant | Resource limits specified |
| K-006 | Compliant | Probes configured |
| K-008 | Compliant | Service uses DNS naming |
