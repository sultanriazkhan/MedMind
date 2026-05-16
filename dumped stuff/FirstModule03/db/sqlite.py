"""
Database module for storing processed results
Simple SQLite only
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "lab_results.db"

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_type TEXT,
            raw_text TEXT,
            results_json TEXT,
            summary_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_result(source_type: str, raw_text: str, tests: list, summary: dict):
    """Save processed result to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO processed_results 
           (timestamp, source_type, raw_text, results_json, summary_json) 
           VALUES (?, ?, ?, ?, ?)""",
        (
            datetime.now().isoformat(),
            source_type,
            raw_text[:1000],  # Limit raw text length
            json.dumps(tests),
            json.dumps(summary)
        )
    )
    conn.commit()
    conn.close()

def get_recent_results(limit: int = 10) -> list:
    """Get recent results from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, source_type, summary_json FROM processed_results ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize on import
init_db()