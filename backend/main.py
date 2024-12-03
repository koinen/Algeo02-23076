from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image
import io
from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
import zipfile
import os
from models import TestConnection  # Assuming you have this model

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
        # db.delete(test_record)
        # db.commit()
        
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
    finally:
        db.close()

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        # queryResult = imageQuery(image)
        return Response(
            content=contents,
            media_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
        file_contents = []
        for entry in os.scandir(extract_path):
            if entry.is_file():
                with open(entry.path, 'rb') as f:
                    file_contents.append(f.read())
        return {"message": f"Dataset successfully extracted to {extract_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# @app.post("upload_song")

# Alternatively, if you want to create tables on startup
@app.on_event("startup")
def startup_event():
    # Create tables
    Base.metadata.create_all(bind=engine)