"""
智能回复Action - 官方文档高级特性示例

展示内容：
- 随机激活机制
- LLM_JUDGE智能判断
- 配置驱动的复杂行为
- 性能优化最佳实践
- 缓存机制的使用
"""

from src.plugin_system import BaseAction, ActionActivationType, ChatMode
from typing import Tuple
import random
import time


class SmartResponseAction(BaseAction):
    """
    智能回复Action
    
    展示高级Action特性：
    - 多种激活类型组合使用
    - 复杂的配置驱动行为
    - 性能优化和缓存
    - 智能内容生成
    """
    
    # ==================== 激活控制 ====================
    # 专注模式：LLM智能判断
    focus_activation_type = ActionActivationType.LLM_JUDGE
    
    # 普通模式：随机激活，增加行为随机性
    normal_activation_type = ActionActivationType.RANDOM
    
    # 所有模式下都可激活
    mode_enable = ChatMode.ALL
    
    # 允许与其他Action并行执行
    parallel_action = True
    
    # ==================== 随机激活配置 ====================
    # 概率将从配置中动态获取
    random_activation_probability = 0.1  # 默认10%概率
    
    # ==================== LLM判断配置 ====================
    llm_judge_prompt = """
    判定是否需要使用智能回复动作的条件：
    1. 用户提出了问题或需要建议
    2. 对话内容比较复杂，需要深入回应
    3. 用户表达了情绪，需要情感支持
    4. 当前回复可能不够充分，需要补充
    5. 用户在讨论专业话题，需要相关知识
    
    排除条件：
    1. 用户只是简单打招呼
    2. 对话刚开始，信息还不够
    3. 已经有其他Action在处理
    
    请回答"是"或"否"。
    """
    
    # ==================== 基本信息 ====================
    action_name = "smart_response_action"
    action_description = "智能回复Action，根据对话内容生成相关的补充回复"
    
    # ==================== 功能定义 ====================
    action_parameters = {
        "response_type": "回复类型（informative/supportive/creative/analytical）",
        "context_depth": "上下文深度（shallow/medium/deep）",
        "tone": "回复语调（formal/casual/friendly/professional）",
        "max_length": "最大回复长度",
        "include_examples": "是否包含示例（true/false）"
    }
    
    action_require = [
        "当用户需要额外信息或支持时使用",
        "适合补充对话中的空白信息",
        "可以提供相关的建议或见解",
        "避免与主要回复重复",
        "保持回复的相关性和有用性",
        "不要在简单对话中过度使用"
    ]
    
    associated_types = ["text", "image"]
    
    # ==================== 缓存和性能 ====================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response_cache = {}
        self._last_cache_clear = time.time()
    
    # ==================== 执行逻辑 ====================
    async def execute(self) -> Tuple[bool, str]:
        """
        执行智能回复
        
        展示高级功能：
        - 缓存机制使用
        - 性能监控
        - 复杂配置处理
        - 智能内容生成
        """
        try:
            start_time = time.time()
            
            # 检查功能是否启用
            if not self.get_config("features.enable_smart_responses", True):
                return False, "智能回复功能已禁用"
            
            # 获取配置
            response_probability = self.get_config("actions.response_probability", 0.1)
            max_response_length = self.get_config("actions.max_response_length", 200)
            cache_enabled = self.get_config("advanced.cache_enabled", True)
            performance_monitor = self.get_config("advanced.performance_monitor", False)
            debug_mode = self.get_config("plugin.debug_mode", False)
            
            # 更新随机激活概率（配置驱动）
            self.random_activation_probability = response_probability
            
            # 获取Action参数
            response_type = self.action_data.get("response_type", "informative")
            context_depth = self.action_data.get("context_depth", "medium")
            tone = self.action_data.get("tone", "friendly")
            max_length = self.action_data.get("max_length", max_response_length)
            include_examples = self.action_data.get("include_examples", False)
            
            # 调试信息
            if debug_mode:
                await self.send_text(
                    f"🤖 智能回复：类型={response_type}, 深度={context_depth}, 语调={tone}"
                )
            
            # 检查缓存
            cache_key = f"{response_type}_{context_depth}_{tone}"
            if cache_enabled and cache_key in self._response_cache:
                cached_response = self._response_cache[cache_key]
                await self.send_text(cached_response)
                
                if debug_mode:
                    await self.send_text("📋 使用了缓存回复")
                
                return True, "发送了缓存的智能回复"
            
            # 清理过期缓存
            if cache_enabled:
                await self._cleanup_expired_cache()
            
            # 生成智能回复
            smart_response = await self._generate_smart_response(
                response_type, context_depth, tone, max_length, include_examples
            )
            
            # 限制长度
            if len(smart_response) > max_length:
                smart_response = smart_response[:max_length] + "..."
            
            # 发送回复
            await self.send_text(smart_response)
            
            # 更新缓存
            if cache_enabled:
                self._response_cache[cache_key] = smart_response
            
            # 记录动作信息
            await self.store_action_info(
                action_build_into_prompt=True,
                action_prompt_display=f"提供了智能回复：{smart_response[:30]}...",
                action_done=True,
                response_type=response_type,
                response_length=len(smart_response),
                from_cache=cache_key in self._response_cache
            )
            
            # 性能监控
            if performance_monitor:
                execution_time = time.time() - start_time
                if execution_time > 2.0:  # 如果执行时间超过2秒
                    await self.send_text(f"⚠️ 性能警告：执行时间 {execution_time:.2f}s")
            
            return True, f"成功生成智能回复，类型：{response_type}"
            
        except Exception as e:
            error_msg = f"智能回复Action执行失败: {str(e)}"
            
            if self.get_config("plugin.debug_mode", False):
                await self.send_text(f"❌ {error_msg}")
            
            return False, error_msg
    
    # ==================== 私有方法 ====================
    async def _generate_smart_response(self, response_type: str, context_depth: str, 
                                     tone: str, max_length: int, include_examples: bool) -> str:
        """
        生成智能回复内容
        
        根据参数生成不同类型的回复
        """
        # 基础回复模板
        response_templates = {
            "informative": [
                "关于这个话题，我了解到一些有趣的信息...",
                "补充一下相关的背景知识：",
                "这让我想到了一些相关的内容："
            ],
            "supportive": [
                "我理解你的想法，这确实是一个值得考虑的问题。",
                "你的观点很有意思，我想分享一些相关的想法：",
                "从另一个角度来看，也许可以这样考虑："
            ],
            "creative": [
                "这激发了我的一些创意想法：",
                "从创意的角度来看，我们可以这样思考：",
                "让我分享一个有趣的想法："
            ],
            "analytical": [
                "从分析的角度来看，这个问题有几个维度：",
                "让我们深入分析一下这个情况：",
                "数据表明这种现象背后可能有以下原因："
            ]
        }
        
        # 选择基础模板
        templates = response_templates.get(response_type, response_templates["informative"])
        base_response = random.choice(templates)
        
        # 根据语调调整
        if tone == "formal":
            base_response = base_response.replace("我", "本系统").replace("你", "您")
        elif tone == "casual":
            base_response += " 😊"
        
        # 添加内容深度
        if context_depth == "deep":
            base_response += "\n\n深入来看，这个话题涉及多个层面的考虑..."
        elif context_depth == "medium":
            base_response += "\n\n这其中有一些重要的要点值得注意。"
        
        # 添加示例
        if include_examples:
            base_response += "\n\n举个例子来说..."
        
        return base_response
    
    async def _cleanup_expired_cache(self):
        """清理过期缓存"""
        current_time = time.time()
        cache_ttl = self.get_config("advanced.cache_ttl", 3600)
        
        # 每小时清理一次
        if current_time - self._last_cache_clear > cache_ttl:
            self._response_cache.clear()
            self._last_cache_clear = current_time
            
            if self.get_config("plugin.debug_mode", False):
                await self.send_text("🗑️ 已清理过期缓存")
