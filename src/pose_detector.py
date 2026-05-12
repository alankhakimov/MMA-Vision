"""
pose_detector.py - Pose Detection and Fighter Tracking
Uses YOLOv8 Pose with ByteTrack for consistent fighter identity across frames
"""
 
from ultralytics import YOLO
 
 
class PoseDetector:
    """
    Detects poses and tracks fighter identity across frames.
    Uses YOLOv8 Pose + ByteTrack for consistent tracking.
    """
    
    def __init__(self, model_name="yolov8n-pose", confidence=0.5):
        """
        Initialize pose detector.
        
        Args:
            model_name: YOLOv8 model variant
            confidence: Confidence threshold for detections
        """
        self.model = YOLO(model_name)
        self.confidence = confidence
    
    def detect(self, frame):
        """
        Detect poses and track fighters in frame.
        
        Args:
            frame: OpenCV frame (numpy array)
        
        Returns:
            results object with detections, keypoints, and track IDs
        """
        results = self.model(
            frame,
            conf=self.confidence,
            tracker="bytetrack.yaml",
            verbose=False
        )
        
        return results[0]
    
    def get_tracked_fighters(self, results):
        """
        Extract fighter data with track IDs and keypoints.
        """
        fighters = []
        
        if results.boxes is not None and len(results.boxes) > 0:
            for i, box in enumerate(results.boxes):
                # Use track ID if ByteTrack assigned one, otherwise use index
                track_id = int(box.id) if box.id is not None else i
                
                fighter = {
                    'track_id': track_id,
                    'confidence': float(box.conf),
                    'bbox': box.xyxy[0].tolist(),
                    'keypoints': results.keypoints.xy[i].tolist() if results.keypoints else None
                }
                fighters.append(fighter)
        
        return fighters