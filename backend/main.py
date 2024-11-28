from fastapi import FastAPI
from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
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
        db.delete(test_record)
        db.commit()
        
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
    finally:
        db.close()

# Alternatively, if you want to create tables on startup
@app.on_event("startup")
def startup_event():
    # Create tables
    Base.metadata.create_all(bind=engine)