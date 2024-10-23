from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, time
from create_db import CurrentCamera, TrafficCount
from datetime import datetime

engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')
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
        time.sleep(2)

session.commit()
session.close()