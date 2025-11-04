#!/bin/bash
# Start iPhone Location Tracker with Docker

echo "=========================================="
echo "iPhone Location Tracker - Docker Mode"
echo "=========================================="
echo ""

# Check if .env exists in parent directory
if [ ! -f ../.env ]; then
    echo "❌ Error: .env file not found in parent directory"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cd .. && cp .env.example .env"
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
echo ""

# Check if container is already running
if docker ps | grep -q iphone-location-tracker; then
    echo "⚠️  Container is already running!"
    echo "To restart, run: ./docker-restart.sh"
    echo "To stop, run: ./docker-stop.sh"
    echo "To view logs, run: ./docker-logs.sh"
    exit 0
fi

echo "Building and starting Docker container..."
echo ""

# Build and start
docker compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Container started successfully!"
    echo ""
    echo "📊 View logs:"
    echo "  ./docker-logs.sh"
    echo ""
    echo "🔍 Check status:"
    echo "  docker ps | grep iphone-location-tracker"
    echo ""
    echo "🌐 API Endpoints:"
    echo "  http://localhost:5000/          - Health check"
    echo "  http://localhost:5000/location  - Get latest location"
    echo "  http://localhost:5000/status    - Device status"
    echo ""
    echo "🚨 Trigger alarm:"
    echo "  curl -X POST http://localhost:5000/alarm"
    echo ""
    echo "⏹️  Stop container:"
    echo "  ./docker-stop.sh"
    echo ""
else
    echo ""
    echo "❌ Failed to start container"
    exit 1
fi
