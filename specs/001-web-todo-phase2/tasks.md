# Tasks: Phase-2 Web-Based Todo Application

**Input**: Design documents from `/specs/001-web-todo-phase2/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included as per SDD best practices to ensure modularity.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (backend/, frontend/, docker-compose.yml)
- [X] T002 Initialize backend with `uv init` and add FastAPI, SQLAlchemy, Better Auth dependencies
- [X] T003 [P] Initialize frontend with `npx create-next-app` and add required dependencies
- [X] T004 [P] Configure `.python-version` (3.14), `.nvmrc` (Node 20+), and tool configs in `pyproject.toml` and `package.json`
- [X] T005 [P] Create initial `backend/src/__init__.py`, `frontend/src/__init__.ts`, and module docstrings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Constitution Check**:
- [X] T006 [P] Verify Phase-I constraints compliance (no modifications to Phase-1 code)
- [X] T007 [P] Ensure agent-compatible control flow architecture (separation of frontend/backend)

**Foundation Tasks**:
- [X] T008 Create `backend/src/database/connection.py` with PostgreSQL connection setup
- [X] T009 [P] Create `backend/src/models/user.py` and `backend/src/models/task.py` with SQLAlchemy models
- [X] T010 [P] Create `backend/src/database/schemas/user_schema.py` and `backend/src/database/schemas/task_schema.py` with Pydantic models
- [X] T011 [P] Create `backend/src/services/auth_service.py` and `backend/src/services/task_service.py` with business logic
- [X] T012 [P] Create `frontend/src/types/User.ts` and `frontend/src/types/Task.ts` with TypeScript interfaces
- [X] T013 [P] Setup basic `frontend/src/services/api.ts` for API communication
- [X] T014 Setup Alembic for database migrations in `backend/alembic/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentication & Authorization (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, login, and authenticate themselves securely.

**Independent Test**: Register a new user, login successfully, and access protected endpoints.

### Implementation for User Story 1

- [X] T015 [P] [US1] Implement `/api/auth/register` endpoint in `backend/src/api/routes/auth.py`
- [X] T016 [P] [US1] Implement `/api/auth/login` endpoint in `backend/src/api/routes/auth.py`
- [X] T017 [P] [US1] Implement `/api/auth/logout` endpoint in `backend/src/api/routes/auth.py`
- [X] T018 [P] [US1] Implement `/api/auth/me` endpoint in `backend/src/api/routes/auth.py`
- [X] T019 [US1] Implement authentication middleware in `backend/src/api/middleware/auth_middleware.py`
- [X] T020 [P] [US1] Create `frontend/src/components/Auth/Login.tsx` component
- [X] T021 [P] [US1] Create `frontend/src/components/Auth/Register.tsx` component
- [X] T022 [P] [US1] Create protected route wrapper in `frontend/src/components/Layout/MainLayout.tsx`
- [X] T023 [US1] Create login and register pages in `frontend/src/pages/login.tsx` and `frontend/src/pages/register.tsx`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Task Management (Priority: P2)

**Goal**: Enable authenticated users to create, view, update, and delete their tasks.

**Independent Test**: Create a task, view it in the list, update it, and delete it.

### Implementation for User Story 2

- [X] T024 [P] [US2] Implement `/api/tasks` GET endpoint in `backend/src/api/routes/tasks.py`
- [X] T025 [P] [US2] Implement `/api/tasks` POST endpoint in `backend/src/api/routes/tasks.py`
- [X] T026 [P] [US2] Implement `/api/tasks/{task_id}` GET endpoint in `backend/src/api/routes/tasks.py`
- [X] T027 [P] [US2] Implement `/api/tasks/{task_id}` PUT endpoint in `backend/src/api/routes/tasks.py`
- [X] T028 [P] [US2] Implement `/api/tasks/{task_id}` DELETE endpoint in `backend/src/api/routes/tasks.py`
- [X] T029 [P] [US2] Implement `/api/tasks/{task_id}/toggle` PATCH endpoint in `backend/src/api/routes/tasks.py`
- [X] T030 [P] [US2] Create `frontend/src/components/TaskList.tsx` component with task display
- [X] T031 [P] [US2] Create `frontend/src/components/TaskForm.tsx` component for task creation/editing
- [X] T032 [US2] Create dashboard page in `frontend/src/pages/dashboard.tsx` to display tasks
- [X] T033 [US2] Integrate API calls in frontend components using `frontend/src/services/api.ts`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - User Experience & Polish (Priority: P3)

**Goal**: Enhance the user experience with improved UI/UX and additional features.

**Independent Test**: Complete user journey from registration to task management with good UX.

### Implementation for User Story 3

- [X] T034 [P] [US3] Add loading states and error handling in frontend components
- [X] T035 [P] [US3] Implement responsive design and accessibility features
- [X] T036 [P] [US3] Add form validation in frontend components
- [X] T037 [US3] Create home page in `frontend/src/pages/index.tsx` with proper navigation
- [X] T038 [US3] Add toast notifications for user feedback
- [X] T039 [US3] Implement proper error pages and user feedback

**Checkpoint**: All core features are now independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final hardening, testing, and documentation.

- [X] T040 [P] Implement comprehensive backend unit tests in `backend/tests/unit/`
- [X] T041 [P] Implement backend integration tests in `backend/tests/integration/`
- [X] T042 [P] Implement frontend component tests in `frontend/tests/unit/`
- [X] T043 [P] Implement frontend integration tests in `frontend/tests/integration/`
- [X] T044 [P] Implement end-to-end tests in `frontend/tests/e2e/`
- [X] T045 [P] Set up environment configurations for dev, staging, and production
- [X] T046 [P] Create comprehensive `README.md` with setup and usage instructions
- [X] T047 [P] Update `CLAUDE.md` with Phase-2 information
- [X] T048 Final manual validation against all quality gates in spec.md
- [X] T049 Set up Docker Compose configuration for easy local development

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on T001, T002.
- **US1 (Phase 3)**: Depends on Phase 2 completion.
- **US2, US3**: Depend on Phase 2; can be done in parallel or sequence after US1.

### Parallel Opportunities

- **T009, T010, T011**: Backend models and schemas can be created in parallel.
- **T015-T018**: Auth endpoints can be implemented in parallel.
- **T024-T029**: Task endpoints can be implemented in parallel.
- **T020, T021, T022**: Frontend auth components can be created in parallel.
- **T030, T031**: Frontend task components can be created in parallel.

---

## Technical Strategy

- **MVP First**: Complete Phase 1-2 to get authentication working, then add basic task functionality.
- **Incremental**: Add advanced features and polish.
- **Validation**: Each story must be manually verified via the web interface before starting the next.