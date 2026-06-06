import cv2
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class MultiCameraManager:
    """
    Manager for multiple USB cameras (1-4 cameras)
    Handles simultaneous capture from multiple cameras
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize Multi Camera Manager
        
        Args:
            config: Camera configuration from config.yaml
        """
        self.config = config or {}
        self.max_cameras = self.config.get('max_cameras', 4)
        self.cameras = {}  # {camera_id: VideoCapture}
        self.frames = {}   # {camera_id: current_frame}
        self.connected_cameras = []
        
        self._initialize_cameras()
    
    def _initialize_cameras(self):
        """Initialize configured cameras"""
        enabled_cameras = self.config.get('cameras', [])
        
        for cam_config in enabled_cameras:
            cam_id = cam_config.get('id', 0)
            enabled = cam_config.get('enabled', False)
            
            if enabled and cam_id < self.max_cameras:
                self.connect_camera(cam_id, cam_config)
    
    def connect_camera(self, camera_id: int, config: dict = None) -> bool:
        """
        Connect to specific camera
        
        Args:
            camera_id: Camera index (0-3)
            config: Camera configuration
        
        Returns:
            bool: True if successful
        """
        if camera_id >= self.max_cameras:
            print(f"❌ Camera ID {camera_id} exceeds max cameras ({self.max_cameras})")
            return False
        
        try:
            cap = cv2.VideoCapture(camera_id)
            
            if not cap.isOpened():
                print(f"❌ Cannot open camera {camera_id}")
                return False
            
            # Apply camera settings if provided
            if config:
                self._apply_camera_settings(cap, config)
            
            self.cameras[camera_id] = cap
            self.connected_cameras.append(camera_id)
            self.connected_cameras.sort()
            
            print(f"✅ Camera {camera_id} connected")
            logger.info(f"Camera {camera_id} connected")
            return True
        except Exception as e:
            print(f"❌ Error connecting camera {camera_id}: {e}")
            logger.error(f"Error connecting camera {camera_id}: {e}")
            return False
    
    def disconnect_camera(self, camera_id: int) -> bool:
        """
        Disconnect specific camera
        
        Args:
            camera_id: Camera index
        
        Returns:
            bool: True if successful
        """
        try:
            if camera_id in self.cameras:
                cap = self.cameras[camera_id]
                cap.release()
                del self.cameras[camera_id]
                
                if camera_id in self.connected_cameras:
                    self.connected_cameras.remove(camera_id)
                
                if camera_id in self.frames:
                    del self.frames[camera_id]
                
                print(f"✅ Camera {camera_id} disconnected")
                logger.info(f"Camera {camera_id} disconnected")
                return True
            else:
                print(f"⚠️ Camera {camera_id} not connected")
                return False
        except Exception as e:
            print(f"❌ Error disconnecting camera {camera_id}: {e}")
            logger.error(f"Error disconnecting camera {camera_id}: {e}")
            return False
    
    def _apply_camera_settings(self, cap: cv2.VideoCapture, config: dict):
        """Apply camera settings from config"""
        try:
            exposure = config.get('exposure', 100)
            gain = config.get('gain', 1.0)
            
            # Note: Not all cameras support these properties
            # Adjust based on your camera model
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
            cap.set(cv2.CAP_PROP_GAIN, gain)
            
        except Exception as e:
            logger.warning(f"Could not apply camera settings: {e}")
    
    def read_frame(self, camera_id: int) -> Tuple[bool, Optional]:
        """
        Read frame from specific camera
        
        Args:
            camera_id: Camera index
        
        Returns:
            Tuple: (success, frame)
        """
        try:
            if camera_id not in self.cameras:
                return False, None
            
            cap = self.cameras[camera_id]
            ret, frame = cap.read()
            
            if ret:
                self.frames[camera_id] = frame
            
            return ret, frame
        except Exception as e:
            logger.error(f"Error reading camera {camera_id}: {e}")
            return False, None
    
    def read_all_frames(self) -> dict:
        """
        Read frames from all connected cameras
        
        Returns:
            dict: {camera_id: frame}
        """
        frames = {}
        
        for cam_id in self.connected_cameras:
            ret, frame = self.read_frame(cam_id)
            if ret:
                frames[cam_id] = frame
        
        return frames
    
    def get_frame(self, camera_id: int) -> Optional:
        """Get last captured frame from camera"""
        return self.frames.get(camera_id)
    
    def get_all_frames(self) -> dict:
        """Get last captured frames from all cameras"""
        return self.frames.copy()
    
    def set_camera_property(self, camera_id: int, prop_id: int, value: float) -> bool:
        """
        Set camera property
        
        Args:
            camera_id: Camera index
            prop_id: OpenCV property ID
            value: Property value
        
        Returns:
            bool: True if successful
        """
        try:
            if camera_id not in self.cameras:
                return False
            
            cap = self.cameras[camera_id]
            return cap.set(prop_id, value)
        except Exception as e:
            logger.error(f"Error setting property on camera {camera_id}: {e}")
            return False
    
    def get_camera_property(self, camera_id: int, prop_id: int) -> Optional[float]:
        """
        Get camera property value
        
        Args:
            camera_id: Camera index
            prop_id: OpenCV property ID
        
        Returns:
            float: Property value or None
        """
        try:
            if camera_id not in self.cameras:
                return None
            
            cap = self.cameras[camera_id]
            return cap.get(prop_id)
        except Exception as e:
            logger.error(f"Error getting property from camera {camera_id}: {e}")
            return None
    
    def get_camera_resolution(self, camera_id: int) -> Tuple[int, int]:
        """
        Get camera resolution
        
        Args:
            camera_id: Camera index
        
        Returns:
            Tuple: (width, height)
        """
        width = int(self.get_camera_property(
            camera_id,
            cv2.CAP_PROP_FRAME_WIDTH
        ) or 640)
        height = int(self.get_camera_property(
            camera_id,
            cv2.CAP_PROP_FRAME_HEIGHT
        ) or 480)
        
        return width, height
    
    def set_camera_resolution(self, camera_id: int, width: int, height: int) -> bool:
        """Set camera resolution"""
        try:
            self.set_camera_property(camera_id, cv2.CAP_PROP_FRAME_WIDTH, width)
            self.set_camera_property(camera_id, cv2.CAP_PROP_FRAME_HEIGHT, height)
            print(f"✅ Camera {camera_id} resolution set to {width}x{height}")
            return True
        except Exception as e:
            logger.error(f"Error setting resolution: {e}")
            return False
    
    def get_connected_cameras(self) -> List[int]:
        """Get list of connected camera IDs"""
        return self.connected_cameras.copy()
    
    def get_camera_count(self) -> int:
        """Get number of connected cameras"""
        return len(self.connected_cameras)
    
    def release_all(self):
        """Release all cameras"""
        for cam_id in list(self.cameras.keys()):
            self.disconnect_camera(cam_id)
        
        print(f"✅ All cameras released")
        logger.info("All cameras released")
    
    def get_status(self) -> dict:
        """Get status of all cameras"""
        status = {
            'total_connected': self.get_camera_count(),
            'max_cameras': self.max_cameras,
            'cameras': {}
        }
        
        for cam_id in self.connected_cameras:
            width, height = self.get_camera_resolution(cam_id)
            status['cameras'][cam_id] = {
                'id': cam_id,
                'connected': cam_id in self.cameras,
                'resolution': f"{width}x{height}",
                'fps': int(self.get_camera_property(cam_id, cv2.CAP_PROP_FPS) or 30)
            }
        
        return status
    
    def display_status(self):
        """Display camera status"""
        status = self.get_status()
        print("\n" + "="*50)
        print("CAMERA STATUS")
        print("="*50)
        print(f"Connected Cameras: {status['total_connected']}/{status['max_cameras']}")
        
        for cam_id, cam_info in status['cameras'].items():
            print(f"\nCamera {cam_id}:")
            print(f"  Resolution: {cam_info['resolution']}")
            print(f"  FPS: {cam_info['fps']}")
        
        print("="*50 + "\n")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release_all()
