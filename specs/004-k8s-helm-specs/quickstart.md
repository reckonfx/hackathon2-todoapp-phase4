# Quickstart: Deploying Todo AI Chatbot to Minikube

**Feature**: 004-k8s-helm-specs
**Date**: 2026-02-02
**Purpose**: Step-by-step deployment guide for local Kubernetes cluster.

## Prerequisites

### Required Software

| Software | Version | Verification Command |
|----------|---------|---------------------|
| Minikube | Latest | `minikube version` |
| kubectl | 1.28+ | `kubectl version --client` |
| Helm | 3.x | `helm version` |
| Docker | Latest | `docker --version` |

### Minimum Resources

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| Memory | 4GB | 8GB |
| Disk | 20GB | 40GB |

## Quick Deploy (Development)

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Create namespace
kubectl create namespace todo-dev

# 3. Create secrets (replace with actual values)
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@host:5432/db' \
  --from-literal=SECRET_KEY='your-secret-key-minimum-32-chars!' \
  --from-literal=OPENAI_API_KEY='sk-your-openai-api-key' \
  --from-literal=AUTH_SECRET='your-auth-secret-minimum-32-chars' \
  -n todo-dev

# 4. Load container images (if using local images)
minikube image load todo-frontend:dev
minikube image load todo-backend:dev

# 5. Deploy backend
helm install todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev

# 6. Deploy frontend
helm install todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev

# 7. Access application
minikube service todo-frontend-dev -n todo-dev
```

## Detailed Steps

### Step 1: Start Minikube

```bash
# Start with recommended resources
minikube start --cpus=4 --memory=8192

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

**Expected Output**:
```
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

### Step 2: Create Namespaces

```bash
# Create all namespaces
kubectl create namespace todo-dev
kubectl create namespace todo-staging
kubectl create namespace todo-prod

# Verify
kubectl get namespaces | grep todo
```

**Expected Output**:
```
todo-dev       Active   10s
todo-prod      Active   8s
todo-staging   Active   9s
```

### Step 3: Create Secrets

**Development Secrets**:
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:password@neon-host.neon.tech:5432/todo_dev' \
  --from-literal=SECRET_KEY='development-jwt-secret-key-32ch!' \
  --from-literal=OPENAI_API_KEY='sk-your-openai-api-key-here' \
  --from-literal=AUTH_SECRET='development-auth-secret-32chars!' \
  -n todo-dev
```

**Verify Secret**:
```bash
kubectl get secret todo-backend-secrets -n todo-dev
kubectl describe secret todo-backend-secrets -n todo-dev
```

**Expected Output**:
```
Name:         todo-backend-secrets
Namespace:    todo-dev
Type:         Opaque

Data
====
AUTH_SECRET:     32 bytes
DATABASE_URL:    58 bytes
OPENAI_API_KEY:  51 bytes
SECRET_KEY:      34 bytes
```

### Step 4: Load Container Images

**Option A: Load pre-built images**:
```bash
minikube image load todo-frontend:dev
minikube image load todo-backend:dev

# Verify images
minikube image ls | grep todo
```

**Option B: Build in Minikube's Docker**:
```bash
eval $(minikube docker-env)
docker build -t todo-frontend:dev ./frontend
docker build -t todo-backend:dev ./backend
```

### Step 5: Deploy Backend

```bash
# Install backend chart
helm install todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev

# Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/instance=todo-backend-dev \
  -n todo-dev \
  --timeout=120s

# Verify deployment
kubectl get pods -n todo-dev
kubectl get svc -n todo-dev
```

**Expected Output**:
```
NAME                               READY   STATUS    RESTARTS   AGE
todo-backend-dev-xxxxxxxxx-xxxxx   1/1     Running   0          30s

NAME               TYPE        CLUSTER-IP       PORT(S)    AGE
todo-backend-dev   ClusterIP   10.96.xxx.xxx    8000/TCP   30s
```

### Step 6: Deploy Frontend

```bash
# Install frontend chart
helm install todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev

# Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/instance=todo-frontend-dev \
  -n todo-dev \
  --timeout=120s

# Verify deployment
kubectl get pods -n todo-dev
kubectl get svc -n todo-dev
```

**Expected Output**:
```
NAME                                READY   STATUS    RESTARTS   AGE
todo-backend-dev-xxxxxxxxx-xxxxx    1/1     Running   0          2m
todo-frontend-dev-xxxxxxxxx-xxxxx   1/1     Running   0          30s

NAME                TYPE        CLUSTER-IP       PORT(S)          AGE
todo-backend-dev    ClusterIP   10.96.xxx.xxx    8000/TCP         2m
todo-frontend-dev   NodePort    10.96.xxx.xxx    3000:3xxxx/TCP   30s
```

### Step 7: Access Application

**Method 1: Minikube Service (Recommended)**:
```bash
minikube service todo-frontend-dev -n todo-dev
```
This opens browser automatically.

**Method 2: Port Forward**:
```bash
# Frontend
kubectl port-forward svc/todo-frontend-dev 3000:3000 -n todo-dev &

# Backend (for API testing)
kubectl port-forward svc/todo-backend-dev 8000:8000 -n todo-dev &

# Access
echo "Frontend: http://localhost:3000"
echo "Backend Health: http://localhost:8000/health"
```

