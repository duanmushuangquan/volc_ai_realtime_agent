"""
Tool Manager - 工具管理器
定义和管理AI Agent可调用的工具
"""

import asyncio
import subprocess
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger
import json


class ToolType(Enum):
    """工具类型"""
    WEB_SEARCH = "web_search"
    KNOWLEDGE_BASE = "knowledge_base"
    COMMAND_EXECUTION = "command_execution"
    FILE_OPERATIONS = "file_operations"
    HARDWARE_CONTROL = "hardware_control"
    CALCULATOR = "calculator"
    TIME = "time"
    CUSTOM = "custom"


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    tool_type: ToolType
    parameters: Dict[str, Any]
    handler: Callable
    enabled: bool = True
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }


class ToolManager:
    """
    工具管理器
    
    负责：
    1. 注册工具
    2. 管理工具启停
    3. 提供工具列表
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
        logger.info(f"ToolManager initialized with {len(self.tools)} tools")
    
    def _register_default_tools(self):
        """注册默认工具"""
        # 网页搜索工具
        self.register_tool(Tool(
            name="web_search",
            description="搜索网络信息。当需要查询最新新闻、天气、股票等信息时使用。",
            tool_type=ToolType.WEB_SEARCH,
            parameters={
                'query': {
                    'type': 'string',
                    'description': '搜索查询内容',
                    'required': True
                },
                'count': {
                    'type': 'integer',
                    'description': '返回结果数量',
                    'default': 5
                }
            },
            handler=self._web_search_handler,
            enabled=True
        ))
        
        # 知识库检索工具
        self.register_tool(Tool(
            name="knowledge_search",
            description="搜索机器人知识库。用于查询产品规格、使用说明、技术文档等。",
            tool_type=ToolType.KNOWLEDGE_BASE,
            parameters={
                'query': {
                    'type': 'string',
                    'description': '知识库查询内容',
                    'required': True
                },
                'top_k': {
                    'type': 'integer',
                    'description': '返回最相关的条目数',
                    'default': 3
                }
            },
            handler=self._knowledge_search_handler,
            enabled=True
        ))
        
        # 系统命令执行工具
        self.register_tool(Tool(
            name="execute_command",
            description="执行Linux系统命令。用于文件操作、系统信息查询等。",
            tool_type=ToolType.COMMAND_EXECUTION,
            parameters={
                'command': {
                    'type': 'string',
                    'description': '要执行的命令',
                    'required': True
                }
            },
            handler=self._execute_command_handler,
            enabled=True
        ))
        
        # 计算器工具
        self.register_tool(Tool(
            name="calculator",
            description="执行数学计算。用于算术运算、函数计算等。",
            tool_type=ToolType.CALCULATOR,
            parameters={
                'expression': {
                    'type': 'string',
                    'description': '数学表达式',
                    'required': True
                }
            },
            handler=self._calculator_handler,
            enabled=True
        ))
        
        # 时间工具
        self.register_tool(Tool(
            name="get_time",
            description="获取当前时间和日期。",
            tool_type=ToolType.TIME,
            parameters={},
            handler=self._get_time_handler,
            enabled=True
        ))
        
        # 硬件控制工具
        self.register_tool(Tool(
            name="hardware_control",
            description="控制机器人硬件，如移动、转向、抬起机械臂等。",
            tool_type=ToolType.HARDWARE_CONTROL,
            parameters={
                'action': {
                    'type': 'string',
                    'description': '控制动作',
                    'enum': ['move_forward', 'move_backward', 'turn_left', 'turn_right', 
                            'arm_up', 'arm_down', 'grip_open', 'grip_close', 'stop'],
                    'required': True
                },
                'parameter': {
                    'type': 'number',
                    'description': '动作参数（如距离、角度）',
                    'default': 1.0
                }
            },
            handler=self._hardware_control_handler,
            enabled=False  # 默认禁用，需要配置硬件
        ))
    
    def register_tool(self, tool: Tool) -> None:
        """注册工具"""
        self.tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")
    
    def unregister_tool(self, tool_name: str) -> bool:
        """注销工具"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.debug(f"Unregistered tool: {tool_name}")
            return True
        return False
    
    def enable_tool(self, tool_name: str) -> bool:
        """启用工具"""
        if tool_name in self.tools:
            self.tools[tool_name].enabled = True
            logger.info(f"Enabled tool: {tool_name}")
            return True
        return False
    
    def disable_tool(self, tool_name: str) -> bool:
        """禁用工具"""
        if tool_name in self.tools:
            self.tools[tool_name].enabled = False
            logger.info(f"Disabled tool: {tool_name}")
            return True
        return False
    
    def get_enabled_tools(self) -> List[Tool]:
        """获取所有已启用的工具"""
        return [tool for tool in self.tools.values() if tool.enabled]
    
    def get_all_tools(self) -> List[Dict]:
        """获取所有工具列表（用于Agent）"""
        return [tool.to_dict() for tool in self.tools.values() if tool.enabled]
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """获取指定工具"""
        return self.tools.get(tool_name)
    
    # ========== 工具处理器 ==========
    
    async def _web_search_handler(self, query: str, count: int = 5) -> str:
        """网页搜索处理器"""
        try:
            from coze_coding_dev_sdk import SearchClient
            client = SearchClient()
            
            response = client.web_search(
                query=query,
                count=count,
                need_summary=True
            )
            
            if response.web_items:
                results = []
                for i, item in enumerate(response.web_items, 1):
                    results.append(f"{i}. {item.title}\n   {item.summary}\n   来源: {item.site_name}")
                return "\n\n".join(results)
            else:
                return "未找到相关搜索结果"
        
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return f"搜索失败: {str(e)}"
    
    async def _knowledge_search_handler(self, query: str, top_k: int = 3) -> str:
        """知识库检索处理器"""
        # 模拟知识库检索
        # 实际实现需要连接向量数据库
        return f"知识库检索结果（关键词: {query}，返回top-{top_k}）：\n\n根据您的查询'{query}'，在知识库中找到以下相关内容..."
    
    async def _execute_command_handler(self, command: str) -> str:
        """系统命令执行处理器"""
        # 安全检查
        dangerous_commands = ['rm', 'dd', 'mkfs', ':(){:|:&};:', 'shutdown', 'reboot', 'init']
        
        for dangerous in dangerous_commands:
            if command.strip().startswith(dangerous):
                return f"禁止执行危险命令: {dangerous}"
        
        try:
            # 设置超时
            result = await asyncio.wait_for(
                asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                ),
                timeout=10.0
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return stdout.decode('utf-8', errors='ignore') or "命令执行成功"
            else:
                return f"命令执行失败:\n{stderr.decode('utf-8', errors='ignore')}"
        
        except asyncio.TimeoutError:
            return "命令执行超时（超过10秒）"
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return f"命令执行错误: {str(e)}"
    
    async def _calculator_handler(self, expression: str) -> str:
        """计算器处理器"""
        try:
            # 安全检查：只允许数学运算
            allowed_chars = set('0123456789+-*/().%^ ')
            if not all(c in allowed_chars for c in expression):
                return "计算表达式包含非法字符"
            
            result = eval(expression)
            return f"计算结果: {result}"
        
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    async def _get_time_handler(self) -> str:
        """时间工具处理器"""
        from datetime import datetime
        now = datetime.now()
        return f"当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}\n星期: {['一','二','三','四','五','六','日'][now.weekday()]}"
    
    async def _hardware_control_handler(
        self,
        action: str,
        parameter: float = 1.0
    ) -> str:
        """硬件控制处理器"""
        # 实际实现需要调用底层C++接口
        logger.info(f"Hardware control: {action} with parameter {parameter}")
        return f"硬件动作 '{action}' 已发送（参数: {parameter}）"


class ToolExecutor:
    """
    工具执行器
    
    负责执行工具调用
    """
    
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> str:
        """执行工具"""
        tool = self.tool_manager.get_tool(tool_name)
        
        if not tool:
            return f"工具不存在: {tool_name}"
        
        if not tool.enabled:
            return f"工具已禁用: {tool_name}"
        
        try:
            logger.info(f"Executing tool: {tool_name} with params: {parameters}")
            
            # 调用工具处理器
            result = await tool.handler(**parameters)
            return result
        
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"工具执行失败: {str(e)}"
    
    async def execute_tools_parallel(
        self,
        tool_calls: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """并行执行多个工具"""
        tasks = []
        
        for call in tool_calls:
            tool_name = call.get('name')
            parameters = call.get('parameters', {})
            task = self.execute_tool(tool_name, parameters)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            {
                'tool': call.get('name'),
                'result': str(result) if isinstance(result, Exception) else result,
                'success': not isinstance(result, Exception)
            }
            for call, result in zip(tool_calls, results)
        ]
