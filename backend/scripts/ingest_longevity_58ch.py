#!/usr/bin/env python3
"""
ingest_longevity_58ch.py
============================================================
Longevity (58 Chapters) -- Full Book KE Ingest
Batch ID : longevity_58ch_v1
Science  : kp_jyotish

Source files:
  Ch04     NLM decode  (escaped markdown JSON)
             /Users/apple/Documents/Knowledge Engine_eBooks/
               Longevity_Ch4_Notebook LM_Decode basis CC Prompt_Updated.md
  Ch05     NLM decode  (escaped markdown JSON)
             Longevity_Ch5_Notebook LM Decode_Updated.md
  Ch06-19  CC decode   (clean JSON in ```json blocks)
             Longevity_CC_Decode/Longevity_Ch06_*_Decoded.md  ...
  Ch20-24  SKIP -- benchmark log only, zero rules extracted
  Ch36-58  Pre-built JSON array (case study rules)
             Longevity_CC_Decode/Longevity_CaseStudies_Ch36-58_Rules.json

Run sequence (mandatory -- never skip steps):
  # Step 1 -- Dry run: extract, validate locally, write JSON files
  python3 backend/scripts/ingest_longevity_58ch.py --dry-run \\
    --save /tmp/longevity_58ch_rules/longevity_all_rules_DRY_RUN.json

  # Step 2 -- Export full MongoDB for dedup comparison
  MONGO_URL="..." python3 backend/scripts/export_mongo_for_dedup.py

  # Step 3 -- Dedup Longevity rules vs entire MongoDB
  python3 backend/ke_dedup_script.py \\
    --folder-a /tmp/longevity_58ch_rules/ \\
    --folder-b /tmp/mongo_existing_rules_dedup/ \\
    --output-report dedup_longevity_vs_mongodb_all.md

  # Step 4 -- Review dedup report; if clean, upload
  python3 backend/scripts/ingest_longevity_58ch.py \\
    --upload /tmp/longevity_58ch_rules/longevity_all_rules_DRY_RUN.json \\
    --mongo-url "$MONGO_URL"

  # Step 5 -- Post-upload structural validation
  python3 backend/scripts/validate_ingest_batch.py \\
    --batch-id longevity_58ch_v1 \\
    --mongo-url "$MONGO_URL" --db-name horoscope_db

  # Step 6 -- Commit output files and updated trackers to git
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── CONSTANTS ─────────────────────────────────────────────────────────────────

BATCH_ID   = "longevity_58ch_v1"
SOURCE_BOOK = "Longevity (58 Chapters)"
SCIENCE_ID  = "kp_jyotish"
BOOK_ID     = "longevity_kp_v1_20260518"
BOOK_TITLE  = "Longevity and Astro System"

EBOOKS_DIR     = Path("/Users/apple/Documents/Knowledge Engine_eBooks")
CC_DECODE_DIR  = EBOOKS_DIR / "Longevity_CC_Decode"

NLM_CH4 = EBOOKS_DIR / "Longevity_Ch4_Notebook LM_Decode basis CC Prompt_Updated.md"
NLM_CH5 = EBOOKS_DIR / "Longevity_Ch5_Notebook LM Decode_Updated.md"

CC_FILES = [
    (6,  "General House Traits",    CC_DECODE_DIR / "Longevity_Ch06_GeneralHouseTraits_Decoded.md"),
    (7,  "Mesha (Aries) Lagna",     CC_DECODE_DIR / "Longevity_Ch07_Aries_Decoded.md"),
    (8,  "Vrishabha (Taurus) Lagna",CC_DECODE_DIR / "Longevity_Ch08_Taurus_Decoded.md"),
    (9,  "Mithuna (Gemini) Lagna",  CC_DECODE_DIR / "Longevity_Ch09_Gemini_Decoded.md"),
    (10, "Karka (Cancer) Lagna",    CC_DECODE_DIR / "Longevity_Ch10_Cancer_Decoded.md"),
    (11, "Simha (Leo) Lagna",       CC_DECODE_DIR / "Longevity_Ch11_Leo_Decoded.md"),
    (12, "Kanya (Virgo) Lagna",     CC_DECODE_DIR / "Longevity_Ch12_Virgo_Decoded.md"),
    (13, "Tula (Libra) Lagna",      CC_DECODE_DIR / "Longevity_Ch13_Libra_Decoded.md"),
    (14, "Vrischika (Scorpio) Lagna", CC_DECODE_DIR / "Longevity_Ch14_Scorpio_Decoded.md"),
    (15, "Dhanu (Sagittarius) Lagna", CC_DECODE_DIR / "Longevity_Ch15_Sagittarius_Decoded.md"),
    (16, "Makara (Capricorn) Lagna",  CC_DECODE_DIR / "Longevity_Ch16_Capricorn_Decoded.md"),
    (17, "Kumbha (Aquarius) Lagna",   CC_DECODE_DIR / "Longevity_Ch17_Aquarius_Decoded.md"),
    (18, "Meena (Pisces) Lagna",      CC_DECODE_DIR / "Longevity_Ch18_Pisces_Decoded.md"),
    (19, "Method of Analysis",        CC_DECODE_DIR / "Longevity_Ch19_MethodOfAnalysis_Decoded.md"),
]

CS_JSON = CC_DECODE_DIR / "Longevity_CaseStudies_Ch36-58_Rules.json"

# ── SCHEMA MAPPINGS ───────────────────────────────────────────────────────────

# Normalise non-standard condition types to registered VALID_CONDITION_TYPES
CONDITION_TYPE_MAP = {
    "kp_sub_lord":          "kp_sublord",          # spelling normalisation
    "kp_badhaka":           "engine_specification", # definitional rule
    "kp_longevity_factor":  "engine_specification", # KP methodology spec
    "kp_significator":      "engine_specification", # foundation signification rule
}

# Map claim_scope (NLM field) → scope (KE canonical field)
SCOPE_MAP = {
    "engine_specification": "engine_specification",
    "natal_trait":          "natal",
    "natal":                "natal",
    "event_timing":         "dasha",
    "dasha":                "dasha",
    "transit":              "transit",
    "natal_lagna":          "natal_lagna",
}

VALID_SCOPES = {
    "natal", "transit", "dasha", "engine_specification", "natal_lagna",
}

VALID_CONDITION_TYPES = {
    "planet_in_house", "planet_in_sign", "planet_in_nakshatra",
    "planet_aspect", "planet_conjunction", "planet_dignity",
    "planet_retrograde", "house_lord_in_house", "yoga",
    "dasha_period", "dasha_planet", "dasha_of_house_lord",
    "transit", "kp_sublord", "composite", "engine_specification",
    "planet_in_house_and_sign", "yoga_combination", "transit_position",
    "aspect_rule", "neechabhanga_rule", "lagna_sign",
    "ashtakavarga_threshold",
}


# ── NLM FILE PARSER ──────────────────────────────────────────────────────────

def parse_nlm_file(path: Path) -> list[dict]:
    """
    Parse a NLM-decode markdown file containing escaped JSON arrays.

    NLM escapes underscores and brackets in the JSON:
        \\_  →  _
        \\[  →  [
        \\]  →  ]

    Also fixes 'maraka_houses': with missing value (invalid JSON produced by NLM
    when the field value is undefined) → coerced to null.

    The file may contain MULTIPLE JSON arrays (e.g. Ch5 has two blocks).
    Arrays are identified by a line whose stripped content is exactly '[' (after
    unescaping), terminated by a line stripped to ']'.
    """
    if not path.exists():
        print(f"  ❌  NLM file not found: {path}", file=sys.stderr)
        return []

    text = path.read_text(encoding="utf-8")

    # Step 1 -- unescape ALL common markdown escapes produced by NLM
    # NLM escapes: \_ \[ \] \. \+ \) \( and others depending on content
    # Order: do NOT replace \\ first (we want literal backslash-char pairs)
    _MARKDOWN_ESCAPABLE = "_[].()+!-*{}#|~`<>"
    for _ch in _MARKDOWN_ESCAPABLE:
        text = text.replace("\\" + _ch, _ch)

    # Step 2 -- fix 'maraka_houses': with no value (NLM bug)
    # Pattern: the key is followed by optional whitespace then a newline
    # Replace with null before the newline (keep the newline for readability)
    text = re.sub(r'"maraka_houses":\s*\n', '"maraka_houses": null\n', text)

    # Step 3 -- extract JSON arrays line by line
    rules: list[dict] = []
    lines = text.split("\n")
    in_array = False
    array_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not in_array:
            if stripped == "[":
                in_array = True
                array_lines = [line]
        else:
            array_lines.append(line)
            if stripped == "]":
                block = "\n".join(array_lines)
                try:
                    parsed = json.loads(block)
                    if isinstance(parsed, list):
                        rules.extend(parsed)
                    else:
                        print(f"  ⚠  Unexpected JSON root type in {path.name} block",
                              file=sys.stderr)
                except json.JSONDecodeError as e:
                    print(f"  ❌  JSON parse error in {path.name}: {e}", file=sys.stderr)
                    # Emit first 10 lines of block for diagnosis
                    for i, bl in enumerate(array_lines[:10]):
                        print(f"       {i:3}: {bl[:100]}", file=sys.stderr)
                in_array = False
                array_lines = []

    if in_array:
        print(f"  ⚠  {path.name}: JSON array not closed -- check file integrity",
              file=sys.stderr)

    return rules


# ── CC DECODE FILE PARSER ────────────────────────────────────────────────────

def parse_cc_file(chapter: int, path: Path) -> list[dict]:
    """
    Extract rules from a CC decode markdown file.
    Rules are in ```json code blocks.
    """
    if not path.exists():
        print(f"  ❌  CC decode file not found: {path}", file=sys.stderr)
        return []

    text = path.read_text(encoding="utf-8")

    # Find all ```json ... ``` blocks
    pattern = r"```json\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    rules: list[dict] = []
    for i, match in enumerate(matches):
        try:
            parsed = json.loads(match)
        except json.JSONDecodeError as e:
            print(f"  ❌  JSON error in Ch{chapter} block {i+1}: {e}", file=sys.stderr)
            continue

        if isinstance(parsed, list):
            rules.extend(parsed)
        elif isinstance(parsed, dict) and parsed.get("rule_id"):
            rules.append(parsed)
        # Skip non-rule blocks (data tables, etc.)

    return rules


