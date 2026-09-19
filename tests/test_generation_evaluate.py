"""Hand-verified generation outcome classification, using the real q028
(k=10, correct) and ad-hoc refusal-test answers from this project's own
generation runs."""

from src.generation.evaluate import aggregate_generation, classify_outcome, evaluate_generation
from src.generation.prompt import REFUSAL_TEXT

CONTEXT = [{"rfc": 9113, "sections": ["6.8"], "text": "..."}]
GOLD = [{"rfc": 9113, "section": "6.8"}]
GOOD_ANSWER = "0x07 (RFC 9113 §6.8)."


def test_the_four_outcome_cells():
    assert classify_outcome(REFUSAL_TEXT, "refuse") == "correct_refusal"
    assert classify_outcome(GOOD_ANSWER, "refuse") == "unsupported_but_answered"
    assert classify_outcome(REFUSAL_TEXT, "answer") == "false_refusal"
    assert classify_outcome(GOOD_ANSWER, "answer") == "answered"


def test_answered_outcome_carries_citation_checks():
    result = evaluate_generation(GOOD_ANSWER, "answer", CONTEXT, GOLD)
    assert result["outcome"] == "answered"
    assert result["citation_validity"]["validity_rate"] == 1.0
    assert result["citation_relevance"] == 1.0


def test_refusal_outcome_has_no_citation_fields():
    result = evaluate_generation(REFUSAL_TEXT, "refuse", CONTEXT, None)
    assert result["outcome"] == "correct_refusal"
    assert "citation_validity" not in result
    assert "citation_relevance" not in result


def test_aggregate_computes_independent_rates_per_subset():
    rows = [
        evaluate_generation(GOOD_ANSWER, "answer", CONTEXT, GOLD),        # answered
        evaluate_generation(REFUSAL_TEXT, "refuse", [], None),            # correct_refusal
        evaluate_generation(REFUSAL_TEXT, "answer", CONTEXT, GOLD),       # false_refusal
    ]
    agg = aggregate_generation(rows)
    assert agg["n_total"] == 3
    assert agg["n_refuse_expected"] == 1
    assert agg["n_answer_expected"] == 2
    assert agg["refusal_rate"] == 1.0               # 1/1 refuse-expected correctly refused
    assert agg["unsupported_but_answered_rate"] == 0.0
    assert agg["false_refusal_rate"] == 0.5         # 1/2 answer-expected wrongly refused
    assert agg["mean_citation_validity"] == 1.0     # only over the single "answered" row
    assert agg["mean_citation_relevance"] == 1.0


def test_aggregate_handles_an_empty_subset_without_dividing_by_zero():
    rows = [evaluate_generation(GOOD_ANSWER, "answer", CONTEXT, GOLD)]
    agg = aggregate_generation(rows)
    assert agg["n_refuse_expected"] == 0
    assert agg["refusal_rate"] is None
    assert agg["unsupported_but_answered_rate"] is None
