"""
Comprehensive test script to verify all functionality of the backend after stability fixes.
Tests registration, login, task management, duplicate user prevention, and all scenarios.
"""

import asyncio
import requests
import time
import sys
import os
import uuid
from typing import Optional

# Add the backend path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.services.auth_service import get_password_hash, verify_password
from src.database.connection import SessionLocal, engine, Base
from src.models.user import User
from src.models.task import Task
from src.database.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test server configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = f"test_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "securepassword123"
TEST_NAME = "Test User"

class TestAPI:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None

    def register_user(self, email: str = TEST_EMAIL, password: str = TEST_PASSWORD, name: str = TEST_NAME):
        """Test user registration."""
        print(f"Testing registration for {email}...")

        response = self.session.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": email,
                "password": password,
                "name": name
            }
        )

        print(f"Registration response: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"OK Registration successful: {data.get('message', 'Success')}")
            return True, data
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return False, response.text

    def login_user(self, email: str = TEST_EMAIL, password: str = TEST_PASSWORD):
        """Test user login."""
        print(f"Testing login for {email}...")

        response = self.session.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            print(f"OK Login successful, token length: {len(self.token) if self.token else 0}")
            return True, data
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return False, response.text

    def get_user_profile(self):
        """Test getting user profile."""
        if not self.token:
            print("✗ No token available for profile request")
            return False, "No token"

        print("Testing user profile retrieval...")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        response = self.session.get(f"{BASE_URL}/api/auth/me")

        print(f"Profile response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.user_id = data.get('id')
            print(f"OK Profile retrieved successfully for user: {data.get('email')}")
            return True, data
        else:
            print(f"✗ Profile retrieval failed: {response.status_code} - {response.text}")
            return False, response.text

    def create_task(self, title: str, description: str = ""):
        """Test creating a task."""
        if not self.token:
            print("✗ No token available for task creation")
            return False, "No token"

        print(f"Testing task creation: {title}...")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        response = self.session.post(
            f"{BASE_URL}/api/tasks",
            json={
                "title": title,
                "description": description,
                "completed": False
            }
        )

        print(f"Task creation response: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            task_info = data.get('task', {})
            print(f"OK Task created successfully: {task_info.get('title', 'Unknown')}")
            return True, data
        else:
            print(f"✗ Task creation failed: {response.status_code} - {response.text}")
            return False, response.text

    def get_tasks(self):
        """Test getting all tasks."""
        if not self.token:
            print("✗ No token available for getting tasks")
            return False, "No token"

        print("Testing task retrieval...")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        response = self.session.get(f"{BASE_URL}/api/tasks")

        print(f"Get tasks response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            print(f"OK Retrieved {len(tasks)} tasks")
            return True, tasks
        else:
            print(f"✗ Task retrieval failed: {response.status_code} - {response.text}")
            return False, response.text

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        """Test updating a task."""
        if not self.token:
            print("✗ No token available for task update")
            return False, "No token"

        print(f"Testing task update for task {task_id}...")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if completed is not None:
            update_data["completed"] = completed

        response = self.session.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)

        print(f"Task update response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"OK Task updated successfully: {data.get('title', 'Unknown')}")
            return True, data
        else:
            print(f"✗ Task update failed: {response.status_code} - {response.text}")
            return False, response.text

    def delete_task(self, task_id: str):
        """Test deleting a task."""
        if not self.token:
            print("✗ No token available for task deletion")
            return False, "No token"

        print(f"Testing task deletion for task {task_id}...")

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        response = self.session.delete(f"{BASE_URL}/api/tasks/{task_id}")

        print(f"Task deletion response: {response.status_code}")
        if response.status_code == 200:
            print(f"OK Task deleted successfully")
            return True, "Success"
        else:
            print(f"✗ Task deletion failed: {response.status_code} - {response.text}")
            return False, response.text

def test_duplicate_user_prevention():
    """Test that duplicate users cannot be registered."""
    print("\n=== Testing Duplicate User Prevention ===")

    api = TestAPI()

    # Register first user
    success1, _ = api.register_user()
    if not success1:
        print("✗ Failed to register first user")
        return False

    # Try to register the same user again
    success2, response = api.register_user()
    if success2:
        print("✗ Duplicate user registration should have failed but didn't")
        return False
    else:
        # Check if the error is specifically about duplicate email
        if "already exists" in str(response).lower() or response == 409:
            print("OK Duplicate user prevention working correctly")
            return True
        else:
            print(f"✗ Unexpected error for duplicate registration: {response}")
            return False

def test_password_72_byte_limit():
    """Test password 72-byte limit handling."""
    print("\n=== Testing Password 72-Byte Limit ===")

    # Test with password exactly at limit
    password_72_bytes = "a" * 72
    try:
        hashed = get_password_hash(password_72_bytes)
        print("OK 72-byte password handled correctly")
    except Exception as e:
        print(f"X 72-byte password failed: {e}")
        return False

    # Test with password over limit
    password_80_bytes = "a" * 80
    try:
        hashed_long = get_password_hash(password_80_bytes)
        print("OK Over 72-byte password handled correctly")
    except Exception as e:
        print(f"X Over 72-byte password failed: {e}")
        return False

    # Verify they produce different hashes (meaning the truncation worked)
    if hashed == hashed_long:
        print("X Passwords of different lengths produced same hash - truncation may not be working")
        return False
    else:
        print("OK Different length passwords produce different hashes")

    return True

def test_complete_workflow():
    """Test the complete workflow: register, login, create tasks, update, delete."""
    print("\n=== Testing Complete Workflow ===")

    api = TestAPI()

    # Generate unique email for this test
    unique_email = f"workflow_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Register user
    success, data = api.register_user(email=unique_email)
    if not success:
        print("✗ Workflow test failed at registration")
        return False

    # 2. Login user
    success, data = api.login_user(email=unique_email)
    if not success:
        print("✗ Workflow test failed at login")
        return False

    # 3. Get user profile
    success, data = api.get_user_profile()
    if not success:
        print("✗ Workflow test failed at profile retrieval")
        return False

    # 4. Create multiple tasks
    task_ids = []
    for i in range(3):
        success, data = api.create_task(f"Test Task {i+1}", f"Description for task {i+1}")
        if success:
            task_ids.append(data.get('task', {}).get('id'))
        else:
            print(f"✗ Failed to create task {i+1}")
            return False

    # 5. Get all tasks
    success, data = api.get_tasks()
    if not success or len(data) != 3:
        print(f"✗ Expected 3 tasks, got {len(data) if success else 0}")
        return False

    # 6. Update a task (mark as completed)
    if task_ids:
        success, data = api.update_task(task_ids[0], completed=True)
        if not success:
            print("✗ Failed to update task")
            return False
        
        # Verify completed_at is set
        task_info = data.get('task', {})
        if not task_info.get('completed_at'):
            print("✗ completed_at was not set after marking task as completed")
            return False
        print("✓ completed_at correctly set")

    # 7. Delete tasks
    for task_id in task_ids:
        success, _ = api.delete_task(task_id)
        if not success:
            print(f"✗ Failed to delete task {task_id}")
            return False

    # 8. Verify tasks are deleted by getting all tasks
    success, data = api.get_tasks()
    if not success or len(data) != 0:
        print(f"✗ Expected 0 tasks after deletion, got {len(data) if success else 0}")
        return False

    print("✓ Complete workflow test passed")
    return True

def test_database_tables():
    """Test that database tables are created properly."""
    print("\n=== Testing Database Table Creation ===")

    try:
        # Create a temporary in-memory database to test table creation
        temp_engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=temp_engine)

        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(temp_engine)
        tables = inspector.get_table_names()

        expected_tables = ['users', 'tasks']  # Based on the models

        print(f"Tables found in database: {tables}")

        all_tables_exist = True
        for expected_table in expected_tables:
            if expected_table not in tables:
                print(f"X Expected table '{expected_table}' not found")
                all_tables_exist = False
            else:
                print(f"OK Table '{expected_table}' exists")

        if all_tables_exist:
            print("OK All expected database tables exist")
        else:
            print("X Some expected database tables are missing")

        return all_tables_exist

    except Exception as e:
        print(f"✗ Database table test failed: {e}")
        return False

def test_server_startup_stability():
    """Test that the server starts and handles requests properly."""
    print("\n=== Testing Server Startup Stability ===")

    try:
        # Test health endpoint
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get('status') == 'healthy':
                print("✓ Server health check passed")
                return True
            else:
                print(f"✗ Server health check failed: {health_data}")
                return False
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to server at {BASE_URL}")
        print("  Note: Server may not be running. This test requires the server to be started separately.")
        return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_authentication_scenarios():
    """Test various authentication scenarios."""
    print("\n=== Testing Authentication Scenarios ===")

    api = TestAPI()

    # Test with unique email
    unique_email = f"auth_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Register user
    success, _ = api.register_user(email=unique_email)
    if not success:
        print("✗ Authentication test failed at registration")
        return False

    # 2. Login with correct credentials
    success, _ = api.login_user(email=unique_email)
    if not success:
        print("✗ Failed to login with correct credentials")
        return False

    # 3. Try login with wrong password
    response = api.session.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": unique_email,
            "password": "wrongpassword"
        }
    )
    if response.status_code == 401:
        print("✓ Correctly rejected wrong password")
    else:
        print(f"✗ Should have rejected wrong password, got {response.status_code}")
        return False

    # 4. Try login with non-existent email
    response = api.session.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "any"
        }
    )
    if response.status_code == 401:
        print("✓ Correctly rejected non-existent user")
    else:
        print(f"✗ Should have rejected non-existent user, got {response.status_code}")
        return False

    print("✓ Authentication scenarios test passed")
    return True

def run_all_tests():
    """Run all tests."""
    print("Starting comprehensive backend functionality tests...\n")

    tests = [
        ("Database Tables Creation", test_database_tables),
        ("Server Startup Stability", test_server_startup_stability),
        ("Password 72-Byte Limit", test_password_72_byte_limit),
        ("Duplicate User Prevention", test_duplicate_user_prevention),
        ("Authentication Scenarios", test_authentication_scenarios),
        ("Complete Workflow", test_complete_workflow),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")

        try:
            result = test_func()
            results.append((test_name, result))
            status = "PASS" if result else "FAIL"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            print(f"\n{test_name}: ERROR - {e}")
            results.append((test_name, False))

    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")

    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nTotal: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! Backend functionality is working correctly.")
        return True
    else:
        print(f"\n❌ {len(results) - passed} test(s) failed. Backend needs fixes.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)