# ── CASE STUDY JSON LOADER ───────────────────────────────────────────────────

def load_cs_rules(path: Path) -> list[dict]:
    """Load the Ch36-58 case study rules from the pre-built JSON array."""
    if not path.exists():
        print(f"  ❌  Case study JSON not found: {path}", file=sys.stderr)
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ❌  JSON parse error in {path.name}: {e}", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print(f"  ❌  {path.name}: expected a JSON array at root", file=sys.stderr)
        return []
    return data


# ── SCHEMA TRANSFORMATION ────────────────────────────────────────────────────

def _normalise_condition(condition: dict) -> dict:
    """Normalise condition.type to a registered VALID_CONDITION_TYPE."""
    if not isinstance(condition, dict):
        return {"type": "engine_specification"}
    cond = dict(condition)
    raw_type = cond.get("type", "engine_specification")
    cond["type"] = CONDITION_TYPE_MAP.get(raw_type, raw_type)
    return cond


def transform_nlm_cc_rule(rule: dict, chapter: int, chapter_name: str,
                           now: str) -> dict:
    """
    Transform a raw NLM or CC decode rule to the canonical KE ingest schema.

    Field mapping:
      full_text    → interpretation.detailed
      summary      → interpretation.summary
      claim_scope  → scope  (via SCOPE_MAP)
      condition.type normalised via CONDITION_TYPE_MAP
      source.batch_id overridden to BATCH_ID
    """
    # -- interpretation block ------------------------------------------------
    interp = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary")  or "").strip()

    if not detailed:
        detailed = (rule.get("full_text") or "").strip()
    if not summary:
        summary = (rule.get("summary") or "").strip()
    if not summary:
        summary = detailed[:250] if detailed else ""

    # -- scope ---------------------------------------------------------------
    raw_scope = rule.get("claim_scope") or rule.get("scope") or "natal"
    scope = SCOPE_MAP.get(raw_scope, "natal")

    # -- condition -----------------------------------------------------------
    condition = _normalise_condition(rule.get("condition") or {})

    # -- source block --------------------------------------------------------
    source = dict(rule.get("source") or {})
    source["batch_id"]     = BATCH_ID
    source["book"]         = source.get("book") or BOOK_TITLE
    source["book_id"]      = source.get("book_id") or BOOK_ID
    source["chapter"]      = source.get("chapter") or chapter
    source["chapter_name"] = source.get("chapter_name") or chapter_name

    # -- result block --------------------------------------------------------
    raw_result = rule.get("result") or {}
    result: dict = {}
    for k in ("effect", "severity", "aayu_bucket", "remedy_available",
               "remedy_ref_id"):
        result[k] = raw_result.get(k)
    # Preserve edge_case fields if present
    if raw_result.get("edge_case_zone"):
        result["edge_case_zone"]  = raw_result["edge_case_zone"]
        result["edge_case_gates"] = raw_result.get("edge_case_gates", [])

    return {
        "rule_id":          rule["rule_id"],
        "science_id":       SCIENCE_ID,
        "active":           rule.get("active", True),
        "approval_status":  "pending_human_review",
        "checkable":        rule.get("checkable", False),
        "source":           source,
        "title":            (rule.get("title") or "").strip(),
        "tags":             rule.get("tags") or [],
        "category":         rule.get("category") or "kp_foundation",
        "condition":        condition,
        "claim_axis":       rule.get("claim_axis") or "longevity",
        "scope":            scope,
        "claim_polarity":   rule.get("claim_polarity") or "neutral",
        "timing_bias":      rule.get("timing_bias"),
        "strength_band":    rule.get("strength_band"),
        "result":           result,
        "interpretation": {
            "detailed": detailed,
            "summary":  summary,
        },
        "ingest_batch_id": BATCH_ID,
        "source_book":     SOURCE_BOOK,
        "ingested_at":     now,
    }


