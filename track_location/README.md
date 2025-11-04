# iPhone Location Tracker API

A single-file Flask application that continuously tracks your iPhone 16 Pro location to MongoDB and provides API endpoints to trigger the phone alarm.

## Features

- 🔄 **Continuous Location Tracking**: Automatically tracks your iPhone location in the background
- 💾 **MongoDB Storage**: Stores location history with timestamps
- 📍 **Location API**: REST API to query latest location
- 🚨 **Alarm Trigger**: API endpoint to make your phone ring (Find My feature)
- 🔋 **Battery Monitoring**: Track battery level along with location
- 📱 **Single File**: Everything in one file (`app.py`)
- 🐳 **Docker Support**: Easy deployment with Docker Compose

## Prerequisites

1. **For Direct Run**: Python 3.10-3.13 + Poetry
2. **For Docker Run**: Docker + Docker Compose
3. MongoDB database (local or MongoDB Atlas)
4. iCloud account with 2FA already authenticated (run setup first)

## Setup

### Option A: Docker (Recommended for 24/7 operation)

#### 1. Configure Environment Variables

Copy `.env.example` to `.env` in the root directory:

```bash
cd ..  # Go to root directory
cp .env.example .env
```

**Generate a secure API key:**
```bash
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Edit `.env`:
```
MONGODB_URI=mongodb+srv://your-connection-string
API_KEY=your_generated_secure_api_key_here  # REQUIRED!
TRACKING_INTERVAL=300  # 5 minutes
PORT=5000
```

⚠️ **Important:** The API_KEY protects your endpoints from unauthorized access. Without it, anyone can trigger your alarm!

#### 2. Authenticate with iCloud

Run the setup script (requires Poetry temporarily):

```bash
poetry install  # One-time setup
poetry run python setup/icloud_auth.py
```

This creates `icloud_session.pkl` that Docker will use.

#### 3. Start with Docker

```bash
cd track_location

# Start the container (builds automatically)
./docker-start.sh

# View logs
./docker-logs.sh

# Stop the container
./docker-stop.sh

# Restart the container
./docker-restart.sh
```

**Direct Docker Commands:**

```bash
# Start
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

The Docker container will:
- ✅ Run continuously in the background
- ✅ Restart automatically if it crashes
- ✅ Track locations at specified interval
- ✅ Expose API on port 5000

---

### Option B: Direct Python Run

#### 1. Install Dependencies

```bash
cd ..  # Go to root directory
poetry install
```

#### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` as shown above.

#### 3. Authenticate with iCloud

```bash
poetry run python setup/icloud_auth.py
```

#### 4. Run the Application

```bash
cd track_location
./start.sh
```

Or from root directory:

```bash
poetry run python track_location/app.py
```

## API Endpoints

### Health Check
```bash
GET /
```

Returns server status and tracking information. **No authentication required.**

**Response:**
```json
{
  "status": "running",
  "service": "iPhone Location Tracker",
  "tracking_active": true,
  "device": "Herman's iPhone"
}
```

### Get Latest Location
```bash
GET /location
```

Returns the most recent location data from MongoDB. **Requires API key.**

**Authentication:** Provide API key via header or query parameter

**Response:**
```json
{
  "device_id": "...",
  "name": "Herman's Huawei P90",
  "model": "iPhone 16 Pro",
  "battery_level": 0.21,
  "timestamp": "2025-11-04T12:00:00",
  "location_data": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 10,
    "position_type": "GPS"
  }
}
```

### Get Device Status
```bash
GET /status
```

Returns current device status (battery, etc.). **Requires API key.**

**Response:**
```json
{
  "device_id": "...",
  "name": "Herman's Huawei P90",
  "model": "iPhone 16 Pro",
  "battery_level": 0.21,
  "device_status": "200",
  "location_enabled": true,
  "timestamp": "2025-11-04T12:00:00"
}
```

### Trigger Alarm
```bash
POST /alarm
```

Makes your iPhone play a sound (Find My feature). **Requires API key.**

**Response:**
```json
{
  "status": "success",
  "message": "Alarm triggered on Herman's iPhone",
  "timestamp": "2025-11-04T12:00:00"
}
```

---

