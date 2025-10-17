import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import os

# Set the cache directory for Hugging Face models
os.environ['HF_HOME'] = 'D:/huggingface_cache'

# Check if a GPU is available and set the device
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cpu":
    print("Warning: Running on CPU. This will be very slow.")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")

image_path = input("Enter Image Path: ")
raw_image = Image.open(image_path)

# conditional image captioning
# text = "a photography of"
# inputs = processor(raw_image, text, return_tensors="pt").to(device)

inputs = processor(raw_image, return_tensors="pt").to(device)

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

