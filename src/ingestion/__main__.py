"""Command-line entry point for RFC ingestion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .artefacts import read_rfc
from .sections import extract_sections, load_metadata


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest RFCs into section JSON.")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("rfc", nargs="?", type=int, help="RFC number to ingest")
    selection.add_argument("--all", action="store_true", help="Ingest every raw RFC")
    return parser.parse_args()


def _process(number: int, root: Path, metadata: dict) -> None:
    source = root / "data" / "raw" / f"rfc{number}.txt"
    if not source.is_file():
        raise FileNotFoundError(f"RFC source does not exist: {source}")

    result = read_rfc(source)
    sections = extract_sections(result.text)
    output = {
        "rfc_number": number,
        "metadata": metadata.get(str(number), {}),
        "sections": sections,
    }
    destination = root / "data" / "processed" / "sections" / f"rfc{number}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"RFC {number}: {len(sections)} sections, "
        f"{result.boundaries} form-feed boundaries, "
        f"{result.lines_removed} pagination lines stripped"
    )


def main() -> None:
    args = _arguments()
    root = Path(__file__).resolve().parents[2]
    metadata = load_metadata(root / "data" / "rfc_metadata.json")
    if args.all:
        numbers = sorted(
            int(path.stem[3:])
            for path in (root / "data" / "raw").glob("rfc*.txt")
            if path.stem[3:].isdigit()
        )
    else:
        numbers = [args.rfc]
    for number in numbers:
        _process(number, root, metadata)


if __name__ == "__main__":
    main()
