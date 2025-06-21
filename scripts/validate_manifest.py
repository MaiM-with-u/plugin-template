#!/usr/bin/env python3
"""
插件Manifest验证脚本

用于验证插件的_manifest.json文件是否符合规范
"""

import json
import os
import sys
import re
from typing import Dict, Any


class ManifestValidator:
    """简化版的Manifest验证器"""
    
    REQUIRED_FIELDS = [
        "manifest_version",
        "name", 
        "version",
        "description",
        "author"
    ]
    
    SUPPORTED_MANIFEST_VERSIONS = [3]
    
    def validate_manifest_file(self, manifest_path: str) -> bool:
        """验证manifest文件"""
        if not os.path.exists(manifest_path):
            print(f"❌ Manifest文件不存在: {manifest_path}")
            return False
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Manifest文件JSON格式错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 读取manifest文件失败: {e}")
            return False
        
        return self.validate_manifest_data(manifest_data)
    
    def validate_manifest_data(self, data: Dict[str, Any]) -> bool:
        """验证manifest数据"""
        errors = []
        warnings = []
        
        # 检查必需字段
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"缺少必需字段: {field}")
            elif not data[field]:
                errors.append(f"必需字段不能为空: {field}")
        
        # 检查manifest版本
        if "manifest_version" in data:
            version = data["manifest_version"]
            if version not in self.SUPPORTED_MANIFEST_VERSIONS:
                errors.append(f"不支持的manifest版本: {version}")
        
        # 检查版本号格式
        if "version" in data:
            version = data["version"]
            if not re.match(r'^\d+\.\d+\.\d+(-\w+\.\d+)?$', version):
                warnings.append(f"版本号格式建议使用语义化版本: {version}")
        
        # 输出结果
        if errors:
            print("❌ Manifest验证失败:")
            for error in errors:
                print(f"   • {error}")
        
        if warnings:
            print("⚠️  Manifest警告:")
            for warning in warnings:
                print(f"   • {warning}")
        
        if not errors and not warnings:
            print("✅ Manifest验证通过")
        
        return len(errors) == 0


def main():
    """主函数"""
    manifest_path = "_manifest.json"
    
    if len(sys.argv) > 1:
        manifest_path = sys.argv[1]
    
    validator = ManifestValidator()
    success = validator.validate_manifest_file(manifest_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()