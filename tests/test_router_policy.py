from src.agent_router import route_query


def test_recent_query_routes_to_web():
    decision = route_query("quais são as notícias mais recentes sobre LLMOps?")
    assert decision.primary_tool == "web_search"


def test_private_project_query_routes_to_rag():
    decision = route_query("o que meus documentos dizem sobre Qwen local?")
    assert decision.primary_tool == "local_rag"


def test_math_query_routes_to_python():
    decision = route_query("calcule 128 * 64")
    assert decision.primary_tool == "python"
