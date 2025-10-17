import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration, BitsAndBytesConfig
import time
import os

# Set the cache directory for Hugging Face models
os.environ['HF_HOME'] = 'D:/huggingface_cache'

# Check if a GPU is available and set the device
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cpu":
    print("Warning: Running on CPU. This will be very slow.")


quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)


model_id = "llava-hf/llava-1.5-7b-hf"


model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    dtype=torch.float16,
    low_cpu_mem_usage=True,
).to(device)

processor = AutoProcessor.from_pretrained(model_id)



image_path = input("Enter Image Path: ")
raw_image = Image.open(image_path)


prompt_text = "USER: <image>\nPlease describe this image in detail. Also Do make sure to cover any object any text or any living being shown, it must be in the description. ASSISTANT:"


start = time.time()


inputs = processor(text=prompt_text, images=raw_image, return_tensors='pt').to(device, torch.float16)
output = model.generate(
    **inputs,
    max_new_tokens=300,
    do_sample=True,
    temperature=0.6,
    top_p=0.9
)
response_text = processor.decode(output[0][2:], skip_special_tokens=True)


end = time.time()
print(f"Execution time: {end - start:.4f} seconds")
print("--- Model Description ---")
print(response_text)