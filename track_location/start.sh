#!/bin/bash
# Quick start script for iPhone Location Tracker

echo "=========================================="
echo "iPhone Location Tracker API"
echo "=========================================="
echo ""

# Check if .env exists in parent directory
if [ ! -f ../.env ]; then
    echo "❌ Error: .env file not found in parent directory"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# Check if icloud_session.pkl exists in parent directory
if [ ! -f ../icloud_session.pkl ]; then
    echo "❌ Error: icloud_session.pkl not found in parent directory"
    echo "Please authenticate with iCloud first:"
    echo "  cd .. && poetry run python setup/icloud_auth.py"
    echo ""
    exit 1
fi

echo "✓ Configuration files found"
echo "Starting application..."
echo ""

# Run the app from parent directory
cd .. && poetry run python track_location/app.py
