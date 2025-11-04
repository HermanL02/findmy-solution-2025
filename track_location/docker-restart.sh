#!/bin/bash
# Restart iPhone Location Tracker Docker container

echo "Restarting iPhone Location Tracker..."
docker compose restart

if [ $? -eq 0 ]; then
    echo "✅ Container restarted successfully"
    echo ""
    echo "📊 View logs:"
    echo "  ./docker-logs.sh"
else
    echo "❌ Failed to restart container"
    exit 1
fi
