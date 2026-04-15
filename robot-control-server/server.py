"""
Robot Control Server - 机器人控制服务端
用于火山引擎AI音视频互动方案的Function Calling接口

此服务接收火山引擎AI服务端的Function Calling请求，
执行机器人控制命令，并返回执行结果。
"""

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from loguru import logger
import asyncio
import uuid

# 导入工具模块
from tools.robot import RobotController
from tools.knowledge import KnowledgeBase
from tools.search import WebSearchTool
from utils.config import Config
from utils.logging import setup_logger

# 初始化配置和日志
config = Config()
logger = setup_logger()

# FastAPI应用
app = FastAPI(
    title="Robot Control Server",
    description="火山引擎AI音视频互动方案 - 机器人控制服务端",
    version="1.0.0"
)

# 全局实例
robot_controller: Optional[RobotController] = None
knowledge_base: Optional[KnowledgeBase] = None
web_search: Optional[WebSearchTool] = None


# ========== 数据模型 ==========

class FunctionCallRequest(BaseModel):
    """火山引擎Function Calling请求"""
    TaskId: str = Field(..., description="任务ID")
    RoomId: str = Field(..., description="房间ID")
    ToolCallId: str = Field(..., description="工具调用ID")
    FunctionName: str = Field(..., description="函数名称")
    Arguments: Dict[str, Any] = Field(default_factory=dict, description="函数参数")
    Timestamp: int = Field(..., description="时间戳")


class FunctionCallResponse(BaseModel):
    """Function Calling响应"""
    ToolCallId: str
    Result: str
    Success: bool = True
    Error: Optional[str] = None


class StatusCallbackRequest(BaseModel):
    """状态回调请求"""
    TaskId: str
    Event: str
    Data: Dict[str, Any]
    Timestamp: int


# ========== 工具注册 ==========

