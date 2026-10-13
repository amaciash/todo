"""Data layer: all SQL for the to-do app lives here."""
from db import cursor

# Only these columns can be changed through update_task (prevents bad column names).
EDITABLE_FIELDS = {"title", "description", "priority", "due_date"}


def add_task(title, description=None, priority="medium", due_date=None):
    with cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title, description, priority, due_date) "
            "VALUES (%s, %s, %s, %s)",
            (title, description or None, priority, due_date),
        )
        return cur.lastrowid


def get_task(task_id):
    with cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        return cur.fetchone()


def list_tasks(status=None, priority=None, search=None):
    """Return tasks, optionally filtered. Pending first, soonest due date first."""
    sql = "SELECT * FROM tasks WHERE 1 = 1"
    params = []
    if status:
        sql += " AND status = %s"
        params.append(status)
    if priority:
        sql += " AND priority = %s"
        params.append(priority)
    if search:
        sql += " AND (title LIKE %s OR description LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])
    sql += (
        " ORDER BY status = 'done', due_date IS NULL, due_date,"
        " FIELD(priority, 'high', 'medium', 'low')"
    )
    with cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def update_task(task_id, **fields):
    changes = {k: v for k, v in fields.items() if k in EDITABLE_FIELDS}
    if not changes:
        return 0
    set_clause = ", ".join(f"{column} = %s" for column in changes)
    with cursor() as cur:
        cur.execute(
            f"UPDATE tasks SET {set_clause} WHERE task_id = %s",
            [*changes.values(), task_id],
        )
        return cur.rowcount


def complete_task(task_id):
    """Mark a pending task as done. Returns 1 if it changed, 0 otherwise."""
    with cursor() as cur:
        cur.execute(
            "UPDATE tasks SET status = 'done', completed_at = NOW() "
            "WHERE task_id = %s AND status = 'pending'",
            (task_id,),
        )
        return cur.rowcount


def delete_task(task_id):
    with cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        return cur.rowcount


def get_stats():
    with cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)                                          AS total,
                   COALESCE(SUM(status = 'pending'), 0)              AS pending,
                   COALESCE(SUM(status = 'done'), 0)                 AS done,
                   COALESCE(SUM(status = 'pending'
                                AND due_date < CURDATE()), 0)        AS overdue
            FROM tasks
            """
        )
        return cur.fetchone()
