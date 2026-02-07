# Data Model: Neon PostgreSQL Migration

## Entity: Todo
**Table Name**: `todos`

### Fields
- `id`: Integer (Primary Key, Auto-increment) - Unique identifier for each todo
- `title`: String (VARCHAR, max 255) - Title of the todo item
- `description`: Text (Optional) - Detailed description of the todo
- `completed`: Boolean - Status indicating if the todo is completed
- `created_at`: DateTime (Timezone-aware) - Timestamp when the todo was created
- `updated_at`: DateTime (Timezone-aware) - Timestamp when the todo was last updated

### Relationships
- No direct relationships defined in the basic Todo entity

### Validation Rules
- `title` is required and must not exceed 255 characters
- `completed` defaults to False
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any modification

### PostgreSQL-Specific Considerations
- Use TIMESTAMP WITH TIME ZONE for `created_at` and `updated_at`
- Use native BOOLEAN type for `completed` field
- Index on `completed` field for efficient querying
- Potential JSON field for extended metadata if needed

## Entity: Database Session
**Conceptual**: Not a physical table but represents the async session management

### Characteristics
- Async SQLAlchemy session for database operations
- Proper lifecycle management with async context managers
- Connection pooling with configurable parameters
- Transaction handling with rollback capabilities

### PostgreSQL Connection Parameters
- Connection string: `postgresql+asyncpg://username:password@host:port/database`
- Pool size: Configurable (recommended: 20 for production)
- Pool recycle: 300 seconds
- Pool pre-ping: Enabled for connection health checks

## Entity: Connection Pool
**Conceptual**: Represents PostgreSQL connection pooling configuration

### Configuration Parameters
- `pool_size`: Number of connections to maintain (default: 20)
- `max_overflow`: Additional connections allowed beyond pool_size (default: 0)
- `pool_timeout`: Timeout for getting connection from pool (default: 30)
- `pool_recycle`: Seconds after which to recreate connections (default: 300)
- `pool_pre_ping`: Verify connections before use (default: True)

## State Transitions
- Todo creation: `completed` defaults to False
- Todo update: `updated_at` automatically updated
- Todo completion: `completed` changes from False to True
- Todo reopening: `completed` changes from True to False

## Indexing Strategy
- Primary key index on `id` (automatic)
- Index on `completed` for filtering completed/incomplete todos
- Composite index on `(created_at, completed)` for chronological queries
- Potential full-text search index on `title` and `description` for search functionality

## Data Migration Requirements
- Transform SQLite datetime strings to PostgreSQL TIMESTAMP WITH TIME ZONE
- Convert SQLite integer booleans to PostgreSQL native BOOLEAN
- Preserve all existing data during migration
- Validate data integrity after migration
- Handle NULL values consistently between database systems