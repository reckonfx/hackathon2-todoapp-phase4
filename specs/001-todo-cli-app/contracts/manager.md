# TodoManager Interface Contract

The `TodoManager` acts as the service layer for task management.

## Methods

### `add_task(title: str, description: str = "") -> tuple[bool, str, Task|None]`
- **Input**: Validated title and description.
- **Output**: `(success, message, created_task)`.

### `delete_task(task_id: int) -> tuple[bool, str]`
- **Input**: Task ID.
- **Output**: `(success, message)`.

### `update_task(task_id: int, title: str|None = None, description: str|None = None) -> tuple[bool, str, Task|None]`
- **Input**: Task ID and optional new fields.
- **Output**: `(success, message, updated_task)`.

### `get_all_tasks() -> list[Task]`
- **Output**: List of all current tasks.

### `toggle_complete(task_id: int) -> tuple[bool, str, Task|None]`
- **Input**: Task ID.
- **Output**: `(success, message, modified_task)`.
