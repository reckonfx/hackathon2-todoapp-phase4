# Quickstart: Backend Stability for Phase-2 Web Todo Application

## Overview

This guide provides instructions for setting up, running, and validating the Phase-2 Web Todo application backend with stability fixes applied.

## Prerequisites

- Python 3.14 or higher
- PostgreSQL database (Neon-compatible)
- pip package manager
- git (for cloning/configuring)

## Setup Instructions

### 1. Clone and Navigate
```bash
cd hackathon-2/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create or update `.env` file in the backend directory:
```env
# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
# For Neon PostgreSQL, use: postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_db

# Authentication settings
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Additional settings
BACKEND_ENV=development
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### 4. Run the Application
```bash
cd backend
uvicorn src.main:app --reload
```

The server should start on `http://localhost:8000`.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login existing user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Tasks
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Validation Steps

### 1. Server Startup
```bash
# From backend directory
uvicorn src.main:app --reload
```
- Server should start without errors
- Should remain stable in reload mode
- Health check available at `GET /` and `GET /health`

### 2. Registration Test
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123",
    "name": "Test User"
  }'
```
- Should return 201 status
- Should create user with properly hashed password
- Should not show any bcrypt errors

### 3. Login Test
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```
- Should return 200 status
- Should return valid JWT token
- Should authenticate successfully

### 4. Long-running Stability Test
- Keep the server running for at least 1 hour
- Perform periodic requests to ensure stability
- Monitor for any crashes or restarts

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Symptom**: Module not found errors during startup
**Solution**: Verify all `__init__.py` files exist in directories and dependencies are installed

#### 2. Database Connection Issues
**Symptom**: Cannot connect to PostgreSQL
**Solution**:
- Verify DATABASE_URL is correctly set
- Ensure PostgreSQL server is running
- Check SSL settings for Neon (sslmode=require)

#### 3. Bcrypt Errors
**Symptom**: Password hashing fails with "password is too long" error
**Solution**: Verify password is under 72 bytes (not characters) before hashing

#### 4. Reload Instability
**Symptom**: Server crashes or restarts unexpectedly during reload
**Solution**: Ensure database initialization happens in lifespan events, not at import time

## Configuration Options

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `BACKEND_ENV`: Environment (development, production)
- `BACKEND_PORT`: Port to run the server on

### SSL Configuration for Neon
The application automatically detects PostgreSQL URLs and applies `sslmode=require` for secure connections.

## Performance Monitoring

### Expected Response Times
- Authentication endpoints: <500ms
- Task endpoints: <200ms
- Health check: <50ms

### Resource Usage
- Memory usage should remain stable during extended operation
- No memory leaks during reload cycles
- Database connections should be properly pooled

## Next Steps

1. **Integration Testing**: Test with frontend application
2. **Security Review**: Validate authentication and authorization
3. **Performance Testing**: Load test under expected traffic
4. **Production Deployment**: Prepare for production environment with proper security settings