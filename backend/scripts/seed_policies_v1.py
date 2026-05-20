#!/usr/bin/env python3
"""
seed_policies_v1.py
Seeds the MongoDB `policies` collection from the 5 legal .docx files.

Usage:
  python3 backend/scripts/seed_policies_v1.py --mongo-url "$MONGO_URL" --db-name horoscope_db
  python3 backend/scripts/seed_policies_v1.py --source-dir "$HOME/Documents/Everyday Horoscope-Documents" --dry-run

Requirements:
  pip install pymongo python-docx
  (python-docx reads .docx without pandoc dependency)

Docx source files are discovered from `--source-dir` or the default source
directories defined below.
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
DEFAULT_SOURCE_DIRS = [
    Path.home() / "Documents" / "Everyday Horoscope",
    Path.home() / "Documents" / "Everyday Horoscope-Documents",
]
CONTACT_EMAIL = "prateekmalhotra.contentcreator@gmail.com"

DOCX_SOURCES = {
    "terms": {
        "filename": "1. TERMS OF SERVICE.docx",
        "title": "Terms of Service",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/terms",
    },
    "privacy": {
        "filename": "2. Privacy Policy.docx",
        "title": "Privacy Policy",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/privacy",
    },
    "subscription-terms": {
        "filename": "3. SUBSCRIPTION TERMS.docx",
        "title": "Subscription Terms",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/subscription-terms",
    },
    "refund-policy": {
        "filename": "4. Refund & Cancellation Policy.docx",
        "title": "Refund & Cancellation Policy",
        "effective_date": "18 February 2026",
        "last_updated": "18 February 2026",
        "company": "SkyHound Studios",
        "url_slug": "/refund-policy",
    },
    "cookie-policy": {
        "filename": "5. Cookie Policy.docx",
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


def resolve_source_dir(explicit_dir: str | None) -> Path:
    if explicit_dir:
        source_dir = Path(explicit_dir).expanduser()
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        return source_dir

    for candidate in DEFAULT_SOURCE_DIRS:
        if candidate.exists():
            return candidate

    searched = ", ".join(str(path) for path in DEFAULT_SOURCE_DIRS)
    raise FileNotFoundError(f"Could not find a policy source directory. Searched: {searched}")


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


def upsert_section(sections: list[dict], heading: str, content: str) -> None:
    for section in sections:
        if section.get("heading", "").strip().lower() == heading.strip().lower():
            section["content"] = content
            return
    sections.append({"heading": heading, "content": content})


def retitle_section(sections: list[dict], old_heading: str, new_heading: str, content: str) -> None:
    for section in sections:
        if section.get("heading", "").strip().lower() == old_heading.strip().lower():
            section["heading"] = new_heading
            section["content"] = content
            return
    sections.append({"heading": new_heading, "content": content})


def apply_compliance_overrides(policy_type: str, sections: list[dict]) -> list[dict]:
    if policy_type == "privacy":
        upsert_section(
            sections,
            "2.5 Transaction & Payment Data",
            "Payments are processed through Razorpay, our payment processing partner. We do not store full credit or debit card numbers, CVV values, UPI PINs, or payment authentication credentials on Everyday Horoscope systems. We may retain limited transaction metadata such as order identifiers, payment status, report type, subscription plan, and billing timestamps for accounting, fraud prevention, customer support, and legal compliance.",
        )
        upsert_section(
            sections,
            "7. DATA SHARING & THIRD-PARTY PROCESSORS",
            "We may share personal data only with trusted service providers who help us operate the Services, including Razorpay for payment processing, Google Analytics for aggregated website and app usage analytics, cloud hosting providers, customer support tools, and legal or regulatory authorities where required. We do not sell personal data to third parties. All processors are expected to handle personal data only for authorized business purposes and under appropriate contractual or legal safeguards.",
        )
        upsert_section(
            sections,
            "12. COOKIES & TRACKING TECHNOLOGIES",
            "We use essential cookies to keep users signed in and maintain platform security, analytics cookies including Google Analytics to understand aggregate usage trends, and preference cookies to remember user choices. Users may control cookies through browser settings and can review more detail in our Cookie Policy.",
        )
        upsert_section(
            sections,
            "13. CHILDREN'S PRIVACY",
            "Our Services are not directed to children under the age of 13, and we do not knowingly collect personal data from children under 13. Certain premium or account-based Services may require users to be 18 years of age or older under our Terms of Service. If we learn that a child under 13 has provided personal data, we will take reasonable steps to delete it.",
        )

    elif policy_type == "refund-policy":
        upsert_section(
            sections,
            "4. DIGITAL REPORTS & PERSONALIZED SERVICES",
            "Personalized reports are generated using User-provided birth details and other inputs. Individual reports, downloadable files, and personalized digital services are non-refundable once the report has been generated, delivered, accessed, or downloaded. No refund shall be granted where incorrect or incomplete data is provided by the User, and consultations are non-refundable once initiated, regardless of duration or perceived quality.",
        )
        retitle_section(
            sections,
            "5. TWO-HOUR CANCELLATION WINDOW (PRE-SERVICE)",
            "5. SEVEN-DAY REFUND ELIGIBILITY FOR UNUSED DIGITAL SERVICES",
            "Refund requests for eligible digital purchases may be considered if the User contacts the Company within 7 days of purchase and the purchased service, subscription benefit, or report has not been accessed, generated, initiated, or downloaded. Requests submitted after 7 days, or after the underlying service has been used, are generally not eligible for refund except where required by applicable law.",
        )
        upsert_section(
            sections,
            "6. SUBSCRIPTIONS",
            "Users may cancel subscriptions at any time from their account settings or by contacting support. Cancellation stops future renewals only, and access continues until the end of the current billing period. Refunds for subscription purchases may be considered within 7 days of purchase only where subscription benefits have not been accessed or used. Monthly and annual plans renew automatically unless cancelled before the next renewal date.",
        )
        upsert_section(
            sections,
            "9. REFUND PROCESSING",
            f"Approved refunds are processed to the original payment method within 5 to 7 business days after review. To request a refund, Users must email {CONTACT_EMAIL} with their order ID, payment receipt, registered email address, and a short description of the issue. Banking timelines and payment gateway processing may affect the final credit date.",
        )

    elif policy_type == "cookie-policy":
        upsert_section(
            sections,
            "3.2 Performance and Analytics Cookies",
            "These cookies help us understand how Users interact with the Services, including feature usage patterns, navigation behavior, technical performance, and aggregate traffic trends. We may use Google Analytics or similar analytics tools to measure aggregated usage and improve the reliability and usability of the platform.",
        )
        upsert_section(
            sections,
            "4. THIRD-PARTY COOKIES",
            "Trusted service providers may place cookies or related tracking technologies for limited business purposes. This may include Google Analytics for aggregated traffic reporting and Razorpay or similar payment providers when a checkout flow is initiated. Users should review the privacy and cookie policies of third-party providers because their practices are governed by their own terms.",
        )
        upsert_section(
            sections,
            "5. USER CONTROL AND COOKIE CHOICES",
            "Users may manage cookie preferences through browser configuration settings, device privacy controls, and any in-app consent or preference management tools we make available. Users who want to limit Google Analytics tracking can adjust browser settings, block analytics cookies, or use Google's browser opt-out tools where available. Disabling certain cookies may affect platform functionality, reduce personalization quality, or limit availability of certain features.",
        )

    return sections


def build_policy_doc(policy_type: str, meta: dict, source_dir: Path) -> dict:
    path = source_dir / meta["filename"]
    if not path.exists():
        raise FileNotFoundError(f"Cannot find: {path}")
    sections = apply_compliance_overrides(policy_type, extract_sections(path))
    return {
        "type": policy_type,
        "title": meta["title"],
        "effective_date": meta["effective_date"],
        "last_updated": meta["last_updated"],
        "company": meta["company"],
        "url_slug": meta["url_slug"],
        "sections": sections,
        "seeded_at": datetime.now(timezone.utc).isoformat(),
        "version": "v1.1-compliance-refresh",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MongoDB policies collection from .docx files")
    parser.add_argument("--mongo-url", required=True, help="MongoDB connection string")
    parser.add_argument("--db-name", default="horoscope_db")
    parser.add_argument("--dry-run", action="store_true", help="Print docs without uploading")
    parser.add_argument("--type", help="Seed only this policy type (e.g. 'terms')")
    parser.add_argument("--source-dir", help="Directory containing the 5 legal .docx files")
    args = parser.parse_args()
    source_dir = resolve_source_dir(args.source_dir)

    targets = {args.type: DOCX_SOURCES[args.type]} if args.type else DOCX_SOURCES

    docs = []
    for policy_type, meta in targets.items():
        print(f"Processing: {policy_type} ({meta['filename']})")
        try:
            doc = build_policy_doc(policy_type, meta, source_dir)
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
