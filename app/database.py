import sqlite3

DB_NAME = "issues.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
            repo TEXT,
            title TEXT,
            body TEXT,
            html_url TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()
