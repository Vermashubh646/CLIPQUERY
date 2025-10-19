import os
from video_processing.Full_extraction import process_video
from video_processing.Description_JSON_Generator import process_all_sets
from Frame_Description.BLIP import get_description, load_model_blip
from Audio_transcription.Whisper import load_model_whisper,get_transcript
from Pipe_summarization import run_summarization_pipeline
from DB_integrate import get_db_integrated


# Declare Path of Video
filename = "Breaking Bad - _I am the Danger_ Scene S4 E6 1080p.mp4"
VIDEO_PATH = os.path.join("video_processing/Video/",filename)
OUTPUT_PATH = os.path.join("video_processing/Sets/",filename)
SET_DURATION = 15.0  
FRAME_GRAB_RATE = 2.0


# # Get Sets Extracted
# process_video(VIDEO_PATH, OUTPUT_PATH, chunk_duration=15.0, frame_interval=2.0)

# # OUTPUT_PATH has the sets of out structure

# # Next let's Process each set
# process_all_sets(OUTPUT_PATH, FRAME_GRAB_RATE, get_transcript, get_description, load_model_blip, load_model_whisper)

# # Get the Descriptions
# run_summarization_pipeline(filename)

#Serealize and Embed

def run_full_video_pipeline(video_filename: str):
    """
    Runs the complete video processing pipeline (Pipes 1, 2, and 3)
    for a given video filename.
    
    :param video_filename: The name of the video file (e.g., "my_video.mp4")
                            located in 'video_processing/Video/'.
    """
    
    # --- 1. Define Constants & Paths ---
    SET_DURATION = 15.0
    FRAME_GRAB_RATE = 2.0
    
    VIDEO_PATH = os.path.join("video_processing/Video/", video_filename)
    OUTPUT_PATH = os.path.join("video_processing/Sets/", video_filename)
    
    # --- 2. Check if video exists ---
    if not os.path.exists(VIDEO_PATH):
        print(f"[Error] Video file not found: {VIDEO_PATH}")
        print("Please make sure the video is in the 'video_processing/Video' folder.")
        return # Exit function
        
    # --- 3. Run Pipe 1: Video to Sets ---
    print(f"--- 1/3: Extracting sets from {video_filename} ---")
    process_video(VIDEO_PATH, OUTPUT_PATH, chunk_duration=SET_DURATION, frame_interval=FRAME_GRAB_RATE)
    print(f"--- Set extraction complete. ---")
    
    # --- 4. Run Pipe 2: Sets to data.json ---
    print(f"--- 2/3: Generating descriptions (data.json) ---")
    # This call matches the structure from your snippet
    process_all_sets(
        OUTPUT_PATH, 
        FRAME_GRAB_RATE, 
        get_transcript, 
        get_description, 
        load_model_blip, 
        load_model_whisper
    )
    print(f"--- Description generation complete. ---")
    
    # --- 5. Run Pipe 3: data.json to summary.json ---
    print(f"--- 3/3: Generating final summaries (summary_data.json) ---")
    # This function (from your Pipe 3 script) handles its own looping
    run_summarization_pipeline(video_filename)
    print(f"--- Final summary generation complete. ---")
    
    print(f"\n--- 🚀 PIPELINE COMPLETE FOR {video_filename} ---")
    
    get_db_integrated(video_filename)
    
    return 1