def transform_cs_rule(rule: dict, now: str) -> dict:
    """
    Transform a Ch36-58 case study rule to the canonical KE ingest schema.

    These rules already have scope (not claim_scope), interpretation.detailed,
    interpretation.summary.  They lack a nested source dict -- build it here.
    """
    # -- source block (not present in original JSON) --------------------------
    source = {
        "book":         BOOK_TITLE,
        "book_id":      BOOK_ID,
        "chapter":      "ch36-ch58",
        "chapter_name": "Case Studies -- Ch36 to Ch58 (Cross-chart principles)",
        "sloka":        None,
        "batch_id":     BATCH_ID,
        "passage_ref_id": None,
    }

    # -- interpretation (already correct format) ----------------------------
    interp = rule.get("interpretation") or {}
    detailed = (interp.get("detailed") or "").strip()
    summary  = (interp.get("summary")  or "").strip()
    if not summary:
        summary = (rule.get("title") or detailed[:250]).strip()

    # -- condition -----------------------------------------------------------
    condition = _normalise_condition(rule.get("condition") or {})

    # -- scope (already "natal", "dasha", "transit", or "engine_specification")
    scope = rule.get("scope") or "natal"
    if scope not in VALID_SCOPES:
        scope = "natal"

    # -- result --------------------------------------------------------------
    raw_result = rule.get("result") or {}
    result: dict = {
        "effect":           raw_result.get("effect"),
        "severity":         raw_result.get("severity"),
        "aayu_bucket":      raw_result.get("aayu_bucket"),
        "remedy_available": False,
        "remedy_ref_id":    None,
    }
    if raw_result.get("edge_case_zone"):
        result["edge_case_zone"]  = raw_result["edge_case_zone"]
        result["edge_case_gates"] = raw_result.get("edge_case_gates", [])
    if raw_result.get("engine_note"):
        result["engine_note"] = raw_result["engine_note"]

    return {
        "rule_id":          rule["rule_id"],
        "science_id":       SCIENCE_ID,
        "active":           rule.get("active", True),
        "approval_status":  "pending_human_review",
        "checkable":        False,
        "source":           source,
        "title":            (rule.get("title") or "").strip(),
        "tags":             rule.get("tags") or [],
        "category":         rule.get("category") or "kp_longevity_analysis",
        "condition":        condition,
        "claim_axis":       rule.get("claim_axis") or "longevity",
        "scope":            scope,
        "claim_polarity":   rule.get("claim_polarity") or "neutral",
        "timing_bias":      rule.get("timing_bias"),
        "strength_band":    rule.get("strength_band"),
        "result":           result,
        "interpretation": {
            "detailed": detailed,
            "summary":  summary,
        },
        "ingest_batch_id":        BATCH_ID,
        "source_book":            SOURCE_BOOK,
        "ingested_at":            now,
        "cross_chapter_evidence": rule.get("cross_chapter_evidence") or [],
    }


