# Data Model: Todo CLI App

## Task Entity

The core entity representing a todo item.

| Field | Type | Rules |
|-------|------|-------|
| `id` | `int` | Unique, auto-incrementing |
| `title` | `str` | Required, max 100 chars, stripped |
| `description` | `str` | Optional, max 500 chars, stripped |
| `completed` | `bool` | Default: `False` |

## Validation Rules

1. **Title**:
    - Must not be empty after stripping whitespace.
    - Must not exceed 100 characters.
2. **Description**:
    - Must not exceed 500 characters.
3. **ID**:
    - Must exist in the manager's task list for update/delete/toggle operations.
