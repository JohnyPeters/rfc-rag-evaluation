"""Hand-computed verification of RRF fusion - see README.md's worked example
(dense: A,B,C,D,E; BM25: F,C,A,G,B) for the numbers this mirrors.
"""

from src.retrieval.fusion import rrf_fuse

DENSE = ["A", "B", "C", "D", "E"]
BM25 = ["F", "C", "A", "G", "B"]


def test_matches_hand_computed_example():
    result = dict(rrf_fuse([DENSE, BM25], k=60))
    assert result["A"] == 1 / 61 + 1 / 63
    assert result["C"] == 1 / 63 + 1 / 62
    assert result["B"] == 1 / 62 + 1 / 65
    assert result["F"] == 1 / 61
    assert result["D"] == 1 / 64
    assert result["G"] == 1 / 64
    assert result["E"] == 1 / 65


def test_ranking_order_matches_hand_computed_example():
    order = [item for item, _ in rrf_fuse([DENSE, BM25], k=60)]
    assert order[0] == "A"   # top of dense + mid of BM25 beats BM25's own #1
    assert order[1] == "C"   # never #1 anywhere, but decent in both - wins by consensus
    assert order[3] == "F"   # BM25's #1, absent from dense - drops out of the top 3


def test_item_absent_from_both_lists_never_appears():
    result = dict(rrf_fuse([DENSE, BM25], k=60))
    assert "Z" not in result


def test_single_list_fusion_is_just_that_lists_own_ranks():
    result = dict(rrf_fuse([DENSE], k=60))
    assert result["A"] == 1 / 61
    assert result["E"] == 1 / 65
