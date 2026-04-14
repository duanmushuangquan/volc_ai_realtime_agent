"""
Chat Manager - 对话管理器
使用LangChain管理对话上下文和历史
"""

import asyncio
from typing import List, Dict, Optional, Any, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger


@dataclass
class Message:
    """对话消息"""
    role: str  # user, assistant, system, tool
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


class ChatManager:
    """
    对话管理器
    
    负责：
    1. 管理对话历史
    2. 维护系统提示词
    3. 提供对话上下文
    """
    
    def __init__(
        self,
        system_prompt: str = "你是一个智能机器人助手。",
        max_history: int = 20
    ):
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.conversations: Dict[str, List[Message]] = {}
        self.current_conversation_id: Optional[str] = None
        
        logger.info(f"ChatManager initialized with max_history={max_history}")
    
    def create_conversation(self, conversation_id: str) -> None:
        """创建新的对话会话"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            logger.info(f"Created new conversation: {conversation_id}")
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Message:
        """添加消息到对话"""
        if conversation_id not in self.conversations:
            self.create_conversation(conversation_id)
        
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.conversations[conversation_id].append(message)
        
        # 限制历史长度
        if len(self.conversations[conversation_id]) > self.max_history:
            self.conversations[conversation_id] = \
                self.conversations[conversation_id][-self.max_history:]
        
        logger.debug(f"Added {role} message to {conversation_id}: {content[:50]}...")
        return message
    
    def get_conversation_history(
        self,
        conversation_id: str,
        include_system: bool = True
    ) -> List[Dict]:
        """获取对话历史"""
        if conversation_id not in self.conversations:
            return []
        
        history = []
        
        if include_system:
            history.append({
                'role': 'system',
                'content': self.system_prompt
            })
        
        for msg in self.conversations[conversation_id]:
            history.append(msg.to_dict())
        
        return history
    
    def get_recent_messages(
        self,
        conversation_id: str,
        n: int = 10
    ) -> List[Message]:
        """获取最近n条消息"""
        if conversation_id not in self.conversations:
            return []
        
        return self.conversations[conversation_id][-n:]
    
    def clear_conversation(self, conversation_id: str) -> None:
        """清空对话历史"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id] = []
            logger.info(f"Cleared conversation: {conversation_id}")
    
    def delete_conversation(self, conversation_id: str) -> None:
        """删除对话"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
    
    async def stream_response(
        self,
        conversation_id: str,
        user_message: str,
        response_generator
    ) -> AsyncGenerator[str, None]:
        """
        流式生成响应
        
        Args:
            conversation_id: 对话ID
            user_message: 用户消息
            response_generator: 异步响应生成器
        
        Yields:
            响应文本片段
        """
        # 添加用户消息
        self.add_message(conversation_id, 'user', user_message)
        
        # 流式生成响应
        full_response = ""
        async for chunk in response_generator:
            full_response += chunk
            yield chunk
        
        # 添加助手消息
        self.add_message(conversation_id, 'assistant', full_response)
    
    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """获取对话摘要"""
        if conversation_id not in self.conversations:
            return {
                'message_count': 0,
                'first_message': None,
                'last_message': None,
                'duration': None
            }
        
        messages = self.conversations[conversation_id]
        
        return {
            'message_count': len(messages),
            'first_message': messages[0].content[:100] if messages else None,
            'last_message': messages[-1].content[:100] if messages else None,
            'duration': (
                messages[-1].timestamp - messages[0].timestamp
                if len(messages) > 1 else None
            )
        }


# 异步生成器类型提示
from typing import AsyncGenerator
