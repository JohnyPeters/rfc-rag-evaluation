"""Retrieval metrics: Recall@k, MRR, hit rate.

Scoring rule (see README.md "Retrieval Evaluation" and "Scoring, precisely"):
a query's gold is a set of (rfc, section) pairs. A retrieved chunk maps to
zero, one or several sections via its precomputed "sections" field (already
built with the min(100, section_length) overlap threshold - see
src/chunking/mapping.py). Recall@k is computed over the UNION of sections
found across the top-k chunks, never per-chunk - several chunks landing on
the same section must not be double-counted, and one chunk straddling two
sections must credit both.
"""

from __future__ import annotations


def _gold_set(gold_sections: list[dict]) -> set[tuple[int, str]]:
    return {(g["rfc"], g["section"]) for g in gold_sections}


def _chunk_sections(chunk: dict) -> set[tuple[int, str]]:
    rfc = chunk["rfc"]
    return {(rfc, s) for s in chunk.get("sections", [])}


def sections_found(retrieved_chunks: list[dict], k: int) -> set[tuple[int, str]]:
    """Union of sections mapped to the top-k retrieved chunks, deduplicated."""
    found: set[tuple[int, str]] = set()
    for chunk in retrieved_chunks[:k]:
        found |= _chunk_sections(chunk)
    return found


def recall_at_k(retrieved_chunks: list[dict], gold_sections: list[dict], k: int) -> float:
    """Fraction of gold sections present in the union of the top-k chunks' sections."""
    gold = _gold_set(gold_sections)
    if not gold:
        raise ValueError("recall_at_k requires at least one gold section")
    found = sections_found(retrieved_chunks, k)
    return len(found & gold) / len(gold)


def hit_rate_at_k(retrieved_chunks: list[dict], gold_sections: list[dict], k: int) -> float:
    """1.0 if at least one gold section is present in the top-k, else 0.0."""
    gold = _gold_set(gold_sections)
    found = sections_found(retrieved_chunks, k)
    return 1.0 if found & gold else 0.0


def reciprocal_rank(retrieved_chunks: list[dict], gold_sections: list[dict], k_max: int) -> float:
    """1/rank of the first chunk (within the top-k_max) whose sections intersect gold.

    0.0 if no chunk within k_max hits the gold. Rank is 1-indexed.
    """
    gold = _gold_set(gold_sections)
    for rank, chunk in enumerate(retrieved_chunks[:k_max], start=1):
        if _chunk_sections(chunk) & gold:
            return 1.0 / rank
    return 0.0


def aggregate(per_query_scores: list[dict]) -> dict:
    """Mean of each numeric field across a list of per-query score dicts,
    both overall and grouped by the 'category' field. per_query_scores
    entries look like {"category": ..., "recall_at_5": ..., "mrr": ..., ...}.
    """
    if not per_query_scores:
        raise ValueError("aggregate requires at least one query")

    metric_names = [k for k in per_query_scores[0] if k != "category"]

    def _mean(rows: list[dict], name: str) -> float:
        return sum(r[name] for r in rows) / len(rows)

    result = {"overall": {name: _mean(per_query_scores, name) for name in metric_names},
              "overall_n": len(per_query_scores),
              "by_category": {}}

    categories = sorted({r["category"] for r in per_query_scores})
    for cat in categories:
        rows = [r for r in per_query_scores if r["category"] == cat]
        result["by_category"][cat] = {name: _mean(rows, name) for name in metric_names}
        result["by_category"][cat]["n"] = len(rows)

    return result