# ── ALTERNATE SCHEMA NORMALIZER (Ch12 / Ch13) ────────────────────────────────

def _is_alternate_schema(rule: dict) -> bool:
    """Detect Ch12/Ch13 rules that use trigger/outcome instead of title/condition."""
    return "trigger" in rule and "title" not in rule


def _normalize_alternate_schema(rule: dict, chapter: int,
                                 chapter_name: str) -> dict:
    """
    Normalise Ch12/Ch13 rules (trigger + outcome format) to the standard
    NLM/CC schema so they can flow through transform_nlm_cc_rule() cleanly.

    Mapping:
      trigger.planet + trigger.house_position → condition dict
      outcome.qualifier                       → title + interpretation.summary
      full_text                               → interpretation.detailed
      outcome.aayu_bucket + severity          → result block
    """
    trigger = rule.get("trigger") or {}
    outcome = rule.get("outcome") or {}
    src     = rule.get("source") or {}
    result  = rule.get("result") or {}

    qualifier = (outcome.get("qualifier") or "").strip()
    full_text = (rule.get("full_text") or "").strip()
    notes     = (rule.get("notes") or "").strip()

    # Title: prefer outcome.qualifier (most descriptive), fallback to full_text
    title = qualifier[:120] if qualifier else (
        full_text[:120] if full_text else f"Rule {rule.get('rule_id', '')}")

    # Condition type from trigger content
    planet    = trigger.get("planet")
    house_pos = trigger.get("house_position")
    star_lord = trigger.get("star_lord")

    if star_lord:
        ctype = "kp_sublord"
    elif planet and house_pos is not None:
        ctype = "planet_in_house"
    else:
        ctype = "engine_specification"

    condition: dict = {"type": ctype}
    if planet:
        condition["planet"] = planet
    if house_pos is not None:
        condition["house"] = house_pos
    if star_lord:
        condition["star_lord"] = star_lord
    if rule.get("lagna_modality"):
        condition["lagna_modality"] = rule["lagna_modality"]
    if rule.get("badhaka_house"):
        condition["badhaka_house"] = rule["badhaka_house"]

    # Source block (preserve existing page/section, upgrade to full schema)
    source = {
        "book":          BOOK_TITLE,
        "book_id":       BOOK_ID,
        "chapter":       src.get("chapter") or chapter,
        "chapter_name":  src.get("chapter_name") or chapter_name,
        "sloka":         src.get("sloka"),
        "batch_id":      BATCH_ID,
        "passage_ref_id": src.get("passage_ref_id"),
    }

    # claim_scope: lagna-specific rules are natal
    claim_scope = "natal_trait"

    # Result block
    normalised_result = {
        "effect":          outcome.get("longevity_direction"),
        "severity":        rule.get("severity"),
        "aayu_bucket":     outcome.get("aayu_bucket"),
        "remedy_available": False,
        "remedy_ref_id":   result.get("remedy_ref_id"),
    }

    # Interpretation
    summary  = qualifier[:300] if qualifier else (notes[:300] if notes else full_text[:300])
    detailed = full_text if full_text else qualifier

    return {
        "rule_id":          rule["rule_id"],
        "science_id":       SCIENCE_ID,
        "active":           True,
        "approval_status":  "pending_human_review",
        "checkable":        False,
        "source":           source,
        "title":            title,
        "summary":          summary,     # mapped by transform_nlm_cc_rule
        "full_text":        detailed,    # mapped by transform_nlm_cc_rule
        "tags":             rule.get("tags") or [],
        "category":         "kp_longevity_lagna_rules",
        "condition":        condition,
        "claim_axis":       "longevity",
        "claim_scope":      claim_scope,
        "claim_polarity":   rule.get("claim_polarity") or "neutral",
        "timing_bias":      None,
        "strength_band":    rule.get("strength_band"),
        "result":           normalised_result,
        # Extra metadata preserved for future reference
        "lagna_applicability": rule.get("lagna_applicability") or [],
        "badhaka_house":       rule.get("badhaka_house"),
        "notes":               notes,
    }


