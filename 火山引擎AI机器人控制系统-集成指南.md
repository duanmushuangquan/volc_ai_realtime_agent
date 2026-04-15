# 火山引擎AI音视频互动方案 - 机器人控制系统集成指南

## 📋 方案概述

本项目基于火山引擎**AI音视频互动方案**（StartVoiceChat API）构建智能机器人控制系统。

**核心特点**：
- ✅ **火山引擎提供完整AI能力** - 无需自建Agent
- ✅ **RTC实时音视频** - 低延迟语音交互
- ✅ **Function Calling** - 接入自定义工具（机器人控制）
- ✅ **C++底层控制** - 机器人硬件驱动

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用户（说话/听声音）                            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 语音
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Linux RTC客户端 (C++)                             │
│  - 音频采集（麦克风）                                                 │
│  - 音频播放（扬声器）                                                 │
│  - RTC房间通信                                                       │
│  - 控制指令收发                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ RTC音频流
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    火山引擎RTC Cloud + AI服务                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   ASR识别   │→ │  LLM处理    │→ │  TTS合成    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                          │                                          │
│                          ↓ (Function Calling)                        │
│                   ┌─────────────┐                                   │
│                   │ 自定义工具   │                                   │
│                   │ Webhook回调  │                                   │
│                   └─────────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP POST
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    机器人控制服务端 (Python)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │ 工具注册表  │  │ 命令执行器  │  │ 知识库      │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│  ┌─────────────┐  ┌─────────────┐                                   │
│  │ 网页搜索   │  │ 状态查询    │                                   │
│  └─────────────┘  └─────────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 串口/CAN
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         机器人硬件                                   │
│  - 移动底盘                                                          │
│  - 机械臂                                                            │
│  - 传感器                                                            │
└─────────────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
├── 火山引擎AI机器人控制系统/
│   │
│   ├── 架构文档.md                 # 本架构文档
│   ├── 集成指南.md                 # 本集成指南
│   │
│   ├── robot-control-server/      # 机器人控制服务端
│   │   ├── server.py              # FastAPI主服务（Function Calling Webhook）
│   │   ├── requirements.txt       # Python依赖
│   │   ├── tools/                  # 工具模块
│   │   │   ├── robot.py           # 机器人控制
│   │   │   ├── knowledge.py       # 知识库
│   │   │   └── search.py          # 网页搜索
│   │   └── utils/                 # 工具函数
│   │       ├── config.py          # 配置管理
│   │       └── logging.py         # 日志
│   │
│   └── linux-rtc-client/          # Linux RTC客户端
│       ├── CMakeLists.txt         # CMake配置
│       ├── README.md              # 使用说明
│       ├── include/               # 头文件
│       │   └── RobotRTCClient.h   # RTC客户端接口
│       └── src/                    # 源文件
│           ├── RobotRTCClient.cpp # RTC客户端实现
│           └── main.cpp           # 主程序
```

## 🚀 快速集成

### 步骤1：配置火山引擎服务

1. 登录 [火山引擎控制台](https://console.volcengine.com/)
2. 开通 **RTC** 服务，获取 `AppId` 和 `Token`
3. 开通 **AI音视频互动方案**
4. 配置 **Function Calling 回调URL**：
   ```
   https://your-server.com/tools/call
   ```

### 步骤2：部署机器人控制服务端

```bash
# 进入服务端目录
cd robot-control-server

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export VOLC_APP_ID="your_app_id"
export VOLC_TOKEN="your_token"
export SERVER_PORT=8080

# 启动服务
python server.py

# 或使用uvicorn
uvicorn server:app --host 0.0.0.0 --port 8080
```

**验证服务**：
```bash
# 健康检查
curl http://localhost:8080/health

# 获取工具列表
curl http://localhost:8080/tools
```

### 步骤3：编译Linux RTC客户端

```bash
# 进入客户端目录
cd linux-rtc-client

# 安装依赖
sudo apt install build-essential cmake libpulse-dev

# 编译
mkdir build && cd build
cmake ..
make -j$(nproc)

# 安装
sudo make install
```

### 步骤4：启动对话

```bash
# 基本运行
./robot_rtc_client --app-id your_app_id --room-id robot-room-001

