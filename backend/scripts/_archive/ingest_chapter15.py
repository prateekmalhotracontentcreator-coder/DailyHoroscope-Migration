#!/usr/bin/env python3
"""
Chapter 15 — Planets in Different Houses: Option B ingest.

For every (planet, house) block this script produces:
  1. One  planet_in_house      rule  — full verbatim text (main rule)
  2. N×   planet_in_house_in_sign rules — one per zodiac sign mentioned
  3. Up to 4 special-state rules — exalted / debilitated / own_sign / enemy_sign

The sign and special-state rules act as cross-book placeholders: when Phase 1
books (BPHS, Phaladeepika, Lal Kitab) are ingested later they add their own
version of "Sun in Cancer in 1H" to the same condition slot.  MongoDB lets
multiple rules share the same (planet, house, sign) combination — the query
layer union-merges them by confidence weight.

Usage:
  python3 scripts/ingest_chapter15.py \\
    --rtf "~/Documents/Knowledge Engine_eBooks/Chapter 15.rtf" \\
    --mongo-url "mongodb+srv://..." \\
    --db-name EverydayHoroscope \\
    [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pymongo import MongoClient

# ─── Constants ───────────────────────────────────────────────────────────────

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
           "Saturn", "Rahu", "Ketu"]

HOUSE_WORDS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4,
    "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
    "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12,
}

# Sign lookup: lower-case name → (canonical name, house number, 3-letter code)
SIGN_NAME_MAP: dict[str, tuple[str, int, str]] = {
    "aries":       ("Aries",       1,  "ARI"),
    "taurus":      ("Taurus",      2,  "TAU"),
    "gemini":      ("Gemini",      3,  "GEM"),
    "cancer":      ("Cancer",      4,  "CAN"),
    "leo":         ("Leo",         5,  "LEO"),
    "virgo":       ("Virgo",       6,  "VIR"),
    "libra":       ("Libra",       7,  "LIB"),
    "scorpio":     ("Scorpio",     8,  "SCO"),
    "sagittarius": ("Sagittarius", 9,  "SAG"),
    "capricorn":   ("Capricorn",  10,  "CAP"),
    "aquarius":    ("Aquarius",   11,  "AQU"),
    "pisces":      ("Pisces",     12,  "PIS"),
}

# Sign number (1-12) → same tuple
SIGN_NUM_MAP: dict[int, tuple[str, int, str]] = {
    info[1]: info for info in SIGN_NAME_MAP.values()
}

# Special states: key → (rule-id suffix, condition.special_state value)
SPECIAL_STATES: dict[str, tuple[str, str]] = {
    "exalted":    ("EXA", "exalted"),
    "debilitated": ("DEB", "debilitated"),
    "own_sign":   ("OWN", "own_sign"),
    "enemy_sign": ("ENE", "enemy_sign"),
}

BOOK     = "A Text Book of Astrology"
CHAPTER  = "Chapter 15 — Planets in Different Houses: Prediction"
SCIENCE  = "vedic_astrology"
BATCH_ID = f"a-text-book-ch15-v2-{datetime.now(timezone.utc).strftime('%Y%m%d')}"


# ─── RTF stripper ────────────────────────────────────────────────────────────

def strip_rtf(rtf_text: str) -> str:
    """Convert RTF to plain text (handles Mac TextEdit RTF output)."""
    # Remove RTF header + font/colour tables up to \viewkind0
    text = re.sub(r"^\{\\rtf1.*?\\viewkind0\s*", "", rtf_text, flags=re.DOTALL)
    # Page breaks → double newlines
    text = re.sub(r"\\page\s*", "\n\n", text)
    # Colour switches → nothing
    text = re.sub(r"\\cf\d+\s*", "", text)
    # Paragraph style directives → newline
    text = re.sub(r"\\pard[^\n\\]*", "\n", text)
    # Remaining control words with optional numeric param
    text = re.sub(r"\\[a-zA-Z]+(-?\d+)?[ ]?", "", text)
    # RTF braces
    text = text.replace("{", "").replace("}", "")
    # RTF line continuation
    text = text.replace("\\\n", "\n")
    # Collapse runs of blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ─── Structure parser ─────────────────────────────────────────────────────────

def parse_chapter15(plain_text: str) -> list[dict]:
    """
    Returns a list of dicts:
      { planet, house, text, female_text }
    """
    planet_pat = re.compile(
        r"^(" + "|".join(PLANETS) + r")$", re.IGNORECASE | re.MULTILINE
    )
    house_pat = re.compile(
        r"^(" + "|".join(HOUSE_WORDS) + r")\s+house$", re.IGNORECASE | re.MULTILINE
    )
    female_pat = re.compile(r"in\s+female\s+horoscope\s*:?", re.IGNORECASE)

    rules: list[dict] = []
    current_planet: str = ""
    current_house: int  = 0
    current_lines: list[str] = []

    def flush() -> None:
        if not current_planet or not current_house or not current_lines:
            return
        full_text = " ".join(current_lines).strip()
        female_match = female_pat.search(full_text)
        if female_match:
            main_text   = full_text[: female_match.start()].strip()
            female_text = full_text[female_match.end() :].strip()
        else:
            main_text   = full_text
            female_text = ""
        rules.append({
            "planet":      current_planet,
            "house":       current_house,
            "text":        main_text,
            "female_text": female_text,
        })

    for line in plain_text.splitlines():
        line = line.strip()
        if not line:
            continue
        pm = planet_pat.match(line)
        if pm:
            flush()
            current_planet = pm.group(1).capitalize()
            current_house  = 0
            current_lines  = []
            continue
        hm = house_pat.match(line)
        if hm:
            flush()
            current_house = HOUSE_WORDS[hm.group(1).lower()]
            current_lines = []
            continue
        if current_planet and current_house:
            current_lines.append(line)

    flush()
    return rules


# ─── Sign / special-state extractor ──────────────────────────────────────────

# Sentence splitter (handles abbreviations inside words too)
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def split_sentences(text: str) -> list[str]:
    """Split text into rough sentences for condition scanning."""
    parts = _SENT_SPLIT.split(text)
    # Further split on '. If ' boundaries (common in this book)
    sentences: list[str] = []
    for part in parts:
        # split on '. If' or '. if'
        sub = re.split(r"\.\s+(?=[Ii]f\b)", part)
        sentences.extend(s.strip() for s in sub if s.strip())
    return sentences


def extract_named_signs(text: str) -> set[str]:
    """Return set of sign lower-case keys explicitly named in text."""
    found = set()
    lower = text.lower()
    for key in SIGN_NAME_MAP:
        # match the sign name as a word boundary
        if re.search(r"\b" + key + r"\b", lower):
            found.add(key)
    return found


def extract_numbered_signs(text: str) -> set[int]:
    """
    Detect patterns like 'signs 1, 4, 5, 8' or 'sign 7, 10 and 11'.
    Returns set of sign numbers.
    """
    found: set[int] = []
    # Pattern: "sign(s) <nums>" where nums is a comma/space/and-separated list
    pat = re.compile(
        r"\bsigns?\s+([\d][0-9\s,]+(?:and\s+\d+)?)",
        re.IGNORECASE,
    )
    for m in pat.finditer(text):
        nums_str = m.group(1)
        nums = re.findall(r"\d+", nums_str)
        for n in nums:
            val = int(n)
            if 1 <= val <= 12:
                found.append(val)
    return set(found)


def extract_special_states(text: str) -> dict[str, str]:
    """
    Returns {state_key: extracted_sentence} for each special state found.
    State keys: exalted, debilitated, own_sign, enemy_sign
    """
    lower_text = text.lower()
    states: dict[str, str] = {}

    # Collect sentences that contain each state marker
    sentences = split_sentences(text)

    def find_sentences_for(pattern: str) -> str:
        pat = re.compile(pattern, re.IGNORECASE)
        matched = [s for s in sentences if pat.search(s)]
        return " ".join(matched).strip()

    if re.search(r"\bexalted\b", lower_text):
        states["exalted"] = find_sentences_for(r"\bexalted\b")

    if re.search(r"\bdebilitated\b", lower_text):
        states["debilitated"] = find_sentences_for(r"\bdebilitated\b")

    if re.search(r"\bown\s+sign\b", lower_text):
        states["own_sign"] = find_sentences_for(r"\bown\s+sign\b")

    if re.search(r"\benemy(?:'s)?\s+sign\b", lower_text):
        states["enemy_sign"] = find_sentences_for(r"\benemy(?:'s)?\s+sign\b")

    return states


def collect_sign_sentences(text: str, sign_key: str) -> str:
    """Return sentences that explicitly mention the named sign."""
    sign_name = SIGN_NAME_MAP[sign_key][0]
    pat = re.compile(r"\b" + re.escape(sign_name) + r"\b", re.IGNORECASE)
    sentences = split_sentences(text)
    matched = [s for s in sentences if pat.search(s)]
    return " ".join(matched).strip()


# ─── Rule builders ────────────────────────────────────────────────────────────

def _source_block(detailed: str) -> dict:
    return {
        "primary":           BOOK,
        "chapter":           CHAPTER,
        "author_voice":      "classical",
        "secondary_sources": [],
        "batch_id":          BATCH_ID,
    }


def _passage(text: str) -> dict:
    return {
        "text":             text,
        "source":           BOOK,
        "chapter":          CHAPTER,
        "word_count":       len(text.split()),
        "voice_tone":       "classical",
        "confidence":       "HIGH",
        "paraphrase_notes": "verbatim — no paraphrase applied",
    }


def build_main_rule(entry: dict, seq: int) -> dict:
    """Build the planet_in_house base rule (full verbatim text)."""
    planet  = entry["planet"]
    house   = entry["house"]
    text    = entry["text"]
    f_text  = entry["female_text"]

    first_sentence = re.split(r"(?<=[.!?])\s+", text)[0][:250] if text else ""
    detailed = text
    if f_text:
        detailed += f"\n\nIn female horoscope: {f_text}"

    planet_short = planet[:3].upper()
    rule_id = f"R-ATEXTB-{planet_short}-{house}H-V-{seq:03d}"

    return {
        "rule_id":          rule_id,
        "version":          1,
        "science_id":       SCIENCE,
        "approval_status":  "pending_review",
        "life_domain":      "general",
        "claim_axis":       "general_trend",
        "claim_scope":      "tendency",
        "claim_polarity":   "neutral",
        "timing_bias":      "none",
        "strength_band":    "medium",
        "subject_scope":    "self",
        "condition": {
            "type":           "planet_in_house",
            "planet":         planet,
            "house":          house,
            "sign":           "",
            "sub_conditions": [],
            "operator":       "and",
        },
        "interpretation": {
            "summary":             first_sentence,
            "detailed":            detailed,
            "full_text_passages":  [_passage(detailed)],
            "positive_aspects":    [],
            "challenging_aspects": [],
            "remedies":            [],
        },
        "categories":    ["general"],
        "source":        _source_block(detailed),
        "modifiers":     [],
        "conflicts_with": [],
        "weight":        1.0,
        "tags":          ["verbatim", "planet_in_house", "chapter15"],
        "active":        True,
    }


def build_sign_rule(entry: dict, sign_key: str, seq: int, sub_seq: int) -> dict:
    """Build a planet_in_house_in_sign placeholder rule for a named zodiac sign."""
    planet = entry["planet"]
    house  = entry["house"]

    canon_name, sign_num, sign_code = SIGN_NAME_MAP[sign_key]
    # Extract sentences from main text + female text that mention this sign
    combined = entry["text"]
    if entry["female_text"]:
        combined += " " + entry["female_text"]
    detailed = collect_sign_sentences(combined, sign_key)
    if not detailed:
        detailed = f"[Placeholder] {planet} in house {house} in {canon_name}. " \
                   f"Refer to cross-book enrichment from BPHS / Lal Kitab."

    planet_short = planet[:3].upper()
    rule_id = f"R-ATEXTB-{planet_short}-{house}H-{sign_code}-V-{seq:03d}-{sub_seq:02d}"

    return {
        "rule_id":          rule_id,
        "version":          1,
        "science_id":       SCIENCE,
        "approval_status":  "pending_review",
        "life_domain":      "general",
        "claim_axis":       "general_trend",
        "claim_scope":      "tendency",
        "claim_polarity":   "neutral",
        "timing_bias":      "none",
        "strength_band":    "medium",
        "subject_scope":    "self",
        "condition": {
            "type":           "planet_in_house_in_sign",
            "planet":         planet,
            "house":          house,
            "sign":           canon_name,
            "sign_number":    sign_num,
            "sub_conditions": [],
            "operator":       "and",
        },
        "interpretation": {
            "summary":             detailed[:250],
            "detailed":            detailed,
            "full_text_passages":  [_passage(detailed)],
            "positive_aspects":    [],
            "challenging_aspects": [],
            "remedies":            [],
        },
        "categories":    ["general"],
        "source":        _source_block(detailed),
        "modifiers":     [],
        "conflicts_with": [],
        "weight":        1.0,
        "tags":          ["verbatim", "planet_in_house_in_sign", "sign_variant", "chapter15"],
        "active":        True,
    }


def build_special_rule(entry: dict, state_key: str, state_text: str,
                       seq: int, sub_seq: int) -> dict:
    """Build a planet_in_house_special rule for exalted/debilitated/own/enemy."""
    planet = entry["planet"]
    house  = entry["house"]

    suffix_code, state_value = SPECIAL_STATES[state_key]
    # Include female text if it mentions the same state
    combined = entry["text"]
    if entry["female_text"]:
        combined += " " + entry["female_text"]
    # Re-extract sentences for state from combined text
    state_sentences = extract_special_states(combined).get(state_key, state_text)
    detailed = state_sentences if state_sentences else state_text

    planet_short = planet[:3].upper()
    rule_id = (
        f"R-ATEXTB-{planet_short}-{house}H-{suffix_code}-V-{seq:03d}-{sub_seq:02d}"
    )

    return {
        "rule_id":          rule_id,
        "version":          1,
        "science_id":       SCIENCE,
        "approval_status":  "pending_review",
        "life_domain":      "general",
        "claim_axis":       "general_trend",
        "claim_scope":      "tendency",
        "claim_polarity":   "neutral",
        "timing_bias":      "none",
        "strength_band":    "medium",
        "subject_scope":    "self",
        "condition": {
            "type":           "planet_in_house_special",
            "planet":         planet,
            "house":          house,
            "sign":           "",
            "special_state":  state_value,
            "sub_conditions": [],
            "operator":       "and",
        },
        "interpretation": {
            "summary":             detailed[:250],
            "detailed":            detailed,
            "full_text_passages":  [_passage(detailed)],
            "positive_aspects":    [],
            "challenging_aspects": [],
            "remedies":            [],
        },
        "categories":    ["general"],
        "source":        _source_block(detailed),
        "modifiers":     [],
        "conflicts_with": [],
        "weight":        1.0,
        "tags":          ["verbatim", "special_state", state_value, "chapter15"],
        "active":        True,
    }


# ─── Main expansion ──────────────────────────────────────────────────────────

def expand_entry(entry: dict, seq: int) -> list[dict]:
    """
    For one (planet, house) block return:
      [main_rule, *sign_rules, *special_state_rules]
    """
    docs: list[dict] = []

    # 1. Main verbatim rule
    docs.append(build_main_rule(entry, seq))

    sub = 1  # sub-sequence counter for derived rules

    # 2. Named signs from both main text and female text
    combined = entry["text"] + " " + entry["female_text"]
    named_signs = extract_named_signs(combined)

    # 3. Numbered signs — treat as named signs
    numbered_signs = extract_numbered_signs(combined)
    for n in numbered_signs:
        if n in SIGN_NUM_MAP:
            # add to named_signs set via reverse lookup
            sign_tuple = SIGN_NUM_MAP[n]
            # find the key
            for k, v in SIGN_NAME_MAP.items():
                if v[1] == n:
                    named_signs.add(k)
                    break

    for sign_key in sorted(named_signs):
        docs.append(build_sign_rule(entry, sign_key, seq, sub))
        sub += 1

    # 4. Special states
    special = extract_special_states(combined)
    for state_key, state_text in sorted(special.items()):
        docs.append(build_special_rule(entry, state_key, state_text, seq, sub))
        sub += 1

    return docs


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtf",       required=True, help="Path to Chapter 15.rtf")
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   required=True)
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    rtf_path = Path(args.rtf).expanduser()
    if not rtf_path.exists():
        sys.exit(f"RTF file not found: {rtf_path}")

    # 1. Read + strip RTF
    raw   = rtf_path.read_text(encoding="utf-8", errors="replace")
    plain = strip_rtf(raw)

    # 2. Parse structure
    entries = parse_chapter15(plain)
    print(f"\nParsed {len(entries)} planet-house blocks from RTF\n")

    # 3. Expand into full rule set (Option B)
    all_rules: list[dict] = []
    for i, entry in enumerate(entries, start=1):
        all_rules.extend(expand_entry(entry, i))

    # 4. Summary table
    main_rules  = [r for r in all_rules if r["condition"]["type"] == "planet_in_house"]
    sign_rules  = [r for r in all_rules if r["condition"]["type"] == "planet_in_house_in_sign"]
    state_rules = [r for r in all_rules if r["condition"]["type"] == "planet_in_house_special"]

    print(f"{'PLANET':<12} {'HOUSE':>5}  {'WORDS':>5}  {'SIGNS':>5}  {'STATES':>6}  SUMMARY")
    print("-" * 90)
    for entry in entries:
        p, h = entry["planet"], entry["house"]
        related_signs  = [r for r in sign_rules  if r["condition"]["planet"] == p
                                                  and r["condition"]["house"]  == h]
        related_states = [r for r in state_rules if r["condition"]["planet"] == p
                                                  and r["condition"]["house"]  == h]
        words   = len(entry["text"].split())
        summary = " ".join(entry["text"].split())[:60]
        sign_names = ", ".join(r["condition"]["sign"] for r in related_signs)
        print(f"{p:<12} {h:>5}  {words:>5}  {len(related_signs):>5}  {len(related_states):>6}"
              f"  {summary}...")
        if sign_names:
            print(f"{'':>12}        signs: {sign_names}")

    print(f"\n{'=' * 60}")
    print(f"Base rules (planet_in_house)         : {len(main_rules)}")
    print(f"Sign variant rules (in_sign)         : {len(sign_rules)}")
    print(f"Special state rules (exalted/deb/own): {len(state_rules)}")
    print(f"TOTAL rules                          : {len(all_rules)}")

    # 5. Check for missing base combos
    missing = set()
    found   = {(r["condition"]["planet"], r["condition"]["house"]) for r in main_rules}
    for p in PLANETS:
        for h in range(1, 13):
            if (p, h) not in found:
                missing.add((p, h))
    if missing:
        print(f"\nMissing planet-house combos ({len(missing)}):")
        for p, h in sorted(missing, key=lambda x: (PLANETS.index(x[0]), x[1])):
            print(f"  {p} in house {h}")
    else:
        print("\nAll 108 planet-house combos present ✅")

    if args.dry_run:
        print(f"\n[DRY RUN] — nothing written to MongoDB.")
        print(f"Run without --dry-run to insert {len(all_rules)} rules.")

        # Detailed sign preview for first 5 entries
        print(f"\n--- Sample sign/state rules (first 3 base entries) ---")
        shown = 0
        for r in all_rules:
            if r["condition"]["type"] != "planet_in_house" and shown < 15:
                cond = r["condition"]
                ctype = cond["type"].replace("planet_in_house_", "")
                label = cond.get("sign") or cond.get("special_state", "")
                print(f"  [{ctype:>15}] {cond['planet']:>8} H{cond['house']:<2}  "
                      f"{label:<15}  {r['rule_id']}")
                shown += 1
        return

    # 6. Insert into MongoDB
    client = MongoClient(args.mongo_url)
    db     = client[args.db_name]
    col    = db["interpretation_rules"]

    existing = col.count_documents({"source.batch_id": BATCH_ID})
    if existing:
        print(f"\n⚠  Batch '{BATCH_ID}' already has {existing} rules in MongoDB.")
        print("   Delete those docs manually then re-run without --dry-run.")
        client.close()
        return

    result = col.insert_many(all_rules, ordered=False)
    print(f"\n✅  Inserted {len(result.inserted_ids)} rules into MongoDB")
    print(f"   batch_id : {BATCH_ID}")
    print(f"   Main     : {len(main_rules)}  |  Sign variants: {len(sign_rules)}"
          f"  |  Special states: {len(state_rules)}")
    print(f"\n   Filter by tag 'sign_variant' or 'special_state' to review sub-rules.")
    print(f"   These condition slots are ready for cross-book enrichment from")
    print(f"   BPHS, Phaladeepika, and Lal Kitab (Phase 1 books).")
    client.close()


if __name__ == "__main__":
    main()
