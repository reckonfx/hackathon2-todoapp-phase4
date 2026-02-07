# Tasks: Todo In-Memory Console App

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included as per SDD best practices to ensure modularity.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (src/, tests/, specs/)
- [X] T002 Initialize Python project with `uv init` and add `rich` dependency
- [X] T003 [P] Configure `.python-version` (3.13) and tool configs in `pyproject.toml`
- [X] T004 [P] Create `src/__init__.py` and module docstrings for all source files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Constitution Check**:
- [X] T005 [P] Verify Phase-I constraints in environment (Python 3.13+, No DB libs)
- [X] T006 [P] Ensure agent-compatible control flow architecture (Manager-UI separation)

**Foundation Tasks**:
- [X] T007 Create `src/models.py` with Task dataclass definition
- [X] T008 [P] Setup logging configuration in `src/main.py`
- [X] T009 [P] Implement `clear_console()` and `prompt_continue()` in `src/ui.py`
- [X] T010 [P] Setup base `tests/` structure (unit, integration)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks and see them in a formatted Rich table.

**Independent Test**: Add tasks via CLI menu and verify Table display.

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement `add_task` in `src/todo_manager.py` (contract: manager.md)
- [X] T012 [P] [US1] Implement `get_all_tasks` in `src/todo_manager.py`
- [X] T013 [P] [US1] Implement `display_tasks(tasks)` using `rich.table` in `src/ui.py`
- [X] T014 [US1] Implement "Add Task" and "View All Tasks" handlers in `src/main.py`
- [X] T015 [US1] Add input validation for title and description in `src/ui.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Manage Task Status (Priority: P2)

**Goal**: Enable users to toggle task completion status.

**Independent Test**: Toggle a task ID and verify status column change in Table.

### Implementation for User Story 2

- [X] T016 [P] [US2] Implement `toggle_complete(task_id)` in `src/todo_manager.py`
- [X] T017 [P] [US2] Implement `prompt_for_task_id()` in `src/ui.py`
- [X] T018 [US2] Implement "Mark Complete" toggle handler in `src/main.py`
- [X] T019 [US2] Add status success/error messages in `src/ui.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Maintenance: Update and Delete (Priority: P3)

**Goal**: Allow users to modify task details or remove them.

**Independent Test**: Update a title and then delete the task; verify table is updated correctly.

### Implementation for User Story 3

- [X] T020 [P] [US3] Implement `update_task` in `src/todo_manager.py`
- [X] T021 [P] [US3] Implement `delete_task` in `src/todo_manager.py`
- [X] T022 [P] [US3] Implement `prompt_for_update_fields()` in `src/ui.py`
- [X] T023 [US3] Implement "Update Task" and "Delete Task" handlers in `src/main.py`

**Checkpoint**: All core features are now independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final hardening and documentation.

- [X] T024 [P] Implement graceful Ctrl+C (KeyboardInterrupt) in `src/main.py`
- [X] T025 [P] Create `README.md` with setup and usage instructions
- [X] T026 [P] Create `CLAUDE.md` documentation
- [X] T027 Final manual validation against all SC-00X criteria in spec.md
- [X] T028 Run `quickstart.md` validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on T001, T002.
- **US1 (Phase 3)**: Depends on Phase 2 completion.
- **US2, US3**: Depend on Phase 2; can be done in parallel or sequence after US1.

### Parallel Opportunities

- **T011, T012, T013**: Code can be written in parallel since they touch different files.
- **T016, T017**: Can be written in parallel for US2.
- **T020, T021, T022**: Can be written in parallel for US3.

---

## Technical Strategy

- **MVP First**: Complete Phase 1-3 to get a working "Add/View" app.
- **Incremental**: Add Toggle, then Update/Delete.
- **Validation**: Each story must be manually verified via the CLI before starting the next.
