"""
示例处理器组件

演示如何创建一个基础的处理器组件
"""

from typing import Dict, Any, Optional
from src.plugin_system.base.base_processor import BaseProcessor


class SampleProcessor(BaseProcessor):
    """示例处理器组件"""
    
    processor_name = "sample_processor"
    description = "这是一个示例处理器，展示处理器组件的基本结构"
    
    async def process(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理数据"""
        self.logger.info(f"示例处理器开始处理数据: {data}")
        
        # 在这里实现你的处理逻辑
        processed_data = data.copy()
        processed_data["processed_by"] = self.processor_name
        processed_data["processed_at"] = self._get_current_timestamp()
        
        self.logger.info(f"示例处理器处理完成")
        
        return processed_data
    
    async def can_process(self, data: Dict[str, Any]) -> bool:
        """检查是否可以处理数据"""
        # 在这里添加处理条件检查
        return "text" in data or "content" in data
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()