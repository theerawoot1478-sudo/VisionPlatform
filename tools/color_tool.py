import cv2
import numpy as np
from typing import Dict, Tuple, List

class ColorTool:
    """
    Color detection tool for vision inspection
    Supports HSV, RGB color space detection
    """
    
    def __init__(self, method: str = "HSV", threshold: int = 50):
        """
        Initialize Color Tool
        
        Args:
            method: Color space method ("HSV" or "RGB")
            threshold: Color detection threshold
        """
        self.method = method
        self.threshold = threshold
        self.target_color = None
        self.lower_bound = None
        self.upper_bound = None
    
    def set_target_color(self, bgr_color: Tuple[int, int, int]):
        """
        Set target color in BGR format
        
        Args:
            bgr_color: Color in BGR format (e.g., (0, 255, 0) for green)
        """
        self.target_color = bgr_color
        self._calculate_bounds()
    
    def _calculate_bounds(self):
        """Calculate color detection bounds"""
        if self.target_color is None:
            return
        
        if self.method == "HSV":
            # Convert BGR to HSV
            color_bgr = np.uint8([[[self.target_color[0], self.target_color[1], self.target_color[2]]]])
            color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]
            
            # Calculate bounds
            h, s, v = color_hsv
            self.lower_bound = np.array([
                max(0, h - self.threshold),
                max(0, s - self.threshold),
                max(0, v - self.threshold)
            ])
            self.upper_bound = np.array([
                min(180, h + self.threshold),
                min(255, s + self.threshold),
                min(255, v + self.threshold)
            ])
        else:  # RGB
            self.lower_bound = np.array([
                max(0, self.target_color[0] - self.threshold),
                max(0, self.target_color[1] - self.threshold),
                max(0, self.target_color[2] - self.threshold)
            ])
            self.upper_bound = np.array([
                min(255, self.target_color[0] + self.threshold),
                min(255, self.target_color[1] + self.threshold),
                min(255, self.target_color[2] + self.threshold)
            ])
    
    def inspect(self, image: np.ndarray) -> Dict:
        """
        Detect color in image
        
        Args:
            image: Input image in BGR format
        
        Returns:
            dict: {
                'result': 'OK' or 'NG',
                'score': percentage (0-100),
                'color_detected': True/False,
                'pixel_count': number of pixels matching color
            }
        """
        if image is None or image.size == 0:
            return {
                'result': 'NG',
                'score': 0,
                'color_detected': False,
                'pixel_count': 0
            }
        
        if self.lower_bound is None or self.upper_bound is None:
            return {
                'result': 'NO_TARGET',
                'score': 0,
                'color_detected': False,
                'pixel_count': 0
            }
        
        try:
            if self.method == "HSV":
                # Convert to HSV
                image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                
                # Create mask
                mask = cv2.inRange(image_hsv, self.lower_bound, self.upper_bound)
            else:
                # Direct RGB comparison
                mask = cv2.inRange(image, self.lower_bound, self.upper_bound)
            
            # Calculate percentage
            total_pixels = image.shape[0] * image.shape[1]
            matching_pixels = cv2.countNonZero(mask)
            percentage = (matching_pixels / total_pixels) * 100
            
            result = 'OK' if percentage >= 10 else 'NG'
            
            return {
                'result': result,
                'score': float(percentage),
                'color_detected': percentage >= 10,
                'pixel_count': int(matching_pixels)
            }
        except Exception as e:
            return {
                'result': 'ERROR',
                'score': 0,
                'color_detected': False,
                'pixel_count': 0,
                'error': str(e)
            }
    
    def get_color_histogram(self, image: np.ndarray) -> Dict:
        """Get color histogram data"""
        if self.method == "HSV":
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([image_hsv], [0, 1], None, [256, 256], [0, 256, 0, 256])
        else:
            hist = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        
        return {
            'histogram': hist,
            'method': self.method
        }