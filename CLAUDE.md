# Working conventions — rfc-rag-evaluation

This is a solo portfolio project, not a LIS repository — the global
`CLAUDE.md` scopes its Mode A / Mode B workflow to LIS repos only. This file
extends the same idea here, by explicit request, adapted to what this project
actually is.

See `README.md` for the technical spec. This file is only about how we work,
not what we're building.

---

## Mode A — pair programming (explain, wait for approval)

Anything that is itself part of the project's story — the stuff that has to be
defensible in an interview, not just working.

- Chunking strategy: window size, overlap, section-aware logic
- Any evaluation metric definition or formula (Recall@k, MRR, RRF, stale
  evidence rate, hit rate)
- The gold-label schema and what counts as a "hit"
- Ablation configuration definitions — what exactly changes between C0-C3, D1
- Generation prompt wording
- Anything where more than one reasonable design exists

Before implementing: explain the approach, wait for approval. If implementing
reveals the plan has to change materially, stop and explain before expanding
scope — same as the global rule.

## Mode B — mechanical, proceed without asking per file

- Corpus fetch / caching script
- CLI wiring, argument parsing, config loading
- Standard library usage following documented patterns (sentence-transformers,
  BM25 library, exact vector search)
- File I/O, logging boilerplate
- Test scaffolding once the first test in a category establishes the pattern

**Tooling split:** Mode B work is offloaded to GitHub Copilot (student pack) to
save tokens here — this session isn't the one writing it. When a task is Mode
B, say so explicitly and hand over a short, self-contained prompt Copilot can
run with, rather than implementing it. Mode A and the gray zone below stay
here, because the value there is the back-and-forth, not typing speed — see
the reasoning in the chat history for why this split exists.

Don't review Mode B output here as a matter of routine — that partly defeats
the point of offloading it. Bring it back only if something fails or there's
a real question about it. (Reviewing is cheaper than writing token-for-token,
but "cheaper than the alternative" isn't the same as "free" — the point of the
split is to not spend tokens here on mechanical work at all.)

## Gray zone — draft it, then explain it back before moving on

These get implemented at Mode B speed, but the point of writing them at all is
lost if they're just accepted without being understood — they're also exactly
where the spec itself warns a silent bug produces plausible-looking wrong
numbers instead of crashing:

- Recall@k / MRR / hit-rate computation
- Chunk-to-section mapping
- RRF fusion

Rule of thumb: before moving to the next piece, be able to explain this one
back in your own words, not just read the diff and accept it.

## Commits

- No ticket prefix — this isn't a LIS repo. Plain imperative messages,
  following what's already in the log.
- No `Co-Authored-By` line. Portfolio work; commits read as solely mine.
- Don't push without being asked, same as the global rule.

## Repo state

- Private for now. Only goes public once the MVP (C0 vs C1), core tests and
  real measured results exist — not before, and not without being asked.
- No LICENSE file for now — not yet decided, revisit before going public.
