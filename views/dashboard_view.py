from kivymd.uix.screen import MDScreen
from viewmodels.task_viewmodel import TaskViewModel
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

class TaskCard(MDCard):
    title = StringProperty()
    module = StringProperty()
    due_date = StringProperty()
    priority = StringProperty()
    is_completed = BooleanProperty()
    task_id = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set dynamic colors based on priority
        Clock.schedule_once(self.set_priority_color)

    def set_priority_color(self, *args):
        if self.priority == "High":
            self.ids.priority_bar.md_bg_color = (0.8, 0.2, 0.2, 1) # Red
        elif self.priority == "Medium":
            self.ids.priority_bar.md_bg_color = (0.9, 0.6, 0.2, 1) # Orange/Yellow
        else:
            self.ids.priority_bar.md_bg_color = (0.2, 0.6, 0.2, 1) # Green

class DashboardView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = TaskViewModel()

    def on_enter(self):
        self.refresh_tasks()

    def refresh_tasks(self, search_query=None):
        try:
            tasks = self.viewmodel.get_tasks(search_query)
            self.ids.task_list.clear_widgets()
            
            for task in tasks:
                # task structure: (id, title, module, due_date, priority, notes, is_completed)
                tid, title, mod, due, prio, notes, completed = task
                
                card = TaskCard(
                    title=str(title),
                    module=str(mod),
                    due_date=str(due),
                    priority=str(prio),
                    is_completed=bool(completed),
                    task_id=tid
                )
                # Link actions
                card.ids.check_btn.bind(on_release=lambda x, tid=tid, status=completed: self.toggle_task(tid, status))
                card.ids.delete_btn.bind(on_release=lambda x, tid=tid: self.delete_task(tid))
                card.bind(on_release=lambda x, t=task: self.edit_task(t))
                
                self.ids.task_list.add_widget(card)
        except Exception as e:
            print(f"UI Error: {e}")

    def toggle_task(self, task_id, current_status):
        self.viewmodel.toggle_status(task_id, current_status)
        self.refresh_tasks()
        MDSnackbar(MDSnackbarText(text="Task status updated")).open()

    def delete_task(self, task_id):
        self.viewmodel.delete_task(task_id)
        self.refresh_tasks()
        MDSnackbar(MDSnackbarText(text="Task deleted")).open()

    def edit_task(self, task_data):
        self.manager.get_screen('task_form').set_task_data(task_data)
        self.manager.current = 'task_form'

    def go_to_add_task(self):
        self.manager.get_screen('task_form').clear_form()
        self.manager.current = 'task_form'

    def handle_logout(self):
        self.manager.current = 'login'
