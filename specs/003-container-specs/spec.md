# Feature Specification: Phase IV Containerization Contracts

**Feature Branch**: `003-container-specs`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase IV containerization specification for frontend, backend, and MCP server containers"

## Overview

This specification defines containerization contracts for the Todo AI Chatbot application services. It establishes what each container includes, excludes, requires, and guarantees—without prescribing implementation details such as Dockerfiles or commands.

### Deployment Topology Summary

| Service | Container | Deployment Unit |
|---------|-----------|-----------------|
| Frontend | `todo-frontend` | Standalone container |
| Backend + MCP Server | `todo-backend` | Co-located in single container |
| Database | External (Neon PostgreSQL) | NOT containerized |

### MCP Server Co-Location Justification

The MCP server is co-located within the backend container rather than deployed separately for the following reasons:

1. **Architectural Integration**: The MCP server (`backend/src/mcp/`) is implemented as an in-process module that shares the database session and service layer with the backend API
2. **No Separate Runtime**: The MCP tools are invoked directly by the OpenAI agent integration service within the same Python process
3. **Database Session Sharing**: MCP tools require the same async database session as the API routes
4. **Statelessness Compliance**: Both backend API and MCP tools are stateless; separating them would add network overhead without benefit
5. **Phase III Design**: The research.md R3 specification mandates "in-process MCP server using stdio transport"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend Container Specification (Priority: P1)

A DevOps engineer needs a complete containerization contract for the backend service (including MCP server) that ensures the container can run in any Kubernetes environment.

**Why this priority**: The backend is the core service; without it, neither frontend nor AI features function.

**Independent Test**: Can be fully tested by verifying the contract document contains all required fields and is reviewable by infrastructure team.

**Acceptance Scenarios**:

1. **Given** the backend container contract, **When** reviewed by infrastructure team, **Then** all required sections are present and unambiguous
2. **Given** the backend container contract, **When** an environment variable is missing at runtime, **Then** the container fails to start with a clear error message
3. **Given** the backend container contract, **When** the health check endpoint is called, **Then** it returns the expected response within the specified timeout

---

### User Story 2 - Frontend Container Specification (Priority: P1)

A DevOps engineer needs a complete containerization contract for the frontend service that ensures the container serves the web application correctly.

**Why this priority**: The frontend is the user-facing interface; it must be containerized to complete the deployment.

**Independent Test**: Can be fully tested by verifying the contract document contains all required fields and is reviewable by infrastructure team.

**Acceptance Scenarios**:

1. **Given** the frontend container contract, **When** reviewed by infrastructure team, **Then** all required sections are present and unambiguous
2. **Given** the frontend container contract, **When** the backend URL is misconfigured, **Then** the container still starts but displays connection error to users
3. **Given** the frontend container contract, **When** the health check endpoint is called, **Then** it returns the expected response within the specified timeout

---

### User Story 3 - Container Compliance Verification (Priority: P2)

A DevOps engineer needs to verify that all container specifications comply with Phase IV containerization rules (C-001 to C-008).

**Why this priority**: Compliance ensures containers are suitable for Kubernetes deployment and follow governance rules.

**Independent Test**: Can be fully tested by checking each specification against the C-001 to C-008 checklist.

**Acceptance Scenarios**:

1. **Given** any container specification, **When** checked against C-001 (specification document), **Then** the document exists
2. **Given** any container specification, **When** checked against C-007 (no baked secrets), **Then** no secrets appear in the specification
3. **Given** any container specification, **When** checked against C-006 (environment variables), **Then** all configuration is via environment variables

---

### Edge Cases

- What happens when a required environment variable is missing? Container MUST fail fast with a clear error message.
- What happens when the database is unreachable at startup? Container MUST start and report unhealthy via health check.
- What happens when the frontend cannot reach the backend? Frontend MUST display a user-friendly error message.

---

## Container Specifications

### Container 1: Frontend (`todo-frontend`)

#### Purpose

Serve the Todo AI Chatbot web interface to end users.

#### Included Components

| Component | Description |
|-----------|-------------|
| Next.js 15 Application | Server-side rendered React 19 application |
| Static Assets | Compiled CSS, JavaScript bundles, images |
| Node.js Runtime | Production runtime for server components |

#### Excluded Components

