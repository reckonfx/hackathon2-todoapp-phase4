# Specification: Backend Stability for Phase-2 Web Todo Application

## Feature Description

The Phase-2 Web Todo application backend is experiencing stability issues when running in background mode. The system needs to be audited and corrected to ensure reliable operation with `uvicorn src.main:app --reload`, proper authentication functionality, and correct database connectivity.

## Context

- Project: Phase-2 Web Todo Application
- Backend: FastAPI + SQLAlchemy + PostgreSQL (Neon)
- Entry: backend/src/main.py
- Current issues:
  - bcrypt password errors (72 byte issue)
  - registration failing for valid passwords
  - possible double hashing
  - incorrect schema/service separation
  - uvicorn reload instability
  - Neon SSL misconfiguration risk
  - dependency/lifecycle ordering issues

## User Scenarios & Testing

### Scenario 1: Developer starts backend in reload mode
- **Given**: Developer has the Phase-2 backend code
- **When**: Developer runs `uvicorn src.main:app --reload`
- **Then**: Server starts successfully and remains stable in background mode

### Scenario 2: User registers with valid credentials
- **Given**: Backend server is running stably
- **When**: User submits registration with a valid password (including longer passwords)
- **Then**: User account is created successfully with properly hashed password

### Scenario 3: User logs into the application
- **Given**: User has a valid account
- **When**: User submits login credentials
- **Then**: Authentication succeeds and returns valid token

### Scenario 4: Application connects to Neon database
- **Given**: Database credentials are configured
- **When**: Application starts up
- **Then**: Successfully connects to Neon PostgreSQL with proper SSL configuration

## Functional Requirements

### FR-1: Stable Server Startup
- The backend must start without errors when running `uvicorn src.main:app --reload`
- The server process must remain stable in background mode with reload functionality
- All dependencies must be properly imported without module errors
- No lifecycle ordering issues should occur during startup

### FR-2: Correct Password Handling
- Password hashing must occur exactly once using bcrypt
- Passwords must be handled correctly up to 72 bytes as per bcrypt limitations
- No double hashing should occur during registration or authentication
- Schema objects must not perform password hashing or mutation
- Service layer must own all authentication business logic

### FR-3: Proper Schema/Service Separation
- Schemas must only handle data validation and serialization
- Services must handle all business logic including password operations
- Data flow must follow schema → service → model pattern
- No cross-layer contamination between schema and service layers

### FR-4: Neon PostgreSQL Connection
- Database connection must use proper SSL configuration for Neon
- SSL mode must be set to "require" for Neon compatibility
- No channel binding issues should occur
- Connection should be resilient to startup timing issues

### FR-5: Dependency and Import Management
- All imports must resolve correctly without circular dependencies
- FastAPI dependency injection (Depends) must work properly
- No import errors should occur during application startup
- All required modules must be accessible

## Success Criteria

### Measurable Outcomes
- Server starts successfully 100% of the time when running `uvicorn src.main:app --reload`
- Authentication endpoints (register/login) return success responses within 2 seconds
- Database connection establishes within 5 seconds of application startup
- Background processes remain stable for at least 1 hour of continuous operation
- No bcrypt-related errors occur during password processing

### Quality Measures
- Password hashing occurs exactly once per registration
- No schema-layer data mutation occurs
- All FastAPI dependencies resolve without errors
- Neon PostgreSQL SSL connection established correctly
- No import or dependency errors during startup

### Performance Targets
- API response time under 500ms for authentication endpoints
- Database connection pool properly managed with no connection leaks
- Memory usage remains stable during extended operation

## Key Entities

### Authentication System
- **AuthService**: Handles registration, login, token management with proper password hashing
- **Password Handling**: Uses bcrypt with correct 72-byte limit handling
- **User Registration**: Validates input through schemas, processes through services
- **Schema Validation**: Pure validation without data mutation

### Database Connection
- **Neon PostgreSQL**: Cloud database with SSL requirements
- **Connection Configuration**: Proper SSL mode settings for Neon compatibility
- **Database Initialization**: Safe table creation without race conditions

### API Framework
- **FastAPI Application**: Core web framework with proper lifecycle management
- **Dependency Injection**: Correct use of Depends() for database sessions
- **Route Definitions**: Properly structured authentication and task routes

## Assumptions

- The Phase-2 backend code exists in the `backend/` directory structure
- PostgreSQL database credentials are available via environment variables
- The application follows FastAPI best practices for dependency injection
- Current codebase has functionality but needs stability improvements
- Environment variables are properly configured for the target deployment
- Phase-1 code should not be modified during this process

## Dependencies

- Python 3.14 with required packages (FastAPI, SQLAlchemy, passlib, etc.)
- PostgreSQL database (Neon-compatible)
- Environment variables for database connection and authentication
- Proper directory structure with `backend/src/main.py` as entry point

## Scope

### In Scope
- Fixing bcrypt password errors and 72-byte handling
- Correcting double hashing issues
- Fixing schema/service separation violations
- Stabilizing uvicorn reload functionality
- Fixing Neon PostgreSQL SSL configuration
- Resolving import and dependency issues
- Ensuring proper FastAPI lifecycle management
- Maintaining all existing Phase-2 functionality

### Out of Scope
- Modifying Phase-1 code
- Adding new features beyond stability fixes
- Changing core business logic of the todo application
- Modifying frontend code
- Performance optimization beyond stability requirements