# 交互模式
./robot_rtc_client
```

## 📡 API接口

### 机器人控制服务端 - Function Calling接口

**接口地址**：`POST /tools/call`

**请求示例**（火山引擎发送）：
```json
{
  "TaskId": "task-xxx",
  "RoomId": "robot-room-001",
  "ToolCallId": "call-xxx",
  "FunctionName": "robot_control",
  "Arguments": {
    "action": "move_forward",
    "parameter": 1.5
  },
  "Timestamp": 1712345678901
}
```

**响应示例**：
```json
{
  "ToolCallId": "call-xxx",
  "Result": "机器人已向前移动1.5米",
  "Success": true
}
```

### 可用工具

| 工具名称 | 说明 | 参数 |
|---------|------|------|
| `robot_control` | 控制机器人动作 | action, parameter |
| `get_robot_status` | 查询机器人状态 | status_type |
| `search_knowledge` | 知识库检索 | query, top_k |
| `web_search` | 网页搜索 | query, count |
| `execute_command` | 执行系统命令 | command |

### 状态回调接口

**接口地址**：`POST /status/callback`

**支持的事件**：

| 事件 | 说明 |
|------|------|
| `start` | 任务开始 |
| `asrResult` | ASR识别结果 |
| `llmOutput` | LLM输出 |
| `answerStart` | AI开始说话 |
| `toolCall` | 工具调用 |
| `toolResult` | 工具结果 |
| `interrupted` | AI被打断 |
| `end` | 任务结束 |

## 🔧 配置说明

### 火山引擎StartVoiceChat配置

```json
{
  "AppId": "your_app_id",
  "AgentConfig": {
    "UserId": "robot-assistant",
    "WelcomeSpeech": "您好，我是机器人助手，有什么可以帮助您的？"
  },
  "LLMConfig": {
    "Model": "doubao-seed-1.6",
    "Temperature": 0.7,
    "MaxTokens": 2048
  },
  "ASRConfig": {
    "Model": "volc_engine_asr",
    "TurnDetectionMode": 0
  },
  "TTSConfig": {
    "VoiceType": "female_yunyang",
    "Speed": 1.0
  },
  "FunctionCallingConfig": {
    "Enabled": true,
    "FunctionUrl": "https://your-server.com/tools/call",
    "Timeout": 5000
  }
}
```

### 工具定义

在火山引擎控制台配置以下工具定义：

```json
{
  "name": "robot_control",
  "description": "控制机器人执行各种动作",
  "parameters": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["move_forward", "move_backward", "turn_left", "turn_right", 
                 "arm_up", "arm_down", "grip_open", "grip_close", "stop"]
      },
      "parameter": {
        "type": "number"
      }
    }
  }
}
```

## 📝 使用示例

### 场景1：用户让机器人移动

```
用户：机器人，向前走两米
```

**处理流程**：
1. 用户语音 → ASR识别 → "机器人，向前走两米"
2. LLM识别意图 → 调用 `robot_control` 工具
3. 机器人控制服务端接收请求 → 执行移动命令
4. 返回结果 → LLM生成回复 → TTS合成 → 播放
5. AI："好的，机器人正在向前移动两米"

### 场景2：用户查询机器人状态

```
用户：电量还剩多少？
```

**处理流程**：
1. ASR识别 → "电量还剩多少？"
2. LLM识别意图 → 调用 `get_robot_status`
3. 服务端查询电池状态 → 返回 "电量80%"
4. AI："电池电量还剩80%，建议适时充电"

### 场景3：用户询问知识库内容

```
用户：机器人的操作注意事项有哪些？
```

**处理流程**：
1. ASR识别 → "机器人的操作注意事项有哪些？"
2. LLM识别意图 → 调用 `search_knowledge`
3. 服务端检索知识库 → 返回相关内容
4. AI朗读注意事项

## 🐛 调试指南

### 查看服务端日志

```bash
# 实时查看日志
tail -f /tmp/robot_server.log

# 查看错误日志
grep -i error /tmp/robot_server.log
```

### 测试Function Calling接口

```bash
curl -X POST http://localhost:8080/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "TaskId": "test-001",
    "RoomId": "test-room",
    "ToolCallId": "test-call-001",
    "FunctionName": "robot_control",
    "Arguments": {"action": "move_forward", "parameter": 1.0},
    "Timestamp": 1712345678901
  }'
```

### 测试机器人控制

```bash
# 直接控制机器人
curl -X POST "http://localhost:8080/robot/control?action=move_forward&parameter=1.5"

# 查询状态
curl "http://localhost:8080/robot/status?status_type=all"
```

## ⚠️ 注意事项

1. **Function Calling URL必须公网可访问**
   - 火山引擎服务器需要回调此URL
   - 使用ngrok或内网穿透
   - 或部署到公网服务器

2. **响应时间限制**
   - 默认超时5秒
   - 复杂操作需要提前返回

3. **安全考虑**
   - 验证回调请求的签名
   - 限制危险命令执行
   - 防止未授权访问

4. **音频配置**
   - 推荐：16kHz, 16bit, 单声道
   - 确保网络稳定

## 📚 相关文档

- [火山引擎RTC文档](https://www.volcengine.com/docs/6348/)
- [AI音视频互动方案](https://www.volcengine.com/docs/6348/1544162)
- [StartVoiceChat API](https://www.volcengine.com/docs/6348/131050)
- [判停与对话触发](https://www.volcengine.com/docs/6348/1544164)

## 🔗 技术支持

- 火山引擎控制台：https://console.volcengine.com/
- 技术支持邮箱：support@volcengine.com
