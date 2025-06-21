"""
插件辅助工具函数

提供通用的工具函数，遵循代码复用原则
"""

import json
import re
from typing import Any, Dict, List, Optional


def validate_json_schema(data: dict, schema: dict) -> tuple[bool, str]:
    """
    验证JSON数据是否符合Schema
    
    Args:
        data: 要验证的数据
        schema: Schema定义
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        # 简单的schema验证实现
        for key, field_type in schema.items():
            if key not in data:
                return False, f"缺少必需字段: {key}"
            
            if not isinstance(data[key], field_type):
                return False, f"字段类型错误: {key} 应为 {field_type.__name__}"
        
        return True, "验证通过"
    except Exception as e:
        return False, f"验证失败: {str(e)}"


def format_config_value(value: Any) -> str:
    """
    格式化配置值用于显示
    
    Args:
        value: 配置值
        
    Returns:
        格式化后的字符串
    """
    if value is None:
        return "null"
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, list):
        return f"[{', '.join(map(str, value))}]"
    elif isinstance(value, bool):
        return "true" if value else "false"
    else:
        return str(value)


def parse_version(version_str: str) -> tuple[int, int, int]:
    """
    解析版本号字符串
    
    Args:
        version_str: 版本号字符串，如 "1.2.3"
        
    Returns:
        (主版本号, 次版本号, 修订号)
    """
    # 移除可能的前缀和后缀
    clean_version = re.sub(r'[^0-9.]', '', version_str)
    parts = clean_version.split('.')
    
    # 确保有三个部分
    while len(parts) < 3:
        parts.append('0')
    
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return 0, 0, 0


def compare_versions(version1: str, version2: str) -> int:
    """
    比较两个版本号
    
    Args:
        version1: 版本号1
        version2: 版本号2
        
    Returns:
        -1: version1 < version2
         0: version1 = version2
         1: version1 > version2
    """
    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)
    
    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    
    return 0


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    清理用户输入
    
    Args:
        text: 输入文本
        max_length: 最大长度
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除危险字符
    sanitized = re.sub(r'[<>"\'\x00-\x1f]', '', text)
    
    # 限制长度
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized.strip()


def extract_keywords(text: str) -> List[str]:
    """
    从文本中提取关键词
    
    Args:
        text: 输入文本
        
    Returns:
        关键词列表
    """
    # 简单的关键词提取实现
    # 实际应用中可能需要更复杂的NLP处理
    
    # 移除标点符号并分词
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean_text.split()
    
    # 过滤停用词（简化版）
    stop_words = {
        '的', '了', '在', '是', '我', '你', '他', '她', '它', '们',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'
    }
    
    keywords = [word for word in words if word not in stop_words and len(word) > 1]
    
    # 去重并保持顺序
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords


def create_error_response(error_type: str, message: str, details: Optional[Dict] = None) -> Dict:
    """
    创建标准错误响应
    
    Args:
        error_type: 错误类型
        message: 错误消息
        details: 详细信息
        
    Returns:
        错误响应字典
    """
    response = {
        "success": False,
        "error_type": error_type,
        "message": message,
        "timestamp": "2025-01-20T12:00:00Z"  # 实际应用中应使用当前时间
    }
    
    if details:
        response["details"] = details
    
    return response


def create_success_response(data: Any, message: str = "操作成功") -> Dict:
    """
    创建标准成功响应
    
    Args:
        data: 响应数据
        message: 成功消息
        
    Returns:
        成功响应字典
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": "2025-01-20T12:00:00Z"  # 实际应用中应使用当前时间
    }


def deep_merge_dict(dict1: Dict, dict2: Dict) -> Dict:
    """
    深度合并两个字典
    
    Args:
        dict1: 字典1
        dict2: 字典2
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    
    return result


class ConfigHelper:
    """配置辅助类"""
    
    @staticmethod
    def validate_config_key(key: str) -> bool:
        """验证配置键格式"""
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$"
        return bool(re.match(pattern, key))
    
    @staticmethod
    def parse_config_path(path: str) -> List[str]:
        """解析配置路径"""
        return path.split('.') if path else []
    
    @staticmethod
    def get_nested_value(data: Dict, path: List[str], default=None):
        """获取嵌套字典的值"""
        current = data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    @staticmethod
    def set_nested_value(data: Dict, path: List[str], value: Any):
        """设置嵌套字典的值"""
        current = data
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value


class PerformanceMonitor:
    """性能监控辅助类"""
    
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, name: str):
        """开始计时"""
        import time
        self.metrics[name] = {"start": time.time()}
    
    def end_timer(self, name: str) -> float:
        """结束计时并返回耗时"""
        import time
        if name in self.metrics:
            elapsed = time.time() - self.metrics[name]["start"]
            self.metrics[name]["elapsed"] = elapsed
            return elapsed
        return 0.0
    
    def get_metrics(self) -> Dict:
        """获取性能指标"""
        return self.metrics.copy()
