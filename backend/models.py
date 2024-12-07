from sqlalchemy import Column, Integer, String
from db import Base

class TestConnection(Base):
    __tablename__ = 'test_connection'
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=True)

class songRaw(Base):
    __tablename__ = 'songRaw'
    
    song_id = Column(Integer, primary_key=True, index=True)
    song_name = Column(String, nullable=False)
    song_album = Column(String, nullable=False)
    song_album_image = Column(String, nullable=False)


class songCalculated(Base):
    __tablename__ = 'songCalculated'
    
    song_id = Column(Integer, primary_key=True, index=True)
    song_name = Column(String, nullable=False)
    song_album = Column(String, nullable=False)
    song_album_image = Column(String, nullable=False)


    