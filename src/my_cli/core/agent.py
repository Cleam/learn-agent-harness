"""my_cli.core.agent — AI 代理核心逻辑。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openai import OpenAI

from my_cli.config import settings

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletionMessageParam


@dataclass
class Message:
    """单条对话消息。"""

    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class AgentSession:
    """维护一次完整的多轮对话状态。"""

    system_prompt: str = "你是一个专业的 AI 编程助手，帮助用户编写、调试和优化代码。"
    messages: list[Message] = field(default_factory=list)

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------

    def _build_payload(self) -> list[ChatCompletionMessageParam]:
        payload: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
        ]
        for msg in self.messages:
            payload.append({"role": msg.role, "content": msg.content})  # type: ignore[arg-type, misc]
        return payload

    # ------------------------------------------------------------------
    # 公开 API
    # ------------------------------------------------------------------

    def add_user_message(self, content: str) -> None:
        """将用户消息追加到历史。"""
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """将助手消息追加到历史。"""
        self.messages.append(Message(role="assistant", content=content))

    def clear(self) -> None:
        """清空对话历史（保留 system prompt）。"""
        self.messages.clear()

    def chat(self, user_input: str) -> str:
        """向 LLM 发送消息并返回回复文本。

        Args:
            user_input: 用户输入的文本。

        Returns:
            助手的回复文本。

        Raises:
            ValueError: 当 API Key 未配置时。
            openai.OpenAIError: 当 API 请求失败时。
        """
        api_key = settings.openai_api_key.get_secret_value()
        if not api_key:
            raise ValueError(
                "未检测到 API Key，请在 .env 文件或环境变量 MY_CLI_OPENAI_API_KEY 中配置。"
            )

        client = OpenAI(
            api_key=api_key,
            base_url=settings.openai_base_url,
        )

        self.add_user_message(user_input)
        response = client.chat.completions.create(
            model=settings.model,
            messages=self._build_payload(),
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
        )

        reply = response.choices[0].message.content or ""
        self.add_assistant_message(reply)
        return reply
