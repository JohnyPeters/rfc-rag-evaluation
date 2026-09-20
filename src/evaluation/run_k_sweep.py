"""Evaluate retrieval metrics across several values of k."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.evaluation.run_eval import _load_queries, _project_root, retrieve_chunks
from src.evaluation.metrics import (
    aggregate,
    hit_rate_at_k,
    recall_at_k,
    reciprocal_rank,
)
from src.retrieval.embed import STRATEGIES


K_VALUES = [3, 5, 10, 15, 20]
VALID_STRATEGIES = (*STRATEGIES, "hybrid_c2", "bm25_d1", "validity_c3")


def run(strategy: str, *, root: Path | None = None) -> dict[str, Any]:
    """Run the k sweep for one retrieval strategy."""
    if strategy not in VALID_STRATEGIES:
        raise ValueError(f"strategy must be one of {VALID_STRATEGIES}, got {strategy!r}")

    project_root = root or _project_root()
    queries = _load_queries(project_root / "eval" / "queries.yaml")
    per_query: list[dict[str, Any]] = []
    skipped_queries = 0

    for query in queries:
        gold_sections = query["gold_sections"]
        if not gold_sections:
            skipped_queries += 1
            continue

        retrieved = retrieve_chunks(
            strategy,
            str(query["query"]),
            k=max(K_VALUES),
            root=project_root,
        )
        row: dict[str, Any] = {
            "id": query["id"],
            "category": query["category"],
        }
        for k in K_VALUES:
            row[f"recall_at_{k}"] = recall_at_k(retrieved, gold_sections, k)
            row[f"hit_rate_at_{k}"] = hit_rate_at_k(retrieved, gold_sections, k)
        row["mrr"] = reciprocal_rank(retrieved, gold_sections, max(K_VALUES))
        per_query.append(row)

    aggregate_rows = [
        {
            key: value
            for key, value in row.items()
            if key != "id"
        }
        for row in per_query
    ]
    return {
        "per_query": per_query,
        "aggregate": aggregate(aggregate_rows),
        "skipped_queries": skipped_queries,
    }


def _print_table(result: dict[str, Any]) -> None:
    overall = result["aggregate"]["overall"]
    print("k\trecall\thit_rate")
    for k in K_VALUES:
        print(
            f"{k}\t{overall[f'recall_at_{k}']:.4f}"
            f"\t{overall[f'hit_rate_at_{k}']:.4f}"
        )
    print(f"Skipped queries with empty gold_sections: {result['skipped_queries']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", required=True, choices=VALID_STRATEGIES)
    args = parser.parse_args()

    result = run(args.strategy)
    output = _project_root() / "results" / args.strategy / "k_sweep.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    _print_table(result)


if __name__ == "__main__":
    main()
