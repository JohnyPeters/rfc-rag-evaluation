"""BM25 lexical retrieval over the section-aware RFC chunk corpus."""

from __future__ import annotations

import argparse
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from .embed import _output_paths, load_chunks

TOKEN_RE = re.compile(r"\w+")


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _load_bm25_class() -> Any:
    try:
        from rank_bm25 import BM25Okapi
    except ImportError as exc:
        raise RuntimeError(
            "rank_bm25 is required for BM25 retrieval; install requirements first"
        ) from exc
    return BM25Okapi


def _data_key(data_dir: Path | None) -> str:
    return str((data_dir or Path(__file__).resolve().parents[2] / "data").resolve())


@lru_cache(maxsize=4)
def _build_cached(data_key: str) -> tuple[Any, int]:
    data_dir = Path(data_key)
    chunks = load_chunks("section_aware", data_dir)
    _, metadata_path = _output_paths("section_aware", data_dir)
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read section-aware metadata {metadata_path}: {exc}") from exc
    if (
        not isinstance(metadata, list)
        or len(metadata) != len(chunks)
        or any(not isinstance(item, dict) for item in metadata)
    ):
        raise ValueError(
            "section-aware metadata must be a list of objects aligned with chunks "
            f"({len(metadata) if isinstance(metadata, list) else 'invalid'} vs {len(chunks)})"
        )
    bm25 = _load_bm25_class()([_tokenize(chunk["text"]) for chunk in chunks])
    return bm25, len(chunks)


def load_index(data_dir: Path | None = None) -> Any:
    """Load a cached BM25 index aligned with section-aware chunk row indices."""
    return _build_cached(_data_key(data_dir))[0]


def build_index(data_dir: Path | None = None) -> Any:
    """Build or reuse the cached BM25 index for the section-aware corpus."""
    return load_index(data_dir)


def search(
    query: str,
    k: int = 5,
    *,
    data_dir: Path | None = None,
    index: Any | None = None,
) -> list[tuple[int, float]]:
    """Return ``(index, score)`` pairs sorted by descending BM25 score."""
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")
    if index is None:
        index, corpus_size = _build_cached(_data_key(data_dir))
    else:
        corpus_size = len(index.doc_freqs)
    if k > corpus_size:
        raise ValueError(f"k={k} exceeds corpus size {corpus_size}")
    scores = index.get_scores(_tokenize(query))
    return [
        (row_index, float(scores[row_index]))
        for row_index in sorted(range(corpus_size), key=lambda i: (-scores[i], i))[:k]
    ]


def main() -> None:
    """Run the BM25-search CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    results = search(args.query, args.k)
    chunks = load_chunks("section_aware")
    _, metadata_path = _output_paths("section_aware", None)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for index, score in results:
        item = metadata[index]
        preview = chunks[index]["text"][:150].replace("\n", " ")
        print(f"{score:.6f} RFC {item['rfc']} sections={item['sections']} {preview}")


if __name__ == "__main__":
    main()
