# Crush Skills

这是一个 **AI 助手技能（Skills）仓库**，用于存放和管理可被 AI 助手自动调用的功能模块。

## 项目结构

```
skills/
├── <skill_name>/
│   ├── SKILL.md           # 技能定义文件（必需）
│   ├── scripts/           # Python 脚本目录（可选）
│   │   └── *.py           # 跨平台 Python 脚本
│   ├── references/        # 参考资料（可选）
│   └── assets/            # 静态资源（可选）
```

## 技能列表

| 技能名称 | 描述 |
|----------|------|
| [system-info](skills/system-info/) | 获取操作系统和 Shell 信息 |

## 快速开始

### 调用技能

通过 `/` 命令调用技能，例如：

```bash
/system-info    # 获取系统信息
```

### 开发新技能

1. 在 `skills/` 目录下创建新目录
2. 创建 `SKILL.md` 文件，包含 YAML frontmatter：
   ```yaml
   ---
   name: <skill_name>
   description: "<技能描述 - AI 根据此字段判断是否触发>"
   ---
   ```
3. 如需脚本，创建 `scripts/` 目录并添加 Python 脚本
4. 确保脚本仅使用标准库且跨平台兼容

详细规范请参阅 [CLAUDE.md](CLAUDE.md)

## 代码规范

- **Python 脚本**：仅使用标准库，跨平台支持 Windows/Linux/macOS
- **错误处理**：使用 `try-except` 捕获异常，设置超时
- **安全执行**：使用 `shell=False` 避免 shell 注入
- **文档注释**：使用中文，仅解释"为什么"

## 测试技能

```bash
# 运行技能脚本测试
python skills/<skill_name>/scripts/<script>.py
```

## 许可证

MIT
