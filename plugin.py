"""
MaiBot标准插件模板
=================

本插件模板展示了基于官方文档的最佳实践，包括：
- Schema驱动的配置系统
- 智能Action组件设计
- 命令Command组件实现
- 完整的错误处理机制
- 配置版本管理

严格遵循官方文档要求，绝不手动创建config.toml文件！
"""

from src.plugin_system import BasePlugin, register_plugin
from src.plugin_system.base.config_types import ConfigField
from src.plugin_system.core.component_info import ComponentInfo
from typing import List, Tuple, Type

# 导入组件
from .components.actions.greeting_action import GreetingAction
from .components.actions.smart_response_action import SmartResponseAction
from .components.commands.help_command import HelpCommand
from .components.commands.config_command import ConfigCommand


@register_plugin
class ExampleTemplatePlugin(BasePlugin):
    """
    MaiBot标准插件模板
    
    展示官方推荐的插件结构和最佳实践：
    - 强制manifest机制
    - Schema驱动配置
    - 智能Action设计
    - 命令Command实现
    """
    
    # ==================== 插件基本信息 ====================
    plugin_name = "example_template_plugin"
    plugin_description = "MaiBot标准插件模板，展示Action/Command/配置的最佳实践"
    plugin_version = "1.0.0"
    plugin_author = "MaiBot开发团队"
    enable_plugin = True
    config_file_name = "config.toml"
    
    # ==================== 配置定义 ====================
    # 配置节描述 - 将作为配置文件的注释
    config_section_descriptions = {
        "plugin": "插件基本配置",
        "features": "功能开关配置", 
        "actions": "Action组件配置",
        "commands": "Command组件配置",
        "advanced": "高级功能配置"
    }
    
    # Schema驱动的配置定义 - 系统会自动生成配置文件
    config_schema = {
        "plugin": {
            "enabled": ConfigField(
                type=bool, 
                default=True, 
                description="是否启用插件"
            ),
            "config_version": ConfigField(
                type=str, 
                default="1.0.0", 
                description="配置文件版本"
            ),
            "debug_mode": ConfigField(
                type=bool, 
                default=False, 
                description="是否启用调试模式"
            )
        },
        
        "features": {
            "enable_greetings": ConfigField(
                type=bool, 
                default=True, 
                description="是否启用问候功能"
            ),
            "enable_smart_responses": ConfigField(
                type=bool, 
                default=True, 
                description="是否启用智能回复功能"
            ),
            "enable_help_command": ConfigField(
                type=bool, 
                default=True, 
                description="是否启用帮助命令"
            ),
            "enable_config_command": ConfigField(
                type=bool, 
                default=False, 
                description="是否启用配置管理命令"
            )
        },
        
        "actions": {
            "greeting_keywords": ConfigField(
                type=list,
                default=["你好", "hello", "hi", "嗨"],
                description="问候Action的触发关键词"
            ),
            "response_probability": ConfigField(
                type=float,
                default=0.1,
                description="智能回复Action的随机激活概率（0.0-1.0）"
            ),
            "max_response_length": ConfigField(
                type=int,
                default=200,
                description="智能回复的最大长度"
            ),
            "enable_emoji": ConfigField(
                type=bool,
                default=True,
                description="是否在回复中包含表情符号"
            )
        },
        
        "commands": {
            "help_prefix": ConfigField(
                type=str,
                default="📖",
                description="帮助命令的消息前缀"
            ),
            "config_admin_only": ConfigField(
                type=bool,
                default=True,
                description="配置命令是否仅限管理员使用"
            ),
            "command_timeout": ConfigField(
                type=int,
                default=30,
                description="命令执行超时时间（秒）"
            )
        },
        
        "advanced": {
            "cache_enabled": ConfigField(
                type=bool,
                default=True,
                description="是否启用缓存机制"
            ),
            "cache_ttl": ConfigField(
                type=int,
                default=3600,
                description="缓存生存时间（秒）"
            ),
            "log_level": ConfigField(
                type=str,
                default="INFO",
                description="日志记录级别",
                choices=["DEBUG", "INFO", "WARNING", "ERROR"]
            ),
            "performance_monitor": ConfigField(
                type=bool,
                default=False,
                description="是否启用性能监控"
            )
        }
    }
    
    # ==================== 组件注册 ====================
    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        """
        根据配置动态注册组件
        
        遵循官方文档的最佳实践：
        - 根据配置决定组件启用状态
        - 使用配置驱动的组件行为
        - 支持运行时组件控制
        """
        components = []
        
        # 检查插件是否启用
        if not self.get_config("plugin.enabled", True):
            return components
        
        # 根据配置注册Action组件
        if self.get_config("features.enable_greetings", True):
            components.append((
                GreetingAction.get_action_info(), 
                GreetingAction
            ))
        
        if self.get_config("features.enable_smart_responses", True):
            components.append((
                SmartResponseAction.get_action_info(), 
                SmartResponseAction
            ))
        
        # 根据配置注册Command组件
        if self.get_config("features.enable_help_command", True):
            components.append((
                HelpCommand.get_command_info(), 
                HelpCommand
            ))
        
        if self.get_config("features.enable_config_command", False):
            components.append((
                ConfigCommand.get_command_info(), 
                ConfigCommand
            ))
        
        return components
    
    # ==================== 插件生命周期 ====================
    async def on_plugin_load(self):
        """插件加载时的初始化操作"""
        if self.get_config("plugin.debug_mode", False):
            print(f"[{self.plugin_name}] 插件加载完成，调试模式已启用")
        
        # 性能监控初始化
        if self.get_config("advanced.performance_monitor", False):
            await self._init_performance_monitor()
    
    async def on_plugin_unload(self):
        """插件卸载时的清理操作"""
        if self.get_config("plugin.debug_mode", False):
            print(f"[{self.plugin_name}] 插件正在卸载...")
        
        # 清理缓存
        if self.get_config("advanced.cache_enabled", True):
            await self._cleanup_cache()
    
    # ==================== 私有方法 ====================
    async def _init_performance_monitor(self):
        """初始化性能监控"""
        # 这里可以初始化性能监控相关的功能
        pass
    
    async def _cleanup_cache(self):
        """清理缓存"""
        # 这里可以实现缓存清理逻辑
        pass
