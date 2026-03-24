"""测试 CLI 顶层入口及 version/config 子命令。"""

from __future__ import annotations

import os
from pathlib import Path

from typer.testing import CliRunner

from my_cli import __version__
from my_cli.main import app


def test_app_help(runner: CliRunner) -> None:
    """--help 应成功输出帮助信息。"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "my-cli" in result.output.lower() or "AI" in result.output


def test_version_show(runner: CliRunner) -> None:
    """version show 应输出正确版本号。"""
    result = runner.invoke(app, ["version", "show"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_version_show_verbose(runner: CliRunner) -> None:
    """version show --verbose 应额外输出 Python 版本。"""
    result = runner.invoke(app, ["version", "show", "--verbose"])
    assert result.exit_code == 0
    assert "Python" in result.output


def test_config_show(runner: CliRunner) -> None:
    """config show 应以表格形式列出配置项。"""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "model" in result.output
    assert "openai_base_url" in result.output


def test_config_init(runner: CliRunner, tmp_path: Path) -> None:
    """config init 应在当前目录生成 .env 文件。"""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["config", "init"])
        assert result.exit_code == 0
        assert (tmp_path / ".env").exists()
    finally:
        os.chdir(original_dir)


def test_config_init_force(runner: CliRunner, tmp_path: Path) -> None:
    """config init --force 应覆盖已存在的 .env 文件。"""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        (tmp_path / ".env").write_text("existing", encoding="utf-8")
        result = runner.invoke(app, ["config", "init", "--force"])
        assert result.exit_code == 0
        content = (tmp_path / ".env").read_text(encoding="utf-8")
        assert "MY_CLI_OPENAI_API_KEY" in content
    finally:
        os.chdir(original_dir)


def test_config_init_no_force_fails(runner: CliRunner, tmp_path: Path) -> None:
    """config init 在 .env 已存在且未指定 --force 时应失败。"""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        (tmp_path / ".env").write_text("existing", encoding="utf-8")
        result = runner.invoke(app, ["config", "init"])
        assert result.exit_code != 0
    finally:
        os.chdir(original_dir)