| Component | Reason |
|-----------|--------|
| Development dependencies | Not needed in production (C-004) |
| Test files | Not needed in production |
| Source TypeScript files | Only compiled JavaScript included |
| `node_modules` dev packages | Production dependencies only |
| `.env` files | Configuration via environment variables (C-006) |

#### Runtime Assumptions

| Assumption | Specification |
|------------|---------------|
| Node.js Version | 20.x LTS (pinned, not `latest`) |
| Memory | Minimum 256MB, recommended 512MB |
| CPU | Minimum 0.25 cores, recommended 0.5 cores |
| Network | Must reach backend API endpoint |
| Filesystem | Read-only (no local state) |

#### Required Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API base URL | `http://todo-backend:8000` |
| `NODE_ENV` | Yes | Runtime environment | `production` |
| `PORT` | No | Listen port (default: 3000) | `3000` |

#### Exposed Ports

| Port | Protocol | Description |
|------|----------|-------------|
| 3000 | TCP | HTTP server for web application |

#### Health Check Expectations

| Endpoint | Method | Expected Response | Timeout |
|----------|--------|-------------------|---------|
| `/` | GET | HTTP 200 with HTML content | 5 seconds |

#### Statelessness Guarantees

- Container maintains NO local state
- All user data flows through backend API
- Container can be replaced at any time without data loss
- Multiple replicas can run simultaneously without coordination

---

### Container 2: Backend (`todo-backend`)

#### Purpose

Serve the Todo API, chat functionality, and AI agent integration (including MCP tools).

#### Included Components

| Component | Description |
|-----------|-------------|
| FastAPI Application | REST API for tasks, auth, and chat |
| MCP Server Module | In-process MCP tools for AI agent |
| OpenAI Agents SDK | AI agent integration |
| SQLAlchemy + asyncpg | Async database connectivity |
| Uvicorn | ASGI server |
| Alembic | Database migrations (run separately) |

#### Excluded Components

| Component | Reason |
|-----------|--------|
| Development dependencies | Not needed in production (C-004) |
| Test files and pytest | Not needed in production |
| `.env` files | Configuration via environment variables (C-006) |
| Database data | External database (Neon PostgreSQL) |
| Alembic migration runner | Migrations run as separate job |

#### Runtime Assumptions

| Assumption | Specification |
|------------|---------------|
| Python Version | 3.13+ (pinned, not `latest`) |
| Memory | Minimum 512MB, recommended 1GB |
| CPU | Minimum 0.5 cores, recommended 1 core |
| Network | Must reach external PostgreSQL, OpenAI API |
| Filesystem | Read-only (no local state) |
| Database | External Neon PostgreSQL (NOT containerized) |

#### Required Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host:5432/db` |
| `SECRET_KEY` | Yes | JWT signing key | (secret - not baked) |
| `OPENAI_API_KEY` | Yes | OpenAI API key for agents | (secret - not baked) |
| `BACKEND_ENV` | Yes | Runtime environment | `production` |
| `BACKEND_HOST` | No | Listen host (default: 0.0.0.0) | `0.0.0.0` |
| `BACKEND_PORT` | No | Listen port (default: 8000) | `8000` |
| `CORS_ORIGINS` | Yes | Allowed CORS origins | `http://todo-frontend:3000` |
| `AUTH_SECRET` | Yes | Authentication secret | (secret - not baked) |
| `AUTH_TOKEN_EXPIRE_MINUTES` | No | Token expiry (default: 60) | `60` |
| `POOL_SIZE` | No | DB connection pool size (default: 20) | `20` |
| `MAX_OVERFLOW` | No | DB pool overflow (default: 0) | `0` |
| `POOL_TIMEOUT` | No | DB pool timeout (default: 30) | `30` |
| `CHAT_MAX_MESSAGES` | No | Max messages per conversation (default: 50) | `50` |

#### Exposed Ports

| Port | Protocol | Description |
|------|----------|-------------|
| 8000 | TCP | HTTP server for REST API |

#### Health Check Expectations

| Endpoint | Method | Expected Response | Timeout |
|----------|--------|-------------------|---------|
| `/health` | GET | HTTP 200 with JSON `{"status": "healthy"}` | 10 seconds |

**Health Check Response Schema**:

