"""
示例动作组件

演示如何创建一个基础的动作组件
"""

from typing import Dict, Any, Optional
from src.plugin_system.base.base_action import BaseAction


class SampleAction(BaseAction):
    """示例动作组件"""
    
    action_name = "sample_action"
    description = "这是一个示例动作，展示动作组件的基本结构"
    activation_keywords = ["示例", "模板", "测试"]
    
    async def execute(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """执行动作"""
        user_input = context.get("user_input", "")
        
        self.logger.info(f"示例动作被触发，用户输入: {user_input}")
        
        # 在这里实现你的动作逻辑
        response = f"示例动作收到输入: {user_input}"
        
        return {
            "success": True,
            "response": response,
            "action": self.action_name
        }
    
    async def can_execute(self, context: Dict[str, Any]) -> bool:
        """检查是否可以执行动作"""
        user_input = context.get("user_input", "")
        
        # 检查是否包含激活关键词
        return any(keyword in user_input for keyword in self.activation_keywords)