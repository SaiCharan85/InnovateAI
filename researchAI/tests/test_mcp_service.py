from model.api.mcp_service import MCPToolService


def test_build_topic_graph_creates_structure():
    service = MCPToolService()
    documents = [
        {
            "title": "Large Language Models in Healthcare",
            "content": "Large language models are transforming healthcare support systems.",
            "topic": "healthcare",
        },
        {
            "title": "AI for Research Discovery",
            "content": "AI tools help researchers discover related topics and papers.",
            "topic": "research",
        },
        {
            "title": "Topic Graphs for Knowledge Navigation",
            "content": "Topic graphs connect related concepts for better navigation.",
            "topic": "knowledge",
        },
    ]

    graph = service.build_topic_graph("ai", documents)

    assert graph["center_topic"] == "ai"
    assert any(node["id"] == "ai" for node in graph["nodes"])
    assert len(graph["edges"]) >= 1
