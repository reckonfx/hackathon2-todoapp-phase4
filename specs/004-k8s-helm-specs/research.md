# Research: Helm and Kubernetes Deployment Best Practices

**Feature**: 004-k8s-helm-specs
**Date**: 2026-02-02
**Purpose**: Document Helm chart patterns, Kubernetes deployment strategies, and Minikube-specific considerations for Phase IV implementation.

## 1. Helm Chart Best Practices

### 1.1 Chart Structure

**Standard Layout** (per Helm documentation):
```
mychart/
├── Chart.yaml          # Required: Chart metadata
├── values.yaml         # Required: Default configuration values
├── charts/             # Optional: Chart dependencies (subcharts)
├── templates/          # Required: Template files
│   ├── NOTES.txt       # Optional: Post-install instructions
│   ├── _helpers.tpl    # Convention: Partial templates
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── .helmignore         # Optional: Files to ignore during packaging
```

**Key Findings**:
- `_helpers.tpl` should define reusable template helpers (labels, names, selectors)
- `NOTES.txt` is rendered after install/upgrade to show user instructions
- Templates use Go template syntax with Sprig functions

### 1.2 Naming Conventions

**Release Name Pattern** (per H-008):
```
{service}-{environment}
```
Examples: `todo-frontend-dev`, `todo-backend-prod`

**Resource Naming**:
```yaml
name: {{ include "mychart.fullname" . }}
```
Standard helper generates: `{release-name}-{chart-name}`

### 1.3 Label Standards

**Recommended Labels** (Kubernetes conventions):
```yaml
labels:
  app.kubernetes.io/name: {{ include "mychart.name" . }}
  app.kubernetes.io/instance: {{ .Release.Name }}
  app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
  app.kubernetes.io/managed-by: {{ .Release.Service }}
  helm.sh/chart: {{ include "mychart.chart" . }}
```

### 1.4 Values.yaml Best Practices

**Structure Pattern**:
```yaml
# Image configuration
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: IfNotPresent

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 250m
    memory: 512Mi

# Service configuration
service:
  type: ClusterIP
  port: 3000

# Probes
probes:
  liveness:
    path: /
    initialDelaySeconds: 10
  readiness:
    path: /
    initialDelaySeconds: 5
```

**Key Findings**:
- Nest related values under common keys
- Use sensible defaults for optional values
- Document all values with comments
- Never include secrets in values.yaml

### 1.5 Environment-Specific Overrides (per H-004)

**Pattern**: Separate files in `values/` directory

```
values/
├── dev.yaml       # Development: minimal resources, debug enabled
├── staging.yaml   # Staging: production-like, test data allowed
└── prod.yaml      # Production: full resources, strict security
```

**Usage**:
```bash
helm install todo-frontend ./todo-frontend -f ./todo-frontend/values/dev.yaml -n todo-dev
```

## 2. Kubernetes Deployment Patterns

### 2.1 Deployment Specification

**Minimum Viable Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

### 2.2 Health Probes (per K-006)

**Liveness Probe** - Determines if container should be restarted:
```yaml
livenessProbe:
  httpGet:
    path: {{ .Values.probes.liveness.path }}
    port: {{ .Values.service.port }}
  initialDelaySeconds: {{ .Values.probes.liveness.initialDelaySeconds }}
  periodSeconds: 30
  timeoutSeconds: 5
  failureThreshold: 3
```

**Readiness Probe** - Determines if container should receive traffic:
```yaml
readinessProbe:
  httpGet:
    path: {{ .Values.probes.readiness.path }}
    port: {{ .Values.service.port }}
  initialDelaySeconds: {{ .Values.probes.readiness.initialDelaySeconds }}
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

**Key Findings**:
- Frontend: Probe at `/` (Next.js serves index page)
- Backend: Probe at `/health` (FastAPI health endpoint)
- Readiness should have shorter period than liveness
- Initial delay should account for application startup time

### 2.3 Resource Management (per K-005)

**Resource Specification Pattern**:
```yaml
resources:
  requests:
    cpu: {{ .Values.resources.requests.cpu }}
    memory: {{ .Values.resources.requests.memory }}
  limits:
    cpu: {{ .Values.resources.limits.cpu }}
    memory: {{ .Values.resources.limits.memory }}
```

**Guidelines**:
- Requests: Guaranteed resources for scheduling
- Limits: Maximum resources before OOMKill/throttling
- Ratio: Limits typically 2-4x requests for burstable workloads

### 2.4 Rolling Update Strategy

**Default Strategy** (recommended for stateless services):
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%
      maxSurge: 25%
```

## 3. Service and Networking

### 3.1 Service Types for Minikube

**ClusterIP** (internal only):
- Default for backend services
- Accessible only within cluster
- Use for service-to-service communication

