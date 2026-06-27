from __future__ import annotations

from typing import Any, Dict, List, Optional
import re


class MCPToolService:
    """A minimal MCP-style tool service for topic search and graph building."""

    def __init__(self) -> None:
        self.tool_names = {
            "search_documents": self.search_documents,
            "get_related_topics": self.get_related_topics,
            "build_topic_graph": self.build_topic_graph,
        }

    def search_documents(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search documents by a simple keyword match."""
        query_terms = re.findall(r"\w+", query.lower())
        if not query_terms:
            return documents

        results: List[Dict[str, Any]] = []
        for document in documents:
            text = " ".join(
                [
                    str(document.get("title", "")),
                    str(document.get("content", "")),
                    str(document.get("topic", "")),
                ]
            ).lower()
            score = sum(1 for term in query_terms if term in text)
            if score:
                results.append({**document, "match_score": score})

        results.sort(key=lambda item: item.get("match_score", 0), reverse=True)
        return results

    def get_related_topics(self, topic: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return related topic labels from the document set."""
        topic_lower = topic.lower()
        related: List[Dict[str, Any]] = []
        seen = set()

        for document in documents:
            doc_topic = str(document.get("topic", "")).strip().lower()
            if not doc_topic or doc_topic == topic_lower:
                continue
            if doc_topic not in seen:
                seen.add(doc_topic)
                related.append({"topic": doc_topic, "title": document.get("title", "")})

        return related

    def build_topic_graph(
        self,
        center_topic: str,
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Create a lightweight topic graph structure for UI rendering."""
        related_topics = self.get_related_topics(center_topic, documents)
        nodes = [{"id": center_topic, "label": center_topic, "group": "center"}]
        edges: List[Dict[str, Any]] = []

        for topic in related_topics:
            node_id = topic["topic"]
            nodes.append({"id": node_id, "label": node_id, "group": "related"})
            edges.append({"source": center_topic, "target": node_id, "weight": 1})

        return {
            "center_topic": center_topic,
            "nodes": nodes,
            "edges": edges,
        }
