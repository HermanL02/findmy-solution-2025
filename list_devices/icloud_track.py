#!/usr/bin/env python3
"""
iCloud Device Tracker
This script tracks your Apple devices using pyicloud
"""

import os
import sys
import json
import pickle
from datetime import datetime
from pyicloud import PyiCloudService


def load_session():
    """Load saved iCloud session or create new one"""

    session_file = "icloud_session.pkl"

    if not os.path.exists(session_file):
        print(f"Error: No saved session found at {session_file}")
        print("Please run 'poetry run python setup/icloud_auth.py' first to authenticate.")
        return None

    print("Loading saved session...")

    try:
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

        print("Session loaded successfully!\n")
        return api

    except Exception as e:
        print(f"Error loading session: {e}")
        print("Please re-authenticate with: poetry run python setup/icloud_auth.py")
        return None


def fetch_devices(api):
    """Fetch all devices from Find My iPhone"""

    print("Fetching your devices...")

    try:
        devices = api.devices
        return devices
    except Exception as e:
        print(f"Error fetching devices: {e}")
        import traceback
        traceback.print_exc()
        return []


def display_device_info(devices):
    """Display information about each device"""

    if not devices:
        print("No devices found.")
        return

    print(f"Found {len(devices)} device(s):\n")
    print("=" * 80)

    for i, device in enumerate(devices, 1):
        print(f"\nDevice #{i}")
        print("-" * 80)

        # Basic info
        data = device.data
        status = device.status()

        print(f"Name: {data.get('name', 'Unknown')}")
        print(f"Model: {data.get('deviceDisplayName', 'Unknown')}")
        print(f"Device Class: {data.get('deviceClass', 'Unknown')}")
        print(f"Device Model: {data.get('rawDeviceModel', 'Unknown')}")

        # Location info
        try:
            location = device.location()
        except:
            location = None

        if location:
            print(f"\nLocation:")
            print(f"  Latitude: {location.get('latitude', 'N/A')}")
            print(f"  Longitude: {location.get('longitude', 'N/A')}")
            print(f"  Accuracy: {location.get('horizontalAccuracy', 'N/A')} meters")

            # Timestamp
            timestamp = location.get('timeStamp')
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1000)
                print(f"  Last Updated: {dt.strftime('%Y-%m-%d %H:%M:%S')}")

            # Position type
            position_type = location.get('positionType', 'Unknown')
            print(f"  Position Type: {position_type}")

            # Is old location
            is_old = location.get('isOld', False)
            print(f"  Is Old Location: {is_old}")
        else:
            print("\nLocation: Not available")

        # Battery info
        battery_level = status.get('batteryLevel')
        if battery_level is not None:
            print(f"\nBattery: {battery_level * 100:.0f}%")

        battery_status = status.get('batteryStatus')
        if battery_status:
            print(f"Battery Status: {battery_status}")

        # Device status
        device_status = data.get('deviceStatus')
        if device_status:
            print(f"Device Status: {device_status}")

        # Lost mode
        lost_mode_capable = data.get('lostModeCapable', False)
        print(f"Lost Mode Capable: {lost_mode_capable}")

        # Location enabled
        location_enabled = data.get('locationEnabled', False)
        print(f"Location Enabled: {location_enabled}")

        print("=" * 80)


def export_to_json(devices, filename="icloud_devices.json"):
    """Export device data to JSON file"""

    device_data = []

    for device in devices:
        data = device.data
        status = device.status()

        try:
            location = device.location()
        except:
            location = None

        device_info = {
            "name": data.get('name', 'Unknown'),
            "model": data.get('deviceDisplayName', 'Unknown'),
            "device_class": data.get('deviceClass', 'Unknown'),
            "raw_model": data.get('rawDeviceModel', 'Unknown'),
            "device_status": data.get('deviceStatus', 'Unknown'),
            "battery_level": status.get('batteryLevel'),
            "battery_status": status.get('batteryStatus'),
            "location_enabled": data.get('locationEnabled', False),
            "lost_mode_capable": data.get('lostModeCapable', False)
        }

        if location:
            device_info["location"] = {
                "latitude": location.get('latitude'),
                "longitude": location.get('longitude'),
                "accuracy": location.get('horizontalAccuracy'),
                "timestamp": location.get('timeStamp'),
                "position_type": location.get('positionType'),
                "is_old": location.get('isOld', False)
            }

        device_data.append(device_info)

    with open(filename, 'w') as f:
        json.dump(device_data, f, indent=2)

    print(f"\nDevice data exported to {filename}")


def play_sound(device):
    """Play a sound on the device"""
    print(f"\nPlaying sound on '{device.data.get('name')}'...")
    device.play_sound()
    print("Sound request sent!")


def main():
    """Main entry point"""

    print("=" * 80)
    print("iCloud Device Tracker")
    print("=" * 80)
    print()

    # Load session
    api = load_session()
    if not api:
        return 1

    try:
        # Fetch devices
        devices = fetch_devices(api)

        # Display device info
        display_device_info(devices)

        # Interactive menu
        if devices:
            print("\nOptions:")
            print("1. Export device data to JSON")
            print("2. Play sound on a device")
            print("3. Exit")

            choice = input("\nEnter your choice [1-3]: ").strip()

            if choice == '1':
                export_to_json(devices)
            elif choice == '2':
                for i, device in enumerate(devices):
                    print(f"{i}: {device.data.get('name')}")
                device_index = int(input("\nSelect device (enter number): ").strip())
                if 0 <= device_index < len(devices):
                    play_sound(devices[device_index])
                else:
                    print("Invalid device number")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
