import sqlite3
import json
import sqlite_vec
import numpy as np
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path("data/friendlyclaw.db")

@contextmanager
def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
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
        # Vector Table for RAG
        c.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_memories USING vec0(
                id INTEGER PRIMARY KEY,
                embedding FLOAT[768]
            )
        """)
        # Persistent Pending Actions
        c.execute("""
            CREATE TABLE IF NOT EXISTS pending_actions (
                action_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                action_data TEXT NOT NULL,
                original_message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def save_pending_action(action_id: str, user_id: str, action_data: dict, message: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO pending_actions (action_id, user_id, action_data, original_message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (action_id, user_id, json.dumps(action_data), message, datetime.now().isoformat()))
        conn.commit()

def get_pending_action(action_id: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT action_data, original_message FROM pending_actions WHERE action_id=?", (action_id,))
        row = c.fetchone()
        if row:
            return {"action": json.loads(row[0]), "message": row[1]}
        return None

def delete_pending_action(action_id: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM pending_actions WHERE action_id=?", (action_id,))
        conn.commit()

def save_memory_vector(user_id: str, memory_id: int, embedding: list):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO vec_memories(id, embedding) VALUES (?, ?)",
            (memory_id, sqlite_vec.serialize_float32(embedding))
        )
        conn.commit()

def search_memories(user_id: str, query_embedding: list, limit: int = 5):
    with get_db() as conn:
        c = conn.cursor()
        # Join with memories table to get the actual text
        c.execute("""
            SELECT m.key, m.value, v.distance
            FROM vec_memories v
            JOIN memories m ON v.id = m.id
            WHERE m.user_id = ?
              AND v.embedding MATCH ?
              AND k = ?
            ORDER BY v.distance
        """, (user_id, sqlite_vec.serialize_float32(query_embedding), limit))
        rows = c.fetchall()
        return [{"key": r[0], "value": r[1], "score": r[2]} for r in rows]

def save_profile(user_id: str, profile: dict):
    with get_db() as conn:
        c = conn.cursor()
        now = datetime.now().isoformat()
        c.execute("""
            INSERT INTO profile (user_id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at
        """, (user_id, json.dumps(profile), now, now))
        conn.commit()

def get_profile(user_id: str) -> dict:
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT data FROM profile WHERE user_id=?", (user_id,))
        row = c.fetchone()
        return json.loads(row[0]) if row else {}

def add_message(user_id: str, role: str, content: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO messages (user_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, role, content, datetime.now().isoformat()))
        conn.commit()

def get_history(user_id: str, limit: int = 30) -> list:
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT role, content FROM messages
            WHERE user_id=?
            ORDER BY id DESC LIMIT ?
        """, (user_id, limit))
        rows = c.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

def save_memory(user_id: str, key: str, value: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO memories (user_id, key, value, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, key, value, datetime.now().isoformat()))
        conn.commit()
        return c.lastrowid

def get_memories(user_id: str, limit: int = 20) -> list:
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT key, value, timestamp FROM memories
            WHERE user_id=?
            ORDER BY id DESC LIMIT ?
        """, (user_id, limit))
        rows = c.fetchall()
        return [{"key": r[0], "value": r[1], "when": r[2]} for r in rows]

def add_fact(user_id: str, fact: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO facts (user_id, fact, timestamp)
            VALUES (?, ?, ?)
        """, (user_id, fact, datetime.now().isoformat()))
        conn.commit()

def get_facts(user_id: str) -> list:
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT fact FROM facts WHERE user_id=? ORDER BY id DESC LIMIT 50", (user_id,))
        rows = c.fetchall()
        return [r[0] for r in rows]

def clear_user(user_id: str):
    with get_db() as conn:
        c = conn.cursor()
        for table in ["profile", "messages", "memories", "facts"]:
            # Use a safe way to format table names even though these are hardcoded
            c.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
        conn.commit()
