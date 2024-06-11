import sqlite3
import os

DATABASE_PATH = 'db/football_club.db'

def create_tables() -> None:
    """
    Create tables for the football club database if they do not already exist.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            points INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            score1 INTEGER DEFAULT 0,
            score2 INTEGER DEFAULT 0
        )
    """)
    
    # cursor.execute("DROP TABLE IF EXISTS seats")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            sector TEXT,
            row INTEGER,
            seat INTEGER,
            price REAL,
            purchased INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_admin(email: str, password: str) -> None:
    """
    Add an admin to the admins table if not already exists.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
    admin = cursor.fetchone()
    
    if admin:
        print("Администратор уже существует.")
    else:
        cursor.execute("INSERT INTO admins (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        print("Администратор добавлен.")
    
    conn.close()

if __name__ == "__main__":
    if not os.path.exists('db'):
        os.makedirs('db')
    
    create_tables()
    add_admin('admin@bk.ru', '1')
