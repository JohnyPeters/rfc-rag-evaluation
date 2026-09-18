"""Fixed-size chunking over the complete raw RFC document."""

from __future__ import annotations

from src.ingestion.artefacts import strip_pagination_artifacts

WINDOW_SIZE = 800
OVERLAP = 150
STRIDE = WINDOW_SIZE - OVERLAP


def chunk_fixed_window(raw_text: str, rfc: int | str) -> list[dict[str, object]]:
    """Return overlapping windows covering artefact-stripped *raw_text*."""
    cleaned_text = strip_pagination_artifacts(raw_text).text
    if not cleaned_text:
        return []

    chunks: list[dict[str, object]] = []
    start = 0
    while start < len(cleaned_text):
        end = min(start + WINDOW_SIZE, len(cleaned_text))
        chunks.append(
            {
                "rfc": rfc,
                "char_start": start,
                "char_end": end,
                "text": cleaned_text[start:end],
                "strategy": "fixed_window",
            }
        )
        if end == len(cleaned_text):
            break
        start += STRIDE

    _assert_coverage(chunks, len(cleaned_text))
    return chunks


def _assert_coverage(chunks: list[dict[str, object]], document_length: int) -> None:
    """Check ordering and complete, gap-free range coverage."""
    if document_length == 0:
        assert not chunks
        return
    assert chunks
    assert chunks[0]["char_start"] == 0
    assert chunks[-1]["char_end"] == document_length
    previous_end = 0
    for chunk in chunks:
        start = int(chunk["char_start"])
        end = int(chunk["char_end"])
        assert 0 <= start < end <= document_length
        assert start >= previous_end - OVERLAP
        assert start <= previous_end
        previous_end = max(previous_end, end)
