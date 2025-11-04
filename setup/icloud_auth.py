#!/usr/bin/env python3
"""
iCloud Authentication Script
This script handles Apple Account authentication using pyicloud
"""

import os
import pickle
from pyicloud import PyiCloudService


def authenticate():
    """Authenticate with iCloud"""

    print("=" * 80)
    print("iCloud Authentication")
    print("=" * 80)
    print()

    # Get credentials
    email = input("Apple ID email: ").strip()
    password = input("Password: ").strip()

    print("\nAuthenticating...")

    try:
        # Create PyiCloudService instance
        api = PyiCloudService(email, password)

        # Check if 2FA is required
        if api.requires_2fa:
            print("\n2FA authentication required.")
            code = input("Enter the 2FA code you received: ").strip()

            result = api.validate_2fa_code(code)

            if not result:
                print("Failed to verify 2FA code")
                return None

            print("2FA authentication successful!")

            # You may need to trust this device
            if not api.is_trusted_session:
                print("\nTrusting this session...")
                result = api.trust_session()

                if not result:
                    print("Failed to trust session. You may need to authenticate again later.")
                else:
                    print("Session trusted!")

        # Check if 2SA (two-step authentication) is required instead
        elif api.requires_2sa:
            print("\n2SA (Two-Step Authentication) required.")

            # Get available devices
            devices = api.trusted_devices
            print("\nTrusted devices:")
            for i, device in enumerate(devices):
                print(f"{i}: {device.get('deviceName', 'Unknown Device')} "
                      f"({device.get('phoneNumber', 'No number')})")

            device_index = int(input("\nSelect device (enter number): ").strip())
            selected_device = devices[device_index]

            # Request SMS code
            if not api.send_verification_code(selected_device):
                print("Failed to send verification code")
                return None

            code = input("\nEnter the verification code: ").strip()

            if not api.validate_verification_code(selected_device, code):
                print("Failed to verify code")
                return None

            print("2SA authentication successful!")

        print("\n" + "=" * 80)
        print("Authentication successful!")
        print("=" * 80)

        # Save session to root directory
        session_file = "icloud_session.pkl"
        with open(session_file, 'wb') as f:
            pickle.dump({
                'email': email,
                'password': password,
                'cookies': api.session.cookies
            }, f)

        print(f"\nSession saved to: {session_file}")
        print("You can now use icloud_track.py to track your devices.")

        return api

    except Exception as e:
        print(f"\nAuthentication failed: {e}")
        return None


def main():
    """Main entry point"""
    api = authenticate()

    if api:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
