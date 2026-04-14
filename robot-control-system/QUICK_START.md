# Robot Control System - 快速开始指南

## 1. 项目概述

这是一个基于火山引擎豆包大模型的智能机器人控制系统，实现了以下核心功能：

- 🤖 **智能对话**：基于豆包大模型的自然语言交互
- 🔍 **网页搜索**：实时网络信息查询
- 📚 **知识库检索**：私有知识库问答
- 🔧 **工具调用**：系统命令执行、数学计算等
- 📹 **音视频互动**：火山引擎RTC集成（可选）
- 🤖 **硬件控制**：机器人运动控制（预留接口）

## 2. 快速开始

### 方式一：Docker部署（推荐）

```bash
# 进入docker目录
cd robot-control-system/docker

# 初始化项目
chmod +x deploy.sh
./deploy.sh init

# 编辑配置文件
vim .env  # 填入您的火山引擎配置

# 构建镜像
./deploy.sh build

# 启动服务
./deploy.sh start

# 查看状态
./deploy.sh status

# 查看日志
./deploy.sh logs
```

### 方式二：直接运行

```bash
# 进入项目目录
cd robot-control-system

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export VOLC_APP_ID="your-app-id"
export VOLC_TOKEN="your-token"
export COZE_API_KEY="your-api-key"

# 启动服务
cd python
python -m api.main
```

## 3. 访问系统

服务启动后，访问以下地址：

- **Web界面**：http://localhost:5000
- **API文档**：http://localhost:5000/docs
- **健康检查**：http://localhost:5000/api/health

## 4. 基本使用

### 4.1 Web界面使用

1. 打开浏览器访问 http://localhost:5000
2. 在输入框中输入问题或指令
3. 点击发送按钮或按回车
4. 系统会智能识别意图并调用相应工具

### 4.2 API调用示例

#### 对话接口

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "conversation_id": "test"
  }'
```

#### 工具调用

```bash
# 获取当前时间
curl -X POST http://localhost:5000/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_time",
    "parameters": {}
  }'

# 数学计算
curl -X POST http://localhost:5000/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "calculator",
    "parameters": {"expression": "100+200"}
  }'
```

#### 知识库检索

```bash
# 添加知识
curl -X POST http://localhost:5000/api/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "content": "机器人的前进命令是 move_forward",
    "metadata": {"category": "command"}
  }'

# 检索知识
curl -X POST "http://localhost:5000/api/knowledge/search?query=机器人&top_k=3"
```

#### 硬件控制

```bash
curl -X POST http://localhost:5000/api/hardware/control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "move_forward",
    "parameter": 1.0
  }'
```

### 4.3 WebSocket实时对话

```javascript
// 连接WebSocket
const ws = new WebSocket('ws://localhost:5000/ws/chat/client_001');

// 发送消息
ws.send(JSON.stringify({
    message: '你好',
    conversation_id: 'test',
    stream: true
}));

// 接收消息
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(data);
};
```

## 5. 配置说明

### 5.1 火山引擎配置

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 创建应用，获取 AppID 和 Token
3. 获取 API Key
4. 配置到环境变量或 `.env` 文件

### 5.2 RTC配置（可选）

如需启用音视频功能：

1. 在火山引擎控制台开通 RTC 服务
2. 获取 RTC AppID 和 Token
3. 配置到环境变量
4. 确保Linux系统已安装音视频依赖：
   ```bash
   sudo apt install libgl-dev libpulse-dev libva2
   ```

### 5.3 硬件配置

编辑 `config/settings.yaml`：

```yaml
hardware:
  serial:
    enabled: true
    port: "/dev/ttyUSB0"
    baudrate: 115200
```

## 6. 功能测试

### 6.1 运行单元测试

```bash
cd robot-control-system/python
python test_system.py
```

### 6.2 API测试

```bash
# 健康检查
curl http://localhost:5000/api/health

# 获取工具列表
curl http://localhost:5000/api/tools

# 知识库统计
curl http://localhost:5000/api/knowledge/stats
```

## 7. 扩展开发

### 7.1 添加自定义工具

编辑 `python/agent/tools.py`：

```python
@self.register_tool
def my_custom_tool(self, param1: str, param2: int):
    """自定义工具描述"""
    # 工具实现
    return f"处理结果: {param1}, {param2}"
```

### 7.2 扩展Agent能力

编辑 `python/agent/graph.py`，添加新的节点和边。

### 7.3 集成RTC SDK

1. 编译C++ RTC SDK
2. 使用ctypes封装
3. 在 `python/rtc/` 中集成

## 8. 故障排查

### 8.1 服务无法启动

```bash
# 查看日志
docker-compose logs robot-control

# 检查端口占用
netstat -tulpn | grep 5000

# 检查配置
cat .env
```

### 8.2 API调用失败

```bash
# 检查健康状态
curl http://localhost:5000/api/health

# 查看详细日志
docker-compose logs --tail=100 robot-control
```

### 8.3 知识库检索不准确

```bash
# 清空知识库
curl -X DELETE http://localhost:5000/api/knowledge/clear

# 重新添加知识
```

## 9. 性能优化

### 9.1 使用生产级WSGI服务器

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 api.main:app
```

### 9.2 启用缓存

编辑 `config/settings.yaml`：

```yaml
cache:
  enabled: true
  type: "redis"
  host: "localhost"
  port: 6379
```

### 9.3 数据库优化

- 使用PostgreSQL替代SQLite
- 配置向量数据库索引
- 启用查询缓存

## 10. 安全建议

1. **API密钥保护**：不要将密钥提交到代码仓库
2. **网络隔离**：生产环境使用VPN或内网访问
3. **命令执行限制**：严格限制可执行的系统命令
4. **硬件操作权限**：最小化硬件控制权限
5. **日志脱敏**：生产环境关闭敏感信息日志

## 11. 常见问题

**Q: 如何查看系统支持哪些工具？**
A: 访问 `GET /api/tools` 接口

**Q: 能否离线使用？**
A: 可以，但部分功能（如网页搜索）需要网络

**Q: 如何添加新的对话主题？**
A: 向知识库添加相关文档

**Q: 支持多机器人控制吗？**
A: 支持，每个机器人使用不同的 conversation_id

## 12. 技术支持

- 文档：查看 README.md
- 问题反馈：提交 Issue
- 社区支持：加入开发者群

---

快速开始指南完成！如有问题，请查阅详细文档或联系技术支持。
