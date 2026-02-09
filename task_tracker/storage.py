# task_tracker/storage.py

from pathlib import Path
import json

DATA_FILE = Path.home() / ".tasktracker" / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    DATA_FILE.parent.mkdir(parent=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
