# Robot RTC Client - Linux

火山引擎AI音视频互动方案的Linux RTC客户端

## 功能特性

- RTC房间管理
- 音频采集和播放
- 消息收发（文本、二进制）
- 事件回调处理
- 控制指令解析

## 依赖

- CMake 3.13+
- C++17 编译器
- PulseAudio 开发库（Linux）
- 火山引擎RTC SDK

### 安装依赖（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install -y \
    build-essential \
    cmake \
    pkg-config \
    libpulse-dev \
    libasound2-dev
```

## 编译

```bash
# 创建构建目录
mkdir build && cd build

# 配置
cmake ..

# 编译
make -j$(nproc)

# 安装
sudo make install
```

## 运行

```bash
# 基本运行
./robot_rtc_client --app-id your_app_id --room-id robot-room-001

# 交互模式
./robot_rtc_client
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --app-id | 火山引擎App ID | - |
| --room-id | RTC房间ID | robot-room-001 |
| --user-id | 用户ID | robot-client-001 |

## 交互命令

| 命令 | 说明 |
|------|------|
| help | 显示帮助 |
| join \<room\> | 加入房间 |
| leave | 离开房间 |
| start | 开始音频采集 |
| stop | 停止音频采集 |
| send \<text\> | 发送文本消息 |
| trigger | 发送触发信号 |
| interrupt | 发送打断信号 |
| quit | 退出程序 |

## 集成说明

### 1. 集成火山引擎RTC SDK

```bash
# 下载RTC SDK
git clone https://github.com/volcengine/rtc-sdk-linux.git

# 设置环境变量
export RTC_SDK_PATH=/path/to/rtc-sdk

# 重新编译
cd build
cmake .. -DRTC_SDK_PATH=${RTC_SDK_PATH}
make
```

### 2. 集成nlohmann/json

```bash
git clone https://github.com/nlohmann/json.git
sudo cp -r json/include/nlohmann /usr/local/include/
```

## 与机器人控制服务端集成

```
┌─────────────┐    RTC音频流    ┌─────────────────┐
│   机器人    │ ──────────────→ │  火山引擎AI服务  │
│  (C++ RTC)  │                 │                 │
└─────────────┘                 │  - ASR识别      │
        ↑                       │  - LLM处理      │
        │                       │  - TTS合成      │
   控制指令                      │  - Function Call│
        ↑                       └────────┬────────┘
        │                                │
        │ HTTP Webhook                   ↓
        │                         ┌─────────────────┐
        └──────────────────────── │ 机器人控制服务端 │
          Function Calling结果    │  (Python FastAPI)│
                                 └────────┬────────┘
                                          │
                                          ↓
                                 ┌─────────────────┐
                                 │   机器人硬件     │
                                 └─────────────────┘
```

## 许可证

MIT License
