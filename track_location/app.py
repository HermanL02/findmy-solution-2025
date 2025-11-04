#!/usr/bin/env python3
"""
iPhone Location Tracker with Alarm API
A single-file Flask app that tracks iPhone 16 Pro location to MongoDB
and provides an API endpoint to trigger the phone alarm.
"""

import os
import pickle
import threading
import time
import secrets
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pyicloud import PyiCloudService

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variables
icloud_api = None
mongo_collection = None
target_device = None
tracking_active = False

# API Key from environment
API_KEY = os.getenv('API_KEY')


def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip authentication if no API_KEY is set (for testing)
        if not API_KEY:
            return jsonify({
                "error": "API_KEY not configured",
                "message": "Please set API_KEY in .env file for security"
            }), 500

        # Check for API key in headers
        provided_key = request.headers.get('X-API-Key')

        # Also check query parameter as fallback
        if not provided_key:
            provided_key = request.args.get('api_key')

        if not provided_key:
            return jsonify({
                "error": "Missing API key",
                "message": "Provide API key via X-API-Key header or ?api_key= parameter"
            }), 401

        if provided_key != API_KEY:
            return jsonify({
                "error": "Invalid API key",
                "message": "The provided API key is incorrect"
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def connect_to_mongodb():
    """Connect to MongoDB and return the collection"""
    mongodb_uri = os.getenv('MONGODB_URI')

    if not mongodb_uri:
        raise ValueError("MONGODB_URI not found in .env file")

    client = MongoClient(mongodb_uri)
    client.admin.command('ping')
    print("✓ Connected to MongoDB")

    db = client['findmy']
    return db['device_locations']


def load_icloud_session():
    """Load saved iCloud session"""
    # Look for session file - check Docker location first, then parent directory
    docker_session_file = os.path.join(os.path.dirname(__file__), "icloud_session.pkl")
    parent_session_file = os.path.join(os.path.dirname(__file__), "..", "icloud_session.pkl")

    if os.path.exists(docker_session_file):
        session_file = docker_session_file
    else:
        session_file = parent_session_file

    if not os.path.exists(session_file):
        raise FileNotFoundError(
            f"No saved session found at {session_file}. "
            "Please run 'poetry run python setup/icloud_auth.py' first."
        )

    with open(session_file, 'rb') as f:
        session_data = pickle.load(f)

    api = PyiCloudService(
        session_data['email'],
        session_data['password']
    )

    # Try to access devices to verify session is valid
    try:
        _ = api.devices
        if api.requires_2fa or api.requires_2sa:
            raise Exception("Session expired. Please re-authenticate with setup/icloud_auth.py")
    except Exception as e:
        if "2FA" in str(e) or "authentication" in str(e).lower():
            raise Exception("Session expired. Please re-authenticate with setup/icloud_auth.py")
        raise

    print("✓ iCloud session loaded")
    return api


def find_target_device(api, model_name="iPhone 16 Pro"):
    """Find the target iPhone device"""
    devices = api.devices

    for device in devices:
        data = device.data
        if data.get('deviceDisplayName') == model_name:
            print(f"✓ Found target device: {data.get('name')} ({model_name})")
            return device

    raise Exception(f"Could not find device with model: {model_name}")


def track_location():
    """Background thread to continuously track location"""
    global icloud_api, mongo_collection, target_device, tracking_active

    print("🔄 Starting location tracking...")
    interval = int(os.getenv('TRACKING_INTERVAL', 300))  # Default 5 minutes

    while tracking_active:
        try:
            # Fetch device location
            data = target_device.data
            status = target_device.status()

            try:
                location = target_device.location
            except:
                location = None

            # Prepare document for MongoDB
            device_info = {
                "device_id": data.get('id'),
                "name": data.get('name', 'Unknown'),
                "model": data.get('deviceDisplayName', 'Unknown'),
                "device_class": data.get('deviceClass', 'Unknown'),
                "battery_level": status.get('batteryLevel'),
                "battery_status": status.get('batteryStatus')
                # timestamp will be auto-generated by MongoDB
            }

            if location:
                device_info["location"] = {
                    "type": "Point",
                    "coordinates": [
                        location.get('longitude'),
                        location.get('latitude')
                    ]
                }
                device_info["location_data"] = {
                    "latitude": location.get('latitude'),
                    "longitude": location.get('longitude'),
                    "accuracy": location.get('horizontalAccuracy'),
                    "position_type": location.get('positionType'),
                    "is_old": location.get('isOld', False),
                    "location_timestamp": location.get('timeStamp')
                }

                print(f"📍 Tracked: {device_info['location_data']['latitude']:.6f}, "
                      f"{device_info['location_data']['longitude']:.6f} "
                      f"(±{device_info['location_data']['accuracy']}m) "
                      f"Battery: {status.get('batteryLevel', 0) * 100:.0f}%")
            else:
                device_info["location"] = None
                device_info["location_data"] = None
                print("📍 Location not available")

            # Save to MongoDB with server-generated timestamp
            result = mongo_collection.insert_one(device_info)

            # Add server-generated timestamp (MongoDB $currentDate)
            mongo_collection.update_one(
                {"_id": result.inserted_id},
                {"$currentDate": {"timestamp": True}}
            )

        except Exception as e:
            print(f"Error tracking location: {e}")

        # Wait for next iteration
        time.sleep(interval)

    print("⏹️ Location tracking stopped")


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "iPhone Location Tracker",
        "tracking_active": tracking_active,
        "device": target_device.data.get('name') if target_device else None
    })


