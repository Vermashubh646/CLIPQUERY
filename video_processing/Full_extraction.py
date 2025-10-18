import os
import subprocess
import math
import shlex

def get_video_duration(video_path):
    """Gets the total duration of the video in seconds."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except FileNotFoundError:
        print("Error: ffprobe not found. Is FFmpeg installed and in your system's PATH?")
        return None
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return None

def format_time(seconds):
    """Converts seconds to HH:MM:SS.sss format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    return f"{hours:02}:{minutes:02}:{sec:06.3f}"

def run_ffmpeg_command(command):
    """Runs a given FFmpeg command."""
    args = shlex.split(command)
    try:
        subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running FFmpeg command: {e.stderr.decode()}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Is FFmpeg installed and in your system's PATH?")

def process_video(video_file_path, base_output_folder, chunk_duration=15.0, frame_interval=2.0):
    """
    Extracts audio clips, frames, and time info from a video file into structured folders.

    :param video_file_path: Absolute path to the source video file.
    :param base_output_folder: Absolute path to the main folder where sets will be created.
    :param chunk_duration: Duration of each audio/frame set in seconds.
    :param frame_interval: How often to grab a frame, in seconds.
    """
    
    print(f"Starting processing for: {video_file_path}")
    
    # 1. Check if video file exists
    if not os.path.exists(video_file_path):
        print(f"Error: Video file not found: {video_file_path}")
        return

    # 2. Get video duration
    total_duration = get_video_duration(video_file_path)
    if total_duration is None:
        return
    print(f"Total video duration: {format_time(total_duration)} ({total_duration:.2f}s)")

    # 3. Create the main output folder
    os.makedirs(base_output_folder, exist_ok=True)
    print(f"Created/found base folder: {base_output_folder}")

    # 4. Calculate number of sets
    num_sets = math.ceil(total_duration / chunk_duration)
    print(f"Video will be split into {num_sets} sets.")

    # 5. Loop and process each set
    for i in range(num_sets):
        set_number = i + 1
        set_name = f"set_{set_number:03d}"
        set_folder_path = os.path.join(base_output_folder, set_name)
        
        # Create the set folder
        os.makedirs(set_folder_path, exist_ok=True)
        print(f"\nProcessing {set_name}...")

        # Calculate start and end times
        start_time = i * chunk_duration
        current_chunk_duration = min(chunk_duration, total_duration - start_time)
        end_time = start_time + current_chunk_duration
        
        # --- Task 1: Extract Audio Clip ---
        audio_output_path = os.path.join(set_folder_path, "audio.mp3")
        audio_command = (
            f'ffmpeg -ss {start_time} -i "{video_file_path}" -t {current_chunk_duration} '
            f'-vn -q:a 2 "{audio_output_path}"'
        )
        print(f"  Extracting audio: {format_time(start_time)} to {format_time(end_time)}")
        run_ffmpeg_command(audio_command)

        # --- Task 2: Extract Frames ---
        frames_output_pattern = os.path.join(set_folder_path, "frame_%04d.png")
        frames_command = (
            f'ffmpeg -ss {start_time} -i "{video_file_path}" -t {current_chunk_duration} '
            f'-vf "fps=1/{frame_interval}" -q:v 2 "{frames_output_pattern}"'
        )
        print(f"  Extracting frames every {frame_interval}s...")
        run_ffmpeg_command(frames_command)

        # --- Task 3: Create TXT file ---
        info_file_path = os.path.join(set_folder_path, "time_info.txt")
        print(f"  Writing time info to {info_file_path}")
        with open(info_file_path, "w") as f:
            f.write(f"set_number: {set_number}\n")
            f.write(f"start_time_seconds: {start_time:.3f}\n")
            f.write(f"end_time_seconds: {end_time:.3f}\n")
            f.write(f"start_time_formatted: {format_time(start_time)}\n")
            f.write(f"end_time_formatted: {format_time(end_time)}\n")

    print("\nProcessing complete!")

