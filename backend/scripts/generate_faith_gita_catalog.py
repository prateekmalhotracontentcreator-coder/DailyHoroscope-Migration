#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import unicodedata
from pathlib import Path


CHAPTER_TITLES = {
    1: "Observing the Armies on the Battlefield of Kurukshetra",
    2: "Contents of the Gita Summarized",
    3: "Karma-yoga",
    4: "Transcendental Knowledge",
    5: "Karma-yoga - Action in Krishna Consciousness",
    6: "Dhyana-yoga",
    7: "Knowledge of the Absolute",
    8: "Attaining the Supreme",
    9: "The Most Confidential Knowledge",
    10: "The Opulence of the Absolute",
    11: "The Universal Form",
    12: "Devotional Service",
    13: "Nature, the Enjoyer, and Consciousness",
    14: "The Three Modes of Material Nature",
    15: "The Yoga of the Supreme Person",
    16: "The Divine and Demoniac Natures",
    17: "The Divisions of Faith",
    18: "Conclusion - The Perfection of Renunciation",
}

CHAPTER_NAMES = [
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
    "SIX",
    "SEVEN",
    "EIGHT",
    "NINE",
    "TEN",
    "ELEVEN",
    "TWELVE",
    "THIRTEEN",
    "FOURTEEN",
    "FIFTEEN",
    "SIXTEEN",
    "SEVENTEEN",
    "EIGHTEEN",
]
CHAPTER_MAP = {name: index + 1 for index, name in enumerate(CHAPTER_NAMES)}
SPECIAL_VERSE_SPLITS = {
    (17, 8): [8, 9, 10],
}
SPECIAL_LINE_SPLITS = {
    (17, 8): [3, 3, 4],
}
SPECIAL_TRANSLATION_OVERRIDES = {
    (17, 8): "Foods in the mode of goodness increase the duration of life, purify one's existence and give strength, health, happiness and satisfaction. Such nourishing foods are sweet, juicy, fattening and palatable.",
    (17, 9): "Foods that are too bitter, too sour, salty, pungent, dry and hot, are liked by people in the modes of passion. Such foods cause pain, distress, and disease.",
    (17, 10): "Food cooked more than three hours before being eaten, which is tasteless, stale, putrid, decomposed and unclean, is food liked by people in the mode of ignorance.",
}


