"""
load.py - Video Ingestion Gate
Handles video loading and validation using OpenCV
"""
 
import cv2
from pathlib import Path
 
 
def load_video(video_path):
    """
    Load and validate video file.
    
    Args:
        video_path: Path to input video (MOV or MP4)
    
    Returns:
        Tuple of (cv2.VideoCapture object, metadata dict)
    
    Raises:
        FileNotFoundError: If video file doesn't exist
        ValueError: If video is invalid or doesn't meet requirements
    """
    video_path = Path(video_path)
    
    # Check if file exists
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Check file extension
    if video_path.suffix.lower() not in ['.mov', '.mp4']:
        raise ValueError(f"Unsupported format: {video_path.suffix}. Use MOV or MP4.")
    
    # Open video with OpenCV
    cap = cv2.VideoCapture(str(video_path))
    
    # Check if video opened successfully
    if not cap.isOpened():
        raise ValueError(f"Failed to open video: {video_path}")
    
    # Extract metadata
    metadata = _get_video_metadata(cap, video_path)
    
    # Validate video
    _validate_video(metadata)

    # test that we can read first frame
    ret, _ = cap.read()
    if not ret:
        cap.release()
        raise ValueError("Cannot read video frames - file may be corrupted")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to start
    
    return cap, metadata
 
 
def _get_video_metadata(cap, video_path):
    """Extract video metadata from OpenCV VideoCapture object"""
    metadata = {
        'path': str(video_path),
        'filename': video_path.name,
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration_seconds': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    }
    return metadata
 
 
def _validate_video(metadata):
    """Validate video meets requirements"""
    # Check resolution
    if metadata['width'] == 0 or metadata['height'] == 0:
        raise ValueError(f"Invalid resolution: {metadata['width']}x{metadata['height']}")
    
    # Check FPS
    if metadata['fps'] == 0 or metadata['fps'] < 1:
        raise ValueError(f"Invalid FPS: {metadata['fps']}")
    
    # Check duration
    if metadata['duration_seconds'] < 5:   # Minimum 5 seconds
        raise ValueError(f"Video too short: {metadata['duration_seconds']:.2f}s (minimum: 5s)")
    
    if metadata['duration_seconds'] > 3600:  # 1 hour max
        raise ValueError(f"Video too long: {metadata['duration_seconds']:.2f}s (maximum: 3600s)")
    
    # Check frame count
    if metadata['frame_count'] == 0:
        raise ValueError("Unable to read video frames")
    
    # Check FPS
    MIN_FPS = 24
    if metadata['fps'] < MIN_FPS:
        raise ValueError(f"FPS too low: {metadata['fps']} (minimum: {MIN_FPS}fps)")