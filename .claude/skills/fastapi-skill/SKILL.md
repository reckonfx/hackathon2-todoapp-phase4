---
name: fastapi-skill
description: Helps Claude assist developers with FastAPI projects, including writing routes, models, schemas, authentication, validation, and implementing best practices with security-focused guidance.
---
# FastAPI-Skill

This skill enables Claude to effectively assist developers working with FastAPI, providing expert guidance on building robust, secure, and efficient web applications using the FastAPI framework.

## Purpose

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. This skill provides Claude with the necessary knowledge to:
- Generate well-structured FastAPI route code based on requirements
- Suggest appropriate Pydantic models and database schemas
- Implement authentication and validation best practices
- Debug common FastAPI errors and provide improvement recommendations
- Follow security best practices and FastAPI conventions

## Instructions for Handling FastAPI Projects

### 1. Route Generation
When generating FastAPI routes:
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH) based on the operation
- Implement proper status codes (200, 201, 204, 400, 401, 403, 404, 422, 500)
- Apply path parameters and query parameters correctly
- Use dependency injection for authentication, database sessions, and other reusable components
- Include proper response models using Pydantic classes

### 2. Model and Schema Creation
When creating Pydantic models and database schemas:
- Follow the Create, Read, Update, Delete (CRUD) pattern with separate models for different operations
- Use appropriate field validations and constraints
- Implement proper relationships between models
- Separate input models (for creation) from output models (for responses)
- Apply security best practices like excluding sensitive fields from responses

### 3. Authentication and Validation
When implementing security features:
- Use OAuth2 with Password Flow or JWT tokens for authentication
- Implement proper password hashing with bcrypt
- Validate user permissions and roles appropriately
- Apply rate limiting and input sanitization
- Include proper error handling and logging

### 4. Error Debugging and Recommendations
When debugging or improving code:
- Identify common FastAPI pitfalls like incorrect dependency injection
- Recommend performance optimizations
- Suggest security improvements
- Point out missing validation or error handling
- Propose code organization improvements

## Examples

### Example 1: Basic CRUD Endpoint
**Input:**
```
Create a FastAPI endpoint to manage users. Need endpoints to create, read, update, and delete users. Users should have id, name, email, and age fields. Include proper validation for email format and age range.
```

**Expected Output:**
```python
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Pydantic Models
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# Routes
@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Implementation here
    pass

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # Implementation here
    pass

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    # Implementation here
    pass

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    # Implementation here
    pass
```

### Example 2: Authentication Implementation
**Input:**
```
I need to add JWT-based authentication to protect certain endpoints. Users should authenticate with username and password, and protected endpoints should verify the token.
```

**Expected Output:**
```python
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = "your-secret-key"  # In production, use environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    # Verify user exists in database here
    return token_data

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserLogin):
    # Verify user credentials here
    # user = authenticate_user(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated!"}
```

### Example 3: Database Integration with SQLAlchemy
**Input:**
```
I want to integrate SQLAlchemy with my FastAPI application to connect to a PostgreSQL database. Show me how to set up the database connection, define a model, and create a dependency for database sessions.
```

**Expected Output:**
```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends, HTTPException
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer)
    is_active = Column(Boolean, default=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route using database dependency
@app.post("/items/")
def create_item(item_data: dict, db: Session = Depends(get_db)):
    # Create item in database
    db_item = Item(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

## Guidelines for Using This Skill

### When to Activate
- When asked to generate FastAPI route code
- When assisting with Pydantic model creation
- When implementing authentication systems
- When debugging FastAPI applications
- When optimizing FastAPI performance
- When addressing security concerns in FastAPI apps

### Best Practices
- Always follow FastAPI's dependency injection patterns
- Use Pydantic for request/response validation
- Implement proper error handling with HTTPException
- Follow REST API conventions for endpoint design
- Apply security best practices (input validation, authentication, etc.)
- Use environment variables for sensitive configuration
- Include proper type hints and documentation

### Response Structure
1. **Analysis**: Understand the requirement and identify the FastAPI components needed
2. **Implementation**: Provide well-structured, commented code
3. **Security Considerations**: Highlight any security implications
4. **Best Practices**: Mention relevant FastAPI conventions
5. **Testing Suggestions**: Recommend how to test the implementation

### Quality Checks
- Does the code follow FastAPI conventions?
- Are proper status codes used?
- Is input validation implemented correctly?
- Are security best practices followed?
- Is the code well-documented and readable?
- Are dependencies properly managed?

Use this skill whenever FastAPI development assistance is needed, ensuring secure, efficient, and maintainable code is produced that follows industry best practices.
