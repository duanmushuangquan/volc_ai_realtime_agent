# volc_ai_realtime_agent

基于火山引擎实时音视频（RTC）+ AI 音视频互动方案的机器人控制系统

## 项目概述

本项目旨在开发一个支持 AI 语音交互的机器人控制系统，具有以下特点：

- **实时音视频交互**：基于火山 veRTC SDK
- **多模态 AI 能力**：ASR + LLM + TTS 三段式 / S2S 端到端
- **云边协同**：支持云端和离线模式自动切换
- **仿真/真机切换**：基于 Robot Harness 架构
- **多协议通信**：DDS / HTTP / WebSocket

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                    用户交互层                        │
│         (Web UI / 手机 APP / 语音终端)               │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│                  AI 交互引擎层                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ ASR Bridge│ │ LLM Bridge│ │ TTS Bridge│ │ Memory │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │              Skills Executor                  │   │
│  │   DDS Skills / HTTP Skills / WS Skills       │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│                   Robot Harness                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │SafetyMonitor│ │     RAL     │ │ActionExecutor│   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 技术栈

| 模块 | 技术选型 |
|------|----------|
| 实时通信 | 火山 veRTC |
| ASR (在线) | 火山 ASR |
| ASR (离线) | FunASR |
| TTS (在线) | 火山 TTS |
| TTS (离线) | Coqui XTTS |
| LLM (在线) | 豆包 Pro |
| LLM (离线) | Qwen3-8B |
| DDS | Fast DDS |
| 仿真 | Isaac Sim |
| 硬件 | NVIDIA Orin AGX/NX |

## 目录结构

```
volc_ai_realtime_agent/
├── src/                    # 源代码
├── tests/                  # 测试
├── docs/
│   ├── research/           # 调研文档
│   └── plan/              # 实施计划
├── scripts/                # 辅助脚本
├── configs/                # 配置文件
├── Makefile
└── README.md
```

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-org/volc_ai_realtime_agent.git
cd volc_ai_realtime_agent
```

### 2. 初始化项目
```bash
make new-research TOPIC=volc_rtc  # 创建调研文档
make new-plan TOPIC=volc_rtc      # 创建计划文档
```

### 3. 查看计划进度
```bash
make show-plan TOPIC=volc_rtc
```

### 4. 开发流程
```bash
# 标记任务完成
make done TASK=1 TOPIC=volc_rtc

# 运行测试
make test

# 编译
make build

# 代码检查
make lint
```

## Makefile 命令

| 命令 | 功能 |
|------|------|
| `make new-research TOPIC=<topic>` | 创建调研文档 |
| `make new-plan TOPIC=<topic>` | 创建计划文档 |
| `make show-plan TOPIC=<topic>` | 显示计划进度 |
| `make done TASK=N TOPIC=<topic>` | 标记任务完成 |
| `make test` | 运行测试 |
| `make build` | 编译项目 |
| `make lint` | 代码检查 |
| `make sync-push` | 推送到云电脑 |
| `make sync-pull` | 从云电脑拉取 |
| `make download-sdk PRODUCT=<product>` | 下载 SDK |

## 开发指南

### 添加新调研
```bash
make new-research TOPIC=openclaw
# 编辑 docs/research/openclaw.md
```

### 添加新计划
```bash
make new-plan TOPIC=openclaw
# 编辑 docs/plan/openclaw_plan.md
```

### 子任务执行流程
1. 阅读计划，确认当前任务
2. 实现代码
3. 编写测试和示例
4. 运行 `make test` 验证
5. 报告结果，等待确认

## 参考文档

- [火山 RTC 文档](https://www.volcengine.com/docs/6348/)
- [AGENTS.md](./AGENTS.md) - 开发规范
- [火山 RTC 调研](./docs/research/volc_rtc.md)
- [火山 RTC 计划](./docs/plan/volc_rtc_plan.md)

## License

MIT

## 云电脑同步 (Git + Webhook)

### 前提条件

1. **SSH 公钥配置**：将 `.ssh/id_ed25519.pub` 的内容添加到云电脑

```bash
# 在云电脑上执行
mkdir -p ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

2. **GitHub 仓库**：确保代码已推送到 GitHub

### 使用流程

```bash
# 1. 在沙箱编写代码...

# 2. 推送到 GitHub 并触发云电脑编译
make sync-all

# 3. 查看编译状态
make sync-status

# 4. SSH 到云电脑调试（如需要）
make cloud-ssh
```

### 云电脑首次设置

```bash
# 1. 在云电脑上克隆仓库（首次）
ssh -i .ssh/id_ed25519 coze@115.190.107.107
mkdir -p /home/coze/projects
cd /home/coze/projects
git clone https://github.com/your-org/volc_ai_realtime_agent.git

# 2. 在云电脑上启动 Webhook 服务
cd volc_ai_realtime_agent
python3 scripts/cloud_build.py --webhook
```

### 命令清单

| 命令 | 说明 |
|------|------|
| `make sync-github` | 仅推送到 GitHub |
| `make sync-trigger` | 仅触发云电脑编译 |
| `make sync-all` | 推送 + 触发（常用） |
| `make sync-status` | 查看编译状态 |
| `make cloud-ssh` | SSH 连接云电脑 |
| `make cloud-webhook` | 启动 Webhook 服务 |

## 参考链接

- [火山 RTC 文档](https://www.volcengine.com/docs/6348/?lang=zh)
- [AGENTS.md](./AGENTS.md) - 开发规范
# End-to-end test
# E2E Test Tue Apr 21 15:44:28 CST 2026
