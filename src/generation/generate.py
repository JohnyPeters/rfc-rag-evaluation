"""Generate cited answers from retrieved RFC context with Ollama."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from src.generation import citations, prompt
from src.retrieval import bm25_search, hybrid_search, validity_search
from src.retrieval.dense_search import search as dense_search
from src.retrieval.embed import STRATEGIES, load_chunks


_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_RFC_METADATA: dict[str, Any] = json.loads(
    (_DATA_DIR / "rfc_metadata.json").read_text(encoding="utf-8")
)


def _ollama_chat(model: str, user_message: str) -> str:
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError(
            "The Ollama Python client is not installed; install requirements first."
        ) from exc

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt.SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            options={"temperature": 0},
        )
    except Exception as exc:
        raise RuntimeError(
            f"Could not call Ollama model {model!r}. Start Ollama and pull the model "
            f"with 'ollama pull {model}'. Original error: {exc}"
        ) from exc

    try:
        return str(response["message"]["content"])
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Ollama returned a response without message content") from exc


def generate(
    query: str,
    chunks: list[dict],
    model: str = "llama3.1:8b",
) -> str:
    """Generate an answer from the supplied ranked chunks."""
    return _ollama_chat(
        model,
        prompt.build_user_message(query, chunks, _RFC_METADATA),
    )


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _retrieve(
    strategy: str,
    query: str,
    k: int,
    data_dir: Path,
) -> list[dict[str, Any]]:
    if strategy in STRATEGIES:
        results = dense_search(strategy, query, k=k, data_dir=data_dir)
    elif strategy == "hybrid_c2":
        results = hybrid_search.search(query, k=k, data_dir=data_dir)
    elif strategy == "bm25_d1":
        results = bm25_search.search(query, k=k, data_dir=data_dir)
    elif strategy == "validity_c3":
        results = validity_search.search(query, k=k, data_dir=data_dir)
    else:
        raise ValueError(f"unsupported strategy: {strategy}")

    corpus_strategy = "section_aware" if strategy in {
        "hybrid_c2",
        "bm25_d1",
        "validity_c3",
    } else strategy
    chunks = load_chunks(corpus_strategy, data_dir)
    return [chunks[index] for index, _ in results]


def _gold_sections(query: str, root: Path) -> list[dict] | None:
    queries_path = root / "eval" / "queries.yaml"
    try:
        entries = yaml.safe_load(queries_path.read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError):
        return None
    for entry in entries or []:
        if isinstance(entry, dict) and entry.get("query") == query:
            return entry.get("gold_sections", [])
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strategy",
        required=True,
        choices=(*STRATEGIES, "hybrid_c2", "bm25_d1", "validity_c3"),
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--model", default="llama3.1:8b")
    args = parser.parse_args()
    if args.k <= 0:
        parser.error("--k must be a positive integer")

    root = _project_root()
    chunks = _retrieve(args.strategy, args.query, args.k, root / "data")
    answer = generate(args.query, chunks, args.model)
    gold = _gold_sections(args.query, root)
    validity = citations.citation_validity(answer, chunks)

    print(f"Answer:\n{answer}")
    print(f"Refusal: {citations.is_refusal(answer)}")
    print(f"Citation validity: {json.dumps(validity)}")
    if gold is None:
        print("Citation relevance: unavailable (query not found in eval/queries.yaml)")
    else:
        print(
            "Citation relevance: "
            f"{citations.citation_relevance(answer, gold):.4f}"
        )


if __name__ == "__main__":
    main()
