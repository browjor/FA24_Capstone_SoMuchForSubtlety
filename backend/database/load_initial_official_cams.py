from backend.local_processing.auxiliary.aux_program import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import OfficialCameraList

#get cam info from server
load_dotenv()
request_string = os.getenv("MAP_SERVER_REQUEST")
json = get_off_cam_info(request_string)
off_cam_data = json['features']
if off_cam_data is HTTPError or off_cam_data is int:
    print("Error")
else:
    #create connection to db
    engine = create_engine('sqlite:///my_database.db')
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




