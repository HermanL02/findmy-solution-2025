#!/bin/bash
# Start the location tracker in Docker

echo "🚀 Starting FindMy Location Tracker..."
echo ""

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "❌ Error: .env file not found in parent directory"
    echo "Please create ../.env with MONGODB_URI"
    exit 1
fi

# Check if icloud_session.pkl exists
if [ ! -f "../icloud_session.pkl" ]; then
    echo "❌ Error: icloud_session.pkl not found"
    echo "Please authenticate first:"
    echo "  poetry run python setup/icloud_auth.py"
    exit 1
fi

# Build and start the container
echo "🔨 Building Docker image..."
docker-compose up --build -d

echo ""
echo "✅ Location tracker started!"
echo ""
echo "Commands:"
echo "  View logs:    ./logs.sh"
echo "  Stop tracker: ./stop.sh"
echo "  Restart:      ./restart.sh"
echo ""
