"""
Database dependency injection module for the Phase-2 Web-Based Todo Application.
Provides database session dependency for FastAPI (async PostgreSQL only).
"""

from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .connection import get_async_db, get_session_makers


async def get_db() -> AsyncGenerator:
    """
    Dependency to get async database session for all routes.
    
    PostgreSQL-only (async). This function is used as a FastAPI dependency
    to provide an async database session to route handlers.
    """
    async for session in get_async_db():
        yield session


def get_sync_db() -> Generator:
    """
    Dependency to get sync database session for auth routes.
    
    This function is used as a FastAPI dependency to provide
    a sync database session to route handlers that haven't been
    migrated to async yet (auth routes).
    """
    _, sync_session_maker, _ = get_session_makers()
    db = sync_session_maker()
    try:
        yield db
    finally:
        db.close()