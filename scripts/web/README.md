# Web 开发脚本

## 目录说明

```
scripts/web/
├── update_config.sh  # 更新 Web SDK 配置（生成 Token）
├── start.sh         # 启动开发服务器
└── README.md        # 本文件
```

## 使用流程

### 1. 配置 Token

从模板复制配置文件：

```bash
cp config/token.conf.example config/token.conf
```

编辑 `config/token.conf`，填写你的火山引擎配置：

```ini
[volc]
app_id = "你的AppId"
app_key = "你的AppKey"
room_id = "test_room"

[users]
user_ids = ["user_001", "user_002"]

[options]
expire = 604800  # 7 天（最大支持 30 天 = 2592000 秒）
```

### 2. 生成 Token 并更新配置

```bash
bash scripts/web/update_config.sh
```

脚本会自动：
- 读取 `config/token.conf`
- 调用 Python 工具生成 Token
- 更新 `src/web/volc_web_sdk/src/config.ts`

### 3. 启动开发服务器

```bash
bash scripts/web/start.sh
```

或者手动启动：

```bash
cd src/web/volc_web_sdk
pnpm start
```

## Token 有效期

| 值 | 说明 |
|-----|------|
| 3600 | 1 小时（测试用） |
| 86400 | 1 天 |
| 604800 | 7 天（推荐） |
| 2592000 | 30 天（最大支持值） |

## 注意事项

- `config/token.conf` 包含敏感信息，**不要提交到 Git**
- `.gitignore` 已配置忽略此文件
- Token 过期后需要重新生成
