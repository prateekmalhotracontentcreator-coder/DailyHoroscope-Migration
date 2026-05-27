#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


IGNORED_HEADINGS = {
    "SCRIPTURE FOR EVERY MOMENT",
    "PEACE CHURCH",
}

HEADING_RE = re.compile(r"^[A-Z][A-Z -]+$")
REFERENCE_RE = re.compile(
    r"^(?:[1-3]|I{1,3})?\s*[A-Za-z][A-Za-z.'&\s-]*\d+:\d+(?:[--]\d+)?(?:,\d+(?:[--]\d+)?)?$"
)

REFERENCE_NORMALIZATIONS = {
    "Deut.": "Deuteronomy",
    "I Chron.": "1 Chronicles",
    "II Chron.": "2 Chronicles",
    "I Cor.": "1 Corinthians",
    "II Cor": "2 Corinthians",
    "II Cor.": "2 Corinthians",
    "I Peter": "1 Peter",
    "II Peter": "2 Peter",
    "I Samuel": "1 Samuel",
    "II Samuel": "2 Samuel",
    "Psalms": "Psalm",
}


def _slugify(value: str) -> str:
    normalized = value.lower().replace("&", "and").replace("'", "")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def _read_pdf_text(pdf_path: Path) -> str:
    return subprocess.run(
        ["pdftotext", str(pdf_path), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _normalize_reference(value: str) -> str:
    text = " ".join(value.replace("\x0c", " ").split())
    for old, new in REFERENCE_NORMALIZATIONS.items():
        text = text.replace(old, new)
    return text


def build_support_reference_catalog(pdf_path: Path) -> list[dict]:
    lines = [line.replace("\x0c", "").strip() for line in _read_pdf_text(pdf_path).splitlines()]
    buckets: dict[str, dict] = {}
    current_heading: str | None = None

    for line in lines:
        if not line:
            continue
        if HEADING_RE.fullmatch(line):
            if line in IGNORED_HEADINGS:
                continue
            current_heading = line
            if current_heading:
                slug = _slugify(current_heading)
                buckets.setdefault(
                    slug,
                    {
                        "slug": slug,
                        "title": current_heading.title(),
                        "source_heading": current_heading,
                        "source_label": "Scripture for Every Moment",
                        "source_pdf": pdf_path.name,
                        "source_type": "supporting_reference_bank",
                        "references": [],
                    },
                )
            continue

        if not current_heading or not REFERENCE_RE.fullmatch(line):
            continue

        slug = _slugify(current_heading)
        bucket = buckets[slug]
        reference = _normalize_reference(line)
        if reference not in bucket["references"]:
            bucket["references"].append(reference)

    catalog = []
    for item in buckets.values():
        item["reference_count"] = len(item["references"])
        if item["reference_count"] > 0:
            catalog.append(item)

    catalog.sort(key=lambda entry: entry["title"])
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Faith Bible supporting reference catalog.")
    parser.add_argument(
        "--pdf",
        default="/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Scripture_for_Every_Moment.pdf",
        help="Path to the Scripture for Every Moment PDF.",
    )
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().parents[1] / "assets" / "faith" / "bible_supporting_references.json",
        type=Path,
        help="Output JSON path.",
    )
    args = parser.parse_args()

    catalog = build_support_reference_catalog(Path(args.pdf))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    print(f"Wrote {len(catalog)} supporting reference sections to {args.output}")
    if catalog:
        print(f"First section: {catalog[0]['title']} ({catalog[0]['reference_count']} refs)")
        print(f"Last section: {catalog[-1]['title']} ({catalog[-1]['reference_count']} refs)")


if __name__ == "__main__":
    main()
