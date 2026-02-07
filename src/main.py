"""Main entry point for the Todo application."""

import sys
from ui import (
    console, clear_console, prompt_continue, get_menu_choice,
    display_tasks, prompt_for_task_details, display_success,
    display_error, prompt_for_id
)
from todo_manager import TodoManager
from rich.prompt import Prompt

def main():
    """Application main loop."""
    manager = TodoManager()

    while True:
        try:
            clear_console()
            choice = get_menu_choice()

            if choice == "1":
                title, desc = prompt_for_task_details()
                if title:
                    success, msg, _ = manager.add_task(title, desc)
                    if success:
                        display_success(msg)
                    else:
                        display_error(msg)

            elif choice == "2":
                task_id = prompt_for_id()
                if task_id != -1:
                    success, msg = manager.delete_task(task_id)
                    if success:
                        display_success(msg)
                    else:
                        display_error(msg)
                else:
                    display_error("Invalid ID format")

            elif choice == "3":
                task_id = prompt_for_id()
                if task_id != -1:
                    # Find task to show current details
                    task = next((t for t in manager.get_all_tasks() if t.id == task_id), None)
                    if task:
                        console.print(f"Current Title: {task.title}")
                        console.print(f"Current Description: {task.description}")
                        new_title = Prompt.ask("Enter new title (Enter to skip)").strip()
                        new_desc = Prompt.ask("Enter new description (Enter to skip)").strip()

                        success, msg, _ = manager.update_task(
                            task_id,
                            title=new_title if new_title else None,
                            description=new_desc if new_desc else None
                        )
                        if success:
                            display_success(msg)
                        else:
                            display_error(msg)
                    else:
                        display_error(f"Task with ID {task_id} not found")
                else:
                    display_error("Invalid ID format")

            elif choice == "4":
                display_tasks(manager.get_all_tasks())

            elif choice == "5":
                task_id = prompt_for_id()
                if task_id != -1:
                    success, msg, _ = manager.toggle_complete(task_id)
                    if success:
                        display_success(msg)
                    else:
                        display_error(msg)
                else:
                    display_error("Invalid ID format")

            elif choice == "q":
                console.print("\nThank you for using Todo App. Goodbye!")
                break

            prompt_continue()

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            sys.exit(0)
        except Exception as e:
            display_error(f"An unexpected error occurred: {e}")
            prompt_continue()

if __name__ == "__main__":
    main()
