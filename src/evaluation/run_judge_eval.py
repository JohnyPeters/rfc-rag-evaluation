"""Run correctness and faithfulness evaluation with an LLM judge."""

from __future__ import annotations

import argparse
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import yaml

from src.evaluation.run_eval import retrieve_chunks
from src.generation import generate, judge, prompt


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> list[dict[str, Any]]:
    try:
        values = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"could not read YAML file {path}: {exc}") from exc
    if not isinstance(values, list):
        raise ValueError(f"YAML file {path} must contain a list")
    return values


def _load_generation_results(path: Path) -> list[dict[str, Any]]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read generation results {path}: {exc}") from exc
    rows = result.get("per_query") if isinstance(result, dict) else None
    if not isinstance(rows, list):
        raise ValueError(f"generation results {path} has no per_query list")
    return rows


@contextmanager
def _judge_generation(user_message: str, model: str) -> Iterator[str]:
    original_builder = prompt.build_user_message
    original_system_prompt = prompt.SYSTEM_PROMPT
    prompt.build_user_message = lambda query, chunks, rfc_metadata=None: user_message
    prompt.SYSTEM_PROMPT = "You are a careful, literal-minded grader."
    try:
        yield generate.generate("", [], model=model)
    finally:
        prompt.build_user_message = original_builder
        prompt.SYSTEM_PROMPT = original_system_prompt


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    correctness_scores = [
        row["correctness"]["score"]
        for row in rows
        if row.get("correctness", {}).get("score") is not None
    ]
    faithfulness_scores = [
        row["faithfulness"]["faithfulness_score"]
        for row in rows
        if row.get("faithfulness", {}).get("faithfulness_score") is not None
    ]
    return {
        "n_total": len(rows),
        "n_answered": len(rows),
        "mean_correctness": _mean(correctness_scores),
        "n_correctness_unparseable": len(rows) - len(correctness_scores),
        "mean_faithfulness": _mean(faithfulness_scores),
        "n_faithfulness_unparseable": len(rows) - len(faithfulness_scores),
    }


def run(*, root: Path | None = None, model: str = "llama3.1:8b") -> dict[str, Any]:
    project_root = root or _project_root()
    result_path = project_root / "results" / "validity_c3" / "generation_metrics.json"
    generation_rows = _load_generation_results(result_path)
    queries = {query["id"]: query for query in _load_yaml(project_root / "eval" / "queries.yaml")}
    metadata = json.loads(
        (project_root / "data" / "rfc_metadata.json").read_text(encoding="utf-8")
    )
    rows: list[dict[str, Any]] = []

    answered_rows = [row for row in generation_rows if row.get("outcome") == "answered"]
    for number, generation_row in enumerate(answered_rows, start=1):
        query = queries[generation_row["id"]]
        query_text = str(query["query"])
        chunks = retrieve_chunks("validity_c3", query_text, k=10, root=project_root)
        context = prompt.format_context(chunks, metadata)
        answer = generation_row["answer_text"]

        correctness_message = judge.build_correctness_prompt(
            query_text, answer, query["reference_answer"]
        )
        with _judge_generation(correctness_message, model) as correctness_output:
            correctness = judge.parse_correctness(correctness_output)

        faithfulness_message = judge.build_faithfulness_prompt(answer, context)
        with _judge_generation(faithfulness_message, model) as faithfulness_output:
            faithfulness = judge.parse_faithfulness(faithfulness_output)

        rows.append(
            {
                "id": generation_row["id"],
                "category": generation_row["category"],
                "correctness": correctness,
                "faithfulness": faithfulness,
            }
        )
        print(f"{number}/{len(answered_rows)}", flush=True)

    categories = sorted({row["category"] for row in rows})
    return {
        "per_query": rows,
        "aggregate": _aggregate(rows),
        "aggregate_by_category": {
            category: _aggregate(
                [row for row in rows if row["category"] == category]
            )
            for category in categories
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="llama3.1:8b")
    args = parser.parse_args()
    result = run(model=args.model)
    output = _project_root() / "results" / "validity_c3" / "judge_metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["aggregate"], indent=2))


if __name__ == "__main__":
    main()
