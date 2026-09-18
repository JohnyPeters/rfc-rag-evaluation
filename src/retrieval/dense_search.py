"""Exact dense retrieval over precomputed RFC embeddings."""

from __future__ import annotations

import argparse
import json
from typing import Any

import numpy as np

from .embed import (
    STRATEGIES,
    _load_model,
    _output_paths,
    load_chunks,
    normalize_rows,
)


def search(
    strategy: str,
    query: str,
    k: int = 5,
    *,
    data_dir: Any | None = None,
    model: Any | None = None,
) -> list[tuple[int, float]]:
    """Return ``(index, score)`` pairs sorted by descending dot product."""
    if strategy not in STRATEGIES:
        raise ValueError(f"strategy must be one of {STRATEGIES}, got {strategy!r}")
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")
    embedding_path, metadata_path = _output_paths(strategy, data_dir)
    try:
        embeddings = np.asarray(np.load(embedding_path), dtype=np.float32)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"embeddings for strategy {strategy!r} do not exist; run embed first"
        ) from exc
    if embeddings.ndim != 2 or not len(embeddings):
        raise ValueError("embedding matrix must be a non-empty 2-D array")
    if not isinstance(metadata, list) or len(metadata) != len(embeddings):
        raise ValueError("embedding and metadata lengths do not match")
    if k > len(embeddings):
        raise ValueError(f"k={k} exceeds corpus size {len(embeddings)}")
    encoder = model or _load_model()
    try:
        encoded = encoder.encode([query], convert_to_numpy=True)
    except TypeError:
        encoded = encoder.encode([query])
    query_vector = normalize_rows(encoded)
    if query_vector.shape[1] != embeddings.shape[1]:
        raise ValueError(
            f"query dimension {query_vector.shape[1]} does not match "
            f"embedding dimension {embeddings.shape[1]}"
        )
    scores = embeddings @ query_vector[0]
    indices = np.argsort(-scores, kind="mergesort")[:k]
    return [(int(index), float(scores[index])) for index in indices]


def main() -> None:
    """Run the dense-search CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", required=True, choices=STRATEGIES)
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    results = search(args.strategy, args.query, args.k)
    chunks = load_chunks(args.strategy)
    _, metadata_path = _output_paths(args.strategy, None)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for index, score in results:
        item = metadata[index]
        preview = chunks[index]["text"][:150].replace("\n", " ")
        print(f"{score:.6f} RFC {item['rfc']} sections={item['sections']} {preview}")


if __name__ == "__main__":
    main()
