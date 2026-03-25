# cleam-cli — Python CLI 工具 Starter

> 一个类似 **Claude Code** 的 AI 驱动命令行工具项目模板，开箱即用，内置代码规范约束、完整测试体系与中文文档。

---

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [目录结构](#目录结构)
- [快速开始](#快速开始)
- [命令参考](#命令参考)
- [配置说明](#配置说明)
- [开发指南](#开发指南)
- [代码规范](#代码规范)
- [测试说明](#测试说明)
- [扩展指南](#扩展指南)
- [常见问题](#常见问题)

---

## 项目简介

本项目是一个 **Python CLI 工具 Starter**，参考 Claude Code 的交互模式，提供：

- 基于 [Typer](https://typer.tiangolo.com/) 的多子命令 CLI 框架
- 基于 [Rich](https://rich.readthedocs.io/) 的彩色终端输出与代码高亮
- 对接 OpenAI 兼容接口的多轮对话代理（`AgentSession`）
- 通过 [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) 管理配置
- 使用 [Ruff](https://docs.astral.sh/ruff/) 进行代码格式化与静态检查
- 使用 [Mypy](https://mypy.readthedocs.io/) 进行类型检查
- 使用 [Pytest](https://docs.pytest.org/) + 覆盖率报告进行测试

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 多轮对话 | `chat start` 进入交互式 REPL，支持历史管理与清空 |
| 单次查询 | `chat start --message "..."` 非交互模式，适合脚本调用 |
| 配置管理 | `config show` 查看配置，`config init` 生成 `.env` 模板 |
| 版本信息 | `version show [--verbose]` 查看版本及依赖 |
| 自定义 API | 支持任意 OpenAI 兼容接口（通过 `CLEAM_CLI_OPENAI_BASE_URL` 配置） |

---

## 目录结构

```
learn-agent-harness/
│
├── src/
│   └── cleam_cli/                  # 主包（src layout）
│       ├── __init__.py          # 包版本与名称定义
│       ├── main.py              # CLI 入口，注册子命令
│       ├── config.py            # 全局配置（pydantic-settings）
│       │
│       ├── commands/            # 子命令模块
│       │   ├── __init__.py
│       │   ├── chat.py          # chat 子命令（交互式对话）
│       │   ├── config.py        # config 子命令（配置管理）
│       │   └── version.py       # version 子命令（版本信息）
│       │
│       ├── core/                # 核心业务逻辑
│       │   ├── __init__.py
│       │   └── agent.py         # AgentSession — 多轮对话状态机
│       │
│       └── utils/               # 工具模块
│           ├── __init__.py
│           └── console.py       # Rich 终端输出辅助函数
│
├── tests/                       # 测试目录
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures（共享 runner）
│   ├── test_main.py             # CLI 命令集成测试
│   ├── test_agent.py            # AgentSession 单元测试
│   └── test_console.py          # console 工具函数测试
│
├── docs/                        # 文档目录
│   └── README.md                # 扩展开发文档
│
├── pyproject.toml               # 项目配置（依赖、ruff、mypy、pytest）
├── .gitignore                   # Git 忽略规则
└── README.md                    # 项目主文档（中文，即本文件）
```

### 各目录说明

| 目录/文件 | 说明 |
|-----------|------|
| `src/cleam_cli/` | 主包，采用 **src layout** 避免意外导入本地目录 |
| `src/cleam_cli/main.py` | Typer app 入口，汇总所有子命令，处理全局 `--verbose` |
| `src/cleam_cli/config.py` | 单例 `settings`，自动读取 `.env` / 环境变量，字段带校验 |
| `src/cleam_cli/commands/` | 每个子命令一个文件，通过 `app.add_typer()` 挂载到主 app |
| `src/cleam_cli/core/agent.py` | `AgentSession` 维护对话历史，调用 OpenAI 接口 |
| `src/cleam_cli/utils/console.py` | 封装 Rich Console，提供 `print_info/success/error` 等函数 |
| `tests/` | pytest 测试，覆盖 CLI 命令、业务逻辑、工具函数 |
| `pyproject.toml` | 单一配置文件，管理构建、依赖、lint、类型检查、测试 |

---

## 快速开始

### 1. 克隆项目并安装依赖

```bash
git clone <repo-url>
cd learn-agent-harness

# 使用 uv（推荐）
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# 或使用 pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. 配置 API Key

```bash
# 方式一：生成 .env 模板后填写
cleam-cli config init
# 编辑 .env，填入 CLEAM_CLI_OPENAI_API_KEY=sk-xxx

# 方式二：直接设置环境变量
export CLEAM_CLI_OPENAI_API_KEY=sk-xxx
```

### 3. 开始对话

```bash
# 交互式对话
cleam-cli chat start

# 单次查询
cleam-cli chat start --message "帮我写一个快速排序算法"

# 使用自定义系统提示词
cleam-cli chat start --system "你是一个 Linux 运维专家"
```

---

## 命令参考

### 全局选项

```
cleam-cli [--verbose/-v] <子命令>
```

| 选项 | 说明 |
|------|------|
| `--verbose, -v` | 输出详细日志 |
| `--help` | 显示帮助信息 |

---

### `chat` — 对话命令组

#### `cleam-cli chat start`

启动与 AI 助手的对话。

```bash
cleam-cli chat start [OPTIONS]
```

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--system, -s TEXT` | 编程助手提示词 | 自定义系统提示词 |
| `--message, -m TEXT` | _(空)_ | 单次消息，发送后立即退出 |

**交互模式特殊命令：**

| 命令 | 说明 |
|------|------|
| `exit` / `quit` / `q` | 退出会话 |
| `/clear` | 清空对话历史（保留系统提示词） |
| `/history` | 查看当前会话历史摘要 |

**示例：**

```bash
# 交互式
cleam-cli chat start

# 单次
cleam-cli chat start -m "Python 中如何读取 JSON 文件？"

# 自定义提示词
cleam-cli chat start -s "你是一个 SQL 优化专家，用中文回答"
```

---

### `config` — 配置命令组

#### `cleam-cli config show`

以表格形式列出所有配置项和当前值。

```bash
cleam-cli config show
```

#### `cleam-cli config init`

在当前目录生成 `.env` 配置模板文件。

```bash
cleam-cli config init [--force/-f]
```

| 选项 | 说明 |
|------|------|
| `--force, -f` | 强制覆盖已存在的 `.env` 文件 |

---

### `version` — 版本命令组

#### `cleam-cli version show`

打印版本号，附加 `--verbose` 可显示 Python 版本及依赖版本。

```bash
cleam-cli version show [--verbose/-v]
```

---

## 配置说明

所有配置项均支持通过**环境变量**（前缀 `CLEAM_CLI_`）或 **.env 文件**设置。

| 配置项（环境变量） | 默认值 | 说明 |
|-------------------|--------|------|
| `CLEAM_CLI_OPENAI_API_KEY` | _(空)_ | API 密钥（**必填**） |
| `CLEAM_CLI_OPENAI_BASE_URL` | `https://api.openai.com/v1` | 接口地址，可替换为兼容接口 |
| `CLEAM_CLI_MODEL` | `gpt-4o` | 使用的模型名称 |
| `CLEAM_CLI_MAX_TOKENS` | `4096` | 单次最大 token 数 |
| `CLEAM_CLI_TEMPERATURE` | `0.7` | 生成温度（0.0 ~ 2.0） |
| `CLEAM_CLI_HISTORY_DIR` | `~/.cleam_cli/history` | 历史记录存储目录 |
| `CLEAM_CLI_MAX_HISTORY` | `100` | 保存的最大历史条数 |
| `CLEAM_CLI_NO_COLOR` | `false` | 禁用彩色输出 |

### 使用国内/自定义接口

兼容 OpenAI API 的第三方服务（如 DeepSeek、Moonshot、Azure OpenAI 等）只需修改接口地址：

```bash
# .env
CLEAM_CLI_OPENAI_BASE_URL=https://api.deepseek.com/v1
CLEAM_CLI_OPENAI_API_KEY=sk-xxx
CLEAM_CLI_MODEL=deepseek-chat
```

---

## 开发指南

### 日常开发命令

```bash
# 代码格式化
ruff format src/ tests/

# 代码检查（lint）
ruff check src/ tests/

# 自动修复可修复的问题
ruff check --fix src/ tests/

# 类型检查
mypy src/

# 运行测试
pytest

# 运行测试并查看覆盖率
pytest --cov=cleam_cli --cov-report=html
open htmlcov/index.html
```

### 一键检查（CI 等效）

```bash
ruff format --check src/ tests/ && \
ruff check src/ tests/ && \
mypy src/ && \
pytest
```

---

## 代码规范

本项目使用 **Ruff** 统一管理格式化与 Lint，规则集包括：

| 规则集 | 说明 |
|--------|------|
| `E` / `W` | pycodestyle 错误与警告 |
| `F` | pyflakes（未使用变量/导入等） |
| `I` | isort（导入排序） |
| `B` | flake8-bugbear（常见 Bug 模式） |
| `C4` | flake8-comprehensions（推导式优化） |
| `UP` | pyupgrade（语法升级到 Python 3.11+） |
| `N` | pep8-naming（命名规范） |
| `ANN` | flake8-annotations（类型注解覆盖） |
| `S` | bandit 安全检查 |
| `RUF` | Ruff 专属规则 |

**格式化规则：**

- 缩进：4 空格
- 最大行长：100 字符
- 字符串引号：双引号
- 行尾：自动检测（LF）

**类型检查（Mypy）：**

- 开启 `strict` 模式（要求完整类型注解）
- Python 3.11 目标版本

---

## 测试说明

### 测试文件说明

| 文件 | 测试内容 |
|------|---------|
| `tests/test_main.py` | CLI 顶层命令、version/config 子命令集成测试 |
| `tests/test_agent.py` | `AgentSession` 单元测试（含 mock API 响应） |
| `tests/test_console.py` | console 工具函数输出测试 |

### 运行测试

```bash
# 基础运行
pytest

# 指定文件
pytest tests/test_agent.py

# 查看详细输出
pytest -v

# 生成 HTML 覆盖率报告
pytest --cov-report=html
```

### Mock 策略

`AgentSession.chat()` 会发起真实 API 调用，测试时使用 `unittest.mock.patch` 拦截：

```python
from unittest.mock import MagicMock, patch

with patch("cleam_cli.core.agent.OpenAI") as mock_cls:
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = fake_response
    mock_cls.return_value = mock_client
    reply = session.chat("你好")
```

---

## 扩展指南

### 添加新子命令

1. 在 `src/cleam_cli/commands/` 下新建文件，例如 `run.py`：

```python
"""cleam_cli.commands.run — 代码执行子命令。"""
import typer

app = typer.Typer(help="执行代码片段。")

@app.command("python")
def run_python(code: str = typer.Argument(..., help="Python 代码字符串。")) -> None:
    """执行 Python 代码并打印结果。"""
    exec(code)  # noqa: S102
```

2. 在 `src/cleam_cli/main.py` 中注册：

```python
from cleam_cli.commands import run   # 新增
app.add_typer(run.app, name="run")  # 新增
```

3. 添加对应测试文件 `tests/test_run.py`。

### 替换 LLM 后端

`AgentSession.chat()` 使用标准 OpenAI SDK，替换后端只需修改 `.env` 中的
`CLEAM_CLI_OPENAI_BASE_URL` 即可。如需更复杂的定制（流式输出、工具调用等），
在 `src/cleam_cli/core/agent.py` 中扩展 `AgentSession` 类。

### 持久化对话历史

当前版本仅在内存中维护历史。如需持久化，可在 `AgentSession` 中添加
`save()`/`load()` 方法，将 `messages` 序列化为 JSON 保存到 `settings.history_dir`。

---

## 常见问题

**Q：提示 `未检测到 API Key`？**

确保已设置环境变量 `CLEAM_CLI_OPENAI_API_KEY` 或在 `.env` 文件中填写。

**Q：如何使用代理？**

设置标准 HTTP 代理环境变量即可，OpenAI SDK 会自动识别：

```bash
export HTTPS_PROXY=http://127.0.0.1:7890
```

**Q：ruff / mypy 找不到命令？**

确认已安装 dev 依赖：

```bash
pip install -e ".[dev]"
```

**Q：如何修改项目名称？**

1. 修改 `pyproject.toml` 中的 `name` 和 `[project.scripts]` 入口
2. 重命名 `src/cleam_cli/` 目录为新名称
3. 全局替换 `cleam_cli` / `cleam-cli` 引用

---

## 许可证

[MIT](LICENSE)
