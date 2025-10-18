import os
import json
import chromadb
import glob
from JSON_embed.JSON_Embed import load_embedder,generate_embedding_from_file,serialize_scene_to_text
from ChromaDB import populate_chroma_db

SETS_BASE_FOLDER = "video_processing/Sets/"
CHROMA_DB_PATH = 'chroma_db'
CHROMA_COLLECTION_NAME = 'video_scenes'
filename = "Breaking Bad - _I am the Danger_ Scene S4 E6 1080p.mp4"

#Serealize and Embed
embedding_model = load_embedder()


client = chromadb.PersistentClient(path=CHROMA_DB_PATH) 
collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

files_path = os.path.join(SETS_BASE_FOLDER,filename)
set_folders = sorted(glob.glob(os.path.join(files_path, "set_*")))

print(f"Found {len(set_folders)} sets to process.")

for set_folder in set_folders:

            data_json_path = os.path.join(set_folder, "summary.json")
            curr_embedding = generate_embedding_from_file(embedding_model,data_json_path)
            
            with open(data_json_path, 'r') as f:
                scene_data = json.load(f)
            
            serialized_text = serialize_scene_to_text(scene_data)
                
            prev_desc = scene_data.get("previous_description")
            start_time = scene_data.get("start_time", 0.0)
            end_time = scene_data.get("end_time", 0.0)
            summary = scene_data.get("scene_summary", "")
            transcript = scene_data.get("transcript", "")
            
            populate_chroma_db(curr_embedding, collection, SETS_BASE_FOLDER, filename,CHROMA_COLLECTION_NAME,start_time,end_time,serialized_text,summary)
            