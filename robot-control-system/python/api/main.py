"""
Robot Control System API
FastAPI Web服务入口
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
from loguru import logger
import json
import os

# 导入Agent模块
from agent import ChatManager, ToolManager, KnowledgeBase, AgentGraph


# ========== 全局实例 ==========

chat_manager: Optional[ChatManager] = None
tool_manager: Optional[ToolManager] = None
knowledge_base: Optional[KnowledgeBase] = None
agent_graph: Optional[AgentGraph] = None


# ========== 生命周期管理 ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global chat_manager, tool_manager, knowledge_base, agent_graph
    
    logger.info("Initializing Robot Control System...")
    
    # 初始化组件
    chat_manager = ChatManager(
        system_prompt="你是一个智能机器人控制助手。你可以帮助用户进行对话、搜索信息、执行命令、控制硬件等。",
        max_history=20
    )
    
    tool_manager = ToolManager()
    
    knowledge_base = KnowledgeBase(
        db_type="chroma",
        persist_directory="/tmp/vector_db",
        collection_name="robot_knowledge"
    )
    
    # 加载示例知识库
    await knowledge_base.load_sample_knowledge()
    
    agent_graph = AgentGraph(
        tool_manager=tool_manager,
        knowledge_base=knowledge_base,
        chat_manager=chat_manager
    )
    
    logger.info("Robot Control System initialized successfully")
    
    yield
    
    logger.info("Shutting down Robot Control System...")


# ========== FastAPI应用 ==========

app = FastAPI(
    title="Robot Control System API",
    description="火山引擎AI音视频互动方案 - 机器人控制系统API",
    version="1.0.0",
    lifespan=lifespan
)


# ========== 请求/响应模型 ==========

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., description="用户消息")
    conversation_id: str = Field(default="default", description="对话ID")
    stream: bool = Field(default=True, description="是否流式响应")


class ChatResponse(BaseModel):
    """聊天响应"""
    success: bool
    response: str
    conversation_id: str
    intent: Optional[str] = None
    tools_used: List[str] = []
    timestamp: str


class ToolCallRequest(BaseModel):
    """工具调用请求"""
    tool_name: str = Field(..., description="工具名称")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="工具参数")


class KnowledgeAddRequest(BaseModel):
    """知识添加请求"""
    content: str = Field(..., description="知识内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class HardwareControlRequest(BaseModel):
    """硬件控制请求"""
    action: str = Field(..., description="控制动作")
    parameter: float = Field(default=1.0, description="动作参数")


# ========== API路由 ==========

@app.get("/", response_class=HTMLResponse)
async def root():
    """Web界面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robot Control System</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .info {
                background: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .endpoints {
                list-style: none;
                padding: 0;
            }
            .endpoints li {
                padding: 10px;
                margin: 5px 0;
                background: #e8e8e8;
                border-radius: 5px;
            }
            code {
                background: #333;
                color: #fff;
                padding: 2px 6px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Robot Control System</h1>
            <div class="info">
                <strong>火山引擎AI音视频互动方案 - 机器人控制系统</strong>
                <p>基于豆包大模型的智能机器人控制系统，支持对话、搜索、工具调用、知识库检索等功能。</p>
            </div>
            <h2>API端点</h2>
            <ul class="endpoints">
                <li><code>POST /api/chat</code> - 对话接口</li>
                <li><code>WebSocket /ws/chat</code> - WebSocket实时对话</li>
                <li><code>POST /api/tools/call</code> - 工具调用</li>
                <li><code>GET /api/tools</code> - 获取可用工具列表</li>
                <li><code>POST /api/knowledge/add</code> - 添加知识</li>
                <li><code>POST /api/knowledge/search</code> - 知识检索</li>
                <li><code>GET /api/health</code> - 健康检查</li>
            </ul>
            <div class="info">
                <strong>使用示例：</strong>
                <pre>
curl -X POST http://localhost:5000/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "你好", "conversation_id": "test"}'
                </pre>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """对话接口"""
    try:
        result = await agent_graph.process(
            user_input=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            success=result['success'],
            response=result['response'],
            conversation_id=request.conversation_id,
            intent=result.get('intent'),
            tools_used=result.get('tools_used', []),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式对话接口（Server-Sent Events）"""
    from sse_starlette.sse import EventSourceResponse
    
    async def event_generator():
        try:
            async for chunk in agent_graph.process_stream(
                user_input=request.message,
                conversation_id=request.conversation_id
            ):
                yield {
                    "event": "message",
                    "data": json.dumps({
                        "chunk": chunk,
                        "timestamp": datetime.now().isoformat()
                    })
                }
            
            # 发送完成信号
            yield {
                "event": "done",
                "data": json.dumps({
                    "timestamp": datetime.now().isoformat()
                })
            }
        
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket connected: {client_id}")
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"WebSocket disconnected: {client_id}")
    
    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """WebSocket实时对话"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message = message_data.get('message', '')
            conversation_id = message_data.get('conversation_id', client_id)
            
            if not message:
                continue
            
            # 处理消息
            if message_data.get('stream', True):
                # 流式响应
                await websocket.send_json({
                    'type': 'start',
                    'timestamp': datetime.now().isoformat()
                })
                
                full_response = ""
                async for chunk in agent_graph.process_stream(
                    user_input=message,
                    conversation_id=conversation_id
                ):
                    full_response += chunk
                    await websocket.send_json({
                        'type': 'chunk',
                        'data': chunk,
                        'timestamp': datetime.now().isoformat()
                    })
                
                await websocket.send_json({
                    'type': 'done',
                    'data': full_response,
                    'timestamp': datetime.now().isoformat()
                })
            
            else:
                # 非流式响应
                result = await agent_graph.process(
                    user_input=message,
                    conversation_id=conversation_id
                )
                
                await websocket.send_json({
                    'type': 'response',
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(client_id)


@app.get("/api/tools")
async def get_tools():
    """获取可用工具列表"""
    tools = tool_manager.get_all_tools()
    return {
        "success": True,
        "tools": tools,
        "count": len(tools)
    }


@app.post("/api/tools/call")
async def call_tool(request: ToolCallRequest):
    """调用指定工具"""
    from agent.tools import ToolExecutor
    
    executor = ToolExecutor(tool_manager)
    
    try:
        result = await executor.execute_tool(
            request.tool_name,
            request.parameters
        )
        
        return {
            "success": True,
            "tool": request.tool_name,
            "result": result
        }
    
    except Exception as e:
        logger.error(f"Tool call error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/add")
async def add_knowledge(request: KnowledgeAddRequest):
    """添加知识条目"""
    try:
        item_id = await knowledge_base.add_knowledge(
            content=request.content,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "id": item_id
        }
    
    except Exception as e:
        logger.error(f"Knowledge add error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/search")
async def search_knowledge(
    query: str,
    top_k: int = 3
):
    """检索知识"""
    try:
        results = await knowledge_base.search(
            query=query,
            top_k=top_k
        )
        
        return {
            "success": True,
            "query": query,
            "results": [item.to_dict() for item in results],
            "count": len(results)
        }
    
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge/stats")
async def get_knowledge_stats():
    """获取知识库统计"""
    stats = knowledge_base.get_statistics()
    return {
        "success": True,
        "statistics": stats
    }


@app.post("/api/hardware/control")
async def hardware_control(request: HardwareControlRequest):
    """硬件控制接口"""
    from agent.tools import ToolExecutor
    
    executor = ToolExecutor(tool_manager)
    
    try:
        result = await executor.execute_tool(
            'hardware_control',
            {
                'action': request.action,
                'parameter': request.parameter
            }
        )
        
        return {
            "success": True,
            "action": request.action,
            "result": result
        }
    
    except Exception as e:
        logger.error(f"Hardware control error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """获取对话历史"""
    history = chat_manager.get_conversation_history(conversation_id)
    summary = chat_manager.get_conversation_summary(conversation_id)
    
    return {
        "success": True,
        "conversation_id": conversation_id,
        "messages": history,
        "summary": summary
    }


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """删除对话"""
    chat_manager.delete_conversation(conversation_id)
    
    return {
        "success": True,
        "message": f"Conversation {conversation_id} deleted"
    }


if __name__ == "__main__":
    import uvicorn
    
    # 配置日志
    logger.add(
        "/tmp/robot_control.log",
        rotation="100 MB",
        retention="7 days",
        level="INFO"
    )
    
    # 启动服务
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info"
    )
