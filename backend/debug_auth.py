"""
Debug script to test the authentication flow directly.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import SessionLocal
from src.database.schemas.user_schema import UserCreate
from src.services.auth_service import register_user

def test_registration_directly():
    # Create a test user data
    user_data = UserCreate(email="test@example.com", name="Test User", password="testpass")

    print(f"Attempting to register user with:")
    print(f"  Email: {user_data.email}")
    print(f"  Name: {user_data.name}")
    print(f"  Password: {user_data.password} (length: {len(user_data.password)})")

    # Create a database session
    db = SessionLocal()

    try:
        result = register_user(db, user_data)
        print(f"Registration successful: {result}")
    except Exception as e:
        print(f"Registration failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_registration_directly()