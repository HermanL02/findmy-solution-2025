# Security Guidelines | 安全指南

[English](#english) | [中文](#中文)

---

## English

### 🔒 Protected Files - NEVER COMMIT THESE

The following files contain sensitive credentials and personal data. **Never commit or share these files:**

#### Critical Files:
- **`.env`** - Contains MongoDB credentials and API keys
- **`icloud_session.pkl`** - Your Apple ID session
- **`account.json`** - FindMy.py authentication data
- **`ani_libs.bin`** - Anisette libraries
- **`icloud_devices.json`** - Device location data

### ✅ What's Safe to Commit

- `.env.example` - Template file (no real credentials)
- `*.py` - Python scripts
- `*.md` - Documentation
- `pyproject.toml` - Dependencies
- `.gitignore` - Git ignore rules
- Docker files - Dockerfile, docker-compose.yml

### 🛡️ Best Practices

#### 1. Environment Variables

**DO:**
```bash
# Use .env file (already in .gitignore)
MONGODB_URI=your_actual_uri_here
```

**DON'T:**
```python
# Never hardcode credentials
mongodb_uri = "mongodb+srv://user:pass@cluster..."
```

#### 2. Git Repository

**Before committing, always check:**
```bash
# Check what files will be committed
git status

# Make sure .env is ignored
git check-ignore .env  # Should output: .env

# View what will be committed
git diff --cached
```

#### 3. Sharing Code

If sharing your code:
- ✅ Copy `.env.example` to `.env`
- ✅ Fill in your real credentials in `.env` (never commit)
- ✅ Push to private repository only
- ❌ Never push to public repositories with credentials

#### 4. Docker Security

```yaml
# In docker-compose.yml, use environment variables
environment:
  - MONGODB_URI=${MONGODB_URI}  # ✅ Reference from .env

# Not like this:
environment:
  - MONGODB_URI=mongodb+srv://user:pass@...  # ❌ Hardcoded
```

### 🚨 If You Accidentally Commit Credentials

1. **Rotate credentials immediately:**
   - Change MongoDB password
   - Revoke Apple session
   - Update `.env` with new credentials

2. **Remove from Git history:**
```bash
# Remove file from all commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (warning: rewrites history)
git push origin --force --all
```

3. **Consider using tools:**
   - [git-secrets](https://github.com/awslabs/git-secrets)
   - [gitleaks](https://github.com/gitleaks/gitleaks)

### 📋 Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] No credentials hardcoded in scripts
- [ ] `icloud_session.pkl` is in `.gitignore`
- [ ] Repository is private (if on GitHub)
- [ ] `.env.example` has placeholder values only
- [ ] MongoDB uses strong password
- [ ] Regular security audits of dependencies

---

## 中文

### 🔒 受保护的文件 - 切勿提交这些文件

以下文件包含敏感凭据和个人数据。**切勿提交或分享这些文件：**

#### 关键文件：
- **`.env`** - 包含 MongoDB 凭据和 API 密钥
- **`icloud_session.pkl`** - 您的 Apple ID 会话
- **`account.json`** - FindMy.py 认证数据
- **`ani_libs.bin`** - Anisette 库
- **`icloud_devices.json`** - 设备位置数据

### ✅ 可以安全提交的内容

- `.env.example` - 模板文件（无真实凭据）
- `*.py` - Python 脚本
- `*.md` - 文档
- `pyproject.toml` - 依赖项
- `.gitignore` - Git 忽略规则
- Docker 文件 - Dockerfile, docker-compose.yml

### 🛡️ 最佳实践

#### 1. 环境变量

**正确做法：**
```bash
# 使用 .env 文件（已在 .gitignore 中）
MONGODB_URI=your_actual_uri_here
```

**错误做法：**
```python
# 切勿硬编码凭据
mongodb_uri = "mongodb+srv://user:pass@cluster..."
```

#### 2. Git 仓库

**提交前务必检查：**
```bash
# 检查将要提交的文件
git status

# 确保 .env 被忽略
git check-ignore .env  # 应该输出：.env

# 查看将要提交的内容
git diff --cached
```

#### 3. 分享代码

如果分享您的代码：
- ✅ 复制 `.env.example` 为 `.env`
- ✅ 在 `.env` 中填写真实凭据（切勿提交）
- ✅ 仅推送到私有仓库
- ❌ 切勿推送到包含凭据的公共仓库

#### 4. Docker 安全

```yaml
# 在 docker-compose.yml 中，使用环境变量
environment:
  - MONGODB_URI=${MONGODB_URI}  # ✅ 从 .env 引用

# 不要这样做：
environment:
  - MONGODB_URI=mongodb+srv://user:pass@...  # ❌ 硬编码
```

### 🚨 如果意外提交了凭据

1. **立即轮换凭据：**
   - 更改 MongoDB 密码
   - 撤销 Apple 会话
   - 使用新凭据更新 `.env`

2. **从 Git 历史中删除：**
```bash
# 从所有提交中删除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（警告：重写历史）
git push origin --force --all
```

3. **考虑使用工具：**
   - [git-secrets](https://github.com/awslabs/git-secrets)
   - [gitleaks](https://github.com/gitleaks/gitleaks)

### 📋 安全检查清单

- [ ] `.env` 文件在 `.gitignore` 中
- [ ] 脚本中无硬编码凭据
- [ ] `icloud_session.pkl` 在 `.gitignore` 中
- [ ] 仓库为私有（如在 GitHub 上）
- [ ] `.env.example` 仅包含占位符值
- [ ] MongoDB 使用强密码
- [ ] 定期审计依赖项的安全性

---

## Additional Resources | 其他资源

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [MongoDB Security Checklist](https://docs.mongodb.com/manual/administration/security-checklist/)
