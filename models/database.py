import sqlite3
import os
from pathlib import Path

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized: return
        
        try:
            # We use the current project directory for the database
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_dir = os.path.join(base_path, "database")
            
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            self.db_path = os.path.join(db_dir, "planner.db")
            # Use check_same_thread=False to allow cross-screen updates in Kivy
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            self.create_tables()
            self._prepopulate_demo_data()
            self.initialized = True
            print(f"[DB SUCCESS] Connected to unified database: {self.db_path}")
            
        except Exception as e:
            print(f"[DB ERROR] Database initialization failed: {e}")

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                module TEXT,
                due_date TEXT,
                priority TEXT,
                notes TEXT,
                is_completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def get_all_tasks(self, search_query=None):
        if search_query:
            # Case-insensitive fuzzy search
            self.cursor.execute("SELECT * FROM tasks WHERE title LIKE ? OR module LIKE ?", 
                              (f'%{search_query}%', f'%{search_query}%'))
        else:
            self.cursor.execute("SELECT * FROM tasks ORDER BY is_completed ASC, due_date ASC")
        return self.cursor.fetchall()

    def add_task(self, title, module, due_date, priority, notes):
        self.cursor.execute('''
            INSERT INTO tasks (title, module, due_date, priority, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, module, due_date, priority, notes))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_task(self, task_id, title, module, due_date, priority, notes, is_completed):
        self.cursor.execute('''
            UPDATE tasks SET title=?, module=?, due_date=?, priority=?, notes=?, is_completed=?
            WHERE id=?
        ''', (title, module, due_date, priority, notes, is_completed, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def toggle_task_complete(self, task_id, status):
        self.cursor.execute("UPDATE tasks SET is_completed=? WHERE id=?", (status, task_id))
        self.conn.commit()

    def _prepopulate_demo_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        if self.cursor.fetchone()[0] == 0:
            demo = [
                ("Math assignment", "Introduction to Algebra", "2026-04-25", "High", "Challenging equations", 0),
                ("Submit Lab Report", "Chemistry 101", "2026-04-26", "Medium", "Focus on results", 0),
                ("History Essay", "Modern World History", "2026-05-01", "Low", "Topic: Revolution", 1)
            ]
            self.cursor.executemany("INSERT INTO tasks (title, module, due_date, priority, notes, is_completed) VALUES (?,?,?,?,?,?)", demo)
            self.conn.commit()
