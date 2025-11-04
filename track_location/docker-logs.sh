#!/bin/bash
# View logs from iPhone Location Tracker Docker container

echo "📊 Viewing iPhone Location Tracker logs..."
echo "Press Ctrl+C to exit"
echo ""

docker compose logs -f --tail=50
