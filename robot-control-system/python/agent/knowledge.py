"""
Knowledge Base - 知识库管理
向量数据库和知识检索
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np
from loguru import logger


@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'metadata': self.metadata
        }


class KnowledgeBase:
    """
    知识库管理器
    
    负责：
    1. 管理知识向量
    2. 知识检索
    3. 知识添加/更新/删除
    """
    
    def __init__(
        self,
        db_type: str = "chroma",
        persist_directory: str = "/tmp/vector_db",
        collection_name: str = "robot_knowledge",
        embedding_dim: int = 384
    ):
        self.db_type = db_type
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        
        # 内存向量存储（简化版）
        self.documents: List[KnowledgeItem] = []
        
        # 初始化向量数据库
        self._initialize_db()
        
        logger.info(f"KnowledgeBase initialized: type={db_type}, collection={collection_name}")
    
    def _initialize_db(self):
        """初始化向量数据库"""
        if self.db_type == "chroma":
            try:
                import chromadb
                from chromadb.config import Settings
                
                self.client = chromadb.PersistentClient(
                    path=self.persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info("ChromaDB initialized successfully")
            
            except ImportError:
                logger.warning("ChromaDB not installed, using in-memory storage")
                self.client = None
                self.collection = None
        
        else:
            logger.warning(f"Unsupported db_type: {db_type}, using in-memory storage")
            self.client = None
            self.collection = None
    
    async def add_knowledge(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        generate_embedding: bool = True
    ) -> str:
        """
        添加知识条目
        
        Args:
            content: 知识内容
            metadata: 元数据
            generate_embedding: 是否生成向量
        
        Returns:
            知识ID
        """
        import uuid
        
        item_id = str(uuid.uuid4())
        
        # 生成向量
        embedding = None
        if generate_embedding:
            embedding = await self._generate_embedding(content)
        
        item = KnowledgeItem(
            id=item_id,
            content=content,
            metadata=metadata or {},
            embedding=embedding
        )
        
        # 存储
        if self.collection:
            self.collection.add(
                ids=[item_id],
                documents=[content],
                metadatas=[metadata or {}]
            )
        else:
            self.documents.append(item)
        
        logger.info(f"Added knowledge: {item_id}")
        return item_id
    
    async def add_knowledge_batch(
        self,
        knowledge_items: List[Dict[str, Any]]
    ) -> List[str]:
        """
        批量添加知识
        
        Args:
            knowledge_items: 知识条目列表
                [{
                    'content': '知识内容',
                    'metadata': {'source': 'manual', 'category': 'manual'}
                }]
        
        Returns:
            添加的知识ID列表
        """
        ids = []
        
        for item in knowledge_items:
            item_id = await self.add_knowledge(
                content=item['content'],
                metadata=item.get('metadata'),
                generate_embedding=True
            )
            ids.append(item_id)
        
        logger.info(f"Batch added {len(ids)} knowledge items")
        return ids
    
    async def search(
        self,
        query: str,
        top_k: int = 3,
        filter_metadata: Optional[Dict] = None
    ) -> List[KnowledgeItem]:
        """
        检索知识
        
        Args:
            query: 查询文本
            top_k: 返回数量
            filter_metadata: 元数据过滤条件
        
        Returns:
            相关的知识条目列表
        """
        # 生成查询向量
        query_embedding = await self._generate_embedding(query)
        
        results = []
        
        if self.collection:
            # ChromaDB检索
            query_results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                where=filter_metadata
            )
            
            if query_results and query_results['ids']:
                for i, item_id in enumerate(query_results['ids'][0]):
                    idx = query_results['documents'][0][i]
                    metadata = query_results['metadatas'][0][i]
                    
                    results.append(KnowledgeItem(
                        id=item_id,
                        content=idx,
                        metadata=metadata,
                        embedding=None
                    ))
        
        else:
            # 内存检索（简化版余弦相似度）
            similarities = []
            
            for item in self.documents:
                if item.embedding is not None:
                    similarity = self._cosine_similarity(
                        query_embedding,
                        item.embedding
                    )
                    similarities.append((similarity, item))
            
            # 排序并返回top_k
            similarities.sort(key=lambda x: x[0], reverse=True)
            results = [item for _, item in similarities[:top_k]]
        
        logger.debug(f"Search '{query}' returned {len(results)} results")
        return results
    
    def delete_knowledge(self, item_id: str) -> bool:
        """删除知识条目"""
        if self.collection:
            self.collection.delete(ids=[item_id])
            logger.info(f"Deleted knowledge: {item_id}")
            return True
        else:
            self.documents = [d for d in self.documents if d.id != item_id]
            logger.info(f"Deleted knowledge from memory: {item_id}")
            return True
    
    def clear_knowledge(self) -> None:
        """清空知识库"""
        if self.collection:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
        else:
            self.documents.clear()
        
        logger.info("Knowledge base cleared")
    
    async def _generate_embedding(self, text: str) -> np.ndarray:
        """
        生成文本向量
        
        实际实现可以使用：
        1. OpenAI text-embedding-ada-002
        2. HuggingFace sentence-transformers
        3. 火山引擎embedding API
        """
        # 简化实现：使用词袋模型
        # 实际应使用专业的embedding模型
        
        words = text.lower().split()
        vector = np.zeros(self.embedding_dim)
        
        for i, word in enumerate(words[:self.embedding_dim]):
            vector[i] = hash(word) % 100 / 100.0
        
        # L2归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        if self.collection:
            count = self.collection.count()
        else:
            count = len(self.documents)
        
        return {
            'db_type': self.db_type,
            'collection_name': self.collection_name,
            'document_count': count,
            'embedding_dim': self.embedding_dim
        }
    
    async def load_sample_knowledge(self):
        """加载示例知识库"""
        sample_knowledge = [
            {
                'content': '机器人移动命令：forward向前，backward向后，turn_left左转，turn_right右转',
                'metadata': {'category': 'command', 'type': 'movement'}
            },
            {
                'content': '机械臂控制：arm_up抬起，arm_down放下，grip_open张开，grip_close抓取',
                'metadata': {'category': 'command', 'type': 'arm'}
            },
            {
                'content': '系统状态查询：status查看状态，battery查看电量，location查看位置',
                'metadata': {'category': 'command', 'type': 'system'}
            },
            {
                'content': '安全注意事项：1. 确保周围无障碍物 2. 保持安全距离 3. 定期检查设备',
                'metadata': {'category': 'safety', 'type': 'guideline'}
            },
            {
                'content': '故障排除：1. 重启系统 2. 检查连接线 3. 联系技术支持',
                'metadata': {'category': 'troubleshooting', 'type': 'guide'}
            }
        ]
        
        await self.add_knowledge_batch(sample_knowledge)
        logger.info("Sample knowledge loaded")