def _read_pdf_text(pdf_path: Path) -> str:
    return subprocess.run(
        ["pdftotext", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def _normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _to_ascii(value: str) -> str:
    stripped = "".join(
        char for char in unicodedata.normalize("NFKD", value) if not unicodedata.combining(char)
    )
    return stripped.replace("'", "'").replace(""", '"').replace(""", '"')


def _looks_like_iast(line: str) -> bool:
    candidate = line.strip()
    if not candidate:
        return False
    if "TRANSLATION" in candidate or "PURPORT" in candidate:
        return False
    if "--" in candidate:
        return False
    if any(char in candidate for char in "\\[]{}<>@#$%^*_+=|"):
        return False
    if "(" in candidate or ")" in candidate:
        return False
    if any(char.isdigit() for char in candidate):
        return False
    letters = [char for char in candidate if char.isalpha()]
    if not letters:
        return False
    lowered = sum(1 for char in letters if char.islower())
    return lowered / len(letters) > 0.8


def _split_iast_lines(chapter: int, start_verse: int, verse_numbers: list[int], iast_lines: list[str]) -> list[list[str]]:
    if not iast_lines:
        return [[] for _ in verse_numbers]

    special_key = (chapter, start_verse)
    if special_key in SPECIAL_LINE_SPLITS:
        sizes = SPECIAL_LINE_SPLITS[special_key]
    else:
        base = len(iast_lines) // len(verse_numbers)
        remainder = len(iast_lines) % len(verse_numbers)
        if base == 0:
            return [iast_lines[:] for _ in verse_numbers]
        sizes = [base + (1 if index < remainder else 0) for index in range(len(verse_numbers))]

    segments: list[list[str]] = []
    cursor = 0
    for size in sizes:
        segments.append(iast_lines[cursor : cursor + size])
        cursor += size
    if cursor < len(iast_lines) and segments:
        segments[-1].extend(iast_lines[cursor:])
    while len(segments) < len(verse_numbers):
        segments.append(iast_lines[:])
    return segments


def _split_translation(chapter: int, start_verse: int, verse_numbers: list[int], translation: str) -> list[str]:
    if len(verse_numbers) == 1:
        return [translation]

    special_key = (chapter, start_verse)
    if special_key == (17, 8):
        return [SPECIAL_TRANSLATION_OVERRIDES[(chapter, verse)] for verse in verse_numbers]

    return [translation for _ in verse_numbers]


def _parse_glossary(block_lines: list[str]) -> list[dict[str, str]]:
    glossary_lines: list[str] = []
    in_glossary = False
    for raw_line in block_lines:
        line = raw_line.strip()
        if not line:
            continue
        if line == "TRANSLATION":
            break
        if "--" in line:
            in_glossary = True
        if in_glossary:
            glossary_lines.append(line)
    glossary_text = _normalize_spaces(" ".join(glossary_lines))
    glossary: list[dict[str, str]] = []
    for chunk in glossary_text.split(";"):
        if "--" not in chunk:
            continue
        term, gloss = chunk.split("--", 1)
        cleaned_term = _normalize_spaces(term)
        cleaned_gloss = _normalize_spaces(gloss)
        if cleaned_term and cleaned_gloss:
            glossary.append({"term": cleaned_term, "gloss": cleaned_gloss})
    return glossary


def _parse_blocks(text: str) -> list[dict]:
    chapter_headers = {f"CHAPTER {name}" for name in CHAPTER_NAMES}
    lines = text.splitlines()
    current_chapter: int | None = None
    blocks: list[dict] = []
    current_block: dict | None = None

    for raw_line in lines:
        line = raw_line.replace("\x0c", "").rstrip()
        stripped = line.strip()
        if stripped in chapter_headers:
            current_chapter = CHAPTER_MAP[stripped.split()[-1]]
            continue

        match = re.match(r"^TEXTS?\s+(\d+)(?:\s*[--]\s*(\d+))?$", stripped)
        if match and current_chapter is not None:
            if current_block is not None:
                blocks.append(current_block)
            start = int(match.group(1))
            end = int(match.group(2) or start)
            current_block = {
                "chapter": current_chapter,
                "start": start,
                "end": end,
                "lines": [],
            }
            continue

        if current_block is not None:
            current_block["lines"].append(line)

    if current_block is not None:
        blocks.append(current_block)
    return blocks


def build_catalog(pdf_path: Path) -> list[dict]:
    blocks = _parse_blocks(_read_pdf_text(pdf_path))
    verses: list[dict] = []

    for block in blocks:
        chapter = block["chapter"]
        start = block["start"]
        end = block["end"]
        lines = block["lines"]

        verse_numbers = SPECIAL_VERSE_SPLITS.get((chapter, start), list(range(start, end + 1)))

        iast_lines: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped == "TRANSLATION" or stripped == "PURPORT":
                break
            if "--" in stripped:
                break
            if _looks_like_iast(stripped):
                iast_lines.append(stripped)

        translation_lines: list[str] = []
        in_translation = False
        for line in lines:
            stripped = line.strip()
            if stripped == "TRANSLATION":
                in_translation = True
                continue
            if stripped == "PURPORT":
                break
            if in_translation and stripped:
                translation_lines.append(stripped)
        translation = _normalize_spaces(" ".join(translation_lines))

        glossary = _parse_glossary(lines)
        iast_segments = _split_iast_lines(chapter, start, verse_numbers, iast_lines)
        translation_segments = _split_translation(chapter, start, verse_numbers, translation)

        for index, verse_number in enumerate(verse_numbers):
            verse_iast_lines = iast_segments[index] if index < len(iast_segments) else iast_lines
            verse_translation = translation_segments[index] if index < len(translation_segments) else translation
            verse_iast = _normalize_spaces(" ".join(verse_iast_lines))
            verses.append(
                {
                    "chapter": chapter,
                    "chapter_title": CHAPTER_TITLES[chapter],
                    "verse": verse_number,
                    "reference": f"Bhagavad Gita {chapter}:{verse_number}",
                    "iast": verse_iast,
                    "transliteration": _to_ascii(verse_iast),
                    "translation": SPECIAL_TRANSLATION_OVERRIDES.get((chapter, verse_number), verse_translation),
                    "glossary": glossary[:12],
                    "source": "Bhagavad-gita As It Is verse text",
                }
            )

    verses.sort(key=lambda item: (item["chapter"], item["verse"]))
    return verses


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Faith Gita verse catalog.")
    parser.add_argument(
        "--pdf",
        default="/Users/apple/Documents/Knowledge Engine_eBooks/Bible & Gita/Bhagavad-gita-As-It-Is.pdf",
        help="Path to the source Bhagavad Gita PDF.",
    )
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().parents[1] / "assets" / "faith" / "gita_verses.json",
        type=Path,
        help="Output JSON path.",
    )
    args = parser.parse_args()

    verses = build_catalog(Path(args.pdf))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(verses, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {len(verses)} Gita verses to {args.output}")
    if verses:
        print(f"First verse: {verses[0]['reference']}")
        print(f"Last verse: {verses[-1]['reference']}")


if __name__ == "__main__":
    main()
