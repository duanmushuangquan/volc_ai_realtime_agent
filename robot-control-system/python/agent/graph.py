"""
Agent Graph - 任务编排图
使用LangGraph实现复杂任务的编排和执行
"""

from typing import Dict, List, Any, TypedDict, Optional, Literal, Annotated
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import json


class AgentState(TypedDict):
    """Agent状态"""
    messages: List[Dict[str, Any]]  # 对话历史
    intent: Optional[str]  # 识别到的意图
    tools_to_use: List[Dict[str, Any]]  # 需要调用的工具
    tool_results: List[Dict[str, Any]]  # 工具执行结果
    current_step: str  # 当前步骤
    memory: Dict[str, Any]  # 记忆数据


class AgentNode(Enum):
    """Agent节点"""
    INTENT_DETECTION = "intent_detection"
    TOOL_PLANNING = "tool_planning"
    TOOL_EXECUTION = "tool_execution"
    RESPONSE_SYNTHESIS = "response_synthesis"
    END = "end"


class AgentGraph:
    """
    Agent任务编排图
    
    使用LangGraph实现以下流程：
    1. 意图检测 -> 判断用户意图
    2. 工具规划 -> 选择合适的工具
    3. 工具执行 -> 执行选定的工具
    4. 响应综合 -> 汇总结果生成响应
    """
    
    def __init__(
        self,
        llm_client=None,  # 大模型客户端
        tool_manager=None,  # 工具管理器
        knowledge_base=None,  # 知识库
        chat_manager=None  # 对话管理器
    ):
        self.llm_client = llm_client
        self.tool_manager = tool_manager
        self.knowledge_base = knowledge_base
        self.chat_manager = chat_manager
        
        # 节点映射
        self.nodes = {
            AgentNode.INTENT_DETECTION: self._intent_detection_node,
            AgentNode.TOOL_PLANNING: self._tool_planning_node,
            AgentNode.TOOL_EXECUTION: self._tool_execution_node,
            AgentNode.RESPONSE_SYNTHESIS: self._response_synthesis_node,
        }
        
        # 边映射
        self.edges = {
            AgentNode.INTENT_DETECTION: self._intent_detection_edge,
            AgentNode.TOOL_PLANNING: self._tool_planning_edge,
            AgentNode.TOOL_EXECUTION: self._tool_execution_edge,
        }
        
        logger.info("AgentGraph initialized")
    
    async def process(
        self,
        user_input: str,
        conversation_id: str = "default",
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
            conversation_id: 对话ID
            context: 额外上下文
        
        Returns:
            处理结果
        """
        # 初始化状态
        state = AgentState(
            messages=[{
                'role': 'user',
                'content': user_input,
                'timestamp': self._get_timestamp()
            }],
            intent=None,
            tools_to_use=[],
            tool_results=[],
            current_step=AgentNode.INTENT_DETECTION.value,
            memory=context or {}
        )
        
        try:
            # 步骤1：意图检测
            state = await self._intent_detection_node(state)
            
            # 步骤2：工具规划（如果需要）
            if state['tools_to_use']:
                state = await self._tool_planning_node(state)
                
                # 步骤3：工具执行
                state = await self._tool_execution_node(state)
            
            # 步骤4：响应综合
            state = await self._response_synthesis_node(state)
            
            # 添加助手消息到对话历史
            if self.chat_manager:
                self.chat_manager.add_message(
                    conversation_id,
                    'assistant',
                    state['messages'][-1]['content'],
                    metadata={'intent': state['intent']}
                )
            
            return {
                'success': True,
                'response': state['messages'][-1]['content'],
                'intent': state['intent'],
                'tools_used': [t['name'] for t in state['tools_to_use']],
                'tool_results': state['tool_results']
            }
        
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': f"处理您的请求时出现错误: {str(e)}"
            }
    
    async def process_stream(
        self,
        user_input: str,
        conversation_id: str = "default"
    ):
        """
        流式处理用户输入
        
        Yields:
            响应片段
        """
        result = await self.process(user_input, conversation_id)
        
        if result['success']:
            response = result['response']
            # 模拟流式输出
            for i in range(0, len(response), 50):
                yield response[i:i+50]
                await self._async_sleep(0.05)
        else:
            yield result['response']
    
    # ========== 节点实现 ==========
    
    async def _intent_detection_node(self, state: AgentState) -> AgentState:
        """意图检测节点"""
        user_input = state['messages'][-1]['content']
        
        logger.debug(f"Intent detection: {user_input[:50]}...")
        
        # 简化的意图检测逻辑
        # 实际应使用LLM进行意图识别
        
        intent_keywords = {
            'search': ['搜索', '查询', '查找', '什么', '最新'],
            'knowledge': ['知识库', '文档', '手册', '说明'],
            'command': ['执行', '运行', '命令', '打开', '关闭'],
            'hardware': ['移动', '转向', '机械臂', '控制'],
            'calculation': ['计算', '多少', '+', '-', '*', '/'],
            'time': ['时间', '几点', '日期', '今天']
        }
        
        detected_intent = 'general'
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                detected_intent = intent
                break
        
        state['intent'] = detected_intent
        state['current_step'] = AgentNode.TOOL_PLANNING.value
        
        logger.debug(f"Detected intent: {detected_intent}")
        return state
    
    async def _tool_planning_node(self, state: AgentState) -> AgentState:
        """工具规划节点"""
        intent = state['intent']
        user_input = state['messages'][-1]['content']
        
        logger.debug(f"Tool planning for intent: {intent}")
        
        # 根据意图选择工具
        tools_to_use = []
        
        if intent == 'search':
            tools_to_use.append({
                'name': 'web_search',
                'parameters': {
                    'query': user_input,
                    'count': 5
                }
            })
        
        elif intent == 'knowledge':
            tools_to_use.append({
                'name': 'knowledge_search',
                'parameters': {
                    'query': user_input,
                    'top_k': 3
                }
            })
        
        elif intent == 'command':
            # 提取命令
            command = user_input.replace('执行', '').replace('运行', '').strip()
            tools_to_use.append({
                'name': 'execute_command',
                'parameters': {
                    'command': command
                }
            })
        
        elif intent == 'hardware':
            # 解析硬件控制命令
            action = 'stop'
            if '向前' in user_input or '前进' in user_input:
                action = 'move_forward'
            elif '向后' in user_input or '后退' in user_input:
                action = 'move_backward'
            elif '左转' in user_input:
                action = 'turn_left'
            elif '右转' in user_input:
                action = 'turn_right'
            
            tools_to_use.append({
                'name': 'hardware_control',
                'parameters': {
                    'action': action,
                    'parameter': 1.0
                }
            })
        
        elif intent == 'calculation':
            # 提取数学表达式
            import re
            expression = re.search(r'[\d+\-*/().%\s]+', user_input)
            if expression:
                tools_to_use.append({
                    'name': 'calculator',
                    'parameters': {
                        'expression': expression.group().strip()
                    }
                })
        
        elif intent == 'time':
            tools_to_use.append({
                'name': 'get_time',
                'parameters': {}
            })
        
        state['tools_to_use'] = tools_to_use
        state['current_step'] = AgentNode.TOOL_EXECUTION.value
        
        logger.debug(f"Planned tools: {[t['name'] for t in tools_to_use]}")
        return state
    
    async def _tool_execution_node(self, state: AgentState) -> AgentState:
        """工具执行节点"""
        from .tools import ToolExecutor
        
        if not self.tool_manager:
            logger.warning("No tool manager available")
            return state
        
        executor = ToolExecutor(self.tool_manager)
        
        tool_results = []
        
        for tool_call in state['tools_to_use']:
            tool_name = tool_call['name']
            parameters = tool_call['parameters']
            
            try:
                result = await executor.execute_tool(tool_name, parameters)
                tool_results.append({
                    'tool': tool_name,
                    'result': result,
                    'success': True
                })
                logger.debug(f"Tool {tool_name} executed successfully")
            
            except Exception as e:
                tool_results.append({
                    'tool': tool_name,
                    'result': str(e),
                    'success': False
                })
                logger.error(f"Tool {tool_name} execution failed: {e}")
        
        state['tool_results'] = tool_results
        state['current_step'] = AgentNode.RESPONSE_SYNTHESIS.value
        
        return state
    
    async def _response_synthesis_node(self, state: AgentState) -> AgentState:
        """响应综合节点"""
        intent = state['intent']
        tool_results = state['tool_results']
        
        logger.debug("Synthesizing response")
        
        # 简单响应综合
        if tool_results:
            response_parts = []
            
            for result in tool_results:
                if result['success']:
                    response_parts.append(result['result'])
                else:
                    response_parts.append(f"工具{result['tool']}执行失败")
            
            response = "\n".join(response_parts)
        else:
            # 无工具调用，直接回复
            response = self._generate_direct_response(intent, state['messages'][-1]['content'])
        
        state['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': self._get_timestamp()
        })
        
        return state
    
    # ========== 边实现（路由逻辑） ==========
    
    def _intent_detection_edge(self, state: AgentState) -> str:
        """意图检测后的路由"""
        intent = state['intent']
        
        if intent in ['search', 'knowledge', 'command', 'hardware', 'calculation', 'time']:
            return AgentNode.TOOL_PLANNING.value
        else:
            return AgentNode.RESPONSE_SYNTHESIS.value
    
    def _tool_planning_edge(self, state: AgentState) -> str:
        """工具规划后的路由"""
        if state['tools_to_use']:
            return AgentNode.TOOL_EXECUTION.value
        else:
            return AgentNode.RESPONSE_SYNTHESIS.value
    
    def _tool_execution_edge(self, state: AgentState) -> str:
        """工具执行后的路由"""
        return AgentNode.RESPONSE_SYNTHESIS.value
    
    # ========== 辅助方法 ==========
    
    def _generate_direct_response(self, intent: str, user_input: str) -> str:
        """生成直接响应"""
        responses = {
            'greeting': '您好！我是机器人控制助手，请问有什么可以帮助您的？',
            'help': '我可以帮您：\n1. 搜索网络信息\n2. 查询知识库\n3. 执行系统命令\n4. 控制机器人硬件\n5. 进行数学计算\n\n请告诉我您的需求！',
            'general': '我理解您的需求，让我为您处理...'
        }
        
        # 问候语检测
        greetings = ['你好', '您好', 'hi', 'hello', '嗨']
        if any(g in user_input.lower() for g in greetings):
            return responses['greeting']
        
        # 帮助检测
        if '帮助' in user_input or 'help' in user_input.lower():
            return responses['help']
        
        return responses['general']
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def _async_sleep(self, seconds: float):
        """异步睡眠"""
        import asyncio
        await asyncio.sleep(seconds)
    
    def get_graph_info(self) -> Dict[str, Any]:
        """获取图信息"""
        return {
            'nodes': [node.value for node in AgentNode],
            'edges': {
                'intent_detection': self._intent_detection_edge(None),
                'tool_planning': self._tool_planning_edge(None),
                'tool_execution': self._tool_execution_edge(None)
            }
        }
