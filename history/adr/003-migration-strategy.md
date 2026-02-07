# ADR-003: Database Migration Strategy

**Status**: Accepted
**Date**: 2026-01-15

## Context

The application needs to migrate from SQLite to PostgreSQL without losing existing data or disrupting service. The migration approach must be safe, reversible, and suitable for both development and production environments. We need to decide on the migration methodology and whether to maintain backward compatibility with SQLite.

## Decision

We will adopt an Alembic-first migration strategy with no SQLite fallback:

- **Alembic for all schema management**: All database schema changes will be managed through Alembic migrations
- **No SQLite fallback**: Remove all conditional SQLite code and support only PostgreSQL
- **Clean migration path**: Two possible approaches depending on requirements:
  - Fresh installation: Clean PostgreSQL schema with initial Alembic migration
  - Data migration: Transfer existing SQLite data to PostgreSQL with validation
- **Environment-specific configurations**: Different settings for development, staging, and production

## Alternatives Considered

1. **Dual database support**: Maintaining both SQLite and PostgreSQL paths would increase complexity and testing burden
2. **Direct schema creation**: Skipping Alembic and using Base.metadata.create_all() would be unsafe for production
3. **Manual SQL migration scripts**: Would lack version control and rollback capabilities
4. **Gradual migration**: Keeping SQLite for some operations would prolong the transition period
5. **ORM-managed schema only**: Would not provide the control and safety of Alembic migrations

## Consequences

### Positive
- Simplified codebase without conditional database logic
- Safe, version-controlled schema changes with Alembic
- Consistent behavior across all environments
- Production-ready migration process
- Clear separation of schema management from application code

### Negative
- Loss of local development convenience of SQLite
- Requires PostgreSQL availability for all environments
- More complex initial setup for development
- Irreversible commitment to PostgreSQL (though other databases could be swapped in later)

## References

- specs/001-db-migration/plan.md
- specs/001-db-migration/research.md
- specs/001-db-migration/quickstart.md