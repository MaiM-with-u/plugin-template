# MaiBot插件模板

这是一个MaiBot插件开发模板，提供了创建插件所需的基础结构和示例代码。

## 快速开始

### 1. 使用此模板

1. 点击 "Use this template" 按钮创建新仓库
2. 克隆你的新仓库到本地
3. 修改插件名称和描述
4. 开始开发你的插件功能

### 2. 自定义插件

1. **修改manifest文件** (`_manifest.json`)
   - 更新插件名称、描述、作者等信息
   - 设置版本兼容性要求
   - 配置插件元数据

2. **实现插件逻辑** (`plugin.py`)
   - 继承BasePlugin基类
   - 实现加载/卸载方法
   - 注册组件

3. **添加组件**
   - Actions: 处理用户交互的动作
   - Processors: 数据处理器
   - Tools: 工具函数

### 3. Manifest文件说明

插件必须包含`_manifest.json`文件，这是插件的元数据描述：

```json
{
  "manifest_version": 3,
  "name": "你的插件名称",
  "version": "1.0.0",
  "description": "插件描述",
  "author": {
    "name": "作者名称",
    "url": "作者主页"
  },
  "host_application": {
    "name": "MaiBot",
    "min_version": "0.8.0",
    "max_version": ""
  }
}
```
### 4. 版本兼容性

- 当前模板支持MaiBot 0.8.0及以上版本
- 版本号支持语义化版本（semver）格式
- 支持snapshot版本（如0.8.0-snapshot.1）

### 5. 开发工具

使用提供的脚本工具：

```bash
# 验证manifest文件
python scripts/validate_manifest.py

```

## 插件组件类型

### Actions（动作组件）
处理用户交互，响应特定的触发条件。

### Tools（工具组件）
提供可调用的工具函数。

## 最佳实践

1. **错误处理**: 在所有async方法中妥善处理异常
2. **日志记录**: 使用self.logger记录重要信息
3. **资源管理**: 在on_unload中清理资源
4. **配置验证**: 验证插件配置的有效性
5. **文档完善**: 为所有组件提供清晰的文档

## 测试

运行测试确保插件正常工作：

```bash
python -m pytest tests/
```

## 许可证

[MIT License](./LICENSE) - 查看LICENSE文件了解详情。