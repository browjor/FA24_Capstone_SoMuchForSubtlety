import time
from backend.database.create_db import CurrentCamera, TrafficCount
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
import urllib.request
from urllib.error import ContentTooShortError, HTTPError
from datetime import datetime
engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')

def wait_until_time_is_up(start_time):
    end_time = time.time() - start_time
    while end_time <= 9:
        time.sleep(1)
        end_time = time.time() - start_time
    return


while True:
    start_time = time.time()
    Session = sessionmaker(bind=engine)
    session = Session()
    oldest_camera = session.query(CurrentCamera).order_by(asc(CurrentCamera.last_update)).first()

    #if camera doesn't have a link (which is possible), mark as updated in db and continue (we haven't requested image yet)
    if oldest_camera.snapshot is None:
        oldest_camera.last_update = datetime.now()
        session.commit()
        session.close()
        continue

    #this request replaces the old picture in the temp_storage_path
    try:
        urllib.request.urlretrieve(oldest_camera.snapshot, oldest_camera.temp_storage_path)

    except ContentTooShortError as e:
        print(e, "Error")
        #logic for handling ContentTooShortError which happens randomly
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

    #placeholder for results
    model_results = 5

    #if results are higher than the historical max, make the current result the historical max
    historical = session.query(TrafficCount).order_by(asc(TrafficCount.traffic_time)).first()

    if historical.max_traffic_count<model_results:
        current_traffic_count = TrafficCount(
            cam_id=
        )



    #upon successful loop, close the db session and wait until time is up
    session.close()
    wait_until_time_is_up(start_time)

