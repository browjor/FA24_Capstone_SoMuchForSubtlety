from sqlalchemy import create_engine, Column, Integer, Double, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
# Define the engine and Base

load_dotenv()
engine = create_engine = create_engine(os.getenv('SQLite_DB_LOC'))
Base = declarative_base()

# Define tables
class CurrentCamera(Base):
    __tablename__ = 'current_camera'
    
    camera_id = Column(Integer, primary_key=True)
    cam_status = Column(String, nullable=False)
    snapshot = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    last_update = Column(DateTime, nullable=False)
    temp_storage_path = Column(String, nullable=False)
    conditions = Column(Integer, nullable=False)
    zone = Column(Integer, nullable=False)

class OfficialCameraList(Base):
    __tablename__ = 'official_camera_list'
    
    oid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(Integer, nullable=False)
    county = Column(String, nullable=False)
    highway = Column(String, nullable=True)
    milemarker = Column(Double, nullable=True)
    description = Column(String, nullable=False)
    direction = Column(String, nullable=True)
    snapshot = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    updateTS = Column(Integer, nullable=False)
    

class TrafficCount(Base):
    __tablename__ = 'traffic_count'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cam_id = Column(Integer, nullable=False)
    traffic_count = Column(Integer, nullable=False)
    traffic_time = Column(DateTime, nullable=False)
    max_traffic_count = Column(Integer, nullable=False)
    max_traffic_time = Column(DateTime, nullable=False)

# Create the tables
Base.metadata.create_all(engine)
