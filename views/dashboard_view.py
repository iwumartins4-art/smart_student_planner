from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from viewmodels.task_viewmodel import TaskViewModel
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.metrics import dp
import datetime

class TaskCard(MDCard):
    title = StringProperty()
    module = StringProperty()
    due_date = StringProperty()
    priority = StringProperty()
    status = StringProperty("Not Started")
    task_id = NumericProperty()
    # index property removed as per Mandatory Fix 5

    def on_menu_click(self, button):
        app = MDApp.get_running_app()
        dashboard = app.root.get_screen('dashboard')
        # CRITICAL: Always use task_id as the primary identifier
        dashboard.open_task_menu(button, self.task_id)

class DashboardView(MDScreen):
    rv_data = ListProperty([])
    today_count = NumericProperty(0)
    completion_percent = NumericProperty(0)
    deadline_text = StringProperty("None")
    username = StringProperty("Student")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = TaskViewModel()
        self.dialog = None
        self.menu = None
        self.status_menu = None

    def on_enter(self):
        app = MDApp.get_running_app()
        if app.user_data and 'username' in app.user_data:
            self.username = app.user_data['username']
        self.refresh_tasks()

    def refresh_tasks(self, search_query=None):
        try:
            # Mandatory Fix 3 & 6: Reload everything and force full RecycleView refresh
            tasks = self.viewmodel.get_tasks(search_query)
            self.update_metrics(tasks)
            
            # Explicitly reset data to force view recycling
            self.rv_data = [] 
            self.rv_data = tasks
            
            # Ensure the RecycleView knows the data changed
            if 'task_rv' in self.ids:
                self.ids.task_rv.refresh_from_data()
                
        except Exception as e:
            print(f"STABILITY ERROR: {e}")

    def update_metrics(self, tasks):
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        self.today_count = sum(1 for t in tasks if t['due_date'] == today_str)
        
        total = len(tasks)
        completed = sum(1 for t in tasks if t['status'] == "Completed")
        self.completion_percent = int((completed / total) * 100) if total > 0 else 0
        
        pending = [t for t in tasks if t['status'] != "Completed"]
        if not pending:
            self.deadline_text = "Done!"
            return
            
        try:
            pending.sort(key=lambda x: x['due_date'])
            nearest = pending[0]['due_date']
            target_date = datetime.datetime.strptime(nearest, "%Y-%m-%d")
            diff = target_date - datetime.datetime.now()
            hours = diff.total_seconds() / 3600
            
            if hours < 0: self.deadline_text = "Overdue"
            elif hours < 24: self.deadline_text = f"{int(hours)}h"
            else: self.deadline_text = f"{int(hours/24)}d"
        except:
            self.deadline_text = "---"

    def open_task_menu(self, caller, task_id):
        # Mandatory Fix 1: Operations strictly use task_id
        menu_items = [
            {"text": "Change Status", "on_release": lambda *x: self.open_status_selector(caller, task_id)},
            {"text": "Edit Task", "on_release": lambda *x: self.edit_task_by_id(task_id)},
            {"text": "Delete Task", "on_release": lambda *x: self.confirm_delete_by_id(task_id)},
        ]
        self.menu = MDDropdownMenu(caller=caller, items=menu_items, width=dp(160))
        self.menu.open()

    def open_status_selector(self, caller, task_id):
        if self.menu: self.menu.dismiss()
        status_items = [
            {"text": "Not Started", "on_release": lambda *x, s="Not Started": self.set_task_status(task_id, s)},
            {"text": "In Progress", "on_release": lambda *x, s="In Progress": self.set_task_status(task_id, s)},
            {"text": "Completed", "on_release": lambda *x, s="Completed": self.set_task_status(task_id, s)},
        ]
        self.status_menu = MDDropdownMenu(caller=caller, items=status_items, width=dp(160))
        self.status_menu.open()

    def set_task_status(self, task_id, new_status):
        if self.status_menu: self.status_menu.dismiss()
        # Update database through ViewModel
        self.viewmodel.update_status_only(task_id, new_status, 0)
        # Mandatory Fix 3: Full refresh after update
        self.refresh_tasks()
        MDSnackbar(MDSnackbarText(text=f"Status: {new_status}")).open()

    def edit_task_by_id(self, task_id):
        if self.menu: self.menu.dismiss()
        # Mandatory Fix 5: Find task by task_id, not index
        t = next((task for task in self.rv_data if task['task_id'] == task_id), None)
        if t:
            task_tuple = (t['task_id'], t['title'], t['module'], t['due_date'], t['priority'], t['notes'], t['status'], t['is_completed'])
            self.manager.get_screen('task_form').set_task_data(task_tuple)
            self.manager.current = 'task_form'

    def confirm_delete_by_id(self, task_id):
        if self.menu: self.menu.dismiss()
        self.dialog = MDDialog(
            MDDialogIcon(icon="delete-alert"),
            MDDialogHeadlineText(text="Delete Task?"),
            MDDialogSupportingText(text="This action cannot be undone."),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="Delete"), style="tonal", theme_bg_color="Custom", md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x, tid=task_id: self.delete_task_final(tid)),
                spacing="8dp",
            ),
        )
        self.dialog.open()

    def delete_task_final(self, task_id):
        if self.dialog: self.dialog.dismiss()
        self.viewmodel.delete_task(task_id)
        # Mandatory Fix 3: Full refresh after delete
        self.refresh_tasks()
        MDSnackbar(MDSnackbarText(text="Task deleted")).open()

    def go_to_add_task(self):
        self.manager.get_screen('task_form').clear_form()
        self.manager.current = 'task_form'

    def confirm_logout(self):
        self.dialog = MDDialog(
            MDDialogIcon(icon="logout"),
            MDDialogHeadlineText(text="Logout?"),
            MDDialogSupportingText(text="Are you sure you want to log out?"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="Logout"), style="tonal", on_release=lambda x: self.handle_logout()),
                spacing="8dp",
            ),
        )
        self.dialog.open()

    def handle_logout(self):
        if self.dialog: self.dialog.dismiss()
        self.manager.get_screen('login').clear_fields()
        MDApp.get_running_app().user_data = {}
        self.manager.current = 'login'
