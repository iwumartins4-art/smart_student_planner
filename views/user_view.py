from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.app import MDApp

class UserView(MDScreen):
    full_name = StringProperty("Student User")
    email = StringProperty("student@example.edu")
    major = StringProperty("Computer Science")
    student_id = StringProperty("STU-123456")

    def on_enter(self):
        app = MDApp.get_running_app()
        if app.user_data:
            self.full_name = app.user_data.get("full_name", "N/A")
            self.email = app.user_data.get("email", "N/A")
            self.major = app.user_data.get("major", "N/A")
            self.student_id = app.user_data.get("student_id", "N/A")

    def go_back(self):
        self.manager.current = 'dashboard'
