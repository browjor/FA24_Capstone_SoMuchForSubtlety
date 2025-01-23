from backend.database.create_db import OfficialCameraList
from dotenv import load_dotenv
import os,requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def send_web_request(request_str):
    try:
        response = requests.get(request_str, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request to {request_str} returned status code {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"Request to {request_str} timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred for {request_str}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request to {request_str}: {e}")
        return None


#get cam info from server
load_dotenv()
request_string = os.getenv("MAP_SERVER_REQUEST")
json = send_web_request(request_string)
off_cam_data = json['features']
try:
    #create connection to db
    engine = create_engine(os.getenv('SQLite_DB_LOC'))
    Session = sessionmaker(bind=engine)
    session = Session()

    #deletes rows in table to replace them
    #only applicable for initialization of table from SCRATCH
    session.query(OfficialCameraList).delete()
    session.commit()


    try:
        for feature in off_cam_data:
            attribute_dict = feature['attributes']
            camera = OfficialCameraList(
                oid=attribute_dict['oid'],
                id=attribute_dict['id'],
                name=attribute_dict['name'],
                status=attribute_dict['status'],
                state=attribute_dict['state'],
                district=attribute_dict['district'],
                county=attribute_dict['county'],
                highway=attribute_dict['highway'],
                milemarker=attribute_dict['milemarker'],
                description=attribute_dict['description'],
                direction=attribute_dict['direction'],
                snapshot=attribute_dict['snapshot'],
                latitude=attribute_dict['latitude'],
                longitude=attribute_dict['longitude'],
                updateTS=attribute_dict['updateTS']
            )
            session.add(camera)
            session.commit()


        all_cameras=session.query(OfficialCameraList).all()

        session.close()

        for camera in all_cameras:
            print(camera.id, camera.status, camera.snapshot)
    except Exception as e:
        print(str(e) + "\n")
    finally:
        session.close()
        print("Session closed")
except Exception as e:
    print(str(e) + "\n")




