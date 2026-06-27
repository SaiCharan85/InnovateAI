from fastapi import APIRouter
from typing import Any, Dict, List

from api.mcp_service import MCPToolService

router = APIRouter()
service = MCPToolService()


@router.post("/mcp/search")
async def mcp_search(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = str(payload.get("query", ""))
    documents = payload.get("documents", [])
    results = service.search_documents(query, documents)
    return {"results": results}


@router.post("/mcp/topics")
async def mcp_related_topics(payload: Dict[str, Any]) -> Dict[str, Any]:
    topic = str(payload.get("topic", ""))
    documents = payload.get("documents", [])
    related = service.get_related_topics(topic, documents)
    return {"topics": related}


@router.post("/mcp/graph")
async def mcp_graph(payload: Dict[str, Any]) -> Dict[str, Any]:
    topic = str(payload.get("topic", ""))
    documents = payload.get("documents", [])
    graph = service.build_topic_graph(topic, documents)
    return graph
