import yaml
import json
import os
from typing import Any, Dict, Optional

class ConfigManager:
    """Manages application configuration from YAML file"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize ConfigManager
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Load configuration from YAML file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.config_path):
                print(f"⚠️ Config file not found: {self.config_path}")
                self.create_default_config()
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            print(f"✅ Config loaded: {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return False
    
    def create_default_config(self):
        """Create default configuration file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.write("# Default configuration\n")
            print(f"✅ Default config created: {self.config_path}")
        except Exception as e:
            print(f"❌ Error creating config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation)
        
        Args:
            key: Configuration key (e.g., 'camera.max_cameras')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return default
            
            return value if value is not None else default
        except Exception as e:
            print(f"❌ Error getting config key '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value by key (supports dot notation)
        
        Args:
            key: Configuration key (e.g., 'camera.max_cameras')
            value: Value to set
        
        Returns:
            bool: True if successful
        """
        try:
            keys = key.split('.')
            config = self.config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            print(f"✅ Config updated: {key} = {value}")
            return True
        except Exception as e:
            print(f"❌ Error setting config key '{key}': {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Save current configuration to YAML file
        
        Returns:
            bool: True if successful
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            print(f"✅ Config saved: {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def get_camera_config(self, camera_id: int = 0) -> Optional[Dict]:
        """
        Get camera configuration
        
        Args:
            camera_id: Camera ID (0-3)
        
        Returns:
            Camera configuration dictionary
        """
        cameras = self.get('camera.cameras', [])
        
        for cam in cameras:
            if cam.get('id') == camera_id:
                return cam
        
        return None
    
    def get_enabled_cameras(self) -> list:
        """
        Get list of enabled camera IDs
        
        Returns:
            List of enabled camera IDs
        """
        cameras = self.get('camera.cameras', [])
        return [cam['id'] for cam in cameras if cam.get('enabled', False)]
    
    def get_plc_config(self) -> Dict:
        """
        Get PLC configuration
        
        Returns:
            PLC configuration dictionary
        """
        return self.get('plc', {})
    
    def get_tool_config(self, tool_name: str) -> Optional[Dict]:
        """
        Get tool configuration
        
        Args:
            tool_name: Tool name (e.g., 'pattern', 'ocr')
        
        Returns:
            Tool configuration dictionary
        """
        return self.get(f'tools.{tool_name}')
    
    def export_json(self, filepath: str = "config.json") -> bool:
        """
        Export configuration to JSON file
        
        Args:
            filepath: Path to save JSON file
        
        Returns:
            bool: True if successful
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            print(f"✅ Config exported to JSON: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exporting config: {e}")
            return False
    
    def display_config(self):
        """Display current configuration"""
        print("\n" + "="*50)
        print("CURRENT CONFIGURATION")
        print("="*50)
        print(yaml.dump(self.config, default_flow_style=False))
        print("="*50 + "\n")
