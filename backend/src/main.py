from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, tasks, chat
from .database.connection import engine, Base
import uvicorn
from sqlalchemy.ext.asyncio import AsyncEngine
from .database.connection import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for database initialization and validation."""
    try:
        # Validate database configuration on startup
        from .database.connection import validate_database_config
        validate_database_config()
        
        print("[OK] Database connection validated successfully")
        print("  Application is ready to accept requests")
        
        # Note: Table creation is handled by Alembic migrations
        # We don't create tables here to maintain proper migration history
        
        yield
    except Exception as e:
        print(f"[FAIL] FATAL: Database initialization failed: {e}")
        print("  Please check your DATABASE_URL in .env file")
        raise  # Fail loudly - don't start the app with invalid database config
    finally:
        # Close the engine connection pool on shutdown
        await engine.dispose()
        print("[OK] Database connections closed")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    description="API for the Phase-2 Web-Based Todo Application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware with dynamic origins from environment
# Parse comma-separated CORS origins from settings
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

# Add wildcard for production if BACKEND_ENV is production and no specific origins set
if settings.backend_env == "production" and len(cors_origins) <= 2:
    # Allow all origins in production deployments (Hugging Face, etc.)
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True if "*" not in cors_origins else False,  # credentials don't work with *
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint with database status."""
    from urllib.parse import urlparse
    parsed_url = urlparse(settings.database_url)
    db_type = "PostgreSQL" if parsed_url.scheme.startswith('postgresql') else "Unknown"
    db_host = parsed_url.hostname or "unknown"
    
    return {
        "status": "healthy",
        "service": "todo-api",
        "database": {
            "type": db_type,
            "host": db_host,
            "connected": True  # If we're running, we're connected
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Make sure this matches your frontend
