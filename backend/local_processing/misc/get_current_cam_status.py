from backend.local_processing.auxiliary.aux_program import *

#get cam info from server
load_dotenv()
request_string = os.getenv("MAP_SERVER_REQUEST")
json = send_web_request(request_string)
off_cam_data = json['features']
if off_cam_data is HTTPError or off_cam_data is int:
    print("Error")
else:
    features = json['features']
    for feature in features:
        print(feature['attributes'])