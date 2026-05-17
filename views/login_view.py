from kivymd.uix.screen import MDScreen
from viewmodels.auth_viewmodel import AuthViewModel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.app import MDApp
import webbrowser

class LoginView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = AuthViewModel()

    def handle_login(self, username, password):
        success, message = self.viewmodel.login(username, password)
        if success:
            app = MDApp.get_running_app()
            app.user_data = self.viewmodel.current_user_data
            self.manager.current = 'dashboard'
            MDSnackbar(MDSnackbarText(text=f"Welcome back, {app.user_data.get('full_name')}!")).open()
        else:
            MDSnackbar(MDSnackbarText(text=message)).open()

    def clear_fields(self):
        self.ids.username.text = ""
        self.ids.password.text = ""

    def open_github(self):
        webbrowser.open("https://github.com/iwumartins4-art/smart_student_planner")
