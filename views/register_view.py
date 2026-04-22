from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

class RegisterView(MDScreen):
    def handle_register(self, username, password, confirm_password):
        if not username or not password:
            self.show_error("Please fill all fields")
            return
            
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
            
        # In a real app, you'd save this to the DB
        # For this demo, we'll just show success and go back to login
        MDSnackbar(
            MDSnackbarText(
                text="Registration Successful!",
            ),
            y="24dp",
            orientation="horizontal",
            pos_hint={"center_x": .5},
            size_hint_x=.8,
        ).open()
        
        self.go_to_login()

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
