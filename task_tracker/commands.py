# Task management commands for the task tracker CLI.

from pathlib import Path
import json
from datetime import datetime

DATA_FILE = Path("tasks.json")


def _load_tasks():
    # Load tasks from JSON file
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_tasks(tasks):
    # Save tasks to JSON file
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    # Add a new task
    tasks = _load_tasks()
    task_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": task_id,
        "title": title,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    _save_tasks(tasks)
    print(f"Task added: {title} (ID: {task_id})")


def list_tasks():
    # List all tasks
    tasks = _load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"[{status}] {task['id']}: {task['title']}")


def done_task(task_id):
    # Mark a task as done
    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            _save_tasks(tasks)
            print(f"Task {task_id} marked as done: {task['title']}")
            return
    print(f"Task {task_id} not found.")
