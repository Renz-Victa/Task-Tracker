# task_tracker/cli.py
import argparse
import json
import os
from task_tracker.commands import add_task, list_tasks, done_task

FILE = "tasks.json"

# Helpers


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


def list_tasks(task_id):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task["completed"] else "X"
        print(f"{task['id']}. [{status}] {task['title']}")

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
    update_parser.add_argument("id", type=int, help="Task ID")
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


if __name__ == "__main__":
    main()
