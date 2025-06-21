"""
插件核心功能测试

测试插件的基本功能：
- 插件加载和卸载
- 配置系统
- 组件注册
- 生命周期管理
"""

import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# 添加插件路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugin import ExampleTemplatePlugin


class TestExampleTemplatePlugin(unittest.TestCase):
    """插件核心功能测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.plugin = ExampleTemplatePlugin()
        
        # 模拟配置
        self.mock_config = {
            "plugin": {
                "enabled": True,
                "config_version": "1.0.0",
                "debug_mode": False
            },
            "features": {
                "enable_greetings": True,
                "enable_smart_responses": True,
                "enable_help_command": True,
                "enable_config_command": False
            }
        }
        
        # 模拟get_config方法
        self.plugin.get_config = Mock(side_effect=self._mock_get_config)
    
    def _mock_get_config(self, key, default=None):
        """模拟配置获取"""
        keys = key.split('.')
        current = self.mock_config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def test_plugin_basic_info(self):
        """测试插件基本信息"""
        self.assertEqual(self.plugin.plugin_name, "example_template_plugin")
        self.assertEqual(self.plugin.plugin_version, "1.0.0")
        self.assertEqual(self.plugin.plugin_author, "MaiBot开发团队")
        self.assertTrue(self.plugin.enable_plugin)
    
    def test_config_schema_structure(self):
        """测试配置Schema结构"""
        schema = self.plugin.config_schema
        
        # 检查必需的配置节
        required_sections = ["plugin", "features", "actions", "commands", "advanced"]
        for section in required_sections:
            self.assertIn(section, schema, f"缺少配置节: {section}")
        
        # 检查plugin节的必需字段
        plugin_section = schema["plugin"]
        self.assertIn("enabled", plugin_section)
        self.assertIn("config_version", plugin_section)
        self.assertIn("debug_mode", plugin_section)
    
    def test_config_section_descriptions(self):
        """测试配置节描述"""
        descriptions = self.plugin.config_section_descriptions
        
        # 检查所有配置节都有描述
        for section in self.plugin.config_schema.keys():
            self.assertIn(section, descriptions, f"配置节 {section} 缺少描述")
    
    def test_get_plugin_components_enabled(self):
        """测试启用状态下的组件注册"""
        components = self.plugin.get_plugin_components()
        
        # 应该注册Action和Command组件
        self.assertGreater(len(components), 0, "应该注册至少一个组件")
        
        # 检查组件类型
        component_types = [comp[1].__name__ for comp in components]
        self.assertIn("GreetingAction", component_types)
        self.assertIn("SmartResponseAction", component_types)
        self.assertIn("HelpCommand", component_types)
    
    def test_get_plugin_components_disabled(self):
        """测试禁用状态下的组件注册"""
        # 禁用插件
        self.mock_config["plugin"]["enabled"] = False
        
        components = self.plugin.get_plugin_components()
        
        # 插件禁用时不应该注册任何组件
        self.assertEqual(len(components), 0, "插件禁用时不应该注册组件")
    
    def test_get_plugin_components_feature_disabled(self):
        """测试功能禁用状态下的组件注册"""
        # 禁用问候功能
        self.mock_config["features"]["enable_greetings"] = False
        
        components = self.plugin.get_plugin_components()
        component_types = [comp[1].__name__ for comp in components]
        
        # 问候Action不应该被注册
        self.assertNotIn("GreetingAction", component_types)
        
        # 其他组件应该正常注册
        self.assertIn("SmartResponseAction", component_types)
        self.assertIn("HelpCommand", component_types)
    
    @patch.object(ExampleTemplatePlugin, '_init_performance_monitor')
    async def test_on_plugin_load_with_performance_monitor(self, mock_init_monitor):
        """测试性能监控初始化"""
        # 启用性能监控
        self.mock_config["advanced"] = {"performance_monitor": True}
        
        await self.plugin.on_plugin_load()
        
        # 应该调用性能监控初始化
        mock_init_monitor.assert_called_once()
    
    @patch.object(ExampleTemplatePlugin, '_cleanup_cache')
    async def test_on_plugin_unload_with_cache(self, mock_cleanup_cache):
        """测试缓存清理"""
        # 启用缓存
        self.mock_config["advanced"] = {"cache_enabled": True}
        
        await self.plugin.on_plugin_unload()
        
        # 应该调用缓存清理
        mock_cleanup_cache.assert_called_once()
    
    def test_config_field_types(self):
        """测试配置字段类型定义"""
        from src.plugin_system.base.config_types import ConfigField
        
        schema = self.plugin.config_schema
        
        # 检查所有字段都是ConfigField类型
        def check_config_fields(section):
            for key, field in section.items():
                self.assertIsInstance(field, ConfigField, 
                                    f"配置字段 {key} 应该是 ConfigField 类型")
                
                # 检查必需属性
                self.assertIsNotNone(field.type, f"字段 {key} 缺少类型定义")
                self.assertIsNotNone(field.default, f"字段 {key} 缺少默认值")
                self.assertIsNotNone(field.description, f"字段 {key} 缺少描述")
        
        for section_name, section in schema.items():
            check_config_fields(section)
    
    def test_config_default_values(self):
        """测试配置默认值的合理性"""
        schema = self.plugin.config_schema
        
        # 检查布尔类型的默认值
        bool_fields = {
            "plugin.enabled": True,
            "plugin.debug_mode": False,
            "features.enable_greetings": True,
            "actions.enable_emoji": True
        }
        
        for field_path, expected_default in bool_fields.items():
            keys = field_path.split('.')
            field = schema[keys[0]][keys[1]]
            self.assertEqual(field.default, expected_default, 
                           f"字段 {field_path} 的默认值应该是 {expected_default}")
    
    def test_config_choices_validation(self):
        """测试配置选择项验证"""
        schema = self.plugin.config_schema
        
        # 检查有选择项的字段
        log_level_field = schema["advanced"]["log_level"]
        self.assertIsNotNone(log_level_field.choices, "log_level 应该有选择项")
        
        expected_choices = ["DEBUG", "INFO", "WARNING", "ERROR"]
        self.assertEqual(log_level_field.choices, expected_choices,
                        "log_level 的选择项不正确")
        
        # 默认值应该在选择项中
        self.assertIn(log_level_field.default, log_level_field.choices,
                     "默认值应该在选择项中")


class TestPluginConfiguration(unittest.TestCase):
    """插件配置系统测试"""
    
    def test_config_version_management(self):
        """测试配置版本管理"""
        plugin = ExampleTemplatePlugin()
        
        # 检查配置版本字段存在
        config_version_field = plugin.config_schema["plugin"]["config_version"]
        self.assertEqual(config_version_field.default, "1.0.0")
        self.assertEqual(config_version_field.type, str)
    
    def test_config_file_name(self):
        """测试配置文件名"""
        plugin = ExampleTemplatePlugin()
        self.assertEqual(plugin.config_file_name, "config.toml")
    
    def test_section_descriptions_completeness(self):
        """测试配置节描述的完整性"""
        plugin = ExampleTemplatePlugin()
        
        schema_sections = set(plugin.config_schema.keys())
        description_sections = set(plugin.config_section_descriptions.keys())
        
        # 所有Schema节都应该有描述
        missing_descriptions = schema_sections - description_sections
        self.assertEqual(len(missing_descriptions), 0,
                        f"以下配置节缺少描述: {missing_descriptions}")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
