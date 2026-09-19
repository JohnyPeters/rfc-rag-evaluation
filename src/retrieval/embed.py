"""Create deterministic SentenceTransformer embeddings for RFC chunks."""

from __future__ import annotations

import argparse
import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

MODEL_NAME = "BAAI/bge-small-en-v1.5"
STRATEGIES = ("fixed_window", "section_aware")
RFC_COUNT = 16


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def chunk_paths(strategy: str, data_dir: Path | None = None) -> list[Path]:
    """Return source chunk files in RFC-number order."""
    if strategy not in STRATEGIES:
        raise ValueError(f"strategy must be one of {STRATEGIES}, got {strategy!r}")
    chunk_dir = (data_dir or _project_root() / "data") / "processed" / "chunks"
    paths = sorted(
        chunk_dir.glob(f"rfc*_{strategy}.json"),
        key=lambda path: int(path.name.split("_", 1)[0][3:]),
    )
    if len(paths) != RFC_COUNT:
        raise FileNotFoundError(
            f"expected {RFC_COUNT} {strategy!r} chunk JSON files in {chunk_dir}, "
            f"found {len(paths)}"
        )
    return paths


def load_chunks(strategy: str, data_dir: Path | None = None) -> list[dict[str, Any]]:
    """Load and concatenate chunks, preserving deterministic source order."""
    chunks: list[dict[str, Any]] = []
    for path in chunk_paths(strategy, data_dir):
        try:
            with path.open(encoding="utf-8") as source:
                items = json.load(source)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"could not read chunk file {path}: {exc}") from exc
        if not isinstance(items, list):
            raise ValueError(f"chunk file {path} must contain a JSON list")
        if any(not isinstance(item, dict) or not isinstance(item.get("text"), str) for item in items):
            raise ValueError(f"chunk file {path} contains an invalid chunk")
        chunks.extend(items)
    if not chunks:
        raise ValueError(f"empty {strategy!r} chunk corpus")
    return chunks


@lru_cache(maxsize=1)
def _load_model() -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "sentence-transformers is required to create embeddings; install requirements first"
        ) from exc
    try:
        return SentenceTransformer(MODEL_NAME)
    except Exception as exc:
        raise RuntimeError(f"could not load embedding model {MODEL_NAME!r}: {exc}") from exc


def _as_array(encoded: Any) -> np.ndarray:
    """Convert tensor, ndarray, or sequence encoder output to a float array."""
    if hasattr(encoded, "detach"):
        encoded = encoded.detach()
    if hasattr(encoded, "cpu"):
        encoded = encoded.cpu()
    if hasattr(encoded, "numpy"):
        encoded = encoded.numpy()
    return np.asarray(encoded, dtype=np.float32)


def normalize_rows(embeddings: Any) -> np.ndarray:
    """Return float32 row-normalized embeddings, rejecting zero rows."""
    array = _as_array(embeddings)
    if array.ndim != 2:
        raise ValueError(f"encoder output must be a 2-D matrix, got shape {array.shape}")
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("encoder output contains a zero-norm embedding")
    return (array / norms).astype(np.float32, copy=False)


def _output_paths(strategy: str, data_dir: Path | None) -> tuple[Path, Path]:
    output_dir = (data_dir or _project_root() / "data") / "processed" / "embeddings"
    return output_dir / f"{strategy}.npy", output_dir / f"{strategy}_meta.json"


def build_embeddings(
    strategy: str,
    *,
    model: Any | None = None,
    data_dir: Path | None = None,
) -> tuple[np.ndarray, list[dict[str, Any]], bool]:
    """Build or load fresh embeddings and aligned metadata.

    The final boolean is true when existing fresh outputs were reused.
    """
    paths = chunk_paths(strategy, data_dir)
    embedding_path, metadata_path = _output_paths(strategy, data_dir)
    newest_source = max(path.stat().st_mtime_ns for path in paths)
    if (
        embedding_path.exists()
        and metadata_path.exists()
        and embedding_path.stat().st_mtime_ns > newest_source
        and metadata_path.stat().st_mtime_ns > newest_source
    ):
        try:
            embeddings = np.load(embedding_path)
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if embeddings.ndim == 2 and len(metadata) == len(embeddings):
                return embeddings, metadata, True
        except (OSError, ValueError, json.JSONDecodeError):
            pass

    chunks = load_chunks(strategy, data_dir)
    texts = [str(chunk["text"]) for chunk in chunks]
    encoder = model or _load_model()
    try:
        encoded = encoder.encode(texts, convert_to_numpy=True)
    except TypeError:
        encoded = encoder.encode(texts)
    embeddings = normalize_rows(encoded)
    metadata = [
        {
            "rfc": chunk.get("rfc"),
            "char_start": chunk.get("char_start"),
            "char_end": chunk.get("char_end"),
            "sections": chunk.get("sections", []),
            "strategy": strategy,
        }
        for chunk in chunks
    ]
    if len(metadata) != len(embeddings):
        raise ValueError(
            f"encoder returned {len(embeddings)} rows for {len(metadata)} chunks"
        )
    embedding_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(embedding_path, embeddings.astype(np.float32, copy=False))
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return embeddings, metadata, False


def main() -> None:
    """Run the embedding CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", required=True, choices=STRATEGIES)
    args = parser.parse_args()
    started = time.perf_counter()
    embeddings, _, reused = build_embeddings(args.strategy)
    elapsed = time.perf_counter() - started
    status = "reused" if reused else "created"
    print(
        f"{status} {len(embeddings)} chunks, embedding dimension "
        f"{embeddings.shape[1]}, elapsed {elapsed:.2f}s"
    )


if __name__ == "__main__":
    main()
