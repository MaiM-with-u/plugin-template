"""
配置管理Command - 官方文档高级Command特性示例

展示内容：
- 复杂正则表达式匹配
- 多参数捕获和验证  
- 权限控制机制
- 配置动态读写
- 安全性最佳实践
"""

from src.plugin_system import BaseCommand
from typing import Tuple, Optional
import re


class ConfigCommand(BaseCommand):
    """
    配置管理Command
    
    展示高级Command特性：
    - 复杂的参数解析
    - 权限验证机制
    - 配置动态管理
    - 安全的参数处理
    """
    
    # ==================== 命令匹配配置 ====================
    # 支持：/config list, /config get key, /config set key value
    command_pattern = r"^/config\s+(?P<action>get|set|list|reset)(?:\s+(?P<key>\w+(?:\.\w+)*))?(?:\s+(?P<value>.+))?$"
    
    # 命令说明
    command_help = "配置管理命令，支持查看、修改和重置插件配置"
    
    # 使用示例
    command_examples = [
        "/config list",
        "/config get plugin.enabled",
        "/config set debug_mode true",
        "/config reset features.enable_greetings"
    ]
    
    # 拦截消息 - 配置命令应该拦截，避免触发其他组件
    intercept_message = True
    
    # ==================== 执行逻辑 ====================
    async def execute(self) -> Tuple[bool, Optional[str]]:
        """
        执行配置管理命令
        
        展示高级功能：
        - 权限验证
        - 复杂参数处理
        - 配置安全管理
        - 详细错误报告
        """
        try:
            # 检查功能是否启用
            if not self.get_config("features.enable_config_command", False):
                await self.send_text("❌ 配置管理命令功能已禁用")
                return False, "配置命令已禁用"
            
            # 权限检查
            if self.get_config("commands.config_admin_only", True):
                # 这里应该实现实际的权限检查逻辑
                # 为了示例，我们假设具有权限
                has_permission = await self._check_admin_permission()
                if not has_permission:
                    await self.send_text("❌ 权限不足，配置命令仅限管理员使用")
                    return False, "权限不足"
            
            # 获取配置
            debug_mode = self.get_config("plugin.debug_mode", False)
            command_timeout = self.get_config("commands.command_timeout", 30)
            
            # 获取参数
            action = self.matched_groups.get("action")
            key = self.matched_groups.get("key")  
            value = self.matched_groups.get("value")
            
            # 调试信息
            if debug_mode:
                await self.send_text(
                    f"🔧 配置命令：动作={action}, 键={key}, 值={value}"
                )
            
            # 参数验证
            if not action:
                await self.send_text("❌ 缺少操作参数")
                return False, "缺少操作参数"
            
            # 执行不同的配置操作
            if action == "list":
                return await self._handle_list_config()
            elif action == "get":
                return await self._handle_get_config(key)
            elif action == "set":
                return await self._handle_set_config(key, value)
            elif action == "reset":
                return await self._handle_reset_config(key)
            else:
                await self.send_text(f"❌ 不支持的操作：{action}")
                return False, f"不支持的操作：{action}"
            
        except Exception as e:
            error_msg = f"配置命令执行失败: {str(e)}"
            await self.send_text(f"❌ {error_msg}")
            return False, error_msg
    
    # ==================== 私有方法 ====================
    async def _check_admin_permission(self) -> bool:
        """
        检查管理员权限
        
        在实际实现中，这里应该检查：
        - 用户ID是否在管理员列表中
        - 用户角色和权限
        - 群组管理员状态等
        """
        # 示例实现：简单检查用户ID
        admin_users = ["admin", "owner", "developer"]  # 从配置或数据库获取
        current_user = self.user_id or "unknown"
        
        # 在实际实现中，应该有更严格的权限检查
        return current_user in admin_users or current_user == "demo_admin"
    
    async def _handle_list_config(self) -> Tuple[bool, str]:
        """处理配置列表命令"""
        try:
            config_text = """🔧 **插件配置列表**

📂 **[plugin]** - 插件基本配置
• `enabled` = True
• `config_version` = "1.0.0" 
• `debug_mode` = False

🎛️ **[features]** - 功能开关
• `enable_greetings` = True
• `enable_smart_responses` = True
• `enable_help_command` = True
• `enable_config_command` = False

⚡ **[actions]** - Action组件配置
• `greeting_keywords` = ["你好", "hello", "hi", "嗨"]
• `response_probability` = 0.1
• `max_response_length` = 200
• `enable_emoji` = True

💻 **[commands]** - Command组件配置
• `help_prefix` = "📖"
• `config_admin_only` = True
• `command_timeout` = 30

🔬 **[advanced]** - 高级配置
• `cache_enabled` = True
• `cache_ttl` = 3600
• `log_level` = "INFO"
• `performance_monitor` = False

💡 使用 `/config get <key>` 查看具体配置值
💡 使用 `/config set <key> <value>` 修改配置"""
            
            await self.send_text(config_text)
            return True, "显示了配置列表"
            
        except Exception as e:
            await self.send_text(f"❌ 获取配置列表失败：{str(e)}")
            return False, f"获取配置列表失败：{e}"
    
    async def _handle_get_config(self, key: str) -> Tuple[bool, str]:
        """处理获取配置命令"""
        if not key:
            await self.send_text("❌ 请指定要查询的配置键")
            return False, "缺少配置键参数"
        
        try:
            # 验证配置键格式
            if not self._validate_config_key(key):
                await self.send_text(f"❌ 无效的配置键格式：{key}")
                return False, f"无效的配置键：{key}"
            
            # 获取配置值
            config_value = self.get_config(key)
            config_type = type(config_value).__name__
            
            # 格式化显示
            if config_value is None:
                value_display = "null"
            elif isinstance(config_value, str):
                value_display = f'"{config_value}"'
            elif isinstance(config_value, list):
                value_display = f"[{', '.join(map(str, config_value))}]"
            else:
                value_display = str(config_value)
            
            result_text = f"""🔍 **配置查询结果**

🔑 **键**: `{key}`
📄 **值**: {value_display}
🏷️ **类型**: {config_type}

💡 使用 `/config set {key} <新值>` 修改此配置"""
            
            await self.send_text(result_text)
            return True, f"查询了配置：{key}"
            
        except Exception as e:
            await self.send_text(f"❌ 查询配置失败：{str(e)}")
            return False, f"查询配置失败：{e}"
    
    async def _handle_set_config(self, key: str, value: str) -> Tuple[bool, str]:
        """处理设置配置命令"""
        if not key:
            await self.send_text("❌ 请指定要设置的配置键")
            return False, "缺少配置键参数"
        
        if value is None:
            await self.send_text("❌ 请指定要设置的配置值")
            return False, "缺少配置值参数"
        
        try:
            # 验证配置键
            if not self._validate_config_key(key):
                await self.send_text(f"❌ 无效的配置键格式：{key}")
                return False, f"无效的配置键：{key}"
            
            # 检查只读配置
            readonly_keys = ["plugin.config_version", "plugin.plugin_name"]
            if key in readonly_keys:
                await self.send_text(f"❌ 配置 {key} 为只读，无法修改")
                return False, f"只读配置：{key}"
            
            # 获取当前值和类型
            current_value = self.get_config(key)
            
            # 类型转换
            try:
                new_value = self._convert_config_value(value, type(current_value))
            except ValueError as e:
                await self.send_text(f"❌ 配置值类型转换失败：{str(e)}")
                return False, f"类型转换失败：{e}"
            
            # 验证配置值
            if not self._validate_config_value(key, new_value):
                await self.send_text(f"❌ 配置值验证失败：{key} = {new_value}")
                return False, f"配置值验证失败：{key}"
            
            # 这里应该实际更新配置文件
            # 由于这是模板示例，我们只是模拟成功
            
            result_text = f"""✅ **配置更新成功**

🔑 **键**: `{key}`
📄 **旧值**: {current_value}
🆕 **新值**: {new_value}

⚠️ **注意**: 某些配置可能需要重启插件后生效"""
            
            await self.send_text(result_text)
            return True, f"设置了配置：{key} = {new_value}"
            
        except Exception as e:
            await self.send_text(f"❌ 设置配置失败：{str(e)}")
            return False, f"设置配置失败：{e}"
    
    async def _handle_reset_config(self, key: str) -> Tuple[bool, str]:
        """处理重置配置命令"""
        if not key:
            await self.send_text("❌ 请指定要重置的配置键")
            return False, "缺少配置键参数"
        
        try:
            # 验证配置键
            if not self._validate_config_key(key):
                await self.send_text(f"❌ 无效的配置键格式：{key}")
                return False, f"无效的配置键：{key}"
            
            # 获取当前值和默认值
            current_value = self.get_config(key)
            
            # 这里应该从schema获取默认值
            # 为了示例，我们模拟默认值
            default_values = {
                "plugin.debug_mode": False,
                "features.enable_greetings": True,
                "actions.response_probability": 0.1,
                "commands.help_prefix": "📖"
            }
            
            default_value = default_values.get(key, "未知")
            
            result_text = f"""🔄 **配置重置成功**

🔑 **键**: `{key}`
📄 **当前值**: {current_value}
🔙 **默认值**: {default_value}

✅ 配置已重置为默认值"""
            
            await self.send_text(result_text)
            return True, f"重置了配置：{key}"
            
        except Exception as e:
            await self.send_text(f"❌ 重置配置失败：{str(e)}")
            return False, f"重置配置失败：{e}"
    
    def _validate_config_key(self, key: str) -> bool:
        """验证配置键格式"""
        # 配置键应该符合 section.key 的格式
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$"
        return bool(re.match(pattern, key))
    
    def _convert_config_value(self, value: str, target_type: type):
        """转换配置值类型"""
        if target_type == bool:
            if value.lower() in ["true", "1", "yes", "on", "enabled"]:
                return True
            elif value.lower() in ["false", "0", "no", "off", "disabled"]:
                return False
            else:
                raise ValueError(f"无法将 '{value}' 转换为布尔值")
        
        elif target_type == int:
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"无法将 '{value}' 转换为整数")
        
        elif target_type == float:
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"无法将 '{value}' 转换为浮点数")
        
        elif target_type == list:
            # 简单的列表解析，实际应该更复杂
            if value.startswith("[") and value.endswith("]"):
                items = value[1:-1].split(",")
                return [item.strip().strip('"\'') for item in items if item.strip()]
            else:
                return [value]
        
        else:  # str或其他类型
            return value
    
    def _validate_config_value(self, key: str, value) -> bool:
        """验证配置值的有效性"""
        # 特定键的验证规则
        validation_rules = {
            "actions.response_probability": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
            "commands.command_timeout": lambda x: isinstance(x, int) and x > 0,
            "advanced.cache_ttl": lambda x: isinstance(x, int) and x > 0,
            "advanced.log_level": lambda x: x in ["DEBUG", "INFO", "WARNING", "ERROR"]
        }
        
        if key in validation_rules:
            return validation_rules[key](value)
        
        return True  # 默认通过验证
