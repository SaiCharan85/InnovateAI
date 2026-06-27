"""Tech Trends RAG System."""

from importlib import import_module

__version__ = "1.0.0"

__all__ = [
    "TechTrendsRAGPipeline",
    "DocumentProcessor",
    "DocumentChunker",
    "HybridEmbedder",
    "HybridRetriever",
    "ResponseGenerator",
    "config",
]


def __getattr__(name):
    mapping = {
        "TechTrendsRAGPipeline": (".pipeline", "TechTrendsRAGPipeline"),
        "DocumentProcessor": (".data_processing.document_processor", "DocumentProcessor"),
        "DocumentChunker": (".data_processing.chunking", "DocumentChunker"),
        "HybridEmbedder": (".data_processing.embedding", "HybridEmbedder"),
        "HybridRetriever": (".retrieval.retriever", "HybridRetriever"),
        "ResponseGenerator": (".generation.generator", "ResponseGenerator"),
        "config": (".config.settings", "config"),
    }
    if name in mapping:
        module_name, attr_name = mapping[name]
        module = import_module(module_name, __name__)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")