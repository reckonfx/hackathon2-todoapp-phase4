"""
Simple test script to verify the authentication functions work properly.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.auth_service import get_password_hash, verify_password

def test_password_functions():
    test_passwords = ["short", "testpass", "password123", "a" * 50, "a" * 70, "a" * 80]

    for password in test_passwords:
        print(f"Testing password length: {len(password)}")
        try:
            hashed = get_password_hash(password)
            print(f"  Successfully hashed: {password[:10]}{'...' if len(password) > 10 else ''}")

            verified = verify_password(password, hashed)
            print(f"  Verification: {'PASS' if verified else 'FAIL'}")
        except Exception as e:
            print(f"  ERROR: {e}")
        print()

if __name__ == "__main__":
    test_password_functions()