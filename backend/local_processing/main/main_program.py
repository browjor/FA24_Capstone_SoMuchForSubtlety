import time
from backend.database.create_db import CurrentCamera, TrafficCount
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
import urllib.request
from urllib.error import ContentTooShortError, HTTPError

engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')

while True:
    start_time = time.time()
    Session = sessionmaker(bind=engine)
    session = Session()
    oldest_camera = session.query(CurrentCamera).order_by(asc(CurrentCamera.last_update)).first()
#   if oldest_camera.snapshot is None:
#      do nothing and wait until time is done

    try:
        urllib.request.urlretrieve(oldest_camera.snapshot, oldest_camera.temp_storage_path)
    except ContentTooShortError as e:
        print(e, "Error")
        #this is a pretty basic exception, maybe retry
    except HTTPError as e:
        print(e, "Error")
        #logic for handling HTTP error


#   if oldest_camera.conditions == "Sunny":
#       logic for determining model based on conditions
