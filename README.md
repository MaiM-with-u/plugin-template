# MaiBot 标准插件模板

> 基于官方文档的MaiBot插件开发标准模板，包含Action/Command/配置Schema的最佳实践和推荐结构。

## 📦 模板结构

```
plugin-template/
├── plugin.py                    # 主插件文件
├── _manifest.json              # 插件元数据（强制要求）
├── README.md                   # 本文档
├── requirements.txt            # Python依赖
├── .gitignore                  # Git忽略文件
├── config_example.toml         # 配置示例（仅供参考）
├── components/                 # 组件目录
│   ├── __init__.py
│   ├── actions/                # Action组件
│   │   ├── __init__.py
│   │   ├── greeting_action.py  # 示例Action
│   │   └── smart_response_action.py
│   └── commands/               # Command组件
│       ├── __init__.py
│       ├── help_command.py     # 示例Command
│       └── config_command.py
├── utils/                      # 工具模块
│   ├── __init__.py
│   └── helpers.py
├── tests/                      # 测试目录
│   ├── __init__.py
│   ├── test_plugin.py          # 插件测试
│   ├── test_actions.py         # Action测试
│   └── test_commands.py        # Command测试
└── scripts/                    # 脚本目录
    ├── validate_manifest.py    # Manifest验证脚本
    └── generate_docs.py        # 文档生成脚本
```

## 🚀 快速开始

### 1. 使用模板

```bash
# 克隆模板
git clone <template-repo> my-plugin
cd my-plugin

# 安装依赖
pip install -r requirements.txt

# 验证manifest
python scripts/validate_manifest.py

# 运行测试
python -m pytest tests/
```

### 2. 自定义插件

1. **修改基本信息**：编辑 `plugin.py` 中的插件元数据
2. **更新manifest**：修改 `_manifest.json` 中的插件信息
3. **实现组件**：在 `components/` 目录下添加您的Action和Command
4. **配置Schema**：定义插件的配置结构
5. **测试验证**：运行测试确保功能正常

## 📋 官方文档遵循情况

### ✅ Manifest机制
- ✅ 强制要求 `_manifest.json` 文件
- ✅ 包含所有必需字段和可选字段
- ✅ 支持版本兼容性检查
- ✅ 符合语义化版本规范

### ✅ 配置系统
- ✅ Schema驱动的配置生成
- ✅ 支持配置版本管理
- ✅ 自动配置迁移
- ✅ 绝不手动创建config.toml

### ✅ Action组件
- ✅ 两层决策机制（激活控制+使用决策）
- ✅ 完整的激活类型支持
- ✅ 聊天模式控制
- ✅ 智能参数定义

### ✅ Command组件
- ✅ 正则表达式匹配
- ✅ 参数捕获机制
- ✅ 拦截控制支持
- ✅ 错误处理最佳实践

### ✅ 开发规范
- ✅ 符合项目代码风格
- ✅ 完善的错误处理
- ✅ 详细的文档注释
- ✅ 全面的单元测试

## 🎯 最佳实践

### Action设计原则
- **智能激活**：合理选择激活类型，避免过度激活
- **单一职责**：每个Action只负责一个明确的功能
- **清晰描述**：提供准确的action_require帮助LLM决策
- **错误处理**：妥善处理执行过程中的异常情况

### Command设计原则
- **命令直观**：使用清晰的命令格式（动作+对象+参数）
- **参数验证**：早期验证参数有效性
- **帮助完整**：提供详细的帮助信息和示例
- **拦截控制**：合理设置拦截行为

### 配置管理原则
- **Schema优先**：所有配置项都在config_schema中声明
- **版本管理**：及时更新config_version
- **默认安全**：提供合理的默认值
- **文档自动**：依靠Schema生成配置文档

## 📖 开发指南

详细的开发指南请参考：
- [开发指南](docs/DEVELOPMENT.md)
- [API文档](docs/API.md)
- [官方文档](https://docs.mai-mai.org/develop/plugin_develop/)

## 🔧 脚本工具

### Manifest验证
```bash
python scripts/validate_manifest.py
```

### 文档生成
```bash
python scripts/generate_docs.py
```

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_actions.py

# 测试覆盖率
python -m pytest tests/ --cov=components
```

## 📄 许可证

本模板采用 MIT 许可证，您可以自由使用、修改和分发。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个模板！

## 📞 支持

- [官方文档](https://docs.mai-mai.org/)
- [开发者指南](https://docs.mai-mai.org/develop/plugin_develop/)

---

**注意**: 本模板严格遵循MaiBot官方文档的最佳实践，确保您的插件能够与主系统完美集成。
