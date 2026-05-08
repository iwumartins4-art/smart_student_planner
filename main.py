import os
import sys

# CRITICAL FIX: Force ANGLE backend on Windows to prevent Intel GPU crashes #
if sys.platform == 'win32':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from kivy.utils import platform

# Set window size only for desktop simulation #
if platform in ['win', 'linux', 'macosx']:
    Window.size = (360, 640)

# Absolute path loading to prevent file-not-found errors
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from kivy.properties import DictProperty

class SmartStudentPlanner(MDApp):
    user_data = DictProperty({})

    def build(self):
        # Certified Material 3 Palette
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        
        # Absolute path loading to prevent file-not-found errors
        from kivy.lang import Builder
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'login_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'register_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'dashboard_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'task_form_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'settings_view.kv'))
        Builder.load_file(os.path.join(PROJECT_ROOT, 'views', 'user_view.kv'))
 
        from kivy.uix.screenmanager import ScreenManager
        from views.login_view import LoginView
        from views.register_view import RegisterView
        from views.dashboard_view import DashboardView
        from views.task_form_view import TaskFormView
        from views.settings_view import SettingsView
        from views.user_view import UserView

        sm = ScreenManager()
        sm.add_widget(LoginView(name='login'))
        sm.add_widget(RegisterView(name='register'))
        sm.add_widget(DashboardView(name='dashboard'))
        sm.add_widget(TaskFormView(name='task_form'))
        sm.add_widget(SettingsView(name='settings'))
        sm.add_widget(UserView(name='user'))
        
        return sm

if __name__ == "__main__":
    try:
        from views.login_view import LoginView
        from views.register_view import RegisterView
        from views.dashboard_view import DashboardView
        from views.task_form_view import TaskFormView
        from views.settings_view import SettingsView
        from views.user_view import UserView
        
        SmartStudentPlanner().run()
        
    except Exception:
        import traceback
        # Attempt to write to a PUBLIC folder (Downloads) so the user can easily find it
        # On Android 10, /sdcard/Download/ is usually reachable
        log_found = False
        for folder in ["/sdcard/Download", "/storage/emulated/0/Download", os.path.expanduser("~")]:
            try:
                log_path = os.path.join(folder, "CRASH_LOG.txt")
                with open(log_path, "w") as f:
                    f.write("--- SMART STUDENT PLANNER CRASH LOG ---\n")
                    f.write(f"PROJECT_ROOT: {PROJECT_ROOT}\n")
                    f.write(traceback.format_exc())
                log_found = True
                break
            except:
                continue
        
        # Re-raise so the system still knows it crashed
        raise
