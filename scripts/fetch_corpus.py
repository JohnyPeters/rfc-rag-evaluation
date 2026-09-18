"""Download and cache the RFC corpus and its official metadata."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests
from lxml import etree


RFC_NUMBERS = (
    9110,
    9111,
    9112,
    9113,
    9114,
    7541,
    9204,
    6265,
    2616,
    7230,
    7231,
    7232,
    7233,
    7234,
    7235,
    7540,
)
CURRENT_RFC_NUMBERS = {9110, 9111, 9112, 9113, 9114, 7541, 9204, 6265}
BASE_URL = "https://www.rfc-editor.org"
INDEX_URL = f"{BASE_URL}/rfc-index.xml"
USER_AGENT = "rfc-rag-evaluation/1.0 (corpus fetcher)"
REQUEST_DELAY_SECONDS = 1.0


def _download(
    session: requests.Session,
    url: str,
    destination: Path,
    description: str,
) -> bool:
    """Download one file, retrying one time after an HTTP or network failure."""
    if destination.exists():
        print(f"Skipped {description}: cached at {destination}")
        return False

    last_error: Exception | None = None
    for attempt in range(2):
        if attempt:
            time.sleep(REQUEST_DELAY_SECONDS)
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(response.content)
            print(f"Downloaded {description}: {destination}")
            return True
        except (requests.RequestException, OSError) as error:
            last_error = error

    raise RuntimeError(
        f"Failed to download {description} from {url} after 2 attempts: "
        f"{last_error}"
    ) from last_error


def _text(element: etree._Element) -> str:
    return (element.text or "").strip()


def _related_numbers(entry: etree._Element, relationship: str) -> list[int]:
    values = []
    for element in entry.findall(f"{{*}}{relationship}/{{*}}doc-id"):
        value = _text(element)
        if value.startswith("RFC") and value[3:].isdigit():
            values.append(int(value[3:]))
    return sorted(set(values))


def _build_metadata(index_path: Path) -> dict[str, dict[str, Any]]:
    tree = etree.parse(str(index_path))
    metadata = {
        str(number): {
            "status": "current" if number in CURRENT_RFC_NUMBERS else "obsoleted",
            "obsoletes": [],
            "obsoleted_by": [],
        }
        for number in RFC_NUMBERS
    }

    for entry in tree.findall(".//{*}rfc-entry"):
        doc_id = entry.find("{*}doc-id")
        if doc_id is None:
            continue
        value = _text(doc_id)
        if not value.startswith("RFC") or not value[3:].isdigit():
            continue
        number = int(value[3:])
        if number not in RFC_NUMBERS:
            continue
        metadata[str(number)]["obsoletes"] = _related_numbers(entry, "obsoletes")
        metadata[str(number)]["obsoleted_by"] = _related_numbers(
            entry, "obsoleted-by"
        )

    return metadata


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    raw_dir = data_dir / "raw"
    index_path = data_dir / "rfc-index.xml"

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    for position, number in enumerate(RFC_NUMBERS):
        if position:
            time.sleep(REQUEST_DELAY_SECONDS)
        _download(
            session,
            f"{BASE_URL}/rfc/rfc{number}.txt",
            raw_dir / f"rfc{number}.txt",
            f"RFC {number}",
        )

    if RFC_NUMBERS:
        time.sleep(REQUEST_DELAY_SECONDS)
    _download(session, INDEX_URL, index_path, "RFC index")

    metadata_path = data_dir / "rfc_metadata.json"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(_build_metadata(index_path), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote RFC metadata: {metadata_path}")


if __name__ == "__main__":
    main()
