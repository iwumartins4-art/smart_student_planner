from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class SettingsView(MDScreen):
    def toggle_theme(self):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
        else:
            app.theme_cls.theme_style = "Dark"

    def go_back(self):
        self.manager.current = 'dashboard'
