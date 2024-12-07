from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image
import io
from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
import zipfile
import os
import shutil
from modules.image_processing import *
from modules.audio_processing import *
from models import TestConnection  # Assuming you have this model
from typing import Optional

app = FastAPI()

@app.get("/")
async def root():
    # Create a session
    db = SessionLocal()
    try:
        # Simple database connectivity test
        test_record = TestConnection(message="Database connection successful!")
        db.add(test_record)
        db.commit()
        
        # Optional: remove the test record
        db.delete(test_record)
        db.commit()
        
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
    finally:
        db.close()

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

@app.post("/upload_dataset")
async def upload_dataset(path: str):
    try:
        # Ensure the path exists
        if not os.path.exists(path):
            raise HTTPException(status_code=400, detail="Path does not exist")

        # Open the zip file for extraction
        with zipfile.ZipFile(path, 'r') as zip_ref:
            # Extract all the contents into a directory
            extract_path = os.path.splitext(path)[0]  # Extract the contents of the zip file to a directory named after the zip file (without the .zip extension)
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
                audio_vector = MidiProcessing.processMidi(entry.path)
                audio_data_center.append(audio_vector)
                audio_file_names.append(entry.name)
                print(f"Processed audio {entry.name}")
            # try:
            #     shutil.copy(entry.path, os.path.join(save_path, entry.name))
            # except Exception as e:
            #     raise HTTPException(status_code=500, detail=f"Error copying file {entry.name}: {str(e)}")
            # shutil.copy(entry.path, os.path.join(save_path, entry.name))
        
        # save the image data to the save path
        np.save(os.path.join(save_path, "image_data.npy"), np.array(image_data_center))
        np.save(os.path.join(save_path, "audio_data.npy"), np.array(audio_data_center))
        with open(os.path.join(save_path, "image_file_names.txt"), "w") as f:
            f.write("\n".join(image_file_names))
        with open(os.path.join(save_path, "audio_file_names.txt"), "w") as f:
            f.write("\n".join(audio_file_names))
        return {"message": f"Dataset successfully extracted to {save_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# @app.post("upload_song")

# Alternatively, if you want to create tables on startup
@app.on_event("startup")
def startup_event():
    # Create tables
    Base.metadata.create_all(bind=engine)