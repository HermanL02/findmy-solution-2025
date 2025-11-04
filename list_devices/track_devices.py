#!/usr/bin/env python3
"""
FindMy Device Tracker
This script tracks your Apple devices using a saved FindMy.py session
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from findmy import AppleAccount


async def load_account():
    """Load saved Apple Account session"""
    session_file = "account.json"

    if not os.path.exists(session_file):
        print(f"Error: No saved session found at {session_file}")
        print("Please run 'poetry run python findmy_auth.py' first to authenticate.")
        return None

    print("Loading saved session...")
    account = AppleAccount.from_json(session_file, anisette_libs_path="ani_libs.bin")
    print("Session loaded successfully!\n")

    return account


async def fetch_devices(account):
    """Fetch all devices associated with the account"""
    print("Fetching your devices...")

    try:
        # Fetch current locations from FindMy
        locations = await account.fetch_location()
        return locations
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

        # Basic info - try different attribute names
        name = getattr(device, 'name', getattr(device, 'deviceName', 'Unknown'))
        print(f"Name: {name}")

        model = getattr(device, 'model_display_name',
                       getattr(device, 'deviceDisplayName',
                              getattr(device, 'deviceModel', 'Unknown')))
        print(f"Model: {model}")

        device_class = getattr(device, 'device_class',
                              getattr(device, 'deviceClass', 'Unknown'))
        print(f"Device Class: {device_class}")

        # Location info
        location = getattr(device, 'location', None)
        if location:
            print(f"\nLocation:")

            lat = getattr(location, 'latitude', getattr(location, 'lat', None))
            lon = getattr(location, 'longitude', getattr(location, 'lon', None))

            if lat and lon:
                print(f"  Latitude: {lat}")
                print(f"  Longitude: {lon}")

            accuracy = getattr(location, 'horizontal_accuracy',
                             getattr(location, 'horizontalAccuracy', 'N/A'))
            print(f"  Accuracy: {accuracy} meters" if accuracy != 'N/A' else f"  Accuracy: {accuracy}")

            # Timestamp
            timestamp = getattr(location, 'timestamp',
                              getattr(location, 'timeStamp', None))
            if timestamp:
                try:
                    dt = datetime.fromtimestamp(timestamp / 1000)  # Convert from milliseconds
                    print(f"  Last Updated: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"  Last Updated: {timestamp}")

            # Address if available
            address = getattr(location, 'address', None)
            if address:
                print(f"  Address: {address}")
        else:
            print("\nLocation: Not available")

        # Battery info
        battery = getattr(device, 'battery_level',
                         getattr(device, 'batteryLevel', None))
        if battery is not None:
            print(f"\nBattery: {battery * 100:.0f}%")

        # Battery status
        battery_status = getattr(device, 'battery_status',
                                getattr(device, 'batteryStatus', None))
        if battery_status:
            print(f"Battery Status: {battery_status}")

        # Online status
        is_online = getattr(device, 'is_online',
                           getattr(device, 'isOnline', None))
        if is_online is not None:
            status = "Online" if is_online else "Offline"
            print(f"Status: {status}")

        print("=" * 80)


def export_to_json(devices, filename="devices.json"):
    """Export device data to JSON file"""

    device_data = []
    for device in devices:
        data = {
            "name": getattr(device, 'name', getattr(device, 'deviceName', 'Unknown')),
            "model": getattr(device, 'model_display_name',
                           getattr(device, 'deviceDisplayName',
                                  getattr(device, 'deviceModel', 'Unknown'))),
            "device_class": getattr(device, 'device_class',
                                   getattr(device, 'deviceClass', 'Unknown')),
        }

        location = getattr(device, 'location', None)
        if location:
            lat = getattr(location, 'latitude', getattr(location, 'lat', None))
            lon = getattr(location, 'longitude', getattr(location, 'lon', None))
            accuracy = getattr(location, 'horizontal_accuracy',
                             getattr(location, 'horizontalAccuracy', None))
            timestamp = getattr(location, 'timestamp',
                              getattr(location, 'timeStamp', None))
            address = getattr(location, 'address', None)

            data["location"] = {
                "latitude": lat,
                "longitude": lon,
                "accuracy": accuracy,
                "timestamp": timestamp,
                "address": address
            }

        battery = getattr(device, 'battery_level',
                         getattr(device, 'batteryLevel', None))
        if battery is not None:
            data["battery_level"] = battery

        is_online = getattr(device, 'is_online',
                           getattr(device, 'isOnline', None))
        if is_online is not None:
            data["is_online"] = is_online

        device_data.append(data)

    with open(filename, 'w') as f:
        json.dump(device_data, f, indent=2)

    print(f"\nDevice data exported to {filename}")


async def main():
    """Main entry point"""
    print("=" * 80)
    print("FindMy Device Tracker")
    print("=" * 80)
    print()

    # Load account
    account = await load_account()
    if not account:
        return 1

    try:
        # Fetch devices
        devices = await fetch_devices(account)

        # Display device info
        display_device_info(devices)

        # Ask if user wants to export
        if devices:
            export = input("\nWould you like to export device data to JSON? [y/N]: ").strip().lower()
            if export == 'y':
                export_to_json(devices)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Always close the account
        print("\nClosing session...")
        await account.close()
        print("Done!")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
