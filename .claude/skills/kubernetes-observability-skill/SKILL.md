---
name: kubernetes-observability-skill
description: |
  Specify observability and diagnostic strategies for Kubernetes-deployed systems.
  Use when defining inspection workflows for pods, services, and deployments,
  specifying log analysis patterns, or documenting diagnostic decision trees.
  Read-only observation only - no cluster modifications or fix proposals.
  Produces specification artifacts only - not kubectl commands.
---

# Kubernetes Observability and Debugging Skill (Phase IV)

Specify diagnostic and observability strategies for Kubernetes deployments without generating commands or proposing fixes.

## Purpose

Define observability specifications that guide systematic diagnosis of issues in Kubernetes-deployed applications. Produce documentation that structures inspection workflows, log analysis patterns, and diagnostic decision trees while maintaining strictly read-only cluster interaction.

**Goals:**
- Specify inspection workflows for pods, services, and deployments
- Define log analysis patterns for issue identification
- Document diagnostic decision trees for common failure modes
- Maintain read-only observation principles
- Provide structured explanation of observed issues

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Symptom description | Yes | Observable problem (e.g., "pods not starting", "service unreachable") |
| Namespace | Yes | Target Kubernetes namespace |
| Resource type | Yes | Pod, Service, Deployment, or combination |
| Resource names | No | Specific resource identifiers |
| Time window | No | When issue started or was observed |
| Error messages | No | Any error text already captured |
| Expected behavior | No | What should be happening |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Inspection workflow | Markdown | Ordered steps for gathering diagnostic data |
| Resource checklist | Markdown table | What to examine for each resource type |
| Log analysis guide | Markdown | Patterns to search for in logs |
| Diagnostic decision tree | Markdown | Branching logic based on observations |
| Issue explanation | Markdown | Structured description of diagnosed problem |
| Observation summary | Markdown | Findings without recommendations |

## Constraints

1. **Specification only** - Produce diagnostic workflows, not executable commands
2. **No command generation** - Describe what to observe, not how to run kubectl
3. **Read-only** - All specifications assume non-mutating operations
4. **No fix proposals** - Explain issues, do not suggest remediation
5. **Cluster state unchanged** - Nothing in specification modifies resources
6. **Application unchanged** - No recommendations that alter application behavior
7. **Observation focus** - Output describes what is seen, not what to do about it

## Invariants

1. **Zero cluster mutations** - No specification causes cluster state change
2. **Application behavior preserved** - Observation never affects running workloads
3. **Read-only access** - All inspection assumes viewer permissions only
4. **Explanation not prescription** - Outputs describe, never recommend
5. **Reproducible observations** - Same inputs yield same diagnostic workflow
6. **Structured output** - All findings follow consistent documentation format
7. **Time-bounded** - Observations scoped to specified time windows
8. **Namespace-scoped** - Inspection limited to designated namespace

## Prohibited Actions

| Action | Reason |
|--------|--------|
| Generate kubectl commands | Skill produces specifications only |
| Generate diagnostic scripts | Describe workflows, not implementation |
| Propose fixes or remediation | Observation and explanation only |
| Suggest configuration changes | No modification recommendations |
| Recommend scaling actions | Read-only observation principle |
| Advise restart or delete | No cluster state changes |
| Modify resource definitions | Strictly read-only |
| Change application settings | Application behavior unchanged |

## Inspection Specifications

### Pod Inspection Workflow

Specify what to observe for pod issues:
- Pod phase and conditions
- Container statuses and restart counts
- Resource requests vs actual usage
- Event history for the pod
- Init container completion status

### Service Inspection Workflow

Specify what to observe for service issues:
- Endpoint registration status
- Selector label matching
- Port configuration alignment
- Backend pod readiness
- Service type and exposure

### Deployment Inspection Workflow

Specify what to observe for deployment issues:
- Replica set status
- Rolling update progress
- Pod template changes
- Deployment conditions
- Revision history

### Log Analysis Patterns

Define log inspection specifications:

| Pattern Category | What to Look For |
|------------------|------------------|
| Startup failures | Init errors, dependency timeouts |
| Runtime errors | Exceptions, stack traces, panics |
| Connection issues | Refused, timeout, DNS resolution |
| Resource exhaustion | OOM, CPU throttling, disk full |
| Authentication | Token expired, permission denied |

### Diagnostic Decision Trees

Structure diagnostic logic as decision points:

**Pod Not Starting:**
- Phase = Pending → Check scheduling, resources, node capacity
- Phase = ContainerCreating → Check image pull, secrets, volumes
- Phase = CrashLoopBackOff → Check logs, startup commands, probes

**Service Unreachable:**
- No endpoints → Check selector labels, pod readiness
- Endpoints exist → Check port mappings, network policies
- Intermittent → Check pod health, resource pressure

**Deployment Stuck:**
- Progressing = False → Check replica set events
- Available = False → Check pod failures
- Revision unchanged → Check update strategy

## Observation Categories

### Health Observations

| Aspect | What to Document |
|--------|------------------|
| Liveness | Probe results, failure counts |
| Readiness | Probe results, traffic routing |
| Startup | Initial probe tolerance |

### Resource Observations

| Aspect | What to Document |
|--------|------------------|
| CPU | Request, limit, actual usage |
| Memory | Request, limit, actual usage |
| Storage | PVC status, capacity, usage |

### Network Observations

| Aspect | What to Document |
|--------|------------------|
| DNS | Resolution success, latency |
| Connectivity | Inter-pod, external access |
| Policies | Applied rules, blocked traffic |

## Usage Workflow

1. Document the observed symptom clearly
2. Identify affected namespace and resources
3. Specify inspection workflow for relevant resource types
4. Define log analysis patterns for the symptom category
5. Structure diagnostic decision tree based on observations
6. Produce observation summary documenting findings
7. Explain the issue without proposing fixes
