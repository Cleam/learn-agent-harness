"""pytest fixtures 公共配置。"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner


@pytest.fixture()
def runner() -> CliRunner:
    """提供 Typer CLI 测试客户端。"""
    return CliRunner()
