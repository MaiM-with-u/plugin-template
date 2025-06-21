"""
模板插件主类

演示如何创建一个基础的MaiBot插件
"""

import asyncio
from typing import List, Optional

from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.base_action import BaseAction
from src.plugin_system.base.base_processor import BaseProcessor
from src.plugin_system.base.base_tool import BaseTool

from .actions.sample_action import SampleAction
from .processors.sample_processor import SampleProcessor
from .tools.sample_tool import SampleTool
from .config import TemplatePluginConfig


class TemplatePlugin(BasePlugin):
    """模板插件类
    
    这是一个示例插件，展示了如何：
    1. 继承BasePlugin基类
    2. 注册各种组件（动作、处理器、工具）
    3. 实现插件生命周期方法
    4. 处理插件配置
    """
    
    def __init__(self, plugin_dir: str, config: Optional[dict] = None):
        super().__init__(plugin_dir, config)
        self.plugin_config = TemplatePluginConfig(config or {})
        
    async def on_load(self) -> bool:
        """插件加载时调用"""
        self.logger.info("模板插件开始加载...")
        
        try:
            # 注册组件
            await self._register_components()
            
            self.logger.info("模板插件加载完成")
            return True
            
        except Exception as e:
            self.logger.error(f"模板插件加载失败: {e}")
            return False
    
    async def on_unload(self) -> bool:
        """插件卸载时调用"""
        self.logger.info("模板插件开始卸载...")
        
        try:
            # 清理资源
            await self._cleanup_resources()
            
            self.logger.info("模板插件卸载完成")
            return True
            
        except Exception as e:
            self.logger.error(f"模板插件卸载失败: {e}")
            return False
    
    async def _register_components(self):
        """注册插件组件"""
        # 注册动作组件
        sample_action = SampleAction()
        await self.register_action(sample_action)
        
        # 注册处理器组件
        sample_processor = SampleProcessor()
        await self.register_processor(sample_processor)
        
        # 注册工具组件
        sample_tool = SampleTool()
        await self.register_tool(sample_tool)
        
        self.logger.info("所有组件注册完成")
    
    async def _cleanup_resources(self):
        """清理插件资源"""
        # 在这里添加资源清理逻辑
        # 例如：关闭文件句柄、断开网络连接等
        pass
    
    def get_plugin_info(self) -> dict:
        """获取插件信息"""
        return {
            "name": "Template Plugin",
            "version": "1.0.0",
            "description": "MaiBot插件开发模板",
            "components": {
                "actions": 1,
                "processors": 1,
                "tools": 1
            },
            "config": self.plugin_config.to_dict()
        }