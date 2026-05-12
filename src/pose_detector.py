"""
pose_detector.py - Pose Detection and Fighter Tracking
Uses YOLOv8 Pose for pose estimation without external tracking
"""
from config import MODEL_NAME, CONFIDENCE_THRESHOLD
from ultralytics import YOLO


class PoseDetector:
    """
    Detects poses in frames without external tracking.
    Fighter identity is handled separately by downstream logic.
    """
    
    def __init__(self):
        self.model = YOLO(MODEL_NAME)
        self.confidence = CONFIDENCE_THRESHOLD
    
    def detect(self, frame):
        """
        Detect poses in frame.
        
        Args:
            frame: OpenCV frame (numpy array)
        
        Returns:
            results object with detections and keypoints
        """
        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False
        )
        
        return results[0]
    
    def get_fighters(self, results):
        """
        Extract fighter data with keypoints.
        Each fighter gets a temporary index ID within this frame.
        """
        fighters = []
        
        if results.boxes is not None and len(results.boxes) > 0:
            for i, box in enumerate(results.boxes):
                fighter = {
                    'frame_id': i,  # Temporary ID within this frame only
                    'confidence': float(box.conf),
                    'bbox': box.xyxy[0].tolist(),
                    'keypoints': results.keypoints.xy[i].tolist() if results.keypoints else None
                }
                fighters.append(fighter)
        
        return fighters