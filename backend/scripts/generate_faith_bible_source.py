#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


SECTION_TITLES = [
    "The Promises of God",
    "Promises to Take with You to Your Prayer Closet",
    "Answered Prayer",
    "Assurance",
    "Confidence",
    "Depression",
    "Distress",
    "Faith",
    "Fear",
    "Financial Need",
    "Forgiveness",
    "Fruitfulness",
    "God's Faithfulness",
    "God's Providence",
    "Guidance",
    "Guilt",
    "Healing for the Backslider",
    "Hope",
    "Joy",
    "Loneliness",
    "Marriage",
    "Peace",
    "Perseverance",
    "Persistence",
    "Pressing On",
    "Providence",
    "Reconciliation",
    "Revival",
    "Salvation",
    "Seeking God",
    "Sleeplessness",
    "Suffering",
    "Temptation",
    "The Holy Spirit",
    "Trials",
    "Trouble",
    "Victory Over Sin",
    "Waiting on God",
    "Weariness",
    "Wisdom",
    "Worry",
    "My God is Able",
    "God's Provision",
]


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


def _normalize_text(value: str) -> str:
    value = (
        value.replace("\x0c", "\n")
        .replace(""", '"')
        .replace(""", '"')
        .replace("'", "'")
        .replace("'", "'")
        .replace("--", "-")
    )
    return re.sub(r"\s+", " ", value).strip()


def build_source_catalog(pdf_path: Path) -> list[dict]:
    raw_text = _read_pdf_text(pdf_path)
    lines = [line.replace("\x0c", "").strip() for line in raw_text.splitlines()]
    title_set = set(SECTION_TITLES)
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in lines:
        if line in title_set:
            if current_title and current_lines:
                sections.append((current_title, current_lines))
            current_title = line
            current_lines = []
            continue
        if current_title:
            current_lines.append(line)

    if current_title and current_lines:
        sections.append((current_title, current_lines))

    merged: dict[str, dict] = {}
    for title, content_lines in sections:
        section_text = _normalize_text(" ".join(content_lines))
        verse_entries = []
        for match in re.finditer(r'"([^"]+)"\s*\(([^)]+)\)', section_text):
            quote = _normalize_text(match.group(1))
            reference = _normalize_text(match.group(2))
            if len(quote) < 20 or len(reference) < 3:
                continue
            verse_entries.append({"reference": reference, "text": quote})
        if verse_entries:
            slug = _slugify(title)
            bucket = merged.setdefault(
                slug,
                {
                    "slug": slug,
                    "title": title,
                    "source_label": "The Book of Bible Promises",
                    "source_pdf": pdf_path.name,
                    "source_type": "primary_topic_spine",
                    "verses": [],
                },
            )
            for verse in verse_entries:
                if verse not in bucket["verses"]:
                    bucket["verses"].append(
                        {
                            **verse,
                            "source_section_slug": slug,
                            "source_section_title": title,
                        }
                    )

    catalog = []
    for slug, item in merged.items():
        item["verse_count"] = len(item["verses"])
        catalog.append(item)
    catalog.sort(key=lambda entry: entry["title"])
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Faith Bible source topic catalog.")
    parser.add_argument(
        "--pdf",
        default="/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/the_book_of_bible_promises.pdf",
        help="Path to the Bible promises PDF.",
    )
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().parents[1] / "assets" / "faith" / "bible_promises_source.json",
        type=Path,
        help="Output JSON path.",
    )
    args = parser.parse_args()

    catalog = build_source_catalog(Path(args.pdf))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    print(f"Wrote {len(catalog)} Bible source sections to {args.output}")
    if catalog:
        print(f"First section: {catalog[0]['title']} ({catalog[0]['verse_count']} verses)")
        print(f"Last section: {catalog[-1]['title']} ({catalog[-1]['verse_count']} verses)")


if __name__ == "__main__":
    main()
