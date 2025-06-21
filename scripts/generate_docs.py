#!/usr/bin/env python3
"""
文档生成脚本
根据插件代码自动生成API文档和使用说明
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

def extract_docstrings(file_path: str) -> Dict[str, str]:
    """从Python文件中提取类和函数的文档字符串"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        docstrings = {}
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Str):
                        docstrings[node.name] = node.body[0].value.s
                    elif isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                        docstrings[node.name] = node.body[0].value.value
        
        return docstrings
    except Exception as e:
        print(f"⚠️  无法解析 {file_path}: {e}")
        return {}

def generate_component_docs(components_dir: str) -> str:
    """生成组件文档"""
    docs = []
    components_path = Path(components_dir)
    
    if not components_path.exists():
        return "未找到 components 目录"
    
    # 遍历actions和commands
    for comp_type in ['actions', 'commands']:
        comp_dir = components_path / comp_type
        if not comp_dir.exists():
            continue
        
        docs.append(f"## {comp_type.title()}\n")
        
        for py_file in comp_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            docs.append(f"### {py_file.stem}\n")
            
            # 提取文档字符串
            docstrings = extract_docstrings(str(py_file))
            
            if docstrings:
                for name, docstring in docstrings.items():
                    docs.append(f"#### {name}\n")
                    docs.append(f"```\n{docstring}\n```\n")
            else:
                docs.append("暂无文档\n")
            
            docs.append("")
    
    return "\n".join(docs)

def generate_api_docs() -> str:
    """生成API文档"""
    template = """# API 文档

## 插件结构

所有插件必须包含以下基本结构：

- `plugin.py`: 主插件类
- `_manifest.json`: 插件元数据
- `components/`: 组件目录
  - `actions/`: Action组件
  - `commands/`: Command组件

## 基类说明

### BaseAction
Action组件的基类，用于处理用户输入和生成响应。

**核心方法：**
- `is_activated(context)`: 判断Action是否应该被激活
- `process(context)`: 处理输入并生成响应

### BaseCommand  
Command组件的基类，用于处理命令式交互。

**核心方法：**
- `matches(text)`: 判断文本是否匹配该命令
- `execute(context)`: 执行命令逻辑

## 配置系统

插件使用Pydantic进行配置管理：

```python
from pydantic import BaseModel

class PluginConfig(BaseModel):
    enabled: bool = True
    debug: bool = False
```

## 生命周期钩子

```python
class MyPlugin(BasePlugin):
    async def on_load(self):
        # 插件加载时调用
        pass
    
    async def on_unload(self):
        # 插件卸载时调用
        pass
```

{component_docs}
"""
    
    component_docs = generate_component_docs("components")
    return template.format(component_docs=component_docs)

def generate_development_docs() -> str:
    """生成开发文档"""
    return """# 开发指南

## 开发环境设置

1. 克隆模板仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 复制配置：`cp config_example.toml config.toml`
4. 运行测试：`pytest tests/`

## 开发流程

### 1. 创建新Action

```python
from src.base_action import BaseAction

class MyAction(BaseAction):
    def __init__(self):
        super().__init__()
        self.name = "my_action"
        self.description = "我的Action"
    
    async def is_activated(self, context):
        # 实现激活逻辑
        return True
    
    async def process(self, context):
        # 实现处理逻辑
        return "响应内容"
```

### 2. 创建新Command

```python
from src.base_processor import BaseCommand

class MyCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "mycommand"
        self.description = "我的命令"
    
    def matches(self, text: str) -> bool:
        return text.startswith("/mycommand")
    
    async def execute(self, context):
        # 实现命令逻辑
        return "命令执行结果"
```

### 3. 注册组件

在 `plugin.py` 中注册你的组件：

```python
def get_actions(self):
    return [MyAction()]

def get_commands(self):
    return [MyCommand()]
```

### 4. 更新Manifest

在 `_manifest.json` 中添加组件声明：

```json
{
  "components": {
    "actions": [
      {
        "name": "my_action",
        "module": "components.actions.my_action"
      }
    ]
  }
}
```

## 最佳实践

1. **配置管理**: 使用Pydantic Schema定义配置
2. **错误处理**: 使用try-catch包装可能出错的代码
3. **日志记录**: 使用插件提供的日志接口
4. **测试**: 为每个组件编写单元测试
5. **文档**: 为所有公共方法编写文档字符串

## 调试技巧

1. 使用 `debug=True` 开启调试模式
2. 查看日志文件了解运行状态
3. 使用pytest进行单元测试
4. 使用validate_manifest.py验证配置

## 常见问题

### Q: 如何访问插件配置？
A: 使用 `self.get_config()` 方法

### Q: 如何在Action间共享数据？
A: 使用插件的状态管理或外部存储

### Q: 如何处理异步操作？
A: 所有处理方法都是async，可以直接使用await
"""

def main():
    """主函数"""
    print("🚀 生成插件文档...")
    
    # 确保docs目录存在
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # 生成API文档
    api_docs = generate_api_docs()
    with open(docs_dir / "API.md", 'w', encoding='utf-8') as f:
        f.write(api_docs)
    print("✅ API.md 已生成")
    
    # 生成开发文档
    dev_docs = generate_development_docs()
    with open(docs_dir / "DEVELOPMENT.md", 'w', encoding='utf-8') as f:
        f.write(dev_docs)
    print("✅ DEVELOPMENT.md 已生成")
    
    # 生成变更日志模板
    changelog = """# 变更日志

## [未发布]

### 新增
- 初始版本

### 修改
- 无

### 修复
- 无

## [1.0.0] - 2024-01-01

### 新增
- 插件基本框架
- 示例Action和Command
- 配置管理系统
- 测试套件
"""
    
    with open(docs_dir / "CHANGELOG.md", 'w', encoding='utf-8') as f:
        f.write(changelog)
    print("✅ CHANGELOG.md 已生成")
    
    print("\n📚 文档生成完成！")
    print(f"   - docs/API.md")
    print(f"   - docs/DEVELOPMENT.md")
    print(f"   - docs/CHANGELOG.md")

if __name__ == "__main__":
    main()
