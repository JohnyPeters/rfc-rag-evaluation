"""Hand-verified behaviour of the C3 validity filter, using a scenario
modelled directly on the real q028 (GOAWAY) case: A=9114 (unrelated
homonym, current), B=7540 (obsoleted, its replacement 9113 IS present),
C=9113 (the gold replacement), D=2616 (obsoleted, but its own replacement,
9110, is NOT present in this ranking).
"""

from src.retrieval.validity_filter import apply_validity_filter, mentioned_rfcs

RFC_METADATA = {
    "9114": {"status": "current", "obsoletes": [], "obsoleted_by": []},
    "7540": {"status": "obsoleted", "obsoletes": [], "obsoleted_by": [9113]},
    "9113": {"status": "current", "obsoletes": [7540], "obsoleted_by": []},
    "2616": {"status": "obsoleted", "obsoletes": [], "obsoleted_by": [9110]},
}
RANKED = [("A", 10.0, 9114), ("B", 9.0, 7540), ("C", 8.0, 9113), ("D", 7.0, 2616)]
QUERY = "What frame type value identifies a GOAWAY frame in HTTP/2?"


def test_obsoleted_with_present_replacement_is_demoted():
    result = apply_validity_filter(RANKED, QUERY, RFC_METADATA)
    ids = [item[0] for item in result]
    assert ids == ["A", "C", "D", "B"]


def test_obsoleted_without_a_present_replacement_is_left_alone():
    # D (2616) is obsoleted, but its replacement (9110) never appears in
    # RANKED - nothing to prefer over it, so it must not be penalised.
    result = apply_validity_filter(RANKED, QUERY, RFC_METADATA)
    ids = [item[0] for item in result]
    assert ids.index("D") < ids.index("B")  # D stays ahead of the one that IS penalised
    assert "D" in ids[:3]  # D keeps its original position among the non-penalised


def test_explicit_mention_exempts_that_rfc_from_penalty():
    query = "In RFC 7540, what frame type value identifies GOAWAY?"
    result = apply_validity_filter(RANKED, query, RFC_METADATA)
    ids = [item[0] for item in result]
    assert ids == ["A", "B", "C", "D"]  # unchanged - nothing penalised


def test_mentioned_rfcs_extracts_the_number():
    assert mentioned_rfcs("In RFC 7540, what frame type...") == {7540}
    assert mentioned_rfcs("What frame type identifies GOAWAY?") == set()
    assert mentioned_rfcs("Compare RFC 2616 and RFC 9110") == {2616, 9110}


def test_current_documents_are_never_penalised():
    # A and C are both "current" - must never move relative to each other
    # regardless of what else is in the ranking.
    result = apply_validity_filter(RANKED, QUERY, RFC_METADATA)
    ids = [item[0] for item in result]
    assert ids.index("A") < ids.index("C")  # original relative order preserved
