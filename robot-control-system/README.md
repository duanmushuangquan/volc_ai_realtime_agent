# Robot Control System

火山引擎AI音视频互动方案 - 机器人控制系统

## 项目概述

这是一个基于火山引擎豆包大模型的智能机器人控制系统，支持对话交互、网页搜索、工具调用、知识库检索和硬件控制等功能。

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Robot Control System                      │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (FastAPI + WebSocket)                         │
├─────────────────────────────────────────────────────────────┤
│  AI Agent Layer (LangGraph + 豆包大模型)                     │
│  - Intent Detection  - Tool Planning                        │
│  - Tool Execution     - Response Synthesis                   │
├─────────────────────────────────────────────────────────────┤
│  Tools Layer                                                  │
│  - Web Search        - Knowledge Base                       │
│  - Command Exec      - Hardware Control                     │
├─────────────────────────────────────────────────────────────┤
│  RTC Layer (火山引擎RTC SDK)                                 │
├─────────────────────────────────────────────────────────────┤
│  Hardware Layer (C++/Python)                                 │
└─────────────────────────────────────────────────────────────┘
```

## 核心功能

### 1. 智能对话
- 基于豆包大模型的自然语言对话
- 多轮对话上下文管理
- 流式响应支持

### 2. 网页搜索
- 火山引擎Search API集成
- 实时网络信息查询
- AI摘要生成

### 3. 工具调用
- 系统命令执行（安全限制）
- 知识库检索
- 数学计算
- 时间查询

### 4. 知识库
- 向量数据库存储
- 语义检索
- 知识图谱支持

### 5. 硬件控制
- 机器人运动控制
- 传感器数据采集
- 串口/CAN通信

## 技术栈

### 核心框架
- **Web框架**: FastAPI
- **AI框架**: LangChain + LangGraph
- **火山引擎SDK**: coze-coding-dev-sdk

### 数据层
- **向量数据库**: ChromaDB
- **对话存储**: SQLite

### 通信
- **WebSocket**: 实时通信
- **SSE**: 流式响应
- **gRPC**: 进程间通信

## 快速开始

### 1. 安装依赖

```bash
cd robot-control-system
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
export VOLC_APP_ID="your-app-id"
export VOLC_TOKEN="your-token"
export COZE_API_KEY="your-api-key"
```

### 3. 启动服务

```bash
cd python
python -m api.main
```

或者：

```bash
uvicorn api.main:app --host 0.0.0.0 --port 5000
```

### 4. 访问Web界面

打开浏览器访问：http://localhost:5000

## API文档

启动服务后访问：http://localhost:5000/docs

### 主要接口

#### 对话接口
```bash
POST /api/chat
{
  "message": "你好",
  "conversation_id": "test",
  "stream": true
}
```

#### WebSocket实时对话
```
WS /ws/chat/{client_id}
```

#### 工具调用
```bash
POST /api/tools/call
{
  "tool_name": "web_search",
  "parameters": {
    "query": "最新新闻",
    "count": 5
  }
}
```

#### 知识库检索
```bash
POST /api/knowledge/search?query=机器人控制&top_k=3
```

#### 硬件控制
```bash
POST /api/hardware/control
{
  "action": "move_forward",
  "parameter": 1.0
}
```

## 项目结构

```
robot-control-system/
├── python/                    # Python控制层
│   ├── agent/                 # AI Agent核心
│   │   ├── chat.py           # 对话管理
│   │   ├── tools.py          # 工具管理
│   │   ├── knowledge.py      # 知识库
│   │   └── graph.py          # 任务编排
│   ├── api/                  # API服务
│   │   └── main.py          # FastAPI入口
│   ├── rtc/                  # 音视频
│   └── hardware/             # 硬件控制
├── c++/                       # C++底层
│   └── rtc-sdk/              # RTC SDK封装
├── config/                    # 配置文件
│   └── settings.yaml
├── docker/                    # Docker部署
└── requirements.txt
```

## 配置说明

### 火山引擎配置

编辑 `config/settings.yaml`:

```yaml
volcengine:
  app_id: "${VOLC_APP_ID}"
  token: "${VOLC_TOKEN}"
  api_key: "${COZE_API_KEY}"
  space_id: "${COZE_SPACE_ID}"
  
  rtc:
    app_id: "${RTC_APP_ID}"
    token: "${RTC_TOKEN}"
```

### AI Agent配置

```yaml
agent:
  conversation:
    max_history: 20
    system_prompt: |
      你是一个智能机器人控制系统助手...
  
  tools:
    web_search:
      enabled: true
    knowledge_base:
      enabled: true
    command_execution:
      enabled: true
      allowed_commands:
        - "ls"
        - "pwd"
        - "cat"
```

## 工具说明

### 1. web_search
搜索网络信息

**参数**:
- `query`: 搜索关键词
- `count`: 返回数量（默认5）

### 2. knowledge_search
检索知识库

**参数**:
- `query`: 查询内容
- `top_k`: 返回数量（默认3）

### 3. execute_command
执行系统命令

**参数**:
- `command`: 命令字符串

**注意**: 危险命令被禁止执行

### 4. hardware_control
控制机器人硬件

**参数**:
- `action`: 动作类型
  - `move_forward`: 前进
  - `move_backward`: 后退
  - `turn_left`: 左转
  - `turn_right`: 右转
  - `arm_up`: 机械臂上升
  - `arm_down`: 机械臂下降
  - `stop`: 停止
- `parameter`: 动作参数

### 5. calculator
数学计算

**参数**:
- `expression`: 数学表达式

### 6. get_time
获取当前时间

**参数**: 无

## 开发指南

### 添加新工具

1. 在 `agent/tools.py` 中定义工具处理器
2. 在 `ToolManager._register_default_tools()` 中注册工具
3. 工具将自动出现在API列表中

### 扩展Agent能力

1. 修改 `agent/graph.py` 中的节点实现
2. 添加新的路由逻辑
3. 更新状态定义

### 集成RTC SDK

1. 编译C++ RTC SDK
2. 使用ctypes或cffi封装
3. 在 `python/rtc/` 中集成

## Docker部署

```bash
# 构建镜像
docker build -t robot-control:latest -f docker/Dockerfile .

# 运行容器
docker run -d \
  --privileged \
  --network host \
  -v /dev:/dev \
  -e VOLC_APP_ID="your-app-id" \
  -e VOLC_TOKEN="your-token" \
  -e COZE_API_KEY="your-api-key" \
  robot-control:latest
```

## 性能优化

### 1. 向量数据库
- 使用Faiss加速检索
- 定期更新索引

### 2. 缓存策略
- 对话历史缓存
- 知识库结果缓存
- API响应缓存

### 3. 并发处理
- 工具并行执行
- 异步I/O
- 连接池管理

## 常见问题

### Q: 如何添加自定义知识？
```bash
POST /api/knowledge/add
{
  "content": "机器人的使用说明...",
  "metadata": {
    "category": "manual",
    "version": "1.0"
  }
}
```

### Q: 如何禁用某些工具？
```bash
POST /api/tools/disable
{
  "tool_name": "command_execution"
}
```

### Q: 如何查看系统状态？
```bash
GET /api/health
GET /api/knowledge/stats
GET /api/tools
```

## 许可证

MIT License

## 联系方式

技术支持：[火山引擎官网](https://www.volcengine.com/)
