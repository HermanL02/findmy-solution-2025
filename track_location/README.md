# Track Location to MongoDB | 追踪位置到 MongoDB

[English](#english) | [中文](#中文)

---

## English

Continuously track your Apple device locations and store them in MongoDB for historical analysis.

### Features

- ✅ Automatic location tracking at configurable intervals
- ✅ Store location history in MongoDB
- ✅ Track multiple devices simultaneously
- ✅ GeoJSON format for easy mapping
- ✅ Battery level monitoring
- ✅ Single update or continuous tracking modes

### Setup

#### 1. Configure MongoDB URI

Create or edit `.env` file in the root directory:

```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=YourApp
```

#### 2. Ensure iCloud Authentication

Make sure you've authenticated first:

```bash
poetry run python setup/icloud_auth.py
```

### Usage

#### Option 1: Docker (Recommended for 24/7 tracking)

**Quick Start:**

```bash
cd track_location

# Start the tracker (runs infinitely in background)
./start.sh

# View logs
./logs.sh

# Stop the tracker
./stop.sh

# Restart the tracker
./restart.sh
```

**Docker Commands:**

```bash
# Start with custom interval (in seconds)
TRACKING_INTERVAL=600 docker-compose up -d  # 10 minutes

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

The Docker container will:
- ✅ Run continuously in the background
- ✅ Restart automatically if it crashes
- ✅ Track locations at your specified interval (default: 5 minutes)
- ✅ Store all data in MongoDB

#### Option 2: Direct Python (For testing or one-time runs)

Run the tracking script:

```bash
poetry run python track_location/track_to_mongodb.py
```

You'll see three tracking modes:

1. **Track once and exit** - Single location update
2. **Continuous tracking (5 minutes)** - Updates every 5 minutes
3. **Custom interval** - Specify your own interval in seconds

### Data Structure

Each location record in MongoDB contains:

```json
{
  "device_id": "unique_device_id",
  "name": "Herman's iPhone 16 Pro",
  "model": "iPhone 16 Pro",
  "device_class": "iPhone",
  "battery_level": 0.21,
  "battery_status": "Charging",
  "location": {
    "type": "Point",
    "coordinates": [longitude, latitude]
  },
  "location_data": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 65,
    "position_type": "GPS",
    "is_old": false,
    "location_timestamp": 1699000000000
  },
  "timestamp": "2024-11-03T12:00:00.000Z"
}
```

### MongoDB Database Structure

- **Database**: `findmy`
- **Collection**: `device_locations`

### Querying Location History

Example MongoDB queries:

```javascript
// Get all locations for a specific device
db.device_locations.find({ "name": "Herman's iPhone 16 Pro" })

// Get locations within last 24 hours
db.device_locations.find({
  "timestamp": {
    $gte: ISODate("2024-11-02T00:00:00Z")
  }
})

// Get locations near a specific point (requires geo index)
db.device_locations.createIndex({ "location": "2dsphere" })
db.device_locations.find({
  "location": {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-122.4194, 37.7749]
      },
      $maxDistance: 1000  // meters
    }
  }
})
```

### Stopping Continuous Tracking

Press `Ctrl+C` to stop the tracking loop.

---

## 中文

持续追踪您的 Apple 设备位置并将其存储到 MongoDB 以进行历史分析。

### 功能特点

- ✅ 可配置间隔的自动位置追踪
- ✅ 在 MongoDB 中存储位置历史
- ✅ 同时追踪多个设备
- ✅ GeoJSON 格式便于地图展示
- ✅ 电量监控
- ✅ 单次更新或连续追踪模式

### 设置

#### 1. 配置 MongoDB URI

在根目录创建或编辑 `.env` 文件：

```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=YourApp
```

#### 2. 确保 iCloud 已认证

确保您已先完成认证：

```bash
poetry run python setup/icloud_auth.py
```

### 使用方法

#### 方式 1：Docker（推荐用于 24/7 追踪）

**快速开始：**

```bash
cd track_location

# 启动追踪器（在后台无限运行）
./start.sh

# 查看日志
./logs.sh

# 停止追踪器
./stop.sh

# 重启追踪器
./restart.sh
```

**Docker 命令：**

```bash
# 使用自定义间隔启动（秒）
TRACKING_INTERVAL=600 docker-compose up -d  # 10分钟

# 查看日志
docker-compose logs -f

# 停止
docker-compose down

# 重新构建并启动
docker-compose up --build -d
```

Docker 容器将：
- ✅ 在后台持续运行
- ✅ 崩溃时自动重启
- ✅ 按指定间隔追踪位置（默认：5分钟）
- ✅ 将所有数据存储在 MongoDB

#### 方式 2：直接运行 Python（用于测试或一次性运行）

运行追踪脚本：

```bash
poetry run python track_location/track_to_mongodb.py
```

您将看到三种追踪模式：

1. **追踪一次并退出** - 单次位置更新
2. **连续追踪（5分钟）** - 每5分钟更新一次
3. **自定义间隔** - 指定您自己的间隔时间（秒）

### 数据结构

MongoDB 中的每条位置记录包含：

```json
{
  "device_id": "unique_device_id",
  "name": "Herman 的 iPhone 16 Pro",
  "model": "iPhone 16 Pro",
  "device_class": "iPhone",
  "battery_level": 0.21,
  "battery_status": "充电中",
  "location": {
    "type": "Point",
    "coordinates": [经度, 纬度]
  },
  "location_data": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 65,
    "position_type": "GPS",
    "is_old": false,
    "location_timestamp": 1699000000000
  },
  "timestamp": "2024-11-03T12:00:00.000Z"
}
```

### MongoDB 数据库结构

- **数据库**: `findmy`
- **集合**: `device_locations`

### 查询位置历史

MongoDB 查询示例：

```javascript
// 获取特定设备的所有位置
db.device_locations.find({ "name": "Herman 的 iPhone 16 Pro" })

// 获取最近24小时内的位置
db.device_locations.find({
  "timestamp": {
    $gte: ISODate("2024-11-02T00:00:00Z")
  }
})

// 获取特定点附近的位置（需要创建地理索引）
db.device_locations.createIndex({ "location": "2dsphere" })
db.device_locations.find({
  "location": {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-122.4194, 37.7749]
      },
      $maxDistance: 1000  // 米
    }
  }
})
```

### 停止连续追踪

按 `Ctrl+C` 停止追踪循环。

---

## Use Cases | 使用场景

### English
- **Travel tracking** - Record your device movements during trips
- **Device monitoring** - Keep track of family member devices
- **Lost device recovery** - Historical location data for finding lost devices
- **Location analytics** - Analyze patterns in device movement

### 中文
- **旅行追踪** - 记录旅行期间的设备移动
- **设备监控** - 追踪家庭成员的设备
- **丢失设备恢复** - 历史位置数据帮助找回丢失的设备
- **位置分析** - 分析设备移动模式

## Requirements | 要求

- Authenticated iCloud session | 已认证的 iCloud 会话
- MongoDB connection (Atlas or local) | MongoDB 连接（Atlas 或本地）
- `.env` file with MONGODB_URI | 包含 MONGODB_URI 的 .env 文件
