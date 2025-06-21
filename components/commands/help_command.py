"""
帮助Command - 官方文档Command最佳实践示例

展示内容：
- 正则表达式匹配和参数捕获
- 拦截控制的正确使用
- 错误处理最佳实践
- 配置驱动的命令行为
- 完整的用户体验设计
"""

from src.plugin_system import BaseCommand
from typing import Tuple, Optional
import re


class HelpCommand(BaseCommand):
    """
    帮助Command
    
    遵循官方文档的Command设计原则：
    - 清晰的正则表达式匹配
    - 合理的参数捕获
    - 完善的错误处理
    - 用户友好的帮助信息
    """
    
    # ==================== 命令匹配配置 ====================
    # 支持：/help, /help actions, /help commands, /help config
    command_pattern = r"^/help(?:\s+(?P<topic>actions|commands|config|all))?$"
    
    # 命令说明
    command_help = "显示插件帮助信息，支持查看特定主题"
    
    # 使用示例
    command_examples = [
        "/help",
        "/help actions", 
        "/help commands",
        "/help config",
        "/help all"
    ]
    
    # 拦截消息 - 帮助命令应该拦截，避免触发其他组件
    intercept_message = True
    
    # ==================== 执行逻辑 ====================
    async def execute(self) -> Tuple[bool, Optional[str]]:
        """
        执行帮助命令
        
        遵循官方文档的最佳实践：
        - 早期参数验证
        - 配置驱动的行为
        - 完整的错误处理
        - 清晰的返回值
        """
        try:
            # 检查功能是否启用
            if not self.get_config("features.enable_help_command", True):
                await self.send_text("❌ 帮助命令功能已禁用")
                return False, "帮助命令已禁用"
            
            # 获取配置
            help_prefix = self.get_config("commands.help_prefix", "📖")
            debug_mode = self.get_config("plugin.debug_mode", False)
            
            # 获取参数
            topic = self.matched_groups.get("topic")
            
            # 调试信息
            if debug_mode:
                await self.send_text(f"🔍 调试：帮助主题={topic}")
            
            # 根据主题显示不同的帮助内容
            if topic == "actions":
                await self._show_actions_help(help_prefix)
            elif topic == "commands":
                await self._show_commands_help(help_prefix)
            elif topic == "config":
                await self._show_config_help(help_prefix)
            elif topic == "all":
                await self._show_complete_help(help_prefix)
            else:
                await self._show_general_help(help_prefix)
            
            return True, f"显示了帮助信息，主题：{topic or 'general'}"
            
        except Exception as e:
            error_msg = f"帮助命令执行失败: {str(e)}"
            await self.send_text(f"❌ {error_msg}")
            return False, error_msg
    
    # ==================== 私有方法 ====================
    async def _show_general_help(self, prefix: str):
        """显示通用帮助信息"""
        help_text = f"""{prefix} **插件帮助**

🔌 **插件名称**: Example Template Plugin
📝 **版本**: 1.0.0
👨‍💻 **作者**: MaiBot开发团队

📋 **可用命令**:
• `/help` - 显示此帮助信息
• `/help actions` - 查看Action组件说明
• `/help commands` - 查看Command组件说明  
• `/help config` - 查看配置说明
• `/help all` - 查看完整帮助

🔧 **主要功能**:
• 智能问候：自动回应用户问候
• 智能回复：根据对话内容生成相关回复
• 配置管理：通过命令调整插件设置

💡 **提示**: 使用 `/help <主题>` 查看详细说明"""
        
        await self.send_text(help_text)
    
    async def _show_actions_help(self, prefix: str):
        """显示Action组件帮助"""
        help_text = f"""{prefix} **Action组件说明**

⚡ **Action是什么？**
Action是智能组件，由麦麦根据对话情境自主选择使用，具有随机性和拟人化特点。

🎯 **可用Actions**:

**1. 问候Action (greeting_action)**
• 功能：智能问候回应
• 激活：关键词触发（你好、hello、hi等）
• 特点：支持不同时间和语调的问候

**2. 智能回复Action (smart_response_action)**  
• 功能：生成相关的补充回复
• 激活：随机激活 + LLM智能判断
• 特点：支持多种回复类型和缓存机制

🔧 **配置选项**:
• `features.enable_greetings` - 启用/禁用问候功能
• `features.enable_smart_responses` - 启用/禁用智能回复
• `actions.greeting_keywords` - 自定义问候关键词
• `actions.response_probability` - 智能回复激活概率"""
        
        await self.send_text(help_text)
    
    async def _show_commands_help(self, prefix: str):
        """显示Command组件帮助"""
        help_text = f"""{prefix} **Command组件说明**

💻 **Command是什么？**
Command是直接响应用户指令的组件，通过正则表达式匹配用户输入，提供确定性功能。

📋 **可用Commands**:

**1. 帮助命令 (help_command)**
• 格式：`/help [topic]`
• 功能：显示插件帮助信息
• 示例：`/help actions`

**2. 配置命令 (config_command)**  
• 格式：`/config <action> [key] [value]`
• 功能：查看和修改插件配置
• 示例：`/config get debug_mode`

🎛️ **配置选项**:
• `features.enable_help_command` - 启用/禁用帮助命令
• `features.enable_config_command` - 启用/禁用配置命令
• `commands.help_prefix` - 帮助消息前缀
• `commands.config_admin_only` - 配置命令仅限管理员"""
        
        await self.send_text(help_text)
    
    async def _show_config_help(self, prefix: str):
        """显示配置说明"""
        help_text = f"""{prefix} **配置说明**

⚙️ **配置原则**:
本插件采用Schema驱动的配置系统，配置文件会自动生成，请勿手动创建！

📂 **配置节说明**:

**[plugin]** - 插件基本配置
• `enabled` - 是否启用插件
• `config_version` - 配置文件版本  
• `debug_mode` - 调试模式开关

**[features]** - 功能开关
• `enable_greetings` - 问候功能
• `enable_smart_responses` - 智能回复功能
• `enable_help_command` - 帮助命令
• `enable_config_command` - 配置命令

**[actions]** - Action组件配置
• `greeting_keywords` - 问候关键词列表
• `response_probability` - 智能回复概率
• `max_response_length` - 最大回复长度
• `enable_emoji` - 启用表情符号

**[commands]** - Command组件配置  
• `help_prefix` - 帮助消息前缀
• `config_admin_only` - 配置命令权限
• `command_timeout` - 命令超时时间

**[advanced]** - 高级配置
• `cache_enabled` - 缓存机制
• `cache_ttl` - 缓存生存时间
• `log_level` - 日志级别
• `performance_monitor` - 性能监控

🔧 **修改配置**:
配置文件位置：`plugins/example_template_plugin/config.toml`
修改后需要重启插件生效。"""
        
        await self.send_text(help_text)
    
    async def _show_complete_help(self, prefix: str):
        """显示完整帮助信息"""
        await self.send_text(f"{prefix} **完整帮助信息**")
        await self.send_text("正在加载完整帮助...")
        
        # 显示所有帮助内容
        await self._show_general_help("📖")
        await self._show_actions_help("⚡")  
        await self._show_commands_help("💻")
        await self._show_config_help("⚙️")
        
        # 添加额外信息
        extra_text = f"""{prefix} **额外信息**

🔗 **相关链接**:
• 官方文档：https://docs.mai-mai.org/
• 插件开发：https://docs.mai-mai.org/develop/plugin_develop/
• 配置指南：https://docs.mai-mai.org/develop/plugin_develop/configuration-guide

📞 **技术支持**:
• GitHub Issues: 报告问题和建议
• 社区论坛: 获取使用帮助
• 开发者QQ群: 实时技术交流

💡 **最佳实践**:
1. 定期备份配置文件
2. 测试环境验证配置更改
3. 关注插件更新和兼容性
4. 合理使用调试模式

感谢使用 MaiBot 插件系统！"""
        
        await self.send_text(extra_text)
