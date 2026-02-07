# Database API Contract: Neon PostgreSQL Migration

## Overview
This contract defines the database API interfaces that must be maintained during the migration from SQLite to Neon PostgreSQL. All CRUD operations must preserve the same interface contracts while improving underlying implementation.

## Database Connection Contract

### Connection Interface
```python
# Expected interface after migration
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session."""
    pass
```

### Session Management
- Sessions must be properly closed after use
- Async sessions must support proper context management
- Transaction boundaries must be preserved

## CRUD Operations Contract

### Todo Operations
All existing Todo CRUD operations must maintain the same function signatures:

#### CREATE
- `create_todo(db: AsyncSession, todo_data: TodoCreate) -> Todo`
- Must return complete Todo object with auto-generated fields
- Must handle validation errors appropriately

#### READ
- `get_todo(db: AsyncSession, todo_id: int) -> Todo | None`
- `get_todos(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Todo]`
- Must preserve pagination behavior
- Must handle missing records gracefully

#### UPDATE
- `update_todo(db: AsyncSession, todo_id: int, todo_update: TodoUpdate) -> Todo | None`
- Must update `updated_at` timestamp automatically
- Must preserve record if no changes provided

#### DELETE
- `delete_todo(db: AsyncSession, todo_id: int) -> bool`
- Must return True if deletion successful, False if record not found
- Must handle concurrent access safely

## Data Type Contract

### Field Type Preservation
During migration, the following type mappings must be preserved:

| Logical Type | SQLite Type | PostgreSQL Type | Validation |
|--------------|-------------|-----------------|------------|
| ID | INTEGER PRIMARY KEY | SERIAL PRIMARY KEY | Auto-increment |
| Title | VARCHAR(255) | VARCHAR(255) | Required, max 255 chars |
| Description | TEXT | TEXT | Optional |
| Completed | INTEGER (0/1) | BOOLEAN | True/False |
| Created At | DATETIME | TIMESTAMP WITH TIME ZONE | Auto-set on creation |
| Updated At | DATETIME | TIMESTAMP WITH TIME ZONE | Auto-update on modification |

### Data Integrity
- Primary key constraints must be preserved
- Foreign key relationships (if any) must be migrated correctly
- Unique constraints must be maintained
- Not-null constraints must be preserved

## Error Handling Contract

### Database Errors
- Connection errors must be caught and logged appropriately
- Constraint violations must return appropriate HTTP status codes
- Transaction rollbacks must occur on errors
- Resource cleanup must happen in all error scenarios

### Expected Error Types
- `DatabaseConnectionError` - Unable to connect to database
- `NotFoundError` - Requested record does not exist
- `ValidationError` - Data validation failed
- `IntegrityError` - Database constraint violation

## Performance Contract

### Response Time Expectations
- Simple SELECT operations: < 50ms
- INSERT/UPDATE operations: < 100ms
- Bulk operations: < 500ms
- All operations must maintain current performance levels or improve

### Concurrency Requirements
- Must support concurrent read/write operations
- Transaction isolation must be preserved
- Connection pooling must handle expected load

## Migration Validation Contract

### Pre-Migration Checks
- Backup existing SQLite data
- Verify PostgreSQL connection parameters
- Test migration scripts on copy of data

### Post-Migration Validation
- All existing data must be accessible
- All existing functionality must work identically
- Performance must meet or exceed current levels
- All automated tests must pass

## Testing Contract

### Required Tests
- Unit tests for all database operations
- Integration tests with PostgreSQL
- Performance tests comparing SQLite vs PostgreSQL
- Migration validation tests

### Test Data Requirements
- Test data must be compatible with both SQLite and PostgreSQL
- Date/time values must be timezone-aware
- Boolean values must map correctly