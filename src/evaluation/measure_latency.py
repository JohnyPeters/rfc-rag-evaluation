"""Measure retrieval and local-generation latency for one strategy."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any
from time import perf_counter

from src.evaluation.run_eval import _load_queries, _project_root, retrieve_chunks
from src.generation import generate
from src.retrieval.embed import STRATEGIES


VALID_STRATEGIES = (*STRATEGIES, "hybrid_c2", "bm25_d1", "validity_c3")


def _percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    index = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[index]


def _summary(values: list[float]) -> dict[str, float]:
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "p95": _percentile(values, 0.95),
    }


def measure(
    strategy: str,
    n: int = 15,
    *,
    root: Path | None = None,
    model: str = "llama3.1:8b",
) -> dict[str, Any]:
    """Measure latency for the first *n* answerable evaluation queries."""
    if strategy not in VALID_STRATEGIES:
        raise ValueError(f"strategy must be one of {VALID_STRATEGIES}, got {strategy!r}")
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")

    project_root = root or _project_root()
    queries = [
        query
        for query in _load_queries(project_root / "eval" / "queries.yaml")
        if query["gold_sections"]
    ][:n]

    rows: list[dict[str, Any]] = []
    for number, query in enumerate(queries, start=1):
        query_text = str(query["query"])
        retrieval_started = perf_counter()
        chunks = retrieve_chunks(strategy, query_text, k=10, root=project_root)
        retrieval_seconds = perf_counter() - retrieval_started

        generation_started = perf_counter()
        answer_text = generate.generate(query_text, chunks, model=model)
        generation_seconds = perf_counter() - generation_started

        rows.append(
            {
                "id": query["id"],
                "category": query["category"],
                "retrieval_seconds": retrieval_seconds,
                "generation_seconds": generation_seconds,
                "end_to_end_seconds": retrieval_seconds + generation_seconds,
                "answer_token_count": len(answer_text),
            }
        )
        print(f"{number}/{len(queries)}", flush=True)

    return {
        "per_query": rows,
        "aggregate": {
            "retrieval_seconds": _summary(
                [row["retrieval_seconds"] for row in rows]
            ),
            "generation_seconds": _summary(
                [row["generation_seconds"] for row in rows]
            ),
            "end_to_end_seconds": _summary(
                [row["end_to_end_seconds"] for row in rows]
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", required=True, choices=VALID_STRATEGIES)
    parser.add_argument("--n", type=int, default=15)
    parser.add_argument("--model", default="llama3.1:8b")
    args = parser.parse_args()

    result = measure(args.strategy, args.n, model=args.model)
    output = _project_root() / "results" / args.strategy / "latency.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["aggregate"], indent=2))


if __name__ == "__main__":
    main()
