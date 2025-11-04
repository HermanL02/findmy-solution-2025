# 🚀 Quick Start Guide

## Docker (Recommended) ⚡

### First Time Setup
```bash
# 1. Go to root directory
cd /path/to/findmy

# 2. Generate API key
python -c 'import secrets; print(secrets.token_urlsafe(32))'
# Save this key!

# 3. Configure .env
cp .env.example .env
nano .env  # Add MongoDB URI and API_KEY

# 4. Authenticate with iCloud (one-time)
poetry install
poetry run python setup/icloud_auth.py

# 5. Start with Docker
cd track_location
./docker-start.sh
```

### Daily Usage
```bash
cd track_location

# Start
./docker-start.sh

# View logs
./docker-logs.sh

# Stop
./docker-stop.sh

# Restart
./docker-restart.sh
```

---

## Direct Python Run 🐍

### Start
```bash
cd track_location
./start.sh
```

---

## API Usage 📡

**Note:** Replace `YOUR_API_KEY` with your actual API key from `.env`

### Trigger Alarm on iPhone 16 Pro
```bash
curl -X POST -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/alarm
```

### Get Latest Location
```bash
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/location
```

### Check Device Status
```bash
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/status
```

### Health Check (no auth needed)
```bash
curl http://localhost:5000/
```

---

## Troubleshooting 🔧

### Session Expired
```bash
cd /path/to/findmy
poetry run python setup/icloud_auth.py
```

### View Docker Logs
```bash
cd track_location
./docker-logs.sh
```

### Rebuild Docker Image
```bash
cd track_location
docker-compose build --no-cache
docker-compose up -d
```

### Check Container Status
```bash
docker ps | grep iphone-location-tracker
```

---

## Configuration ⚙️

Edit `.env` file in root directory:
```
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?appName=App
API_KEY=your_generated_secure_api_key_here  # REQUIRED!
TRACKING_INTERVAL=300  # seconds (default: 5 minutes)
PORT=5000              # API port
HOST=0.0.0.0           # API host
```

⚠️ **Security:** The API_KEY protects your endpoints. Keep it secret!

---

## File Locations 📁

```
findmy/
├── .env                           ← Configuration
├── icloud_session.pkl              ← iCloud session (auto-generated)
├── setup/icloud_auth.py            ← Run to authenticate
└── track_location/
    ├── app.py                      ← Main application
    ├── docker-start.sh             ← Start Docker
    ├── docker-stop.sh              ← Stop Docker
    ├── docker-logs.sh              ← View logs
    └── start.sh                    ← Direct Python run
```

---

## Need Help? 📖

- Full documentation: `track_location/README.md`
- Main project docs: `../README.md`
- Docker setup: `track_location/Dockerfile`
