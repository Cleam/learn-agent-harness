"""测试 console 工具函数（确保不抛出异常）。"""

from __future__ import annotations

from collections.abc import Callable
from io import StringIO

from rich.console import Console

from my_cli.utils.console import (
    print_assistant_message,
    print_error,
    print_info,
    print_success,
    print_user_message,
    print_warning,
)


def _capture(func: Callable[..., None], *args: str) -> str:
    """捕获 rich console 输出为字符串。"""
    buf = StringIO()
    test_console = Console(file=buf, highlight=False, no_color=True)
    # 临时替换模块级 console
    import my_cli.utils.console as _mod

    original = _mod.console
    _mod.console = test_console  # type: ignore[assignment]
    try:
        func(*args)
    finally:
        _mod.console = original
    return buf.getvalue()


def test_print_info() -> None:
    out = _capture(print_info, "信息测试")
    assert "信息测试" in out


def test_print_success() -> None:
    out = _capture(print_success, "成功测试")
    assert "成功测试" in out


def test_print_warning() -> None:
    out = _capture(print_warning, "警告测试")
    assert "警告测试" in out


def test_print_user_message() -> None:
    out = _capture(print_user_message, "用户消息测试")
    assert "用户消息测试" in out


def test_print_assistant_message() -> None:
    out = _capture(print_assistant_message, "助手消息测试")
    assert "助手消息测试" in out


def test_print_error_does_not_raise() -> None:
    """print_error 输出到 stderr，不应抛出异常。"""
    print_error("错误测试")  # 只要不抛出即可
