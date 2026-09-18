"""Command-line entry point for RFC chunking."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .fixed_window import chunk_fixed_window
from .mapping import map_chunks_to_sections
from .section_aware import chunk_section_aware


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chunk ingested RFCs.")
    parser.add_argument("--strategy", choices=("fixed_window", "section_aware"), required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--rfc", type=int)
    selection.add_argument("--all", action="store_true")
    return parser.parse_args()


def _numbers(root: Path, args: argparse.Namespace) -> list[int]:
    if args.all:
        return sorted(
            int(path.stem[3:])
            for path in (root / "data" / "raw").glob("rfc*.txt")
            if path.stem[3:].isdigit()
        )
    return [args.rfc]


def _process(number: int, strategy: str, root: Path) -> None:
    raw = (root / "data" / "raw" / f"rfc{number}.txt").read_text(encoding="utf-8-sig")
    section_data: dict[str, Any] = json.loads(
        (root / "data" / "processed" / "sections" / f"rfc{number}.json").read_text(
            encoding="utf-8-sig"
        )
    )
    sections = section_data["sections"]
    chunks = (
        chunk_fixed_window(raw, number)
        if strategy == "fixed_window"
        else chunk_section_aware(sections, number)
    )
    map_chunks_to_sections(chunks, sections)
    destination = root / "data" / "processed" / "chunks" / f"rfc{number}_{strategy}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(chunks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    average = sum(len(str(chunk["text"])) for chunk in chunks) / len(chunks) if chunks else 0
    multi = sum(len(chunk["sections"]) > 1 for chunk in chunks)
    print(f"RFC {number}: {len(chunks)} chunks, average length {average:.1f}, mapped to >1 section: {multi}")


def main() -> None:
    args = _arguments()
    root = Path(__file__).resolve().parents[2]
    for number in _numbers(root, args):
        _process(number, args.strategy, root)


if __name__ == "__main__":
    main()
