#!/bin/bash
# Restart the location tracker

echo "🔄 Restarting FindMy Location Tracker..."
docker-compose restart

echo "✅ Location tracker restarted!"
echo "View logs with: ./logs.sh"
