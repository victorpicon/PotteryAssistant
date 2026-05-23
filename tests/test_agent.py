from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver


def test_create_agent_returns_compiled_graph():
    with patch("pottery_assistant.agent.ChatGoogleGenerativeAI"):
        from pottery_assistant.agent import create_agent
        agent = create_agent(MemorySaver())
    assert agent is not None


def test_agent_graph_has_assistant_node():
    with patch("pottery_assistant.agent.ChatGoogleGenerativeAI"):
        from pottery_assistant.agent import create_agent
        agent = create_agent(MemorySaver())
    assert "assistant" in agent.get_graph().nodes


def test_agent_invokes_llm_and_returns_response():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Use a técnica acordelada!")

    with patch("pottery_assistant.agent.ChatGoogleGenerativeAI", return_value=mock_llm):
        from pottery_assistant.agent import create_agent
        agent = create_agent(MemorySaver())

    result = agent.invoke(
        {"messages": [HumanMessage(content="Como modelar um vaso?")]},
        config={"configurable": {"thread_id": "test-thread"}},
    )

    assert result["messages"][-1].content == "Use a técnica acordelada!"
    mock_llm.invoke.assert_called_once()


def test_agent_includes_system_prompt_in_llm_call():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Resposta")

    with patch("pottery_assistant.agent.ChatGoogleGenerativeAI", return_value=mock_llm):
        from pottery_assistant.agent import SYSTEM_PROMPT, create_agent
        agent = create_agent(MemorySaver())

    agent.invoke(
        {"messages": [HumanMessage(content="Olá")]},
        config={"configurable": {"thread_id": "test-system-prompt"}},
    )

    call_args = mock_llm.invoke.call_args[0][0]
    assert call_args[0].content == SYSTEM_PROMPT
