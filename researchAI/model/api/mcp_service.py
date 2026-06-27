from __future__ import annotations

from typing import Any, Dict, List
import re


class MCPToolService:
    """A minimal MCP-style tool service for topic search and graph building."""

    def __init__(self) -> None:
        self.tool_names = {
            "search_documents": self.search_documents,
            "get_related_topics": self.get_related_topics,
            "build_topic_graph": self.build_topic_graph,
            "expand_topic": self.expand_topic,
        }

    def search_documents(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search documents with keyword and research-aware boosting."""
        query_terms = re.findall(r"\w+", query.lower())
        if not query_terms:
            return documents

        research_terms = {
            "paper",
            "papers",
            "research",
            "survey",
            "benchmark",
            "method",
            "literature",
            "citation",
            "review",
        }
        is_research_query = any(term in research_terms for term in query_terms)

        results: List[Dict[str, Any]] = []
        for document in documents:
            text_parts = [
                str(document.get("title", "")),
                str(document.get("content", "")),
                str(document.get("topic", "")),
            ]
            metadata_keywords = document.get("metadata", {}).get("search_keywords", [])
            if isinstance(metadata_keywords, list):
                text_parts.extend([str(keyword) for keyword in metadata_keywords])

            text = " ".join(text_parts).lower()
            score = sum(1 for term in query_terms if term in text)

            research_boost = 0
            if document.get("topic") == "research" or "paper" in text or "research" in text:
                research_boost = 1
            if is_research_query and document.get("topic") == "research":
                research_boost += 1

            if score or research_boost:
                results.append({**document, "match_score": score + research_boost})

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

    def expand_topic(self, topic: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Expand a topic into related topics and matching documents."""
        related_topics = self.get_related_topics(topic, documents)
        matched_documents = self.search_documents(topic, documents)
        return {
            "topic": topic,
            "related_topics": related_topics,
            "documents": matched_documents[:5],
        }

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
