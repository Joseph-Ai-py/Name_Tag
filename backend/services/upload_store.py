from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "backend" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "uploads.sqlite3"


def initialize_upload_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                path TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
                yield connection
    finally:
                connection.close()


def save_upload(filename: str, path: str) -> int:
    initialize_upload_db()
    created_at = datetime.utcnow().isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO uploads (filename, path, created_at) VALUES (?, ?, ?)",
            (filename, path, created_at),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_upload_rows() -> Iterable[sqlite3.Row]:
    initialize_upload_db()
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT id, filename, path, created_at FROM uploads ORDER BY id DESC"
        )
        return list(cursor.fetchall())
