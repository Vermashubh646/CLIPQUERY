import torch
from PIL import Image
from transformers import Pix2StructForConditionalGeneration, Pix2StructProcessor
import os
import time

# --- 1. Setup ---
os.environ['HF_HOME'] = 'D:/huggingface_cache' 
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# --- 2. Load the CORRECT Fine-Tuned Model ---
# ⚠️ This is the corrected model name.
model_id = "google/pix2struct-textcaps-base" 

model = Pix2StructForConditionalGeneration.from_pretrained(model_id).to(device)
processor = Pix2StructProcessor.from_pretrained(model_id)
print("Model loaded successfully.")

start = time.time()
for i in range(12):
    image_file = f"frame_{i:04d}.jpg"
    image_path = os.path.join("D:\\clipquery_github\\CLIPQUERY\\video_processing\\Frames\\Vid1.mp4", image_file)
    raw_image = Image.open(image_path).convert('RGB')

    # This fine-tuned model does not require a text prompt.
    inputs = processor(images=raw_image, return_tensors="pt").to(device)

    # --- 4. Generate the Description ---
    out = model.generate(**inputs, max_new_tokens=50)
    
    # Decode the output into readable text
    description = processor.decode(out[0], skip_special_tokens=True)
    
    print("\n--- Image Description ---")
    print(description)

end = time.time()
print(f"\nTotal execution time: {end - start:.4f} seconds")