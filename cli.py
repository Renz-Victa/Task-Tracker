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
    try:
        with open(FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []


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


def add_task(description):
    tasks = load_tasks()
    now = current_time()

    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
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


def update_task(task_id, new_title=None, description=None, status=None):
    tasks = load_tasks()
    valid_statuses = ["todo", "in-progress", "done"]

    for task in tasks:
        if task["id"] == task_id:
            if new_title:
                task["title"] = new_title
            if description is not None:
                task["description"] = description
            if status is not None:
                if status not in valid_statuses:
                    print("Invalid status. Use: todo, in-progress, done")
                    return
                task["status"] = status

            task["updateAt"] = current_time()
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
        task for task in tasks if task["status"] == "in-progress"
    ]

    if not in_progress_tasks:
        print("No tasks in progress.")
        return

    print("\nIn-Progress Tasks:\n" + "-" * 30)

    for task in in_progress_tasks:
        print(f"{task['id']}. ⏳ {task['title']}")

# List All Tasks Function


def list_tasks(task_id=None):
    tasks = load_tasks()

    exclude = "done"

    if exclude:
        tasks = [task for task in tasks if task.get("status") != exclude]

    if not tasks:
        print("No tasks found.")
        return

    print("\nYour Tasks:\n" + "-" * 30)

    for task in tasks:
        title = task.get("title") or task.get("description", "Untitled")
        status = task.get("status", "todo")
        completed = task.get("completed", False)
        status_icon = "✓" if completed else "✗"
        print(f"ID: {task['id']}")
        print(f"Title: {title}")
        print(f"Status: {status} {status_icon}")
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

    # Update Command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--status", help="todo | in-progress | done")

    # Pending Command
    pending_parser = subparsers.add_parser(
        "pending", help="List pending tasks")

    # In-progress Command
    in_progress_parser = subparsers.add_parser(
        "in-progress", help="List in-progress tasks")

    # list
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # done
    done = subparsers.add_parser("done", help="Mark a task as done")
    done.add_argument("id", type=int, help="Task ID")

    # delete
    delete = subparsers.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    # Command Handling
    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks(None)
    elif args.command == "update":
        update_task(args.id, args.title, args.description, args.status)
    elif args.command == "done":
        done_task(args.id)
    elif args.command == "pending":
        list_not_done_tasks()
    elif args.command == "in-progress":
        list_in_progress_tasks()
    elif args.command == "delete":
        delete_tasks(args.id)


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
