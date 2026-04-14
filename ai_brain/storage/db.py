import os
import sqlite3
from pathlib import Path
from datetime import datetime

# Global DB Path
GLOBAL_DB_DIR = Path.home() / ".ai-brain"
GLOBAL_DB_PATH = GLOBAL_DB_DIR / "global.db"

def init_db():
    """Initialize the global database."""
    GLOBAL_DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(GLOBAL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT UNIQUE NOT NULL,
            initialized_at DATETIME NOT NULL,
            last_synced_at DATETIME NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_project(name: str, path: str):
    """Register or update a project in the global database."""
    conn = sqlite3.connect(GLOBAL_DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute("SELECT id FROM projects WHERE path = ?", (path,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute("""
            UPDATE projects SET last_synced_at = ? WHERE path = ?
        """, (now, path))
    else:
        cursor.execute("""
            INSERT INTO projects (name, path, initialized_at, last_synced_at)
            VALUES (?, ?, ?, ?)
        """, (name, path, now, now))
        
    conn.commit()
    conn.close()

def update_last_synced(path: str):
    """Update the last_synced_at timestamp for a project."""
    conn = sqlite3.connect(GLOBAL_DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("UPDATE projects SET last_synced_at = ? WHERE path = ?", (now, path))
    conn.commit()
    conn.close()

def get_all_projects():
    """Retrieve all projects."""
    if not GLOBAL_DB_PATH.exists():
        return []
        
    conn = sqlite3.connect(GLOBAL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, path, initialized_at, last_synced_at FROM projects ORDER BY last_synced_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "name": row[0],
            "path": row[1],
            "initialized_at": row[2],
            "last_synced_at": row[3]
        }
        for row in rows
    ]
