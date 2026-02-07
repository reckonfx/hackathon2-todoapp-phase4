# Phase-2: High-Level System Boundaries

## Architecture Overview

The Phase-2 Web-Based Todo Application follows a clear three-tier architecture with well-defined boundaries between each layer.

## Frontend Boundary (Next.js Web UI)

### Scope
- User interface presentation
- Client-side state management
- User interaction handling
- Form validation
- API communication
- Responsive design implementation

### Technologies
- Next.js framework
- React components
- TypeScript
- CSS/styling solutions
- Client-side routing

### External Interfaces
- Backend API endpoints
- Browser storage (cookies, localStorage)
- Better Auth client-side integration

### Internal Boundaries
- Does NOT directly access database
- Does NOT implement business logic
- Does NOT handle authentication tokens directly (delegated to Better Auth)

## Backend Boundary (FastAPI Service)

### Scope
- API endpoint definitions
- Business logic implementation
- Authentication validation
- Database operations
- Request/response handling
- Data validation and sanitization

### Technologies
- FastAPI framework
- Python
- Better Auth integration
- Database connectors
- JWT token handling

### External Interfaces
- Frontend API requests
- PostgreSQL database
- Authentication service (Better Auth)

### Internal Boundaries
- Does NOT contain UI rendering logic
- Does NOT directly manage client-side state
- Does NOT handle browser-specific concerns

## Database Boundary (PostgreSQL via Neon)

### Scope
- Data persistence
- Data integrity enforcement
- Query execution
- Index management
- Transaction handling
- User data isolation

### Technologies
- PostgreSQL database
- Neon cloud database service
- SQL schema definitions
- Connection pooling

### External Interfaces
- Backend API database queries
- Database administration tools

### Internal Boundaries
- Does NOT contain application logic
- Does NOT handle authentication directly
- Does NOT manage user sessions

## Security Boundaries

### Authentication Boundary
- Better Auth handles JWT token generation/verification
- User credential validation
- Session management

### Data Isolation Boundary
- User-specific data access controls
- Query filtering by user ID
- Cross-user data access prevention

## Integration Boundaries

### API Contract Boundary
- Well-defined RESTful endpoints
- Consistent request/response formats
- Versioning strategy
- Error response standardization

### Deployment Boundary
- Separate deployment units for each tier
- Environment-specific configurations
- Secrets management

## Phase-1 Integration Boundary

### Preserved Elements
- Task business logic and operations
- Task data model properties
- Core CRUD operation semantics

### Transformation Boundary
- CLI operations → Web operations
- In-memory persistence → Database persistence
- Single-user → Multi-user
- Terminal UI → Web UI