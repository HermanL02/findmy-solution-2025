#!/usr/bin/env python3
"""
FindMy.py Authentication Script
This script handles Apple Account authentication with 2FA support
"""

import os
import json
from pathlib import Path
from findmy import AppleAccount, LocalAnisetteProvider, LoginState
from findmy import TrustedDeviceSecondFactorMethod, SmsSecondFactorMethod


def login_new_account():
    """Login to a new Apple Account and save the session"""

    # Step 1: Create Anisette provider and AppleAccount instance
    print("Initializing FindMy.py...")
    ani = LocalAnisetteProvider(libs_path="ani_libs.bin")
    account = AppleAccount(ani)

    # Step 2: Get credentials from user
    email = input("Apple ID email: ").strip()
    password = input("Password: ").strip()

    print("\nLogging in...")
    state = account.login(email, password)

    # Step 3: Handle 2FA if required
    if state == LoginState.REQUIRE_2FA:
        print("\n2FA authentication required.")
        methods = account.get_2fa_methods()

        print("\nAvailable 2FA methods:")
        for i, method in enumerate(methods):
            if isinstance(method, TrustedDeviceSecondFactorMethod):
                print(f"{i} - Trusted Device")
            elif isinstance(method, SmsSecondFactorMethod):
                print(f"{i} - SMS ({method.phone_number})")

        # Request 2FA code
        method_index = int(input("\nSelect method (enter number): ").strip())
        selected_method = methods[method_index]

        print("\nRequesting 2FA code...")
        selected_method.request()

        code = input("Enter the 2FA code you received: ").strip()

        print("Submitting code...")
        selected_method.submit(code)

        print("2FA authentication successful!")

    elif state == LoginState.LOGGED_IN:
        print("Login successful! (No 2FA required)")
    else:
        print(f"Unexpected login state: {state}")
        account.close()
        return None

    # Step 4: Save the session
    session_file = "account.json"
    print(f"\nSaving session to {session_file}...")
    account.to_json(session_file)
    print("Session saved successfully!")

    return account


def restore_session():
    """Restore a previously saved Apple Account session"""

    session_file = "account.json"
    if not os.path.exists(session_file):
        print(f"No saved session found at {session_file}")
        return None

    print(f"Restoring session from {session_file}...")
    account = AppleAccount.from_json(session_file, anisette_libs_path="ani_libs.bin")
    print("Session restored successfully!")

    return account


def main():
    """Main entry point for the authentication script"""

    print("=" * 50)
    print("FindMy.py Authentication Setup")
    print("=" * 50)

    session_file = "account.json"

    if os.path.exists(session_file):
        print(f"\nFound existing session file: {session_file}")
        choice = input("Do you want to (u)se existing session or create a (n)ew one? [u/n]: ").strip().lower()

        if choice == 'u':
            account = restore_session()
        else:
            account = login_new_account()
    else:
        print("\nNo existing session found. Creating new session...")
        account = login_new_account()

    if account:
        print("\n" + "=" * 50)
        print("Authentication complete!")
        print("=" * 50)
        print(f"\nYour session has been saved to: {session_file}")
        print("You can now use this session to track FindMy devices.")
        print("\nClosing account session...")
        account.close()
        print("Done!")
    else:
        print("\nAuthentication failed.")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
