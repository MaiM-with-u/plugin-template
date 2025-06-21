"""
插件测试文件

测试插件的各个组件功能
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

# 这里需要根据实际的MaiBot导入路径调整
from plugin import TemplatePlugin
from actions.sample_action import SampleAction
from commands.sample_command import SampleCommand


class TestTemplatePlugin:
    """模板插件测试类"""
    
    @pytest.fixture
    async def plugin(self):
        """创建插件实例"""
        plugin = TemplatePlugin("/test/plugin/dir", {})
        await plugin.on_load()
        return plugin
    
    @pytest.mark.asyncio
    async def test_plugin_load(self):
        """测试插件加载"""
        plugin = TemplatePlugin("/test/plugin/dir", {})
        result = await plugin.on_load()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_plugin_unload(self, plugin):
        """测试插件卸载"""
        result = await plugin.on_unload()
        assert result is True
    
    def test_plugin_info(self, plugin):
        """测试插件信息"""
        info = plugin.get_plugin_info()
        assert info["name"] == "Template Plugin"
        assert info["version"] == "1.0.0"
        assert "components" in info


class TestSampleAction:
    """示例动作测试类"""
    
    @pytest.fixture
    def action(self):
        """创建动作实例"""
        return SampleAction()
    
    @pytest.mark.asyncio
    async def test_action_execute(self, action):
        """测试动作执行"""
        context = {"user_input": "这是一个示例测试"}
        result = await action.execute(context)
        
        assert result["success"] is True
        assert "示例动作收到输入" in result["response"]
        assert result["action"] == "sample_action"
    
    @pytest.mark.asyncio
    async def test_action_can_execute(self, action):
        """测试动作执行条件"""
        # 包含关键词的情况
        context = {"user_input": "这是一个示例"}
        can_execute = await action.can_execute(context)
        assert can_execute is True
        
        # 不包含关键词的情况
        context = {"user_input": "这是其他内容"}
        can_execute = await action.can_execute(context)
        assert can_execute is False


class TestSampleCommand:
    """示例命令测试类"""
    
    @pytest.fixture
    def command(self):
        """创建命令实例"""
        return SampleCommand()
    
    @pytest.mark.asyncio
    async def test_command_hello(self, command):
        """测试hello子命令"""
        args = ["hello", "测试"]
        context = {}
        result = await command.execute(args, context)
        
        assert result["success"] is True
        assert "你好, 测试!" in result["response"]
    
    @pytest.mark.asyncio
    async def test_command_echo(self, command):
        """测试echo子命令"""
        args = ["echo", "这是测试文本"]
        context = {}
        result = await command.execute(args, context)
        
        assert result["success"] is True
        assert "回显: 这是测试文本" in result["response"]
    
    @pytest.mark.asyncio
    async def test_command_help(self, command):
        """测试help子命令"""
        args = ["help"]
        context = {}
        result = await command.execute(args, context)
        
        assert result["success"] is True
        assert "示例命令帮助" in result["response"]
    
    @pytest.mark.asyncio
    async def test_command_invalid(self, command):
        """测试无效子命令"""
        args = ["invalid"]
        context = {}
        result = await command.execute(args, context)
        
        assert result["success"] is False
        assert "未知的子命令" in result["response"]
    
    def test_command_info(self, command):
        """测试命令信息"""
        info = command.get_command_info()
        assert info["name"] == "sample"
        assert "hello" in info["subcommands"]
        assert "echo" in info["subcommands"]