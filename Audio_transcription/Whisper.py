import whisper
import torch
import os
import time

def load_model_whisper():
    custom_dir = "D:\clipquery_github\CLIPQUERY\OpenAI_cache"

    os.makedirs(custom_dir,exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = whisper.load_model('small',download_root=custom_dir)
    model.to(device)
    return model


# filename="Song.mp3"

# audio_path="../video_processing/Audio"

# start = time.time()
# result = model.transcribe(os.path.join(audio_path,filename))
# end = time.time()
# print(f"\nTotal execution time: {end - start:.4f} seconds")
# print("Transcription:")
# print(result['text'])

def get_transcript(file_path,model):
    result = model.transcribe(file_path)
    
    return result['text']