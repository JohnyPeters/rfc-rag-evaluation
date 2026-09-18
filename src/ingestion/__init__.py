"""RFC ingestion utilities."""

from .artefacts import PaginationResult, read_rfc, strip_pagination_artifacts
from .sections import extract_sections, load_metadata

__all__ = [
    "PaginationResult",
    "extract_sections",
    "load_metadata",
    "read_rfc",
    "strip_pagination_artifacts",
]
