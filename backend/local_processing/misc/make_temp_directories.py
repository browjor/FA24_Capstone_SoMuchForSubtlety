import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.create_db import OfficialCameraList
load_dotenv()
base_directory = os.getenv('TEMP_PIC_ROOT')

engine = create_engine(os.getenv('SQLite_DB_LOC'))
Session = sessionmaker(bind=engine)
session = Session()

all_cameras=session.query(OfficialCameraList).all()

for camera in all_cameras:
    subdirectory_path = base_directory + '\\' + str(camera[0])
    os.makedirs(subdirectory_path)

session.commit()
session.close()