# ── LOCAL STRUCTURAL VALIDATION ──────────────────────────────────────────────

def validate_rule_local(rule: dict, idx: int) -> list[str]:
    """
    Lightweight structural check mirroring the key gates in validate_rules.py.
    Returns a list of issue strings (empty = pass).
    """
    issues: list[str] = []
    rid = rule.get("rule_id") or f"[rule #{idx}]"

    if not rule.get("rule_id"):
        issues.append(f"{rid}: missing rule_id")

    if rule.get("science_id") != SCIENCE_ID:
        issues.append(f"{rid}: science_id={rule.get('science_id')} (expected {SCIENCE_ID})")

    if rule.get("approval_status") != "pending_human_review":
        issues.append(f"{rid}: approval_status={rule.get('approval_status')}")

    if rule.get("ingest_batch_id") != BATCH_ID:
        issues.append(f"{rid}: ingest_batch_id={rule.get('ingest_batch_id')}")

    src = rule.get("source") or {}
    if not isinstance(src, dict):
        issues.append(f"{rid}: source is not a dict")
    elif src.get("batch_id") != BATCH_ID:
        issues.append(f"{rid}: source.batch_id={src.get('batch_id')} (expected {BATCH_ID})")

    interp = rule.get("interpretation") or {}
    if not (interp.get("detailed") or "").strip():
        issues.append(f"{rid}: interpretation.detailed is empty")
    if not (interp.get("summary") or "").strip():
        issues.append(f"{rid}: interpretation.summary is empty")

    cond = rule.get("condition") or {}
    if not isinstance(cond, dict) or not cond:
        issues.append(f"{rid}: condition is missing or empty")
    else:
        ctype = cond.get("type", "")
        if ctype not in VALID_CONDITION_TYPES:
            issues.append(f"{rid}: condition.type='{ctype}' not in VALID_CONDITION_TYPES")

    scope = rule.get("scope", "")
    if scope not in VALID_SCOPES:
        issues.append(f"{rid}: scope='{scope}' not in VALID_SCOPES")

    if not (rule.get("title") or "").strip():
        issues.append(f"{rid}: title is empty")

    return issues


