from kivymd.uix.screen import MDScreen
from viewmodels.task_viewmodel import TaskViewModel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
import datetime

class TaskFormView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = TaskViewModel()
        self.editing_task_id = None

    def set_task_data(self, task):
        # task = (id, title, module, due_date, priority, notes, is_completed)
        self.editing_task_id = task[0]
        self.ids.title.text = str(task[1])
        self.ids.module.text = str(task[2])
        self.ids.due_date.text = str(task[3])
        self.ids.priority.text = str(task[4])
        self.ids.notes.text = str(task[5])
        self.ids.form_title.text = "Edit Task"

    def clear_form(self):
        self.editing_task_id = None
        self.ids.title.text = ""
        self.ids.module.text = ""
        self.ids.due_date.text = ""
        self.ids.priority.text = "Medium"
        self.ids.notes.text = ""
        self.ids.form_title.text = "Add Task"

    def open_priority_menu(self):
        from kivymd.uix.menu import MDDropdownMenu
        
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in ["High", "Medium", "Low"]
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.priority,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def set_item(self, text_item):
        self.ids.priority.text = text_item
        self.menu.dismiss()

    def show_date_picker(self):
        try:
            from kivymd.uix.pickers.datepicker.datepicker import MDModalDatePicker
            date_dialog = MDModalDatePicker()
            
            # TRIPLE-SAFE Binding: Catching all possible click events
            date_dialog.bind(on_save=self.on_date_save)
            date_dialog.bind(on_ok=self.on_date_save) 
            date_dialog.bind(on_cancel=self.on_date_cancel)
            
            date_dialog.open()
        except Exception as e:
            print(f"[UI ERROR] Date Picker Error: {e}")
            MDSnackbar(MDSnackbarText(text="Manual entry required.")).open()

    def on_date_save(self, instance, *args):
        try:
            # Official KivyMD 2.0 M3 method to retrieve selection
            dates = instance.get_date()
            print(f"[DEBUG] Captured from get_date(): {dates}")
            
            if dates and len(dates) > 0:
                # Set the first date in the list to your text field
                self.ids.due_date.text = str(dates[0])
            
            instance.dismiss()
        except Exception as e:
            print(f"[DEBUG] Final Save Error: {e}")
            instance.dismiss()


    def on_date_cancel(self, instance, *args):
        instance.dismiss()

    def handle_save(self):
        title = self.ids.title.text.strip()
        module = self.ids.module.text.strip()
        due_date = self.ids.due_date.text.strip()
        priority = self.ids.priority.text.strip()
        notes = self.ids.notes.text.strip()

        if not title or not due_date:
            MDSnackbar(MDSnackbarText(text="Title and Due Date are required!")).open()
            return

        if self.editing_task_id:
            success, message = self.viewmodel.edit_task(
                self.editing_task_id, title, module, due_date, priority, notes, 0
            )
        else:
            success, message = self.viewmodel.add_task(
                title, module, due_date, priority, notes
            )

        if success:
            MDSnackbar(MDSnackbarText(text=message)).open()
            self.manager.current = 'dashboard'
        else:
            MDSnackbar(MDSnackbarText(text=message)).open()

    def go_back(self):
        self.manager.current = 'dashboard'
