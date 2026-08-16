"""
database.py
------------
This file handles saving and loading your notes using SQLite
(a simple built-in database that lives in a single file — no setup needed).

You don't need to install anything extra for this part; Python already
includes SQLite.
"""

import sqlite3
import json
from datetime import datetime

DB_FILE = "notes.db"


def init_db():
    """Creates the notes table if it doesn't already exist. Safe to call every time the app starts."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL,
            note_type TEXT DEFAULT 'note',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_note(content: str, embedding: list, note_type: str = "note"):
    """
    Saves a note to the database.
    - content: the actual text of the note
    - embedding: a list of numbers representing the "meaning" of the text (used for search later)
    - note_type: "note" for normal notes, "story" for generated stories
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (content, embedding, note_type, created_at) VALUES (?, ?, ?, ?)",
        (content, json.dumps(embedding), note_type, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_notes():
    """Returns every note stored, most recent first."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, embedding, note_type, created_at FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    notes = []
    for row in rows:
        notes.append({
            "id": row[0],
            "content": row[1],
            "embedding": json.loads(row[2]),
            "type": row[3],
            "created_at": row[4]
        })
    return notes


def delete_note(note_id: int):
    """Deletes a single note by its id."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
