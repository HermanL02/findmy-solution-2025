# List Devices | 列出设备

## English

This folder contains scripts to list and track your Apple devices.

### Files:
- **icloud_track.py** - ✅ Recommended: Track devices using pyicloud (works on any OS)
- **track_devices.py** - Advanced: Track devices using FindMy.py (requires decryption keys from Mac)

### Quick Start:

**Using pyicloud (Recommended):**
```bash
poetry run python list_devices/icloud_track.py
```

This will:
1. Load your saved authentication session
2. Fetch all your devices
3. Display device information (name, model, location, battery)
4. Offer options to:
   - Export data to JSON
   - Play sound on a device
   - Exit

### What You'll See:
- Device names and models
- Current location (if available)
- Battery levels
- Device status
- Lost mode capability

---

## 中文

此文件夹包含列出和跟踪您的 Apple 设备的脚本。

### 文件说明：
- **icloud_track.py** - ✅ 推荐：使用 pyicloud 跟踪设备（适用于任何操作系统）
- **track_devices.py** - 高级选项：使用 FindMy.py 跟踪设备（需要从 Mac 提取解密密钥）

### 快速开始：

**使用 pyicloud（推荐）：**
```bash
poetry run python list_devices/icloud_track.py
```

这将会：
1. 加载您保存的认证会话
2. 获取所有设备
3. 显示设备信息（名称、型号、位置、电量）
4. 提供选项：
   - 导出数据到 JSON
   - 在设备上播放声音
   - 退出

### 您将看到：
- 设备名称和型号
- 当前位置（如果可用）
- 电量水平
- 设备状态
- 丢失模式功能
