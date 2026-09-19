"""Hand-verified judge output parsing, including a simulated q044 (CORS
citation-laundering) faithfulness check - the real motivating case for why
this metric exists at all."""

from src.generation.judge import parse_correctness, parse_faithfulness

# A judge correctly noticing none of q044's CORS claims are supported by
# the actually-supplied RFC 9112 §3.2.1 text (about origin-form syntax).
Q044_JUDGE_OUTPUT = """
CLAIM: A CORS preflight request uses the OPTIONS method
SUPPORTED: no
CLAIM: The Origin header is sent in a CORS preflight request
SUPPORTED: no
CLAIM: Access-Control-Request-Method is sent in a CORS preflight request
SUPPORTED: no
"""


def test_parse_correctness_extracts_each_verdict():
    assert parse_correctness("VERDICT: correct\nMatches the reference.") == {
        "verdict": "correct", "score": 1.0,
    }
    assert parse_correctness("VERDICT: partially_correct\n...")["score"] == 0.5
    assert parse_correctness("VERDICT: incorrect\n...")["score"] == 0.0


def test_parse_correctness_is_case_insensitive_and_tolerates_trailing_text():
    result = parse_correctness("VERDICT: Correct\nSome extra commentary the model added anyway.")
    assert result["verdict"] == "correct"


def test_parse_correctness_reports_none_on_unparseable_judge_output():
    # A judge that didn't follow the format is a judge-following failure to
    # surface, not a score to silently default to zero or one.
    result = parse_correctness("I think this answer looks fine overall.")
    assert result["verdict"] is None
    assert result["score"] is None


def test_parse_faithfulness_catches_the_q044_citation_laundering_case():
    result = parse_faithfulness(Q044_JUDGE_OUTPUT)
    assert result["n_claims"] == 3
    assert result["n_supported"] == 0
    assert result["faithfulness_score"] == 0.0


def test_parse_faithfulness_on_a_fully_supported_answer():
    output = "CLAIM: Retry-After can be an HTTP-date\nSUPPORTED: yes\nCLAIM: Retry-After can be delay-seconds\nSUPPORTED: yes"
    result = parse_faithfulness(output)
    assert result["faithfulness_score"] == 1.0


def test_parse_faithfulness_on_a_refusal_is_not_applicable_not_zero():
    result = parse_faithfulness("NO_CLAIMS")
    assert result["n_claims"] == 0
    assert result["faithfulness_score"] is None  # not 0.0 - nothing was checked, nothing failed


def test_parse_faithfulness_on_unparseable_output_is_also_not_applicable():
    result = parse_faithfulness("The answer seems fine to me.")
    assert result["faithfulness_score"] is None
