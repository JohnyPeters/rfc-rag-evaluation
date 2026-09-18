"""Extract numbered sections from cleaned RFC text."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SECTION_PATTERN = re.compile(r"^(\d+(\.\d+)*)\.?\s{1,}\S", re.MULTILINE)


def load_metadata(path: Path) -> dict[str, Any]:
    """Load the RFC metadata index."""
    with path.open(encoding="utf-8-sig") as metadata_file:
        return json.load(metadata_file)


def extract_sections(text: str) -> list[dict[str, Any]]:
    """Return numbered section records with offsets into *text*."""
    matches = list(SECTION_PATTERN.finditer(text))
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        sections.append(
            {
                "number": match.group(1),
                "char_start": start,
                "char_end": end,
                "text": text[start:end],
            }
        )
    return sections
