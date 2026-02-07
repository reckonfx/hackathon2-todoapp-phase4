"""
Quick test to verify password hashing works correctly.
Run this before deploying to Hugging Face.
"""
import sys
sys.path.insert(0, 'src')

from src.services.auth_service import get_password_hash

# Test various passwords
test_passwords = [
    "reckon1234",  # Your password
    "short",
    "a" * 50,
    "a" * 72,
    "a" * 100,  # Exceeds 72 bytes
    "password123",
    "MySecurePassword!@#$%^&*()",
]

print("Testing password hashing...")
print("=" * 60)

for password in test_passwords:
    try:
        hashed = get_password_hash(password)
        print(f"✅ Password '{password[:20]}...' ({len(password)} chars, {len(password.encode('utf-8'))} bytes)")
        print(f"   Hash: {hashed[:50]}...")
    except Exception as e:
        print(f"❌ Password '{password[:20]}...' FAILED: {e}")
    print()

print("=" * 60)
print("If all tests passed, the fix is working! Upload to Hugging Face.")
