"""Hand-verified validity-tag behaviour in the generation context, using the
real q028 (GOAWAY) scenario: current, obsoleted-with-replacement, and an
unrelated same-named sibling that must never be tagged."""

from src.generation.prompt import format_context

RFC_METADATA = {
    "9113": {"status": "current", "obsoletes": [7540], "obsoleted_by": []},
    "7540": {"status": "obsoleted", "obsoletes": [], "obsoleted_by": [9113]},
    "9114": {"status": "current", "obsoletes": [], "obsoleted_by": []},
}
CHUNKS = [
    {"rfc": 9113, "sections": ["6.8"], "text": "current text"},
    {"rfc": 7540, "sections": ["6.8"], "text": "obsoleted text"},
    {"rfc": 9114, "sections": ["7.2.6"], "text": "unrelated homonym text"},
]


def test_current_rfc_gets_no_tag():
    out = format_context(CHUNKS, RFC_METADATA)
    assert "[RFC 9113 §6.8]" in out


def test_obsoleted_rfc_with_replacement_is_tagged():
    out = format_context(CHUNKS, RFC_METADATA)
    assert "[RFC 7540 §6.8 [OBSOLETED - see RFC 9113 instead]]" in out


def test_unrelated_sibling_is_never_tagged():
    # 9114 is current and shares no obsoletes/obsoleted_by relationship with
    # 9113 - it must not be tagged just because it happens to share content.
    out = format_context(CHUNKS, RFC_METADATA)
    assert "[RFC 9114 §7.2.6]" in out
    assert "[RFC 9114 §7.2.6 [OBSOLETED" not in out


def test_no_metadata_means_no_tags_at_all():
    out = format_context(CHUNKS, rfc_metadata=None)
    assert "OBSOLETED" not in out


def test_obsoleted_rfc_with_no_known_replacement_is_not_tagged():
    chunks = [{"rfc": 2616, "sections": ["1"], "text": "..."}]
    metadata = {"2616": {"status": "obsoleted", "obsoletes": [], "obsoleted_by": []}}
    out = format_context(chunks, metadata)
    assert "OBSOLETED" not in out