## 🔐 Authentication

All sensitive endpoints (`/location`, `/status`, `/alarm`) require API key authentication.

### Method 1: Using Header (Recommended)
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:5000/location
```

### Method 2: Using Query Parameter
```bash
curl "http://localhost:5000/location?api_key=your_api_key_here"
```

### Error Responses

**Missing API Key (401):**
```json
{
  "error": "Missing API key",
  "message": "Provide API key via X-API-Key header or ?api_key= parameter"
}
```

**Invalid API Key (403):**
```json
{
  "error": "Invalid API key",
  "message": "The provided API key is incorrect"
}
```

---

## Usage Examples

### Using cURL

```bash
# Check if server is running (no auth needed)
curl http://localhost:5000/

# Get latest location (with API key in header)
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/location

# Get latest location (with API key in query)
curl "http://localhost:5000/location?api_key=YOUR_API_KEY"

# Get device status (with API key)
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/status

# Trigger alarm (with API key)
curl -X POST -H "X-API-Key: YOUR_API_KEY" http://localhost:5000/alarm
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:5000"
API_KEY = "your_api_key_here"
HEADERS = {"X-API-Key": API_KEY}

# Get latest location
response = requests.get(f"{BASE_URL}/location", headers=HEADERS)
location = response.json()
print(f"Lat: {location['location_data']['latitude']}")
print(f"Lon: {location['location_data']['longitude']}")

# Trigger alarm
response = requests.post(f"{BASE_URL}/alarm", headers=HEADERS)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const API_KEY = 'your_api_key_here';
const headers = { 'X-API-Key': API_KEY };

// Get latest location
fetch('http://localhost:5000/location', { headers })
  .then(res => res.json())
  .then(data => console.log(data));

// Trigger alarm
fetch('http://localhost:5000/alarm', {
  method: 'POST',
  headers
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## How It Works

1. **Initialization**:
   - Connects to MongoDB
   - Loads iCloud session from `icloud_session.pkl`
   - Finds your iPhone 16 Pro device

2. **Background Tracking**:
   - Starts a background thread that runs continuously
   - Every 5 minutes (configurable), it fetches device location
   - Saves location, battery level, and timestamp to MongoDB

3. **API Server**:
   - Flask server runs on port 5000
   - Provides REST API endpoints for location queries and alarm
   - Runs concurrently with the background tracking thread

## MongoDB Schema

Each location record stored in MongoDB has this structure:

```json
{
  "_id": "ObjectId(...)",
  "device_id": "unique-device-id",
  "name": "Herman's Huawei P90",
  "model": "iPhone 16 Pro",
  "device_class": "iPhone",
  "battery_level": 0.21,
  "battery_status": null,
  "timestamp": "2025-11-04T12:00:00",
  "location": {
    "type": "Point",
    "coordinates": [-122.4194, 37.7749]
  },
  "location_data": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 10,
    "position_type": "GPS",
    "is_old": false,
    "location_timestamp": 1699123200000
  }
}
```

## Deployment

### Running as a Service (systemd)

Create `/etc/systemd/system/iphone-tracker.service`:

```ini
[Unit]
Description=iPhone Location Tracker API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/findmy
Environment="PATH=/path/to/.local/bin:/usr/bin"
ExecStart=/path/to/.local/bin/poetry run python track_location/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable iphone-tracker
sudo systemctl start iphone-tracker
```

### Docker

The app can be containerized. Make sure to mount your session files.

## Troubleshooting

### Session Expired
If you get "Session expired", re-authenticate:
```bash
poetry run python setup/icloud_auth.py
```

### Device Not Found
Make sure your device model name is exactly "iPhone 16 Pro" in iCloud. Check with:
```bash
poetry run python list_devices/track_devices.py
```

### MongoDB Connection Issues
Verify your `MONGODB_URI` is correct and your IP is whitelisted in MongoDB Atlas.

## Security Notes

- Keep your `.env` file secure (it contains MongoDB credentials)
- Keep `icloud_session.pkl` secure (it contains iCloud session)
- Consider using HTTPS if exposing the API publicly
- Add authentication/API keys for production use
- The `.gitignore` already excludes sensitive files

## License

See main project LICENSE file.
