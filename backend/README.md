# Todo Backend API

Backend API for the Phase-2 Web-Based Todo Application with PostgreSQL support.

## Database Migration to PostgreSQL

This project has been migrated from SQLite to PostgreSQL for production readiness.

### Prerequisites

- Python 3.14+
- PostgreSQL server (for production) or SQLite (for development)
- Poetry for dependency management

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
poetry install
```

Or using pip:

```bash
pip install -r requirements.txt
```

### Configuration

Copy the appropriate environment file:

For development (SQLite):
```bash
cp .env.example .env
```

For production (PostgreSQL):
```bash
cp .env.production .env
```

Update the `.env` file with your database connection settings:

```env
# For PostgreSQL
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_app_db

# For SQLite (development)
DATABASE_URL=sqlite:///./todo_app_local.db
```

### Database Setup

#### Using Alembic for Migrations

Initialize the database:

```bash
# Make sure you're in the backend directory
cd backend

# Run migrations to create/update tables
python -m alembic upgrade head
```

#### Generating New Migrations

When you make changes to the models:

```bash
python -m alembic revision --autogenerate -m "Description of changes"
python -m alembic upgrade head
```

### Running the Application

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Files

- `.env` - Development configuration
- `.env.staging` - Staging environment configuration
- `.env.production` - Production environment configuration

### Connection Pooling

The application uses connection pooling with the following default settings:
- `POOL_SIZE=20`
- `MAX_OVERFLOW=0`
- `POOL_TIMEOUT=30`
- `POOL_RECYCLE=300`
- `POOL_PRE_PING=True`

These can be adjusted in your environment files for different environments.

### Data Migration

If migrating from SQLite to PostgreSQL, use the provided migration script:

```bash
python src/database/migration_script.py
```

Validate the migration:

```bash
python src/database/validation_script.py
```

## Hugging Face Spaces Deployment

This backend is configured for deployment on Hugging Face Spaces using Docker.

### Setup on Hugging Face

1. Create a new Space with **Docker** SDK
2. Upload or connect this repository
3. Configure the following **Secrets** in Space Settings:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db` |
| `SECRET_KEY` | JWT signing key | `your-super-secret-key` |
| `OPENAI_API_KEY` | OpenAI API key for chat | `sk-...` |
| `CORS_ORIGINS` | Allowed origins (use `*` for all) | `*` |
| `BACKEND_ENV` | Environment mode | `production` |

### Environment Variables

The following environment variables are supported:

```env
# Required
DATABASE_URL=postgresql+asyncpg://username:password@host:5432/dbname
SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=sk-your-openai-api-key

# Optional
CORS_ORIGINS=*
BACKEND_ENV=production
ACCESS_TOKEN_EXPIRE_MINUTES=30
POOL_SIZE=20
```

### Local Docker Testing

```bash
# Build the image
docker build -t todo-backend .

# Run with environment variables
docker run -p 7860:7860 \
  -e DATABASE_URL="your-db-url" \
  -e SECRET_KEY="your-secret" \
  -e OPENAI_API_KEY="your-key" \
  -e CORS_ORIGINS="*" \
  todo-backend
```

### API Endpoints

Once deployed, the API will be available at:
- Health check: `https://your-space.hf.space/health`
- API docs: `https://your-space.hf.space/docs`
- Auth: `https://your-space.hf.space/api/auth/*`
- Tasks: `https://your-space.hf.space/api/tasks/*`
- Chat: `https://your-space.hf.space/api/{user_id}/chat`