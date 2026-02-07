"""
Final verification test to ensure the application works correctly with PostgreSQL backend
"""

import asyncio
import httpx
import subprocess
import sys
import os

async def test_api_endpoints():
    """Test all API endpoints to verify they work with PostgreSQL"""

    base_url = "http://localhost:8000"

    # Test the health check endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            print(f"Health check: {response.status_code} - {response.json()}")

            if response.status_code != 200:
                print("✗ Health check failed")
                return False

            print("✓ Health check passed")
    except Exception as e:
        print(f"✗ Failed to reach health endpoint: {e}")
        return False

    # Test the root endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/")
            print(f"Root endpoint: {response.status_code} - {response.json()}")

            if response.status_code != 200:
                print("✗ Root endpoint failed")
                return False

            print("✓ Root endpoint passed")
    except Exception as e:
        print(f"✗ Failed to reach root endpoint: {e}")
        return False

    print("✓ All API endpoints are accessible")
    return True

async def test_database_connection():
    """Test database connection directly"""

    try:
        # Import the database connection
        from src.database.connection import get_alembic_engine

        # Get the sync engine
        engine = get_alembic_engine()

        # Test the connection
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            value = result.scalar()

            print(f"Database connection test: {value}")

            if value == 1:
                print("✓ Database connection successful")
                return True
            else:
                print("✗ Database connection failed")
                return False

    except Exception as e:
        print(f"✗ Database connection test failed: {e}")
        return False

def run_unit_tests():
    """Run unit tests to verify functionality"""
    try:
        # Run pytest to execute tests
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"],
                              capture_output=True, text=True, cwd=os.getcwd())

        print(f"Unit tests exit code: {result.returncode}")
        print(f"Unit tests output: {result.stdout}")

        if result.returncode != 0:
            print(f"Unit tests errors: {result.stderr}")
            return False

        print("✓ Unit tests passed")
        return True

    except Exception as e:
        print(f"✗ Failed to run unit tests: {e}")
        return False

async def final_verification():
    """Perform final verification of the PostgreSQL migration"""

    print("Starting final verification of PostgreSQL migration...")

    # Test database connection
    db_success = await test_database_connection()
    if not db_success:
        print("✗ Database connection test failed")
        return False

    # Test API endpoints
    api_success = await test_api_endpoints()
    if not api_success:
        print("✗ API endpoint test failed")
        return False

    # Run unit tests
    tests_success = run_unit_tests()
    if not tests_success:
        print("✗ Unit tests failed")
        return False

    print("\n✓ All verification tests passed!")
    print("✓ PostgreSQL migration is successful")
    print("✓ Application functions correctly with PostgreSQL backend")

    return True

if __name__ == "__main__":
    success = asyncio.run(final_verification())
    exit(0 if success else 1)