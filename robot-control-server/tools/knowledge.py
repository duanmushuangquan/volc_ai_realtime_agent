"""
Knowledge Base - 知识库模块
基于向量数据库的知识检索
"""

import os
from typing import List, Dict, Any, Optional
from loguru import logger


class KnowledgeBase:
    """
    知识库管理器
    
    负责：
    1. 知识条目存储
    2. 语义检索
    3. 知识管理
    """
    
    def __init__(
        self,
        persist_dir: str = "/tmp/knowledge_db",
        collection_name: str = "robot_knowledge"
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        
        # 确保目录存在
        os.makedirs(persist_dir, exist_ok=True)
        
        # 知识条目存储（简化版，实际应使用向量数据库）
        self.documents: List[Dict[str, Any]] = []
        
        # 初始化并加载示例知识
        self._initialize()
        
        logger.info(f"KnowledgeBase initialized: {persist_dir}")
    
    def _initialize(self):
        """初始化知识库"""
        # 加载示例知识
        sample_knowledge = [
            {
                "content": "机器人前进命令是 move_forward，用于让机器人向前移动指定距离",
                "metadata": {"category": "command", "type": "movement"}
            },
            {
                "content": "机器人后退命令是 move_backward，用于让机器人向后移动指定距离",
                "metadata": {"category": "command", "type": "movement"}
            },
            {
                "content": "机器人左转命令是 turn_left，右转命令是 turn_right",
                "metadata": {"category": "command", "type": "movement"}
            },
            {
                "content": "机器人停止命令是 stop，用于立即停止机器人所有运动",
                "metadata": {"category": "command", "type": "movement"}
            },
            {
                "content": "机械臂上升命令是 arm_up，下降命令是 arm_down",
                "metadata": {"category": "command", "type": "arm"}
            },
            {
                "content": "夹爪张开命令是 grip_open，合拢命令是 grip_close",
                "metadata": {"category": "command", "type": "arm"}
            },
            {
                "content": "机器人电池电量低于20%时需要充电",
                "metadata": {"category": "safety", "type": "battery"}
            },
            {
                "content": "机器人运行时请保持周围1米范围内无障碍物",
                "metadata": {"category": "safety", "type": "operation"}
            },
            {
                "content": "机器人的默认IP地址是 192.168.1.100",
                "metadata": {"category": "config", "type": "network"}
            },
            {
                "content": "机器人支持的通信协议包括：串口（115200波特率）、CAN总线、以太网",
                "metadata": {"category": "config", "type": "communication"}
            },
            {
                "content": "机器人的传感器包括：超声波距离传感器、红外传感器、温湿度传感器",
                "metadata": {"category": "hardware", "type": "sensors"}
            },
            {
                "content": "机器人的运动速度范围是 0.1-2.0 m/s",
                "metadata": {"category": "spec", "type": "movement"}
            },
        ]
        
        for item in sample_knowledge:
            self.add(item["content"], item["metadata"])
        
        logger.info(f"Loaded {len(sample_knowledge)} sample knowledge items")
    
    def add(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        添加知识条目
        
        Args:
            content: 知识内容
            metadata: 元数据
        
        Returns:
            知识ID
        """
        import uuid
        
        item_id = str(uuid.uuid4())[:8]
        
        item = {
            "id": item_id,
            "content": content,
            "metadata": metadata or {},
            "created_at": self._get_timestamp()
        }
        
        self.documents.append(item)
        
        logger.debug(f"Added knowledge: {item_id}")
        return item_id
    
    def search(self, query: str, top_k: int = 3) -> str:
        """
        搜索知识
        
        Args:
            query: 查询文本
            top_k: 返回数量
        
        Returns:
            检索结果文本
        """
        # 简化的关键词匹配搜索
        # 实际应使用向量数据库进行语义检索
        
        query_words = query.lower().split()
        scores: List[tuple] = []
        
        for doc in self.documents:
            content = doc["content"].lower()
            
            # 计算匹配分数
            score = 0
            for word in query_words:
                if word in content:
                    score += 1
                    # 完全匹配加分
                    if word in ["机器人", "命令", "控制"]:
                        score += 2
            
            if score > 0:
                scores.append((score, doc))
        
        # 按分数排序
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # 返回top_k结果
        results = scores[:top_k]
        
        if not results:
            return "在知识库中未找到相关内容"
        
        response_parts = ["根据知识库检索结果："]
        
        for i, (score, doc) in enumerate(results, 1):
            response_parts.append(f"\n{i}. {doc['content']}")
        
        return "".join(response_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        categories = {}
        for doc in self.documents:
            cat = doc["metadata"].get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_count": len(self.documents),
            "categories": categories
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


# 向量数据库集成示例（使用ChromaDB）
class ChromaKnowledgeBase:
    """
    ChromaDB知识库（生产环境推荐）
    """
    
    def __init__(
        self,
        persist_dir: str = "/tmp/chroma_db",
        collection_name: str = "robot_knowledge"
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._initialize()
    
    def _initialize(self):
        """初始化ChromaDB"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info("ChromaDB initialized successfully")
        
        except ImportError:
            logger.warning("ChromaDB not installed, falling back to simple storage")
            self.client = None
    
    def add(self, content: str, metadata: Optional[Dict] = None) -> str:
        """添加知识"""
        import uuid
        
        if self.collection:
            item_id = str(uuid.uuid4())
            self.collection.add(
                ids=[item_id],
                documents=[content],
                metadatas=[metadata or {}]
            )
            return item_id
        
        return "ChromaDB not available"
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """语义检索"""
        # 实际应先生成query的embedding
        # 这里简化处理
        return []
