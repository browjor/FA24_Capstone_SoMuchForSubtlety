from flask import Flask, jsonify, request
import hmac, hashlib, time, os, threading, json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from backend.database.create_db import CurrentCamera, TrafficCount

load_dotenv()
SHARED_SECRET = os.getenv('SHARED_SECRET')
server_ipv4 = os.getenv('SERVER_IPV4')
server_port = int(os.getenv('SERVER_PORT'))
engine = create_engine(os.getenv('SQLite_DB_LOC'))
data_condition = threading.Condition()
traffic_data = []
app = Flask(__name__)


def fetch_traffic_data_from_db():
    traffic_data = []
    Session = sessionmaker(bind=engine)
    session = Session()

    latest_cameras = (
        session.query(
            CurrentCamera.camera_id,
            CurrentCamera.latitude,
            CurrentCamera.longitude
        )
        .filter(CurrentCamera.cam_status == "Online")
        .order_by(CurrentCamera.last_update.desc())  # Ensures the most recent cameras are selected
        .distinct(CurrentCamera.camera_id)  # Ensures distinct camera entries
        .all()
    )

    # Step 2: For each camera, find the most recent traffic_count and max_traffic_count
    for cam in latest_cameras:
        latest_traffic = (
            session.query(
                TrafficCount.traffic_count,
                TrafficCount.max_traffic_count
            )
            .filter(TrafficCount.cam_id == cam.camera_id)
            .order_by(TrafficCount.traffic_time.desc())  # Get the latest traffic data
            .first()
        )

        if latest_traffic:  # Ensure there's a valid traffic count entry
            density = latest_traffic.traffic_count / latest_traffic.max_traffic_count if latest_traffic.max_traffic_count else 0
            traffic_data.append({'density': density, 'lat': cam.latitude, 'lon': cam.longitude})
            print(f"Cam ID: {cam.camera_id}, Density: {density}, Latitude: {cam.latitude}, Longitude: {cam.longitude}")


    session.commit()
    session.close()
    return traffic_data



def update_traffic_data():
    global traffic_data
    while True:
        new_data = fetch_traffic_data_from_db()

        with data_condition:
            print("[INFO] Updating traffic data...")
            traffic_data.clear()  # Clear old data
            traffic_data.extend(new_data)  # Update with new data
            data_condition.notify_all()  # Notify readers that data is updated

        time.sleep(9)  # Refresh every 9 seconds


def verify_hmac(request):
    """Verify HMAC-SHA256 authentication."""
    received_hmac = request.headers.get("X-HMAC-Signature")
    timestamp = request.headers.get("X-Timestamp")

    if not received_hmac or not timestamp:
        return False

    try:
        timestamp = int(timestamp)
    except ValueError:
        return False

    # Prevent replay attacks (accept timestamps within a 5-minute window)
    if abs(time.time() - timestamp) > 300:
        return False

    # Compute the expected HMAC
    message = f"{timestamp}".encode()
    expected_hmac = hmac.new(SHARED_SECRET.encode(), message, hashlib.sha256).hexdigest()

    return hmac.compare_digest(received_hmac, expected_hmac)

def generate_response_hmac(response_json, response_timestamp):
    """Generate HMAC signature for the response data and timestamp."""
    message = json.dumps(response_json, separators=(',', ':')).encode() + str(response_timestamp).encode()
    response_hmac = hmac.new(SHARED_SECRET.encode(), message, hashlib.sha256).hexdigest()
    return response_hmac

@app.route("/traffic-data", methods=["GET"])
def get_traffic_data():
    if not verify_hmac(request):
        return jsonify({"error": "Unauthorized"}), 403

    response_timestamp = int(time.time())  # Include timestamp in response
    with data_condition:
        data_condition.wait()  # Wait until traffic_data is fully updated
        response_json = {"data": traffic_data, "timestamp": response_timestamp}
        response_hmac = generate_response_hmac(response_json, response_timestamp)

    return jsonify({
        "data": traffic_data,
        "hmac": response_hmac  # Send signed HMAC to frontend
    })

if __name__ == "__main__":
    threading.Thread(target=update_traffic_data, daemon=True).start()
    app.run(host=server_ipv4, port=server_port, debug=False)

