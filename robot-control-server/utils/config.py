"""
Configuration - 配置管理
"""

import os
from typing import Any, Optional
from loguru import logger


class Config:
    """配置管理器"""
    
    def __init__(self):
        self.config = self._load_env_config()
    
    def _load_env_config(self) -> dict:
        """从环境变量加载配置"""
        return {
            # 火山引擎配置
            "volcengine.app_id": os.getenv("VOLC_APP_ID", ""),
            "volcengine.token": os.getenv("VOLC_TOKEN", ""),
            
            # 知识库配置
            "knowledge.persist_dir": os.getenv("KNOWLEDGE_DIR", "/tmp/knowledge_db"),
            
            # 硬件配置
            "hardware.serial.port": os.getenv("SERIAL_PORT", "/dev/ttyUSB0"),
            "hardware.serial.baudrate": int(os.getenv("SERIAL_BAUDRATE", "115200")),
            
            # 服务配置
            "server.host": os.getenv("SERVER_HOST", "0.0.0.0"),
            "server.port": int(os.getenv("SERVER_PORT", "8080")),
            "server.debug": os.getenv("DEBUG", "false").lower() == "true",
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
    
    def __getitem__(self, key: str) -> Any:
        """支持 dict[] 访问"""
        return self.config.get(key)
