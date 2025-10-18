import json
from sentence_transformers import SentenceTransformer

# --- 1. Load the Embedding Model ---
# (Using a standard, available model)
def load_embedder():
    try:
        print("Loading embedding model...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        embedding_model = None
    return embedding_model

# --- 2. Serialization Function (UPDATED) ---

def serialize_scene_to_text(scene_data: dict) -> str:
    """
    Serializes the structured scene data into a single string 
    using your specified format.
    """
    
    # Get all the data fields
    prev_desc = scene_data.get("previous_description")
    start_time = scene_data.get("start_time", 0.0)
    end_time = scene_data.get("end_time", 0.0)
    summary = scene_data.get("scene_summary", "")
    transcript = scene_data.get("transcript", "")
    
    # Handle the case for the first scene (no previous description)
    if prev_desc is None:
        context = "This is the first scene."
    else:
        context = f"Previously: {prev_desc}"

    # Your exact f-string format:
    serialized_text = (
        f"{context} "
        f"In this scene from {start_time}s to {end_time}s, {summary} "
        f"The dialogue includes: \"{transcript}\""
    )
    
    return serialized_text.strip()

# --- 3. Embedding Function (Unchanged) ---

def get_embedding(text: str,embedding_model):
    """
    Converts a single string of text into a numerical embedding.
    """
    if embedding_model is None:
        print("Embedding model is not loaded. Cannot generate embedding.")
        return None
        
    embedding = embedding_model.encode(text)
    return embedding


def generate_embedding_from_file(embedding_model,json_file_path: str):
    """
    Loads a scene JSON file, serializes it, and returns its embedding.

    :param json_file_path: The file path to a JSON file (e.g., "summary_data.json").
    :return: A numerical embedding (NumPy array) or None on failure.
    """
    print(f"\nProcessing file: {json_file_path}")
    
    # 1. Read the JSON file
    try:
        with open(json_file_path, 'r') as f:
            scene_data = json.load(f)
    except FileNotFoundError:
        print(f"  [Error] File not found: {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"  [Error] File is not valid JSON: {json_file_path}")
        return None
    except Exception as e:
        print(f"  [Error] Could not read file: {e}")
        return None
        
    # 2. Serialize the data to text
    serialized_text = serialize_scene_to_text(scene_data)
    print(f"  Serialized text: \"{serialized_text}...\"") # Print snippet
    
    # 3. Generate and return the embedding
    embedding_vector = get_embedding(serialized_text,embedding_model)
    
    if embedding_vector is not None:
        print(f"  Embedding generated (Dimensions: {embedding_vector.shape})")
        
    return embedding_vector

