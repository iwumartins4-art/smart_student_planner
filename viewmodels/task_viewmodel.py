from models.database import Database

class TaskViewModel:
    def __init__(self):
        self.db = Database()

    def get_tasks(self, search_query=None):
        return self.db.get_all_tasks(search_query)

    def add_task(self, title, module, due_date, priority, notes):
        # Validation logic
        if not title:
            return False, "Task title is required"
        if not due_date:
            return False, "Due date is required"
        
        self.db.add_task(title, module, due_date, priority, notes)
        return True, "Task added successfully"

    def edit_task(self, task_id, title, module, due_date, priority, notes, is_completed):
        if not title:
            return False, "Task title is required"
        
        self.db.update_task(task_id, title, module, due_date, priority, notes, is_completed)
        return True, "Task updated successfully"

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        return True, "Task deleted"

    def toggle_status(self, task_id, current_status):
        new_status = 0 if current_status == 1 else 1
        self.db.toggle_task_complete(task_id, new_status)
        return True, "Status updated"

    def search_tasks(self, keyword):
        if not keyword:
            return self.get_tasks()
        return self.db.get_all_tasks(keyword)
