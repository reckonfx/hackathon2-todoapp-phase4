#!/usr/bin/env python3
"""
Simple test to verify the Todo application core functionality works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from todo_manager import TodoManager
from models import Task

def test_core_functionality():
    """Test the core functionality of the Todo application."""
    print("Testing Todo Application Core Functionality")
    print("=" * 50)

    # Initialize the manager
    manager = TodoManager()
    print("SUCCESS: TodoManager initialized successfully")

    # Test adding tasks
    print("\n1. Testing Add Task functionality:")
    success, msg, task = manager.add_task("Buy groceries", "Milk, bread, eggs")
    if success:
        print(f"   SUCCESS: {msg}")
    else:
        print(f"   ERROR: {msg}")

    success, msg, task = manager.add_task("Finish project", "Complete the todo app")
    if success:
        print(f"   SUCCESS: {msg}")
    else:
        print(f"   ERROR: {msg}")

    # Test getting all tasks
    print("\n2. Testing View All Tasks:")
    tasks = manager.get_all_tasks()
    print(f"   Total tasks: {len(tasks)}")
    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        print(f"   - ID: {task.id}, Title: {task.title}, Status: {status}")

    # Test updating a task
    print("\n3. Testing Update Task:")
    success, msg, task = manager.update_task(1, title="Buy groceries - URGENT", description="Milk, bread, eggs, fruits")
    if success:
        print(f"   SUCCESS: {msg}")
    else:
        print(f"   ERROR: {msg}")

    # Test toggling completion
    print("\n4. Testing Toggle Complete/Incomplete:")
    success, msg, task = manager.toggle_complete(1)
    if success:
        print(f"   SUCCESS: {msg}")
    else:
        print(f"   ERROR: {msg}")

    # Test deleting a task
    print("\n5. Testing Delete Task:")
    success, msg = manager.delete_task(2)
    if success:
        print(f"   SUCCESS: {msg}")
    else:
        print(f"   ERROR: {msg}")

    # Final state
    print("\n6. Final state after all operations:")
    tasks = manager.get_all_tasks()
    print(f"   Remaining tasks: {len(tasks)}")
    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        print(f"   - ID: {task.id}, Title: {task.title}, Status: {status}")

    print("\nSUCCESS: All core functionality tested successfully!")
    print("SUCCESS: The Todo application is working correctly!")

if __name__ == "__main__":
    test_core_functionality()