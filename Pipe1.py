import os
from video_processing.Full_extraction import process_video
from video_processing.Description_JSON_Generator import process_all_sets
from Frame_Description.BLIP import get_description, load_model_blip
from Audio_transcription.Whisper import load_model_whisper,get_transcript
from Pipe_summarization import run_summarization_pipeline



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



            
        