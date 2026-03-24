"""my_cli.config — 配置管理，读取环境变量与配置文件。"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用全局配置。

    优先级（从高到低）：
    1. 环境变量
    2. 项目根目录下的 ``.env`` 文件
    3. 字段默认值
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MY_CLI_",
        case_sensitive=False,
        extra="ignore",
    )

    # --- LLM ---
    openai_api_key: SecretStr = Field(
        default=SecretStr(""),
        description="OpenAI API 密钥（或兼容接口密钥）。",
    )
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI 兼容接口地址。",
    )
    model: str = Field(
        default="gpt-4o",
        description="使用的模型名称。",
    )
    max_tokens: int = Field(
        default=4096,
        ge=1,
        description="单次请求最大 token 数量。",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="生成温度（0-2）。",
    )

    # --- 历史记录 ---
    history_dir: Path = Field(
        default=Path.home() / ".my_cli" / "history",
        description="对话历史存储目录。",
    )
    max_history: int = Field(
        default=100,
        ge=1,
        description="保存的最大历史条数。",
    )

    # --- 输出 ---
    no_color: bool = Field(
        default=False,
        description="禁用彩色输出。",
    )


# 全局单例
settings = Settings()
