"""cleam_cli.utils.console — 终端输出辅助工具（基于 Rich）。"""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.theme import Theme

_THEME = Theme(
    {
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "user": "bold blue",
        "assistant": "bold magenta",
        "dim": "dim white",
    }
)

console = Console(theme=_THEME)
error_console = Console(stderr=True, theme=_THEME)


# ---------------------------------------------------------------------------
# 便捷打印函数
# ---------------------------------------------------------------------------


def print_info(message: str) -> None:
    """打印信息提示（青色）。"""
    console.print(f"[info]ℹ {escape(message)}[/info]")


def print_success(message: str) -> None:
    """打印成功提示（绿色）。"""
    console.print(f"[success]✓ {escape(message)}[/success]")


def print_warning(message: str) -> None:
    """打印警告提示（黄色）。"""
    console.print(f"[warning]⚠ {escape(message)}[/warning]")


def print_error(message: str) -> None:
    """打印错误提示（红色，输出到 stderr）。"""
    error_console.print(f"[error]✗ {escape(message)}[/error]")


def print_user_message(message: str) -> None:
    """渲染用户消息气泡。"""
    console.print(Panel(escape(message), title="[user]你[/user]", border_style="blue"))


def print_assistant_message(message: str) -> None:
    """渲染 AI 助手消息气泡。"""
    console.print(Panel(message, title="[assistant]助手[/assistant]", border_style="magenta"))


def print_code(code: str, language: str = "python") -> None:
    """高亮打印代码块。"""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)


def print_separator() -> None:
    """打印分隔线。"""
    console.rule(style="dim")
