# Research: Neon PostgreSQL Migration

## Decision: Database Engine Migration (SQLite → Neon PostgreSQL)

### Rationale
- Neon PostgreSQL provides production-ready scalability and reliability
- Better concurrency support than SQLite
- Neon offers serverless PostgreSQL with smart caching
- Required for Phase-II web application deployment

### Alternatives Considered
1. **Continue with SQLite**: Limited scalability, not suitable for production web app
2. **Self-hosted PostgreSQL**: More operational overhead than Neon's managed service
3. **Alternative databases (MySQL, MongoDB)**: PostgreSQL offers better ACID compliance and JSON support

### Chosen Solution
Neon PostgreSQL with asyncpg driver for optimal async performance in FastAPI application

## Decision: Async Database Driver (asyncpg)

### Rationale
- asyncpg is the fastest async PostgreSQL driver for Python
- Native async support for FastAPI
- Better performance than psycopg2 with asyncio
- Recommended for production FastAPI applications

### Alternatives Considered
1. **psycopg2 with async wrapper**: Slower performance than native async
2. **aiopg**: Less actively maintained than asyncpg
3. **SQLAlchemy sync with thread pools**: Would block event loop

### Chosen Solution
asyncpg with SQLAlchemy async extensions for optimal performance

## Decision: Migration Strategy (Alembic-first)

### Rationale
- Alembic provides safe, reversible database migrations
- Essential for production database schema management
- Supports both automated and manual migration scripts
- Industry standard for SQLAlchemy applications

### Alternatives Considered
1. **Direct schema creation**: Unsafe for production environments
2. **Manual SQL scripts**: Error-prone and not version-controlled
3. **ORM-managed schema**: Less control and potentially unsafe for production

### Chosen Solution
Alembic with automated migration generation and manual review process

## Decision: No SQLite Fallback

### Rationale
- Simplifies codebase by removing conditional logic
- Ensures consistent behavior across all environments
- Forces complete migration to production-ready database
- Reduces maintenance burden of supporting multiple database engines

### Alternatives Considered
1. **Dual support (SQLite + PostgreSQL)**: Increased complexity and testing burden
2. **Environment-specific databases**: Risk of environment drift
3. **Gradual migration**: Prolongs support of legacy database

### Chosen Solution
Complete migration to PostgreSQL with no fallback mechanism

## PostgreSQL-Specific Considerations Researched

### DateTime with Timezone
- PostgreSQL stores timestamps with timezone info
- SQLAlchemy requires explicit timezone-aware datetime objects
- Migration requires updating all datetime fields to use timezone-aware types

### Connection Pooling
- Neon recommends connection pooling for optimal performance
- SQLAlchemy AsyncSession requires specific pool configuration
- Need to configure appropriate pool sizes for different environments

### JSON Field Support
- PostgreSQL has native JSON/JSONB support
- More efficient than SQLite's text-based JSON storage
- Enables complex queries on JSON data

### Boolean Fields
- PostgreSQL has native boolean type
- More efficient than SQLite's integer-based booleans
- Better type safety and validation

## Migration Process Options Researched

### Fresh Installation Path
- Clean slate approach with initial Alembic migration
- Suitable for new deployments
- Tables created via Alembic migration scripts

### Data Migration Path
- Transfer existing SQLite data to PostgreSQL
- Requires data transformation for type compatibility
- Validates data integrity during migration
- Recommended approach: Export CSV from SQLite, import to PostgreSQL with validation