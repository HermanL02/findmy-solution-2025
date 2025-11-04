# Setup / Authentication | 设置 / 认证

## English

This folder contains authentication scripts for both FindMy.py and pyicloud.

### Files:
- **icloud_auth.py** - ✅ Recommended: Simple authentication using pyicloud (works on any OS)
- **findmy_auth.py** - Advanced: FindMy.py authentication (requires Mac for device keys)

### Quick Start:

**Use pyicloud (Recommended):**
```bash
poetry run python setup/icloud_auth.py
```

This will:
1. Prompt for your Apple ID and password
2. Handle 2FA authentication
3. Save session to `icloud_session.pkl` in the root directory

---

## 中文

此文件夹包含 FindMy.py 和 pyicloud 的认证脚本。

### 文件说明：
- **icloud_auth.py** - ✅ 推荐：使用 pyicloud 进行简单认证（适用于任何操作系统）
- **findmy_auth.py** - 高级选项：FindMy.py 认证（需要 Mac 来提取设备密钥）

### 快速开始：

**使用 pyicloud（推荐）：**
```bash
poetry run python setup/icloud_auth.py
```

这将会：
1. 提示输入您的 Apple ID 和密码
2. 处理双因素认证（2FA）
3. 将会话保存到根目录的 `icloud_session.pkl`
