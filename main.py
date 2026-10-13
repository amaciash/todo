"""Command-line interface for the to-do app."""
from datetime import date, datetime

import mysql.connector

import tasks

PRIORITIES = ("high", "medium", "low")


# ---------- input helpers ----------
def ask_text(prompt, required=False, default=None):
    """Ask for text. If a default is given, pressing Enter keeps it."""
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if value or not required:
            return value
        print("This field is required.")


def ask_priority(default="medium"):
    while True:
        value = input(f"Priority (high/medium/low) [{default}]: ").strip().lower()
        if not value:
            return default
        if value in PRIORITIES:
            return value
        print("Please type high, medium or low.")


def ask_date(default=None):
    shown = default.isoformat() if default else "none"
    while True:
        value = input(
            f"Due date YYYY-MM-DD [{shown}] (type 'none' to clear): "
        ).strip().lower()
        if not value:
            return default
        if value == "none":
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Example: 2026-12-31")


def ask_id(prompt="Task ID"):
    while True:
        value = input(f"{prompt}: ").strip()
        if value.isdigit():
            return int(value)
        print("Please enter a number.")


def confirm(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == "y"


# ---------- display ----------
def show_tasks(rows):
    if not rows:
        print("\nNo tasks to show.")
        return
    today = date.today()
    print(f"\n{'ID':<4} {'Done':<5} {'Prio':<7} {'Due':<11} Title")
    print("-" * 60)
    for t in rows:
        mark = "[x]" if t["status"] == "done" else "[ ]"
        due = t["due_date"].isoformat() if t["due_date"] else "-"
        flag = ""
        if t["status"] == "pending" and t["due_date"] and t["due_date"] < today:
            flag = "  << OVERDUE"
        print(f"{t['task_id']:<4} {mark:<5} {t['priority']:<7} {due:<11} "
              f"{t['title']}{flag}")


def show_one(task):
    print(f"\n#{task['task_id']}  {task['title']}")
    print(f"  Description: {task['description'] or '-'}")
    print(f"  Priority:    {task['priority']}")
    print(f"  Status:      {task['status']}")
    print(f"  Due date:    {task['due_date'] or '-'}")


# ---------- actions ----------
def action_add():
    title = ask_text("Title", required=True)
    description = ask_text("Description (optional)")
    priority = ask_priority()
    due = ask_date()
    new_id = tasks.add_task(title, description, priority, due)
    print(f"\nTask #{new_id} created.")


def action_list_all():
    show_tasks(tasks.list_tasks())


def action_list_pending():
    show_tasks(tasks.list_tasks(status="pending"))


def action_filter_priority():
    show_tasks(tasks.list_tasks(priority=ask_priority()))


def action_search():
    term = ask_text("Search for", required=True)
    show_tasks(tasks.list_tasks(search=term))


def action_view():
    task = tasks.get_task(ask_id())
    if task:
        show_one(task)
    else:
        print("Task not found.")


def action_edit():
    task = tasks.get_task(ask_id())
    if not task:
        print("Task not found.")
        return
    show_one(task)
    print("\nPress Enter to keep the current value.")
    tasks.update_task(
        task["task_id"],
        title=ask_text("Title", default=task["title"]),
        description=ask_text("Description", default=task["description"] or ""),
        priority=ask_priority(task["priority"]),
        due_date=ask_date(task["due_date"]),
    )
    print("Task updated.")


def action_complete():
    if tasks.complete_task(ask_id()):
        print("Task marked as done.")
    else:
        print("Task not found or already done.")


def action_delete():
    task_id = ask_id()
    task = tasks.get_task(task_id)
    if not task:
        print("Task not found.")
        return
    if confirm(f"Delete '{task['title']}'?"):
        tasks.delete_task(task_id)
        print("Task deleted.")
    else:
        print("Cancelled.")


def action_stats():
    s = tasks.get_stats()
    print(f"\nTotal: {s['total']}  |  Pending: {s['pending']}  |  "
          f"Done: {s['done']}  |  Overdue: {s['overdue']}")
    if s["total"]:
        print(f"Completion rate: {100 * s['done'] / s['total']:.0f}%")


MENU = {
    "1": ("Add task", action_add),
    "2": ("List all tasks", action_list_all),
    "3": ("List pending tasks", action_list_pending),
    "4": ("Filter by priority", action_filter_priority),
    "5": ("Search", action_search),
    "6": ("View task details", action_view),
    "7": ("Edit task", action_edit),
    "8": ("Mark task as done", action_complete),
    "9": ("Delete task", action_delete),
    "10": ("Statistics", action_stats),
    "0": ("Exit", None),
}


def main():
    print("=== TO-DO APP ===")
    while True:
        print("\n--- Menu ---")
        for key, (label, _) in MENU.items():
            print(f"{key:>2}. {label}")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice not in MENU:
            print("Invalid option.")
            continue
        try:
            MENU[choice][1]()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except KeyboardInterrupt:
            print("\nCancelled.")


if __name__ == "__main__":
    main()
