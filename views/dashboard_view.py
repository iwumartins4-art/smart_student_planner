from kivy.factory import Factory
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from viewmodels.task_viewmodel import TaskViewModel
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText, MDFabButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.metrics import dp
import datetime

class TaskCard(MDBoxLayout):
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
        dashboard.open_task_menu(button, self.task_id)

    def on_title(self, instance, value):
        if 'title_label' in self.ids:
            self.ids.title_label.text = str(value) if value else ""
            self.ids.title_label.texture_update()

    def on_module(self, instance, value):
        self._update_secondary_label()

    def on_due_date(self, instance, value):
        self._update_secondary_label()

    def _update_secondary_label(self):
        if 'module_label' in self.ids:
            self.ids.module_label.text = f"{self.module} • {self.due_date}"
            self.ids.module_label.texture_update()

    def on_status(self, instance, value):
        if 'status_label' in self.ids:
            self.ids.status_label.text = str(value) if value else "Not Started"
            self.ids.status_label.texture_update()

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
            self.username = str(app.user_data['username'])
        else:
            self.username = "Student"
            
        if 'welcome_label' in self.ids:
            self.ids.welcome_label.text = f"Hi, {self.username}!"
            
        print(f"[DASHBOARD DEBUG] Entering dashboard. User: {self.username}")
        self.refresh_tasks()

    def refresh_tasks(self, search_query=None):
        try:
            print(f"[DASHBOARD DEBUG] Refreshing tasks. Query: {search_query}")
            tasks = self.viewmodel.get_tasks(search_query)
            print(f"[DASHBOARD DEBUG] Fetched {len(tasks)} tasks.")
            self.update_metrics(tasks)
            
            self.rv_data = [] 
            self.rv_data = tasks
            
            # Populate manual task list
            self.refresh_task_list(tasks)
                
        except Exception as e:
            print(f"STABILITY ERROR in refresh_tasks: {e}")
            import traceback
            traceback.print_exc()

    def refresh_task_list(self, tasks):
        if 'task_list_container' not in self.ids:
            return
            
        container = self.ids.task_list_container
        container.clear_widgets()
        
        if not tasks:
            # Add "No tasks found" label
            no_task_label = Factory.MDLabel(
                text="No tasks found",
                halign="center",
                theme_text_color="Secondary",
                font_style="Title",
                role="medium",
                size_hint_y=None,
                height=dp(100)
            )
            container.add_widget(no_task_label)
            return
            
        for task in tasks:
            card = TaskCard(
                task_id=task['task_id'],
                title=task['title'],
                module=task['module'],
                due_date=task['due_date'],
                priority=task['priority'],
                status=task['status']
            )
            container.add_widget(card)

    def _update_rv_height(self, dt):
        if 'task_rv' in self.ids:
            rv = self.ids.task_rv
            # Calculate height based on item count and spacing (dp(120) per item + dp(16) spacing)
            count = len(rv.data)
            new_height = count * dp(136) + dp(100) # extra padding at bottom
            rv.height = new_height

    def update_metrics(self, tasks):
        try:
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            self.today_count = sum(1 for t in tasks if t['due_date'] == today_str)
            
            total = len(tasks)
            completed = sum(1 for t in tasks if t['status'] == "Completed")
            self.completion_percent = int((completed / total) * 100) if total > 0 else 0
            
            pending = [t for t in tasks if t['status'] != "Completed"]
            if not pending:
                self.deadline_text = "Done!"
            else:
                try:
                    pending.sort(key=lambda x: x['due_date'])
                    nearest = pending[0]['due_date']
                    target_date = datetime.datetime.strptime(nearest, "%Y-%m-%d")
                    diff = target_date - datetime.datetime.now()
                    hours = diff.total_seconds() / 3600
                    
                    if hours < 0: self.deadline_text = "Overdue"
                    elif hours < 24: self.deadline_text = f"{int(hours)}h"
                    else: self.deadline_text = f"{int(hours/24)}d"
                except Exception as e:
                    print(f"[DASHBOARD DEBUG] Error calculating deadline: {e}")
                    self.deadline_text = "---"

            # EXPLICIT ID UPDATES (Mandatory Fix for Blank Cards)
            if 'today_tasks_label' in self.ids:
                self.ids.today_tasks_label.text = str(self.today_count)
            if 'deadline_label' in self.ids:
                self.ids.deadline_label.text = str(self.deadline_text)
            if 'goal_label' in self.ids:
                self.ids.goal_label.text = f"{self.completion_percent}%"
            
            print(f"[DASHBOARD DEBUG] Metrics updated: Today={self.today_count}, Goal={self.completion_percent}%, Next={self.deadline_text}")

        except Exception as e:
            print(f"STABILITY ERROR in update_metrics: {e}")
            import traceback
            traceback.print_exc()

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
