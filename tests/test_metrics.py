"""Hand-computed verification of retrieval metrics.

Per README.md's Testing section, this is the single most important test in
the repository: a bug in Recall@k or MRR does not crash, it produces a
plausible-looking wrong number, and every conclusion drawn from the results
tables inherits it silently.

The single-gold case below is the actual retrieved ranking for the corrected
"Retry-After" query against C0 (see the project's chat history / README) -
not a synthetic fixture - so this test also stands as a permanent record of
that first real, verified retrieval result.
"""

from src.evaluation.metrics import (
    aggregate,
    hit_rate_at_k,
    reciprocal_rank,
    recall_at_k,
    sections_found,
)

# Real C0 (fixed_window) top-5 for: "What header field tells a client how
# long to wait before retrying, and what two formats can its value take?"
# Gold: RFC 9110 section 10.2.3.
RETRY_AFTER_C0_TOP5 = [
    {"rfc": 2616, "sections": ["14.37", "14.38"]},
    {"rfc": 9110, "sections": ["10.2.3"]},          # gold, rank 2
    {"rfc": 7231, "sections": ["7.1.3", "7.1.4"]},
    {"rfc": 9110, "sections": ["10.2.2", "10.2.3"]},  # also touches gold, rank 4
    {"rfc": 9110, "sections": ["10.1.1"]},
]
RETRY_AFTER_GOLD = [{"rfc": 9110, "section": "10.2.3"}]


def test_recall_at_1_misses_before_gold_appears():
    assert recall_at_k(RETRY_AFTER_C0_TOP5, RETRY_AFTER_GOLD, 1) == 0.0


def test_recall_at_3_and_5_find_the_gold():
    assert recall_at_k(RETRY_AFTER_C0_TOP5, RETRY_AFTER_GOLD, 3) == 1.0
    assert recall_at_k(RETRY_AFTER_C0_TOP5, RETRY_AFTER_GOLD, 5) == 1.0


def test_mrr_is_reciprocal_of_first_hit_rank():
    # Gold first appears at rank 2 -> 1/2, regardless of it appearing again at rank 4.
    assert reciprocal_rank(RETRY_AFTER_C0_TOP5, RETRY_AFTER_GOLD, 10) == 0.5


def test_hit_rate_at_5_is_one():
    assert hit_rate_at_k(RETRY_AFTER_C0_TOP5, RETRY_AFTER_GOLD, 5) == 1.0


def test_reciprocal_rank_is_zero_when_gold_never_appears():
    no_hit = [{"rfc": 2616, "sections": ["1"]}, {"rfc": 2616, "sections": ["2"]}]
    assert reciprocal_rank(no_hit, RETRY_AFTER_GOLD, 10) == 0.0
    assert recall_at_k(no_hit, RETRY_AFTER_GOLD, 10) == 0.0


def test_multi_gold_recall_is_a_fraction_not_binary():
    # Two gold sections, only one appears in the retrieved chunks.
    retrieved = [
        {"rfc": 9111, "sections": ["5.2.1.1"]},
        {"rfc": 9110, "sections": ["15.5.1"]},
    ]
    gold = [
        {"rfc": 9111, "section": "5.2.1.1"},
        {"rfc": 9111, "section": "5.2.2.1"},
    ]
    assert recall_at_k(retrieved, gold, 2) == 0.5


def test_two_chunks_on_the_same_section_are_not_double_counted():
    # Both chunks map to the SAME single gold section - union, not count.
    retrieved = [
        {"rfc": 9110, "sections": ["10.2.3"]},
        {"rfc": 9110, "sections": ["10.2.3"]},
    ]
    gold = [{"rfc": 9110, "section": "10.2.3"}]
    assert recall_at_k(retrieved, gold, 2) == 1.0
    assert sections_found(retrieved, 2) == {(9110, "10.2.3")}


def test_one_chunk_straddling_two_sections_credits_both():
    retrieved = [{"rfc": 9110, "sections": ["10.2.2", "10.2.3"]}]
    gold_a = [{"rfc": 9110, "section": "10.2.2"}]
    gold_b = [{"rfc": 9110, "section": "10.2.3"}]
    assert recall_at_k(retrieved, gold_a, 1) == 1.0
    assert recall_at_k(retrieved, gold_b, 1) == 1.0


def test_aggregate_computes_overall_and_per_category_means():
    rows = [
        {"category": "direct_factual", "recall_at_5": 1.0, "mrr": 1.0},
        {"category": "direct_factual", "recall_at_5": 0.0, "mrr": 0.0},
        {"category": "multi_section", "recall_at_5": 0.5, "mrr": 0.5},
    ]
    result = aggregate(rows)
    assert result["overall"]["recall_at_5"] == 0.5
    assert result["overall_n"] == 3
    assert result["by_category"]["direct_factual"]["recall_at_5"] == 0.5
    assert result["by_category"]["direct_factual"]["n"] == 2
    assert result["by_category"]["multi_section"]["recall_at_5"] == 0.5
    assert result["by_category"]["multi_section"]["n"] == 1
