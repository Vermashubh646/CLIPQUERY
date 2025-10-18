import os
import json
import glob
import re

#  HELPER FUNCTION

def read_time_info(info_file_path):
    """Reads the time_info.txt file and returns start/end times as floats."""
    times = {}
    try:
        with open(info_file_path, 'r') as f:
            for line in f:
                if line.startswith("start_time_seconds:"):
                    times['start_time'] = float(line.split(":")[1].strip())
                elif line.startswith("end_time_seconds:"):
                    times['end_time'] = float(line.split(":")[1].strip())
        if 'start_time' not in times or 'end_time' not in times:
            return None, None
        return times['start_time'], times['end_time']
    except Exception as e:
        print(f"  [Error] Could not read {info_file_path}: {e}")
        return None, None

# CORE PROCESSING FUNCTION

def process_set_folder(set_folder_path, frame_interval, transcript_func, caption_func, model_c, processor, device, model_t):
    """
    Processes a single set folder (e.g., 'set_001') and creates 
    a 'data.json' file inside it.

    :param set_folder_path: Path to the individual set folder.
    :param frame_interval: The rate (in sec) at which frames were captured (e.g., 2.0).
    :param transcript_func: The function to call for audio transcription (takes audio_path).
    :param caption_func: The function to call for image captioning (takes image_path).
    :return: A dictionary with the set's data, or None on failure.
    """
    print(f"\nProcessing folder: {os.path.basename(set_folder_path)}")
    
    
    # 1. Define all file paths
    time_info_file = os.path.join(set_folder_path, "time_info.txt")
    audio_file = os.path.join(set_folder_path, "audio.mp3")
    output_json_file = os.path.join(set_folder_path, "data.json")
    frame_files = sorted(glob.glob(os.path.join(set_folder_path, "frame_*.png")))

    # 2. Get Set Start/End Times
    set_start_time, set_end_time = read_time_info(time_info_file)
    if set_start_time is None:
        print(f"  [Skipping] Missing or corrupt time_info.txt in {set_folder_path}")
        return None

    # 3. Get Audio Transcript
    if not os.path.exists(audio_file):
        print(f"  [Skipping] Missing audio.mp3 in {set_folder_path}")
        return None
    transcript_text = transcript_func(audio_file, model_t)
    
    # 4. Process all visual frames
    visuals_list = []
    frame_number_regex = re.compile(r"frame_(\d+)\.png$")

    for frame_path in frame_files:
        match = frame_number_regex.search(frame_path)
        if not match:
            continue
            
        frame_num = int(match.group(1)) # 1-based index
        
        # (frame_num - 1) because frame_0001 is at the 0-second offset
        time_offset = (frame_num - 1) * frame_interval
        frame_timestamp = set_start_time + time_offset
        
        if frame_timestamp > set_end_time + 0.1: # 0.1s buffer for float math
            continue 

        # Get image caption
        caption_text = caption_func(frame_path,model_c, processor, device)
        
        visual_entry = {
            "timestamp": round(frame_timestamp, 3),
            "description": caption_text
        }
        visuals_list.append(visual_entry)
        
    # 5. Assemble the final structure
    final_data = {
        "start_time": round(set_start_time, 3),
        "end_time": round(set_end_time, 3),
        "transcript": transcript_text,
        "visuals": visuals_list
    }
    
    # 6. Save as JSON
    try:
        with open(output_json_file, 'w') as f:
            json.dump(final_data, f, indent=2)
        print(f"  Successfully created {os.path.basename(output_json_file)}")
    except Exception as e:
        print(f"  [Error] Could not write JSON file: {e}")
        return None
        
    return final_data

# MAIN CALLABLE FUNCTION

def process_all_sets(sets_base_folder, frame_interval, transcript_func, caption_func, load_model_capt, load_model_transc):
    """
    Finds all 'set_*' folders within a base directory and processes them.

    :param sets_base_folder: The path to the folder containing all sets (e.g., ".../Sets/Vid1.mp4").
    :param frame_interval: The rate (in sec) at which frames were captured (e.g., 2.0).
    :param transcript_func: The function to call for audio transcription.
    :param caption_func: The function to call for image captioning.
    :return: A list containing all data dictionaries from all sets.
    """
    
    model_c, processor, device = load_model_capt()
    model_t = load_model_transc()
    
    print("--- 🚀 Starting JSON Generation Task ---")
    if not os.path.isdir(sets_base_folder):
        print(f"[Fatal Error] Sets folder not found at: {sets_base_folder}")
        print("Please check your path.")
        return []

    print(f"Scanning for set folders in: {sets_base_folder}")
    
    # Find all 'set_...' folders
    set_folders = sorted(glob.glob(os.path.join(sets_base_folder, "set_*")))
    
    if not set_folders:
        print(f"[Error] No 'set_...' folders found in {sets_base_folder}.")
        return []

    all_data = []
    for folder_path in set_folders:
        if os.path.isdir(folder_path):
            data = process_set_folder(
                folder_path, 
                frame_interval, 
                transcript_func, 
                caption_func,
                model_c, 
                processor, 
                device,
                model_t
            )
            if data:
                all_data.append(data)
                
    # Save a single file with all data combined
    all_data_file = os.path.join(sets_base_folder, "all_sets_data.json")
    try:
        with open(all_data_file, 'w') as f:
            json.dump(all_data, f, indent=2)
        print(f"\n--- ✨ Task Complete ---")
        print(f"All data combined and saved to: {all_data_file}")
    except Exception as e:
        print(f"\n[Error] Could not write combined JSON file: {e}")
        
    return all_data