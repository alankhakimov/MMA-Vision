"""
config.py - Configuration for MMA Video Analysis System
"""
 
# Debug mode - uses faster models for quicker iteration
DEBUG_MODE = True
 
# Model selection
if DEBUG_MODE:
    MODEL_NAME = "yolov8n-pose"  # Nano - fast
else:
    MODEL_NAME = "yolov8m-pose"  # Medium - accurate
 
# Pose detection
CONFIDENCE_THRESHOLD = 0.5
 
# Video processing
FRAME_SKIP = 1  # Process every Nth frame (1 = every frame)
 
# Paths
VIDEO_INPUT_DIR = "data"
 
# Displayw
DISPLAY_SKELETON = True
DISPLAY_BBOX = False
DISPLAY_CONFIDENCE = False