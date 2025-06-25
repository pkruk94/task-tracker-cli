import argparse
from task_manager import (
    add_task, update_task, delete_task,
    mark_task_done, mark_task_in_progress,
    list_all_tasks, list_all_tasks_filtered, TaskStatus
)

TASK_ID = "Task ID"

def print_task(task):
    print(
        f"[{task['id']}] {task['description']}\n"
        f"    Status: {task['status']}\n"
        f"    Created: {task['createdAt']}\n"
        f"    Updated: {task.get('updatedAt', '-')}"
    )

def print_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print_task(task)
            print("-" * 40)

def main():
    parser = argparse.ArgumentParser(prog="task-cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")

    # Update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help=TASK_ID)
    update_parser.add_argument("description", type=str, help="New description")

    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help=TASK_ID)

    # Mark in progress
    mip_parser = subparsers.add_parser("mark-in-progress", help="Mark task as in progress")
    mip_parser.add_argument("id", type=int, help=TASK_ID)

    # Mark done
    md_parser = subparsers.add_parser("mark-done", help="Mark task as done")
    md_parser.add_argument("id", type=int, help=TASK_ID)

    # List
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("status", nargs="?", choices=["todo", "done", "in-progress"], help="Filter by status")

    args = parser.parse_args()

    try:
        if args.command == "add":
            task_id = add_task(args.description)
            print(f"Task added successfully (ID: {task_id})")
        elif args.command == "update":
            update_task(args.id, args.description)
            print("Task updated successfully")
        elif args.command == "delete":
            delete_task(args.id)
            print("Task deleted successfully")
        elif args.command == "mark-in-progress":
            mark_task_in_progress(args.id)
            print("Task marked as in progress")
        elif args.command == "mark-done":
            mark_task_done(args.id)
            print("Task marked as done")
        elif args.command == "list":
            if args.status:
                status = TaskStatus(args.status.replace("-", "_"))
                tasks = list_all_tasks_filtered(status)
            else:
                tasks = list_all_tasks()
            print_tasks(tasks)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()