"""Per-query generation outcome classification and aggregation.

is_refusal() alone only says whether the model refused - it says nothing
about whether refusing was CORRECT. That depends on the query's own
expected_behaviour, giving four distinct outcomes, not two:

                        refused             answered
expected: refuse    correct_refusal   unsupported_but_answered
expected: answer     false_refusal            answered

citation_validity/citation_relevance only mean anything for the "answered"
outcome - a refusal has no citations to check by construction, and forcing a
number there would misrepresent what was actually measured.
"""

from __future__ import annotations

from src.generation.citations import citation_relevance, citation_validity, is_refusal


def classify_outcome(answer: str, expected_behaviour: str) -> str:
    refused = is_refusal(answer)
    if expected_behaviour == "refuse":
        return "correct_refusal" if refused else "unsupported_but_answered"
    return "false_refusal" if refused else "answered"


def evaluate_generation(
    answer: str,
    expected_behaviour: str,
    context_chunks: list[dict],
    gold_sections: list[dict] | None = None,
) -> dict:
    """Full per-query result: the outcome cell, plus citation checks when -
    and only when - the model actually attempted an answer."""
    outcome = classify_outcome(answer, expected_behaviour)
    result: dict = {
        "outcome": outcome,
        "expected_behaviour": expected_behaviour,
        "is_refusal": is_refusal(answer),
    }
    if outcome == "answered":
        result["citation_validity"] = citation_validity(answer, context_chunks)
        if gold_sections:
            result["citation_relevance"] = citation_relevance(answer, gold_sections)
    return result


def aggregate_generation(per_query_results: list[dict]) -> dict:
    """Rates over a list of evaluate_generation() outputs.

    refusal_rate / unsupported_but_answered_rate are computed only over
    queries where expected_behaviour == "refuse" (they are complements of
    each other by construction - they must sum to 1.0 over that subset).
    false_refusal_rate is computed only over expected_behaviour == "answer"
    queries. citation validity/relevance are averaged only over the
    "answered" outcome, since that is the only outcome where they exist.
    """
    refuse_expected = [r for r in per_query_results if r["expected_behaviour"] == "refuse"]
    answer_expected = [r for r in per_query_results if r["expected_behaviour"] == "answer"]
    answered = [r for r in per_query_results if r["outcome"] == "answered"]

    def _rate(rows: list[dict], outcome: str) -> float | None:
        return len([r for r in rows if r["outcome"] == outcome]) / len(rows) if rows else None

    validity_rates = [r["citation_validity"]["validity_rate"] for r in answered]
    relevance_scores = [r["citation_relevance"] for r in answered if "citation_relevance" in r]

    return {
        "n_total": len(per_query_results),
        "n_refuse_expected": len(refuse_expected),
        "n_answer_expected": len(answer_expected),
        "refusal_rate": _rate(refuse_expected, "correct_refusal"),
        "unsupported_but_answered_rate": _rate(refuse_expected, "unsupported_but_answered"),
        "false_refusal_rate": _rate(answer_expected, "false_refusal"),
        "mean_citation_validity": sum(validity_rates) / len(validity_rates) if validity_rates else None,
        "mean_citation_relevance": sum(relevance_scores) / len(relevance_scores) if relevance_scores else None,
    }
