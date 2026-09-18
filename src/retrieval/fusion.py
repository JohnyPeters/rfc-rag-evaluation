"""Reciprocal Rank Fusion (RRF) for combining dense and BM25 rankings.

See README.md "C2's RRF, precisely: unweighted." - this is the exact formula
documented there: RRF(item) = sum over each ranked list the item appears in
of 1 / (k + rank), rank is 1-indexed, no per-list weight. A weighted variant
is a deliberate, documented extension (see "Optional extensions"), not
implemented here.

Items are identified by whatever hashable id the caller uses consistently
across both ranked lists - in this project, that is the row index into a
strategy's embeddings/_meta.json ordering, since both the dense index and the
BM25 index are built over the same section_aware chunk ordering (see C2 in
the Experiments table: "= C1" chunking, hybrid retrieval only).
"""

from __future__ import annotations


def rrf_fuse(ranked_lists: list[list], k: int = 60) -> list[tuple]:
    """Fuse any number of ranked lists (each a list of item ids, best first).

    Returns a list of (item_id, rrf_score) sorted by score descending. An
    item appearing in more than one list gets its contributions summed - see
    the module docstring and README.md for the worked example of why this
    rewards items multiple signals agree on more than one signal's top pick.
    """
    scores: dict = {}
    for ranked_list in ranked_lists:
        for rank, item_id in enumerate(ranked_list, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
