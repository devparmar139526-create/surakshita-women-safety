import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('surakshita.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Incidents table with High Alert support
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            incident_type TEXT NOT NULL,
            description TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            priority TEXT DEFAULT 'Normal',
            is_sos BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add columns to existing incidents table if they don't exist
    try:
        cursor.execute('ALTER TABLE incidents ADD COLUMN priority TEXT DEFAULT "Normal"')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE incidents ADD COLUMN is_sos BOOLEAN DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
