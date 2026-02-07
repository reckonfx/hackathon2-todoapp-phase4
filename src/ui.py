"""Command-line interface utilities using the rich library."""

import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

def clear_console():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_continue():
    """Wait for user to press Enter to continue."""
    Confirm.ask("\nPress Enter to continue", show_choices=False, default=True)

def display_error(message: str):
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")

def display_success(message: str):
    """Display a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")

from rich.table import Table

def display_tasks(tasks: list):
    """Display tasks in a formatted Rich table."""
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Todo Tasks")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="white")

    for task in tasks:
        status = "[green]✓[/green]" if task.completed else "[red] [/red]"
        title = task.title if len(task.title) <= 40 else f"{task.title[:37]}..."
        table.add_row(str(task.id), status, title, task.description)

    console.print(table)
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    console.print(f"\nSummary: Total: {total} ({completed} completed, {total - completed} incomplete)")

def get_menu_choice() -> str:
    """Prompt for and return the user's menu choice."""
    console.print(Panel.fit(
        "1. Add Task\n"
        "2. Delete Task\n"
        "3. Update Task\n"
        "4. View All Tasks\n"
        "5. Mark Complete\n"
        "q. Exit",
        title="Todo Application"
    ))
    return Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "q"], default="4")

def prompt_for_task_details() -> tuple[str, str]:
    """Prompt for title and description."""
    title = ""
    for _ in range(3):
        title = Prompt.ask("Enter task title").strip()
        if title:
            break
        display_error("Title is required.")

    if not title:
        return "", ""

    description = Prompt.ask("Enter task description (optional)").strip()
    return title, description

def prompt_for_id(prompt_text: str = "Enter task ID") -> int:
    """Prompt for and return a task ID."""
    val = Prompt.ask(prompt_text)
    try:
        return int(val)
    except ValueError:
        return -1
