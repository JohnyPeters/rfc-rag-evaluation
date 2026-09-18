"""C3 retrieval: apply document-validity ordering to hybrid candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import hybrid_search
from .embed import _output_paths, load_chunks
from .validity_filter import apply_validity_filter


_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_META_PATH = _DATA_DIR / "rfc_metadata.json"
_RFC_METADATA: dict[str, Any] = json.loads(_META_PATH.read_text(encoding="utf-8"))


def _load_row_metadata(data_dir: Path | None = None) -> list[dict[str, Any]]:
    _, metadata_path = _output_paths("section_aware", data_dir)
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read section-aware metadata {metadata_path}: {exc}") from exc


def search(
    query: str,
    k: int = 5,
    *,
    data_dir: Path | None = None,
) -> list[tuple[int, float]]:
    """Return hybrid candidates reordered by C3 document validity."""
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")

    row_metadata = _load_row_metadata(data_dir)
    candidates = hybrid_search.search(query, k=20, data_dir=data_dir)
    ranked: list[tuple[int, float, int]] = []
    for item_id, score in candidates:
        try:
            rfc = int(row_metadata[item_id]["rfc"])
        except (IndexError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid RFC metadata for candidate row {item_id}") from exc
        ranked.append((item_id, score, rfc))

    reordered = apply_validity_filter(ranked, query, _RFC_METADATA)
    return [(int(item_id), float(score)) for item_id, score, _ in reordered[:k]]


def main() -> None:
    """Run the validity-aware search CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    results = search(args.query, args.k)
    chunks = load_chunks("section_aware")
    row_metadata = _load_row_metadata()
    for item_id, score in results:
        item = row_metadata[item_id]
        preview = chunks[item_id]["text"][:150].replace("\n", " ")
        print(f"{score:.6f} RFC {item['rfc']} sections={item['sections']} {preview}")


if __name__ == "__main__":
    main()
