"""Chunk RFC sections while retaining section context."""

from __future__ import annotations

import re
from typing import Any

from .fixed_window import OVERLAP, STRIDE, WINDOW_SIZE

_HEADER = re.compile(r"^\s*(\d+(?:\.\d+)*)\.?\s+(.*?)\s*$")


def _parts(section: dict[str, Any]) -> tuple[str, str]:
    text = str(section["text"])
    lines = text.splitlines(keepends=True)
    header = lines[0].strip() if lines else str(section["number"])
    match = _HEADER.match(header)
    title = match.group(2).strip() if match else header
    body = "".join(lines[1:]).lstrip()
    return title, body


def _record(
    rfc: int | str,
    section: dict[str, Any],
    text: str,
    start: int,
    end: int,
) -> dict[str, object]:
    title, _ = _parts(section)
    header = f"§{section['number']} {title}\n\n"
    return {
        "rfc": rfc,
        "char_start": start,
        "char_end": end,
        "text": header + text,
        "strategy": "section_aware",
    }


def chunk_section_aware(
    sections: list[dict[str, Any]], rfc: int | str
) -> list[dict[str, object]]:
    """Chunk parsed sections, carrying short section bodies into the next leaf."""
    chunks: list[dict[str, object]] = []
    carry = ""
    carry_start: int | None = None
    for index, section in enumerate(sections):
        section_start = int(section["char_start"])
        section_end = int(section["char_end"])
        _, body = _parts(section)
        own_length = len(body)
        is_last = index == len(sections) - 1

        if own_length < 100 and not is_last:
            carry += body
            if carry_start is None:
                carry_start = section_start
            continue

        carried_text = carry
        combined = carried_text + body
        emitted_start = carry_start if carry_start is not None else section_start
        carry = ""
        carry_start = None
        if own_length <= 1000:
            chunks.append(_record(rfc, section, combined, emitted_start, section_end))
            continue

        # The window ranges remain in this section's original range.  The
        # section header is synthetic and repeated in every emitted chunk.
        split_chunks: list[dict[str, object]] = []
        offsets = list(range(0, len(body), STRIDE))
        for offset in offsets:
            body_end = min(offset + WINDOW_SIZE, len(body))
            start = emitted_start if offset == 0 else section_start + offset
            end = min(section_start + body_end, section_end)
            text = body[offset:body_end]
            if offset == 0:
                text = carried_text + text
            split_chunks.append(_record(rfc, section, text, start, end))

        remainder_length = len(body) - offsets[-1]
        if remainder_length < 100 and len(split_chunks) > 1:
            split_chunks.pop()
            split_chunks[-1]["char_end"] = section_end
        chunks.extend(split_chunks)

    assert all(
        any(
            int(chunk["char_start"]) < int(section["char_end"])
            and int(chunk["char_end"]) > int(section["char_start"])
            for chunk in chunks
        )
        for section in sections
    )
    return chunks
