import cv2
import os

def extract_frames(video_path, output_folder, interval=1):
    """
    Extracts frames from a video at a specified time interval.

    :param video_path: Path to the input video file.
    :param output_folder: Path to the directory where frames will be saved.
    :param interval: Time interval in seconds between frame extractions.
    """
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    # Get the frames per second (fps) of the video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: Could not determine video FPS. Assuming 30 FPS.")
        fps = 30 # Default to 30 if FPS cannot be read
    
    print(f"Video FPS: {fps}")

    frame_count = 0
    saved_frame_count = 0
    
    # Calculate the frame interval based on the desired time interval
    frame_interval = int(fps * interval)

    while True:
        # Read the next frame
        success, frame = video_capture.read()
        
        # If there are no more frames, break the loop
        if not success:
            break
        
        # Check if the current frame is one to be saved
        if frame_count % frame_interval == 0:
            # Construct the output file path
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")
            
            # Save the frame as a JPEG image
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")
            saved_frame_count += 1
            
        frame_count += 1

    # Release the video capture object
    video_capture.release()
    print(f"\nExtraction complete. Total frames saved: {saved_frame_count}")


if __name__ == "__main__":
    filename='Vid1.mp4'
    # Specify the path to your video file
    input_video_path = "Video"
    
    # Specify the folder where you want to save the extracted frames
    output_frames_folder = "Frames"
    
    # Set the time interval (in seconds) for extracting frames
    # For example, interval=5 will save one frame every 5 seconds.
    extraction_interval = 5  # seconds

    # Call the function to start the frame extraction process
    extract_frames(os.path.join(input_video_path,filename), os.path.join(output_frames_folder,filename), interval=extraction_interval)

