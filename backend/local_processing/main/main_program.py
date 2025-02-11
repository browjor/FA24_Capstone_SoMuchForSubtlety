import time, logging, os, urllib.request
from backend.database.create_db import CurrentCamera, TrafficCount
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc
import sqlalchemy.exc
from urllib.error import ContentTooShortError, HTTPError, URLError
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
    if camera is not None:
        camera.last_update = datetime.now()
        if not full_pass:
            camera.cam_status = "Offline"
        if error is None and full_pass:
            logging.info(f"Main Loop entering wait for camera: {camera.camera_id}")
        elif error is not None:
            logging.info(f"Main Loop entering wait for camera: {camera.camera_id} with error: {error}")
        else:
            logging.info(f"Main Loop skipping wait for Offline camera: {camera.camera_id}")
    else:
        logging.info("Main Loop Error in Querying Database")
    session.commit()
    session.close()
    if wait_on_time:
        wait_until_time_is_up(start_time)

def request_latest_cam_from_db(db_session):
    bool_continue = False
    try:
        oldest_camera = db_session.query(CurrentCamera).order_by(asc(CurrentCamera.last_update)).first()
        if oldest_camera.snapshot is None:
            bool_continue = True
            return bool_continue,db_session,oldest_camera
    except Exception as e:
        logging.info(f"MainLoop - InitialDBRequest: {e}")
        bool_continue = True
        return bool_continue,db_session,None
    return bool_continue,db_session,oldest_camera

def retrieve_image_from_url_into_storage(snapshot, storage_path):
    bool_continue = False
    try:
        urllib.request.urlretrieve(snapshot, storage_path + '\\current.png')
    except URLError as e:
        bool_continue = True
        return bool_continue,e
    except Exception as e:
        bool_continue = True
        return bool_continue,e
    return bool_continue, None

def perform_model_evaluation(camera_path, model_path, confidence, evaluation_mode, conditions, image_name):
    bool_continue = False
    if not retrieval_result[0] and os.path.exists(camera_path) and os.path.exists(model_path):
        try:
            model_path_name = os.path.basename(model_path).strip('.pt')
            count = process_image(camera_path, model_path, confidence, evaluation_mode, model_path_name, conditions, image_name)
            return bool_continue,None,count
        except Exception as e:
            bool_continue = True
            return bool_continue,e,None

def update_traffic_count(model_result, camera):
    bool_continue = False
    current_datetime = datetime.now()
    try:
        historical = session.query(TrafficCount).filter(TrafficCount.cam_id == camera.camera_id).order_by(
            asc(TrafficCount.traffic_time)).first()
        if historical is None:
            current_traffic_count = TrafficCount(
                cam_id=camera.camera_id,
                traffic_count=model_result,
                traffic_time=current_datetime,
                max_traffic_count=model_result,
                max_traffic_time=current_datetime
            )
            session.add(current_traffic_count)
            session.commit()
        # if the traffic is higher than the historical max, replace the historical max
        elif historical.max_traffic_count < model_result:
            current_traffic_count = TrafficCount(
                cam_id=camera.camera_id,
                traffic_count=model_result,
                traffic_time=current_datetime,
                max_traffic_count=model_result,
                max_traffic_time=current_datetime
            )
            session.add(current_traffic_count)
            session.commit()
        else:
            current_traffic_count = TrafficCount(
                cam_id=camera.camera_id,
                traffic_count=model_result,
                traffic_time=current_datetime,
                max_traffic_count=historical.max_traffic_count,
                max_traffic_time=historical.max_traffic_time
            )
            session.add(current_traffic_count)
            session.commit()

        return bool_continue, None

    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.info(f"General SQLAlchemy error: {e}")
        return True, e
    except Exception as e:
        logging.info(f"General SQLAlchemy ORM error: {e}")
        return True, e
if __name__ == "__main__":
    while True:
        #start timer
        start_time = time.time()
        #starting and closing session each loop to ensure SQL writes are finished each loop
        Session = sessionmaker(bind=engine)
        session = Session()


        #query database
        db_result = request_latest_cam_from_db(session)

        #handle errors for initial database query
        if db_result[0]:
            pass_to_next_loop(db_result[1], db_result[2], False, start_time, False, None)
            continue

        #ease of use label
        camera = db_result[2]

        #get image from url and store it to file
        retrieval_result = retrieve_image_from_url_into_storage(camera.snapshot, camera.temp_storage_path)

        #handle errors for url retrieval and storage
        if retrieval_result[0]:
            pass_to_next_loop(session, camera, True, start_time, False, retrieval_result[1])
            continue

        #getting name for when detections are saved
        image_name = f"{camera.camera_id}_{datetime.now().strftime('%d%m%y_%H%M%S')}"
        # apply model to image and get results
        model_results = perform_model_evaluation(camera.temp_storage_path+'\\current.png', os.getenv('MODEL_PATH_1'), 0.5, True, camera.conditions, image_name)

        #handle errors for model processing
        if model_results[0]:
            pass_to_next_loop(session, camera, True, start_time, False, model_results[1])
            continue

        update_result = update_traffic_count(model_results[2], camera)
        pass_to_next_loop(session, camera, True, start_time, not update_result[0], update_result[1])







