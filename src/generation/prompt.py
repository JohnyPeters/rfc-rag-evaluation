"""The generation prompt and context format - fixed across every
configuration (C0-C3), by design. See README.md's Experiments section:
"Held fixed across all four: ... prompt ..." - changing this between
configurations would confound the ladder's single-variable comparisons.
The validity label added below is an exception that proves the rule: it is
applied identically in every configuration, so it changes absolute
generation quality everywhere at once without confounding the *relative*
C0-C3 comparison, which is what "fixed" is actually protecting.

Citation format is deliberately rigid ("RFC <n> §<section>") so parsing it
back out of the model's answer (src/generation/citations.py) does not need
to guess at loose natural-language phrasing. The validity tag is metadata
about the excerpt, not part of the citation format, and is never expected
back in the model's answer - citations.py's regex is unaffected by it.

Why the tag exists at all: C3's validity filter (src/retrieval/validity_filter.py)
decides current-vs-obsoleted at retrieval time, by reordering candidates
before generation ever sees them. If it successfully pushes an obsoleted
chunk below the cutoff, generation never sees it and has nothing to decide.
But if too few non-penalised candidates exist to fill k, an obsoleted chunk
can still reach generation - and without this tag, the model has no way to
tell current from obsoleted from the text alone (that is precisely the
premise of this whole project: the wording reads nearly identically across
eras). The tag is a second, independent line of defence at the generation
layer, not a replacement for the retrieval-side filter.
"""

SYSTEM_PROMPT = """You are a technical assistant answering questions about HTTP protocol specifications using ONLY the excerpts provided below.

Rules, follow them strictly:
1. Answer using only the information in the provided context. Do not use any outside knowledge, even if you are confident it is correct.
2. Every factual claim must be followed by a citation in exactly this format: RFC <number> §<section>. Use one citation per claim, referencing the excerpt it came from.
3. Some excerpts are marked [OBSOLETED - see RFC <n> instead]. When an excerpt without that mark covers the same point, prefer it. Use an OBSOLETED excerpt anyway only if the question explicitly names that exact RFC number.
4. If the provided context does not contain enough information to answer the question, respond with exactly this sentence and nothing else: "I don't have enough information in the provided context to answer this question."
5. Be concise. Do not repeat the question or add unrequested commentary."""

REFUSAL_TEXT = "I don't have enough information in the provided context to answer this question."


def _validity_tag(rfc: int, rfc_metadata: dict | None) -> str:
    """" (OBSOLETED - see RFC <n> instead)" for an obsoleted RFC with a known
    replacement, "" for a current RFC or when no metadata is available."""
    if not rfc_metadata:
        return ""
    meta = rfc_metadata.get(str(rfc))
    if not meta or meta.get("status") != "obsoleted":
        return ""
    replacements = meta.get("obsoleted_by") or []
    if not replacements:
        return ""
    named = ", ".join(f"RFC {r}" for r in replacements)
    return f" [OBSOLETED - see {named} instead]"


def format_context(chunks: list[dict], rfc_metadata: dict | None = None) -> str:
    """One labelled block per chunk, in the order given (already ranked).

    Each chunk must have "rfc", "sections" (list of section numbers this
    chunk maps to - see src/chunking/mapping.py) and "text". rfc_metadata,
    if given, is the loaded data/rfc_metadata.json dict - used only to add
    the validity tag; omitting it (e.g. in a quick manual test) just means
    no tag is added, not an error.
    """
    blocks = []
    for chunk in chunks:
        rfc = chunk["rfc"]
        sections = chunk.get("sections") or ["?"]
        label = " / ".join(f"RFC {rfc} §{s}" for s in sections)
        blocks.append(f"[{label}{_validity_tag(rfc, rfc_metadata)}]\n{chunk['text']}")
    return "\n\n".join(blocks)


def build_user_message(query: str, chunks: list[dict], rfc_metadata: dict | None = None) -> str:
    return f"Context:\n{format_context(chunks, rfc_metadata)}\n\nQuestion: {query}"
