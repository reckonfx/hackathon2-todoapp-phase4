# Feature Specification: Todo In-Memory Console App

**Feature Branch**: `001-todo-cli-app`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description for a Python CLI todo app with in-memory storage, formatted with Rich.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)
As a user, I want to add tasks with a title and optional description so that I can see them in a formatted list.

**Why this priority**: Core functionality of a todo app. Delivers the primary value of tracking items.

**Independent Test**: Add 3 tasks via the menu and select "View All Tasks" to verify they appear correctly in the Rich table.

**Acceptance Scenarios**:
1. **Given** an empty todo list, **When** I add a task with title "Buy Milk", **Then** the system returns "✓ Task added successfully! ID: 1".
2. **Given** 1 task exists, **When** I select "View All Tasks", **Then** I see a Rich table with 1 row showing "ID: 1" and "Title: Buy Milk".

---

### User Story 2 - Manage Task Status (Priority: P2)
As a user, I want to mark tasks as complete or incomplete so that I can track my progress.

**Why this priority**: Essential for productivity tracking.

**Independent Test**: Mark an existing task as complete and verify the "View All Tasks" list shows the status change.

**Acceptance Scenarios**:
1. **Given** a task with ID 1 is incomplete, **When** I mark ID 1 as complete, **Then** the system returns "✓ Task #1 marked as complete".
2. **Given** a task with ID 1 is complete, **When** I mark ID 1 as complete (toggle), **Then** the status changes back to incomplete.

---

### User Story 3 - Maintenance: Update and Delete (Priority: P3)
As a user, I want to update task details or delete tasks I no longer need.

**Why this priority**: Keeps the list clean and accurate over time.

**Independent Test**: Update a task's title and then delete it; verify it no longer appears in the list.

**Acceptance Scenarios**:
1. **Given** a task with ID 1, **When** I update its title to "New Title", **Then** the list shows the updated title.
2. **Given** a task with ID 1, **When** I delete ID 1, **Then** the list becomes empty and showing "No tasks found".

---

### Edge Cases

- **Duplicate Title**: Adding two tasks with the same title should be allowed but given unique IDs.
- **Invalid ID**: Entering a non-numeric ID or an ID that doesn't exist should display a friendly error message and return to the main menu.
- **Empty Title**: Re-prompts the user up to 3 times before returning to the main menu.
- **Long Input**: Titles > 100 characters or descriptions > 500 characters should be truncated or rejected according to validation rules.

## Phase Context & Constraints *(Phase-I)*

- **Persistence**: In-memory only (stateless/volatile)
- **Interface**: Command-line only (Python 3.13+)
- **Intelligence**: Rule-based (future agent compatibility mandatory)
- **External Specs**: None

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow adding tasks with a required title (max 100 chars) and optional description (max 500 chars).
- **FR-002**: System MUST assign an auto-incrementing unique integer ID starting from 1 to each task.
- **FR-003**: System MUST display all tasks in a formatted Rich table with columns for ID, Status, Title (truncated at 40), and Description.
- **FR-004**: System MUST allow deleting a task by its ID.
- **FR-005**: System MUST allow updating a task's title and description independently.
- **FR-006**: System MUST allow toggling the completion status of a task by its ID.
- **FR-007**: System MUST provide a menu-driven interface using `rich.panel` and handle 'q' for exit.
- **FR-008**: System MUST clear the console screen after each operation and wait for user acknowledgement (Enter) before returning to the menu.

### Key Entities

- **Task**: Represents a single todo item.
  - `id`: Unique identifier (Integer)
  - `title`: Short summary (String, required)
  - `description`: Detailed notes (String, optional)
  - `completed`: Completion state (Boolean)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete adding a task in under 15 seconds.
- **SC-002**: The application handles up to 1,000 in-memory tasks without perceptible UI lag (under 100ms response time).
- **SC-003**: 100% of invalid user inputs (non-integer IDs, empty titles) generate a guided error message instead of crashing.
- **SC-004**: The console UI remains readable on standard terminal sizes (80x24) despite Rich formatting.
- **SC-005**: 100% of core features (Add, Delete, Update, View, Toggle) are accessible via the main menu.
