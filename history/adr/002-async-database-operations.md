# ADR-002: Async Database Operations

**Status**: Accepted
**Date**: 2026-01-15

## Context

The application uses FastAPI, which is built on asyncio for high-performance async operations. The current database layer uses synchronous SQLAlchemy operations, which can block the event loop and limit the benefits of FastAPI's async architecture. For production readiness and scalability, we need to implement proper async database operations.

## Decision

We will implement fully async database operations using:
- **SQLAlchemy 2.0+ async extensions** for database operations
- **create_async_engine** instead of create_engine
- **AsyncSession** for database sessions
- **async/await patterns** throughout all database interactions
- **Proper async dependency injection** for FastAPI database dependencies

## Alternatives Considered

1. **Keep sync operations with thread pools**: Would block event loop and reduce performance benefits of FastAPI
2. **Mixed sync/async operations**: Would create inconsistency and potential deadlocks
3. **Alternative async ORMs**: SQLAlchemy has the strongest async support and ecosystem in Python
4. **Raw async database drivers**: Would lose ORM benefits like relationship handling and query building

## Consequences

### Positive
- Full utilization of FastAPI's async capabilities for improved performance
- Better concurrency handling under load
- Proper resource utilization without blocking the event loop
- Scalable architecture for production use
- Future-proof foundation for additional async features

### Negative
- More complex implementation than sync operations
- Requires careful handling of async context in dependency injection
- Steeper learning curve for async SQLAlchemy patterns
- Potential for subtle bugs if async patterns are mixed incorrectly

## References

- specs/001-db-migration/plan.md
- specs/001-db-migration/research.md
- specs/001-db-migration/data-model.md