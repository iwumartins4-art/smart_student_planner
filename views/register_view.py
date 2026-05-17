from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

class RegisterView(MDScreen):
    def handle_register(self, full_name, username, email, password, confirm_password, major, student_id):
        if not all([full_name, username, email, password, major, student_id]):
            self.show_error("Please fill in all fields")
            return
            
        if "@" not in email or "." not in email:
            self.show_error("Please enter a valid email address")
            return
            
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
            
        from viewmodels.auth_viewmodel import AuthViewModel
        auth = AuthViewModel()
        success, message = auth.register(full_name, username, email, password, major, student_id)
        
        if success:
            MDSnackbar(MDSnackbarText(text="Account created successfully!")).open()
            self.go_to_login()
        else:
            self.show_error(message)

    def show_error(self, text):
        MDSnackbar(
            MDSnackbarText(
                text=text,
            ),
            y="24dp",
            pos_hint={"center_x": .5},
            size_hint_x=.8,
        ).open()

    def go_to_login(self):
        self.manager.current = 'login'
