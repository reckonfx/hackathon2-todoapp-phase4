# Phase-2 Specification – Web-Based Todo Application

## Status
**Active Phase**  
Phase-1 is **COMPLETE, FROZEN, and READ-ONLY**

---

## Phase Relationship
This phase extends **Phase-1: CLI Todo Application**.

- Phase-1 functionality must be preserved
- Phase-1 code and specs MUST NOT be modified
- Phase-1 serves as a functional and behavioral reference only

---

## Purpose
To build a modern, secure, full-stack web-based Todo application using a
Next.js frontend, FastAPI backend, Better Auth for authentication, and
PostgreSQL (Neon) for persistence.

---

## In Scope

- Web-based user interface
- User authentication and authorization
- Persistent task storage
- RESTful API
- Automated testing across frontend, backend, database, and integrations

---

## Out of Scope

- AI features
- Mobile applications
- Background workers / cron jobs
- Multi-tenant organizations

---

## Core Features

### Authentication & Authorization
- User registration (email + password)
- Secure login and logout
- JWT-based authentication using Better Auth
- Password reset and session management

### Task Management
- Create tasks
- View task list
- Update tasks
- Delete tasks
- Tasks must be scoped per authenticated user

---

## High-Level Architecture

### Frontend
- Next.js (App Router)
- Modern, clean, and accessible UI
- Auth-aware routing and protected pages

### Backend
- FastAPI
- RESTful endpoints
- Authentication middleware
- Business logic layer

### Database
- PostgreSQL (Neon)
- Relational schema for users and tasks
- Accessed ONLY via backend

---

## System Boundaries

- Frontend communicates with backend ONLY via API
- Backend owns all validation and authorization logic
- Database is never accessed directly by frontend

---

## Testing Strategy

### Backend
- Unit tests for services and routes
- Authentication and authorization tests
- Database integration tests

### Frontend
- Component tests
- Authentication flow tests
- Protected route tests

### Integration
- API + DB integration tests
- End-to-end smoke tests for critical user flows

---

## Quality Gates

### Functional
- All Phase-1 features are available via web UI
- Authenticated users cannot access others’ tasks

### Technical
- Test coverage for critical paths
- Stable database connections
- Clean separation of concerns

### Security
- Auth required for all task operations
- Secure token handling and storage

---

## Success Criteria

- Users can register, login, and manage tasks successfully
- Tasks persist across sessions
- All tests pass before phase completion
