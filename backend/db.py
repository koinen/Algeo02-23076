import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with the loaded URL
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,  # Test connection before using
)
# check if the connection is successful
# try:
#     engine.connect()
#     print("Database connected successfully")
# except Exception as e:
#     print(f"Database connection failed: {str(e)}")

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern way to create a base class
class Base(DeclarativeBase):
    pass