# Token 鉴权实施计划

## 背景

Web Demo 启动后，输入 userId 会闪退回登录界面，原因是缺少有效的 Token。

火山 RTC 使用 Token 鉴权机制，需要服务端生成 Token 供客户端使用。

## 阶段目标

实现 Token 生成工具，支持 Web Demo 正常运行。

---

## 子任务清单

### [ ] Task 1: 创建 Token 生成 Python 工具

**目标**: 创建 Python 版 Token 生成器

**实施方案**:
1. 创建 `web/tools/token/token_generator.py`
2. 实现 HMAC-SHA256 签名算法
3. 支持命令行和配置文件方式
4. 添加单元测试

**验收标准**:
- [ ] Python 脚本可独立运行
- [ ] 生成的 Token 格式正确
- [ ] 可用于 Web Demo joinRoom

**文件改动**:
- `web/tools/token/token_generator.py` (新增)
- `web/tools/token/requirements.txt` (新增)

---

### [ ] Task 2: 创建 Token 生成 C++ 工具

**目标**: 创建 C++ 版 Token 生成器（可选）

**实施方案**:
1. 创建 `web/tools/token/token_generator.cpp`
2. 使用 OpenSSL 进行 HMAC-SHA256
3. 保持与 Python 版本一致

**验收标准**:
- [ ] C++ 脚本可编译运行
- [ ] 生成的 Token 与 Python 版本一致

**文件改动**:
- `web/tools/token/token_generator.cpp` (新增)

---

### [ ] Task 3: 修改 Web Demo 支持 Token

**目标**: 在 Web Demo 中集成 Token 动态获取

**实施方案**:
1. 创建 Token 获取接口（可选本地服务）
2. 或配置静态 Token
3. 验证 joinRoom 功能

**验收标准**:
- [ ] Web Demo 可正常加入房间
- [ ] 音视频功能正常

**文件改动**:
- `src/web/volc_web_sdk/src/config.ts` (修改)

---

### [ ] Task 4: 完善 Token 更新机制

**目标**: 实现 updateToken 功能

**实施方案**:
1. 在 Web Demo 中添加 Token 更新逻辑
2. 设置 Token 快过期时的自动更新

**验收标准**:
- [ ] Token 快过期时自动更新
- [ ] 不中断通话

---

## 命令清单

```bash
# Python Token 生成
cd web/tools/token
pip install -r requirements.txt
python token_generator.py --app-id <app_id> --app-key <app_key> --room-id test --user-id user1

# C++ 编译
cd web/tools/token
g++ -o token_generator token_generator.cpp -lssl -lcrypto
./token_generator --app-id <app_id> --app-key <app_key> --room-id test --user-id user1
```

---

## Token 生成算法

```python
import hmac
import hashlib
import base64
import time

def generate_token(app_id: str, app_key: str, room_id: str, user_id: str, expire: int = 3600) -> str:
    expire_time = int(time.time()) + expire
    message = f"{app_id}_{room_id}_{user_id}_{expire_time}"
    signature = hmac.new(app_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    token_content = f"{signature}:{message}"
    return base64.b64encode(token_content.encode()).decode()
```

---

## 执行记录

| 日期 | 完成任务 | 状态 |
|------|----------|------|
| 2026-04-22 | Task 1: 创建 Token 生成工具 | ⏳ |
| 2026-04-22 | Task 2: 创建 C++ Token 工具 | ⏳ |
| 2026-04-22 | Task 3: 修改 Web Demo 支持 Token | ⏳ |
| 2026-04-22 | Task 4: 完善 Token 更新机制 | ⏳ |
