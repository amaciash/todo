# To-Do App (Python + MySQL)

A command-line task manager backed by a MySQL database. Tasks have a title,
description, priority, due date and status, and persist between sessions.

## Features
- Add, view, edit, complete and delete tasks
- Filter by priority, search by keyword, list pending tasks
- Overdue tasks are flagged automatically
- Statistics: totals, pending, done, overdue, completion rate
- Input validation (dates, priorities, IDs) and friendly database error messages

## Setup
1. Install MySQL 8+.
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create the database (from the MySQL client):
   ```
   source /full/path/to/schema.sql
   ```
4. Copy `.env.example` to `.env` and fill in your MySQL credentials.
5. Run the app:
   ```
   python main.py
   ```

## Project structure
| File | Responsibility |
|---|---|
| `schema.sql` | Database and table definition |
| `db.py` | Connection and transaction helper (commit / rollback) |
| `tasks.py` | Data layer: every SQL query for tasks |
| `main.py` | Command-line menu and input validation |

## Design notes
- All queries are parameterized to prevent SQL injection.
- Editable columns are whitelisted in `update_task`.
- The data layer is separate from the interface, so the CLI could later be
  replaced with a web API without touching the SQL.

## Next steps
- Unit tests with pytest
- Categories/tags table (one-to-many)
- REST API with FastAPI
