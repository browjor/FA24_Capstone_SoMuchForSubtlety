from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import current_timestamp
import os, time

from create_db import OfficialCameraList, CurrentCamera
from datetime import datetime

engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')
Session = sessionmaker(bind=engine)
session = Session()

all_cameras=session.query(OfficialCameraList).all()
temp_storage_paths = 'C:\\Users\\johnb\\PycharmProjects\\FA24_Capstone_SoMuchForSubtlety\\backend\\local_processing\\temp_storage\\'

for camera in all_cameras:
    current_camera = CurrentCamera(
        camera_id=camera.id,
        cam_status=camera.status,
        snapshot=camera.snapshot,
        latitude=camera.latitude,
        longitude=camera.longitude,
        last_update=datetime.now(),
        temp_storage_path=(temp_storage_paths+str(camera.id)),
        conditions="Sunny"
    )
    session.add(current_camera)
    time.sleep(1)

session.commit()

all_cameras = session.query(CurrentCamera).all()
for camera in all_cameras:
    print(camera.camera_id, camera.last_update, camera.temp_storage_path)
session.close()



