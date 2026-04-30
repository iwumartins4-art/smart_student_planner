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
            from kivymd.app import MDApp
            from kivy.utils import platform
            
            # Determine a writable directory based on the platform
            if platform in ['android', 'ios']:
                # On mobile, use the app's official private data directory
                # This is more stable than manually importing storage logic
                app = MDApp.get_running_app()
                if app:
                    base_path = app.user_data_dir
                else:
                    # Fallback if App isn't running yet
                    from os.path import expanduser
                    base_path = expanduser("~")
            else:
                # On Desktop, use the project root
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
            # Fallback to in-memory database to prevent crash, though data won't persist
            self.db_path = ":memory:"
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_tables()
            self.initialized = True

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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                password TEXT NOT NULL,
                major TEXT,
                student_id TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, full_name, username, email, password, major, student_id):
        try:
            self.cursor.execute('''
                INSERT INTO users (full_name, username, email, password, major, student_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (full_name, username, email, password, major, student_id))
            self.conn.commit()
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, str(e)

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

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
