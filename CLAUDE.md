# CLAUDE.md

## 项目概述

这是一个 **Crush Skills 仓库**，用于存放和管理 AI 助手技能（Skills）。每个 Skill 是一个独立的功能模块，可以被 Crush AI 助手根据描述自动触发调用。

## 目录结构

```
skills/
├── <skill_name>/
│   ├── SKILL.md           # 技能定义文件（必需）
│   ├── scripts/           # 脚本目录（可选）
│   │   └── *.py           # Python 脚本
│   ├── references/        # 参考资料（可选）
│   └── assets/            # 静态资源（可选）
```

## SKILL.md 文件格式

每个技能必须包含 `SKILL.md` 文件，格式如下：

```markdown
---
name: <skill_name>
description: "<描述何时使用此技能 - 这是触发匹配的关键字段>"
---

# Skill Title

技能说明文档...

## Usage

如何使用此技能...
```

### YAML Frontmatter 字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 是 | 技能唯一标识符，用于匹配和调用 |
| `description` | 是 | 技能描述，**AI 根据此字段判断是否触发该技能** |

**重要**: `description` 字段应清晰描述技能的使用场景，便于 AI 自动匹配。

## 代码规范

### Python 脚本

- **仅使用标准库** - 确保跨平台兼容性，无需额外依赖
- **跨平台支持** - 必须支持 Windows、Linux、macOS (Darwin)
- **错误处理** - 使用 `try-except` 捕获所有可能的异常（`subprocess.TimeoutExpired`, `FileNotFoundError`, `OSError`, `PermissionError`）
- **超时设置** - 所有 `subprocess.run` 调用必须设置 `timeout` 参数
- **安全执行** - 使用 `shell=False`（默认值）避免 shell 注入风险

```python
# 示例：安全的 subprocess 调用
result = subprocess.run(
    ['command', 'arg'],
    capture_output=True,
    text=True,
    timeout=5,
    shell=False
)
if result.returncode == 0:
    # 处理成功结果
    pass
except (subprocess.TimeoutExpired, FileNotFoundError, OSError, PermissionError):
    pass
```

### 文档规范

- 使用中文编写文档和注释
- 代码注释仅解释"为什么"，不解释字面意思
- 在 SKILL.md 中提供清晰的使用示例

## 常用命令

### 验证技能脚本

```bash
# 运行技能脚本测试
python skills/<skill_name>/scripts/<script>.py
```

### 检查技能格式

```bash
# 验证 SKILL.md frontmatter 格式
head -n 10 skills/<skill_name>/SKILL.md
```

## 现有技能

### system_info

- **位置**: `skills/system_info/`
- **功能**: 获取操作系统和 Shell 信息
- **触发场景**: 用户询问系统详情、OS 版本、Shell 类型或系统配置
- **脚本**: `scripts/system_info.py` - 跨平台支持 Windows/Linux/macOS

## 开发新技能

1. 在 `skills/` 下创建新目录
2. 创建 `SKILL.md` 文件，包含 YAML frontmatter
3. 在 `description` 中清晰描述触发场景
4. 如需脚本，创建 `scripts/` 目录并添加 Python 脚本
5. 确保脚本仅使用标准库且跨平台兼容