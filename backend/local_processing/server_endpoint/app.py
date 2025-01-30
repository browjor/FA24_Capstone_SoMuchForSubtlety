from flask import Flask, request, abort
from flask_restful import Resource, Api, marshal_with, fields
from backend.database.create_db import TrafficCount, OfficialCameraList  # Import models only
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, json, time, hmac, hashlib

load_dotenv()
engine = create_engine(os.getenv('SQLite_DB_LOC'))
SHARED_SECRET = os.getenv('SHARED_SECRET')
server_ipv4 = os.getenv('SERVER_IPV4')
server_port = int(os.getenv('SERVER_PORT'))
app = Flask(__name__)
api = Api(app)

dataFields = {
    'id': fields.Integer,
    'density': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float
}

def verify_request_signature(headers):
    signature = headers.get("X-Signature")
    print(signature)
    message = headers.get("X-Message")
    print(message)

    #if malformed
    if not signature or not message:
        print("No signature or no message")
        abort(403)

    #create server version
    expected_signature = hmac.new(
        SHARED_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    print(expected_signature)

    # get time value, see if it matches, prevent replay attacks
    try:
        method, timestamp = message.split(" ")
        timestamp = int(timestamp)  # Convert timestamp to integer
        current_time = int(time.time())
        if -15 < abs(current_time - timestamp) < 15:
            print(str(abs(current_time - timestamp)))
    except (ValueError, AttributeError):
        print("Value Error or Attribute Error")
        abort(403)

    #bad entry
    if not hmac.compare_digest(signature, expected_signature):
        print("Signature Did Not Match")
        abort(403)



class LatestTrafficData(Resource):
    @marshal_with(dataFields)
    def get(self):
        with app.app_context():

            verify_request_signature(request.headers)

            Session = sessionmaker(bind=engine)
            session = Session()

            # getting the last updated camera
            recent_traffic = session.query(TrafficCount).order_by(desc(TrafficCount.traffic_time)).first()

            if not recent_traffic:
                abort(404, message="No traffic data found.")

            camera_info = session.query(OfficialCameraList).filter_by(id=recent_traffic.cam_id).first()

            if not camera_info:
                abort(404, message="Camera information not found for the given cam_id.")

            density = recent_traffic.traffic_count / recent_traffic.max_traffic_count if recent_traffic.max_traffic_count else 0

            result = {
                'id': recent_traffic.cam_id,
                'density': density,
                'latitude': camera_info.latitude,
                'longitude': camera_info.longitude
            }
            session.commit()
            session.close()
            return result


api.add_resource(LatestTrafficData, '/latest-traffic')


@app.route('/')
def home():
    return 'Hello, Flask!'


if __name__ == '__main__':
    app.run(debug=True, host= server_ipv4, port=server_port)