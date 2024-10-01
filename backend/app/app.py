from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, marshal_with,fields, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


api=Api(app)
user_args = reqparse.RequestParser()
user_args.add_argument('cam_ID', required=True, type=int, help='Camera ID must not be blank')

#format of output JSON
dataFields = {
    'id': fields.Integer,
    'density': fields.Float,
    'lattitude': fields.Float,
    'longitude': fields.Float
}


#defines what happens when a GET request is received
class Camera(Resource):
    @marshal_with(dataFields)
    def get(self, cam_id):
        #logic for sending cam id to function that requests image

        #logic for sending image to yolov8

        #logic for putting results of yolov8 into database

        #logic for getting updated data on that camera
        data = CameraModel.query.filter_by(cam_id=cam_id).first()

        if not data:
            abort(404)
        return data

api.add_resource(Camera, '/<int:cam_id>')


#defines the database model for cameras
class CameraModel(db.Model):
    cam_ID = db.Column(db.Integer, primary_key=True)
    cam_descr = db.Column(db.String(300), unique=True, nullable=False)
    cam_url = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Camera ID = {self.cam_ID}"
@app.route('/')
def home():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
