"""
智能问候Action - 官方文档最佳实践示例

展示内容：
- 两层决策机制（激活控制+使用决策）  
- 多种激活类型的正确使用
- 聊天模式控制
- 配置驱动的行为
- 错误处理最佳实践
"""

from src.plugin_system import BaseAction, ActionActivationType, ChatMode
from typing import Tuple
import random


class GreetingAction(BaseAction):
    """
    智能问候Action
    
    遵循官方文档的Action设计原则：
    - 单一职责：专注于问候功能
    - 智能激活：结合关键词和LLM判断
    - 配置驱动：行为可通过配置调整
    - 错误处理：完善的异常处理机制
    """
    
    # ==================== 激活控制（第一层决策） ====================
    # 专注模式：使用LLM智能判断何时激活
    focus_activation_type = ActionActivationType.LLM_JUDGE
    
    # 普通模式：使用关键词快速激活
    normal_activation_type = ActionActivationType.KEYWORD
    
    # 启用的聊天模式
    mode_enable = ChatMode.ALL
    
    # 不允许与其他Action并行执行
    parallel_action = False
    
    # ==================== 关键词激活配置 ====================
    # 关键词将从配置中动态获取
    activation_keywords = ["你好", "hello", "hi", "嗨"]  # 默认值，实际使用配置
    keyword_case_sensitive = False
    
    # ==================== LLM判断配置 ====================
    llm_judge_prompt = """
    判定是否需要使用问候动作的条件：
    1. 用户发送了问候语或打招呼的消息
    2. 用户表达了友好的开场白
    3. 对话刚开始，适合问候
    4. 用户使用了礼貌的称呼
    
    请回答"是"或"否"。
    """
    
    # ==================== 基本信息 ====================
    action_name = "greeting_action"
    action_description = "智能问候Action，根据用户问候提供友好回应"
    
    # ==================== 功能定义（第二层决策） ====================
    action_parameters = {
        "greeting_type": "问候类型（formal/casual/friendly）",
        "user_name": "用户姓名（可选）",
        "time_context": "时间上下文（morning/afternoon/evening）",
        "custom_message": "自定义问候消息（可选）"
    }
    
    action_require = [
        "当用户发送问候语时使用",
        "适合在对话开始时建立友好氛围",
        "根据时间和用户偏好调整问候方式",
        "不要在同一对话中重复过多问候",
        "保持问候的自然性和多样性"
    ]
    
    associated_types = ["text", "emoji"]
    
    # ==================== 执行逻辑 ====================
    async def execute(self) -> Tuple[bool, str]:
        """
        执行智能问候
        
        遵循官方文档的执行方法最佳实践：
        - 完整的错误处理
        - 配置驱动的行为
        - 清晰的返回值
        - 适当的日志记录
        """
        try:
            # 检查功能是否启用
            if not self.get_config("features.enable_greetings", True):
                return False, "问候功能已禁用"
            
            # 获取配置
            greeting_keywords = self.get_config("actions.greeting_keywords", 
                                              ["你好", "hello", "hi", "嗨"])
            enable_emoji = self.get_config("actions.enable_emoji", True)
            debug_mode = self.get_config("plugin.debug_mode", False)
            
            # 更新激活关键词（配置驱动）
            self.activation_keywords = greeting_keywords
            
            # 获取Action参数
            greeting_type = self.action_data.get("greeting_type", "friendly")
            user_name = self.action_data.get("user_name", "")
            time_context = self.action_data.get("time_context", "")
            custom_message = self.action_data.get("custom_message", "")
            
            # 调试信息
            if debug_mode:
                await self.send_text(f"🔍 调试：问候类型={greeting_type}, 用户={user_name}")
            
            # 生成问候消息
            greeting_message = await self._generate_greeting(
                greeting_type, user_name, time_context, custom_message
            )
            
            # 发送问候消息
            await self.send_text(greeting_message)
            
            # 根据配置添加表情
            if enable_emoji:
                emoji_list = ["😊", "👋", "🌟", "💫", "✨"]
                selected_emoji = random.choice(emoji_list)
                # 注意：这里应该使用 send_text 而不是 send_emoji，因为示例中没有表情包文件
                await self.send_text(selected_emoji)
            
            # 记录动作信息
            await self.store_action_info(
                action_build_into_prompt=True,
                action_prompt_display=f"发送了问候消息：{greeting_message[:50]}...",
                action_done=True,
                greeting_type=greeting_type,
                user_mentioned=bool(user_name)
            )
            
            return True, f"成功发送问候消息，类型：{greeting_type}"
            
        except Exception as e:
            # 错误处理
            error_msg = f"问候Action执行失败: {str(e)}"
            
            # 调试模式下显示详细错误
            if self.get_config("plugin.debug_mode", False):
                await self.send_text(f"❌ {error_msg}")
            
            return False, error_msg
    
    # ==================== 私有方法 ====================
    async def _generate_greeting(self, greeting_type: str, user_name: str, 
                               time_context: str, custom_message: str) -> str:
        """
        生成问候消息
        
        根据参数和配置生成合适的问候消息
        """
        if custom_message:
            return custom_message
        
        # 时间相关的问候
        time_greetings = {
            "morning": ["早上好", "上午好", "Good morning"],
            "afternoon": ["下午好", "Good afternoon"],
            "evening": ["晚上好", "Good evening", "晚安"]
        }
        
        # 根据类型选择问候方式
        if greeting_type == "formal":
            base_greetings = ["您好", "很高兴见到您", "欢迎"]
        elif greeting_type == "casual":
            base_greetings = ["嗨", "你好呀", "Hey"]
        else:  # friendly
            base_greetings = ["你好", "很高兴遇到你", "Hi there"]
        
        # 组合问候消息
        if time_context and time_context in time_greetings:
            greeting_options = time_greetings[time_context]
        else:
            greeting_options = base_greetings
        
        selected_greeting = random.choice(greeting_options)
        
        # 添加用户名
        if user_name:
            selected_greeting += f"，{user_name}"
        
        # 添加友好的后缀
        friendly_suffixes = ["！", "~", "！😊", "！很高兴见到你"]
        selected_greeting += random.choice(friendly_suffixes)
        
        return selected_greeting
