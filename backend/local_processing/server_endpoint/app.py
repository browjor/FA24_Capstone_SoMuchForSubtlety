from flask import Flask
from flask_restful import Resource, Api, marshal_with, fields, abort
from backend.database.create_db import TrafficCount, OfficialCameraList  # Import models only
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')
app = Flask(__name__)
api = Api(app)

dataFields = {
    'id': fields.Integer,
    'density': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float
}


class LatestTrafficData(Resource):
    @marshal_with(dataFields)
    def get(self):
        with app.app_context():
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
    app.run(debug=True, host='0.0.0.0', port=5000)