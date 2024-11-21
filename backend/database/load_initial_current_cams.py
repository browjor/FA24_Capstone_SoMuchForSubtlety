from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import current_timestamp
import os, time
from dotenv import load_dotenv
from create_db import OfficialCameraList, CurrentCamera
from datetime import datetime

load_dotenv()

engine = create_engine(os.getenv('SQLite_DB_LOC'))
Session = sessionmaker(bind=engine)
session = Session()

all_cameras=session.query(OfficialCameraList).all()
temp_storage_paths = os.getenv('TEMP_PIC_ROOT')

for camera in all_cameras:
    current_camera = CurrentCamera(
        camera_id=camera.id,
        cam_status=camera.status,
        snapshot=camera.snapshot,
        latitude=camera.latitude,
        longitude=camera.longitude,
        last_update=datetime.now(),
        temp_storage_path=(temp_storage_paths+"\\"+str(camera.id)),
        conditions="Sunny"
    )
    session.add(current_camera)
    time.sleep(1)

session.commit()

all_cameras = session.query(CurrentCamera).all()
for camera in all_cameras:
    print(camera.camera_id, camera.last_update, camera.temp_storage_path)
session.close()



