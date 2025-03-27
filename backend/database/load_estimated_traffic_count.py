from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, time
from create_db import CurrentCamera, TrafficCount
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('SQLite_DB_LOC'))
Session = sessionmaker(bind=engine)
session = Session()

all_cameras = session.query(CurrentCamera).all()

for camera in all_cameras:
    if (camera.snapshot is None) or (camera.cam_status == "Offline"):
        continue
    else:
        current_timestamp = datetime.now()
        traffic_count = TrafficCount(
            cam_id=camera.camera_id,
            traffic_count = 10,
            traffic_time = current_timestamp,
            max_traffic_count= 10,
            max_traffic_time= current_timestamp
        )
        session.add(traffic_count)

session.commit()
session.close()
