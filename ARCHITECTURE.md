# AI 音视频交互方案机器人控制系统架构

> **文档状态**：初期调研，待完善
> **创建时间**：2025年
> **维护者**：待定
> **版本**：v0.1

---

## 目录

1. [项目背景与目标](#1-项目背景与目标)
2. [核心需求分析](#2-核心需求分析)
3. [技术调研总结](#3-技术调研总结)
4. [系统架构设计](#4-系统架构设计)
5. [模块详细设计](#5-模块详细设计)
6. [通信链路设计](#6-通信链路设计)
7. [部署形态](#7-部署形态)
8. [关键技术选型](#8-关键技术选型)
9. [健康与安全系统](#9-健康与安全系统)
10. [实施计划](#10-实施计划)
11. [待确认问题](#11-待确认问题)
12. [假设与约束](#12-假设与约束)

---

## 1. 项目背景与目标

### 1.1 项目愿景

构建一个**云边协同**的机器人控制系统，核心能力：
- 实时语音交互（自然对话）
- 工具调用与知识检索
- 真机/仿真无缝切换
- 网络自适应（在线/离线）

### 1.2 目标平台

| 平台 | 架构 | 说明 |
|------|------|------|
| 主机 | AMD/x86 | 开发环境、高性能推理 |
| 边缘 | ARM/NVIDIA Orin | 部署到机器人的计算单元 |
| 仿真 | Isaac Sim | NVIDIA 物理仿真 |

### 1.3 目标机器人类型

1. **人形机器人**
2. **智能远洋船舶**

---

## 2. 核心需求分析

### 2.1 语音交互能力

| 模式 | 描述 | 延迟要求 |
|------|------|----------|
| **三段式** | ASR → LLM → TTS | <500ms |
| **端到端 (S2S)** | 语音 → 语音直接转换 | <500ms |

### 2.2 工具调用能力

支持多种通信协议的**统一工具调用**：

```yaml
技能类型:
  - DDS: 机器人控制命令
  - HTTP: 外部服务调用（网页搜索、数据库查询）
  - WebSocket: 实时数据流（遥测、视频）
```

### 2.3 仿真与真机

| 能力 | 描述 |
|------|------|
| **单独调试** | 真机和仿真各自独立运行 |
| **联合调试** | 仿真与真机同时运行 |
| **无缝切换** | 通过配置切换 Runtime 模式 |

### 2.4 网络自适应

```
网络状态检测 → 自动切换模式
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
    [在线模式]            [离线模式]
    火山云服务           本地模型
```

---

## 3. 技术调研总结

### 3.1 火山引擎 RTC + AI 语音

| 组件 | 能力 | 独立性 | 离线支持 |
|------|------|--------|----------|
| **veRTC SDK (C++/Linux)** | 实时音视频传输 | ⭐ 核心独立 | ❌ 依赖云服务 |
| **ASR 流式识别 API** | 语音→文本 | ⭐ 可独立调用 | ❌ |
| **TTS 流式合成 API** | 文本→语音 | ⭐ 可独立调用 | ❌ |
| **LLM 对话 API** | 文本生成（豆包等） | ⭐ 可独立调用 | ❌ |
| **S2S 端到端** | 语音→语音直接 | ⭐ 可独立调用 | ❌ |
| **边缘大模型网关** | 云端模型边缘部署 | ⚠️ 企业合作 | ✅ |

**关键发现**：
- ASR/TTS 均提供**双向流式 API**
- 三段式（ASR + LLM + TTS）是标准组合，可拆解替换
- 火山离线方案需企业合作，短期不推荐

### 3.2 离线语音方案对比

#### ASR 方案

| 方案 | 参数量 | 离线 | Orin 性能 | 中文支持 | 推荐度 |
|------|--------|------|-----------|----------|--------|
| **FunASR** | ~400MB | ✅ | <200ms | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Qwen3-ASR 1.7B** | ~3.5GB | ✅ | 300-500ms | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Whisper** | ~3GB | ✅ | 500ms+ | ⭐⭐⭐ | ⭐⭐⭐ |
| **NVIDIA Riva** | ~2GB | ✅ | 24-160ms | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **火山 ASR** | 云端 | ❌ | <100ms | ⭐⭐⭐⭐⭐ | 云端首选 |

#### TTS 方案

| 方案 | 离线 | 中文支持 | 音色克隆 | 推荐度 |
|------|------|----------|----------|--------|
| **FunTTS** | ✅ | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |
| **Coqui XTTS-v2** | ✅ | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **火山 TTS** | ❌ | ⭐⭐⭐⭐⭐ | ✅ | 云端首选 |

#### S2S 端到端方案

| 方案 | 类型 | 离线 | 延迟 | 推荐度 |
|------|------|------|------|--------|
| **Fun-Audio-Chat** | 开源 | ✅ | 500ms+ | ⭐⭐⭐⭐ |
| **火山 S2S** | 云服务 | ❌ | <500ms | 云端首选 |
| **Pipecat + 本地模型** | 框架 | ✅ | 500ms | ⭐⭐⭐⭐ |

#### Orin 推理优化建议

1. **TensorRT 优化**：延迟降低 3 倍
2. **INT8 量化**：内存减半，性能损失 <5%
3. **音频帧对齐**：按 64 字节对齐（ARM 优化）

### 3.3 OpenClaw 架构分析

OpenClaw 是**面向具身智能**的开源框架，核心架构：

```
Gateway（网关）+ Agent（大脑）+ Skills（技能）+ Memory（记忆）
```

| 组件 | 职责 | 本项目借鉴 |
|------|------|------------|
| **Gateway** | 协议适配、认证、任务分发 | ⭐⭐⭐ 非常关键 |
| **Agent** | 任务规划、决策 | ⭐⭐⭐ 核心 |
| **Skills** | 工具执行 | ⭐⭐⭐ 直接对应 |
| **Memory** | 记忆管理 | ⭐⭐ 可选 |

**你的理解纠偏**：
- ✅ 记忆处理是 OpenClaw 特色
- ✅ Gateway 逻辑值得借鉴
- ❌ OpenClaw 不一定需要集成，借鉴其设计理念即可

### 3.4 Fast DDS / ROS2 通信

#### DDS 核心特点

| 特性 | 说明 |
|------|------|
| **实时性** | 毫秒级延迟 |
| **QoS 策略** | 可靠性、持久性等配置 |
| **去中心化** | 无需 ROS Master |
| **多传输** | UDP/TCP/SHM |

#### DDS vs ROS2

| 方面 | 纯 DDS | ROS2 |
|------|--------|------|
| 耦合度 | 低 | 高 |
| 工具链 | 需要自建 | 丰富 |
| 生态 | 一般 | 丰富 |
| **推荐** | ⭐⭐⭐⭐ | ⭐⭐⭐ |

**结论**：推荐**独立使用 Fast DDS API**，ROS2 桥接作为可选后期添加。

### 3.5 DDS 桥接说明

**问题**：DDS 与非 DDS 系统桥接是什么？

**解答**：

```
┌─────────────────────────────────────────┐
│            DDS 桥接示意图               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐      ┌──────────┐        │
│  │ ROS2 系统│◄────►│ DDS桥接  │◄────►│ 你的系统 │
│  │ (Subscriber)│   │         │        │ (Publisher)│ │
│  └──────────┘      └──────────┘        │
│                                         │
└─────────────────────────────────────────┘

作用：让你的 DDS 消息可被 ROS2 订阅
```

**建议**：先实现纯 DDS，ROS2 桥接作为可选模块后期添加。

### 3.6 硬实时 vs 软实时

| 类型 | 定义 | 适用场景 | 推荐 |
|------|------|----------|------|
| **硬实时** | 超时 = 系统失败 | 工业控制、航空 | ❌ |
| **软实时** | 超时 = 体验下降 | 语音、视频、机器人控制 | ✅ |

**结论**：你的场景不需要硬实时，选择标准配置即可。

### 3.7 Voice Agent 框架

**Pipecat** 是当前热门的开源框架：

| 特性 | 说明 |
|------|------|
| **延迟** | 500ms 级端到端 |
| **集成** | 60+ AI 服务 |
| **语言** | Python |
| **定位** | 语音 + 多模态 AI Agent |

**借鉴价值**：Pipecat 的流式处理和模型集成模式可参考。

---

## 4. 系统架构设计

### 4.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          用户交互层                                       │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────────────┐   │
│   │ Web UI  │  │ 手机 APP │  │ 语音终端│  │ Isaac Sim (仿真模式)     │   │
│   └────┬────┘  └────┬────┘  └────┬────┘  └───────────┬─────────────┘   │
│        │            │            │                    │                 │
│   ┌────┴────────────┴────────────┴────────────────────┴────────────┐   │
│   │              WebSocket / HTTP (调试/配置)                          │   │
│   └─────────────────────────────┬────────────────────────────────────┘   │
└──────────────────────────────────┼────────────────────────────────────────┘
                                   │
┌──────────────────────────────────┼────────────────────────────────────────┐
│                        AI 交互引擎层 (核心)                               │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                     Voice Gateway                                  │   │
│   │  ┌──────────────────────────────────────────────────────────┐   │   │
│   │  │                    AI Orchestrator                        │   │   │
│   │  │  ┌────────────┐ ┌────────────┐ ┌────────────────────┐   │   │   │
│   │  │  │ 模式管理器  │ │ 网络检测   │ │ 模型健康监控        │   │   │   │
│   │  │  │ 三段式/S2S │ │ 在线/离线  │ │ 降级/恢复策略       │   │   │   │
│   │  │  └────────────┘ └────────────┘ └─────────────────────┘   │   │   │
│   │  └──────────────────────────────────────────────────────────┘   │   │
│   │                                                                  │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│   │  │  ASR Bridge  │  │  LLM Bridge  │  │  TTS Bridge          │  │   │
│   │  │  ┌─────────┐ │  │  ┌─────────┐ │  │  ┌────────────────┐ │  │   │
│   │  │  │ 火山ASR │ │  │  │ 豆包LLM │ │  │  │    火山TTS     │ │  │   │
│   │  │  │ FunASR  │ │  │  │ Qwen3   │ │  │  │    FunTTS      │ │  │   │
│   │  │  │ Whisper │ │  │  │ Ollama  │ │  │  │    Coqui XTTS  │ │  │   │
│   │  │  │ (统一接口)│ │  │  │ (统一接口)│  │  │    (统一接口)  │ │  │   │
│   │  │  └─────────┘ │  │  └─────────┘ │  │  └────────────────┘ │  │   │
│   │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│   │                                                                  │   │
│   │  ┌──────────────────────────────────────────────────────────┐   │   │
│   │  │                   Memory System                            │   │   │
│   │  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐  │   │   │
│   │  │  │ 瞬时记忆 │ │短期记忆 │ │     长期记忆 (文件/DB)    │  │   │   │
│   │  │  │ (当前对话)│ │(会话级) │ │  (跨会话持久化)           │  │   │   │
│   │  │  └──────────┘ └──────────┘ └──────────────────────────┘  │   │   │
│   │  └──────────────────────────────────────────────────────────┘   │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                   Skills Executor                                │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│   │  │ DDS Skills   │  │ HTTP Skills  │  │  WebSocket Skills   │  │   │
│   │  │ - move_arm   │  │ - query_db   │  │  - stream_video     │  │   │
│   │  │ - walk       │  │ - search_web │  │  - telemetry        │  │   │
│   │  │ - gripper    │  │ - call_api   │  │                     │  │   │
│   │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│   │                                                                  │   │
│   │  ┌──────────────────────────────────────────────────────────┐   │   │
│   │  │                   MCP Server (可选)                       │   │   │
│   │  │  - 标准化工具定义  - 工具发现  - 统一接口                 │   │   │
│   │  └──────────────────────────────────────────────────────────┘   │   │
│   └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                        DDS (机器人内部通信)
                                   │
┌──────────────────────────────────┼────────────────────────────────────────┐
│                        Robot Harness 层                                 │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                   Safety Monitor (独立进程)                       │   │
│   │  - 碰撞检测  - 速度/位置限制  - 温度监控  - 急停              │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │               Robot Abstraction Layer (RAL)                     │   │
│   │  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │   │
│   │  │ RealRobotAdapter│  │ IsaacSimAdapter│  │ OtherSimAdapter │   │   │
│   │  │  (真机驱动)     │  │ (Isaac Sim)    │  │ (Gazebo等)      │   │   │
│   │  └───────┬────────┘  └───────┬────────┘  └────────┬────────┘   │   │
│   │          │                   │                    │            │   │
│   │  ┌───────┴───────────────────┴────────────────────┴────────┐   │   │
│   │  │           Unified Robot Interface                         │   │   │
│   │  │   joint_control | eef_control | sensor_read | state     │   │   │
│   │  └────────────────────────────────────────────────────────┘   │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │               DDS-ROS2 Bridge (可选，后期添加)                   │   │
│   └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. 模块详细设计

### 5.1 Voice Gateway（语音网关）

#### 核心职责

1. **协议统一**：ASR/TTS/模型抽象成统一接口
2. **模式切换**：三段式 ↔ S2S ↔ 本地/云端
3. **网络检测**：自动检测网络质量，触发降级/恢复

#### 接口设计（C++）

```cpp
// ASR 统一接口
class IASRProvider {
public:
    virtual ~IASRProvider() = default;
    virtual void start_streaming(std::function<void(const std::string&)> on_result) = 0;
    virtual void send_audio(const AudioFrame& frame) = 0;
    virtual void stop() = 0;
    virtual ProviderInfo get_info() const = 0;
};

// TTS 统一接口
class ITTSProvider {
public:
    virtual ~ITTSProvider() = default;
    virtual void synthesize(const std::string& text,
                           std::function<void(const AudioFrame&)> on_audio) = 0;
    virtual void stop() = 0;
    virtual ProviderInfo get_info() const = 0;
};

// LLM 统一接口
class ILLMProvider {
public:
    virtual ~ILLMProvider() = default;
    virtual void chat(const ChatMessage& msg,
                     std::function<void(const std::string&)> on_token) = 0;
    virtual bool support_function_call() const = 0;
    virtual ProviderInfo get_info() const = 0;
};

// 统一提供者信息
struct ProviderInfo {
    std::string name;
    std::string version;
    bool is_cloud;
    double latency_estimate_ms;
};
```

#### 配置示例（YAML）

```yaml
# config/models.yaml
asr:
  cloud:
    provider: volc_asr
    endpoint: wss://rtc.volcengine.com/asr
    api_key: ${VOLC_ASR_KEY}
  offline:
    provider: funasr
    model_path: /models/funasr
    device: orin
    quantization: int8

tts:
  cloud:
    provider: volc_tts
    endpoint: wss://rtc.volcengine.com/tts
    api_key: ${VOLC_TTS_KEY}
  offline:
    provider: coffin_xtts
    model_path: /models/xtts
    device: orin

llm:
  cloud:
    provider: volc_llm
    model: doubao-pro
    api_key: ${VOLC_LLM_KEY}
  offline:
    provider: qwen3
    model_path: /models/qwen3-8b
    device: orin

# 模式切换策略
mode_strategy:
  default: cloud
  fallback_order: [cloud, offline]
  network_check_interval_ms: 5000
  latency_threshold_ms: 1000
```

### 5.2 Skills Executor（技能执行器）

#### 核心职责

1. **工具注册**：DDS/HTTP/WebSocket 服务注册为 Skills
2. **FunctionCall 解析**：解析 LLM 输出的工具调用
3. **执行协调**：调用对应服务，返回结果给 LLM

#### Skills 定义示例

```yaml
# config/skills.yaml
skills:
  # DDS 技能
  - name: move_forward
    type: dds
    topic: /robot/cmd_vel
    msg_type: geometry_msgs/Twist
    params:
      linear_x:
        type: float
        required: true
        unit: m/s
        range: [-1.0, 1.0]
      duration:
        type: float
        default: 1.0
        unit: s

  - name: walk_to
    type: dds
    topic: /humanoid/navigation
    msg_type: nav_msgs/Path
    params:
      target_x:
        type: float
        required: true
        unit: m
      target_y:
        type: float
        required: true
        unit: m

  - name: set_arm_pose
    type: dds
    topic: /arm/joint_command
    msg_type: robot_control/JointCommand
    params:
      joint_positions:
        type: array[float]
        required: true
        unit: rad

  # HTTP 技能
  - name: web_search
    type: http
    endpoint: ${SEARCH_SERVICE_URL}/api/search
    method: POST
    timeout_ms: 5000
    params:
      query:
        type: string
        required: true
        max_length: 500

  - name: query_knowledge_base
    type: http
    endpoint: ${KB_SERVICE_URL}/api/query
    method: POST
    params:
      question:
        type: string
        required: true

  # WebSocket 技能
  - name: stream_telemetry
    type: websocket
    endpoint: ws://${TELEMETRY_SERVICE}/stream
    params:
      topics:
        type: array[string]
        required: true
      sample_rate_hz:
        type: int
        default: 30
```

### 5.3 Robot Harness（机器人抽象层）

#### 核心职责

1. **仿真/真机无缝切换**
2. **统一控制接口**
3. **Safety 监控**

#### 接口设计

```cpp
// 统一机器人接口
class IRobotAdapter {
public:
    virtual ~IRobotAdapter() = default;

    // 初始化与销毁
    virtual bool initialize() = 0;
    virtual void shutdown() = 0;

    // 关节控制
    virtual void set_joint_positions(const std::vector<double>& positions) = 0;
    virtual std::vector<double> get_joint_positions() = 0;
    virtual void set_joint_velocities(const std::vector<double>& velocities) = 0;

    // 末端控制
    virtual void set_ee_pose(const Pose& pose) = 0;
    virtual Pose get_ee_pose() = 0;

    // 传感器
    virtual JointState get_joint_states() = 0;
    virtual Image get_camera_image(const std::string& camera_name) = 0;
    virtual ImuData get_imu() = 0;

    // 仿真控制
    virtual void step() = 0;  // 仿真器推进
    virtual void reset() = 0;
    virtual double get_sim_time() = 0;

    // 状态
    virtual RobotState get_state() = 0;
};

// 机器人状态
struct RobotState {
    bool is_connected;
    bool is_moving;
    bool has_error;
    std::string error_message;
    double timestamp;
};

// 姿态
struct Pose {
    double x, y, z;           // 位置 (m)
    double qx, qy, qz, qw;   // 四元数
};

// 关节状态
struct JointState {
    std::vector<std::string> names;
    std::vector<double> positions;    // rad
    std::vector<double> velocities;    // rad/s
    std::vector<double> efforts;       // Nm
    double timestamp;
};
```

#### 适配器实现

```cpp
// 真机适配器
class RealRobotAdapter : public IRobotAdapter {
private:
    std::unique_ptr<FastDDSClient> dds_client_;
    std::vector<std::string> joint_names_;
    // ...

public:
    RealRobotAdapter(const RobotConfig& config);
    bool initialize() override;
    void set_joint_positions(const std::vector<double>& positions) override;
    // ...
};

// Isaac Sim 适配器
class IsaacSimAdapter : public IRobotAdapter {
private:
    // Omniverse/PhysX 相关
    omni::stage::WorldPtr world_;
    physx::ScenePtr scene_;
    // ...

public:
    IsaacSimAdapter(const SimConfig& config);
    bool initialize() override;
    void step() override;  // 推进仿真
    void set_joint_positions(const std::vector<double>& positions) override;
    // ...
};

// Gazebo 适配器 (备选)
class GazeboAdapter : public IRobotAdapter {
    // ...
};
```

### 5.4 Memory System（记忆系统）

#### 层级设计

| 层级 | 存储位置 | 生命周期 | 内容 |
|------|----------|----------|------|
| **瞬时记忆** | 内存 | 对话轮次 | 当前任务、即时需求 |
| **短期记忆** | 内存 + Redis | 会话 | 会话历史、上下文 |
| **长期记忆** | 文件/数据库 | 跨会话 | 偏好、知识、技能 |

#### 实现示例

```cpp
class MemorySystem {
public:
    // 瞬时记忆
    void set_working_memory(const std::string& key, const std::string& value);
    std::optional<std::string> get_working_memory(const std::string& key);

    // 短期记忆
    void add_to_short_term(const MemoryItem& item);
    std::vector<MemoryItem> get_short_term_history(int max_items = 10);
    void clear_short_term();

    // 长期记忆
    void store_to_long_term(const MemoryItem& item);
    std::vector<MemoryItem> search_long_term(const std::string& query);
    void update_memory_priority(const std::string& id, float priority);
};
```

---

## 6. 通信链路设计

### 6.1 通信分层

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           通信链路分层                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Layer 1: 外部通信 (用户 ↔ 系统)                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  WebSocket: 用户界面 / 实时调试                                     │   │
│  │  HTTP: 配置管理 / 状态查询                                          │   │
│  │  火山 RTC: 语音/视频流 (在线模式)                                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│  Layer 2: AI 模块间通信                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  gRPC + Protobuf: ASR ↔ LLM ↔ TTS (流式、低延迟)                  │   │
│  │  HTTP: 外部服务调用 (Web Search 等)                               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│  Layer 3: 机器人内部通信                                                │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  DDS (Fast DDS): 实时控制命令 / 传感器数据                         │   │
│  │  - /robot/cmd_vel (速度命令)                                       │   │
│  │  - /robot/joint_states (关节状态)                                  │   │
│  │  - /robot/camera/image (视觉数据)                                  │   │
│  │  - /robot/safety/status (安全状态)                                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  Layer 4: 仿真 ↔ 真机 (二选一，通过 RAL 适配)                            │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  真机模式: DDS ↔ 真实机器人驱动                                    │   │
│  │  仿真模式: DDS ↔ Isaac Sim (Omniverse)                            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 DDS 消息定义（IDL）

```idl
// robot_control.idl
module robot_control {
    @nested
    struct JointCommand {
        string robot_name;
        sequence<string> joint_names;
        sequence<double> positions;
        double duration;
    };

    @nested
    struct EEFCommand {
        string robot_name;
        sequence<double> pose;  // x, y, z, qx, qy, qz, qw
        double duration;
    };

    @nested
    struct VelocityCommand {
        string robot_name;
        double linear_x;
        double linear_y;
        double angular_z;
    };
};

// robot_sensor.idl
module robot_sensor {
    @nested
    struct JointState {
        string robot_name;
        sequence<string> joint_names;
        sequence<double> positions;
        sequence<double> velocities;
        sequence<double> efforts;
        @optional double timestamp;
    };

    @nested
    struct Heartbeat {
        string robot_name;
        string status;
        double cpu_temp;
        double battery_level;
        @optional double timestamp;
    };
};
```

---

## 7. 部署形态

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          部署架构                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     机器人端 (ARM/Orin)                           │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐   │    │
│  │  │ Voice Engine│ │ DDS Client  │ │ Robot Harness            │   │    │
│  │  │ - FunASR    │ │ - Publisher│ │ - RealRobotAdapter      │   │    │
│  │  │ - FunTTS    │ │ - Subscriber│ │ - IsaacSimAdapter       │   │    │
│  │  │ - Qwen3-8B  │ │ - QoS配置   │ │ - SafetyMonitor        │   │    │
│  │  │ (可选本地)   │ │             │ │                        │   │    │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐   │    │
│  │  │              Skills Executor                             │   │    │
│  │  │  - DDS Skills  - HTTP Skills  - WS Skills               │   │    │
│  │  └─────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  OS: Ubuntu 22.04 / JetPack 6.0                                │    │
│  │  资源: Orin AGX (32GB) / Orin NX (8GB)                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                      │
│                          LAN / WiFi / 5G / Satellite                     │
│                                    │                                      │
│  ┌─────────────────────────────────┴─────────────────────────────────┐   │
│  │                     远端服务器 (AMD/x86) (可选)                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    火山 RTC 服务                             │   │   │
│  │  │  - 语音通话   - TURN服务   - 信令服务                       │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    云端 AI 服务 (可选)                        │   │   │
│  │  │  - 豆包 LLM   - 火山 ASR/TTS                                │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Isaac Sim (仿真服务器)                      │   │   │
│  │  │  - GPU 服务器 (RTX 4090+)                                    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. 关键技术选型

### 8.1 语音模块

| 模块 | 在线方案 | 离线方案 (Orin) | 备选 |
|------|---------|----------------|------|
| **ASR** | 火山 ASR (<100ms) | FunASR (<200ms) | Qwen3-ASR, Whisper |
| **TTS** | 火山 TTS | Coqui XTTS-v2 | FunTTS |
| **LLM** | 豆包 Pro | Qwen3-8B | Ollama |
| **S2S** | 火山 S2S | Fun-Audio-Chat | - |

### 8.2 通信与中间件

| 组件 | 选型 | 说明 |
|------|------|------|
| **实时通信** | 火山 veRTC | 全球低延迟 (~200ms) |
| **DDS** | Fast DDS | 独立 API，不深度耦合 ROS2 |
| **HTTP Server** | FastAPI / uWebSockets | 高性能异步 |
| **WebSocket** | uWebSockets | 轻量级 |
| **gRPC** | gRPC + Protobuf | AI 模块间流式通信 |

### 8.3 仿真

| 仿真器 | 选型 | 说明 |
|--------|------|------|
| **首选** | Isaac Sim | NVIDIA 生态、物理准确 |
| **备选** | Gazebo | 开源、ROS2 原生支持 |

### 8.4 硬件

| 平台 | 选型 | 说明 |
|------|------|------|
| **边缘计算** | NVIDIA Orin AGX/NX | AI 加速 |
| **开发主机** | AMD64 + NVIDIA GPU | 高性能推理 |

### 8.5 工具链

| 组件 | 选型 |
|------|------|
| **语言** | C++ (核心), Python (AI 模块) |
| **构建** | CMake + Conan |
| **容器** | Docker |
| **编排** | Docker Compose |

---

## 9. 健康与安全系统

### 9.1 Safety Monitor（独立进程）

```cpp
class SafetyMonitor {
public:
    void start();
    void stop();

private:
    // DDS 心跳订阅
    void on_heartbeat(const HeartbeatMsg& msg);

    // 定时检查
    void check_system_health();

    // Safety 触发
    void trigger_emergency_stop(const std::string& reason);

    // 规则检查
    bool check_velocity_limit(const VelocityCommand& cmd);
    bool check_position_limit(const JointCommand& cmd);
    bool check_collision(const Pose& pose);
};
```

### 9.2 Safety Rules

```yaml
# config/safety_rules.yaml
safety_rules:
  - name: humanoid_walk
    max_velocity: 0.5        # m/s
    max_acceleration: 1.0   # m/s²
    joint_limits_min: -1.5   # rad
    joint_limits_max: 1.5    # rad
    collision_threshold: 0.1  # m

  - name: humanoid_arm
    max_velocity: 1.0        # rad/s
    max_acceleration: 2.0    # rad/s²
    joint_limits_min: -3.0   # rad
    joint_limits_max: 3.0     # rad
    collision_threshold: 0.05  # m

  - name: ship_actuator
    max_velocity: 0.2        # m/s
    max_acceleration: 0.5    # m/s²
    collision_threshold: 0.2  # m

health_check:
  heartbeat_timeout_ms: 1000
  cpu_temp_warning: 80.0      # °C
  cpu_temp_critical: 90.0     # °C
  battery_warning: 20.0      # %
  battery_critical: 10.0     # %
```

---

## 10. 实施计划

### 10.1 近期（1-2 周）

#### 目标：搭建基础框架 + 跑通 Demo

1. **项目初始化**
   - 创建项目结构
   - 配置 CMake + Conan
   - 搭建 Docker 开发环境

2. **ASR/TTS 统一接口**
   - 定义 `IASRProvider` / `ITTSProvider` 接口
   - 实现 FunASR 适配器
   - 实现 Coqui XTTS 适配器

3. **基础 Demo**
   - Linux 桌面版：三段式对话（ASR + LLM + TTS）
   - 验证延迟和效果

### 10.2 中期（1 个月）

#### 目标：集成火山 RTC + 实现 Skills 系统

1. **火山 RTC 集成**
   - 对接 veRTC SDK
   - 实现云/离线自动切换
   - 性能对比测试

2. **Skills Executor**
   - 实现 Skills 注册系统
   - DDS 通信基础
   - 简单工具调用 Demo

3. **Memory System（可选）**
   - 短期记忆实现
   - 对话历史管理

### 10.3 远期（2-3 个月）

#### 目标：集成 Isaac Sim + 完善安全系统

1. **Robot Harness**
   - 实现 RAL 统一接口
   - RealRobotAdapter 开发
   - IsaacSimAdapter 开发

2. **Safety Monitor**
   - 健康检查实现
   - Safety Rules 配置
   - 急停机制

3. **ROS2 桥接（可选）**
   - DDS-ROS2 话题转换
   - 协议适配

---

## 11. 待确认问题

### 11.1 核心决策

| # | 问题 | 选项 |
|---|------|------|
| Q1 | **本地 LLM 选型** | A. Qwen3-8B（推荐） B. 其他（请说明） |
| Q2 | **仿真器授权** | A. Isaac Sim（有授权） B. Gazebo（开源备选） |
| Q3 | **船舶场景特殊需求** | 是否有卫星通信、特殊传感器需求？ |

### 11.2 技术细节

| # | 问题 | 说明 |
|---|------|------|
| T1 | **Orin 型号** | Orin AGX (32GB) 还是 Orin NX (8GB)？ |
| T2 | **本地模型量化** | INT8 还是 FP16？ |
| T3 | **记忆系统优先级** | 是否需要长期记忆？ |
| T4 | **MCP 集成** | 是否需要 MCP 协议支持？ |

---

## 12. 假设与约束

### 12.1 当前假设

1. **网络**：大部分场景有网络，优先使用火山云服务
2. **延迟**：语音端到端 <500ms 即可接受
3. **实时性**：软实时即可，不需要硬实时
4. **ROS2**：不深度耦合 ROS2，使用纯 DDS API
5. **VLA**：暂不集成 VLA 模型，后期可扩展

### 12.2 约束条件

1. **平台**：Linux (AMD64/ARM)
2. **边缘**：NVIDIA Orin
3. **延迟**：语音响应越快越好
4. **灵活性**：模型可替换、可切换

### 12.3 风险提示

| 风险 | 影响 | 应对 |
|------|------|------|
| 火山离线方案不可用 | 离线体验下降 | 准备 FunASR/XTTS 方案 |
| Isaac Sim 授权问题 | 仿真受限 | 准备 Gazebo 备选 |
| Orin 推理性能不足 | 延迟过高 | TensorRT 优化 + 模型量化 |

---

## 附录

### A. 参考资料

1. 火山引擎 RTC 文档：https://www.volcengine.com/docs/6348/
2. FunASR GitHub：https://github.com/modelscope/FunASR
3. Qwen3-ASR：阿里通义千问语音识别模型
4. Coqui XTTS：https://github.com/coqui-ai/TTS
5. Fast DDS：https://www.eprosima.com/index.php/products-all/eprosima-fast-dds
6. OpenClaw：面向具身智能的开源框架
7. Pipecat：实时语音 AI Agent 框架
8. Isaac Sim：https://developer.nvidia.com/isaac-sim

### B. 术语表

| 术语 | 说明 |
|------|------|
| ASR | Automatic Speech Recognition，语音识别 |
| TTS | Text-to-Speech，语音合成 |
| LLM | Large Language Model，大语言模型 |
| S2S | Speech-to-Speech，端到端语音 |
| DDS | Data Distribution Service，数据分发服务 |
| VLA | Vision-Language-Action，视觉-语言-动作模型 |
| RAL | Robot Abstraction Layer，机器人抽象层 |
| RTC | Real-Time Communication，实时通信 |
| QoS | Quality of Service，服务质量 |
| MCP | Model Context Protocol，模型上下文协议 |

---

*文档最后更新：待补充*
