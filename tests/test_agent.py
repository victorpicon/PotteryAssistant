from unittest.mock import patch

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
