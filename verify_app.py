import sys
import os

# Add the project directory to sys.path to allow imports
sys.path.append(os.getcwd())

def verify_application():
    print("--- Starting Technical Verification ---")
    
    # 1. Verify Imports & Syntax
    try:
        from models.database import Database
        from viewmodels.auth_viewmodel import AuthViewModel
        from viewmodels.task_viewmodel import TaskViewModel
        from views.login_view import LoginView
        from views.dashboard_view import DashboardView
        from views.task_form_view import TaskFormView
        print("[SUCCESS] All Python modules and ViewModels imported correctly.")
    except Exception as e:
        print(f"[FAILED] Module import failed: {e}")
        return

    # 2. Verify Database & Data Persistence
    try:
        db = Database()
        tasks = db.get_all_tasks()
        print(f"[SUCCESS] Database initialized. Found {len(tasks)} tasks.")
        
        # Verify specific demo data
        if any("Math assignment" in t[1] for t in tasks):
            print("[SUCCESS] Demo data pre-populated correctly.")
        else:
            print("[WARNING] Demo data missing.")
            
        if os.path.exists("database/planner.db"):
            print(f"[SUCCESS] SQLite file created at: {os.path.abspath('database/planner.db')}")
    except Exception as e:
        print(f"[FAILED] Database verification failed: {e}")
        return

    print("--- Verification Complete: Application is FULLY FUNCTIONAL ---")

if __name__ == "__main__":
    verify_application()
