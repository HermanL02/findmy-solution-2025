# 🐳 Docker Setup - Complete Guide

## What Was Created

### Docker Files
- **Dockerfile** - Python 3.12 slim image with Flask app
- **docker-compose.yml** - Service configuration with health checks
- **.dockerignore** - Files excluded from Docker build

### Helper Scripts
- **docker-start.sh** - Builds and starts container
- **docker-stop.sh** - Stops and removes container
- **docker-logs.sh** - View real-time logs
- **docker-restart.sh** - Restart running container

---

## Quick Start (3 Steps)

### 1. Setup (First Time Only)
```bash
cd /path/to/findmy

# Configure environment
cp .env.example .env
nano .env  # Add: MONGODB_URI=mongodb+srv://...

# Authenticate with iCloud
poetry install
poetry run python setup/icloud_auth.py
```

### 2. Start with Docker
```bash
cd track_location
./docker-start.sh
```

### 3. Test the API
```bash
# Trigger alarm on your iPhone 16 Pro
curl -X POST http://localhost:5000/alarm

# Get location
curl http://localhost:5000/location
```

---

## Docker Architecture

### Container Features
- **Base Image**: python:3.12-slim (lightweight)
- **Port**: 5000 (configurable via .env)
- **Restart Policy**: unless-stopped
- **Health Checks**: Every 30s
- **Log Rotation**: Max 10MB, keep 3 files
- **Network**: Isolated bridge network

### Volume Mounts (Read-Only)
```
Parent Directory → Container
../icloud_session.pkl → /app/icloud_session.pkl
../.env → /app/.env
../account.json → /app/account.json
../ani_libs.bin → /app/ani_libs.bin
```

### Environment Variables
```
MONGODB_URI        - MongoDB connection string (required)
TRACKING_INTERVAL  - Seconds between updates (default: 300)
HOST              - API host (default: 0.0.0.0)
PORT              - API port (default: 5000)
```

---

## Management Commands

### Start Container
```bash
./docker-start.sh
# Or: docker compose up --build -d
```

### View Logs
```bash
./docker-logs.sh
# Or: docker compose logs -f
```

### Stop Container
```bash
./docker-stop.sh
# Or: docker compose down
```

### Restart Container
```bash
./docker-restart.sh
# Or: docker compose restart
```

### Check Status
```bash
docker ps | grep iphone-location-tracker
```

### View Resource Usage
```bash
docker stats iphone-location-tracker
```

---

## Advanced Usage

### Custom Tracking Interval
```bash
TRACKING_INTERVAL=600 docker compose up -d  # 10 minutes
```

### Custom Port
```bash
PORT=8080 docker compose up -d
```

### Rebuild Image from Scratch
```bash
docker compose build --no-cache
docker compose up -d
```

### Execute Commands in Container
```bash
# Check Python version
docker exec iphone-location-tracker python --version

# View running processes
docker exec iphone-location-tracker ps aux

# Interactive shell
docker exec -it iphone-location-tracker /bin/bash
```

### View Container Logs (Detailed)
```bash
# Last 100 lines
docker compose logs --tail=100

# Follow logs with timestamps
docker compose logs -f -t

# Logs from specific time
docker compose logs --since 2024-11-04T12:00:00
```

---

## Troubleshooting

### Issue: Container Won't Start

**Check if session file exists:**
```bash
ls -la ../icloud_session.pkl
```

**Solution:** Re-authenticate
```bash
cd ..
poetry run python setup/icloud_auth.py
```

### Issue: MongoDB Connection Failed

**Check MongoDB URI:**
```bash
cat ../.env | grep MONGODB_URI
```

**Test MongoDB connection:**
```bash
docker exec iphone-location-tracker python -c "
from pymongo import MongoClient
import os
client = MongoClient(os.getenv('MONGODB_URI'))
client.admin.command('ping')
print('Connected!')
"
```

### Issue: Port Already in Use

**Find process using port 5000:**
```bash
sudo lsof -i :5000
```

**Use different port:**
```bash
PORT=8080 docker compose up -d
```

### Issue: Container Crashes Repeatedly

**View crash logs:**
```bash
docker compose logs --tail=100
```

**Check health status:**
```bash
docker inspect iphone-location-tracker | grep -A 10 Health
```

### Issue: Session Expired in Container

**Update session file:**
```bash
cd ..
poetry run python setup/icloud_auth.py
cd track_location
./docker-restart.sh
```

---

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/iphone-tracker.service`:
```ini
[Unit]
Description=iPhone Location Tracker
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/findmy/track_location
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable iphone-tracker
sudo systemctl start iphone-tracker
```

### Monitoring

**Set up alerts:**
```bash
# Check if container is running
docker ps | grep iphone-location-tracker || echo "Container down!"

# Check health
docker inspect iphone-location-tracker | grep -q '"Status": "healthy"' || echo "Unhealthy!"
```

### Backup Important Files

```bash
# Backup session and config
tar -czf backup-$(date +%Y%m%d).tar.gz \
  ../.env \
  ../icloud_session.pkl \
  ../account.json
```

---

## Security Considerations

### Read-Only Mounts
All volume mounts are read-only to prevent container from modifying host files.

### Network Isolation
Container runs in isolated bridge network, not host network.

### No Root User (Recommended)
To run as non-root user, add to Dockerfile:
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Secrets Management
Never commit `.env` file. Use environment-specific configs:
```bash
# Development
.env.dev

# Production
.env.prod
```

---

## Performance Optimization

### Reduce Image Size
Currently using `python:3.12-slim` (~150MB)

### Health Check Tuning
Adjust in `docker-compose.yml`:
```yaml
healthcheck:
  interval: 60s      # Check every minute
  timeout: 5s        # Wait 5 seconds
  start_period: 30s  # Grace period on startup
  retries: 3         # Retry 3 times before unhealthy
```

### Resource Limits
Add to `docker-compose.yml`:
```yaml
services:
  iphone-tracker:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

---

## Uninstall

### Stop and Remove Container
```bash
cd track_location
./docker-stop.sh
```

### Remove Docker Image
```bash
docker rmi $(docker images | grep iphone-tracker | awk '{print $3}')
```

### Remove All Docker Resources
```bash
docker compose down --volumes --rmi all
```

---

## Support

For issues:
1. Check logs: `./docker-logs.sh`
2. Verify session: `ls -la ../icloud_session.pkl`
3. Test MongoDB: Check connection string in `.env`
4. Review README: `track_location/README.md`

