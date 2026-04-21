# Web 开发脚本

## 目录说明

```
scripts/web/
├── cli.sh           # 交互式 CLI 入口（推荐使用）
├── update_config.sh # 更新 Web SDK 配置（生成 Token）
├── start.sh         # 启动开发服务器
├── stop.sh          # 停止 Web 服务
├── kill.sh          # 强制清理后台进程
└── README.md        # 本文件
```

## 快速开始

### 交互式 CLI（推荐）

```bash
bash scripts/web/cli.sh
```

菜单选项：
1. 更新配置 - 生成 Token 并更新 SDK
2. 启动服务 - 启动 Web 开发服务器
3. 安装依赖 - 安装 npm/pnpm 依赖
4. 构建项目 - 构建生产版本
5. 停止服务 - 优雅停止 Web 服务
6. 清理进程 - 强制清理后台 node 进程
0. 退出

## 单独使用脚本

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

### 3. 启动开发服务器

```bash
bash scripts/web/start.sh
```

### 4. 停止服务

```bash
bash scripts/web/stop.sh
```

### 5. 清理进程

如果服务无法正常停止，强制清理：

```bash
bash scripts/web/kill.sh
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
- 服务运行在端口 5000
