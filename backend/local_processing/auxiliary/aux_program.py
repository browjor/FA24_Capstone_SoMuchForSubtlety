import requests
from dotenv import load_dotenv
import os
from requests import HTTPError
from backend.database.create_db import OfficialCameraList

load_dotenv()
request_string = os.getenv("MAP_SERVER_REQUEST")

#returns json from map server, an HTTP error status code, or an HTTP error
def get_off_cam_info(request_str):
    try:
        response = requests.get(request_str)
        if response.status_code == 200:
            json_format = response.json()
            return json_format
        else:
            return response.status_code

    except HTTPError as e:
        print("Error in fetching request: "+str(e))
        return e

#look for offline cameras in json response, look for offline cameras in database
def prepare_changes_in_cam_info(data):

    #get offline list from data
    offline_list = []
    features = data.get('features', [])
    for feature in features:
        if feature[0]['attributes']['status'] == 'Offline':
            offline_list.append([feature[0]['attributes']['id'],
                                 feature[0]['attributes']['oid'],
                                 feature[0]['attributes']['status']])

    #get records from official_camera_list_table as object and compare
    #if offline or online in BOTH do nothing
    #if offline in response and online in database, change database to reflect
    #if online in response and offline in database, change database to reflect