**NodePort** (external access):
- Exposes service on node's IP at static port
- Range: 30000-32767
- Use with `minikube service` command

**LoadBalancer** (with Minikube tunnel):
- Requires `minikube tunnel` running
- Assigns external IP
- Closer to production behavior

### 3.2 DNS Naming (per K-008)

**Kubernetes DNS Pattern**:
```
{service}.{namespace}.svc.cluster.local
```

**Examples**:
- `todo-backend.todo-dev.svc.cluster.local`
- `todo-frontend.todo-prod.svc.cluster.local`

**Short Names** (within same namespace):
- `todo-backend` (resolves via search domain)

### 3.3 Frontend-to-Backend Communication

**Configuration Pattern**:
```yaml
# Frontend values.yaml
env:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
```

**Key Finding**: Use service short name for same-namespace communication.

## 4. Configuration Management

### 4.1 ConfigMap Pattern

**Template**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}-config
data:
  {{- range $key, $value := .Values.env }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
```

**Usage in Deployment**:
```yaml
envFrom:
  - configMapRef:
      name: {{ include "mychart.fullname" . }}-config
```

### 4.2 Secret Reference Pattern (per C-007)

**Key Finding**: Secrets should NOT be in Helm charts. Reference pre-created secrets:

**Template**:
```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: {{ .Values.secrets.existingSecret }}
        key: DATABASE_URL
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: {{ .Values.secrets.existingSecret }}
        key: OPENAI_API_KEY
```

**Secret Pre-creation** (manual step):
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://...' \
  --from-literal=SECRET_KEY='...' \
  --from-literal=OPENAI_API_KEY='...' \
  --from-literal=AUTH_SECRET='...' \
  -n todo-dev
```

## 5. Minikube-Specific Considerations

### 5.1 Image Loading

**Option 1: Local Registry**
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

**Option 2: Docker Environment**
```bash
eval $(minikube docker-env)
docker build -t todo-frontend:latest .
```

**Key Finding**: Use `imagePullPolicy: Never` or `IfNotPresent` with locally loaded images.

### 5.2 Resource Constraints

**Recommended Minikube Configuration**:
```bash
minikube start --cpus=4 --memory=8192
```

**Minimum for Phase IV**:
- CPUs: 2
- Memory: 4GB
- Disk: 20GB

### 5.3 External Database Connectivity

**Challenge**: Connecting to external Neon PostgreSQL from Minikube.

**Solution**: Network is available by default. Pods can reach external internet.

**Verification**:
```bash
kubectl run test --rm -it --image=busybox -- wget -qO- https://neon.tech
```

### 5.4 Accessing Services

**NodePort Access**:
```bash
minikube service todo-frontend -n todo-dev
```

**Tunnel for LoadBalancer**:
```bash
minikube tunnel
```

**Port Forward** (development):
```bash
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-dev
```

## 6. Namespace Strategy (per K-004)

### 6.1 Namespace Creation

**Approach**: Namespaces created before Helm install.

```bash
kubectl create namespace todo-dev
kubectl create namespace todo-staging
kubectl create namespace todo-prod
```

### 6.2 Resource Isolation

**Optional: Resource Quotas**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: todo-quota
  namespace: todo-dev
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 2Gi
    limits.cpu: "4"
    limits.memory: 4Gi
```

**Key Finding**: Resource quotas are recommended but not required for Minikube.

## 7. NOTES.txt Best Practices (per H-006)

**Template Pattern**:
```
Thank you for installing {{ .Chart.Name }}!

Your release is named: {{ .Release.Name }}

To get the application URL:
{{- if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "mychart.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "ClusterIP" .Values.service.type }}
  kubectl port-forward svc/{{ include "mychart.fullname" . }} {{ .Values.service.port }}:{{ .Values.service.port }} -n {{ .Release.Namespace }}
  echo http://127.0.0.1:{{ .Values.service.port }}
{{- end }}
```

## 8. Validation Commands

### 8.1 Chart Validation

```bash
# Lint chart
helm lint ./todo-frontend

# Template rendering (dry-run)
helm template todo-frontend ./todo-frontend -f ./todo-frontend/values/dev.yaml

# Install dry-run
helm install todo-frontend ./todo-frontend --dry-run --debug -n todo-dev
```

### 8.2 Deployment Verification

```bash
# Check pod status
kubectl get pods -n todo-dev

# Check pod logs
kubectl logs -l app.kubernetes.io/name=todo-frontend -n todo-dev

# Describe deployment
kubectl describe deployment todo-frontend -n todo-dev
```

## References

- Helm Best Practices: https://helm.sh/docs/chart_best_practices/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes Probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/
- Minikube Documentation: https://minikube.sigs.k8s.io/docs/
