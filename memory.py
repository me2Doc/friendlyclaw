import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/friendlyclaw.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            user_id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            fact TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_profile(user_id: str, profile: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""
        INSERT INTO profile (user_id, data, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at
    """, (user_id, json.dumps(profile), now, now))
    conn.commit()
    conn.close()


def get_profile(user_id: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM profile WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else {}


def add_message(user_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (user_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_history(user_id: str, limit: int = 30) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT role, content FROM messages
        WHERE user_id=?
        ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]


def save_memory(user_id: str, key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO memories (user_id, key, value, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, key, value, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_memories(user_id: str, limit: int = 20) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT key, value, timestamp FROM memories
        WHERE user_id=?
        ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"key": r[0], "value": r[1], "when": r[2]} for r in rows]


def add_fact(user_id: str, fact: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO facts (user_id, fact, timestamp)
        VALUES (?, ?, ?)
    """, (user_id, fact, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_facts(user_id: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT fact FROM facts WHERE user_id=? ORDER BY id DESC LIMIT 50", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]


def clear_user(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["profile", "messages", "memories", "facts"]:
        c.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
