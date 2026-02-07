# Research: Todo CLI App Best Practices

## Modular UI with Rich

- **Decision**: Use a dedicated `src/ui.py` module for all terminal interactions.
- **Rationale**: Separation of concerns prevents business logic (`todo_manager.py`) from becoming coupled to display logic.
- **Patterns**:
    - Use `rich.console.Console` for printing.
    - Use `rich.table.Table` for list view.
    - Use `rich.panel.Panel` for menus.
    - Clear screen using `os.system('cls' if os.name == 'nt' else 'clear')`.

## Python 3.13 Dataclasses

- **Decision**: Use `dataclasses.dataclass` with `kw_only=True`.
- **Rationale**: Provides a clean, type-hinted data model with automatic constructor generation. `kw_only` prevents accidental field mismatches.
- **Validation**: Use `__post_init__` for field validation (e.g., title length).

## Main Loop and Ctrl+C

- **Decision**: Wrap the main loop in a `try...except KeyboardInterrupt` block in `main.py`.
- **Rationale**: Ensures graceful shutdown and prevents ugly tracebacks when a user exits.

## Package Management with UV

- **Decision**: Use `uv` for environment and dependency management.
- **Rationale**: High-performance replacement for `pip` and `venv`.
