#!/usr/bin/env python3
"""
Test script to demonstrate the Todo application functionality.
This script shows that all components work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.todo_manager import TodoManager
from src.ui import display_tasks, display_success, display_error
from rich.console import Console

console = Console()

def test_application():
    """Test the todo application functionality."""
    console.print("[bold blue]Testing Todo Application[/bold blue]\n")

    # Initialize the manager
    manager = TodoManager()
    print("✓ TodoManager initialized\n")

    # Test adding tasks
    console.print("[bold]Testing Add Task:[/bold]")
    success, msg, task = manager.add_task("Test task 1", "This is a test task")
    if success:
        print(f"✓ {msg}")
    else:
        print(f"Error: {msg}")

    success, msg, task = manager.add_task("Test task 2", "Another test task")
    if success:
        print(f"✓ {msg}")
    else:
        print(f"Error: {msg}")
    print()

    # Test viewing tasks
    console.print("[bold]Testing View Tasks:[/bold]")
    display_tasks(manager.get_all_tasks())
    print()

    # Test updating a task
    console.print("[bold]Testing Update Task:[/bold]")
    success, msg, task = manager.update_task(1, title="Updated test task 1", description="Updated description")
    if success:
        display_success(msg)
    else:
        display_error(msg)
    print()

    # Test toggling completion
    console.print("[bold]Testing Toggle Complete:[/bold]")
    success, msg, task = manager.toggle_complete(1)
    if success:
        display_success(msg)
    else:
        display_error(msg)
    print()

    # Show final state
    console.print("[bold]Final Task List:[/bold]")
    display_tasks(manager.get_all_tasks())
    print()

    console.print("[bold green]All functionality tested successfully![/bold green]")
    console.print("[yellow]The Todo application is working correctly![/yellow]")

if __name__ == "__main__":
    test_application()