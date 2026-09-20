"""Hand-verified citation parsing and validity checking."""

from src.generation.citations import (
    citation_relevance,
    citation_validity,
    extract_citations,
    is_refusal,
)
from src.generation.prompt import REFUSAL_TEXT

CONTEXT = [
    {"rfc": 9110, "sections": ["10.2.3"], "text": "Servers send the Retry-After header field..."},
    {"rfc": 2616, "sections": ["14.37"], "text": "The Retry-After response-header field..."},
]
GOLD = [{"rfc": 9110, "section": "10.2.3"}]


def test_extract_citations_parses_the_fixed_format():
    answer = "Retry-After tells the client how long to wait (RFC 9110 §10.2.3)."
    assert extract_citations(answer) == [(9110, "10.2.3")]


def test_is_refusal_requires_the_exact_sentence():
    assert is_refusal(REFUSAL_TEXT) is True
    assert is_refusal("I do not know.") is False
    assert is_refusal(REFUSAL_TEXT + " ") is True  # tolerate surrounding whitespace


def test_citation_validity_accepts_a_supplied_citation():
    answer = "Retry-After tells the client how long to wait (RFC 9110 §10.2.3)."
    result = citation_validity(answer, CONTEXT)
    assert result["validity_rate"] == 1.0
    assert result["invalid"] == []


def test_citation_validity_rejects_a_fabricated_citation():
    # A real-looking RFC/section that was simply never in this call's context.
    answer = "The header is Retry-After (RFC 9110 §9.9.9)."
    result = citation_validity(answer, CONTEXT)
    assert result["validity_rate"] == 0.0
    assert result["invalid"] == [(9110, "9.9.9")]


def test_citation_validity_on_a_refusal_is_trivially_valid():
    result = citation_validity(REFUSAL_TEXT, CONTEXT)
    assert result["validity_rate"] == 1.0
    assert result["citations"] == []


def test_citation_validity_on_an_uncited_substantive_answer_is_zero():
    # The real q032 case: a correct-sounding, non-refusal answer that cites
    # nothing at all. This used to score 1.0 (a free pass) - fixed to 0.0,
    # since an uncited factual claim is a real rule violation, not a
    # vacuous case like a refusal's empty citation list.
    answer = (
        "The GOAWAY frame allows an endpoint to stop accepting new requests "
        "or pushes while still finishing processing of previously received "
        "requests and pushes."
    )
    result = citation_validity(answer, CONTEXT)
    assert result["validity_rate"] == 0.0
    assert result["citations"] == []


def test_citation_relevance_scores_against_gold_not_context():
    on_topic = "Retry-After (RFC 9110 §10.2.3)."
    off_topic = "See RFC 2616 §14.37 instead."
    assert citation_relevance(on_topic, GOLD) == 1.0
    assert citation_relevance(off_topic, GOLD) == 0.0


def test_citation_relevance_on_a_refusal_is_trivially_relevant():
    assert citation_relevance(REFUSAL_TEXT, GOLD) == 1.0


def test_citation_relevance_on_an_uncited_substantive_answer_is_zero():
    answer = "The GOAWAY frame allows an endpoint to stop accepting new requests."
    assert citation_relevance(answer, GOLD) == 0.0
