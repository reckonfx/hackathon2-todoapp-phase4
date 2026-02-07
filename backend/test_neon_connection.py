import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Direct connection string for Neon - without sslmode in URL
DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_fCJHD4Ak9ixo@ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech/neondb"

async def test_connection():
    try:
        # Connect with SSL settings in connect_args
        engine = create_async_engine(
            DATABASE_URL,
            connect_args={
                "ssl": "require"  # Pass SSL requirement via connect_args
            }
        )
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            print("Connection successful! Result:", result.fetchone())
        await engine.dispose()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    print("Test completed:", "Success" if success else "Failed")