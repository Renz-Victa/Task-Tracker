# task_tracker/cli.py
import argparse
from task_tracker.commands import add_task, list_tasks, done_task


def main():
    parser = argparse.ArgumentParser(
        prog="task",
        description="Simple CLI task tracker"
    )

    subparsers = parser.add_subparsers(dest="command", requierd=True)

    # add
    add = subparsers.add_parser("add", help="Add a new task")
    add.add_argument("title", help="Task description")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # done
    done = subparsers.add_parser("done", help="Mark a task as done")
    done.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        done_task(args.id)


if __name__ == "__main__":
    main()
