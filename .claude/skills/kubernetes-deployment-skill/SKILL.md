---
name: kubernetes-deployment-skill
description: |
  Specify Kubernetes deployment strategies for local clusters using Helm charts.
  Use when planning Minikube deployments, defining install/upgrade/rollback
  procedures, or specifying deployment verification criteria. Supports stateless
  backend applications with external databases. Produces specification artifacts
  only - not kubectl or Helm commands.
---

# Kubernetes Deployment Skill (Phase IV)

Specify deployment strategies for applications on local Kubernetes clusters (Minikube) using Helm charts without generating implementation commands.

## Purpose

Define deployment specifications that guide Helm-based installation, upgrade, and rollback operations on Minikube clusters. Produce design documents that ensure consistent, repeatable deployments while preserving application architecture guarantees.

**Goals:**
- Specify install, upgrade, and rollback procedures for Helm releases
- Define pre-deployment verification requirements
- Establish post-deployment validation criteria
- Maintain stateless backend guarantees throughout deployment lifecycle
- Ensure specifications work within Minikube resource constraints

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Helm chart reference | Yes | Chart location (local path or repository) |
| Release name | Yes | Helm release identifier |
| Namespace | Yes | Target Kubernetes namespace |
| Values overrides | Yes | Environment-specific configuration values |
| Resource constraints | No | CPU/memory limits for Minikube environment |
| Replica counts | No | Desired pod replicas per deployment |
| Image references | No | Container image tags (must match existing images) |
| Ingress configuration | No | Local access configuration (NodePort, Ingress) |
| Health check endpoints | No | Paths for deployment readiness verification |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Pre-deployment checklist | Markdown | Cluster state verification requirements |
| Installation specification | Markdown | First-time deployment parameters and sequence |
| Upgrade specification | Markdown | Version transition requirements and strategy |
| Rollback specification | Markdown | Failure recovery procedures and triggers |
| Validation criteria | Markdown | Post-deployment health verification steps |
| Resource budget | Markdown table | Expected resource consumption per service |

## Constraints

1. **Specification only** - Produce design documents, not executable commands
2. **No command generation** - Describe procedures in prose, not kubectl/helm syntax
3. **Images immutable** - Application container images remain unchanged
4. **Minikube target** - Specifications assume local single-node cluster
5. **Helm-based** - All deployments use Helm chart mechanism
6. **Stateless backend** - No local persistent state in application pods
7. **External database** - Database connections remain outside cluster

## Invariants

1. **Images unchanged** - Deployment never modifies container image contents
2. **Stateless pods** - Backend pods contain no persistent local state
3. **External state** - All persistent data resides in external database
4. **Namespace isolation** - Deployments scoped to designated namespace
5. **Resource bounded** - Deployments respect Minikube resource limits
6. **Rollback capable** - Every deployment supports reversion to previous state
7. **Health observable** - All services expose verifiable health endpoints
8. **Configuration external** - Runtime config via ConfigMaps/Secrets, not baked in

## Prohibited Actions

| Action | Reason |
|--------|--------|
| Generate kubectl commands | Skill produces specifications only |
| Generate Helm commands | Describe procedures, not implementation |
| Modify container images | Images are immutable deployment artifacts |
| Create persistent volumes for app state | Backend must remain stateless |
| Deploy database to cluster | External database requirement |
| Exceed Minikube resources | Local cluster has strict limits |
| Hardcode secrets in specs | Security violation |
| Skip health verification | Deployments must be validated |

## Deployment Lifecycle Specifications

### Pre-Deployment Verification

Specify checks before any deployment:
- Cluster accessibility and health
- Namespace existence or creation requirements
- Required secrets and ConfigMaps present
- Sufficient cluster resources available
- Previous release state (for upgrades)

### Installation Specification

For first-time deployments, define:
- Namespace setup requirements
- Secret and ConfigMap prerequisites
- Helm values for local environment
- Service exposure strategy (NodePort/Ingress)
- Expected resource allocation
- Post-install verification steps

### Upgrade Specification

For version transitions, define:
- Pre-upgrade backup requirements
- Rolling update strategy parameters
- Maximum unavailability tolerance
- Canary or blue-green considerations
- Version compatibility checks
- Rollback trigger conditions

### Rollback Specification

For failure recovery, define:
- Automatic rollback triggers (health check failures)
- Manual rollback decision criteria
- Rollback target selection (previous vs specific revision)
- Post-rollback verification requirements
- Incident documentation needs

### Post-Deployment Validation

Specify verification criteria:
- Pod readiness status
- Service endpoint accessibility
- Health check responses
- Log inspection patterns
- Integration test triggers

## Minikube-Specific Considerations

### Resource Budgeting

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| Frontend | Specify | Specify | Specify | Specify |
| Backend | Specify | Specify | Specify | Specify |

Total must fit within Minikube allocation (typically 2-4 CPU, 4-8GB RAM).

### Access Patterns

Specify local access strategy:
- **NodePort**: Direct port exposure on Minikube IP
- **Ingress**: Host-based routing with ingress controller
- **Port-forward**: Development-time direct access

### External Service Connectivity

Define how cluster reaches external services:
- Database connection string injection
- External API endpoint configuration
- Secret management for credentials

## Usage Workflow

1. Verify Helm chart availability and version
2. Document namespace and release naming
3. Specify values overrides for local environment
4. Define resource budget within Minikube limits
5. Document installation procedure specification
6. Define upgrade strategy and rollback triggers
7. Specify post-deployment validation criteria
8. Document access configuration for local testing
