"""
Authentication service for the Phase-2 Web-Based Todo Application.
Handles user authentication, registration, and token management.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database.deps import get_db
from ..database.connection import settings
from ..models.user import User
from ..database.schemas.user_schema import UserCreate, UserInDB

# Password hashing context with bcrypt
# We handle password truncation manually before hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    # Add tighter control for bcrypt to handle edge cases
    bcrypt__ident="2b",
    bcrypt__rounds=12  # Standard rounds, not too high for Hugging Face environment
)


# -------------------------
# Password utilities
# -------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Process the password the same way as during hashing to ensure consistency
    # First, truncate at character level
    if len(plain_password) > 70:
        plain_password = plain_password[:70]

    # Then ensure byte length is under 70 (leaving buffer for safety)
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 70:
        # Truncate bytes and decode safely
        plain_password = password_bytes[:70].decode('utf-8', errors='ignore')

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password safely for bcrypt (≤72 bytes)."""
    # Validate password is a string
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    # DEBUG: Print what we're receiving to understand the issue
    print(f"DEBUG: Input password type: {type(password)}, length: {len(password)}, bytes: {len(password.encode('utf-8'))}")
    print(f"DEBUG: Input password repr: {repr(password)}")

    # Ensure the password is definitely under the bcrypt limit before passing to bcrypt
    # We'll use the most conservative approach possible
    if len(password) > 70:  # Character length check first
        password = password[:70]

    # Then ensure byte length is under 70 (leaving buffer for safety)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 70:
        # Truncate bytes and decode safely - this is the most reliable approach
        password = password_bytes[:70].decode('utf-8', errors='ignore')

    # Final check
    final_bytes = password.encode('utf-8')
    if len(final_bytes) > 70:
        # Emergency truncation - should not be needed but just in case
        password = final_bytes[:65].decode('utf-8', errors='ignore')

    print(f"DEBUG: Processed password length: {len(password)}, bytes: {len(password.encode('utf-8'))}")

    # Hash with bcrypt - this should now work reliably
    return pwd_context.hash(password)


# -------------------------
# Authentication helpers
# -------------------------

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )


# -------------------------
# Current user resolver
# -------------------------

def get_current_user(
    token: str,
    db: Session = Depends(get_db),
) -> User:
    """Get the current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


# -------------------------
# Registration
# -------------------------

def register_user(db: Session, user_data: UserCreate) -> UserInDB:
    """Register a new user."""

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Hash password safely
    try:
        hashed_password = get_password_hash(user_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # Create user record
    user_name = user_data.name or "User"
    if "use-gemini" not in user_name.lower():
        user_name = f"{user_name} (use-gemini)"

    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_name,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserInDB.from_orm(db_user)
