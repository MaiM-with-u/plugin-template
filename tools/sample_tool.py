"""
示例工具组件

演示如何创建一个基础的工具组件
"""

from typing import Dict, Any, Optional
from src.plugin_system.base.base_tool import BaseTool


class SampleTool(BaseTool):
    """示例工具组件"""
    
    tool_name = "sample_tool"
    description = "这是一个示例工具，展示工具组件的基本结构"
    
    async def execute(self, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """执行工具"""
        self.logger.info(f"示例工具开始执行，参数: {parameters}")
        
        # 在这里实现你的工具逻辑
        text = parameters.get("text", "")
        operation = parameters.get("operation", "echo")
        
        if operation == "echo":
            result = text
        elif operation == "upper":
            result = text.upper()
        elif operation == "lower":
            result = text.lower()
        elif operation == "reverse":
            result = text[::-1]
        else:
            result = f"不支持的操作: {operation}"
        
        return {
            "success": True,
            "result": result,
            "tool": self.tool_name
        }
    
    def get_tool_schema(self) -> Dict[str, Any]:
        """获取工具参数模式"""
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "要处理的文本"
                },
                "operation": {
                    "type": "string",
                    "enum": ["echo", "upper", "lower", "reverse"],
                    "description": "要执行的操作",
                    "default": "echo"
                }
            },
            "required": ["text"]
        }