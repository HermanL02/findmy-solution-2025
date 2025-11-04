#!/usr/bin/env python3
"""
Device Location Tracker with MongoDB Storage (Docker Version)
Runs continuously by default for Docker containers
"""

import os
import sys
import time
import pickle
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pyicloud import PyiCloudService

# Load environment variables
load_dotenv()


def connect_to_mongodb():
    """Connect to MongoDB using URI from environment"""
    mongodb_uri = os.getenv('MONGODB_URI')

    if not mongodb_uri:
        print("❌ Error: MONGODB_URI environment variable not set")
        print("Please set MONGODB_URI in docker-compose.yml or pass via -e flag")
        return None

    try:
        print("🔗 Connecting to MongoDB...")
        client = MongoClient(mongodb_uri)

        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!\n")

        # Use 'findmy' database and 'device_locations' collection
        db = client['findmy']
        collection = db['device_locations']

        return collection
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return None


def load_icloud_session():
    """Load saved iCloud session"""
    session_file = "icloud_session.pkl"

    if not os.path.exists(session_file):
        print(f"❌ Error: No saved session found at {session_file}")
        print("Please ensure icloud_session.pkl is mounted in the container")
        return None

    try:
        print("📱 Loading iCloud session...")
        with open(session_file, 'rb') as f:
            session_data = pickle.load(f)

        api = PyiCloudService(
            session_data['email'],
            session_data['password']
        )

        # Check if re-authentication is needed
        if api.requires_2fa or api.requires_2sa:
            print("❌ Session expired. Please re-authenticate on host machine.")
            print("Run: poetry run python setup/icloud_auth.py")
            return None

        print("✅ iCloud session loaded successfully!\n")
        return api

    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None


def fetch_device_locations(api):
    """Fetch current locations for all devices"""
    try:
        devices = api.devices
        locations = []

        for device in devices:
            data = device.data
            status = device.status()

            try:
                location = device.location()
            except:
                location = None

            device_info = {
                "device_id": data.get('id'),
                "name": data.get('name', 'Unknown'),
                "model": data.get('deviceDisplayName', 'Unknown'),
                "device_class": data.get('deviceClass', 'Unknown'),
                "raw_model": data.get('rawDeviceModel', 'Unknown'),
                "battery_level": status.get('batteryLevel'),
                "battery_status": status.get('batteryStatus'),
                "device_status": data.get('deviceStatus'),
                "location_enabled": data.get('locationEnabled', False),
                "timestamp": datetime.now()
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
            else:
                device_info["location"] = None
                device_info["location_data"] = None

            locations.append(device_info)

        return locations

    except Exception as e:
        print(f"❌ Error fetching device locations: {e}")
        import traceback
        traceback.print_exc()
        return []


def save_to_mongodb(collection, locations):
    """Save device locations to MongoDB"""
    if not locations:
        print("⚠️  No location data to save")
        return 0

    try:
        result = collection.insert_many(locations)
        return len(result.inserted_ids)
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return 0


def display_summary(locations, iteration):
    """Display summary of tracked locations"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("=" * 80)
    print(f"📍 Iteration #{iteration} - {timestamp}")
    print(f"📊 Tracked {len(locations)} device(s)")
    print("=" * 80)

    for loc in locations:
        status_icon = "🟢" if loc.get('location_data') else "🔴"
        battery = loc.get('battery_level')
        battery_str = f"{battery * 100:.0f}%" if battery is not None else "N/A"

        print(f"{status_icon} {loc['name']} ({loc['model']}) - Battery: {battery_str}")

        if loc.get('location_data'):
            lat = loc['location_data']['latitude']
            lon = loc['location_data']['longitude']
            acc = loc['location_data']['accuracy']
            print(f"   📌 {lat:.6f}, {lon:.6f} (±{acc}m)")

    print("=" * 80)


def track_continuously(api, collection, interval):
    """
    Continuously track device locations

    Args:
        api: PyiCloudService instance
        collection: MongoDB collection
        interval: Tracking interval in seconds
    """
    print("=" * 80)
    print("🚀 Starting Continuous Location Tracker")
    print("=" * 80)
    print(f"⏱️  Tracking interval: {interval} seconds ({interval/60:.1f} minutes)")
    print(f"💾 Database: findmy.device_locations")
    print(f"🔄 Mode: Infinite loop")
    print("⏹️  Stop with: docker-compose down or Ctrl+C")
    print("=" * 80)
    print()

    iteration = 0

    try:
        while True:
            iteration += 1

            # Fetch device locations
            locations = fetch_device_locations(api)

            # Display summary
            display_summary(locations, iteration)

            # Save to MongoDB
            saved_count = save_to_mongodb(collection, locations)

            if saved_count > 0:
                print(f"✅ Saved {saved_count} records to MongoDB\n")
            else:
                print(f"⚠️  Failed to save records\n")

            # Wait for next iteration
            print(f"⏳ Next update in {interval} seconds...")
            print()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n⏹️  Tracking stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error during tracking: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("🍎 Apple Device Location Tracker (Docker Version)")
    print("=" * 80)
    print()

    # Get tracking interval from environment
    interval = int(os.getenv('TRACKING_INTERVAL', '300'))

    # Connect to MongoDB
    collection = connect_to_mongodb()
    if collection is None:
        return 1

    # Load iCloud session
    api = load_icloud_session()
    if api is None:
        return 1

    # Start continuous tracking
    track_continuously(api, collection, interval)

    return 0


if __name__ == "__main__":
    sys.exit(main())
