import sqlite3
from contextlib import contextmanager

DATABASE = "dormitory.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        family TEXT NOT NULL,
        student_id TEXT UNIQUE NOT NULL,
        major TEXT,
        degree TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT UNIQUE NOT NULL,
        capacity INTEGER NOT NULL,
        status TEXT DEFAULT 'خالی',
        building TEXT
    )
    """)
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        room_id INTEGER,
        request_date DATE DEFAULT CURRENT_DATE,
        status TEXT DEFAULT 'در انتظار',
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (room_id) REFERENCES rooms(id)
    )
    """)
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date DATE DEFAULT CURRENT_DATE,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    """)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    try:
        yield conn
    finally:
        conn.close()

init_db()