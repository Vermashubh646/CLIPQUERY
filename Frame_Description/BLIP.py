import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
import time

# --- 1. Setup ---
# Set a local cache directory to store the downloaded model
os.environ['HF_HOME'] = 'D:/huggingface_cache' 
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# --- 2. Load Model and Processor ---
# These lines will download the model on the first run and load it from the cache on subsequent runs.
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)
print("Model loaded successfully.")

# --- 3. Describe a Local Image ---
# ⚠️ **ACTION REQUIRED:** Change this path to the image you want to describe.


start = time.time()
for i in range(12):
    image_file = f"frame_{i:04d}.jpg"
    image_path = os.path.join("D:\\clipquery_github\\CLIPQUERY\\video_processing\\Frames\\Vid1.mp4", image_file)
    # Open the image file. The .convert('RGB') is important.
    raw_image = Image.open(image_path).convert('RGB')

    # Prepare the image for the model. Notice we don't pass any text here.
    inputs = processor(raw_image, return_tensors="pt").to(device)

    # --- 4. Generate the Description ---
    # You can increase `max_new_tokens` to get a longer, more detailed description.
    out = model.generate(**inputs, max_new_tokens=50) 
    
    # Decode the model's output into human-readable text
    description = processor.decode(out[0], skip_special_tokens=True)
    
    print("\n--- Image Description ---")
    print(description)
end = time.time()
print(f"\nTotal execution time: {end - start:.4f} seconds")


