from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from pottery_assistant.api import app


@pytest.fixture
def client():
    mock_agent = MagicMock()
    mock_agent.ainvoke = AsyncMock(return_value={
        "messages": [MagicMock(content="Use a técnica acordelada!")]
    })

    mock_checkpointer = AsyncMock()
    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_checkpointer)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)

    with (
        patch("pottery_assistant.api.AsyncRedisSaver") as mock_redis,
        patch("pottery_assistant.api.create_agent", return_value=mock_agent),
    ):
        mock_redis.from_conn_string.return_value = mock_ctx
        with TestClient(app) as c:
            yield c


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_response(client: TestClient) -> None:
    response = client.post("/chat", json={"message": "O que é argila?"})
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Use a técnica acordelada!"
    assert "session_id" in data


def test_chat_generates_session_id_when_omitted(client: TestClient) -> None:
    response = client.post("/chat", json={"message": "Olá"})
    assert response.status_code == 200
    assert len(response.json()["session_id"]) > 0


def test_chat_preserves_provided_session_id(client: TestClient) -> None:
    session_id = "aula-de-ceramica-123"
    response = client.post("/chat", json={"message": "Olá", "session_id": session_id})
    assert response.status_code == 200
    assert response.json()["session_id"] == session_id


def test_chat_returns_500_on_agent_error(client: TestClient) -> None:
    client.app.state.agent.ainvoke = AsyncMock(
        side_effect=RuntimeError("LLM indisponível")
    )
    response = client.post("/chat", json={"message": "Erro?"})
    assert response.status_code == 500
