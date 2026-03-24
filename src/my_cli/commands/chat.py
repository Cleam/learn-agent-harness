"""my_cli.commands.chat — 交互式对话子命令。"""

from __future__ import annotations

import sys

import typer
from rich.prompt import Prompt

from my_cli.core.agent import AgentSession
from my_cli.utils.console import (
    print_assistant_message,
    print_error,
    print_info,
    print_separator,
    print_user_message,
)

app = typer.Typer(help="与 AI 助手进行交互式对话。")

_EXIT_COMMANDS = {"exit", "quit", "q", "/exit", "/quit"}


@app.command("start")
def start(
    system_prompt: str = typer.Option(
        "你是一个专业的 AI 编程助手，帮助用户编写、调试和优化代码。",
        "--system",
        "-s",
        help="自定义系统提示词。",
    ),
    one_shot: str = typer.Option(
        "",
        "--message",
        "-m",
        help="发送单条消息后立即退出（非交互模式）。",
    ),
) -> None:
    """启动交互式对话会话。

    \b
    特殊命令（在对话中输入）：
      exit / quit / q  — 退出会话
      /clear           — 清空对话历史
      /history         — 查看当前会话历史
    """
    session = AgentSession(system_prompt=system_prompt)

    # 单次非交互模式
    if one_shot:
        _send_and_print(session, one_shot)
        return

    # 交互模式
    print_info("对话已开始，输入 'exit' 退出，输入 '/clear' 清空历史。")
    print_separator()

    while True:
        try:
            user_input = Prompt.ask("[bold blue]你[/bold blue]").strip()
        except (EOFError, KeyboardInterrupt):
            print_info("\n已退出对话。")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in _EXIT_COMMANDS:
            print_info("再见！")
            break

        if user_input == "/clear":
            session.clear()
            print_info("对话历史已清空。")
            print_separator()
            continue

        if user_input == "/history":
            _print_history(session)
            continue

        _send_and_print(session, user_input)


def _send_and_print(session: AgentSession, user_input: str) -> None:
    """发送消息并打印回复。"""
    print_user_message(user_input)
    try:
        reply = session.chat(user_input)
        print_assistant_message(reply)
    except ValueError as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        print_error(f"请求失败：{exc}")
        raise typer.Exit(code=1) from exc
    print_separator()


def _print_history(session: AgentSession) -> None:
    """打印当前会话历史。"""
    if not session.messages:
        print_info("暂无对话历史。")
        return
    for i, msg in enumerate(session.messages, 1):
        role_label = "你" if msg.role == "user" else "助手"
        suffix = "..." if len(msg.content) > 80 else ""
        typer.echo(f"  [{i}] {role_label}: {msg.content[:80]}{suffix}")
