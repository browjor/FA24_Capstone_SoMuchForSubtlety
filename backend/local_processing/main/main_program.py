import time, logging, os, urllib.request
from backend.database.create_db import CurrentCamera, TrafficCount
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc
import sqlalchemy.exc
from urllib.error import ContentTooShortError, HTTPError
from datetime import datetime
from backend.local_processing.models.YOLOv8 import process_image
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Main_Loop.log"),
        logging.StreamHandler()
    ]
)

engine = create_engine(os.getenv('SQLite_DB_LOC'))
def wait_until_time_is_up(start_time):
    end_time = time.time() - start_time
    while end_time <= 10:
        time.sleep(1)
        end_time = time.time() - start_time
    logging.info(f"Main Loop Waiting Complete- Start:{start_time} - End:{end_time}")
    return


def pass_to_next_loop(session, camera, wait_on_time, start_time, full_pass, error):
    camera.last_update = datetime.now()
    if not full_pass:
        camera.cam_status = "Offline"
    if error is None and full_pass:
        logging.info(f"Main Loop entering wait for camera: {camera.camera_id}")
    elif error is not None:
        logging.info(f"Main Loop entering wait for camera: {camera.camera_id} with error: {error}")
    else:
        logging.info(f"Main Loop skipping wait for Offline camera: {camera.camera_id}")
    session.commit()
    session.close()
    if wait_on_time:
        wait_until_time_is_up(start_time)

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
        pass_to_next_loop(session,oldest_camera,False,start_time, False, None)
        continue

    #this request replaces the old picture in the temp_storage_path
    try:
        urllib.request.urlretrieve(oldest_camera.snapshot, oldest_camera.temp_storage_path+'\\current.png')

    # logic for handling ContentTooShortError which happens randomly
    except ContentTooShortError as e:
        #making it updated so the loop won't come back to it
        pass_to_next_loop(session,oldest_camera,True,start_time, False, e)
        continue

    except HTTPError as e:
        print(e, "Error")
        #logic for handling HTTP error (which will probably happen repeatedly)
        pass_to_next_loop(session,oldest_camera,True,start_time, False, e)
        continue


#   if oldest_camera.conditions == "Sunny":
#       logic for determining model based on conditions

    #apply model to image and get results
    #do any calculations required for model to get results
    model_results = process_image(oldest_camera.temp_storage_path+'\\current.png', (os.getenv('MODEL_PATH_1')), 0.5, False)
    #get the last updated entry for camera from traffic_count table

    current_datetime = datetime.now()

    try:
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

            # update the db with update time in current_cams
        oldest_camera.last_update = current_datetime
        pass_to_next_loop(session, oldest_camera, True, start_time, True, None)
        i += 1
        continue


    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.info(f"General SQLAlchemy error: {e}")
        wait_until_time_is_up(start_time)
        session.close()
        continue
    except Exception as e:
        logging.info(f"General SQLAlchemy ORM error: {e}")
        wait_until_time_is_up(start_time)
        session.close()
        continue




