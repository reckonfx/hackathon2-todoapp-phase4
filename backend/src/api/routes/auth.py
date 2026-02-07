"""
Authentication routes for the Phase-2 Web-Based Todo Application.
Defines API endpoints for user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt
from datetime import timedelta

from ...database.deps import get_sync_db
from ...database.schemas.user_schema import (
    UserRegister, UserLogin, UserInDB, Token, UserPublic
)
from ...services.auth_service import (
    authenticate_user, create_access_token, register_user
)
from ...models.user import User
from ...database.connection import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_sync_db)):
    """Register a new user."""
    try:
        registered_user = register_user(db, user_data)
        return {
            "success": True,
            "user": UserPublic.from_orm(registered_user),
            "message": "Registration successful"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=dict)
def login(user_credentials: UserLogin, db: Session = Depends(get_sync_db)):
    """Authenticate user and return access token."""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "success": True,
        "user": UserPublic.from_orm(user),
        "token": access_token,
        "message": "Login successful"
    }


@router.post("/logout", response_model=dict)
def logout(token: str = Depends(oauth2_scheme)):
    """Logout user (client-side token removal)."""
    # In a real implementation, you might add the token to a blacklist
    return {
        "success": True,
        "message": "Logout successful"
    }


@router.get("/me", response_model=dict)
def get_current_user_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_sync_db)
):
    """Get the current user's profile information."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        user = db.query(User).filter(User.email == username).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return {
            "success": True,
            "user": UserPublic.from_orm(user)
        }
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )