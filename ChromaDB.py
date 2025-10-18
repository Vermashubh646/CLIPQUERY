import os
import glob
import sys
import json
import chromadb
import re

def populate_chroma_db(embedding, collection, SETS_BASE_FOLDER, VIDEO_FILENAME,CHROMA_COLLECTION_NAME,start_time,end_time,serialized_text,summary):
    """
    Finds all scene summaries, generates embeddings, and adds them to ChromaDB.
    """
    
    # Find all the 'summary_data.json' files
    json_files = sorted(glob.glob(os.path.join(SETS_BASE_FOLDER, "set_*/summary_data.json")))
    
    if not json_files:
        print(f"Error: No 'summary_data.json' files found in {SETS_BASE_FOLDER}")
        print("Please run Pipe1, Pipe2, and Pipe3 first.")
        return

    print(f"Found {len(json_files)} scenes to add to ChromaDB...")

    # We will collect everything in lists to add in one batch (much faster)
    all_embeddings = []
    all_metadatas = []
    all_documents = []
    all_ids = []
    
    # Regex to extract 'set_001' from the path
    set_name_regex = re.compile(r"(set_\d+)")

    for file_path in json_files:
        try:
            # Get a unique ID from the file path
            match = set_name_regex.search(file_path)
            if not match:
                print(f"  [Warning] Skipping file, could not get ID: {file_path}")
                continue
            scene_id = f"{VIDEO_FILENAME}_{match.group(1)}" # e.g., "Vid1.mp4_set_001"

            # Read the JSON file
            with open(file_path, 'r') as f:
                scene_data = json.load(f)

            
        

            # 3. Create Metadata (This is where you store timestamps!)
            metadata = {
                "start_time": start_time,
                "end_time": end_time,
                "summary": summary,
                "source_file": file_path
            }

            # Add all pieces to our lists
            all_embeddings.append(embedding.tolist()) # .tolist() to make it JSON-serializable
            all_metadatas.append(metadata)
            all_documents.append(serialized_text)
            all_ids.append(scene_id)
            
            print(f"  Prepared: {scene_id}")

        except Exception as e:
            print(f"  [Error] Failed to process file {file_path}: {e}")

    # 4. Add to ChromaDB
    # This adds everything in a single, efficient operation
    if all_ids:
        print(f"\nAdding {len(all_ids)} entries to ChromaDB collection '{CHROMA_COLLECTION_NAME}'...")
        collection.add(
            embeddings=all_embeddings,
            metadatas=all_metadatas,
            documents=all_documents,
            ids=all_ids
        )
        print("Successfully added entries to database.")
    else:
        print("No new entries to add.")

# --- 5. Function to Query DB ---
def query_video_for_timestamps(embedder, collection, query_text: str, n_results=1):
    """
    Takes a text query, finds the most similar scene, and returns its timestamps.
    """
    print(f"\n--- Querying for: '{query_text}' ---")
    
    # 1. Generate an embedding for the query text
    query_embedding = embedder.get_embedding(query_text)
    
    if query_embedding is None:
        print("Error: Could not generate embedding for query.")
        return
        
    # 2. Query the collection
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    
    # 3. Process and print the results
    if not results.get('ids') or not results['ids'][0]:
        print("No matching results found.")
        return

    print("Found matching scene(s):")
    
    for i in range(len(results['ids'][0])):
        scene_id = results['ids'][0][i]
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        
        print(f"  Result {i+1}:")
        print(f"    Scene ID: {scene_id}")
        print(f"    Similarity: {1 - distance:.2f} (lower distance is better)")
        print(f"    Start Time: {metadata.get('start_time')}s")
        print(f"    End Time: {metadata.get('end_time')}s")
        print(f"    Summary: \"{metadata.get('summary')}\"")


