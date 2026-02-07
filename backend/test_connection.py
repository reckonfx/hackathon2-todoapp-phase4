"""
Simple test to verify PostgreSQL connection works
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_connection():
    """Test the database connection"""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")

    print(f"Testing connection to: {database_url}")

    try:
        # Create async engine
        engine = create_async_engine(database_url)

        # Try to connect and run a simple query
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()

            print(f"✓ Connection successful! Query result: {value}")

        # Dispose of the engine
        await engine.dispose()
        print("✓ Engine disposed successfully")

        return True

    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)