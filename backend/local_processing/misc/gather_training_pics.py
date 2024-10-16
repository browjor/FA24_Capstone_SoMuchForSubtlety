import time
import urllib.request
from camera_list import *
from urllib.error import ContentTooShortError, HTTPError
from time import localtime
from dotenv import load_dotenv
import os
load_dotenv()
for i in range(2):
    for camera in CameraList:
        try:
            if camera[2] is None:
                time.sleep(15)
                continue
            else:
                urllib.request.urlretrieve(camera[2],
                                           os.getenv("TRAINING_PICS_LOC")
                                            + str(camera[0]) + "_" + camera[4] + "_" + str(localtime().tm_hour) + str(localtime().tm_min) + ".png")
        except ContentTooShortError as e:
            print(e,"Error")
            time.sleep(15)
            continue
        except HTTPError as e:
            print(e,"Error")
            time.sleep(15)
            continue

        time.sleep(15)
    time.sleep(10)
