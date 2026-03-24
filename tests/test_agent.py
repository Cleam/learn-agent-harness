"""测试 AgentSession 核心逻辑（不发起真实 API 请求）。"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from my_cli.core.agent import AgentSession, Message


class TestMessage:
    def test_message_fields(self) -> None:
        msg = Message(role="user", content="你好")
        assert msg.role == "user"
        assert msg.content == "你好"


class TestAgentSession:
    def test_initial_state(self) -> None:
        session = AgentSession()
        assert session.messages == []
        assert "AI" in session.system_prompt or "助手" in session.system_prompt

    def test_add_user_message(self) -> None:
        session = AgentSession()
        session.add_user_message("测试输入")
        assert len(session.messages) == 1
        assert session.messages[0].role == "user"
        assert session.messages[0].content == "测试输入"

    def test_add_assistant_message(self) -> None:
        session = AgentSession()
        session.add_assistant_message("测试回复")
        assert len(session.messages) == 1
        assert session.messages[0].role == "assistant"

    def test_clear(self) -> None:
        session = AgentSession()
        session.add_user_message("消息1")
        session.add_assistant_message("回复1")
        session.clear()
        assert session.messages == []

    def test_build_payload_includes_system(self) -> None:
        session = AgentSession(system_prompt="你是测试助手。")
        session.add_user_message("你好")
        payload = session._build_payload()
        assert payload[0]["role"] == "system"
        assert payload[0]["content"] == "你是测试助手。"
        assert payload[1]["role"] == "user"

    def test_chat_raises_when_no_api_key(self) -> None:
        """当 API Key 为空时，chat() 应抛出 ValueError。"""
        session = AgentSession()
        with patch("my_cli.core.agent.settings") as mock_settings:
            mock_settings.openai_api_key.get_secret_value.return_value = ""
            with pytest.raises(ValueError, match="API Key"):
                session.chat("任意输入")

    def test_chat_returns_reply(self) -> None:
        """使用 mock 模拟 OpenAI 响应，验证 chat() 返回助手内容并追加历史。"""
        session = AgentSession()

        fake_choice = MagicMock()
        fake_choice.message.content = "Mock 回复"
        fake_response = MagicMock()
        fake_response.choices = [fake_choice]

        with (
            patch("my_cli.core.agent.settings") as mock_settings,
            patch("my_cli.core.agent.OpenAI") as mock_openai_cls,
        ):
            mock_settings.openai_api_key.get_secret_value.return_value = "sk-test"
            mock_settings.openai_base_url = "https://api.openai.com/v1"
            mock_settings.model = "gpt-4o"
            mock_settings.max_tokens = 100
            mock_settings.temperature = 0.7

            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = fake_response
            mock_openai_cls.return_value = mock_client

            reply = session.chat("你好")

        assert reply == "Mock 回复"
        assert len(session.messages) == 2
        assert session.messages[0].role == "user"
        assert session.messages[1].role == "assistant"
        assert session.messages[1].content == "Mock 回复"
