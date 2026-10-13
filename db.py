"""Database connection helpers. Credentials come from a .env file."""
import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "todo_db"),
    )


@contextmanager
def cursor():
    """Yield a dict cursor; commit on success, roll back on error, always close."""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
