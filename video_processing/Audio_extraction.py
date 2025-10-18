from moviepy import VideoFileClip
import os
def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file and saves it to a specified path.

    Args:
        video_path (str): The full path to the input MP4 video file.
        audio_path (str): The full path where the extracted audio (e.g., MP3) will be saved.
    """
    try:
        # Load the video file
        video_clip = VideoFileClip(video_path)
        
        # Extract the audio from the video clip
        audio_clip = video_clip.audio
        
        # Write the audio clip to a new file
        audio_clip.write_audiofile(audio_path)
        
        # Close the clips to free up resources
        audio_clip.close()
        video_clip.close()
        
        print(f"✅ Audio successfully extracted to: {audio_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# --- Example of how to use the function ---
if __name__ == "_main_":

    filename='Vid1.mp4'

    # 1. Define the path to your video file
    input_video_path = 'Video' 

    # 2. Define the path for the output audio file
    output_audio_path = 'Audio'

    # 3. Call the function to perform the extraction
    extract_audio(os.path.join(input_video_path,filename), os.path.join(output_audio_path,filename.split('.')[0]+".mp3"))