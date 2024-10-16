from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import current_timestamp

from create_db import OfficialCameraList, CurrentCamera
import time

engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
session = Session()

all_cameras=session.query(OfficialCameraList).all()

current_timestamp()

for camera in all_cameras:
    current_camera = CurrentCamera(
        camera_id=camera.id,
        cam_status=camera.status,
        snapshot=camera.snapshot,
        latitude=camera.latitude,
        longitude=camera.longitude,
        last_update=

    )



session.commit()
session.close()