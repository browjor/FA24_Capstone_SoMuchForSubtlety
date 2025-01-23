from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from backend.database.create_db import CurrentCamera
import geopy.distance
from sqlalchemy import update

load_dotenv()

zones = [
    (1,38.27,-85.81), #top left
    (2,38.26, -85.73), #top 2nd from left
    (3,38.28, -85.64), #top 3rd from left
    (4,38.29, -85.52), #top 4th from left (farthest right)
    (5,38.19, -85.83), #middle left
    (6,38.20, -85.71), #middle 2nd from left
    (7,38.22, -85.58), #slight above middle 3rd from left
    (8,38.12, -85.78), #bottom leftmost
    (9,38.12, -85.64), #bottom 2nd from left
    (10,38.19, -85.51) #middle far right
]

engine = create_engine(os.getenv('SQLite_DB_LOC'))
Session = sessionmaker(bind=engine)
session = Session()

all_cameras = session.query(CurrentCamera).all()

zone_3_tuple_list = []

for camera in all_cameras:
    zone_3_tuple_list.append((camera.camera_id,camera.latitude,camera.longitude))

cam_zone_list = []
try:
    for cam in zone_3_tuple_list:
        cam_zone_options = [cam[0]]
        for zone in zones:
            zone_lat = zone[1]
            zone_lng = zone[2]
            zone_coords = (zone_lat, zone_lng)
            cam_lat = cam[1]
            cam_lng = cam[2]
            cam_coords = (cam_lat, cam_lng)
            distance = geopy.distance.distance(cam_coords,zone_coords).km
            cam_zone_options.append((zone[0], distance))
        cam_zone_list.append(cam_zone_options)
except Exception as e:
    session.commit()
    session.close()

for camera in all_cameras:
    for cam in cam_zone_list:
        if camera.camera_id == cam[0]:
            cam_id = cam.remove(cam[0])
            min_zone = 9999
            min_dis = 99999.0
            for zone in cam:
                if zone[1] < min_dis:
                    min_zone = zone[0]
                    min_dis = zone[1]
            camera.zone = min_zone
            break

session.commit()
session.close()

