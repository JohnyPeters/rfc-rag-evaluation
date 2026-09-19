"""Parse and validate citations from a generated answer.

Citation format is fixed by the prompt (src/generation/prompt.py): exactly
"RFC <number> §<section>". Validity means every citation the model produced
actually corresponds to a chunk that was in the context IT WAS GIVEN for
this call - not "exists somewhere in the corpus". A citation to a real,
correct section the model was never shown is still a fabrication.
"""

from __future__ import annotations

import re

from src.generation.prompt import REFUSAL_TEXT

_CITATION_RE = re.compile(r"RFC\s+(\d+)\s*§\s*([\d.]+)")


def extract_citations(answer: str) -> list[tuple[int, str]]:
    """All (rfc, section) pairs cited in the answer, in the order they appear.
    Duplicates are kept - citation_validity_rate below de-duplicates."""
    return [(int(rfc), section) for rfc, section in _CITATION_RE.findall(answer)]


def is_refusal(answer: str) -> bool:
    """True if the answer is the exact fixed refusal sentence the prompt
    requires - not a fuzzy "sounds like a refusal" check. If the model
    refuses in different words, that is a prompt-following failure, not a
    refusal we should credit it for."""
    return answer.strip() == REFUSAL_TEXT


def citation_validity(answer: str, context_chunks: list[dict]) -> dict:
    """Check every citation in the answer against what was actually supplied.

    context_chunks: the exact chunks passed to build_user_message() for this
    call - each with "rfc" and "sections".

    Returns {"citations": [...], "valid": [...], "invalid": [...],
    "validity_rate": float}. validity_rate is 1.0 for a refusal or an answer
    with no citations at all (nothing to be wrong about) - see the note
    below on why that is the right default, not a free pass.
    """
    supplied: set[tuple[int, str]] = set()
    for chunk in context_chunks:
        rfc = chunk["rfc"]
        for section in chunk.get("sections", []):
            supplied.add((rfc, section))

    cited = extract_citations(answer)
    if not cited:
        # No citations to check. A refusal correctly has none. A non-refusal
        # answer with zero citations is a DIFFERENT failure (an unsupported
        # claim) - that is caught by is_refusal() and a separate check the
        # generation-evaluation harness runs, not by this function inventing
        # a validity score for citations that were never made.
        return {"citations": [], "valid": [], "invalid": [], "validity_rate": 1.0}

    valid = [c for c in cited if c in supplied]
    invalid = [c for c in cited if c not in supplied]
    return {
        "citations": cited,
        "valid": valid,
        "invalid": invalid,
        "validity_rate": len(valid) / len(cited),
    }


def citation_relevance(answer: str, gold_sections: list[dict]) -> float:
    """Fraction of the answer's citations that intersect the query's gold
    sections. 1.0 if the answer has no citations (nothing irrelevant was
    cited, same reasoning as citation_validity's empty case)."""
    gold = {(g["rfc"], g["section"]) for g in gold_sections}
    cited = set(extract_citations(answer))
    if not cited:
        return 1.0
    return len(cited & gold) / len(cited)
