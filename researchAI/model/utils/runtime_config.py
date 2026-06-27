import os
from typing import Optional, Tuple


def resolve_runtime_config(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    repository: Optional[str] = None,
) -> Tuple[Optional[str], str, str]:
    """Resolve runtime settings from env vars and explicit config values."""
    resolved_project_id = project_id or os.getenv("GCP_PROJECT_ID")
    resolved_location = location or os.getenv("GCP_LOCATION") or "us-central1"
    resolved_repository = repository or os.getenv("GCP_ARTIFACT_REPOSITORY") or "rag-models"
    return resolved_project_id, resolved_location, resolved_repository
