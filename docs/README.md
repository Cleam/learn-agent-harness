# 扩展开发文档

> 本文档面向希望在此 Starter 基础上深度定制或扩展功能的开发者。

---

## 架构概览

```
CLI 入口 (main.py)
    │
    ├── chat 子命令组 (commands/chat.py)
    │       └── AgentSession (core/agent.py)
    │               └── OpenAI SDK → LLM API
    │
    ├── config 子命令组 (commands/config.py)
    │       └── Settings (config.py)
    │
    └── version 子命令组 (commands/version.py)

工具层 (utils/console.py)  ← 被所有命令引用
```

---

## 核心类说明

### `AgentSession`（`src/my_cli/core/agent.py`）

多轮对话状态机，负责：

1. 维护 `messages: list[Message]` 历史
2. 构建符合 OpenAI Chat API 格式的 payload
3. 调用 `openai.OpenAI` 客户端发送请求
4. 将回复追加到历史并返回文本

**扩展点：**

- 重写 `_build_payload()` 以实现上下文截断（避免超出 token 限制）
- 在 `chat()` 前后添加钩子（日志、计时、重试）
- 添加 `stream_chat()` 方法支持流式输出

### `Settings`（`src/my_cli/config.py`）

基于 `pydantic-settings` 的配置类，支持：

- 从 `.env` 文件自动加载
- 环境变量覆盖（前缀 `MY_CLI_`）
- 字段类型验证与范围约束

**扩展点：**

- 添加新字段即可自动支持环境变量配置
- 可替换 `SettingsConfigDict` 指定不同的配置文件路径

---

## 流式输出实现示例

```python
from openai import OpenAI
from my_cli.config import settings
from my_cli.utils.console import console

def stream_chat(user_input: str) -> None:
    client = OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        base_url=settings.openai_base_url,
    )
    with client.chat.completions.stream(
        model=settings.model,
        messages=[{"role": "user", "content": user_input}],
    ) as stream:
        for text in stream.text_stream:
            console.print(text, end="")
    console.print()
```

---

## 工具调用（Function Calling）实现思路

1. 在 `AgentSession` 中定义工具列表：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取本地文件内容",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    }
]
```

2. 在 `_build_payload()` 中附加 `tools` 参数。
3. 在 `chat()` 中检查响应的 `finish_reason == "tool_calls"`，执行对应函数后追加结果继续对话。

---

## CI/CD 建议

在 GitHub Actions 中，推荐以下 workflow：

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: ruff format --check src/ tests/
      - run: ruff check src/ tests/
      - run: mypy src/
      - run: pytest
```

---

## 依赖升级指南

```bash
# 查看过时依赖
pip list --outdated

# 使用 uv 升级
uv pip install --upgrade typer rich openai pydantic pydantic-settings

# 升级 dev 工具
uv pip install --upgrade ruff mypy pytest pytest-cov pytest-asyncio
```

升级后务必重新运行完整检查：

```bash
ruff format --check src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest
```
