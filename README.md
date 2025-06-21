# MaiBot 插件开发模板

> 这是一个官方的 MaiBot 插件开发模板仓库，遵循最新的官方文档标准，提供了完整的项目结构和最佳实践示例。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MaiBot](https://img.shields.io/badge/MaiBot-Plugin-green.svg)](https://docs.mai-mai.org/)

## ✨ 特性

- 🏗️ **完整项目结构** - 包含所有必要的文件和目录
- 📋 **标准Manifest** - 遵循官方规范的插件元数据
- 🔧 **配置Schema** - 自动配置生成和版本管理
- 🎯 **示例组件** - Action和Command的最佳实践示例
- 🧪 **测试框架** - 完整的单元测试覆盖
- 📖 **详细文档** - 清晰的代码注释和使用说明
- 🛠️ **开发工具** - Manifest验证和文档生成脚本

## 📦 项目结构

```
plugin-template/
├── plugin.py                    # 主插件文件
├── _manifest.json              # 插件元数据（强制要求）
├── README.md                   # 本文档
├── requirements.txt            # Python依赖
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

### 使用此模板创建新插件

1. **创建新仓库**
   - 点击右上角的 "Use this template" 按钮
   - 或者直接克隆此仓库：
   ```bash
   git clone https://github.com/your-username/plugin-template.git my-plugin
   cd my-plugin
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证环境**
   ```bash
   # 验证manifest文件
   python scripts/validate_manifest.py
   
   # 运行测试
   python -m pytest tests/
   ```

### 自定义您的插件

1. **修改插件信息**
   - 编辑 `_manifest.json` 更新插件元数据
   - 修改 `plugin.py` 中的插件类名和描述
   - 更新 `README.md` 为您的插件说明

2. **实现功能组件**
   - 在 `components/actions/` 添加您的Action组件
   - 在 `components/commands/` 添加您的Command组件
   - 根据需要修改配置Schema

3. **测试和验证**
   - 编写对应的测试用例
   - 确保所有测试通过
   - 验证manifest文件格式正确

## 📋 模板特点

### ✅ 符合官方标准
- **Manifest机制** - 完整的 `_manifest.json` 文件，包含所有必需和可选字段
- **配置系统** - Schema驱动的配置生成，支持版本管理和自动迁移
- **Action组件** - 两层决策机制、完整激活类型支持、聊天模式控制
- **Command组件** - 正则匹配、参数捕获、拦截控制、错误处理
- **开发规范** - 代码风格、错误处理、文档注释、单元测试

### 🎯 最佳实践示例

#### Action设计原则
- **智能激活** - 合理选择激活类型，避免过度激活
- **单一职责** - 每个Action只负责一个明确的功能  
- **清晰描述** - 提供准确的action_require帮助LLM决策
- **错误处理** - 妥善处理执行过程中的异常情况

#### Command设计原则
- **命令直观** - 使用清晰的命令格式（动作+对象+参数）
- **参数验证** - 早期验证参数有效性
- **帮助完整** - 提供详细的帮助信息和示例
- **拦截控制** - 合理设置拦截行为

#### 配置管理原则
- **Schema优先** - 所有配置项都在config_schema中声明
- **版本管理** - 及时更新config_version
- **默认安全** - 提供合理的默认值
- **文档自动** - 依靠Schema生成配置文档

## �️ 开发工具

### Manifest验证
验证您的插件元数据文件是否符合规范：
```bash
python scripts/validate_manifest.py
```

### 文档生成
自动生成插件文档：
```bash
python scripts/generate_docs.py
```

### 测试运行
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_actions.py

# 测试覆盖率报告
python -m pytest tests/ --cov=components
```

## � 学习资源

- [MaiBot 官方文档](https://docs.mai-mai.org/)
- [插件开发指南](https://docs.mai-mai.org/develop/plugin_develop/)
- [Action 组件开发](https://docs.mai-mai.org/develop/plugin_develop/action/)
- [Command 组件开发](https://docs.mai-mai.org/develop/plugin_develop/command/)
- [配置系统说明](https://docs.mai-mai.org/develop/plugin_develop/config/)

## 🤝 贡献指南

欢迎为此模板贡献代码！请遵循以下步骤：

1. Fork 此仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## � 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 💬 获得帮助

如果您在使用此模板时遇到问题：

- 查看 [Issues](https://github.com/MaiM-with-u/plugin-template/issues) 中是否有类似问题
- 阅读 [官方文档](https://docs.mai-mai.org/) 获取更多信息
- 在 [Discussions](https://github.com/MaiM-with-u/plugin-template/discussions) 中提问

## 🎉 开始开发

现在您已经准备好开始开发您的第一个 MaiBot 插件了！记住：

1. 📖 **阅读文档** - 熟悉官方开发指南
2. 🧪 **编写测试** - 确保代码质量
3. 📝 **更新文档** - 帮助其他开发者理解您的插件
4. 🔄 **持续改进** - 根据用户反馈不断优化

祝您开发愉快！🚀

---

**注意**: 此模板严格遵循 MaiBot 官方文档的最佳实践，确保您的插件能够与主系统完美集成。