# ── BUILD ALL RULES ──────────────────────────────────────────────────────────

def build_all_rules() -> tuple[list[dict], dict[str, int], list[str]]:
    """
    Load, parse, and transform all Longevity 58Ch rules.

    Returns:
        all_rules      -- flat list of transformed rule dicts
        chapter_counts -- {label: count}
        all_issues     -- list of validation issue strings
    """
    now = datetime.now(timezone.utc).isoformat()
    all_rules: list[dict] = []
    chapter_counts: dict[str, int] = {}
    all_issues: list[str] = []
    seen_ids: dict[str, str] = {}

    def _add_rules(raw_rules: list[dict], chapter: int, chapter_name: str,
                   is_cs: bool = False) -> int:
        """Transform, validate, dedup and append rules. Returns count added."""
        label = f"Ch{chapter}" if not is_cs else "Ch36-58 CS"
        added = 0
        for rule in raw_rules:
            if not isinstance(rule, dict):
                continue
            rid = rule.get("rule_id")
            if not rid:
                print(f"  ⚠  {label}: rule without rule_id -- skipped")
                continue
            if rid in seen_ids:
                print(f"  ⚠  Duplicate rule_id {rid} "
                      f"(first in {seen_ids[rid]}) -- skipped")
                continue
            seen_ids[rid] = label

            if is_cs:
                transformed = transform_cs_rule(rule, now)
            else:
                # Detect and normalise Ch12/Ch13 alternate schema before transform
                if _is_alternate_schema(rule):
                    rule = _normalize_alternate_schema(rule, chapter, chapter_name)
                transformed = transform_nlm_cc_rule(rule, chapter,
                                                    chapter_name, now)

            issues = validate_rule_local(transformed, len(all_rules))
            all_issues.extend(issues)

            all_rules.append(transformed)
            added += 1
        return added

    # ── Ch4 (NLM) ─────────────────────────────────────────────────────────────
    print(f"\n  Parsing Ch04 NLM decode...")
    raw = parse_nlm_file(NLM_CH4)
    n = _add_rules(raw, 4, "Some Basic Fundamental Rules")
    chapter_counts["Ch04 (NLM)"] = n
    print(f"    → {n} rules loaded")

    # ── Ch5 (NLM) ─────────────────────────────────────────────────────────────
    print(f"  Parsing Ch05 NLM decode...")
    raw = parse_nlm_file(NLM_CH5)
    n = _add_rules(raw, 5, "Basics of Longevity")
    chapter_counts["Ch05 (NLM)"] = n
    print(f"    → {n} rules loaded")

    # ── Ch6-19 (CC decode) ───────────────────────────────────────────────────
    for ch_num, ch_name, cc_path in CC_FILES:
        label = f"Ch{ch_num:02d}"
        print(f"  Parsing {label} CC decode...")
        raw = parse_cc_file(ch_num, cc_path)
        n = _add_rules(raw, ch_num, ch_name)
        chapter_counts[f"{label} (CC)"] = n
        print(f"    → {n} rules loaded")

    # ── Ch20-24 SKIP (benchmark only, zero rules) ─────────────────────────────
    chapter_counts["Ch20-24 (SKIP)"] = 0
    print(f"  Ch20-24: SKIPPED -- benchmark log only, zero rules extracted")

    # ── Ch36-58 case studies ─────────────────────────────────────────────────
    print(f"  Parsing Ch36-58 case study JSON...")
    raw = load_cs_rules(CS_JSON)
    n = _add_rules(raw, 36, "Case Studies Ch36-Ch58", is_cs=True)
    chapter_counts["Ch36-58 CS"] = n
    print(f"    → {n} rules loaded")

    return all_rules, chapter_counts, all_issues


# ── WRITE PER-CHAPTER FILES (for dedup) ──────────────────────────────────────

