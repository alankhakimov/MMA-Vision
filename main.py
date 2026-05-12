from src.load import load_video
from src.debug_loop import debug_loop
from config import *

def main():
    print(f"Running in {'DEBUG' if DEBUG_MODE else 'PRODUCTION'} mode")
    base_path = VIDEO_INPUT_DIR
    filename = "IMG_9264.mov"

    cap, metadata = load_video(f"{base_path}/{filename}")
    debug_loop(cap)

 
if __name__ == "__main__":
    main() 