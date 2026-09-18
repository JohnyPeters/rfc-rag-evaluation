"""Map generated chunks to the sections they substantially overlap."""

from __future__ import annotations


def map_chunks_to_sections(
    chunks: list[dict[str, object]],
    sections: list[dict[str, object]],
    minimum_overlap: int = 100,
) -> list[dict[str, object]]:
    """Add section numbers whose ranges overlap each chunk by *minimum_overlap*."""
    for chunk in chunks:
        chunk_start = int(chunk["char_start"])
        chunk_end = int(chunk["char_end"])
        mapped: list[str] = []
        for section in sections:
            section_start = int(section["char_start"])
            section_end = int(section["char_end"])
            section_length = section_end - section_start
            overlap = min(chunk_end, int(section["char_end"])) - max(
                chunk_start, int(section["char_start"])
            )
            if overlap >= min(minimum_overlap, section_length):
                mapped.append(str(section["number"]))
        chunk["sections"] = mapped
    return chunks