@app.route('/location', methods=['GET'])
@require_api_key
def get_location():
    """Get the latest location of the iPhone (requires API key)"""
    try:
        # Get the most recent location from MongoDB
        latest = mongo_collection.find_one(
            {"device_id": target_device.data.get('id')},
            sort=[("timestamp", -1)]
        )

        if not latest:
            return jsonify({"error": "No location data found"}), 404

        # Convert ObjectId to string for JSON serialization
        latest['_id'] = str(latest['_id'])
        latest['timestamp'] = latest['timestamp'].isoformat()

        return jsonify(latest)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/alarm', methods=['POST'])
@require_api_key
def trigger_alarm():
    """Trigger the alarm on the iPhone (requires API key)"""
    try:
        # Play sound on the device
        target_device.play_sound()

        return jsonify({
            "status": "success",
            "message": f"Alarm triggered on {target_device.data.get('name')}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/status', methods=['GET'])
@require_api_key
def get_status():
    """Get current device status (requires API key)"""
    try:
        status = target_device.status()
        data = target_device.data

        return jsonify({
            "device_id": data.get('id'),
            "name": data.get('name'),
            "model": data.get('deviceDisplayName'),
            "battery_level": status.get('batteryLevel'),
            "battery_status": status.get('batteryStatus'),
            "device_status": data.get('deviceStatus'),
            "location_enabled": data.get('locationEnabled'),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def initialize_app():
    """Initialize the application"""
    global icloud_api, mongo_collection, target_device, tracking_active

    print("=" * 80)
    print("iPhone Location Tracker with Alarm API")
    print("=" * 80)

    # Check API key configuration
    if not API_KEY:
        print("\n⚠️  WARNING: API_KEY not set in .env file!")
        print("Your API endpoints are not protected!")
        print("\nTo generate a secure API key, run:")
        print("  python -c 'import secrets; print(secrets.token_urlsafe(32))'")
        print("\nThen add to .env file:")
        print("  API_KEY=your_generated_key")
        print()
    else:
        print(f"\n✓ API Key authentication enabled")
        print(f"  Key: {API_KEY[:8]}..." if len(API_KEY) > 8 else "  Key: (too short)")

    # Connect to MongoDB
    mongo_collection = connect_to_mongodb()

    # Load iCloud session
    icloud_api = load_icloud_session()

    # Find target device (iPhone 16 Pro)
    target_device = find_target_device(icloud_api)

    # Start background tracking thread
    tracking_active = True
    tracking_thread = threading.Thread(target=track_location, daemon=True)
    tracking_thread.start()

    print("\n✓ Application initialized successfully!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        initialize_app()

        # Get port from environment or use default
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')

        print(f"\n🚀 Starting Flask server on {host}:{port}")
        print(f"\nAPI Endpoints:")
        print(f"  GET  /              - Health check")
        print(f"  GET  /location      - Get latest location")
        print(f"  GET  /status        - Get device status")
        print(f"  POST /alarm         - Trigger phone alarm")
        print("\n")

        app.run(host=host, port=port, debug=False)

    except KeyboardInterrupt:
        print("\n\n⏹️ Shutting down...")
        tracking_active = False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
