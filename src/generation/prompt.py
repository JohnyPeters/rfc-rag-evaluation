"""The generation prompt and context format - fixed across every
configuration (C0-C3), by design. See README.md's Experiments section:
"Held fixed across all four: ... prompt ..." - changing this between
configurations would confound the ladder's single-variable comparisons.

Citation format is deliberately rigid ("RFC <n> §<section>") so parsing it
back out of the model's answer (src/generation/citations.py) does not need
to guess at loose natural-language phrasing.
"""

SYSTEM_PROMPT = """You are a technical assistant answering questions about HTTP protocol specifications using ONLY the excerpts provided below.

Rules, follow them strictly:
1. Answer using only the information in the provided context. Do not use any outside knowledge, even if you are confident it is correct.
2. Every factual claim must be followed by a citation in exactly this format: RFC <number> §<section>. Use one citation per claim, referencing the excerpt it came from.
3. If the provided context does not contain enough information to answer the question, respond with exactly this sentence and nothing else: "I don't have enough information in the provided context to answer this question."
4. Be concise. Do not repeat the question or add unrequested commentary."""

REFUSAL_TEXT = "I don't have enough information in the provided context to answer this question."


def format_context(chunks: list[dict]) -> str:
    """One labelled block per chunk, in the order given (already ranked).

    Each chunk must have "rfc", "sections" (list of section numbers this
    chunk maps to - see src/chunking/mapping.py) and "text".
    """
    blocks = []
    for chunk in chunks:
        rfc = chunk["rfc"]
        sections = chunk.get("sections") or ["?"]
        label = " / ".join(f"RFC {rfc} §{s}" for s in sections)
        blocks.append(f"[{label}]\n{chunk['text']}")
    return "\n\n".join(blocks)


def build_user_message(query: str, chunks: list[dict]) -> str:
    return f"Context:\n{format_context(chunks)}\n\nQuestion: {query}"
