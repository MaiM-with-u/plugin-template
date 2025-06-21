"""
模板插件配置类

演示如何处理插件配置
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TemplatePluginConfig:
    """模板插件配置类"""
    
    enable_feature_a: bool = True
    sample_text: str = "Hello World"
    max_retries: int = 3
    timeout: float = 5.0
    
    def __init__(self, config_dict: Dict[str, Any]):
        """从配置字典初始化"""
        self.enable_feature_a = config_dict.get("enable_feature_a", self.enable_feature_a)
        self.sample_text = config_dict.get("sample_text", self.sample_text)
        self.max_retries = config_dict.get("max_retries", self.max_retries)
        self.timeout = config_dict.get("timeout", self.timeout)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "enable_feature_a": self.enable_feature_a,
            "sample_text": self.sample_text,
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }
    
    def validate(self) -> bool:
        """验证配置有效性"""
        if self.max_retries < 0:
            return False
        if self.timeout <= 0:
            return False
        return True