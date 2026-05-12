import cv2
from src.pose_detector import PoseDetector


def draw_skeleton(frame, keypoints, color=(0, 255, 0)):
    """
    Draw skeleton on frame from keypoints.
    YOLOv8 Pose uses 17 keypoints (COCO format).
    """
    # COCO skeleton connections (joint pairs)
    skeleton = [
        (0, 1), (0, 2), (1, 3), (2, 4),  # Head
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),  # Arms
        (5, 11), (6, 12), (11, 12),  # Torso
        (11, 13), (13, 15), (12, 14), (14, 16)  # Legs
    ]
    
    if keypoints is None:
        return
    
    keypoints = [[int(x), int(y)] for x, y in keypoints]
    
    # Draw connections
    for start_idx, end_idx in skeleton:
        if start_idx < len(keypoints) and end_idx < len(keypoints):
            pt1 = tuple(keypoints[start_idx])
            pt2 = tuple(keypoints[end_idx])
            
            # Only draw if both points are visible
            if pt1[0] > 0 and pt2[0] > 0:
                cv2.line(frame, pt1, pt2, color, 2)
    
    # Draw keypoints
    for kpt in keypoints:
        if kpt[0] > 0 and kpt[1] > 0:
            cv2.circle(frame, tuple(kpt), 4, color, -1)


def debug_loop(cap):
    """
    Interactive frame stepping through video with skeleton visualization.
    Controls:
      - SPACE: Play/Pause
      - D: Next frame (when paused)
      - A: Previous frame (when paused)
      - Q: Quit
    """
    paused = True
    frame_idx = 0
    detector = PoseDetector()
    fighter_registry = {}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break
        
        # Detect poses and track
        results = detector.detect(frame)
        fighters = detector.get_tracked_fighters(results)
        
        # Update registry
        for fighter in fighters:
            track_id = fighter['track_id']
            if track_id not in fighter_registry:
                fighter_registry[track_id] = {'first_seen': frame_idx}
            fighter_registry[track_id]['last_seen'] = frame_idx
        
        # Display frame
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Frame: {frame_idx} | Fighters: {len(fighters)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Draw skeletons for all fighters
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        for i, fighter in enumerate(fighters):
            track_id = fighter['track_id']
            color = colors[i % len(colors)]
            
            # Draw skeleton
            draw_skeleton(display_frame, fighter['keypoints'], color)
            
            # Draw label
            bbox = fighter['bbox']
            cv2.putText(display_frame, f"Fighter {track_id}", 
                       (int(bbox[0]), int(bbox[1])-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.imshow("Debug Loop", display_frame)
        
        frame_idx += 1
        
        # Keyboard input
        if paused:
            key = cv2.waitKey(0) & 0xFF
        else:
            key = cv2.waitKey(33) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
        elif key == ord('d') and paused:
            pass
        elif key == ord('a') and paused:
            if frame_idx > 1:
                frame_idx -= 2
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\nFighters detected:")
    for track_id, info in fighter_registry.items():
        print(f"  Fighter {track_id}: Frames {info['first_seen']}-{info['last_seen']}")