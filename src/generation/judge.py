"""LLM-as-judge prompts and output parsing for answer correctness and
faithfulness. See README.md's Generation Evaluation section for why these
are separate metrics - correctness asks "is this factually right (per the
reference)?", faithfulness asks "is this actually grounded in what was
supplied?", and they can diverge in either direction (q044's CORS answer is
probably correct and definitely unfaithful; a stale-evidence answer can be
faithful to the wrong document and definitely incorrect).

Judge model: the same generator (llama3.1:8b), for simplicity and zero
extra cost - a documented self-judging bias risk, not an oversight. This is
exactly why the judge-human agreement check (Roadmap) is load-bearing here,
not optional polish.

Output format is deliberately NOT strict JSON: the generator itself failed
to hold an exact format under simple instructions once already (the q028
refusal-with-commentary case). A judge running on the same 8B model needs a
format robust to trailing commentary, not one that breaks on it - a fixed
first line, parsed with a tolerant regex, free text after.
"""

from __future__ import annotations

import re

CORRECTNESS_PROMPT = """You are grading whether a generated answer is factually correct compared to a reference answer.

Question: {question}

Reference answer: {reference_answer}

Generated answer: {answer}

Judge the generated answer against the reference answer only - not against your own knowledge. Respond with a first line in exactly this format, then a brief justification:
VERDICT: correct
or
VERDICT: partially_correct
or
VERDICT: incorrect"""

FAITHFULNESS_PROMPT = """You are checking whether every factual claim in an answer is actually supported by the given context - not whether the claim is true in general, only whether THIS context supports it.

Context:
{context}

Answer to check: {answer}

List every distinct factual claim in the answer. For each one, output exactly two lines:
CLAIM: <the claim, in your own words>
SUPPORTED: yes
or
SUPPORTED: no
A claim is "yes" only if the context above states it or clearly implies it. If the answer makes no factual claims (e.g. it is a refusal), output only:
NO_CLAIMS"""

_VERDICT_RE = re.compile(r"VERDICT:\s*(correct|partially_correct|incorrect)", re.IGNORECASE)
_SUPPORTED_RE = re.compile(r"SUPPORTED:\s*(yes|no)", re.IGNORECASE)

_CORRECTNESS_SCORE = {"correct": 1.0, "partially_correct": 0.5, "incorrect": 0.0}


def build_correctness_prompt(question: str, answer: str, reference_answer: str) -> str:
    return CORRECTNESS_PROMPT.format(question=question, answer=answer, reference_answer=reference_answer)


def build_faithfulness_prompt(answer: str, context: str) -> str:
    return FAITHFULNESS_PROMPT.format(answer=answer, context=context)


def parse_correctness(judge_output: str) -> dict:
    """{"verdict": "correct"|"partially_correct"|"incorrect"|None, "score": float|None}.
    None means the judge did not produce a parseable verdict at all - a
    judge-following failure to be reported, not silently defaulted to zero.
    """
    match = _VERDICT_RE.search(judge_output)
    if not match:
        return {"verdict": None, "score": None}
    verdict = match.group(1).lower()
    return {"verdict": verdict, "score": _CORRECTNESS_SCORE[verdict]}


def parse_faithfulness(judge_output: str) -> dict:
    """{"n_claims": int, "n_supported": int, "faithfulness_score": float|None}.
    faithfulness_score is None (not 0.0 or 1.0) when there were no claims to
    check at all - "nothing was unsupported" is not the same claim as
    "nothing was checked", and conflating them would silently inflate the
    aggregate with vacuous cases.

    Real CLAIM/SUPPORTED pairs are checked FIRST, before falling back to the
    NO_CLAIMS case - not the other way around. A bug that checked for the
    literal string "NO_CLAIMS" anywhere in the output before looking for
    real pairs was caught in production: llama3.1:8b sometimes appends a
    stray "NO_CLAIMS" line after already listing genuine claims (observed on
    q001, 17 real pairs followed by a spurious trailing NO_CLAIMS), and that
    ordering was discarding every genuine judgement whenever it happened -
    responsible for most of a ~29% "unparseable" rate on the first real run.
    """
    verdicts = [v.lower() for v in _SUPPORTED_RE.findall(judge_output)]
    if not verdicts:
        return {"n_claims": 0, "n_supported": 0, "faithfulness_score": None}
    n_supported = sum(1 for v in verdicts if v == "yes")
    return {
        "n_claims": len(verdicts),
        "n_supported": n_supported,
        "faithfulness_score": n_supported / len(verdicts),
    }