```json
{
  "status": "healthy",
  "service": "todo-api",
  "database": {
    "type": "PostgreSQL",
    "host": "<hostname>",
    "connected": true
  }
}
```

#### Statelessness Guarantees

- Container maintains NO local state
- All state persisted in external PostgreSQL database
- Container can be replaced at any time without data loss
- Multiple replicas can run simultaneously (database handles concurrency)
- No in-memory session storage (per Phase III 14.2.3)
- Conversation context reconstructed from database on every request

---

### Container 3: MCP Server (NOT SEPARATE)

**Decision**: The MCP server is NOT deployed as a separate container.

**Justification** (restated for completeness):

1. The MCP server is implemented as an in-process Python module (`backend/src/mcp/`)
2. It shares the database session with the backend API
3. The OpenAI agent invokes MCP tools directly within the same process
4. Separating would require inter-process communication with no benefit
5. Phase III design specifies "in-process MCP server using stdio transport"

**Result**: MCP functionality is included in the `todo-backend` container as documented above.

---

## Phase IV Compliance Matrix

| Rule ID | Rule | Frontend | Backend |
|---------|------|----------|---------|
| C-001 | Container specification document exists | Yes | Yes |
| C-002 | Multi-stage builds for production | Required | Required |
| C-003 | Base images pinned (no `latest`) | Node 20.x LTS | Python 3.13 |
| C-004 | No development dependencies | Excluded | Excluded |
| C-005 | Health check endpoints specified | `/` | `/health` |
| C-006 | Environment variables only | Yes | Yes |
| C-007 | No secrets baked in | Yes | Yes |
| C-008 | Exposed ports documented | 3000 | 8000 |

---

## Phase Context & Constraints *(Phase-IV)*

- **Scope**: Containerization specification ONLY — no application logic changes
- **Database**: External Neon PostgreSQL (NOT containerized per K-007)
- **Statelessness**: Preserved from Phase III (per 14.2.3, 15.2.4)
- **Configuration**: Environment variables exclusively (per C-006)
- **Secrets**: Never baked into images (per C-007)
- **External Specs**: Phase III spec at `specs/003-agent-mcp-tools/spec.md`, `specs/004-chat-api-db-contracts/spec.md`

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Frontend container specification MUST include all required sections (purpose, components, environment variables, ports, health check, statelessness)
- **FR-002**: Backend container specification MUST include all required sections (purpose, components, environment variables, ports, health check, statelessness)
- **FR-003**: All containers MUST receive configuration exclusively via environment variables
- **FR-004**: All containers MUST expose health check endpoints as specified
- **FR-005**: All containers MUST be stateless and replaceable without data loss
- **FR-006**: Backend container MUST include MCP server functionality (co-located)
- **FR-007**: No container specification MUST include the database (external dependency)
- **FR-008**: All container specifications MUST comply with Phase IV rules C-001 to C-008
- **FR-009**: Backend container MUST fail fast with clear error if required environment variables are missing
- **FR-010**: Secrets (API keys, passwords) MUST NOT appear in container specifications

### Key Entities

- **Container Specification**: A document defining what a container includes, excludes, requires, and guarantees
- **Environment Variable Contract**: The set of environment variables a container expects at runtime
- **Health Check Contract**: The endpoint, method, and expected response for container health verification
- **Statelessness Guarantee**: The promise that a container maintains no local state

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of container specifications include all required sections
- **SC-002**: 100% compliance with Phase IV containerization rules (C-001 to C-008)
- **SC-003**: All required environment variables are documented with descriptions
- **SC-004**: Health check endpoints are specified for all containers
- **SC-005**: No secrets appear in any container specification
- **SC-006**: MCP server co-location is documented and justified
- **SC-007**: Database exclusion is documented (external dependency)
- **SC-008**: Infrastructure team can review and approve specifications without implementation details

## Assumptions

- Node.js 20.x LTS is the approved base image version for frontend
- Python 3.13 is the approved base image version for backend (per constitution Section 7)
- Multi-stage builds will be used for production images (implementation detail, not specified here)
- Kubernetes deployment will provide environment variables via ConfigMaps and Secrets
- External PostgreSQL database is accessible from Kubernetes cluster network
- OpenAI API is accessible from Kubernetes cluster network
