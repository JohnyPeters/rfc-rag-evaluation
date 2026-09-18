"""D1 is bm25_search alone; C2 combines dense and BM25 retrieval with RRF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import bm25_search, dense_search
from .embed import _output_paths, load_chunks
from .fusion import rrf_fuse


def search(
    query: str,
    k: int = 5,
    *,
    data_dir: Path | None = None,
    model: Any | None = None,
) -> list[tuple[int, float]]:
    """Fuse the top 20 dense and BM25 row-index rankings using RRF."""
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")
    dense_results = dense_search.search(
        "section_aware", query, k=20, data_dir=data_dir, model=model
    )
    bm25_results = bm25_search.search(query, k=20, data_dir=data_dir)
    fused = rrf_fuse(
        [[index for index, _ in dense_results], [index for index, _ in bm25_results]],
        k=60,
    )
    return [(int(index), float(score)) for index, score in fused[:k]]


def main() -> None:
    """Run the hybrid-search CLI."""
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
