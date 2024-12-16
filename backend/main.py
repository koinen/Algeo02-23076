from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import zipfile
import os
import shutil
import json
from modules.image_processing import *
from modules.audio_processing import *
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with a list of allowed origins if necessary.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    pass

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    
    # Validate file type (optional)
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Create directory if it doesn't exist
    os.makedirs("uploads/image", exist_ok=True)
    
    # Generate a unique filename
    file_path = os.path.join("uploads/image", "uploaded_image.jpg")
    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return {"filename": file.filename, "path": file_path}

@app.post("/upload_song")
async def upload_song(file: UploadFile = File(...)):
    # Validate file type (optional)
    allowed_types = ['audio/mid']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    print(file.content_type)
    # Create directory if it doesn't exist
    os.makedirs("uploads/audio", exist_ok=True)
    
    # Generate a unique filename
    file_path = os.path.join("uploads/audio", "uploaded_song.mid")
    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return {"filename": file.filename, "path": file_path}

@app.post("/upload_dataset")
async def upload_dataset(path: str):
    try:
        # Ensure the path exists
        if not os.path.exists(path):
            raise HTTPException(status_code=400, detail="Path does not exist")

        # Ensure the path is a zip file
        if not path.lower().endswith('.zip'):
            raise HTTPException(status_code=400, detail="Path is not a zip file")

        # clean the extracted directory
        shutil.rmtree("uploads/dataset/extracted", ignore_errors=True)
        os.makedirs("uploads/dataset/extracted", exist_ok=True)

        # Open the zip file for extraction
        with zipfile.ZipFile(path, 'r') as zip_ref:
            # Extract all the contents into a directory
            extract_path = "uploads/dataset/extracted"
            zip_ref.extractall(extract_path)
        
        save_path = "uploads/dataset"
        image_data_center = []
        audio_data_center = []
        image_file_names = []
        audio_file_names = []
        os.makedirs(save_path, exist_ok=True)
        for entry in os.scandir(extract_path):
            # check if the entry is an image
            if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(entry.path)
                # process the image to a vector
                image_vector = ImageProcessing.processImage(image)
                image_data_center.append(image_vector)
                image_file_names.append(entry.name)
                print(f"Processed image {entry.name}")
            # check if the entry is an audio file
            elif entry.is_file() and entry.name.lower().endswith(('.mid')):
                # process the audio file to a vector
                audio_matrix = MidiProcessing.processMidi(entry.path)
                audio_data_center.append(audio_matrix)
                audio_file_names.append(entry.name)
                print(f"Processed audio {entry.name}")
        
        # save the image data to the save path
        print("succeeded")
        np.save(os.path.join(save_path, "image_data.npy"), np.array(image_data_center))
        print("succeeded")
        np.save(os.path.join(save_path, "audio_data.npy"), np.array(audio_data_center, dtype=object))
        print("succeeded")
        with open(os.path.join(save_path, "image_file_names.txt"), "w") as f:
            f.write("\n".join(image_file_names))
        with open(os.path.join(save_path, "audio_file_names.txt"), "w") as f:
            f.write("\n".join(audio_file_names))
        
        return {"message": f"Dataset successfully extracted to {save_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/upload_mapping')
async def upload_mapping(file: UploadFile = File(...)):
    # Validate file type (optional)
    # json file
    allowed_types = ['application/json']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Create directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    file_path = "uploads/mapping.json"
    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return {"filename": file.filename, "path": file_path}


@app.get('/dataset')
async def get_dataset(page: Optional[int] = 1):
    try:
        LIMIT = 12
        dataset_path = "uploads/dataset/extracted/"
        not_found = False
        start_idx = (page-1)*LIMIT
        count = min(start_idx + LIMIT, len(os.listdir(dataset_path))) - start_idx + 1

        idx = 1
        song_data = []
        with open("uploads/dataset/audio_file_names.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if idx >= start_idx:
                    song_path = os.path.join(dataset_path, line.strip())
                    song_data.append(song_path)
                idx += 1
                if idx >= start_idx + count:
                    break
        """
        Example mapper file:
        {
            "song_file_name": {
                "title": "song_title",
                "artist": "song_artist",
                "image_path": "image_path",
            }
        }
        """
        print(song_data)
        # if mapper file does not exist, return the song data as is
        if not os.path.exists("uploads/mapping.json"):
            for idx, song in enumerate(song_data):
                print(idx)
                song_data[idx] = {
                    "fileName": os.path.basename(song),
                    "mapping": {
                        "artist": None,
                        "title": None,
                        "image": None
                    }
                }
            
        else:
            # Load the mapping file
            mapper = json.load(open("uploads/mapping.json", "r"))

            # Example usage of mapper
            for idx, song in enumerate(song_data):
                # Extract the base name of the song file
                song_name = os.path.basename(song)  # Assuming each song in song_data is a dictionary with a "song" key
                
                if song_name in mapper:
                    # Map the fields using the mapper
                    song_data[idx] = {
                        "fileName": song_name,
                        "mapping": {
                            "artist": mapper[song_name].get("artist"),
                            "title": mapper[song_name].get("title"),
                            "image": mapper[song_name].get("image")
                        }
                    }
                else:
                    print(f"Song not found in mapper: {song_name}")
            
        return song_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))