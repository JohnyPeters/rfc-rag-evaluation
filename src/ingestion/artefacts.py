"""Read RFC text and remove artefacts introduced by paginated plain text."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PaginationResult:
    """The cleaned text and the pagination artefacts removed from it."""

    text: str
    boundaries: int
    lines_removed: int


def strip_pagination_artifacts(text: str) -> PaginationResult:
    """Remove page-break form feeds and the lines printed at page edges.

    RFC text files use a form feed as a page boundary.  The last non-blank
    line before, and the first non-blank line after, every boundary are
    pagination headers or footers and are removed.
    """
    boundaries = text.count("\f")
    if not boundaries:
        return PaginationResult(text=text, boundaries=0, lines_removed=0)

    parts = text.split("\f")
    removed = 0

    for index in range(len(parts) - 1):
        before_lines = parts[index].splitlines(keepends=True)
        for line_index in range(len(before_lines) - 1, -1, -1):
            if before_lines[line_index].strip():
                del before_lines[line_index]
                removed += 1
                break
        parts[index] = "".join(before_lines)

        after_lines = parts[index + 1].splitlines(keepends=True)
        for line_index, line in enumerate(after_lines):
            if line.strip():
                del after_lines[line_index]
                removed += 1
                break
        parts[index + 1] = "".join(after_lines)

    return PaginationResult(
        text="".join(parts),
        boundaries=boundaries,
        lines_removed=removed,
    )


def read_rfc(path: Path) -> PaginationResult:
    """Read an RFC as UTF-8 (including an optional UTF-8 BOM) and clean it."""
    text = path.read_text(encoding="utf-8-sig")
    return strip_pagination_artifacts(text)


def detect_form_feed_pagination(text: str) -> int:
    """Return the number of form-feed page boundaries in *text*."""
    return text.count("\f")


def remove_pagination_artifacts(text: str) -> str:
    """Return text with pagination artefacts removed."""
    return strip_pagination_artifacts(text).text
