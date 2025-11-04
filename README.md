# Apple Device Tracker | Apple 设备追踪器

[English](#english) | [中文](#中文)

---

## English

Track your Apple devices (iPhone, iPad, Mac, Apple Watch, AirPods) using Python - **no Mac required**!

### 🌟 Features

- ✅ Track all Apple devices without needing a Mac
- ✅ View device locations, battery levels, and status
- ✅ Export device data to JSON
- ✅ Play sound on devices remotely
- ✅ Simple authentication with 2FA support
- ✅ Works on Windows, Linux, and Mac

### 📁 Project Structure

```
findmy/
├── setup/                    # Authentication scripts
│   ├── icloud_auth.py        # ✅ Recommended: pyicloud auth
│   ├── findmy_auth.py        # Advanced: FindMy.py auth
│   └── README.md             # Setup instructions
│
├── list_devices/             # Device tracking scripts
│   ├── icloud_track.py       # ✅ Recommended: pyicloud tracker
│   ├── track_devices.py      # Advanced: FindMy.py tracker
│   └── README.md             # Usage instructions
│
├── track_location/           # 🆕 Location tracking with MongoDB
│   ├── track_to_mongodb.py   # Continuous location tracking
│   └── README.md             # Tracking instructions
│
├── .env                      # Environment variables (MongoDB URI)
├── pyproject.toml            # Dependencies
├── .gitignore                # Protected files
└── README.md                 # This file
```

### 🚀 Quick Start

#### 1. Install Dependencies

```bash
poetry install
```

#### 2. Authenticate (First Time)

```bash
poetry run python setup/icloud_auth.py
```

- Enter your Apple ID and password
- Complete 2FA authentication
- Session saved to `icloud_session.pkl`

#### 3. List Your Devices

```bash
poetry run python list_devices/icloud_track.py
```

You'll see:
- All your devices with names and models
- Current locations (if available)
- Battery levels and status
- Interactive options to export data or play sounds

#### 4. Track Location History to MongoDB (Optional)

Set up continuous location tracking:

1. Create `.env` file with MongoDB URI:
```bash
MONGODB_URI=your_mongodb_connection_string
```

2. Run the tracking script:
```bash
poetry run python track_location/track_to_mongodb.py
```

Choose from:
- Single update
- Continuous tracking (5 min intervals)
- Custom interval tracking

### 📊 What You Can Track

| Device Type | pyicloud (Recommended) | FindMy.py (Advanced) |
|-------------|------------------------|----------------------|
| iPhone/iPad/Mac | ✅ Works on any OS | ❌ Requires Mac for keys |
| Apple Watch | ✅ Works on any OS | ❌ Requires Mac for keys |
| AirPods | ✅ If Find My enabled | ❌ Requires Mac for keys |
| AirTags | ❌ Not supported | ✅ With Mac for keys |
| Friends' locations | ✅ If shared with you | ✅ With Mac for keys |

**Recommendation:** Use **pyicloud** (default) for tracking regular Apple devices. Only use FindMy.py if you need AirTag tracking and have access to a Mac.

### 🔒 Security

Protected files (automatically in `.gitignore`):
- `icloud_session.pkl` - Your authentication session
- `icloud_devices.json` - Exported device data
- `account.json` - FindMy.py session (if used)
- `ani_libs.bin` - Anisette libraries

**Never share or commit these files!**

### 📝 Example Output

```
Device #1
--------------------------------------------------------------------------------
Name: Herman's iPhone 16 Pro
Model: iPhone 16 Pro
Battery: 21%
Location: [latitude, longitude]
Status: Online
```

### 🛠️ Advanced Usage

#### Play Sound on Device (Python)

```python
from pyicloud import PyiCloudService
api = PyiCloudService('your@email.com', 'password')
device = api.devices[0]
device.play_sound()
```

#### Export Device Data

```bash
poetry run python list_devices/icloud_track.py
# Select option 1 to export to JSON
```

### 🔧 Troubleshooting

**"Session expired"**
```bash
poetry run python setup/icloud_auth.py
```

**"No devices found"**
- Ensure Find My iPhone is enabled on devices
- Check devices are signed into your Apple ID
- Verify location services are enabled

**2FA Issues**
- Enter code exactly as received
- Codes expire after a few minutes
- Wait and request a new code if needed

### 📚 Resources

- [pyicloud GitHub](https://github.com/picklepete/pyicloud)
- [FindMy.py GitHub](https://github.com/malmeloo/FindMy.py)
- [Find My Settings](https://www.icloud.com/find)

---

## 中文

使用 Python 追踪您的 Apple 设备（iPhone、iPad、Mac、Apple Watch、AirPods）- **无需 Mac！**

### 🌟 功能特点

- ✅ 无需 Mac 即可追踪所有 Apple 设备
- ✅ 查看设备位置、电量和状态
- ✅ 将设备数据导出为 JSON
- ✅ 远程在设备上播放声音
- ✅ 支持双因素认证的简单登录
- ✅ 支持 Windows、Linux 和 Mac

### 📁 项目结构

```
findmy/
├── setup/                    # 认证脚本
│   ├── icloud_auth.py        # ✅ 推荐：pyicloud 认证
│   ├── findmy_auth.py        # 高级：FindMy.py 认证
│   └── README.md             # 设置说明
│
├── list_devices/             # 设备追踪脚本
│   ├── icloud_track.py       # ✅ 推荐：pyicloud 追踪器
│   ├── track_devices.py      # 高级：FindMy.py 追踪器
│   └── README.md             # 使用说明
│
├── track_location/           # 🆕 MongoDB 位置追踪
│   ├── track_to_mongodb.py   # 连续位置追踪
│   └── README.md             # 追踪说明
│
├── .env                      # 环境变量（MongoDB URI）
├── pyproject.toml            # 依赖项
├── .gitignore                # 受保护的文件
└── README.md                 # 本文件
```

### 🚀 快速开始

#### 1. 安装依赖

```bash
poetry install
```

#### 2. 首次认证

```bash
poetry run python setup/icloud_auth.py
```

- 输入您的 Apple ID 和密码
- 完成双因素认证（2FA）
- 会话保存到 `icloud_session.pkl`

#### 3. 列出您的设备

```bash
poetry run python list_devices/icloud_track.py
```

您将看到：
- 所有设备的名称和型号
- 当前位置（如果可用）
- 电量和状态
- 导出数据或播放声音的交互选项

#### 4. 追踪位置历史到 MongoDB（可选）

设置连续位置追踪：

1. 创建包含 MongoDB URI 的 `.env` 文件：
```bash
MONGODB_URI=your_mongodb_connection_string
```

2. 运行追踪脚本：
```bash
poetry run python track_location/track_to_mongodb.py
```

可选择：
- 单次更新
- 连续追踪（5分钟间隔）
- 自定义间隔追踪

### 📊 可追踪的设备类型

| 设备类型 | pyicloud（推荐） | FindMy.py（高级） |
|---------|-----------------|------------------|
| iPhone/iPad/Mac | ✅ 适用于任何操作系统 | ❌ 需要 Mac 提取密钥 |
| Apple Watch | ✅ 适用于任何操作系统 | ❌ 需要 Mac 提取密钥 |
| AirPods | ✅ 如果启用了"查找" | ❌ 需要 Mac 提取密钥 |
| AirTags | ❌ 不支持 | ✅ 需要 Mac 提取密钥 |
| 朋友位置 | ✅ 如果与您共享 | ✅ 需要 Mac 提取密钥 |

**建议：** 使用 **pyicloud**（默认）追踪常规 Apple 设备。仅当需要追踪 AirTag 且有 Mac 访问权限时使用 FindMy.py。

### 🔒 安全性

受保护的文件（自动在 `.gitignore` 中）：
- `icloud_session.pkl` - 您的认证会话
- `icloud_devices.json` - 导出的设备数据
- `account.json` - FindMy.py 会话（如果使用）
- `ani_libs.bin` - Anisette 库

**切勿分享或提交这些文件！**

### 📝 示例输出

```
设备 #1
--------------------------------------------------------------------------------
名称：Herman 的 iPhone 16 Pro
型号：iPhone 16 Pro
电量：21%
位置：[纬度, 经度]
状态：在线
```

### 🛠️ 高级用法

#### 在设备上播放声音（Python）

```python
from pyicloud import PyiCloudService
api = PyiCloudService('your@email.com', 'password')
device = api.devices[0]
device.play_sound()
```

#### 导出设备数据

```bash
poetry run python list_devices/icloud_track.py
# 选择选项 1 导出到 JSON
```

### 🔧 故障排除

**"会话已过期"**
```bash
poetry run python setup/icloud_auth.py
```

**"未找到设备"**
- 确保设备上启用了"查找我的 iPhone"
- 检查设备已登录您的 Apple ID
- 验证已启用定位服务

**双因素认证问题**
- 准确输入收到的验证码
- 验证码几分钟后过期
- 如需要，等待并请求新验证码

### 📚 资源

- [pyicloud GitHub](https://github.com/picklepete/pyicloud)
- [FindMy.py GitHub](https://github.com/malmeloo/FindMy.py)
- [查找设置](https://www.icloud.com/find)

---

## Requirements | 系统要求

- Python 3.10-3.13
- Poetry package manager
- Active Apple ID with devices | 有设备的活跃 Apple ID

## License | 许可证

This project uses pyicloud and FindMy.py libraries. Please refer to their respective licenses.

本项目使用 pyicloud 和 FindMy.py 库。请参考它们各自的许可证。
