import cv2
import numpy as np
from typing import Dict, Tuple, List

class BlobTool:
    """
    Blob detection tool for finding and analyzing connected components
    Useful for detecting defects, particles, or missing parts
    """
    
    def __init__(self, min_area: int = 50, max_area: int = 50000, threshold: int = 100):
        """
        Initialize Blob Detection Tool
        
        Args:
            min_area: Minimum blob area in pixels
            max_area: Maximum blob area in pixels
            threshold: Binary threshold value
        """
        self.min_area = min_area
        self.max_area = max_area
        self.threshold = threshold
    
    def inspect(self, image: np.ndarray) -> Dict:
        """
        Detect blobs in image
        
        Args:
            image: Input image
        
        Returns:
            dict: {
                'result': 'OK' or 'NG',
                'score': percentage,
                'blob_count': number of blobs detected,
                'blobs': list of blob data,
                'largest_blob_area': area of largest blob
            }
        """
        if image is None or image.size == 0:
            return {
                'result': 'NG',
                'score': 0,
                'blob_count': 0,
                'blobs': [],
                'largest_blob_area': 0
            }
        
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Binary threshold
            _, binary = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze blobs
            blobs = []
            largest_area = 0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                if self.min_area <= area <= self.max_area:
                    # Calculate blob properties
                    moments = cv2.moments(contour)
                    if moments['m00'] > 0:
                        cx = int(moments['m10'] / moments['m00'])
                        cy = int(moments['m01'] / moments['m00'])
                    else:
                        cx, cy = 0, 0
                    
                    x, y, w, h = cv2.boundingRect(contour)
                    perimeter = cv2.arcLength(contour, True)
                    circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
                    
                    blob_data = {
                        'area': float(area),
                        'centroid': (cx, cy),
                        'bounding_rect': (x, y, w, h),
                        'perimeter': float(perimeter),
                        'circularity': float(circularity),
                        'aspect_ratio': float(w / h) if h > 0 else 0
                    }
                    
                    blobs.append(blob_data)
                    largest_area = max(largest_area, area)
            
            # Determine result
            blob_count = len(blobs)
            score = min(100, (blob_count / 5) * 100)  # Normalize to 100%
            
            result = 'NG' if blob_count > 0 else 'OK'
            
            return {
                'result': result,
                'score': float(score),
                'blob_count': blob_count,
                'blobs': blobs,
                'largest_blob_area': float(largest_area)
            }
        except Exception as e:
            return {
                'result': 'ERROR',
                'score': 0,
                'blob_count': 0,
                'blobs': [],
                'largest_blob_area': 0,
                'error': str(e)
            }
    
    def detect_defects(self, image: np.ndarray) -> Dict:
        """
        Detect potential defects based on blob analysis
        
        Args:
            image: Input image
        
        Returns:
            dict: Defect analysis results
        """
        blob_result = self.inspect(image)
        
        defects = {
            'has_defects': blob_result['blob_count'] > 0,
            'defect_count': blob_result['blob_count'],
            'severity': 'NONE',
            'details': []
        }
        
        if blob_result['blob_count'] > 5:
            defects['severity'] = 'HIGH'
        elif blob_result['blob_count'] > 2:
            defects['severity'] = 'MEDIUM'
        elif blob_result['blob_count'] > 0:
            defects['severity'] = 'LOW'
        
        for blob in blob_result['blobs']:
            defects['details'].append({
                'type': 'defect',
                'area': blob['area'],
                'position': blob['centroid']
            })
        
        return defects
    
    def set_min_area(self, min_area: int):
        """Set minimum blob area"""
        self.min_area = max(1, min_area)
    
    def set_max_area(self, max_area: int):
        """Set maximum blob area"""
        self.max_area = max(self.min_area, max_area)
    
    def set_threshold(self, threshold: int):
        """Set binary threshold"""
        self.threshold = max(0, min(255, threshold))