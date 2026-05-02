from kivymd.uix.screen import MDScreen
from viewmodels.task_viewmodel import TaskViewModel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import datetime

class TaskFormView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = TaskViewModel()
        self.editing_task_id = None
        self._menu = None

    def set_task_data(self, task):
        # task = (id, title, module, due_date, priority, notes, status, is_completed)
        self.editing_task_id = task[0]
        self.ids.title.text = str(task[1])
        self.ids.module.text = str(task[2])
        self.ids.due_date.text = str(task[3])
        self.ids.priority.text = str(task[4])
        self.ids.notes.text = str(task[5])
        
        # STRICT STRING BINDING - NO TRANSFORMATION
        db_status = str(task[6])
        if db_status in ["Not Started", "In Progress", "Completed"]:
            self.ids.status.text = db_status
        else:
            # Fallback for unexpected data
            self.ids.status.text = "Not Started"
            
        self.ids.form_title.text = "Edit Task"

    def clear_form(self):
        self.editing_task_id = None
        self.ids.title.text = ""
        self.ids.module.text = ""
        self.ids.due_date.text = ""
        self.ids.priority.text = "Medium"
        self.ids.status.text = "Not Started"
        self.ids.notes.text = ""
        self.ids.form_title.text = "Add Task"

    def open_priority_menu(self):
        if self._menu: self._menu.dismiss()
        menu_items = [{"text": f"{i}", "on_release": lambda *x, p=f"{i}": self.set_item(self.ids.priority, p)} for i in ["High", "Medium", "Low"]]
        self._menu = MDDropdownMenu(caller=self.ids.priority, items=menu_items, width=dp(160))
        self._menu.open()

    def open_status_menu(self):
        if self._menu: self._menu.dismiss()
        # USE ONLY THESE EXACT STRINGS
        menu_items = [{"text": f"{i}", "on_release": lambda *x, s=f"{i}": self.set_item(self.ids.status, s)} for i in ["Not Started", "In Progress", "Completed"]]
        self._menu = MDDropdownMenu(caller=self.ids.status, items=menu_items, width=dp(200))
        self._menu.open()

    def set_item(self, widget, text_item):
        widget.text = text_item
        if self._menu: 
            self._menu.dismiss()
            self._menu = None

    def show_date_picker(self):
        try:
            from kivymd.uix.pickers.datepicker.datepicker import MDModalDatePicker
            date_dialog = MDModalDatePicker()
            date_dialog.bind(on_ok=self.on_date_ok)
            date_dialog.bind(on_cancel=lambda x, *a: x.dismiss())
            date_dialog.open()
        except Exception as e:
            print(f"[STABILITY] DatePicker Error: {e}")
            MDSnackbar(MDSnackbarText(text="Manual entry required.")).open()

    def on_date_ok(self, instance, *args):
        try:
            dates = instance.get_date()
            if dates:
                self.ids.due_date.text = dates[0].strftime("%Y-%m-%d")
            instance.dismiss()
        except Exception as e:
            print(f"[STABILITY] Date Save Error: {e}")
            instance.dismiss()

    def handle_save(self):
        title, mod, due, prio, status, notes = self.ids.title.text.strip(), self.ids.module.text.strip(), self.ids.due_date.text.strip(), self.ids.priority.text, self.ids.status.text, self.ids.notes.text
        if not title or not due:
            MDSnackbar(MDSnackbarText(text="Title and Due Date are required!")).open()
            return

        if self.editing_task_id:
            success, message = self.viewmodel.edit_task(self.editing_task_id, title, mod, due, prio, notes, status, 0)
        else:
            success, message = self.viewmodel.add_task(title, mod, due, prio, notes, status)

        if success:
            self.manager.current = 'dashboard'
            MDSnackbar(MDSnackbarText(text=message)).open()

    def go_back(self):
        self.manager.current = 'dashboard'
