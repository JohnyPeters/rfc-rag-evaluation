"""Run dense retrieval evaluation over the committed query set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from src.retrieval import bm25_search, hybrid_search, validity_search
from src.retrieval.dense_search import search as dense_search
from src.retrieval.embed import STRATEGIES, load_chunks
from .metrics import aggregate, hit_rate_at_k, recall_at_k, reciprocal_rank


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_queries(path: Path) -> list[dict[str, Any]]:
    try:
        queries = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"could not read query file {path}: {exc}") from exc
    if not isinstance(queries, list) or not queries:
        raise ValueError(f"query file {path} must contain a non-empty YAML list")
    if any(not isinstance(query, dict) for query in queries):
        raise ValueError(f"query file {path} contains an invalid query")
    return queries


def evaluate(strategy: str, *, root: Path | None = None) -> dict[str, Any]:
    """Evaluate one retrieval strategy and return per-query and aggregate scores."""
    valid_strategies = (*STRATEGIES, "hybrid_c2", "bm25_d1", "validity_c3")
    if strategy not in valid_strategies:
        raise ValueError(f"strategy must be one of {valid_strategies}, got {strategy!r}")
    project_root = root or _project_root()
    queries = _load_queries(project_root / "eval" / "queries.yaml")
    chunk_strategy = (
        "section_aware"
        if strategy in {"hybrid_c2", "bm25_d1", "validity_c3"}
        else strategy
    )
    chunks = load_chunks(chunk_strategy, project_root / "data")

    per_query: list[dict[str, Any]] = []
    skipped_queries = 0
    for query in queries:
        gold_sections = query["gold_sections"]
        if not gold_sections:
            skipped_queries += 1
            continue
        if strategy in STRATEGIES:
            results = dense_search(
                strategy, str(query["query"]), k=10, data_dir=project_root / "data"
            )
        elif strategy == "hybrid_c2":
            results = hybrid_search.search(
                str(query["query"]), k=10, data_dir=project_root / "data"
            )
        elif strategy == "bm25_d1":
            results = bm25_search.search(
                str(query["query"]), k=10, data_dir=project_root / "data"
            )
        else:
            results = validity_search.search(
                str(query["query"]), k=10, data_dir=project_root / "data"
            )
        retrieved = [chunks[index] for index, _ in results]
        per_query.append(
            {
                "id": query["id"],
                "category": query["category"],
                "recall_at_5": recall_at_k(retrieved, gold_sections, 5),
                "recall_at_10": recall_at_k(retrieved, gold_sections, 10),
                "hit_rate_at_5": hit_rate_at_k(retrieved, gold_sections, 5),
                "mrr": reciprocal_rank(retrieved, gold_sections, 10),
            }
        )

    aggregate_rows = [
        {
            "category": row["category"],
            "recall_at_5": row["recall_at_5"],
            "recall_at_10": row["recall_at_10"],
            "hit_rate_at_5": row["hit_rate_at_5"],
            "mrr": row["mrr"],
        }
        for row in per_query
    ]
    return {
        "per_query": per_query,
        "aggregate": aggregate(aggregate_rows),
        "skipped_queries": skipped_queries,
    }


def _print_aggregate(scores: dict[str, Any]) -> None:
    aggregate_scores = scores["aggregate"]
    metric_names = list(aggregate_scores["overall"])
    header = ["group", "n", *metric_names]
    print("\t".join(header))
    print(
        "\t".join(
            [
                "overall",
                str(aggregate_scores["overall_n"]),
                *[f"{aggregate_scores['overall'][name]:.4f}" for name in metric_names],
            ]
        )
    )
    for category, values in aggregate_scores["by_category"].items():
        print(
            "\t".join(
                [
                    category,
                    str(values["n"]),
                    *[f"{values[name]:.4f}" for name in metric_names],
                ]
            )
        )
    print(f"Skipped queries with empty gold_sections: {scores['skipped_queries']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strategy",
        required=True,
        choices=(*STRATEGIES, "hybrid_c2", "bm25_d1", "validity_c3"),
    )
    args = parser.parse_args()

    scores = evaluate(args.strategy)
    output = _project_root() / "results" / args.strategy / "retrieval_metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    _print_aggregate(scores)


if __name__ == "__main__":
    main()
