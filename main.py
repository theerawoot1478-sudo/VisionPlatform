#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision Platform Enterprise v2.0
Advanced Vision Inspection System with Multi-Camera Support

Author: Theerawoot
Email: theerawoot1478@gmail.com
GitHub: https://github.com/theerawoot1478-sudo/VisionPlatform
"""

import os
import sys
import logging
from pathlib import Path

# Disable CUDA to avoid GPU memory issues
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

from core.config_manager import ConfigManager
from ui.main_window import MainWindow

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


def check_dependencies():
    """
    Check if all required dependencies are installed
    """
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'yaml': 'PyYAML',
        'PyQt5': 'PyQt5',
        'reportlab': 'reportlab'
    }
    
    missing_packages = []
    
    for module, package_name in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("\n" + "="*60)
        print("❌ MISSING DEPENDENCIES")
        print("="*60)
        print("\nPlease install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        print("\nOr install all dependencies:")
        print("pip install -r requirements.txt")
        print("="*60 + "\n")
        return False
    
    return True


def check_directories():
    """
    Create required directories if they don't exist
    """
    required_dirs = [
        'database',
        'recipes',
        'images',
        'images/OK',
        'images/NG',
        'masters',
        'exports'
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Directory ready: {dir_name}")


def check_config():
    """
    Verify configuration file exists
    """
    config_path = Path('config.yaml')
    
    if not config_path.exists():
        logger.warning("⚠️  config.yaml not found. Creating default configuration...")
        config_mgr = ConfigManager('config.yaml')
        config_mgr.create_default_config()
    
    return config_path.exists()


def main():
    """
    Main application entry point
    """
    print("\n" + "="*60)
    print("🎥 VISION PLATFORM ENTERPRISE v2.0")
    print("Advanced Vision Inspection System")
    print("="*60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check directories
    check_directories()
    
    # Check configuration
    if not check_config():
        print("\n❌ Configuration file not found!")
        sys.exit(1)
    
    logger.info("Starting Vision Platform Enterprise v2.0")
    
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("Vision Platform Enterprise")
        app.setApplicationVersion("2.0.0")
        
        # Create and show main window
        logger.info("Creating main window...")
        window = MainWindow()
        window.show()
        
        logger.info("✅ Application started successfully")
        
        # Run application
        sys.exit(app.exec_())
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
