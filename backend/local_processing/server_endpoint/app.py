from flask import Flask, jsonify, request
import hmac, hashlib, time, os, threading, json
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from backend.database.create_db import CurrentCamera, TrafficCount

load_dotenv()
SHARED_SECRET = os.getenv('SHARED_SECRET')
server_ipv4 = os.getenv('SERVER_IPV4')
server_port = int(os.getenv('SERVER_PORT'))

engine = create_engine(os.getenv('SQLite_DB_LOC'))
data_lock = threading.Lock()
traffic_data = []
app = Flask(__name__)

def fetch_traffic_data_from_db():
    new_traffic_data = []
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        latest_data = (
            session.query(
                CurrentCamera.camera_id,
                CurrentCamera.latitude,
                CurrentCamera.longitude,
                TrafficCount.traffic_count,
                TrafficCount.max_traffic_count
            )
            .join(TrafficCount, CurrentCamera.camera_id == TrafficCount.cam_id)
            .filter(CurrentCamera.cam_status == "Online")
            .order_by(CurrentCamera.last_update.desc(), TrafficCount.traffic_time.desc())
            .distinct(CurrentCamera.camera_id)  # Ensures distinct camera entries
            .all()
        )
    except Exception as e:
        print(e)
        session.rollback()
        session.close()
        return []
    for cam in latest_data:
        density = cam.traffic_count / cam.max_traffic_count if cam.max_traffic_count else '0.0'
        if density == 1.0:
            density = int(density)
        if density == 0:
            density = '0.0'
        new_traffic_data.append({'density': density, 'lat': cam.latitude, 'lon': cam.longitude})
        #print(f"Cam ID: {cam.camera_id}, Density: {density}, Latitude: {cam.latitude}, Longitude: {cam.longitude}")
    session.close()
    return new_traffic_data



#thread to update the list
def update_traffic_data():
    global traffic_data
    while True:
        new_data = fetch_traffic_data_from_db()

        if len(new_data) > 0:
            with data_lock:
                traffic_data.clear()
                traffic_data.extend(new_data)
                print("Traffic Data Updated")

        time.sleep(10)

def verify_hmac(request):
    received_hmac = request.headers.get("X-HMAC-Signature")
    timestamp = request.headers.get("X-Timestamp")
    
    if not received_hmac or not timestamp:
        return False

    print("Received Hmac: " + received_hmac)
    print("Received Timestamp: " + timestamp)
    try:
        timestamp = int(timestamp)
    except ValueError:
        return False

    if abs(time.time() - timestamp) > 300:
        print("Time stamp out of date")
        return False

    message = f"{timestamp}".encode()
    expected_hmac = hmac.new(SHARED_SECRET.encode(), message, hashlib.sha256).hexdigest()
    print("Expected Hmac: " +expected_hmac)
    return hmac.compare_digest(received_hmac, expected_hmac)

#matching json with , and : so it'll be received right on the frontend
def generate_response_hmac(response_json):
    # Ensure key ordering and compact JSON format
    message = json.dumps(response_json, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode('utf-8')
    print(message)
    response_hmac = hmac.new(SHARED_SECRET.encode(), message, hashlib.sha256).hexdigest()
    return response_hmac


@app.route("/latest-traffic", methods=["GET"])
def get_traffic_data():
    if not verify_hmac(request):
        return jsonify({"error": "Unauthorized"}), 403

    response_timestamp = str(int(time.time()))
    #telling main thread to not use traffic_data list while being updated
    with data_lock:
        try:
            response_json = {"data": traffic_data, "timestamp": response_timestamp}
            response_hmac = generate_response_hmac(response_json)
            #print(response_hmac)
            return jsonify({
                "data": traffic_data,
                "timestamp": response_timestamp,
                "hmac": response_hmac  # Send signed HMAC to frontend
            })
        except Exception as e:
            return jsonify({"error": "Unable to Fulfill Request"}), 500

if __name__ == "__main__":
    threading.Thread(target=update_traffic_data, daemon=True).start()
    app.run(host=server_ipv4, port=server_port, debug=False)

