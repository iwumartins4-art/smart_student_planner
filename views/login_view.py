from kivymd.uix.screen import MDScreen
from viewmodels.auth_viewmodel import AuthViewModel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

class LoginView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = AuthViewModel()

    def handle_login(self, username, password):
        success, message = self.viewmodel.login(username, password)
        if success:
            self.manager.current = 'dashboard'
            # M3 Snackbar usage
            MDSnackbar(MDSnackbarText(text=f"Welcome back, {username}!")).open()
        else:
            MDSnackbar(MDSnackbarText(text=message)).open()
