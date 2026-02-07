---
name: kubernetes-validation-skill
description: |
  Specify validation criteria for Kubernetes deployments against functional and
  architectural requirements. Use when defining acceptance tests for chatbot
  functionality, persistence validation across pod restarts, stateless backend
  verification, or Helm release validation. Produces specification artifacts
  only - not test scripts or commands.
---

# Kubernetes Deployment Validation Skill (Phase IV)

Specify validation criteria and acceptance requirements for Kubernetes-deployed applications without generating test scripts or commands.

## Purpose

Define validation specifications that verify Kubernetes deployments meet functional and architectural requirements. Produce documentation that structures acceptance criteria, validation workflows, and pass/fail conditions for deployed applications.

**Goals:**
- Specify functional validation criteria for chatbot UI
- Define persistence validation across pod lifecycle events
- Document stateless backend verification requirements
- Establish Helm release validation criteria
- Provide clear pass/fail acceptance conditions

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Deployment reference | Yes | Helm release name and namespace |
| Functional requirements | Yes | Expected application behaviors |
| Architecture constraints | Yes | Stateless, persistence, scaling requirements |
| Access endpoints | Yes | UI URL, API endpoints |
| Database reference | Yes | External database connection info |
| Previous state | No | Data created before validation |
| Pod count | No | Expected replica count |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Validation checklist | Markdown | Complete list of validation criteria |
| Functional test cases | Markdown table | UI/API behavior validations |
| Persistence test cases | Markdown table | Data survival criteria |
| Architecture validation | Markdown table | Stateless/Helm compliance checks |
| Acceptance matrix | Markdown | Pass/fail criteria summary |
| Validation report template | Markdown | Structure for documenting results |

## Constraints

1. **Specification only** - Produce validation criteria, not executable tests
2. **No script generation** - Describe what to validate, not how to automate
3. **No command generation** - Criteria in prose, not kubectl/helm syntax
4. **Manual validation assumed** - Specifications support human execution
5. **Non-destructive** - Validation must not corrupt production data
6. **Repeatable** - Same criteria applicable across environments

## Invariants

1. **Functional completeness** - All user-facing features have validation criteria
2. **Architecture compliance** - Stateless behavior explicitly verified
3. **Persistence guarantee** - Data survival across restarts confirmed
4. **Helm management** - Deployment managed exclusively via Helm
5. **External database** - No in-cluster data persistence for application state
6. **Reproducible results** - Validation yields consistent outcomes
7. **Clear pass/fail** - Every criterion has unambiguous success condition
8. **Isolation** - Validation does not affect other deployments

## Prohibited Actions

| Action | Reason |
|--------|--------|
| Generate test scripts | Skill produces specifications only |
| Generate kubectl commands | Describe criteria, not implementation |
| Generate Helm commands | Validation criteria, not execution |
| Automate validation | Manual execution assumed |
| Modify deployment state | Non-destructive validation |
| Create test data destructively | Preserve existing data integrity |
| Skip architectural checks | All constraints must be validated |

## Validation Categories

### Functional Validation: Chatbot UI

Specify criteria for chatbot functionality:

| Test Case | Validation Criteria | Pass Condition |
|-----------|---------------------|----------------|
| UI Accessibility | Frontend loads at expected URL | HTTP 200, UI renders |
| Authentication | Login/register flows work | User can authenticate |
| Chat Input | Message can be submitted | Input accepted, sent to backend |
| AI Response | Assistant responds to messages | Response received within timeout |
| Task Creation | "Add task" via chat creates task | Task appears in list |
| Task Listing | "Show tasks" displays tasks | Existing tasks shown |
| Task Completion | "Complete task" marks done | Task status updated |
| Conversation History | Previous messages visible | Chat history persists |

### Persistence Validation: Pod Restart Survival

Specify criteria for data persistence across pod lifecycle:

| Test Case | Validation Criteria | Pass Condition |
|-----------|---------------------|----------------|
| Pre-restart baseline | Create identifiable test data | Data exists, recorded |
| Backend pod restart | Backend pod terminated and recreated | New pod running |
| Post-restart data check | Query for pre-restart data | All data intact |
| Frontend pod restart | Frontend pod terminated and recreated | New pod running |
| Session continuity | User session survives restart | Re-auth not required (or graceful) |
| Conversation persistence | Chat history after restart | Previous messages visible |
| Task persistence | Tasks survive backend restart | All tasks intact |

### Architecture Validation: Stateless Backend

Specify criteria for stateless backend compliance:

| Test Case | Validation Criteria | Pass Condition |
|-----------|---------------------|----------------|
| No local storage | Backend pods use no PVCs | No volume claims |
| External database | All state in external PostgreSQL | DB queries confirm data |
| Pod interchangeability | Request works on any pod | Consistent behavior |
| Horizontal scaling | Adding replicas doesn't break state | New pods serve correctly |
| Session externalization | No in-memory session state | Works across pods |
| Config externalization | All config via ConfigMap/Secret | No hardcoded values |

### Helm Validation: Managed Deployment

Specify criteria for Helm-managed deployment:

| Test Case | Validation Criteria | Pass Condition |
|-----------|---------------------|----------------|
| Release exists | Helm release registered | `helm list` shows release |
| Correct namespace | Resources in expected namespace | All resources namespaced |
| Values applied | Custom values reflected | Config matches values.yaml |
| Resource ownership | Resources have Helm labels | `app.kubernetes.io/managed-by: Helm` |
| Upgrade capability | Release can be upgraded | Upgrade succeeds |
| Rollback capability | Release can roll back | Rollback succeeds |
| Uninstall clean | Removal cleans resources | No orphaned resources |

## Validation Workflow

### Pre-Validation Setup

1. Document deployment reference (release name, namespace)
2. Record access endpoints (UI URL, API base)
3. Confirm database connectivity
4. Establish baseline state (existing data count)

### Functional Validation Sequence

1. Verify UI accessibility
2. Test authentication flow
3. Execute chat interactions
4. Verify task operations via chat
5. Confirm conversation persistence

### Persistence Validation Sequence

1. Create identifiable test data
2. Record data identifiers
3. Trigger pod restart
4. Wait for pod ready
5. Query for test data
6. Compare pre/post states

### Architecture Validation Sequence

1. Inspect pod specifications
2. Verify external database usage
3. Test cross-pod consistency
4. Validate configuration sources

### Helm Validation Sequence

1. Verify release status
2. Confirm resource labels
3. Test upgrade path
4. Test rollback path

## Acceptance Matrix

| Category | Weight | Pass Threshold |
|----------|--------|----------------|
| Functional | 40% | All critical paths pass |
| Persistence | 30% | Zero data loss |
| Architecture | 20% | Full stateless compliance |
| Helm | 10% | All management operations work |

**Overall Pass:** All categories meet threshold

## Validation Report Template

```markdown
# Deployment Validation Report

## Deployment Info
- Release: [name]
- Namespace: [namespace]
- Date: [timestamp]
- Validator: [name]

## Summary
- Overall: PASS/FAIL
- Functional: X/Y passed
- Persistence: X/Y passed
- Architecture: X/Y passed
- Helm: X/Y passed

## Detailed Results
[Per-category results]

## Issues Found
[Any failures or concerns]

## Sign-off
[Approval signature]
```
