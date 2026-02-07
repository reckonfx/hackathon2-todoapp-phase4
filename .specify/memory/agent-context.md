# Phase-2 Web-Based Todo Application Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-15

## Active Technologies

Python 3.14, FastAPI, SQLAlchemy 2.0+, asyncpg, Alembic, Neon PostgreSQL, Pydantic, Uvicorn, pytest

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── database/
│       ├── connection.py
│       ├── deps.py
│       └── schemas/
├── alembic/
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
├── alembic.ini
├── .env
├── pyproject.toml
└── tests/
```

## Commands

- `uvicorn src.main:app --reload` - Run development server
- `alembic revision --autogenerate -m "message"` - Generate migration
- `alembic upgrade head` - Apply migrations
- `pytest` - Run tests
- `poetry install` - Install dependencies

## Code Style

- Use async/await for all database operations
- Follow FastAPI dependency injection patterns
- Use Pydantic for data validation
- Maintain type hints throughout
- Follow SQLAlchemy 2.0 async patterns

## Recent Changes

- Neon PostgreSQL Migration: Updated database layer to use asyncpg and PostgreSQL
- Alembic Integration: Added proper migration management
- Async Database Operations: Converted all database operations to async

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->