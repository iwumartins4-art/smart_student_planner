import os
import sys
import logging
import traceback
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("startup_debug.log", mode='w')
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

try:
    logger.info("Starting app diagnostic...")
    
    logger.info("Checking dependencies...")
    import kivy
    import kivymd
    logger.info(f"Kivy version: {kivy.__version__}")
    logger.info(f"KivyMD version: {kivymd.__version__}")

    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.uix.screenmanager import ScreenManager
    from kivy.uix.label import Label

    class DiagnosticApp(MDApp):
        def build(self):
            logger.info("App build() started")
            
            # Create a simple root widget
            sm = ScreenManager()
            
            logger.info("Loading KV file (minimal test)...")
            try:
                # Create a dummy KV string to test loading
                kv_string = """
ScreenManager:
    Screen:
        name: 'test'
        MDLabel:
            text: 'Diagnostic Mode - Success'
            halign: 'center'
"""
                root = Builder.load_string(kv_string)
                logger.info("KV string loaded successfully")
                logger.info("Returning root widget")
                return root
            except Exception as e:
                logger.error(f"Failed to load KV: {e}")
                logger.error(traceback.format_exc())
                return Label(text="KV Load Failed")

    logger.info("Creating App instance...")
    app = DiagnosticApp()
    logger.info("App started successfully")
    app.run()

except Exception as e:
    logger.critical(f"Fatal crash during startup: {e}")
    logger.critical(traceback.format_exc())
    sys.exit(1)