**Method 3: NodePort**:
```bash
export NODE_PORT=$(kubectl get svc todo-frontend-dev -n todo-dev -o jsonpath='{.spec.ports[0].nodePort}')
export NODE_IP=$(minikube ip)
echo "http://${NODE_IP}:${NODE_PORT}"
```

## Verification Checklist

### Pod Health

```bash
# All pods running
kubectl get pods -n todo-dev

# No crash loops
kubectl get pods -n todo-dev -o jsonpath='{.items[*].status.containerStatuses[*].restartCount}'

# Logs clean
kubectl logs -l app.kubernetes.io/instance=todo-frontend-dev -n todo-dev --tail=20
kubectl logs -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev --tail=20
```

### Health Endpoints

```bash
# Backend health (via port-forward)
curl http://localhost:8000/health

# Expected: {"status": "healthy"}
```

### Service Connectivity

```bash
# Test from within cluster
kubectl run test-curl --rm -it --image=curlimages/curl -- \
  curl http://todo-backend-dev.todo-dev.svc.cluster.local:8000/health
```

### Database Connectivity

```bash
# Check backend logs for DB connection
kubectl logs -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev | grep -i database
```

## Common Operations

### View Logs

```bash
# Frontend logs
kubectl logs -l app.kubernetes.io/instance=todo-frontend-dev -n todo-dev -f

# Backend logs
kubectl logs -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev -f
```

### Restart Pods

```bash
# Restart deployment (rolling restart)
kubectl rollout restart deployment todo-backend-dev -n todo-dev
kubectl rollout restart deployment todo-frontend-dev -n todo-dev
```

### Update Configuration

```bash
# Upgrade with new values
helm upgrade todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  -n todo-dev

helm upgrade todo-frontend-dev ./helm/todo-frontend \
  -f ./helm/todo-frontend/values/dev.yaml \
  -n todo-dev
```

### Scale Replicas

```bash
# Scale backend to 2 replicas
kubectl scale deployment todo-backend-dev --replicas=2 -n todo-dev

# Or via Helm upgrade
helm upgrade todo-backend-dev ./helm/todo-backend \
  -f ./helm/todo-backend/values/dev.yaml \
  --set replicaCount=2 \
  -n todo-dev
```

### Update Secrets

```bash
# Delete and recreate secret
kubectl delete secret todo-backend-secrets -n todo-dev
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL='new-url' \
  --from-literal=SECRET_KEY='new-key' \
  --from-literal=OPENAI_API_KEY='new-api-key' \
  --from-literal=AUTH_SECRET='new-auth-secret' \
  -n todo-dev

# Restart pods to pick up new secret
kubectl rollout restart deployment todo-backend-dev -n todo-dev
```

## Cleanup

### Uninstall Charts

```bash
# Remove releases
helm uninstall todo-frontend-dev -n todo-dev
helm uninstall todo-backend-dev -n todo-dev
```

### Delete Secrets

```bash
kubectl delete secret todo-backend-secrets -n todo-dev
```

### Delete Namespace

```bash
kubectl delete namespace todo-dev
```

### Stop Minikube

```bash
minikube stop

# Or delete entirely
minikube delete
```

## Troubleshooting

### Pod Not Starting

```bash
# Describe pod for events
kubectl describe pod -l app.kubernetes.io/instance=todo-backend-dev -n todo-dev

# Common issues:
# - ImagePullBackOff: Image not loaded/available
# - CreateContainerConfigError: Secret missing
# - CrashLoopBackOff: Application error (check logs)
```

### Secret Not Found

```bash
# Verify secret exists
kubectl get secret todo-backend-secrets -n todo-dev

# If missing, create it before installing chart
```

### Database Connection Failed

```bash
# Verify external network access
kubectl run test-network --rm -it --image=busybox -- wget -qO- https://neon.tech

# Check DATABASE_URL in secret
kubectl get secret todo-backend-secrets -n todo-dev -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

### Health Check Failures

```bash
# Check probe configuration
kubectl describe deployment todo-backend-dev -n todo-dev | grep -A 10 "Liveness\|Readiness"

# Test health endpoint manually
kubectl port-forward svc/todo-backend-dev 8000:8000 -n todo-dev &
curl -v http://localhost:8000/health
```

### Resource Limits Hit

```bash
# Check pod resource usage
kubectl top pods -n todo-dev

# Check for OOMKilled
kubectl get pods -n todo-dev -o jsonpath='{.items[*].status.containerStatuses[*].lastState}'
```

## Environment Matrix

| Environment | Namespace | Frontend Service Type | Replicas |
|-------------|-----------|----------------------|----------|
| Development | `todo-dev` | NodePort | 1 |
| Staging | `todo-staging` | ClusterIP | 1 |
| Production | `todo-prod` | ClusterIP | 2 |

## Next Steps

1. **Deploy to Staging**: Repeat steps with `todo-staging` namespace and staging values
2. **Configure Ingress**: Add Ingress controller for production-like routing
3. **Set up Monitoring**: Deploy Prometheus/Grafana for observability
4. **Implement HPA**: Enable Horizontal Pod Autoscaler for auto-scaling
