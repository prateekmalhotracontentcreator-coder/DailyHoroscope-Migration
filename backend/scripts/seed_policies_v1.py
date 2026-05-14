#!/usr/bin/env python3
"""
seed_policies_v1.py
Seeds the MongoDB `policies` collection from the 5 legal .docx files.

Usage:
  python3 backend/scripts/seed_policies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db

Requirements:
  pip install pymongo python-docx
  (python-docx reads .docx without pandoc dependency)

Docx source files expected at paths defined in DOCX_SOURCES below.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx")
    sys.exit(1)

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: pymongo not installed. Run: pip install pymongo")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Source document paths (absolute, outside repo -- user's Documents folder)
# ---------------------------------------------------------------------------
BASE = Path.home() / "Documents" / "Everyday Horoscope"

DOCX_SOURCES = {
    "terms": {
        "path": BASE / "1. TERMS OF SERVICE.docx",
        "title": "Terms of Service",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/terms",
    },
    "privacy": {
        "path": BASE / "2. Privacy Policy.docx",
        "title": "Privacy Policy",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/privacy",
    },
    "subscription-terms": {
        "path": BASE / "3. SUBSCRIPTION TERMS.docx",
        "title": "Subscription Terms",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/subscription-terms",
    },
    "refund-policy": {
        "path": BASE / "4. Refund & Cancellation Policy.docx",
        "title": "Refund & Cancellation Policy",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/refund-policy",
    },
    "cookie-policy": {
        "path": BASE / "5. Cookie Policy.docx",
        "title": "Cookie Policy",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/cookie-policy",
    },
}

# Regex: numbered section heading like "1. INTRO" or "1. Definitions" or "SECTION 1:"
HEADING_RE = re.compile(
    r"^(\d+[\.\)]\s+[A-Z][^\n]{2,}|SECTION\s+\d+[:\.\s][^\n]{2,}|[A-Z][A-Z\s&]{8,})$"
)


def extract_sections(docx_path: Path) -> list[dict]:
    """Parse a .docx file into a list of {heading, content} dicts."""
    doc = Document(str(docx_path))
    sections: list[dict] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    def flush():
        nonlocal current_heading, current_lines
        text = " ".join(current_lines).strip()
        if text or current_heading:
            sections.append({"heading": current_heading or "", "content": text})
        current_heading = None
        current_lines = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style = para.style.name if para.style else ""
        is_heading = (
            "Heading" in style
            or style == "Title"
            or HEADING_RE.match(text)
        )

        if is_heading and len(text) > 3:
            flush()
            current_heading = text
        else:
            current_lines.append(text)

    flush()

    # Remove the document title (first section usually) if it's just the title
    if sections and not sections[0]["content"] and sections[0]["heading"]:
        sections = sections[1:]

    return sections


def build_policy_doc(policy_type: str, meta: dict) -> dict:
    path = meta["path"]
    if not path.exists():
        raise FileNotFoundError(f"Cannot find: {path}")
    sections = extract_sections(path)
    return {
        "type": policy_type,
        "title": meta["title"],
        "effective_date": meta["effective_date"],
        "last_updated": meta["last_updated"],
        "company": meta["company"],
        "url_slug": meta["url_slug"],
        "sections": sections,
        "seeded_at": datetime.now(timezone.utc).isoformat(),
        "version": "v1",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MongoDB policies collection from .docx files")
    parser.add_argument("--mongo-url", required=True, help="MongoDB connection string")
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true", help="Print docs without uploading")
    parser.add_argument("--type", help="Seed only this policy type (e.g. 'terms')")
    args = parser.parse_args()

    targets = {args.type: DOCX_SOURCES[args.type]} if args.type else DOCX_SOURCES

    docs = []
    for policy_type, meta in targets.items():
        print(f"Processing: {policy_type} ({meta['path'].name})")
        try:
            doc = build_policy_doc(policy_type, meta)
            section_count = len(doc["sections"])
            print(f"  -> {section_count} sections extracted")
            docs.append(doc)
        except FileNotFoundError as e:
            print(f"  ERROR: {e}")
            continue

    if args.dry_run:
        import json
        for d in docs:
            preview = {**d, "sections": f"[{len(d['sections'])} sections]"}
            print(json.dumps(preview, indent=2, default=str))
        print(f"\nDry run complete. {len(docs)} documents ready.")
        return

    if not docs:
        print("No documents to upload.")
        return

    client = MongoClient(args.mongo_url)
    col = client[args.db_name]["policies"]

    inserted = 0
    updated = 0
    for doc in docs:
        result = col.update_one(
            {"type": doc["type"]},
            {"$set": doc},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
            print(f"  Inserted: {doc['type']}")
        else:
            updated += 1
            print(f"  Updated: {doc['type']}")

    client.close()
    print(f"\nDone. Inserted: {inserted} | Updated: {updated}")
    print("Verify at: https://everydayhoroscope-api.onrender.com/api/policies/terms")


if __name__ == "__main__":
    main()
