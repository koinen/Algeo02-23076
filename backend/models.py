from sqlalchemy import Column, Integer, String
from db import Base

class TestConnection(Base):
    __tablename__ = 'test_connection'
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=True)