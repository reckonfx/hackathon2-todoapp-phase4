"""
Database connection module for the Phase-2 Web-Based Todo Application.
Handles PostgreSQL connection setup and session management with async support.
"""

from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
import sys
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file into os.environ



class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/todo_app_db"
    test_database_url: str = ""

    # JWT/Authentication settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Additional environment variables from .env
    backend_env: str = "development"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    auth_secret: str = "dev-secret-change-this"
    auth_token_expire_minutes: int = 60

    # CORS settings - comma-separated list of allowed origins
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://127.0.0.1:3000"

    # Connection pooling settings
    pool_size: int = 20
    max_overflow: int = 0
    pool_timeout: int = 30
    pool_recycle: int = 300
    pool_pre_ping: bool = True

    # Phase III: AI Chat settings
    openai_api_key: str = ""
    chat_max_messages: int = 50
    chat_max_message_length: int = 10000

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra env vars not defined in Settings


settings = Settings()

# Base for models
Base = declarative_base()



# Validate database configuration on startup
def validate_database_config():
    """
    Validate that DATABASE_URL is set and points to PostgreSQL.
    Fails loudly with clear error messages if misconfigured.
    """
    if not settings.database_url:
        raise ValueError(
            "DATABASE_URL is not set! Please configure your .env file with a valid PostgreSQL connection string."
        )
    
    parsed_url = urlparse(settings.database_url)
    
    if not parsed_url.scheme.startswith('postgresql'):
        raise ValueError(
            f"Invalid database configuration! Expected PostgreSQL, got: {parsed_url.scheme}\n"
            f"DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'\n"
            f"Current value: {settings.database_url[:50]}...\n"
            f"SQLite is no longer supported to prevent silent fallbacks."
        )
    
    # Log successful validation
    db_host = parsed_url.hostname or "unknown"
    db_name = parsed_url.path.lstrip('/') or "unknown"
    
    print(f"[OK] Database Configuration Validated")
    print(f"  Database Type: PostgreSQL (async)")
    print(f"  Database Name: {db_name}")
    print(f"  Database Host: {db_host}")
    
    # Check if it's a Neon database
    if 'neon.tech' in settings.database_url:
        print(f"  Provider: Neon PostgreSQL")
    
    return True


# Function to create engines - only called when needed to avoid import-time issues
def create_engines():
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import create_async_engine
    
    # Validate configuration first
    validate_database_config()
    
    parsed_url = urlparse(settings.database_url)
    
    # PostgreSQL-only support (async)
    if not parsed_url.scheme.startswith('postgresql'):
        raise ValueError(
            f"Only PostgreSQL is supported. Got: {parsed_url.scheme}\n"
            f"Please update DATABASE_URL in your .env file."
        )
    
    # PostgreSQL connection with async support
    connect_kwargs = {"server_settings": {"application_name": "todo_app"}}
    
    # Check if this is a Neon connection (has neon.tech in the URL)
    if 'neon.tech' in settings.database_url:
        # For Neon, don't pass server_settings that might conflict with Neon's settings
        # Set SSL requirement for Neon
        connect_kwargs = {"ssl": "require"}
    
    # Async engine for application
    async_engine = create_async_engine(
        settings.database_url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
        pool_pre_ping=settings.pool_pre_ping,
        connect_args=connect_kwargs,
        echo=False  # Set to True for SQL query logging during debugging
    )
    
    # Sync engine for Alembic migrations
    sync_database_url = settings.database_url.replace('postgresql+asyncpg://', 'postgresql://')
    sync_engine = create_engine(
        sync_database_url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
        pool_pre_ping=settings.pool_pre_ping
    )
    
    return async_engine, sync_engine



# Cache for session makers to avoid recreating on every request
_cached_session_makers = None

# Create session makers (these will be created when engines are available)
def get_session_makers():
    global _cached_session_makers

    # Return cached session makers if available
    if _cached_session_makers is not None:
        return _cached_session_makers

    async_engine, sync_engine = create_engines()

    # Create async session maker
    if async_engine:
        from sqlalchemy.ext.asyncio import async_sessionmaker
        async_session_maker = async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    else:
        async_session_maker = None

    # Create sync session maker
    sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)

    # Cache the session makers
    _cached_session_makers = (async_session_maker, sync_session_maker, sync_engine)

    return _cached_session_makers


# For async operations
async def get_async_db():
    """Dependency to get async database session (PostgreSQL only)."""
    async_session_maker, _, _ = get_session_makers()
    async with async_session_maker() as session:
        yield session



# For sync operations (e.g., Alembic)
def get_sync_db():
    """Dependency to get sync database session (for Alembic compatibility)."""
    _, sync_session_maker, _ = get_session_makers()
    db = sync_session_maker()
    try:
        yield db
    finally:
        db.close()


# For Alembic compatibility - get sync engine directly
def get_alembic_engine():
    _, _, sync_engine = get_session_makers()
    return sync_engine


# Provide direct access to sync engine for Alembic
sync_engine = get_alembic_engine()

# Provide direct access to async engine for application
def get_async_engine():
    async_engine, _ = create_engines()
    return async_engine

# Initialize engines on module load
engine = get_async_engine()
sync_engine = get_alembic_engine()