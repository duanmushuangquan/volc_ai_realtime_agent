# Coze 云电脑同步配置

## 云电脑信息

| 配置项 | 值 |
|--------|-----|
| **公网 IP** | `115.190.107.107` |
| **SSH 用户** | `coze` |
| **SSH 端口** | `22` |
| **工作目录** | `/home/coze/projects` |

## SSH 连接测试

```bash
# 测试 SSH 连接（公钥添加后）
ssh -i .ssh/id_ed25519 coze@115.190.107.107 "hostname && pwd"
```

## Git + Webhook 工作流

```
┌─────────────────┐     git push      ┌─────────────┐
│   Coze 沙箱     │ ───────────────→ │   GitHub    │
│  (代码编写)     │                   │             │
└─────────────────┘                   └──────┬──────┘
                                             │
                                             │ webhook
                                             ↓
┌─────────────────┐     编译结果     ┌─────────────┐
│   云电脑         │ ←─────────────── │  Git 拉取   │
│  (C++ 编译)     │                   │  + 编译     │
└─────────────────┘                   └─────────────┘
```

## 同步命令

```bash
# 推送代码到云电脑
make sync-push

# 从云电脑拉取结果
make sync-pull

# 在云电脑上执行（首次需要）
cd /home/coze/projects/volc_ai_realtime_agent
mkdir -p build && cd build
cmake .. && make -j$(nproc)
```
