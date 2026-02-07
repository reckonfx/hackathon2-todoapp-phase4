# Todo App

A Python CLI todo application built following Spec-Driven Development (SDD) principles.

## Features

- **Add Task**: Create tasks with titles and optional descriptions.
- **View All Tasks**: See your tasks in a beautifully formatted terminal table.
- **Mark Complete**: Toggle the status of your tasks.
- **Update Task**: Modify existing task details.
- **Delete Task**: Remove tasks you no longer need.
- **Interactive CLI**: Easy-to-use menu system with `rich` formatting.

## Installation

1. **Install uv** (High-performance Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

## Usage

Run the application using `uv`:

```bash
uv run src/main.py
```

### Menu Options

- `1`: Add a new task (Prompt for title and optional description).
- `2`: Delete a task by its ID.
- `3`: Update an existing task's title/description.
- `4`: View all tasks in a table summary.
- `5`: Toggle a task's completion status.
- `q`: Exit the application.

## Development

### Prerequisites

- Python 3.13+
- uv

### Running Tests

```bash
uv run pytest
```

### Project Structure (Phase-I)

- `src/models.py`: Task data model.
- `src/todo_manager.py`: Business logic and state management.
- `src/ui.py`: CLI display and input components.
- `src/main.py`: App entry point and loop.
