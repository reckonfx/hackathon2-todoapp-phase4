# Quickstart: Neon PostgreSQL Migration

## Prerequisites

- Python 3.14+
- Poetry or pip for dependency management
- Neon PostgreSQL account and connection string
- Existing codebase with SQLite setup

## Setup Steps

### 1. Update Environment Variables
```bash
# Update backend/.env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
ENV=development
NEON_POOL_SIZE=20  # Optional: custom connection pool size
```

### 2. Install Dependencies
```bash
cd backend
poetry add asyncpg  # or pip install asyncpg
# Note: psycopg2-binary can remain for sync operations if needed
```

### 3. Update Database Connection Layer
The connection layer needs to be updated to use async SQLAlchemy:

- Replace `create_engine` with `create_async_engine`
- Update session creation to use `AsyncSession`
- Configure connection pooling for async operations

### 4. Initialize Alembic for PostgreSQL
```bash
# From backend directory
alembic init alembic
# Update alembic.ini with PostgreSQL connection
# Generate initial migration
alembic revision --autogenerate -m "Initial migration for PostgreSQL"
# Apply migration
alembic upgrade head
```

### 5. Update Models for PostgreSQL Compatibility
- Change datetime fields to use timezone-aware types
- Update boolean fields to use native PostgreSQL boolean
- Adjust string length constraints as needed

### 6. Update Dependency Injection
- Create async database dependency for FastAPI
- Update session lifecycle management for async operations
- Ensure proper session closing in async context

## Running the Migrated Application

### Development
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Database Connection
```bash
# Run database connectivity test
python -c "
from src.database.connection import engine
import asyncio

async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text('SELECT 1'))
        print('Connection successful:', result.fetchone())

asyncio.run(test_connection())
"
```

## Migration Strategies

### Option A: Fresh Installation (No Existing Data)
1. Set up new PostgreSQL database
2. Run Alembic migrations to create tables
3. Update application configuration
4. Deploy application

### Option B: Data Migration (From SQLite)
1. Export data from SQLite (CSV or JSON format)
2. Transform data for PostgreSQL compatibility
3. Import data to PostgreSQL
4. Validate data integrity
5. Update application configuration
6. Deploy application

## Troubleshooting

### Common Issues
- **SSL Connection Errors**: Ensure sslmode=require in connection string
- **Async Operation Errors**: Verify all database operations use async/await
- **Datetime Format Issues**: Ensure timezone-aware datetime objects
- **Connection Pool Exhaustion**: Adjust pool_size based on traffic

### Verification Commands
```bash
# Check database connectivity
alembic current

# Verify table existence
alembic check

# Run application tests
pytest tests/
```