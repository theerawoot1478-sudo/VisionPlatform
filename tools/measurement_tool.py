import cv2
import numpy as np
from typing import Dict, Tuple, List

class MeasurementTool:
    """
    Measurement tool for dimension and distance measurements
    Useful for checking product dimensions, distances, and geometry
    """
    
    def __init__(self, unit: str = "pixel", pixels_per_mm: float = 1.0):
        """
        Initialize Measurement Tool
        
        Args:
            unit: Measurement unit ("pixel" or "mm")
            pixels_per_mm: Calibration factor (pixels per mm)
        """
        self.unit = unit
        self.pixels_per_mm = pixels_per_mm
        self.calibration_done = False
    
    def calibrate(self, reference_length_pixels: int, reference_length_mm: float) -> bool:
        """
        Calibrate measurement tool using reference length
        
        Args:
            reference_length_pixels: Measured length in pixels
            reference_length_mm: Actual length in mm
        
        Returns:
            bool: True if calibration successful
        """
        try:
            if reference_length_pixels <= 0 or reference_length_mm <= 0:
                return False
            
            self.pixels_per_mm = reference_length_pixels / reference_length_mm
            self.calibration_done = True
            return True
        except Exception as e:
            print(f"❌ Calibration error: {e}")
            return False
    
    def measure_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> Dict:
        """
        Measure distance between two points
        
        Args:
            point1: First point (x, y)
            point2: Second point (x, y)
        
        Returns:
            dict: {
                'distance_pixels': float,
                'distance_mm': float,
                'distance_unit': str
            }
        """
        try:
            dx = point2[0] - point1[0]
            dy = point2[1] - point1[1]
            
            distance_pixels = np.sqrt(dx**2 + dy**2)
            
            if self.unit == "mm" and self.calibration_done:
                distance_mm = distance_pixels / self.pixels_per_mm
            else:
                distance_mm = distance_pixels
            
            return {
                'distance_pixels': float(distance_pixels),
                'distance_mm': float(distance_mm),
                'distance_unit': self.unit
            }
        except Exception as e:
            return {
                'error': str(e),
                'distance_pixels': 0,
                'distance_mm': 0
            }
    
    def measure_contour_width_height(self, contour: np.ndarray) -> Dict:
        """
        Measure width and height of contour
        
        Args:
            contour: OpenCV contour
        
        Returns:
            dict: Dimension measurements
        """
        try:
            x, y, w, h = cv2.boundingRect(contour)
            
            if self.unit == "mm" and self.calibration_done:
                width_mm = w / self.pixels_per_mm
                height_mm = h / self.pixels_per_mm
            else:
                width_mm = w
                height_mm = h
            
            return {
                'width_pixels': int(w),
                'height_pixels': int(h),
                'width_mm': float(width_mm),
                'height_mm': float(height_mm),
                'unit': self.unit
            }
        except Exception as e:
            return {'error': str(e)}
    
    def measure_circle(self, image: np.ndarray, center: Tuple[int, int], 
                       radius_pixels: int) -> Dict:
        """
        Measure circle diameter
        
        Args:
            image: Input image
            center: Circle center (x, y)
            radius_pixels: Radius in pixels
        
        Returns:
            dict: Circle measurements
        """
        try:
            diameter_pixels = radius_pixels * 2
            
            if self.unit == "mm" and self.calibration_done:
                diameter_mm = diameter_pixels / self.pixels_per_mm
                radius_mm = radius_pixels / self.pixels_per_mm
            else:
                diameter_mm = diameter_pixels
                radius_mm = radius_pixels
            
            area_pixels = np.pi * (radius_pixels ** 2)
            
            if self.unit == "mm" and self.calibration_done:
                area_mm = np.pi * (radius_mm ** 2)
            else:
                area_mm = area_pixels
            
            return {
                'center': center,
                'radius_pixels': int(radius_pixels),
                'diameter_pixels': int(diameter_pixels),
                'radius_mm': float(radius_mm),
                'diameter_mm': float(diameter_mm),
                'area_pixels': float(area_pixels),
                'area_mm': float(area_mm),
                'unit': self.unit
            }
        except Exception as e:
            return {'error': str(e)}
    
    def inspect(self, image: np.ndarray, target_dimension: float) -> Dict:
        """
        Inspect if dimensions match target
        
        Args:
            image: Input image
            target_dimension: Target dimension in current unit
        
        Returns:
            dict: Inspection result
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) == 0:
                return {
                    'result': 'NG',
                    'score': 0,
                    'reason': 'No object detected'
                }
            
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            dim = self.measure_contour_width_height(largest_contour)
            
            if 'error' in dim:
                return {
                    'result': 'ERROR',
                    'score': 0
                }
            
            # Compare with target
            measured_dim = dim.get('width_mm' if self.unit == 'mm' else 'width_pixels', 0)
            tolerance = target_dimension * 0.1  # 10% tolerance
            
            diff = abs(measured_dim - target_dimension)
            
            result = 'OK' if diff <= tolerance else 'NG'
            score = max(0, 100 - (diff / target_dimension * 100))
            
            return {
                'result': result,
                'score': float(score),
                'measured': float(measured_dim),
                'target': float(target_dimension),
                'tolerance': float(tolerance),
                'difference': float(diff),
                'unit': self.unit
            }
        except Exception as e:
            return {
                'result': 'ERROR',
                'score': 0,
                'error': str(e)
            }
    
    def get_calibration_status(self) -> Dict:
        """Get calibration status"""
        return {
            'calibration_done': self.calibration_done,
            'pixels_per_mm': self.pixels_per_mm,
            'unit': self.unit
        }