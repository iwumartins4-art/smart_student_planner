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
            
            if platform in ['android', 'ios']:
                app = MDApp.get_running_app()
                if app:
                    base_path = app.user_data_dir
                else:
                    from os.path import expanduser
                    base_path = expanduser("~")
            else:
                # Get the absolute path of the project root
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            
            db_dir = os.path.join(base_path, "database")
            print(f"[DB DEBUG] Attempting to initialize database at: {db_dir}")
            
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"[DB SUCCESS] Created database directory: {db_dir}")
            
            self.db_path = os.path.join(db_dir, "planner.db")
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            self.create_tables()
            # Mandatory Fix 3: Reset/Repair corrupted data
            self._repair_corrupted_data()
            self._prepopulate_demo_data()
            self.initialized = True
            print(f"[DB SUCCESS] Connected to unified database: {self.db_path}")
            
        except Exception as e:
            print(f"[DB ERROR] Database initialization failed: {e}")
            self.db_path = ":memory:"
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_tables()
            self.initialized = True

    def create_tables(self):
        # Mandatory Fix 2: Remove default status override
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                module TEXT,
                due_date TEXT,
                priority TEXT,
                notes TEXT,
                status INTEGER,
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

    def _repair_corrupted_data(self):
        # Mandatory Fix 3: Repair existing rows with invalid values
        try:
            self.cursor.execute("UPDATE tasks SET status = 0 WHERE status IN ('Not Started', '0', '') OR status IS NULL")
            self.cursor.execute("UPDATE tasks SET status = 1 WHERE status IN ('In Progress', '1')")
            self.cursor.execute("UPDATE tasks SET status = 2 WHERE status IN ('Completed', '2')")
            self.conn.commit()
        except Exception as e:
            print(f"[DB REPAIR ERROR] {e}")

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
            self.cursor.execute("SELECT * FROM tasks WHERE title LIKE ? OR module LIKE ? OR notes LIKE ?", 
                              (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        else:
            self.cursor.execute("SELECT * FROM tasks ORDER BY is_completed ASC, due_date ASC")
        return self.cursor.fetchall()

    def add_task(self, title, module, due_date, priority, notes, status):
        # Mandatory Fix 1 & 5: Explicit insert and debug logging
        print(f"[DB DEBUG] Inserting Task: '{title}' | Status: {status}")
        self.cursor.execute('''
            INSERT INTO tasks (title, module, due_date, priority, notes, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, module, due_date, priority, notes, status))
        self.conn.commit()
        
        # Verify save (Mandatory Fix 4)
        new_id = self.cursor.lastrowid
        self.cursor.execute("SELECT status FROM tasks WHERE id=?", (new_id,))
        saved_val = self.cursor.fetchone()[0]
        print(f"[DB DEBUG] Verification: Saved Status is {saved_val}")
        
        return new_id

    def update_task(self, task_id, title, module, due_date, priority, notes, status, is_completed):
        # Mandatory Fix 6: Safe update without fallback
        print(f"[DB DEBUG] Updating Task {task_id}: '{title}' | Status: {status}")
        self.cursor.execute('''
            UPDATE tasks SET title=?, module=?, due_date=?, priority=?, notes=?, status=?, is_completed=?
            WHERE id=?
        ''', (title, module, due_date, priority, notes, status, is_completed, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def _prepopulate_demo_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        if self.cursor.fetchone()[0] == 0:
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            demo = [
                ("Math assignment", "Introduction to Algebra", today, "High", "Challenging equations", 0, 0),
                ("Submit Lab Report", "Chemistry 101", "2026-05-10", "Medium", "Focus on results", 1, 0),
                ("History Essay", "Modern World History", "2026-05-01", "Low", "Topic: Revolution", 2, 1)
            ]
            self.cursor.executemany("INSERT INTO tasks (title, module, due_date, priority, notes, status, is_completed) VALUES (?,?,?,?,?,?,?)", demo)
            self.conn.commit()


# ihbugvytcft