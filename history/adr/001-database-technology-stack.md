# ADR-001: Database Technology Stack

**Status**: Accepted
**Date**: 2026-01-15

## Context

The Phase-2 Web-Based Todo Application currently uses SQLite for its database layer, which is suitable for development but not production-ready. We need to migrate to a production-capable database solution that can handle concurrent users, provide robust data integrity, and offer scalability.

## Decision

We will adopt the following database technology stack:
- **Database Engine**: Neon PostgreSQL (managed serverless PostgreSQL)
- **Async Driver**: asyncpg for optimal async performance with FastAPI
- **Migration Tool**: Alembic for safe, version-controlled schema migrations

## Alternatives Considered

1. **Continue with SQLite**: Limited scalability and concurrency, not suitable for production web applications
2. **Self-hosted PostgreSQL with psycopg2**: Higher operational overhead than Neon's managed service, sync driver would require thread pools
3. **Alternative databases (MySQL, MongoDB)**: PostgreSQL offers superior ACID compliance and advanced features for application requirements
4. **Different migration tools**: Raw SQL scripts would lack version control and rollback capabilities

## Consequences

### Positive
- Production-ready scalability and reliability with Neon's serverless architecture
- Optimal async performance with asyncpg driver
- Safe, version-controlled schema migrations with Alembic
- Industry-standard SQL database with extensive documentation and community support
- Advanced PostgreSQL features like JSON support, full-text search, and advanced indexing

### Negative
- Increased complexity compared to SQLite
- Requires external service dependency (Neon)
- Learning curve for PostgreSQL-specific features
- Potential costs associated with managed PostgreSQL service

## References

- specs/001-db-migration/plan.md
- specs/001-db-migration/research.md
- specs/001-db-migration/data-model.md