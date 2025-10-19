import os
from Pipe1 import run_full_video_pipeline
target_folder="video_processing/Video"

def store_django_video(uploaded_file):
    """
    Saves a Django UploadedFile object to a specified folder.

    :param uploaded_file: The file object from request.FILES['my_file'].
    :param target_folder: The path to the folder where it should be stored.
    """
    
    # 1. Create the target folder if it doesn't already exist
    try:
        os.makedirs(target_folder, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {target_folder}: {e}")
        return None  # Return None to indicate failure

    # 2. Get the original filename from the uploaded file object
    video_filename = uploaded_file.name
    
    # 3. Create the full destination path
    destination_path = os.path.join(target_folder, video_filename)

    # 4. Write the file to the destination
    # We open the destination file in write-binary ('wb+') mode
    try:
        with open(destination_path, 'wb+') as destination:
            # uploaded_file.chunks() handles large files efficiently
            # without loading the whole thing into memory at once.
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        print(f"Successfully saved video to: {destination_path}")
        return destination_path  # Return the new path on success
        
    except Exception as e:
        print(f"Error saving file: {e}")
        return None  # Return None to indicate failure
    return video_filename
    
def initialise(uploaded_file):
    filename = store_django_video(uploaded_file)
    run_full_video_pipeline(filename)