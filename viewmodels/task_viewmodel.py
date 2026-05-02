from models.database import Database

class TaskViewModel:
    # GLOBAL MAPPING LAYER
    STATUS_MAP = {
        0: "Not Started",
        1: "In Progress",
        2: "Completed"
    }
    REVERSE_MAP = {
        "Not Started": 0,
        "In Progress": 1,
        "Completed": 2
    }

    def __init__(self):
        self.db = Database()

    def get_tasks(self, search_query=None):
        raw_tasks = self.db.get_all_tasks(search_query)
        tasks = []
        valid_texts = ["Not Started", "In Progress", "Completed"]
        
        for t in raw_tasks:
            raw_val = t[6]
            
            # CRITICAL FIX: Safe conversion with no shifting or offset
            if raw_val in valid_texts:
                display_status = raw_val
            else:
                try:
                    # Map numeric safely (0=Not Started, 1=In Progress, 2=Completed)
                    idx = int(raw_val)
                    if idx == 0: display_status = "Not Started"
                    elif idx == 1: display_status = "In Progress"
                    elif idx == 2: display_status = "Completed"
                    else: display_status = "Not Started"
                except:
                    # Fallback for any other value
                    display_status = "Not Started"
            
            tasks.append({
                "task_id": t[0],
                "title": str(t[1]),
                "module": str(t[2]),
                "due_date": str(t[3]),
                "priority": str(t[4]),
                "notes": str(t[5]),
                "status": display_status,
                "is_completed": 1 if display_status == "Completed" else 0
            })
        return tasks

    def add_task(self, title, module, due_date, priority, notes, status_text='Not Started'):
        if not title: return False, "Title required"
        if not due_date: return False, "Date required"
        
        # CONVERT DISPLAY (string) -> INTERNAL (int)
        internal_status = self.REVERSE_MAP.get(status_text, 0)
        print(f"[VM DEBUG] Adding Task: '{status_text}' -> Converted to {internal_status}")
        self.db.add_task(title, module, due_date, priority, notes, internal_status)
        return True, "Task added successfully"

    def edit_task(self, task_id, title, module, due_date, priority, notes, status_text, is_completed):
        if not title: return False, "Title required"
        
        # CONVERT DISPLAY (string) -> INTERNAL (int)
        internal_status = self.REVERSE_MAP.get(status_text, 0)
        is_completed = 1 if status_text == "Completed" else 0
        print(f"[VM DEBUG] Editing Task: '{status_text}' -> Converted to {internal_status}")
        self.db.update_task(task_id, title, module, due_date, priority, notes, internal_status, is_completed)
        return True, "Task updated successfully"

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        return True, "Task deleted"

    def update_status_only(self, task_id, status_text, is_completed):
        # CONVERT DISPLAY (string) -> INTERNAL (int)
        internal_status = self.REVERSE_MAP.get(status_text, 0)
        is_completed = 1 if status_text == "Completed" else 0
        print(f"[VM DEBUG] Quick Update: '{status_text}' -> Converted to {internal_status}")
        self.db.cursor.execute("UPDATE tasks SET status=?, is_completed=? WHERE id=?", 
                              (internal_status, is_completed, task_id))
        self.db.conn.commit()
        return True, "Status updated"

    def search_tasks(self, keyword):
        return self.get_tasks(keyword)
