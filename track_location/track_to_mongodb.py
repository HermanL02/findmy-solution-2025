#!/usr/bin/env python3
"""
Device Location Tracker with MongoDB Storage
Continuously tracks device locations and stores them in MongoDB
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
    """Connect to MongoDB using URI from .env file"""
    mongodb_uri = os.getenv('MONGODB_URI')

    if not mongodb_uri:
        print("Error: MONGODB_URI not found in .env file")
        print("Please create a .env file in the root directory with:")
        print("MONGODB_URI=your_mongodb_connection_string")
        return None

    try:
        print("Connecting to MongoDB...")
        client = MongoClient(mongodb_uri)

        # Test connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB!\n")

        # Use 'findmy' database and 'device_locations' collection
        db = client['findmy']
        collection = db['device_locations']

        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def load_icloud_session():
    """Load saved iCloud session"""
    session_file = "icloud_session.pkl"

    if not os.path.exists(session_file):
        print(f"Error: No saved session found at {session_file}")
        print("Please run 'poetry run python setup/icloud_auth.py' first to authenticate.")
        return None

    try:
        print("Loading iCloud session...")
        with open(session_file, 'rb') as f:
            session_data = pickle.load(f)

        api = PyiCloudService(
            session_data['email'],
            session_data['password']
        )

        # Check if re-authentication is needed
        if api.requires_2fa or api.requires_2sa:
            print("\nSession expired. Please re-authenticate.")
            print("Run: poetry run python setup/icloud_auth.py")
            return None

        print("✓ iCloud session loaded successfully!\n")
        return api

    except Exception as e:
        print(f"Error loading session: {e}")
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
        print(f"Error fetching device locations: {e}")
        import traceback
        traceback.print_exc()
        return []


def save_to_mongodb(collection, locations):
    """Save device locations to MongoDB"""
    if not locations:
        print("No location data to save")
        return 0

    try:
        result = collection.insert_many(locations)
        return len(result.inserted_ids)
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        return 0


def display_summary(locations):
    """Display summary of tracked locations"""
    print("=" * 80)
    print(f"Tracked {len(locations)} device(s) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    for loc in locations:
        print(f"\n{loc['name']} ({loc['model']})")

        if loc.get('location_data'):
            lat = loc['location_data']['latitude']
            lon = loc['location_data']['longitude']
            acc = loc['location_data']['accuracy']
            print(f"  Location: {lat:.6f}, {lon:.6f} (±{acc}m)")
        else:
            print(f"  Location: Not available")

        battery = loc.get('battery_level')
        if battery is not None:
            print(f"  Battery: {battery * 100:.0f}%")

    print("=" * 80)


def track_continuously(api, collection, interval=300):
    """
    Continuously track device locations

    Args:
        api: PyiCloudService instance
        collection: MongoDB collection
        interval: Tracking interval in seconds (default: 300 = 5 minutes)
    """
    print(f"\n🔄 Starting continuous tracking (interval: {interval} seconds)")
    print("Press Ctrl+C to stop\n")

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Tracking iteration #{iteration} ---")

            # Fetch device locations
            locations = fetch_device_locations(api)

            # Display summary
            display_summary(locations)

            # Save to MongoDB
            saved_count = save_to_mongodb(collection, locations)
            print(f"✓ Saved {saved_count} location records to MongoDB")

            # Wait for next iteration
            print(f"\n⏳ Next update in {interval} seconds...")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n⏹️  Tracking stopped by user")
    except Exception as e:
        print(f"\nError during tracking: {e}")
        import traceback
        traceback.print_exc()


def track_once(api, collection):
    """Track device locations once and save to MongoDB"""
    print("\n--- Single Location Update ---\n")

    # Fetch device locations
    locations = fetch_device_locations(api)

    # Display summary
    display_summary(locations)

    # Save to MongoDB
    saved_count = save_to_mongodb(collection, locations)
    print(f"\n✓ Saved {saved_count} location records to MongoDB")


def main():
    """Main entry point"""
    print("=" * 80)
    print("Device Location Tracker with MongoDB")
    print("=" * 80)
    print()

    # Connect to MongoDB
    collection = connect_to_mongodb()
    if collection is None:
        return 1

    # Load iCloud session
    api = load_icloud_session()
    if api is None:
        return 1

    # Ask user for tracking mode
    print("Tracking modes:")
    print("1. Track once and exit")
    print("2. Continuous tracking (every 5 minutes)")
    print("3. Continuous tracking (custom interval)")

    try:
        choice = input("\nSelect mode [1-3]: ").strip()
    except EOFError:
        # Default to track once if running non-interactively
        choice = "1"

    if choice == "1":
        track_once(api, collection)
    elif choice == "2":
        track_continuously(api, collection, interval=300)
    elif choice == "3":
        try:
            interval = int(input("Enter tracking interval in seconds: ").strip())
            track_continuously(api, collection, interval=interval)
        except (ValueError, EOFError):
            print("Invalid interval. Using default 300 seconds.")
            track_continuously(api, collection, interval=300)
    else:
        print("Invalid choice. Tracking once.")
        track_once(api, collection)

    print("\n✓ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
