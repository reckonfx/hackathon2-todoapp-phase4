# Action Plan: Neon PostgreSQL Migration

**Feature**: Migrate Backend Database from SQLite to Neon PostgreSQL
**Created**: 2026-01-15
**Input**: specs/001-db-migration/spec.md, specs/001-db-migration/plan.md

**Overview**: This task plan migrates the backend database layer from SQLite to Neon PostgreSQL, ensuring all database operations (create, read, update, delete, merge, migrations) work correctly and are fully tested.

## Dependencies & Parallelization

**User Story Priority Order**: US1 (P1) → US2 (P2) → US3 (P3)

**Parallelizable Tasks**: Tasks marked [P] can be executed in parallel when they operate on different files/modules without dependencies on other incomplete tasks.

**Cross-Story Dependencies**: US2 depends on US1 (PostgreSQL connection must be established before migration can occur).

## Implementation Strategy

**MVP Scope**: Complete US1 (Access Application with PostgreSQL Backend) to establish core PostgreSQL connectivity.

**Delivery Approach**: Incremental delivery starting with database connectivity, followed by migration tools, and finally production configuration.

---

## Phase 1: Setup & Environment Configuration

Goal: Establish development environment and update dependencies for PostgreSQL migration

- [x] T001 Update backend/pyproject.toml to add asyncpg dependency
- [x] T002 [P] Update backend/pyproject.toml to remove or adjust SQLite-specific dependencies
- [x] T003 Create backup of existing SQLite database (backend/todo_app_local.db.bak)
- [x] T004 [P] Update backend/.env to configure PostgreSQL connection string format
- [x] T005 [P] Install new dependencies with poetry install

## Phase 2: Foundational Database Infrastructure

Goal: Establish async PostgreSQL database connection layer and replace SQLite implementation

- [x] T006 [P] Update backend/src/database/connection.py to use create_async_engine
- [x] T007 [P] Update backend/src/database/connection.py to use AsyncSession
- [x] T008 Create backend/src/database/deps.py for async database dependency injection
- [x] T009 [P] Update backend/src/database/connection.py to remove SQLite-specific logic
- [x] T010 [P] Configure connection pooling parameters for PostgreSQL in connection.py
- [x] T011 Update backend/src/database/connection.py to handle PostgreSQL-specific connect_args
- [x] T012 [P] Create test to verify PostgreSQL connection works

## Phase 3: [US1] Access Application with PostgreSQL Backend

Goal: Enable users to use the Todo application with PostgreSQL backend without noticing functionality differences

**Independent Test**: Application successfully connects to PostgreSQL and performs all CRUD operations with identical behavior to SQLite version.

- [x] T013 [P] [US1] Update backend/src/models/todo.py for PostgreSQL compatibility (datetime timezone, boolean fields)
- [x] T014 [P] [US1] Update backend/src/models/__init__.py to import PostgreSQL-compatible models
- [x] T015 [US1] Update backend/src/services/todo_service.py to use async database operations
- [x] T016 [P] [US1] Update backend/src/api/routes/todos.py to inject async database sessions
- [x] T017 [P] [US1] Update backend/src/main.py to use async database initialization
- [ ] T018 [US1] Create integration test to verify all CRUD operations work with PostgreSQL
- [ ] T019 [P] [US1] Update any model validations for PostgreSQL-specific data types
- [ ] T020 [US1] Test application startup with PostgreSQL connection

## Phase 4: [US2] Database Migration Process

Goal: Enable developers to migrate from existing SQLite database to Neon PostgreSQL using automated migration scripts

**Independent Test**: Migration process successfully transfers sample dataset from SQLite to PostgreSQL with validated data integrity.

- [x] T021 [P] [US2] Configure Alembic for PostgreSQL by updating backend/alembic.ini
- [x] T022 [P] [US2] Update backend/alembic/env.py to work with async PostgreSQL connections
- [x] T023 [US2] Generate initial migration using alembic revision --autogenerate
- [x] T024 [P] [US2] Update alembic/env.py to use async database connection
- [x] T025 [US2] Create data migration script to transfer SQLite data to PostgreSQL
- [x] T026 [P] [US2] Create validation script to verify data integrity after migration
- [ ] T027 [US2] Test migration process on sample data
- [ ] T028 [P] [US2] Document migration procedure in quickstart guide

## Phase 5: [US3] Production-Ready Configuration

Goal: Support different environments (development, staging, production) with appropriate database configurations

**Independent Test**: Different environment variables properly configure database connection behaviors.

- [ ] T029 [P] [US3] Update Settings class in backend/src/database/connection.py to support environment-specific configs
- [ ] T030 [P] [US3] Add connection pooling configuration options to Settings
- [ ] T031 [US3] Implement environment-specific database URL configuration
- [ ] T032 [P] [US3] Add SSL configuration options for production PostgreSQL connections
- [x] T033 [US3] Create environment-specific .env files (development, staging, production)
- [ ] T034 [P] [US3] Update documentation with environment configuration instructions

## Phase 6: Testing & Validation

Goal: Ensure all functionality works correctly with PostgreSQL backend

- [ ] T035 [P] Update existing tests to work with PostgreSQL instead of SQLite
- [ ] T036 [P] Create database-specific tests for PostgreSQL features
- [ ] T037 Run all tests to verify functionality is preserved
- [ ] T038 [P] Create performance comparison tests between SQLite and PostgreSQL
- [ ] T039 Verify all existing API tests pass with PostgreSQL backend
- [ ] T040 [P] Test error handling for database connection failures

## Phase 7: Polish & Cross-Cutting Concerns

Goal: Complete the migration with documentation and cleanup

- [x] T041 Update README with PostgreSQL setup instructions
- [ ] T042 [P] Remove any remaining SQLite-specific code or comments
- [x] T043 Document PostgreSQL-specific considerations in developer documentation
- [x] T044 [P] Update docker-compose.yml if needed for PostgreSQL environment
- [x] T045 Perform final testing of complete application with PostgreSQL
- [ ] T046 [P] Update CI/CD configuration if applicable for PostgreSQL testing
- [ ] T047 Verify all acceptance criteria from spec are met

---

## Parallel Execution Examples

**Example 1**: Tasks T006, T007, T008, T009 can run in parallel as they modify different aspects of the database layer
**Example 2**: Tasks T013, T014, T015 can run in parallel as they update different modules for US1
**Example 3**: Tasks T021, T022, T024 can run in parallel as they configure Alembic for PostgreSQL