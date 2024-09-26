import time
import urllib.request
from backend.camera_list import CameraList
from time import localtime
from dotenv import load_dotenv
import os
load_dotenv()
for i in range(10):
    for camera in CameraList:
        urllib.request.urlretrieve(camera[0],
                                   os.getenv("TRAINING_PICS_LOC")
                                    + str(camera[1]) + "_" + str(i) + "_" + str(localtime().tm_hour) + str(localtime().tm_min) + ".png")
        time.sleep(15)
    time.sleep(180)
