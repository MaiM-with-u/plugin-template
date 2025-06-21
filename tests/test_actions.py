"""
Action组件测试

测试Action组件的功能：
- 激活类型和控制
- 执行逻辑
- 配置集成
- 错误处理
"""

import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# 添加插件路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.actions.greeting_action import GreetingAction
from components.actions.smart_response_action import SmartResponseAction
from src.plugin_system import ActionActivationType, ChatMode


class TestGreetingAction(unittest.TestCase):
    """问候Action测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.action = GreetingAction()
        
        # 模拟配置
        self.mock_config = {
            "features.enable_greetings": True,
            "actions.greeting_keywords": ["你好", "hello", "hi"],
            "actions.enable_emoji": True,
            "plugin.debug_mode": False
        }
        
        # 模拟方法
        self.action.get_config = Mock(side_effect=self._mock_get_config)
        self.action.send_text = AsyncMock()
        self.action.store_action_info = AsyncMock()
        
        # 模拟action_data
        self.action.action_data = {}
    
    def _mock_get_config(self, key, default=None):
        """模拟配置获取"""
        return self.mock_config.get(key, default)
    
    def test_action_basic_properties(self):
        """测试Action基本属性"""
        self.assertEqual(self.action.action_name, "greeting_action")
        self.assertEqual(self.action.focus_activation_type, ActionActivationType.LLM_JUDGE)
        self.assertEqual(self.action.normal_activation_type, ActionActivationType.KEYWORD)
        self.assertEqual(self.action.mode_enable, ChatMode.ALL)
        self.assertFalse(self.action.parallel_action)
    
    def test_activation_keywords(self):
        """测试激活关键词"""
        default_keywords = ["你好", "hello", "hi", "嗨"]
        self.assertEqual(self.action.activation_keywords, default_keywords)
        self.assertFalse(self.action.keyword_case_sensitive)
    
    def test_action_parameters(self):
        """测试Action参数定义"""
        parameters = self.action.action_parameters
        
        required_params = ["greeting_type", "user_name", "time_context", "custom_message"]
        for param in required_params:
            self.assertIn(param, parameters)
    
    def test_action_require(self):
        """测试Action使用场景描述"""
        require = self.action.action_require
        self.assertIsInstance(require, list)
        self.assertGreater(len(require), 0)
    
    async def test_execute_success(self):
        """测试成功执行"""
        # 设置Action数据
        self.action.action_data = {
            "greeting_type": "friendly",
            "user_name": "测试用户",
            "time_context": "morning"
        }
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 验证结果
        self.assertTrue(success)
        self.assertIn("friendly", message)
        
        # 验证方法调用
        self.action.send_text.assert_called()
        self.action.store_action_info.assert_called()
    
    async def test_execute_disabled(self):
        """测试功能禁用时的执行"""
        # 禁用问候功能
        self.mock_config["features.enable_greetings"] = False
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 应该返回失败
        self.assertFalse(success)
        self.assertIn("禁用", message)
    
    async def test_execute_with_debug(self):
        """测试调试模式下的执行"""
        # 启用调试模式
        self.mock_config["plugin.debug_mode"] = True
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 应该成功执行
        self.assertTrue(success)
        
        # 应该发送调试信息
        call_args = [call[0][0] for call in self.action.send_text.call_args_list]
        debug_messages = [msg for msg in call_args if "调试" in msg]
        self.assertGreater(len(debug_messages), 0)
    
    async def test_generate_greeting_formal(self):
        """测试生成正式问候"""
        greeting = await self.action._generate_greeting("formal", "用户", "", "")
        
        # 正式问候应该包含敬语
        formal_indicators = ["您好", "您"]
        self.assertTrue(any(indicator in greeting for indicator in formal_indicators))
    
    async def test_generate_greeting_with_time(self):
        """测试带时间的问候"""
        greeting = await self.action._generate_greeting("friendly", "", "morning", "")
        
        # 应该包含时间相关的问候
        time_indicators = ["早上好", "上午好", "Good morning"]
        self.assertTrue(any(indicator in greeting for indicator in time_indicators))
    
    async def test_generate_greeting_custom(self):
        """测试自定义问候消息"""
        custom_message = "自定义问候内容"
        greeting = await self.action._generate_greeting("friendly", "", "", custom_message)
        
        # 应该返回自定义消息
        self.assertEqual(greeting, custom_message)


class TestSmartResponseAction(unittest.TestCase):
    """智能回复Action测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.action = SmartResponseAction()
        
        # 模拟配置
        self.mock_config = {
            "features.enable_smart_responses": True,
            "actions.response_probability": 0.2,
            "actions.max_response_length": 150,
            "advanced.cache_enabled": True,
            "advanced.performance_monitor": False,
            "plugin.debug_mode": False
        }
        
        # 模拟方法
        self.action.get_config = Mock(side_effect=self._mock_get_config)
        self.action.send_text = AsyncMock()
        self.action.store_action_info = AsyncMock()
        
        # 模拟action_data
        self.action.action_data = {}
    
    def _mock_get_config(self, key, default=None):
        """模拟配置获取"""
        return self.mock_config.get(key, default)
    
    def test_action_basic_properties(self):
        """测试Action基本属性"""
        self.assertEqual(self.action.action_name, "smart_response_action")
        self.assertEqual(self.action.focus_activation_type, ActionActivationType.LLM_JUDGE)
        self.assertEqual(self.action.normal_activation_type, ActionActivationType.RANDOM)
        self.assertEqual(self.action.mode_enable, ChatMode.ALL)
        self.assertTrue(self.action.parallel_action)
    
    def test_random_activation_probability(self):
        """测试随机激活概率"""
        self.assertEqual(self.action.random_activation_probability, 0.1)
    
    async def test_execute_success(self):
        """测试成功执行"""
        # 设置Action数据
        self.action.action_data = {
            "response_type": "informative",
            "context_depth": "medium",
            "tone": "friendly"
        }
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 验证结果
        self.assertTrue(success)
        self.assertIn("informative", message)
        
        # 验证方法调用
        self.action.send_text.assert_called()
        self.action.store_action_info.assert_called()
    
    async def test_execute_with_cache(self):
        """测试缓存功能"""
        # 启用缓存
        self.mock_config["advanced.cache_enabled"] = True
        
        # 预设缓存内容
        cache_key = "informative_medium_friendly"
        self.action._response_cache[cache_key] = "缓存的回复内容"
        
        # 设置匹配的Action数据
        self.action.action_data = {
            "response_type": "informative",
            "context_depth": "medium", 
            "tone": "friendly"
        }
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 应该成功并使用缓存
        self.assertTrue(success)
        self.assertIn("缓存", message)
    
    async def test_execute_length_limit(self):
        """测试回复长度限制"""
        # 设置较小的长度限制
        self.mock_config["actions.max_response_length"] = 50
        
        # 设置Action数据
        self.action.action_data = {
            "response_type": "informative",
            "max_length": 50
        }
        
        # 执行Action
        success, message = await self.action.execute()
        
        # 验证成功执行
        self.assertTrue(success)
        
        # 验证发送的文本长度
        sent_text = self.action.send_text.call_args[0][0]
        self.assertLessEqual(len(sent_text), 53)  # 50 + "..."
    
    async def test_generate_smart_response_types(self):
        """测试不同类型的智能回复生成"""
        response_types = ["informative", "supportive", "creative", "analytical"]
        
        for response_type in response_types:
            response = await self.action._generate_smart_response(
                response_type, "medium", "friendly", 200, False
            )
            
            # 回复不应该为空
            self.assertGreater(len(response), 0)
            self.assertIsInstance(response, str)
    
    async def test_generate_smart_response_with_examples(self):
        """测试包含示例的回复生成"""
        response = await self.action._generate_smart_response(
            "informative", "deep", "formal", 200, True
        )
        
        # 应该包含示例相关的内容
        self.assertIn("例", response)
    
    async def test_cleanup_expired_cache(self):
        """测试过期缓存清理"""
        # 设置缓存内容
        self.action._response_cache = {
            "key1": "value1",
            "key2": "value2"
        }
        
        # 模拟缓存过期（设置很长时间前的清理时间）
        import time
        self.action._last_cache_clear = time.time() - 7200  # 2小时前
        
        # 执行缓存清理
        await self.action._cleanup_expired_cache()
        
        # 缓存应该被清理
        self.assertEqual(len(self.action._response_cache), 0)


class TestActionIntegration(unittest.TestCase):
    """Action集成测试"""
    
    def test_action_info_generation(self):
        """测试Action信息生成"""
        from components.actions.greeting_action import GreetingAction
        
        # 测试静态方法存在（如果有的话）
        action = GreetingAction()
        self.assertIsNotNone(action.action_name)
        self.assertIsNotNone(action.action_description)
    
    def test_action_configuration_integration(self):
        """测试Action与配置系统的集成"""
        from components.actions.greeting_action import GreetingAction
        from components.actions.smart_response_action import SmartResponseAction
        
        actions = [GreetingAction(), SmartResponseAction()]
        
        for action in actions:
            # 每个Action都应该有必需的属性
            required_attrs = [
                'action_name', 'action_description', 'action_parameters',
                'action_require', 'associated_types', 'focus_activation_type',
                'normal_activation_type', 'mode_enable', 'parallel_action'
            ]
            
            for attr in required_attrs:
                self.assertTrue(hasattr(action, attr), 
                              f"Action {action.__class__.__name__} 缺少属性: {attr}")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
