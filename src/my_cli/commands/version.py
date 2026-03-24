"""my_cli.commands.version — 版本信息子命令。"""

from __future__ import annotations

import sys

import typer

from my_cli import __version__
from my_cli.utils.console import console

app = typer.Typer(help="显示版本信息。")


@app.command("show")
def show(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="同时打印 Python 版本及依赖信息。"),
) -> None:
    """打印 my-cli 版本号。"""
    console.print(f"my-cli [bold cyan]{__version__}[/bold cyan]")

    if verbose:
        py_ver = ".".join(str(v) for v in sys.version_info[:3])
        console.print(f"Python [dim]{py_ver}[/dim]")

        try:
            import importlib.metadata as meta

            for pkg in ("typer", "rich", "openai", "pydantic"):
                try:
                    ver = meta.version(pkg)
                    console.print(f"  {pkg} [dim]{ver}[/dim]")
                except meta.PackageNotFoundError:
                    console.print(f"  {pkg} [dim](未安装)[/dim]")
        except Exception as exc:
            console.print(f"[dim]无法获取依赖信息：{exc}[/dim]")
