---
name: containerization-skill
description: |
  Create containerization specifications for existing applications without modifying
  application logic. Use when preparing applications for Docker deployment, defining
  multi-service container strategies, or specifying environment configuration for
  containerized workloads. Supports frontend and backend services with external
  databases. Produces specification artifacts only - not Dockerfiles or commands.
---

# Containerization Skill (Phase IV)

Specify containerization strategy for existing applications without modifying application code or generating implementation artifacts.

## Purpose

Define containerization specifications that prepare existing applications for Docker deployment while preserving application logic unchanged. Produce design documents that guide Dockerfile creation and container orchestration setup.

**Goals:**
- Specify container boundaries for multi-service applications (frontend + backend)
- Define environment variable strategy for external service connections
- Establish build and runtime configuration requirements
- Maintain strict separation between containerization and application logic
- Ensure specifications are reusable across similar application stacks

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Application stack | Yes | Framework/runtime for each service (e.g., Next.js, FastAPI) |
| Service topology | Yes | List of services and their relationships |
| Entry points | Yes | Application startup commands per service |
| Port mappings | Yes | Internal ports each service listens on |
| External dependencies | Yes | Services that remain outside containers (databases, APIs) |
| Environment variables | Yes | Required env vars per service (names and purpose) |
| Build requirements | No | Build-time dependencies (npm, pip, etc.) |
| Static assets | No | Files that need special handling (public/, static/) |
| Health endpoints | No | Paths for container health checks |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Container boundary specification | Markdown | What gets containerized vs. remains external |
| Base image recommendations | Markdown table | Suggested base images with rationale |
| Build stage specification | Markdown | Multi-stage build strategy per service |
| Runtime configuration | Markdown | Environment, ports, volumes, user permissions |
| Environment variable matrix | Markdown table | All env vars with scope (build/runtime) and source |
| Health check specification | Markdown | Liveness/readiness probe definitions |
| Orchestration requirements | Markdown | Service dependencies and startup ordering |

## Constraints

1. **Specification only** - Produce design documents, not Dockerfiles or scripts
2. **No command generation** - Describe requirements in prose, not shell commands
3. **No code modification** - Application source code remains untouched
4. **External database** - Database services (PostgreSQL, etc.) stay outside containers
5. **Framework-agnostic descriptions** - Specifications should translate to any container runtime
6. **No secrets in specs** - Reference secret names, never values
7. **Reusable patterns** - Specifications should apply to similar stacks beyond this project

## Invariants

1. **Application code unchanged** - Zero modifications to source files
2. **All config via environment** - No hardcoded connection strings or credentials
3. **Single responsibility per container** - One service per container image
4. **Non-root execution** - Containers run as unprivileged users
5. **Immutable images** - No runtime modifications to container filesystem
6. **External state** - Databases and persistent storage remain outside containers
7. **Health observability** - Every container exposes health check endpoint
8. **Graceful shutdown** - Signal handling for clean termination
9. **Minimal attack surface** - Production images exclude dev dependencies

## Prohibited Actions

| Action | Reason |
|--------|--------|
| Generate Dockerfiles | Skill produces specifications only |
| Write shell commands | Describe requirements, not implementation |
| Modify application code | Containerization is infrastructure-only |
| Containerize databases | External services remain external |
| Embed secrets | Security violation |
| Specify absolute paths from host | Breaks portability |
| Assume specific orchestrator | Stay runtime-agnostic |
| Include dev tools in runtime spec | Minimizes attack surface |

## Specification Patterns

### Container Boundary Definition

For each service, specify:
- **Containerized**: Application runtime, dependencies, static assets
- **External**: Databases, third-party APIs, secrets management

### Multi-Stage Build Strategy

Describe stages without Dockerfile syntax:
- **Stage 1 (Builder)**: Install build tools, compile/bundle application
- **Stage 2 (Runtime)**: Copy artifacts, install runtime dependencies only

### Environment Variable Categories

| Category | Scope | Examples |
|----------|-------|----------|
| Build-time | Docker build | NODE_ENV, API_URL for static embedding |
| Runtime | Container start | DATABASE_URL, SECRET_KEY |
| Platform | Orchestrator-injected | PORT, HOST |

### Service-Specific Patterns

**Frontend (Next.js/React):**
- Static export vs. server-side rendering mode
- Environment variable embedding at build time
- Nginx/Node runtime considerations

**Backend (FastAPI/Python):**
- ASGI server selection (uvicorn, gunicorn)
- Async database driver requirements
- Worker process configuration

**AI/Agent Services:**
- API key injection strategy
- SDK dependency management
- Timeout and resource considerations

### External Service Connections

Specify connection patterns for external dependencies:
- Database: Connection string via environment variable
- External APIs: Base URL + credentials via environment
- Secrets: Reference to secrets manager, not values

## Usage Workflow

1. Inventory application services and their technology stacks
2. Identify external dependencies that remain outside containers
3. Document entry points and port requirements per service
4. Map all environment variables with scope and purpose
5. Specify container boundaries for each service
6. Define multi-stage build requirements
7. Document health check and graceful shutdown needs
8. Specify inter-service communication patterns

## Reusability

This skill applies to any application with:
- Separate frontend and backend services
- External managed database
- Environment-based configuration
- Standard web framework patterns

Adapt specifications by substituting:
- Framework names (Next.js → Vue, FastAPI → Express)
- Database references (PostgreSQL → MySQL)
- Runtime requirements (Python → Node.js)
