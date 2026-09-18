"""C3's validity filter: down-weight obsoleted evidence, but only when it is
safe to. See README.md "C3, precisely" for the full reasoning; summary:

- A ranked candidate from an obsoleted RFC is penalised (pushed after every
  non-penalised candidate) ONLY if a document that obsoletes it is ALSO
  present among the candidates for this query - if the current replacement
  was never retrieved at all, there is nothing to prefer over it, and
  suppressing the only evidence available would manufacture a false refusal.
- That penalty is skipped entirely for any RFC the query names explicitly
  (e.g. "In RFC 2616, ..."), so the *explicit historical version* category
  is never suppressed by this mechanism - detection is a plain "RFC <n>"
  regex against the query text, not a heuristic that has to be tuned.
- The demotion itself is a partition, not a numeric score penalty: every
  non-penalised candidate keeps its relative order and comes first; every
  penalised candidate keeps its relative order and comes after. No penalty
  magnitude to justify or tune.

Explicitly out of scope (see README.md's C3 / Optional Extensions): queries
that are themselves ABOUT how something evolved across versions want several
eras surfaced together, not one preferred over the others - this filter does
not attempt to detect that case.
"""

from __future__ import annotations

import re

_RFC_MENTION_RE = re.compile(r"\bRFC\s*(\d{3,5})\b", re.IGNORECASE)


def mentioned_rfcs(query: str) -> set[int]:
    """RFC numbers the query names explicitly, e.g. "RFC 2616" -> {2616}."""
    return {int(n) for n in _RFC_MENTION_RE.findall(query)}


def apply_validity_filter(
    ranked: list[tuple],
    query: str,
    rfc_metadata: dict,
) -> list[tuple]:
    """Reorder ranked candidates so obsoleted-with-a-present-replacement ones
    sort after everything else, unless the query names that RFC explicitly.

    ranked: list of (item_id, score, rfc) tuples, best first - rfc is that
        candidate's source RFC number (int).
    rfc_metadata: dict keyed by RFC number as a string, each value having at
        least {"status": "current"|"obsoleted", "obsoleted_by": [...]}.

    Returns the same tuples, reordered. Relative order within each of the
    two groups (kept, penalised) is preserved from the input ranking.
    """
    exempt = mentioned_rfcs(query)
    present_rfcs = {rfc for _, _, rfc in ranked}

    def is_penalised(rfc: int) -> bool:
        if rfc in exempt:
            return False
        meta = rfc_metadata.get(str(rfc))
        if not meta or meta.get("status") != "obsoleted":
            return False
        replacements = set(meta.get("obsoleted_by", []))
        return bool(replacements & present_rfcs)

    kept = [item for item in ranked if not is_penalised(item[2])]
    penalised = [item for item in ranked if is_penalised(item[2])]
    return kept + penalised
