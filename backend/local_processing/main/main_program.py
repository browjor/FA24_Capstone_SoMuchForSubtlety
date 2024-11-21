import time
from backend.database.create_db import CurrentCamera, TrafficCount
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
import urllib.request
from urllib.error import ContentTooShortError, HTTPError
from datetime import datetime
from backend.local_processing.models.YOLOv8 import process_image,extract_data
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('SQLite_DB_LOC'))
def wait_until_time_is_up(start_time):
    end_time = time.time() - start_time
    while end_time <= 10:
        time.sleep(1)
        end_time = time.time() - start_time
    return


#for demo purposes
i = 0

while True and i<309:
    #start timer
    start_time = time.time()

    #starting and closing session each loop to ensure SQL writes are finished each loop
    Session = sessionmaker(bind=engine)
    session = Session()

    #getting the last updated camera
    oldest_camera = session.query(CurrentCamera).order_by(asc(CurrentCamera.last_update)).first()

    #if camera doesn't have a link (which is possible), mark as updated in db and continue (we haven't requested image yet)
    if oldest_camera.snapshot is None:
        oldest_camera.last_update = datetime.now()
        session.commit()
        session.close()
        continue

    #this request replaces the old picture in the temp_storage_path
    try:
        urllib.request.urlretrieve(oldest_camera.snapshot, oldest_camera.temp_storage_path+'\\current.png')

    # logic for handling ContentTooShortError which happens randomly
    except ContentTooShortError as e:
        print(e, "Error")
        #making it updated so the loop won't come back to it
        oldest_camera.last_update = datetime.now()
        session.commit()
        session.close()
        wait_until_time_is_up(start_time)
        continue

    except HTTPError as e:
        print(e, "Error")
        #logic for handling HTTP error (which will probably happen repeatedly)
        oldest_camera.last_update = datetime.now()
        oldest_camera.cam_status = "Offline"
        session.commit()
        session.close()
        wait_until_time_is_up(start_time)
        continue

        #mark camera last_updated and wait until time is done

#   if oldest_camera.conditions == "Sunny":
#       logic for determining model based on conditions

    #apply model to image and get results
    #do any calculations required for model to get results
    data = process_image(oldest_camera.temp_storage_path+'\\current.png')
    model_results = extract_data(data)
    #get the last updated entry for camera from traffic_count table

    current_datetime = datetime.now()
    historical = session.query(TrafficCount).filter(TrafficCount.cam_id == oldest_camera.camera_id).order_by(asc(TrafficCount.traffic_time)).first()
    if historical is None:
        current_traffic_count = TrafficCount(
            cam_id=oldest_camera.camera_id,
            traffic_count=model_results,
            traffic_time=current_datetime,
            max_traffic_count=model_results,
            max_traffic_time=current_datetime
        )
        session.add(current_traffic_count)
        session.commit()
    #if the traffic is higher than the historical max, replace the historical max
    elif historical.max_traffic_count<model_results:
        current_traffic_count = TrafficCount(
            cam_id=oldest_camera.camera_id,
            traffic_count = model_results,
            traffic_time=current_datetime,
            max_traffic_count=model_results,
            max_traffic_time=current_datetime
        )
        session.add(current_traffic_count)
        session.commit()
    else:
        current_traffic_count = TrafficCount(
            cam_id=oldest_camera.camera_id,
            traffic_count=model_results,
            traffic_time=current_datetime,
            max_traffic_count=historical.max_traffic_count,
            max_traffic_time=historical.max_traffic_time
        )
        session.add(current_traffic_count)
        session.commit()

    #update the db with update time in current_cams
    oldest_camera.last_update = current_datetime
    session.commit()
    #upon successful loop, close the db session and wait until time is up
    session.close()
    wait_until_time_is_up(start_time)
    i+=1



