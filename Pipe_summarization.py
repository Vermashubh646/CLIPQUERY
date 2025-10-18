import os
import json
import glob
from Gemini_Description.Gemini import generate_scene_summary, load_llm


def run_summarization_pipeline(VIDEO_FILENAME):
    """
    Runs the main summarization pipeline.
    """
    
    env_path = 'D:\clipquery_github\CLIPQUERY\Gemini_Description\.env'
    model_object = load_llm(env_path)
    
    if not model_object:
        print("[Error] Model object is None. Cannot start pipeline.")
        print("Please check your .env file, API key, and model name in 'Gemini.py'.")
        return

    print(" Starting Context-Aware Summary Task ")
    

    sets_base_folder = os.path.join("video_processing/Sets/", VIDEO_FILENAME)
    
    if not os.path.isdir(sets_base_folder):
        print(f"[Fatal Error] Sets folder not found at: {sets_base_folder}")
        print("This folder is created by Pipe1.py. Please run it first.")
        return

    # 2. Find all 'set_...' folders in order
    set_folders = sorted(glob.glob(os.path.join(sets_base_folder, "set_*")))
    
    if not set_folders:
        print(f"[Error] No 'set_...' folders found in {sets_base_folder}.")
        print("Please run Pipe2.py to generate 'data.json' files.")
        return
        
    print(f"Found {len(set_folders)} sets to process.")

    # 3. This variable will hold the summary of the previous scene
    previous_summary_text = None
    all_summaries = []

    # 4. Loop through each set folder
    for set_folder in set_folders:
        data_json_path = os.path.join(set_folder, "data.json")
        
        if not os.path.exists(data_json_path):
            print(f" {set_folders} [Skipping] No 'data.json' found in {os.path.basename(set_folder)} (Run Pipe_summarization)")
            continue
        
        print(f"\nProcessing {os.path.basename(set_folder)}...")
        
        # Read the data from Pipe 2
        with open(data_json_path, 'r') as f:
            current_set_data = json.load(f)
        
        
        # 1. Copy the "previous format" data
        context_json_data = current_set_data.copy() 
        
        # 2. Add the new key with the context from the last loop
        context_json_data["previous_context"] = previous_summary_text
        
        # 3. Define the new file path
        context_json_path = os.path.join(set_folder, "context_data.json")
        
        # 4. Save the new file
        try:
            with open(context_json_path, 'w') as f:
                json.dump(context_json_data, f, indent=2)
            print(f"  Successfully saved 'context_data.json'")
        except Exception as e:
            print(f"  [Error] Could not write 'context_data.json': {e}")

        # Call the LLM to generate the new summary for *this* set
        print("  Calling Gemini to generate summary...")
        new_summary = generate_scene_summary(
            transcript=current_set_data["transcript"],
            visuals=current_set_data["visuals"],
            model=model_object,
            previous_summary=previous_summary_text 
        )
        
        if not new_summary:
            print("  Failed to generate summary for this set. Skipping.")
            continue 
        
        print(f"  Generated Summary: {new_summary}")

        # Create the 'summary_data.json' structure (as before)
        output_data = {
            "start_time": current_set_data["start_time"],
            "end_time": current_set_data["end_time"],
            "previous_description": previous_summary_text, 
            "scene_summary": new_summary,                 
            "transcript": current_set_data["transcript"], 
            "visuals": current_set_data["visuals"]        
        }
        
        # Save the 'summary_data.json' file (as before)
        output_json_path = os.path.join(set_folder, "summary_data.json")
        try:
            with open(output_json_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"  Successfully saved 'summary_data.json'")
            all_summaries.append(output_data)
        except Exception as e:
            print(f"  [Error] Could not write 'summary_data.json' file: {e}")

        # CRITICAL STEP: Update the 'previous_summary' for the *next* loop
        previous_summary_text = new_summary

    # Save one big file with all the new data (as before)
    all_data_file = os.path.join(sets_base_folder, "all_summary_data.json")
    try:
        with open(all_data_file, 'w') as f:
            json.dump(all_summaries, f, indent=2)
        print(f"\n--- ✨ Task Complete ---")
        print(f"All summary data combined and saved to: {all_data_file}")
    except Exception as e:
        print(f"\n[Error] Could not write combined summary JSON: {e}")