def write_chapter_files(all_rules: list[dict], output_dir: Path) -> None:
    """
    Write individual per-chapter JSON files to output_dir for dedup comparison.
    ke_dedup_script.py expects one JSON file per source chapter in the folder.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Group by source.chapter
    chapters: dict = {}
    for rule in all_rules:
        src = rule.get("source") or {}
        ch  = str(src.get("chapter", "unknown"))
        chapters.setdefault(ch, []).append(rule)

    # Also write the consolidated file (dedup script will pick up all *.json)
    for ch, rules in chapters.items():
        fname = f"longevity_ch{ch}_rules.json"
        fpath = output_dir / fname
        fpath.write_text(
            json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )


# ── MAIN ──────────────────────────────────────────────────────────────────────

CHAPTER_LABELS = {
    "Ch04 (NLM)":  "Ch4  Some Basic Fundamental Rules",
    "Ch05 (NLM)":  "Ch5  Basics of Longevity",
    "Ch06 (CC)":   "Ch6  General House Traits",
    "Ch07 (CC)":   "Ch7  Mesha (Aries) Lagna",
    "Ch08 (CC)":   "Ch8  Vrishabha (Taurus) Lagna",
    "Ch09 (CC)":   "Ch9  Mithuna (Gemini) Lagna",
    "Ch10 (CC)":   "Ch10 Karka (Cancer) Lagna",
    "Ch11 (CC)":   "Ch11 Simha (Leo) Lagna",
    "Ch12 (CC)":   "Ch12 Kanya (Virgo) Lagna",
    "Ch13 (CC)":   "Ch13 Tula (Libra) Lagna",
    "Ch14 (CC)":   "Ch14 Vrischika (Scorpio) Lagna",
    "Ch15 (CC)":   "Ch15 Dhanu (Sagittarius) Lagna",
    "Ch16 (CC)":   "Ch16 Makara (Capricorn) Lagna",
    "Ch17 (CC)":   "Ch17 Kumbha (Aquarius) Lagna",
    "Ch18 (CC)":   "Ch18 Meena (Pisces) Lagna",
    "Ch19 (CC)":   "Ch19 Method of Analysis",
    "Ch20-24 (SKIP)": "Ch20-24  Balarishta Benchmarks (ZERO RULES)",
    "Ch36-58 CS":  "Ch36-58  Case Studies (21 cross-chart rules)",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Longevity 58Ch KE Ingest -- batch: longevity_58ch_v1"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Extract + validate only. No DB write. Use with --save."
    )
    parser.add_argument(
        "--save", metavar="PATH",
        help="Save extracted rules to JSON file (use with --dry-run)"
    )
    parser.add_argument(
        "--upload", metavar="PATH",
        help="Upload rules from a saved JSON file to MongoDB"
    )
    parser.add_argument("--mongo-url",  default=os.getenv("MONGO_URL"))
    parser.add_argument("--db-name",    default="horoscope_db")
    args = parser.parse_args()

    if not args.dry_run and not args.upload:
        parser.error("Specify --dry-run [--save PATH] or --upload PATH")

    print("\n" + "=" * 70)
    print(f"LONGEVITY 58Ch INGEST  |  batch: {BATCH_ID}")
    print("=" * 70)

    # ── DRY RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        print("\nPhase 1: Extracting and transforming rules...\n")
        all_rules, chapter_counts, all_issues = build_all_rules()

        print(f"\n{'─' * 70}")
        print(f"{'Chapter':<28} {'Rules':>6}")
        print(f"{'─' * 70}")
        for key in CHAPTER_LABELS:
            label = CHAPTER_LABELS[key]
            count = chapter_counts.get(key, 0)
            flag  = "  ⚠  NO RULES" if count == 0 and key != "Ch20-24 (SKIP)" else ""
            skip  = "  (intentional skip)" if key == "Ch20-24 (SKIP)" else ""
            print(f"  {label:<28} {count:>4}{flag}{skip}")
        print(f"{'─' * 70}")
        print(f"  {'TOTAL':<30} {len(all_rules):>4}")

        print(f"\nPhase 2: Local structural validation...")
        if all_issues:
            print(f"\n  ⚠  {len(all_issues)} issue(s) found:")
            for issue in all_issues[:30]:
                print(f"     {issue}")
            if len(all_issues) > 30:
                print(f"     ... and {len(all_issues) - 30} more")
        else:
            print(f"  ✅  All {len(all_rules)} rules passed structural validation (Issues: 0)")

        # Spot-check first and last rule
        if all_rules:
            for label, r in [("First rule", all_rules[0]),
                              ("Last rule",  all_rules[-1])]:
                print(f"\n{label}:")
                print(f"  rule_id          : {r.get('rule_id')}")
                print(f"  science_id       : {r.get('science_id')}")
                print(f"  approval_status  : {r.get('approval_status')}")
                print(f"  ingest_batch_id  : {r.get('ingest_batch_id')}")
                print(f"  source.batch_id  : {(r.get('source') or {}).get('batch_id')}")
                print(f"  source.chapter   : {(r.get('source') or {}).get('chapter')}")
                print(f"  scope            : {r.get('scope')}")
                print(f"  interpretation.summary  : "
                      f"{(r.get('interpretation') or {}).get('summary', '')[:80]}...")

        if args.save and all_rules:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)

            # Write consolidated file
            save_path.write_text(
                json.dumps(all_rules, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8"
            )
            print(f"\n✅ Saved {len(all_rules)} rules → {save_path}")

            # Write per-chapter files for dedup
            chapter_dir = save_path.parent
            write_chapter_files(all_rules, chapter_dir)
            print(f"✅ Per-chapter files written to {chapter_dir}/")
            print(f"   (dedup: pass --folder-a {chapter_dir}/ to ke_dedup_script.py)")

        elif args.save and not all_rules:
            print("\n⚠  No rules extracted -- nothing saved.")

        print(f"\n[DRY RUN COMPLETE]  No MongoDB writes made.")
        print(f"Issue count: {len(all_issues)}")
        if all_issues:
            print(f"⚠  Fix issues before uploading.")
        else:
            print(f"Next: Run dedup (Steps 2-3), then:")
            print(f"  python3 backend/scripts/ingest_longevity_58ch.py \\")
            print(f"    --upload {args.save or 'PATH'} --mongo-url \"$MONGO_URL\"")
        return

    # ── UPLOAD ────────────────────────────────────────────────────────────────
    if args.upload:
        if not args.mongo_url:
            parser.error("--mongo-url is required for upload (or set MONGO_URL env var)")

        upload_path = Path(args.upload)
        if not upload_path.exists():
            print(f"\n❌ File not found: {upload_path}")
            sys.exit(1)

        all_rules = json.loads(upload_path.read_text(encoding="utf-8"))
        if not isinstance(all_rules, list):
            print(f"❌ Expected JSON array at root of {upload_path}")
            sys.exit(1)

        print(f"\nLoaded {len(all_rules)} rules from {upload_path}")
        print(f"Target: {args.db_name}.interpretation_rules")
        print(f"Batch : {BATCH_ID}\n")

        try:
            from pymongo import MongoClient
            client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)
            col = client[args.db_name]["interpretation_rules"]
            # Connection test
            client.admin.command("ping")
            print("✅ MongoDB connection OK")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            sys.exit(1)

        inserted = 0
        updated  = 0
        errors:  list[str] = []

        print(f"Upserting {len(all_rules)} rules...")

        for rule in all_rules:
            rid = rule.get("rule_id")
            if not rid:
                continue
            try:
                result = col.replace_one({"rule_id": rid}, rule, upsert=True)
                if result.upserted_id:
                    inserted += 1
                elif result.modified_count:
                    updated += 1
            except Exception as e:
                errors.append(f"{rid}: {e}")

        print(f"\n  Inserted : {inserted}")
        print(f"  Updated  : {updated}")
        print(f"  Errors   : {len(errors)}")

        if errors:
            print(f"\n⚠  First 10 errors:")
            for err in errors[:10]:
                print(f"  {err}")

        # Write import_batches log
        try:
            log_entry = {
                "batch_id":       BATCH_ID,
                "book":           SOURCE_BOOK,
                "science_id":     SCIENCE_ID,
                "source_file":    str(upload_path),
                "rules_inserted": inserted,
                "rules_updated":  updated,
                "total_rules":    inserted + updated,
                "errors":         len(errors),
                "uploaded_at":    datetime.now(timezone.utc).isoformat(),
                "chapters":       [4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                   14, 15, 16, 17, 18, 19, "36-58"],
            }
            client[args.db_name]["import_batches"].replace_one(
                {"batch_id": BATCH_ID},
                log_entry,
                upsert=True
            )
            print(f"\n✅ import_batches log updated for batch {BATCH_ID}")
        except Exception as e:
            print(f"⚠  Could not write import_batches log: {e}")

        client.close()

        print(f"\n{'═' * 70}")
        print(f"UPLOAD COMPLETE")
        print(f"{'═' * 70}")
        print(f"\nNEXT STEP -- Post-upload validation:")
        print(f"  python3 backend/scripts/validate_ingest_batch.py \\")
        print(f"    --batch-id {BATCH_ID} \\")
        print(f"    --mongo-url \"$MONGO_URL\" --db-name {args.db_name}")
        print(f"\nAfter validation: triage flagged rules using three-bucket method:")
        print(f"  A (truncation artifact) → auto_approved")
        print(f"  B (validator doctrinal error) → PHR + validator_error:true")
        print(f"  C (genuine issue) → stay flagged, escalate TT/GAI")


if __name__ == "__main__":
    main()
