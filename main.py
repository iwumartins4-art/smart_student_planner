import os
import sys
import logging
import traceback
from pathlib import Path

# --- GLOBAL PATH CONFIGURATION ---
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
VIEWS_DIR = BASE_DIR / "views"
LOG_FILE = BASE_DIR / "app_startup.log"

# --- LOGGING SETUP ---
handlers = [logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')]
if not getattr(sys, 'frozen', False):
    if sys.stdout is not None:
        handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=handlers
)
logger = logging.getLogger("SmartStudentPlanner")

# --- CRITICAL STARTUP FIXES ---
if sys.platform == 'win32':
    logger.info("Windows detected: Forcing ANGLE (OpenGL ES) backend for stability.")
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

try:
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivy.uix.screenmanager import ScreenManager
    from kivy.utils import platform
    from kivy.properties import DictProperty
    
    # Delayed imports to ensure Kivy env is set
    import kivy
    import kivymd
    logger.info(f"Kivy version: {kivy.__version__}")
    logger.info(f"KivyMD version: {kivymd.__version__}")

except Exception as e:
    logger.critical(f"Failed to import core Kivy/KivyMD modules: {e}")
    logger.critical(traceback.format_exc())
    sys.exit(1)

# Set window size for desktop
if platform in ['win', 'linux', 'macosx']:
    Window.size = (360, 640)

def validate_assets():
    """Ensure critical assets exist before startup."""
    required_assets = [
        ASSETS_DIR / "logo.png",
    ]
    for asset in required_assets:
        if not asset.exists():
            logger.warning(f"Missing asset: {asset}. Creating a placeholder if possible.")
            # We don't crash, but we log it.

class SmartStudentPlanner(MDApp):
    user_data = DictProperty({})

    def build(self):
        logger.info("Initializing Application Build...")
        try:
            # Certified Material 3 Palette
            self.theme_cls.primary_palette = "Purple"
            self.theme_cls.theme_style = "Dark"
            
            # Loading KV files with absolute paths
            kv_files = [
                'login_view.kv',
                'register_view.kv',
                'dashboard_view.kv',
                'task_form_view.kv',
                'settings_view.kv',
                'user_view.kv'
            ]
            
            for kv_file in kv_files:
                kv_path = VIEWS_DIR / kv_file
                if kv_path.exists():
                    logger.info(f"Loading KV file: {kv_path}")
                    Builder.load_file(str(kv_path))
                else:
                    logger.error(f"KV file NOT FOUND: {kv_path}")
                    raise FileNotFoundError(f"Missing critical UI file: {kv_file}")

            # Import views inside build to avoid circular dependencies and ensure KV is loaded
            logger.info("Importing View classes...")
            from views.login_view import LoginView
            from views.register_view import RegisterView
            from views.dashboard_view import DashboardView
            from views.task_form_view import TaskFormView
            from views.settings_view import SettingsView
            from views.user_view import UserView

            logger.info("Creating ScreenManager...")
            sm = ScreenManager()
            
            logger.info("Adding widgets to ScreenManager...")
            sm.add_widget(LoginView(name='login'))
            sm.add_widget(RegisterView(name='register'))
            sm.add_widget(DashboardView(name='dashboard'))
            sm.add_widget(TaskFormView(name='task_form'))
            sm.add_widget(SettingsView(name='settings'))
            sm.add_widget(UserView(name='user_profile'))
            
            logger.info("Root widget created successfully.")
            return sm
            
        except Exception as e:
            logger.critical(f"Error during build(): {e}")
            logger.critical(traceback.format_exc())
            # Return a simple error label if build fails so the app doesn't just vanish
            from kivy.uix.label import Label
            return Label(text=f"Startup Error:\n{str(e)}", halign="center")

    def on_start(self):
        logger.info("App started successfully.")

if __name__ == "__main__":
    try:
        validate_assets()
        logger.info("Starting Smart Student Planner...")
        SmartStudentPlanner().run()
    except Exception as e:
        logger.critical(f"Application terminated unexpectedly: {e}")
        logger.critical(traceback.format_exc())
        # Final attempt to log to a reachable place if BASE_DIR is read-only
        try:
            with open(Path.home() / "SSP_CRITICAL_CRASH.log", "w") as f:
                f.write(traceback.format_exc())
        except:
            pass
        sys.exit(3221225477) # Maintain original exit code context
