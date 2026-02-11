# task_tracker/cli.py

import argparse
import json
import os
from datetime import datetime
from task_tracker.commands import add_task, list_tasks, done_task

FILE = "tasks.json"

# Load Tasks from JSON


def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def current_time():
    return datetime.now().isoformat(timespec="seconds")

# Core Functions


def add_task(title):
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!")


def update_status(task_id, new_status):
    tasks = load_tasks()

    valid_statuses = ["todo", "in-progress", "done"]

    if new_status not in valid_statuses:
        print("Invalid status. Use: todo, in-progress, done")
        return


def update_task(task_id, new_title=None, completed=None):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if new_title:
                task["title"] = new_title
            if completed is not None:
                task["completed"] = completed

            save_tasks(tasks)
            print("Task updated successfully!")
            return

    print("Task not found.")


def delete_tasks(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) == len(new_tasks):
        print("Task not found.")
        return

    save_tasks(new_tasks)
    print("Task deleted succesffuly!")


def list_done_tasks():
    tasks = load_tasks()

    done_tasks = [task for task in tasks if task["status"] == "done"]

    if not done_tasks:
        print("No completed tasks found.")
        return

    print("\nCompleted Tasks:\n" + "-" * 30)

    for task in done_tasks:
        print(f"{task['id']}. ✅ {task['title']}")


def list_not_done_tasks():
    tasks = load_tasks()

    not_done_tasks = [task for task in tasks if task["status"] != "done"]

    if not not_done_tasks:
        print("No pending tasks found.")
        return

    print("\nPending Tasks:\n" + "-" * 30)

    for task in not_done_tasks:
        print(f"{task['id']}. [{task['status']}] {task['title']}")


def list_in_progress_tasks():
    tasks = load_tasks()

    in_progress_tasks = [
        task for task in tasks if task("status") == "in-progress"
    ]

    if not in_progress_tasks:
        print("No tasks in progress.")
        return

    print("\nIn-Progress Tasks:\n" + "-" * 30)

    for task in in_progress_tasks:
        print(f"{task['id']}. ⏳ {task['task']}")

# List All Tasks Function


def list_tasks(task_id):
    tasks = load_tasks()

    exclude = "done"

    if status:
        tasks = [task for task in tasks if task["status"] == status]

    if exclude:
        tasks = [task for task in tasks if task["status"] != exclude]

    if not tasks:
        print("No tasks found.")
        return

    print("\nYour Tasks:\n" + "-" * 30)

    for task in tasks:
        status = "✓" if task["completed"] else "X"
        print(f"ID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Status: {task['status']}")
        print("-" * 30)

# CLI Setup


def main():
    parser = argparse.ArgumentParser(
        prog="task",
        description="Simple CLI task tracker"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add = subparsers.add_parser("add", help="Add a new task")
    add.add_argument("title", help="Task description")

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser = subparsers.add_parser("list")
    update_parser = subparsers.add_parser("pending")
    update_parser = subparsers.add_parser("in-progress")
    update_parser.add_argument("--status", help="Filter by status")
    update_parser.add_argument("--exclude", help="Exclude a status")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("status", help="todo | in-progess | done")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--complete", action="store_true")
    update_parser.add_argument("--incomplete", action="store_true")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # done
    done = subparsers.add_parser("done", help="Mark a task as done")
    done.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    # Command Handling

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "status":
        update_status(args.id, args.status)
    elif args.command == "done":
        done_task(args.id)
    elif args.command == "pending":
        list_not_done_tasks(args.id)
    elif args.command == "exclude":
        list_tasks(args.id)
    elif args.command == "in-progress":
        list_in_progress_tasks(args.id)


if __name__ == "__main__":
    main()

status_icons = {
    "todo": "📝",
    "in-progress": "⏳",
    "done": "✅"
}

task = {
    "id": 1,
    "status": "in-progress",
    "title": "Fix the undefined variable error"
}

print(f"{task['id']}. {status_icons[task['status']]} {task['title']}")
