# 火山 RTC Token 鉴权调研

## 调研信息
- 调研时间：2026-04-22
- 信息来源：
  - https://www.volcengine.com/docs/6348/70121
  - https://www.volcengine.com/docs/6348/104478

## 核心发现

### 1. Token 生成原理

火山 RTC 使用 HMAC-SHA256 签名算法生成 Token。

#### Token 结构
```
Token = Base64(HMAC-SHA256 签名 + ":" + 消息体)
```

#### 消息体格式
```
{appId}_{roomId}_{userId}_{expireTime}
```

#### 示例
```
appId = 123456
roomId = demo_room
userId = user_001
expireTime = 1776785857 (Unix 时间戳)

消息体 = "123456_demo_room_user_001_1776785857"
签名 = HMAC-SHA256(消息体, appKey)
Token = Base64(签名 + ":" + 消息体)
```

### 2. joinRoom 接口

```typescript
// Web SDK 示例
const token = await generateToken(appId, appKey, roomId, userId);

await rtcEngine.joinRoom(token, {
  roomId: roomId,
  userId: userId,
});
```

#### 参数说明
| 参数 | 类型 | 说明 |
|------|------|------|
| token | string | 动态签名的 Token |
| roomId | string | 房间 ID |
| userId | string | 用户 ID |

### 3. updateToken 接口

Token 快过期时（建议提前 5 分钟），调用 updateToken 更新：

```typescript
// Web SDK 示例
const newToken = await generateToken(appId, appKey, roomId, userId, newExpireTime);
await rtcEngine.updateToken(newToken);
```

## 各平台 Token 生成方案对比

### 火山官方 SDK

| 平台 | SDK | 语言 | 说明 |
|------|-----|------|------|
| Web | @volcengine/rtc | TypeScript | 内置 Token 生成 |
| Android | veRTC SDK | Java/Kotlin | 内置 Token 生成 |
| iOS | veRTC SDK | Swift/Objective-C | 内置 Token 生成 |
| Windows | veRTC SDK | C++ | 内置 Token 生成 |
| macOS | veRTC SDK | C++/Objective-C | 内置 Token 生成 |
| Linux | veRTC SDK | C++ | 内置 Token 生成 |

### 服务端生成方案

| 语言 | 库 | 说明 | 推荐度 |
|------|-----|------|--------|
| Go | volc/rtc (官方) | 官方推荐，功能完整 | ⭐⭐⭐⭐ |
| Python | volc/rtc (官方) | 官方 SDK，适合 Python 后端 | ⭐⭐⭐⭐ |
| Java | volc/rtc (官方) | 官方 SDK，适合 Java 后端 | ⭐⭐⭐⭐ |
| PHP | volc/rtc (官方) | 官方 SDK | ⭐⭐⭐ |
| C++ | volc/rtc (官方) | C++ 后端服务 | ⭐⭐⭐⭐ |
| Node.js | volc/rtc (官方) | 适合 JS/TS 后端 | ⭐⭐⭐⭐ |

### 纯算法实现

对于不依赖 SDK 的场景，可以直接实现 Token 生成算法：

```python
import hmac
import hashlib
import base64
import time

def generate_token(app_id: str, app_key: str, room_id: str, user_id: str, expire: int = 3600) -> str:
    """
    生成火山 RTC Token

    Args:
        app_id: 应用 ID
        app_key: 应用密钥
        room_id: 房间 ID
        user_id: 用户 ID
        expire: 有效期（秒），默认 1 小时

    Returns:
        Base64 编码的 Token
    """
    expire_time = int(time.time()) + expire
    message = f"{app_id}_{room_id}_{user_id}_{expire_time}"

    signature = hmac.new(
        app_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    token_content = f"{signature}:{message}"
    token = base64.b64encode(token_content.encode('utf-8')).decode('utf-8')

    return token
```

## 推荐方案

### 最佳实践：服务端集中生成

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   客户端    │────▶│   服务端        │────▶│  火山 RTC    │
│  (Web/App)  │     │  (Python/C++)   │     │   服务器     │
└─────────────┘     │  生成 Token     │     └──────────────┘
                    └─────────────────┘
```

**优势**：
- AppKey 不暴露在客户端
- 统一管理 Token 生命周期
- 支持 Token 轮换和撤销

### 语言选择

| 场景 | 推荐语言 | 原因 |
|------|----------|------|
| Web 后端 | Python/Go | 快速开发，官方 SDK 支持 |
| 高性能服务 | C++ | 底层实现，性能最优 |
| 微服务 | Go | 并发支持好，部署简单 |
| 现有系统 | Python | 集成方便 |

## 待确认

- [ ] AppKey 如何安全存储（环境变量/密钥管理服务）
- [ ] Token 有效期设置（建议 1-4 小时）
- [ ] Token 续期策略（前端主动续期 vs 后端推送）

## 相关链接

- [火山 RTC Token 鉴权](https://www.volcengine.com/docs/6348/70121)
- [joinRoom 接口](https://www.volcengine.com/docs/6348/104478#rtcengine-joinroom)
- [updateToken 接口](https://www.volcengine.com/docs/6348/104478#updatetoken)
