from src.load import load_video

def main():
    video_path = r"C:\Users\Alank\Documents\GitHub\MMA_Video_Analysis\data\IMG_9264.mov"
    cap, metadata = load_video(video_path)
    #print(f"Loaded video: {metadata}")

    

if __name__ == "__main__":
    main()