class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        
        # 1. 机器人控制工具
        self.tools["robot_control"] = {
            "name": "robot_control",
            "description": "控制机器人执行各种动作，如移动、转向、机械臂控制等",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "move_forward", "move_backward", "turn_left", "turn_right",
                            "arm_up", "arm_down", "grip_open", "grip_close",
                            "head_up", "head_down", "head_left", "head_right",
                            "led_on", "led_off", "stop"
                        ],
                        "description": "机器人动作"
                    },
                    "parameter": {
                        "type": "number",
                        "description": "动作参数（如距离米数、角度等）",
                        "default": 1.0
                    }
                },
                "required": ["action"]
            }
        }
        
        # 2. 状态查询工具
        self.tools["get_robot_status"] = {
            "name": "get_robot_status",
            "description": "查询机器人当前状态，包括位置、电量、传感器数据等",
            "parameters": {
                "type": "object",
                "properties": {
                    "status_type": {
                        "type": "string",
                        "enum": ["all", "location", "battery", "sensors", "motors"],
                        "description": "查询的状态类型",
                        "default": "all"
                    }
                }
            }
        }
        
        # 3. 知识库检索工具
        self.tools["search_knowledge"] = {
            "name": "search_knowledge",
            "description": "检索机器人知识库，查询产品规格、使用说明、技术文档等",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "查询内容"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
        
        # 4. 网页搜索工具
        self.tools["web_search"] = {
            "name": "web_search",
            "description": "搜索网络信息，查询最新新闻、天气、股票等实时信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "count": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
        
        # 5. 系统命令工具
        self.tools["execute_command"] = {
            "name": "execute_command",
            "description": "执行Linux系统命令，用于查询系统信息、文件操作等",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的命令"
                    }
                },
                "required": ["command"]
            }
        }
        
        logger.info(f"Registered {len(self.tools)} tools")
    
    def get_tool(self, name: str) -> Optional[Dict]:
        """获取工具定义"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> List[Dict]:
        """获取所有工具定义"""
        return list(self.tools.values())
    
    def execute(self, name: str, arguments: Dict[str, Any]) -> str:
        """执行工具"""
        if name == "robot_control":
            return self._execute_robot_control(arguments)
        elif name == "get_robot_status":
            return self._execute_get_status(arguments)
        elif name == "search_knowledge":
            return self._execute_search_knowledge(arguments)
        elif name == "web_search":
            return self._execute_web_search(arguments)
        elif name == "execute_command":
            return self._execute_command(arguments)
        else:
            return f"Unknown tool: {name}"
    
    def _execute_robot_control(self, args: Dict[str, Any]) -> str:
        """执行机器人控制"""
        action = args.get("action")
        parameter = args.get("parameter", 1.0)
        
        if not robot_controller:
            return "机器人控制器未初始化"
        
        return robot_controller.execute_action(action, parameter)
    
    def _execute_get_status(self, args: Dict[str, Any]) -> str:
        """获取机器人状态"""
        status_type = args.get("status_type", "all")
        
        if not robot_controller:
            return "机器人控制器未初始化"
        
        return robot_controller.get_status(status_type)
    
    def _execute_search_knowledge(self, args: Dict[str, Any]) -> str:
        """搜索知识库"""
        query = args.get("query")
        top_k = args.get("top_k", 3)
        
        if not knowledge_base:
            return "知识库未初始化"
        
        return knowledge_base.search(query, top_k)
    
    def _execute_web_search(self, args: Dict[str, Any]) -> str:
        """执行网页搜索"""
        query = args.get("query")
        count = args.get("count", 5)
        
        if not web_search:
            return "搜索引擎未初始化"
        
        return web_search.search(query, count)
    
    def _execute_command(self, args: Dict[str, Any]) -> str:
        """执行系统命令"""
        import subprocess
        
        command = args.get("command", "")
        
        # 安全检查
        dangerous_commands = ["rm", "dd", "mkfs", "shutdown", "reboot", "init", ":(){:|:&};"]
        for cmd in dangerous_commands:
            if command.strip().startswith(cmd):
                return f"禁止执行危险命令: {cmd}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout or "命令执行成功"
            else:
                return f"命令执行失败: {result.stderr}"
        
        except subprocess.TimeoutExpired:
            return "命令执行超时"
        except Exception as e:
            return f"命令执行错误: {str(e)}"


# 全局工具注册表
tool_registry = ToolRegistry()


# ========== API路由 ==========

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Robot Control Server",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "robot_connected": robot_controller.is_connected() if robot_controller else False,
        "tools_count": len(tool_registry.get_all_tools())
    }


@app.get("/tools")
async def get_tools():
    """获取所有可用工具"""
    return {
        "success": True,
        "tools": tool_registry.get_all_tools()
    }


@app.post("/tools/call")
async def tool_call(request: FunctionCallRequest):
    """
    火山引擎Function Calling回调接口
    
    火山引擎AI服务在需要调用工具时会发送POST请求到此接口。
    """
    logger.info(f"Function call received: {request.FunctionName}")
    logger.debug(f"Arguments: {request.Arguments}")
    
    try:
        # 执行工具
        result = tool_registry.execute(
            request.FunctionName,
            request.Arguments
        )
        
        # 返回结果
        response = FunctionCallResponse(
            ToolCallId=request.ToolCallId,
            Result=result,
            Success=True
        )
        
        logger.info(f"Function {request.FunctionName} executed successfully")
        return response
    
    except Exception as e:
        logger.error(f"Function execution error: {e}")
        
        return FunctionCallResponse(
            ToolCallId=request.ToolCallId,
            Result=f"执行失败: {str(e)}",
            Success=False,
            Error=str(e)
        )


@app.post("/tools/call_batch")
async def tool_call_batch(requests: List[FunctionCallRequest]):
    """
    批量工具调用
    
    用于需要并行执行多个工具的场景。
    """
    results = []
    
    for request in requests:
        try:
            result = tool_registry.execute(
                request.FunctionName,
                request.Arguments
            )
            results.append({
                "ToolCallId": request.ToolCallId,
                "Result": result,
                "Success": True
            })
        except Exception as e:
            results.append({
                "ToolCallId": request.ToolCallId,
                "Result": f"执行失败: {str(e)}",
                "Success": False,
                "Error": str(e)
            })
    
    return {
        "success": True,
        "results": results
    }


@app.post("/status/callback")
async def status_callback(request: StatusCallbackRequest):
    """
    状态回调接口
    
    接收火山引擎AI服务的状态更新通知。
    """
    logger.info(f"Status callback: {request.Event}")
    logger.debug(f"Data: {request.Data}")
    
    # 处理各种状态事件
    if request.Event == "start":
        logger.info(f"Task {request.TaskId} started")
    
    elif request.Event == "asrResult":
        text = request.Data.get("text", "")
        logger.info(f"ASR Result: {text}")
    
    elif request.Event == "llmOutput":
        text = request.Data.get("text", "")
        logger.debug(f"LLM Output: {text}")
    
    elif request.Event == "answerStart":
        logger.info(f"AI started speaking for task {request.TaskId}")
    
    elif request.Event == "toolCall":
        tool_name = request.Data.get("tool_name", "")
        logger.info(f"Tool call triggered: {tool_name}")
    
    elif request.Event == "toolResult":
        tool_name = request.Data.get("tool_name", "")
        result = request.Data.get("result", "")
        logger.info(f"Tool {tool_name} result: {result}")
    
    elif request.Event == "interrupted":
        logger.warn(f"AI interrupted for task {request.TaskId}")
    
    elif request.Event == "end":
        logger.info(f"Task {request.TaskId} ended")
    
    return {
        "success": True,
        "received": True
    }


@app.post("/robot/control")
async def robot_control(action: str, parameter: float = 1.0):
    """
    直接控制机器人
    
    用于测试或直接API调用。
    """
    if not robot_controller:
        raise HTTPException(status_code=500, detail="机器人控制器未初始化")
    
    result = robot_controller.execute_action(action, parameter)
    return {
        "success": True,
        "action": action,
        "parameter": parameter,
        "result": result
    }


@app.get("/robot/status")
async def robot_status(status_type: str = "all"):
    """
    获取机器人状态
    """
    if not robot_controller:
        raise HTTPException(status_code=500, detail="机器人控制器未初始化")
    
    status = robot_controller.get_status(status_type)
    return {
        "success": True,
        "status": status
    }


@app.get("/knowledge/search")
async def knowledge_search(query: str, top_k: int = 3):
    """
    知识库检索
    """
    if not knowledge_base:
        raise HTTPException(status_code=500, detail="知识库未初始化")
    
    results = knowledge_base.search(query, top_k)
    return {
        "success": True,
        "query": query,
        "results": results
    }


@app.post("/knowledge/add")
async def knowledge_add(content: str, metadata: Dict[str, Any] = {}):
    """
    添加知识条目
    """
    if not knowledge_base:
        raise HTTPException(status_code=500, detail="知识库未初始化")
    
    item_id = knowledge_base.add(content, metadata)
    return {
        "success": True,
        "id": item_id
    }


@app.get("/knowledge/stats")
async def knowledge_stats():
    """获取知识库统计"""
    if not knowledge_base:
        raise HTTPException(status_code=500, detail="知识库未初始化")
    
    return {
        "success": True,
        "stats": knowledge_base.get_stats()
    }


# ========== 启动初始化 ==========

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    global robot_controller, knowledge_base, web_search
    
    logger.info("Initializing Robot Control Server...")
    
    # 初始化机器人控制器
    robot_controller = RobotController(
        serial_port=config.get("hardware.serial.port", "/dev/ttyUSB0"),
        baudrate=config.get("hardware.serial.baudrate", 115200)
    )
    
    # 初始化知识库
    knowledge_base = KnowledgeBase(
        persist_dir="/tmp/knowledge_db"
    )
    
    # 初始化搜索引擎
    web_search = WebSearchTool()
    
    logger.info("Robot Control Server initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    global robot_controller
    
    logger.info("Shutting down Robot Control Server...")
    
    if robot_controller:
        robot_controller.disconnect()
    
    logger.info("Robot Control Server shutdown complete")


# ========== 启动入口 ==========

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )
