"""cleam_cli.commands.config — 配置查看与修改子命令。"""

from __future__ import annotations

import typer
from rich.table import Table

from cleam_cli.config import settings
from cleam_cli.utils.console import console, print_success

app = typer.Typer(help="查看或修改工具配置。")


@app.command("show")
def show() -> None:
    """显示当前所有配置项及其值。"""
    table = Table(title="当前配置", show_lines=True)
    table.add_column("配置项", style="cyan", no_wrap=True)
    table.add_column("当前值", style="white")
    table.add_column("说明", style="dim")

    rows = [
        ("openai_base_url", settings.openai_base_url, "API 接口地址"),
        ("model", settings.model, "使用的模型"),
        ("max_tokens", str(settings.max_tokens), "最大 token 数"),
        ("temperature", str(settings.temperature), "生成温度"),
        ("history_dir", str(settings.history_dir), "历史记录目录"),
        ("max_history", str(settings.max_history), "最大历史条数"),
        ("no_color", str(settings.no_color), "禁用彩色输出"),
        (
            "openai_api_key",
            "***" if settings.openai_api_key.get_secret_value() else "(未设置)",
            "API 密钥（已脱敏）",
        ),
    ]
    for name, value, desc in rows:
        table.add_row(name, value, desc)

    console.print(table)


@app.command("init")
def init(
    force: bool = typer.Option(False, "--force", "-f", help="覆盖已存在的 .env 文件。"),
) -> None:
    """在当前目录生成 .env 配置文件模板。"""
    import os

    target = ".env"

    if os.path.exists(target) and not force:
        typer.echo(f"⚠ {target} 已存在，使用 --force 覆盖。")
        raise typer.Exit(code=1)

    content = """\
# cleam-cli 配置文件
# 将此文件重命名为 .env 并填写相应值

# OpenAI API 密钥（必填）
CLEAM_CLI_OPENAI_API_KEY=

# API 接口地址（可选，默认为官方接口）
CLEAM_CLI_OPENAI_BASE_URL=https://api.openai.com/v1

# 使用的模型（默认 gpt-4o）
CLEAM_CLI_MODEL=gpt-4o

# 单次最大 token 数
CLEAM_CLI_MAX_TOKENS=4096

# 生成温度（0.0 - 2.0）
CLEAM_CLI_TEMPERATURE=0.7
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    print_success(f".env 模板已生成：{target}")
