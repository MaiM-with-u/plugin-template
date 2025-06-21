#!/usr/bin/env python3
"""
MaiBot插件Manifest验证脚本
严格按照官方文档规范验证_manifest.json的完整性和正确性
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
import re


class ManifestValidator:
    """MaiBot插件manifest.json验证器"""
    
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """验证manifest文件"""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.errors.append(f"无法读取manifest文件: {e}")
            return False
            
        # 按官方文档验证各个字段
        self._validate_manifest_version()
        self._validate_basic_info()
        self._validate_author()
        self._validate_urls()
        self._validate_keywords_categories()
        self._validate_host_application()
        self._validate_locales()
        self._validate_plugin_info()
        
        return len(self.errors) == 0
    
    def _validate_manifest_version(self):
        """验证manifest版本"""
        version = self.manifest.get('manifest_version')
        if version != 3:
            self.errors.append(f"manifest_version必须为3，当前为: {version}")
    
    def _validate_basic_info(self):
        """验证基本信息字段"""
        required_fields = ['name', 'version', 'description']
        for field in required_fields:
            value = self.manifest.get(field)
            if not value or not isinstance(value, str):
                self.errors.append(f"必填字段 '{field}' 缺失或不是字符串")
            elif not value.strip():
                self.errors.append(f"字段 '{field}' 不能为空")
        
        # 验证版本格式
        version = self.manifest.get('version', '')
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            self.errors.append(f"版本号格式无效: {version}，应为 x.y.z 格式")
    
    def _validate_author(self):
        """验证作者信息"""
        author = self.manifest.get('author')
        if not author or not isinstance(author, dict):
            self.errors.append("author字段必须是对象")
            return
            
        if not author.get('name'):
            self.errors.append("author.name是必填字段")
        
        url = author.get('url')
        if url and not self._is_valid_url(url):
            self.warnings.append(f"author.url格式可能无效: {url}")
    
    def _validate_urls(self):
        """验证URL字段"""
        url_fields = ['homepage_url', 'repository_url']
        for field in url_fields:
            url = self.manifest.get(field)
            if url and not self._is_valid_url(url):
                self.warnings.append(f"{field}格式可能无效: {url}")
    
    def _validate_keywords_categories(self):
        """验证关键词和分类"""
        keywords = self.manifest.get('keywords', [])
        if not isinstance(keywords, list):
            self.errors.append("keywords必须是数组")
        elif len(keywords) == 0:
            self.warnings.append("建议添加keywords以提高插件可发现性")
        
        categories = self.manifest.get('categories', [])
        if not isinstance(categories, list):
            self.errors.append("categories必须是数组")
        elif len(categories) == 0:
            self.warnings.append("建议添加categories以分类插件")
    
    def _validate_host_application(self):
        """验证宿主应用要求"""
        host_app = self.manifest.get('host_application')
        if not host_app or not isinstance(host_app, dict):
            self.warnings.append("建议指定host_application版本要求")
            return
        
        min_version = host_app.get('min_version')
        max_version = host_app.get('max_version')
        
        if min_version and not re.match(r'^\d+\.\d+\.\d+$', min_version):
            self.errors.append(f"min_version格式无效: {min_version}")
        
        if max_version and not re.match(r'^\d+\.\d+\.\d+$', max_version):
            self.errors.append(f"max_version格式无效: {max_version}")
    
    def _validate_locales(self):
        """验证本地化设置"""
        default_locale = self.manifest.get('default_locale')
        if default_locale and not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', default_locale):
            self.warnings.append(f"default_locale格式建议为 'xx' 或 'xx-XX': {default_locale}")
        
        locales_path = self.manifest.get('locales_path')
        if locales_path:
            full_path = os.path.join(os.path.dirname(self.manifest_path), locales_path)
            if not os.path.exists(full_path):
                self.warnings.append(f"本地化目录不存在: {locales_path}")
    
    def _validate_plugin_info(self):
        """验证插件信息"""
        plugin_info = self.manifest.get('plugin_info')
        if not plugin_info or not isinstance(plugin_info, dict):
            self.errors.append("plugin_info字段是必需的")
            return
        
        # 验证基本字段
        is_built_in = plugin_info.get('is_built_in')
        if not isinstance(is_built_in, bool):
            self.errors.append("plugin_info.is_built_in必须是布尔值")
        
        plugin_type = plugin_info.get('plugin_type')
        valid_types = ['general', 'game', 'utility', 'entertainment', 'social', 'productivity']
        if plugin_type not in valid_types:
            self.warnings.append(f"plugin_type建议使用标准值: {valid_types}")
        
        # 验证组件信息
        components = plugin_info.get('components', [])
        if not isinstance(components, list):
            self.errors.append("plugin_info.components必须是数组")
        else:
            self._validate_components(components)
    
    def _validate_components(self, components: List[Dict[str, Any]]):
        """验证组件列表"""
        if len(components) == 0:
            self.warnings.append("插件没有定义任何组件")
        
        for i, component in enumerate(components):
            if not isinstance(component, dict):
                self.errors.append(f"组件{i}必须是对象")
                continue
            
            comp_type = component.get('type')
            comp_name = component.get('name')
            comp_desc = component.get('description')
            
            if comp_type not in ['action', 'command', 'tool']:
                self.errors.append(f"组件{i}类型无效: {comp_type}")
            
            if not comp_name or not isinstance(comp_name, str):
                self.errors.append(f"组件{i}缺少有效的name字段")
            
            if not comp_desc or not isinstance(comp_desc, str):
                self.warnings.append(f"组件{i}建议添加description字段")
    
    def _is_valid_url(self, url: str) -> bool:
        """简单的URL格式验证"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def print_results(self):
        """打印验证结果"""
        print("=" * 60)
        print("MaiBot插件Manifest验证结果")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ 发现 {len(self.errors)} 个错误:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️ 发现 {len(self.warnings)} 个警告:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ Manifest验证通过！没有发现任何问题。")
        elif not self.errors:
            print("\n✅ Manifest基本有效，但有一些建议改进的地方。")
        else:
            print("\n❌ Manifest验证失败，请修复上述错误。")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    # 查找manifest文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.dirname(script_dir)
    manifest_path = os.path.join(plugin_dir, '_manifest.json')
    
    if not os.path.exists(manifest_path):
        print(f"❌ 未找到manifest文件: {manifest_path}")
        sys.exit(1)
    
    # 执行验证
    validator = ManifestValidator(manifest_path)
    is_valid = validator.validate()
    validator.print_results()
    
    # 返回适当的退出码
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
