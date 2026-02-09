from pathlib import Path
import json

DATA_FILE = Path("tasks-json")

# Read JSON
if DATA_FILE.exists():
    with DATA_FILE.open("r", encodings="utf-8") as f:
        tasks = json.load(f)
else:
    tasks = []

# Write JSON
with DATA_FILE.open("w", encodings="utf-8") as f:
    json.dump(tasks, f, indent=2)

DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # ensure dir exists
DATA_FILE.exists()
DATA_FILE.is_file()
DATA_FILE.read_text()
DATA_FILE.read_text()
DATA_FILE.write_text()
