"""
Command组件测试

测试Command组件的功能：
- 正则表达式匹配
- 参数捕获
- 拦截控制
- 错误处理
"""

import unittest
from unittest.mock import Mock, AsyncMock
import sys
import os

# 添加插件路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.commands.help_command import HelpCommand
from components.commands.config_command import ConfigCommand


class TestHelpCommand(unittest.TestCase):
    """帮助Command测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.command = HelpCommand()
        
        # 模拟配置
        self.mock_config = {
            "features.enable_help_command": True,
            "commands.help_prefix": "📖",
            "plugin.debug_mode": False
        }
        
        # 模拟方法
        self.command.get_config = Mock(side_effect=self._mock_get_config)
        self.command.send_text = AsyncMock()
        
        # 模拟matched_groups
        self.command.matched_groups = {}
    
    def _mock_get_config(self, key, default=None):
        """模拟配置获取"""
        return self.mock_config.get(key, default)
    
    def test_command_basic_properties(self):
        """测试Command基本属性"""
        self.assertIsNotNone(self.command.command_pattern)
        self.assertIsNotNone(self.command.command_help)
        self.assertIsInstance(self.command.command_examples, list)
        self.assertTrue(self.command.intercept_message)
    
    def test_command_pattern_matching(self):
        """测试命令模式匹配"""
        import re
        pattern = self.command.command_pattern
        
        # 测试有效匹配
        valid_commands = [
            "/help",
            "/help actions",
            "/help commands", 
            "/help config",
            "/help all"
        ]
        
        for cmd in valid_commands:
            match = re.match(pattern, cmd)
            self.assertIsNotNone(match, f"命令 '{cmd}' 应该匹配")
        
        # 测试无效匹配
        invalid_commands = [
            "help",           # 缺少斜杠
            "/help invalid",  # 无效主题
            "/help actions extra",  # 额外参数
            "/HELP",          # 大小写不匹配
        ]
        
        for cmd in invalid_commands:
            match = re.match(pattern, cmd)
            self.assertIsNone(match, f"命令 '{cmd}' 不应该匹配")
    
    async def test_execute_general_help(self):
        """测试显示通用帮助"""
        # 不指定主题
        self.command.matched_groups = {"topic": None}
        
        # 执行命令
        success, message = await self.command.execute()
        
        # 验证结果
        self.assertTrue(success)
        self.assertIn("general", message)
        
        # 验证发送了帮助信息
        self.command.send_text.assert_called()
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("插件帮助", sent_text)
    
    async def test_execute_actions_help(self):
        """测试显示Action帮助"""
        self.command.matched_groups = {"topic": "actions"}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("actions", message)
        
        # 验证发送的内容包含Action信息
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("Action组件", sent_text)
    
    async def test_execute_commands_help(self):
        """测试显示Command帮助"""
        self.command.matched_groups = {"topic": "commands"}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("commands", message)
        
        # 验证发送的内容包含Command信息
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("Command组件", sent_text)
    
    async def test_execute_config_help(self):
        """测试显示配置帮助"""
        self.command.matched_groups = {"topic": "config"}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("config", message)
        
        # 验证发送的内容包含配置信息
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("配置说明", sent_text)
    
    async def test_execute_complete_help(self):
        """测试显示完整帮助"""
        self.command.matched_groups = {"topic": "all"}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("all", message)
        
        # 验证调用了多次send_text（显示完整帮助）
        self.assertGreater(self.command.send_text.call_count, 1)
    
    async def test_execute_disabled(self):
        """测试功能禁用时的执行"""
        # 禁用帮助命令功能
        self.mock_config["features.enable_help_command"] = False
        
        success, message = await self.command.execute()
        
        # 应该返回失败
        self.assertFalse(success)
        self.assertIn("禁用", message)
    
    async def test_execute_with_debug(self):
        """测试调试模式下的执行"""
        # 启用调试模式
        self.mock_config["plugin.debug_mode"] = True
        self.command.matched_groups = {"topic": "actions"}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        
        # 验证发送了调试信息
        call_args = [call[0][0] for call in self.command.send_text.call_args_list]
        debug_messages = [msg for msg in call_args if "调试" in msg]
        self.assertGreater(len(debug_messages), 0)


class TestConfigCommand(unittest.TestCase):
    """配置Command测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.command = ConfigCommand()
        
        # 模拟配置
        self.mock_config = {
            "features.enable_config_command": True,
            "commands.config_admin_only": False,  # 简化测试，不检查权限
            "plugin.debug_mode": False
        }
        
        # 模拟方法
        self.command.get_config = Mock(side_effect=self._mock_get_config)
        self.command.send_text = AsyncMock()
        self.command.user_id = "test_user"
        
        # 模拟matched_groups
        self.command.matched_groups = {}
    
    def _mock_get_config(self, key, default=None):
        """模拟配置获取"""
        return self.mock_config.get(key, default)
    
    def test_command_pattern_matching(self):
        """测试复杂的命令模式匹配"""
        import re
        pattern = self.command.command_pattern
        
        # 测试有效匹配
        test_cases = [
            ("/config list", {"action": "list", "key": None, "value": None}),
            ("/config get plugin.enabled", {"action": "get", "key": "plugin.enabled", "value": None}),
            ("/config set debug_mode true", {"action": "set", "key": "debug_mode", "value": "true"}),
            ("/config reset features.greetings", {"action": "reset", "key": "features.greetings", "value": None})
        ]
        
        for cmd, expected_groups in test_cases:
            match = re.match(pattern, cmd)
            self.assertIsNotNone(match, f"命令 '{cmd}' 应该匹配")
            
            groups = match.groupdict()
            for key, expected_value in expected_groups.items():
                self.assertEqual(groups.get(key), expected_value,
                               f"命令 '{cmd}' 的参数 {key} 应该是 {expected_value}")
    
    async def test_execute_list_config(self):
        """测试列出配置"""
        self.command.matched_groups = {"action": "list", "key": None, "value": None}
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("配置列表", message)
        
        # 验证发送了配置列表
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("plugin", sent_text)
    
    async def test_execute_get_config(self):
        """测试获取配置"""
        self.command.matched_groups = {
            "action": "get", 
            "key": "plugin.enabled", 
            "value": None
        }
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("plugin.enabled", message)
        
        # 验证发送了配置值
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("配置查询结果", sent_text)
    
    async def test_execute_get_config_missing_key(self):
        """测试获取配置时缺少键"""
        self.command.matched_groups = {"action": "get", "key": None, "value": None}
        
        success, message = await self.command.execute()
        
        self.assertFalse(success)
        self.assertIn("配置键", message)
    
    async def test_execute_set_config(self):
        """测试设置配置"""
        self.command.matched_groups = {
            "action": "set",
            "key": "plugin.debug_mode", 
            "value": "true"
        }
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("设置", message)
        
        # 验证发送了设置结果
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("配置更新成功", sent_text)
    
    async def test_execute_set_config_readonly(self):
        """测试设置只读配置"""
        self.command.matched_groups = {
            "action": "set",
            "key": "plugin.config_version",
            "value": "2.0.0"
        }
        
        success, message = await self.command.execute()
        
        self.assertFalse(success)
        self.assertIn("只读", message)
    
    async def test_execute_reset_config(self):
        """测试重置配置"""
        self.command.matched_groups = {
            "action": "reset",
            "key": "plugin.debug_mode",
            "value": None
        }
        
        success, message = await self.command.execute()
        
        self.assertTrue(success)
        self.assertIn("重置", message)
        
        # 验证发送了重置结果
        sent_text = self.command.send_text.call_args[0][0]
        self.assertIn("配置重置成功", sent_text)
    
    def test_validate_config_key(self):
        """测试配置键验证"""
        # 有效的配置键
        valid_keys = [
            "plugin.enabled",
            "features.enable_greetings",
            "actions.greeting_keywords",
            "advanced.cache_enabled"
        ]
        
        for key in valid_keys:
            self.assertTrue(self.command._validate_config_key(key),
                           f"配置键 '{key}' 应该有效")
        
        # 无效的配置键
        invalid_keys = [
            "123invalid",      # 以数字开头
            "plugin..enabled", # 双点
            "plugin.",         # 以点结尾
            ".plugin",         # 以点开头
            "plugin-enabled"   # 包含连字符
        ]
        
        for key in invalid_keys:
            self.assertFalse(self.command._validate_config_key(key),
                            f"配置键 '{key}' 应该无效")
    
    def test_convert_config_value_bool(self):
        """测试布尔值转换"""
        # True值
        true_values = ["true", "1", "yes", "on", "enabled", "TRUE"]
        for value in true_values:
            result = self.command._convert_config_value(value, bool)
            self.assertTrue(result, f"'{value}' 应该转换为 True")
        
        # False值
        false_values = ["false", "0", "no", "off", "disabled", "FALSE"]
        for value in false_values:
            result = self.command._convert_config_value(value, bool)
            self.assertFalse(result, f"'{value}' 应该转换为 False")
    
    def test_convert_config_value_int(self):
        """测试整数值转换"""
        self.assertEqual(self.command._convert_config_value("123", int), 123)
        self.assertEqual(self.command._convert_config_value("-456", int), -456)
        
        # 无效的整数
        with self.assertRaises(ValueError):
            self.command._convert_config_value("abc", int)
    
    def test_convert_config_value_list(self):
        """测试列表值转换"""
        # 标准列表格式
        result = self.command._convert_config_value('["a", "b", "c"]', list)
        self.assertEqual(result, ["a", "b", "c"])
        
        # 单个值
        result = self.command._convert_config_value("single", list)
        self.assertEqual(result, ["single"])
    
    def test_validate_config_value(self):
        """测试配置值验证"""
        # 概率值验证
        self.assertTrue(
            self.command._validate_config_value("actions.response_probability", 0.5)
        )
        self.assertFalse(
            self.command._validate_config_value("actions.response_probability", 1.5)
        )
        
        # 日志级别验证
        self.assertTrue(
            self.command._validate_config_value("advanced.log_level", "INFO")
        )
        self.assertFalse(
            self.command._validate_config_value("advanced.log_level", "INVALID")
        )


class TestCommandIntegration(unittest.TestCase):
    """Command集成测试"""
    
    def test_command_pattern_compilation(self):
        """测试命令模式编译"""
        from components.commands.help_command import HelpCommand
        from components.commands.config_command import ConfigCommand
        
        commands = [HelpCommand(), ConfigCommand()]
        
        for command in commands:
            # 模式应该能够编译
            import re
            try:
                re.compile(command.command_pattern)
            except re.error as e:
                self.fail(f"命令 {command.__class__.__name__} 的正则模式无效: {e}")
    
    def test_command_examples_validity(self):
        """测试命令示例的有效性"""
        from components.commands.help_command import HelpCommand
        from components.commands.config_command import ConfigCommand
        
        commands = [HelpCommand(), ConfigCommand()]
        
        for command in commands:
            import re
            pattern = command.command_pattern
            
            # 所有示例都应该匹配模式
            for example in command.command_examples:
                match = re.match(pattern, example)
                self.assertIsNotNone(match,
                    f"命令 {command.__class__.__name__} 的示例 '{example}' 不匹配模式")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
