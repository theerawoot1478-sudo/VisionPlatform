"""
Vision Platform Enhanced Main Application
Version 2.0 with Config Manager Integration and Error Handling
"""

import os
import sys
import logging
import traceback
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vision_platform.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from core.config_manager import ConfigManager
    from ui.main_window import MainWindow
except ImportError as e:
    logger.error(f"Import Error: {e}")
    print(f"\n❌ Failed to import required modules: {e}")
    sys.exit(1)


class VisionPlatformApp:
    """Main application controller"""
    
    def __init__(self):
        self.config_mgr = None
        self.app = None
        self.window = None
        
    def check_dependencies(self) -> bool:
        """Check if all required packages are installed"""
        try:
            required = {
                'cv2': 'opencv-python',
                'numpy': 'numpy',
                'yaml': 'PyYAML',
                'PyQt5': 'PyQt5',
                'reportlab': 'reportlab'
            }
            
            missing = []
            for module, pkg_name in required.items():
                try:
                    __import__(module)
                except ImportError:
                    missing.append(pkg_name)
            
            if missing:
                print("\n" + "="*60)
                print("❌ MISSING DEPENDENCIES")
                print("="*60)
                print("\nPlease install missing packages:")
                print(f"pip install {' '.join(missing)}")
                print("\nOr install all dependencies:")
                print("pip install -r requirements.txt")
                print("="*60 + "\n")
                return False
            
            logger.info("✅ All dependencies installed")
            return True
        except Exception as e:
            logger.error(f"Dependency check error: {e}")
            return False
    
    def create_directories(self):
        """Create required directories"""
        try:
            dirs = ['database', 'recipes', 'images', 'images/OK', 'images/NG', 'masters', 'exports', 'logs']
            
            for dir_name in dirs:
                Path(dir_name).mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Directory ready: {dir_name}")
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
            raise
    
    def load_config(self) -> bool:
        """Load configuration"""
        try:
            self.config_mgr = ConfigManager('config.yaml')
            
            if not self.config_mgr.config:
                logger.warning("⚠️ Configuration is empty, using defaults")
                return False
            
            logger.info("✅ Configuration loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Configuration load error: {e}")
            return False
    
    def run(self):
        """Run the application"""
        try:
            print("\n" + "="*60)
            print("🎥 VISION PLATFORM ENTERPRISE v2.0")
            print("Advanced Vision Inspection System")
            print("="*60 + "\n")
            
            # Check dependencies
            if not self.check_dependencies():
                sys.exit(1)
            
            # Create directories
            self.create_directories()
            
            # Load configuration
            if not self.load_config():
                logger.warning("⚠️ Using default configuration")
            
            logger.info("Starting Vision Platform Enterprise v2.0")
            
            # Create Qt application
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("Vision Platform Enterprise")
            self.app.setApplicationVersion("2.0.0")
            
            logger.info("Creating main window...")
            
            # Create and show main window
            self.window = MainWindow(self.config_mgr)
            self.window.show()
            
            logger.info("✅ Application started successfully")
            print("\n✅ Application started successfully\n")
            
            # Run application
            sys.exit(self.app.exec_())
        
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            error_msg = f"Error starting application:\n{str(e)}\n\n{traceback.format_exc()}"
            print(f"\n❌ {error_msg}\n")
            
            if self.app:
                QMessageBox.critical(None, "Fatal Error", error_msg)
            
            sys.exit(1)


def main():
    """Entry point"""
    app_controller = VisionPlatformApp()
    app_controller.run()


if __name__ == "__main__":
    main()
