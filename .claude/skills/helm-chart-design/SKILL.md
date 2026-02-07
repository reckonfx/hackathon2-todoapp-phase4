---
name: helm-chart-design
description: |
  Design Helm charts for deploying containerized applications to Kubernetes.
  Use when planning Kubernetes deployment strategy for frontend/backend services,
  defining chart structure, specifying values.yaml configuration, or creating
  environment-agnostic deployment specifications. This skill produces design
  artifacts only - not actual Helm charts or YAML files.
---

# Helm Chart Design Skill (Phase IV)

Design Helm chart specifications for deploying existing containerized applications to Kubernetes without generating implementation artifacts.

## Purpose

Define the structural design and configuration strategy for Helm charts that deploy containerized applications to Kubernetes clusters. Produce specifications that guide Helm chart implementation while remaining agnostic to application internals and deployment environment specifics.

**Goals:**
- Specify chart structure for multi-service deployments (frontend + backend)
- Define configuration externalization strategy via values.yaml
- Ensure portability across local (minikube, kind) and cloud (EKS, GKE, AKS) environments
- Maintain separation between chart design and application logic

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Container images | Yes | List of container image references (registry/image:tag) |
| Service topology | Yes | Frontend/backend service relationships and dependencies |
| Port mappings | Yes | Container ports and service exposure requirements |
| Environment variables | No | Required env vars per service (names only, not values) |
| Resource requirements | No | CPU/memory requests and limits per service |
| Persistence needs | No | Volume requirements for stateful services |
| Ingress requirements | No | External access patterns and routing rules |
| Health check endpoints | No | Liveness/readiness probe paths |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Chart structure specification | Markdown | Directory layout and file organization |
| values.yaml schema | Markdown table | Configuration parameters with types, defaults, descriptions |
| Template specifications | Markdown | Required K8s resources per service (Deployment, Service, ConfigMap, etc.) |
| Environment overlay strategy | Markdown | How to customize for local vs cloud environments |
| Dependency graph | Markdown | Inter-service dependencies and startup ordering |

## Constraints

1. **Specification only** - Produce design documents, not executable Helm charts
2. **No YAML generation** - Describe structure in prose/tables, not YAML syntax
3. **Application-agnostic** - No assumptions about application code, frameworks, or internals
4. **Image-based inputs** - Treat container images as black boxes with defined interfaces
5. **Environment-neutral** - Designs must work across local and cloud K8s clusters
6. **Standard Helm patterns** - Follow Helm 3 conventions and best practices
7. **No hardcoded values** - All environment-specific config flows through values.yaml

## Invariants

1. **Every service has a values.yaml entry** - No service configuration is hardcoded in templates
2. **All secrets are externalized** - Secret references only, never secret values
3. **Resource limits are parameterized** - CPU/memory configurable per environment
4. **Image tags are configurable** - Never hardcode image versions in templates
5. **Replica counts are variable** - Scaling configuration externalized to values
6. **Service discovery uses K8s DNS** - Internal service communication via cluster DNS
7. **Health probes are defined** - Every deployment specifies liveness/readiness checks
8. **Labels follow conventions** - Consistent labeling for app, version, component, environment

## Prohibited Actions

| Action | Reason |
|--------|--------|
| Generate Helm chart files | Skill produces specifications only |
| Write YAML content | Design describes structure, not syntax |
| Embed secrets or credentials | Security violation |
| Hardcode environment-specific values | Breaks portability |
| Assume application internals | Chart design is container-interface only |
| Specify cloud-provider-specific resources | Reduces portability |
| Define cluster-admin resources | Principle of least privilege |
| Create CRDs or operators | Out of scope for application charts |

## Design Principles

### Configuration Hierarchy

```
values.yaml (defaults)
  -> values-local.yaml (local overrides)
  -> values-cloud.yaml (cloud overrides)
    -> --set flags (runtime overrides)
```

### Chart Structure Pattern

Describe the standard directory layout:
- Chart.yaml metadata
- values.yaml defaults
- templates/ directory organization
- helpers (_helpers.tpl) usage
- NOTES.txt for post-install guidance

### Multi-Service Coordination

Specify how frontend and backend services interact:
- Service naming conventions
- Environment variable injection for service discovery
- Startup dependency ordering (initContainers or external tools)
- Shared configuration (ConfigMaps)

### Environment Portability

Define what varies between environments:
- Ingress configuration (local: NodePort/LoadBalancer, cloud: Ingress controller)
- Resource allocations (local: minimal, cloud: production-grade)
- Replica counts (local: 1, cloud: 3+)
- Storage classes (local: hostPath, cloud: provider-specific)

## Usage

1. Gather container image references and service topology
2. Identify port mappings and inter-service dependencies
3. Document environment variable requirements (names, not values)
4. Specify resource and persistence needs
5. Produce chart structure specification
6. Define values.yaml schema with all configurable parameters
7. Describe template specifications for each K8s resource
8. Document environment overlay strategy
