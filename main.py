from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
import sys
import os

from kivy.utils import platform

# Set window size only for desktop simulation
if platform in ['win', 'linux', 'macosx']:
    Window.size = (360, 640)

# Robust path detection for mobile
if platform == 'android':
    PROJECT_ROOT = os.environ.get('PYTHONPATH', '.').split(':')[0]
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.task_form_view import TaskFormView
from views.settings_view import SettingsView

class SmartStudentPlanner(MDApp):
    def build(self):
        # Certified Material 3 Palette
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        
        # Absolute path loading to prevent file-not-found errors
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'login_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'dashboard_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'task_form_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'settings_view.kv'))
 
        sm = ScreenManager()
        sm.add_widget(LoginView(name='login'))
        sm.add_widget(DashboardView(name='dashboard'))
        sm.add_widget(TaskFormView(name='task_form'))
        sm.add_widget(SettingsView(name='settings'))
        
        return sm

if __name__ == "__main__":
    SmartStudentPlanner().run()
