"""CLI 入口 — 注册所有子命令并提供顶层选项。"""

from __future__ import annotations

import typer

from my_cli import __app_name__
from my_cli.commands import chat, config, version

app = typer.Typer(
    name=__app_name__,
    help="一个类似 Claude Code 的 AI 驱动 CLI 工具。",
    add_completion=True,
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=False,
)

# 注册子命令组
app.add_typer(chat.app, name="chat")
app.add_typer(config.app, name="config")
app.add_typer(version.app, name="version")


@app.callback()
def callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="输出详细日志。"),
) -> None:
    """my-cli：与 AI 代理在终端中交互的命令行工具。"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


def main() -> None:
    """程序入口函数（供脚本调用）。"""
    app()


if __name__ == "__main__":
    main()
