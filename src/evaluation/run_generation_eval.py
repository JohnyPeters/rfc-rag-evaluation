"""Run generation evaluation for one retrieval strategy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from src.evaluation.run_eval import retrieve_chunks
from src.generation import generate
from src.generation import evaluate


STRATEGIES = ("fixed_window", "section_aware", "bm25_d1", "hybrid_c2", "validity_c3")


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


def run(strategy: str, *, root: Path | None = None, model: str = "llama3.1:8b") -> dict[str, Any]:
    """Run generation evaluation and return per-query and aggregate results."""
    if strategy not in STRATEGIES:
        raise ValueError(f"strategy must be one of {STRATEGIES}, got {strategy!r}")
    project_root = root or _project_root()
    queries = _load_queries(project_root / "eval" / "queries.yaml")
    per_query: list[dict[str, Any]] = []

    for number, query in enumerate(queries, start=1):
        print(f"{number}/{len(queries)}", flush=True)
        query_text = str(query["query"])
        retrieved = retrieve_chunks(strategy, query_text, k=10, root=project_root)
        answer = generate.generate(query_text, retrieved, model=model)
        outcome = evaluate.evaluate_generation(
            answer,
            query["expected_behaviour"],
            retrieved,
            query.get("gold_sections"),
        )
        per_query.append(
            {
                "id": query["id"],
                "category": query["category"],
                "expected_behaviour": query["expected_behaviour"],
                "outcome": outcome["outcome"],
                "is_refusal": outcome["is_refusal"],
                **{
                    key: outcome[key]
                    for key in ("citation_validity", "citation_relevance")
                    if key in outcome
                },
                "answer_text": answer,
            }
        )

    aggregate = evaluate.aggregate_generation(per_query)
    categories = sorted({row["category"] for row in per_query})
    aggregate_by_category = {
        category: evaluate.aggregate_generation(
            [row for row in per_query if row["category"] == category]
        )
        for category in categories
    }
    return {
        "per_query": per_query,
        "aggregate": aggregate,
        "aggregate_by_category": aggregate_by_category,
    }


def _print_aggregate(result: dict[str, Any]) -> None:
    aggregate = result["aggregate"]
    for name in (
        "refusal_rate",
        "unsupported_but_answered_rate",
        "false_refusal_rate",
        "mean_citation_validity",
        "mean_citation_relevance",
    ):
        print(f"{name}: {aggregate[name]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", required=True, choices=STRATEGIES)
    parser.add_argument("--model", default="llama3.1:8b")
    args = parser.parse_args()

    result = run(args.strategy, model=args.model)
    output = _project_root() / "results" / args.strategy / "generation_metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    _print_aggregate(result)


if __name__ == "__main__":
    main()
