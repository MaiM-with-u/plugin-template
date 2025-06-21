"""
示例命令组件

演示如何创建一个基础的命令组件
"""

from typing import Dict, Any, Optional, List
from src.plugin_system.base.base_command import BaseCommand


class SampleCommand(BaseCommand):
    """示例命令组件"""
    
    command_name = "sample"
    description = "这是一个示例命令，展示命令组件的基本结构"
    usage = "sample [选项] <参数>"
    aliases = ["模板", "示例"]
    
    def __init__(self):
        super().__init__()
        self.subcommands = {
            "hello": self._handle_hello,
            "echo": self._handle_echo,
            "help": self._handle_help
        }
    
    async def execute(self, args: List[str], context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """执行命令"""
        self.logger.info(f"示例命令被调用，参数: {args}")
        
        if not args:
            return await self._handle_help([], context)
        
        subcommand = args[0].lower()
        remaining_args = args[1:] if len(args) > 1 else []
        
        if subcommand in self.subcommands:
            return await self.subcommands[subcommand](remaining_args, context)
        else:
            return {
                "success": False,
                "response": f"未知的子命令: {subcommand}。使用 'sample help' 查看帮助。",
                "command": self.command_name
            }
    
    async def _handle_hello(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """处理hello子命令"""
        name = args[0] if args else "世界"
        response = f"你好, {name}!"
        
        return {
            "success": True,
            "response": response,
            "command": f"{self.command_name} hello",
            "data": {"greeting": response}
        }
    
    async def _handle_echo(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """处理echo子命令"""
        if not args:
            return {
                "success": False,
                "response": "echo命令需要至少一个参数",
                "command": f"{self.command_name} echo"
            }
        
        echo_text = " ".join(args)
        
        return {
            "success": True,
            "response": f"回显: {echo_text}",
            "command": f"{self.command_name} echo",
            "data": {"original": echo_text, "echoed": echo_text}
        }
    
    async def _handle_help(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """处理help子命令"""
        help_text = f"""
示例命令帮助:

用法: {self.usage}
别名: {', '.join(self.aliases)}

子命令:
  hello [名称]    - 打招呼，可选指定名称
  echo <文本>     - 回显输入的文本
  help           - 显示此帮助信息

示例:
  sample hello
  sample hello 张三
  sample echo 这是一段测试文本
  sample help
        """.strip()
        
        return {
            "success": True,
            "response": help_text,
            "command": f"{self.command_name} help"
        }
    
    async def can_execute(self, args: List[str], context: Dict[str, Any]) -> bool:
        """检查是否可以执行命令"""
        # 基础命令组件通常都可以执行，除非有特殊限制
        return True
    
    def get_command_info(self) -> Dict[str, Any]:
        """获取命令信息"""
        return {
            "name": self.command_name,
            "description": self.description,
            "usage": self.usage,
            "aliases": self.aliases,
            "subcommands": list(self.subcommands.keys()),
            "examples": [
                "sample hello",
                "sample hello 张三", 
                "sample echo 测试文本",
                "sample help"
            ]
        }