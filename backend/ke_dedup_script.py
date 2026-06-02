#!/usr/bin/env python3
from __future__ import annotations

"""Cross-text deduplication and contradiction detection for KE decode folders.

Inline test cases:
1. Two identical rules from different texts -> `identical_claim`
2. Same condition, same polarity, different phrasing -> `same_principle_different_phrasing`
3. Same condition, opposite polarity, score >= 0.25, non-null condition fields -> `contradicts`

Contradiction detection guards (added 2026-06-01):
- CONTRADICTION_MIN_SCORE: minimum TF-IDF similarity score for a contradiction to be
  reported. Rules with the same condition_signature but near-zero text similarity are
  structural false positives caused by null/generic condition fields (e.g. yoga rules,
  general house judgement rules). Default 0.25 -- well above the 0.13 max observed for
  confirmed false contradictions, low enough to catch genuine textual conflicts.
- has_meaningful_condition(): at least one of planet/house/sign/planets_involved/
  houses_involved must be non-null for a rule to participate in contradiction detection.
  All-null conditions produce identical signatures across unrelated rules and generate
  false contradiction clusters.

Positional conflict detection (added 2026-06-02):
- detect_positional_conflicts(): finds rules that share the same (planet × house) or
  (planet × sign) condition key but claim a different result. Two sub-types:
    * positional_polarity_conflict -- explicit positive vs negative polarity on the same
      planet×house combination. High-confidence flag.
    * positional_alternate_result -- same planet×house, TF-IDF similarity below
      POSITIONAL_RESULT_SIMILARITY_FLOOR (0.40). Same condition, result texts are
      dissimilar -- likely different outcome. Flag for human review.
  Bypasses the CONTRADICTION_MIN_SCORE floor intentionally: positional matches do not
  need textual similarity to be meaningful (Sun in 1st from BPHS vs Sun in 1st from
  Phaladeepika will share planet+house but use very different prose).

Semantic pass (Phase 2 -- NOT YET IMPLEMENTED):
  See .claude/ke/KE_DEDUP_SEMANTIC_PASS_SPEC.md for the planned embedding-based layer
  that catches same-concept-different-wording duplicates across engine_specification
  (methodology/system) rules (e.g. "9 planets", "27 nakshatras", aspect rules). These
  rules have all-null condition fields and TF-IDF cannot catch them.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_THRESHOLD = 0.82
CONTRADICTION_MIN_SCORE = 0.25       # minimum similarity for a genuine full-condition contradiction
POSITIONAL_RESULT_SIMILARITY_FLOOR = 0.40  # below this = alternate_result on same planet×house key
VALID_POLARITIES = {"positive", "negative", "mixed", "neutral"}
SIMILARITY_RELATIONSHIPS = {
    "identical_claim",
    "near_identical",
    "same_principle_different_phrasing",
    "partial_overlap",
}
CONTRADICTION_RELATIONSHIPS = {"contradicts", "partial_contradiction"}
POSITIONAL_CONFLICT_RELATIONSHIPS = {
    "positional_polarity_conflict",
    "positional_alternate_result",
}


@dataclass
class RuleRecord:
    rule_id: str
    rule: dict[str, Any]
    source_path: Path
    source_index: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-text KE dedup and contradiction detector.")
    parser.add_argument("--folder-a", required=True)
    parser.add_argument("--folder-b", required=True)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--output-report", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-files", action="store_true")
    parser.add_argument(
        "--skip-positional",
        action="store_true",
        help="Skip positional conflict detection (planet×house / planet×sign cross-result check).",
    )
    return parser.parse_args()


def lower_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    return text or None


def normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple(sorted((str(key), normalize_value(subvalue)) for key, subvalue in value.items()))
    if isinstance(value, (list, tuple)):
        normalized_items = [normalize_value(item) for item in value]
        return tuple(sorted(normalized_items, key=repr))
    if isinstance(value, set):
        return tuple(sorted((normalize_value(item) for item in value), key=repr))
    return value


def build_compare_text(rule: dict[str, Any]) -> str:
    condition = rule.get("condition") or {}
    parts = [
        condition.get("type", ""),
        condition.get("planet", ""),
        condition.get("house", ""),
        condition.get("sign", ""),
        rule.get("full_text", ""),
    ]
    return " ".join(str(part).strip() for part in parts if str(part).strip())


def load_rules_from_folder(folder_path: Path, folder_label: str) -> tuple[list[RuleRecord], dict[Path, list[dict[str, Any]]]]:
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")
    if not folder_path.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder_path}")

    records: list[RuleRecord] = []
    file_payloads: dict[Path, list[dict[str, Any]]] = {}
    rule_files = sorted(folder_path.glob("*_Rules*.json"))

    if not rule_files:
        print(f"[warn] No *_Rules*.json files found in {folder_path}", file=sys.stderr)
        return records, file_payloads

    for file_path in rule_files:
        try:
            raw = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"[warn] Skipping {file_path}: JSON parse error ({exc})", file=sys.stderr)
            continue

        # Handle both list-format and dict-format rule files.
        # List-format: [...] -- used by Phase 1 yoga chapters, Ch32, Ch33
        # Dict-format: {"rules": [...], ...} -- used by Thread A/C/D decode sessions
        if isinstance(raw, list):
            payload = raw
        elif isinstance(raw, dict) and isinstance(raw.get("rules"), list):
            payload = raw["rules"]
        else:
            print(f"[warn] Skipping {file_path}: unrecognised JSON structure "
                  f"(expected list or dict with 'rules' key)", file=sys.stderr)
            continue

        file_payloads[file_path] = payload
        for index, rule in enumerate(payload):
            if not isinstance(rule, dict):
                print(f"[warn] Skipping non-object rule in {file_path} at index {index}", file=sys.stderr)
                continue
            rule_id = rule.get("rule_id")
            if not rule_id:
                print(f"[warn] Skipping rule without rule_id in {file_path} at index {index}", file=sys.stderr)
                continue
            record = RuleRecord(rule_id=str(rule_id), rule=rule, source_path=file_path, source_index=index)
            records.append(record)

    print(f"Loaded {len(records)} valid rules from {folder_label}: {folder_path}")
    return records, file_payloads


def similarity_relationship(score: float, same_condition: bool, threshold: float) -> str | None:
    if score >= 0.95:
        return "identical_claim"
    if score >= 0.90:
        return "near_identical"
    if score >= threshold:
        return "same_principle_different_phrasing" if same_condition else "partial_overlap"
    return None


def condition_signature(rule: dict[str, Any]) -> Any:
    return normalize_value(rule.get("condition") or {})


def has_meaningful_condition(rule: dict[str, Any]) -> bool:
    """Return True if the rule has at least one specific, non-null condition field.

    Rules with all-null condition fields (e.g. yoga rules with only condition.type set,
    general house judgement rules, engine_specification rules) share identical condition
    signatures despite being about completely different subjects. These must be excluded
    from contradiction detection to prevent false contradiction clusters.
    """
    condition = rule.get("condition") or {}
    meaningful_fields = (
        "planet",
        "house",
        "sign",
        "planets_involved",
        "houses_involved",
        "signs_involved",
        "yoga_name",
    )
    return any(
        condition.get(field) not in (None, "", [], {})
        for field in meaningful_fields
    )


def condition_type_matches(rule_a: dict[str, Any], rule_b: dict[str, Any]) -> bool:
    condition_a = rule_a.get("condition") or {}
    condition_b = rule_b.get("condition") or {}
    if lower_or_none(condition_a.get("type")) != lower_or_none(condition_b.get("type")):
        return False

    for key in ("planet", "house", "sign"):
        value_a = condition_a.get(key)
        value_b = condition_b.get(key)
        normalized_a = normalize_value(value_a)
        normalized_b = normalize_value(value_b)
        if (value_a is not None or value_b is not None) and normalized_a != normalized_b:
            return False

    return condition_signature(rule_a) == condition_signature(rule_b)


def polarity_relation(rule_a: dict[str, Any], rule_b: dict[str, Any]) -> str | None:
    polarity_a = lower_or_none(rule_a.get("claim_polarity"))
    polarity_b = lower_or_none(rule_b.get("claim_polarity"))
    if polarity_a not in VALID_POLARITIES or polarity_b not in VALID_POLARITIES:
        return None
    if polarity_a == polarity_b:
        return None
    if {polarity_a, polarity_b} == {"positive", "negative"}:
        return "contradicts"
    if "mixed" in {polarity_a, polarity_b} and ({polarity_a, polarity_b} & {"positive", "negative"}):
        return "partial_contradiction"
    return None


def shared_condition(rule_a: dict[str, Any], rule_b: dict[str, Any]) -> dict[str, Any]:
    condition_a = rule_a.get("condition") or {}
    condition_b = rule_b.get("condition") or {}
    shared: dict[str, Any] = {}
    for key in sorted(set(condition_a) | set(condition_b)):
        value_a = condition_a.get(key)
        value_b = condition_b.get(key)
        if value_a is None or value_b is None:
            continue
        if normalize_value(value_a) == normalize_value(value_b):
            shared[key] = value_a
    return shared


def build_similarity_entry(rule_id: str, score: float, relationship: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "similarity_score": round(float(score), 4),
        "relationship": relationship,
    }


def build_similarity_report_entry(
    rule_a: RuleRecord,
    rule_b: RuleRecord,
    score: float,
    relationship: str,
) -> dict[str, Any]:
    return {
        "rule_a_id": rule_a.rule_id,
        "rule_b_id": rule_b.rule_id,
        "similarity_score": round(float(score), 4),
        "relationship": relationship,
        "rule_a_full_text": str(rule_a.rule.get("full_text", "")).strip(),
        "rule_b_full_text": str(rule_b.rule.get("full_text", "")).strip(),
    }


def build_contradiction_report_entry(
    rule_a: RuleRecord,
    rule_b: RuleRecord,
    score: float,
    relationship: str,
) -> dict[str, Any]:
    return {
        "rule_a_id": rule_a.rule_id,
        "rule_b_id": rule_b.rule_id,
        "similarity_score": round(float(score), 4),
        "relationship": relationship,
        "rule_a_polarity": lower_or_none(rule_a.rule.get("claim_polarity")),
        "rule_b_polarity": lower_or_none(rule_b.rule.get("claim_polarity")),
        "shared_condition": shared_condition(rule_a.rule, rule_b.rule),
        "rule_a_full_text": str(rule_a.rule.get("full_text", "")).strip(),
        "rule_b_full_text": str(rule_b.rule.get("full_text", "")).strip(),
    }


def ensure_cross_text_matches(rule: dict[str, Any]) -> list[dict[str, Any]]:
    matches = rule.get("cross_text_matches")
    if not isinstance(matches, list):
        matches = []
    return matches


def upsert_cross_text_matches(
    existing_matches: list[dict[str, Any]],
    fresh_matches: list[dict[str, Any]],
    counterpart_rule_ids: set[str],
) -> list[dict[str, Any]]:
    preserved_matches = [entry for entry in existing_matches if entry.get("rule_id") not in counterpart_rule_ids]
    fresh_map = {entry["rule_id"]: entry for entry in fresh_matches}
    merged = preserved_matches + list(fresh_map.values())
    merged.sort(key=lambda entry: (entry.get("relationship", ""), -float(entry.get("similarity_score", 0.0)), entry.get("rule_id", "")))
    return merged


def compute_similarity_data(
    rules_a: list[RuleRecord],
    rules_b: list[RuleRecord],
    threshold: float,
) -> tuple[list[tuple[RuleRecord, RuleRecord, float, str]], dict[tuple[str, str], float]]:
    if not rules_a or not rules_b:
        return [], {}

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:  # pragma: no cover
        print("scikit-learn is required. Install with `pip install scikit-learn>=1.3.0`.", file=sys.stderr)
        raise SystemExit(1)

    all_texts = [build_compare_text(record.rule) for record in rules_a + rules_b]
    if not all_texts:
        return [], {}

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    matrix_a = tfidf_matrix[: len(rules_a)]
    matrix_b = tfidf_matrix[len(rules_a) :]
    scores = cosine_similarity(matrix_a, matrix_b)

    similarity_pairs: list[tuple[RuleRecord, RuleRecord, float, str]] = []
    score_lookup: dict[tuple[str, str], float] = {}
    for index_a, rule_a in enumerate(rules_a):
        for index_b, rule_b in enumerate(rules_b):
            score = float(scores[index_a, index_b])
            score_lookup[(rule_a.rule_id, rule_b.rule_id)] = score
            relationship = similarity_relationship(score, condition_signature(rule_a.rule) == condition_signature(rule_b.rule), threshold)
            if not relationship:
                continue
            if relationship in CONTRADICTION_RELATIONSHIPS:
                continue
            similarity_pairs.append((rule_a, rule_b, score, relationship))

    return similarity_pairs, score_lookup


def compute_contradiction_pairs(
    rules_a: list[RuleRecord],
    rules_b: list[RuleRecord],
    score_lookup: dict[tuple[str, str], float],
) -> list[tuple[RuleRecord, RuleRecord, float, str]]:
    # Guard 1: exclude rules with no meaningful condition fields.
    # All-null conditions produce identical signatures across unrelated rules,
    # creating false contradiction clusters (confirmed 2026-06-01 -- 47 false
    # contradictions from Ch11/Ch33 yoga/general-principle rules with null conditions).
    eligible_a = [r for r in rules_a if has_meaningful_condition(r.rule)]
    eligible_b = [r for r in rules_b if has_meaningful_condition(r.rule)]

    skipped_a = len(rules_a) - len(eligible_a)
    skipped_b = len(rules_b) - len(eligible_b)
    if skipped_a or skipped_b:
        print(
            f"[contradiction guard] Skipped {skipped_a} rules from A and "
            f"{skipped_b} rules from B with no meaningful condition fields.",
            file=sys.stderr,
        )

    grouped_a: dict[Any, list[RuleRecord]] = {}
    grouped_b: dict[Any, list[RuleRecord]] = {}
    for record in eligible_a:
        grouped_a.setdefault(condition_signature(record.rule), []).append(record)
    for record in eligible_b:
        grouped_b.setdefault(condition_signature(record.rule), []).append(record)

    contradiction_pairs: list[tuple[RuleRecord, RuleRecord, float, str]] = []
    for signature, group_a in grouped_a.items():
        group_b = grouped_b.get(signature)
        if not group_b:
            continue
        for rule_a in group_a:
            for rule_b in group_b:
                relationship = polarity_relation(rule_a.rule, rule_b.rule)
                if not relationship:
                    continue
                score = score_lookup.get((rule_a.rule_id, rule_b.rule_id), 0.0)
                # Guard 2: minimum similarity floor.
                # Genuine contradictions require some textual overlap. Near-zero scores
                # indicate unrelated rules whose condition signatures collided on null fields.
                if score < CONTRADICTION_MIN_SCORE:
                    continue
                contradiction_pairs.append((rule_a, rule_b, score, relationship))

    return contradiction_pairs


def extract_positional_key(rule: dict[str, Any]) -> tuple[str, str, str] | None:
    """Return a positional conflict key for this rule, or None if no planet×house/sign condition.

    Key shape:
        ("ph", planet, house)  -- planet-in-house combination
        ("ps", planet, sign)   -- planet-in-sign combination

    Planet is mandatory -- house-only or sign-only conditions produce too many collisions
    to be useful as a conflict key.  planet×house is preferred; planet×sign is returned
    when house is absent.  Both planet and the spatial field must be non-null strings.
    """
    condition = rule.get("condition") or {}
    planet = lower_or_none(condition.get("planet"))
    if planet is None:
        return None
    house = lower_or_none(condition.get("house"))
    if house is not None:
        return ("ph", planet, house)
    sign = lower_or_none(condition.get("sign"))
    if sign is not None:
        return ("ps", planet, sign)
    return None


def build_positional_conflict_entry(
    rule_a: RuleRecord,
    rule_b: RuleRecord,
    score: float,
    conflict_type: str,
    positional_key: tuple[str, str, str],
) -> dict[str, Any]:
    """Build a report entry for a positional conflict (planet×house or planet×sign)."""
    key_type, planet, house_or_sign = positional_key
    dimension = "house" if key_type == "ph" else "sign"
    return {
        "rule_a_id": rule_a.rule_id,
        "rule_b_id": rule_b.rule_id,
        "similarity_score": round(float(score), 4),
        "relationship": conflict_type,
        "positional_key": f"{planet} in {dimension} {house_or_sign}",
        "rule_a_polarity": lower_or_none(rule_a.rule.get("claim_polarity")),
        "rule_b_polarity": lower_or_none(rule_b.rule.get("claim_polarity")),
        "rule_a_full_text": str(rule_a.rule.get("full_text", "")).strip(),
        "rule_b_full_text": str(rule_b.rule.get("full_text", "")).strip(),
    }


def detect_positional_conflicts(
    rules_a: list[RuleRecord],
    rules_b: list[RuleRecord],
    score_lookup: dict[tuple[str, str], float],
) -> list[tuple[RuleRecord, RuleRecord, float, str, tuple[str, str, str]]]:
    """Find rules from A and B that share a planet×house or planet×sign key but differ in result.

    Two sub-types (both bypass CONTRADICTION_MIN_SCORE intentionally -- positional matches
    are keyed on explicit condition fields, not textual similarity):

    positional_polarity_conflict:
        Both rules have a valid claim_polarity AND the polarity relation is "contradicts"
        (one positive, one negative).  High-confidence flag -- the two texts explicitly
        disagree on whether the placement is beneficial or harmful.

    positional_alternate_result:
        Same planet×house/sign key, TF-IDF score < POSITIONAL_RESULT_SIMILARITY_FLOOR.
        The rules share the same condition but their result texts are dissimilar -- likely
        a different claimed outcome.  Flag for human review; may or may not be a genuine
        conflict (could be two complementary aspects of the same placement).

    Returns list of (rule_a, rule_b, score, conflict_type, positional_key) tuples.
    """
    grouped_a: dict[tuple[str, str, str], list[RuleRecord]] = {}
    grouped_b: dict[tuple[str, str, str], list[RuleRecord]] = {}

    for record in rules_a:
        key = extract_positional_key(record.rule)
        if key is not None:
            grouped_a.setdefault(key, []).append(record)

    for record in rules_b:
        key = extract_positional_key(record.rule)
        if key is not None:
            grouped_b.setdefault(key, []).append(record)

    positional_keys_a = len(grouped_a)
    positional_keys_b = len(grouped_b)
    shared_keys = set(grouped_a) & set(grouped_b)
    print(
        f"[positional] Keyed {positional_keys_a} planet×position groups from A, "
        f"{positional_keys_b} from B -- {len(shared_keys)} shared keys.",
        file=sys.stderr,
    )

    conflicts: list[tuple[RuleRecord, RuleRecord, float, str, tuple[str, str, str]]] = []

    for key in sorted(shared_keys):
        group_a = grouped_a[key]
        group_b = grouped_b[key]
        for rule_a in group_a:
            for rule_b in group_b:
                score = score_lookup.get((rule_a.rule_id, rule_b.rule_id), 0.0)
                pol_rel = polarity_relation(rule_a.rule, rule_b.rule)
                if pol_rel == "contradicts":
                    conflicts.append((rule_a, rule_b, score, "positional_polarity_conflict", key))
                elif score < POSITIONAL_RESULT_SIMILARITY_FLOOR:
                    conflicts.append((rule_a, rule_b, score, "positional_alternate_result", key))

    return conflicts


def write_back_files(
    file_payloads: dict[Path, list[dict[str, Any]]],
    updates_by_rule_id: dict[str, list[dict[str, Any]]],
    rule_ids_a: set[str],
    rule_ids_b: set[str],
) -> None:
    for file_path, payload in file_payloads.items():
        dirty = False
        for rule in payload:
            rule_id = str(rule.get("rule_id") or "")
            if not rule_id:
                continue
            if rule_id in rule_ids_a:
                counterpart_rule_ids = rule_ids_b
            elif rule_id in rule_ids_b:
                counterpart_rule_ids = rule_ids_a
            else:
                continue
            existing_matches = ensure_cross_text_matches(rule)
            fresh_matches = updates_by_rule_id.get(rule_id, [])
            merged_matches = upsert_cross_text_matches(existing_matches, fresh_matches, counterpart_rule_ids)
            if merged_matches or "cross_text_matches" in rule or fresh_matches or counterpart_rule_ids:
                rule["cross_text_matches"] = merged_matches
                dirty = True
        if dirty:
            file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def print_relation(prefix: str, entry: dict[str, Any]) -> None:
    print(
        f"{prefix} {entry['rule_a_id']} <-> {entry['rule_b_id']} "
        f"[{entry['relationship']}] score={entry['similarity_score']:.4f}"
    )


def main() -> None:
    args = parse_args()
    folder_a = Path(args.folder_a).expanduser().resolve()
    folder_b = Path(args.folder_b).expanduser().resolve()
    output_report_path = Path(args.output_report).expanduser().resolve()

    if not folder_a.exists():
        print(f"Folder does not exist: {folder_a}", file=sys.stderr)
        raise SystemExit(1)
    if not folder_b.exists():
        print(f"Folder does not exist: {folder_b}", file=sys.stderr)
        raise SystemExit(1)
    if args.dry_run and args.update_files:
        print("[warn] Both --dry-run and --update-files were supplied; dry-run takes precedence.", file=sys.stderr)

    rules_a, file_payloads_a = load_rules_from_folder(folder_a, "folder-a")
    rules_b, file_payloads_b = load_rules_from_folder(folder_b, "folder-b")
    rule_ids_a = {record.rule_id for record in rules_a}
    rule_ids_b = {record.rule_id for record in rules_b}

    similarity_pairs, score_lookup = compute_similarity_data(rules_a, rules_b, args.threshold)
    contradiction_pairs = compute_contradiction_pairs(rules_a, rules_b, score_lookup)

    if args.skip_positional:
        positional_conflict_pairs: list[tuple[RuleRecord, RuleRecord, float, str, tuple[str, str, str]]] = []
    else:
        positional_conflict_pairs = detect_positional_conflicts(rules_a, rules_b, score_lookup)
    positional_conflict_pairs.sort(key=lambda item: (item[4], item[0].rule_id, item[1].rule_id))

    contradiction_key_set = {(pair[0].rule_id, pair[1].rule_id) for pair in contradiction_pairs}
    similarity_pairs = [
        pair
        for pair in similarity_pairs
        if (pair[0].rule_id, pair[1].rule_id) not in contradiction_key_set
    ]

    similarity_pairs.sort(key=lambda item: (-item[2], item[0].rule_id, item[1].rule_id))
    contradiction_pairs.sort(key=lambda item: (item[0].rule_id, item[1].rule_id))

    print(f"Rules in A: {len(rules_a)}")
    print(f"Rules in B: {len(rules_b)}")
    print(f"Pairs evaluated: {len(rules_a) * len(rules_b)}")
    print(f"Similarity matches: {len(similarity_pairs)}")
    print(f"Contradiction pairs: {len(contradiction_pairs)}")
    print(f"Positional conflicts: {len(positional_conflict_pairs)}")

    similarity_reports = []
    contradiction_reports = []
    positional_conflict_reports = []
    updates_by_rule_id: dict[str, list[dict[str, Any]]] = {}

    for rule_a, rule_b, score, relationship in similarity_pairs:
        report_entry = build_similarity_report_entry(rule_a, rule_b, score, relationship)
        similarity_reports.append(report_entry)
        print_relation("MATCH", report_entry)

        entry_a = build_similarity_entry(rule_b.rule_id, score, relationship)
        entry_b = build_similarity_entry(rule_a.rule_id, score, relationship)
        updates_by_rule_id.setdefault(rule_a.rule_id, []).append(entry_a)
        updates_by_rule_id.setdefault(rule_b.rule_id, []).append(entry_b)

    for rule_a, rule_b, score, relationship in contradiction_pairs:
        report_entry = build_contradiction_report_entry(rule_a, rule_b, score, relationship)
        contradiction_reports.append(report_entry)
        print_relation("CONTRADICTION", report_entry)

        entry_a = build_similarity_entry(rule_b.rule_id, score, relationship)
        entry_b = build_similarity_entry(rule_a.rule_id, score, relationship)
        updates_by_rule_id.setdefault(rule_a.rule_id, []).append(entry_a)
        updates_by_rule_id.setdefault(rule_b.rule_id, []).append(entry_b)

    for rule_a, rule_b, score, conflict_type, positional_key in positional_conflict_pairs:
        report_entry = build_positional_conflict_entry(rule_a, rule_b, score, conflict_type, positional_key)
        positional_conflict_reports.append(report_entry)
        print_relation("POSITIONAL", report_entry)

        entry_a = build_similarity_entry(rule_b.rule_id, score, conflict_type)
        entry_b = build_similarity_entry(rule_a.rule_id, score, conflict_type)
        updates_by_rule_id.setdefault(rule_a.rule_id, []).append(entry_a)
        updates_by_rule_id.setdefault(rule_b.rule_id, []).append(entry_b)

    if args.update_files and not args.dry_run:
        write_back_files({**file_payloads_a, **file_payloads_b}, updates_by_rule_id, rule_ids_a, rule_ids_b)
        print("Source JSON files updated.")
    elif args.dry_run:
        print("Dry run complete. No source JSON files were changed.")

    report = {
        "run_timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "folder_a": str(folder_a),
        "folder_b": str(folder_b),
        "threshold_used": args.threshold,
        "rules_in_a": len(rules_a),
        "rules_in_b": len(rules_b),
        "pairs_evaluated": len(rules_a) * len(rules_b),
        "duplicate_candidates": len(similarity_reports),
        "contradiction_pairs": len(contradiction_reports),
        "positional_conflicts": len(positional_conflict_reports),
        "positional_conflict_skipped": args.skip_positional,
        "matches": similarity_reports,
        "contradictions": contradiction_reports,
        "positional_conflicts_detail": positional_conflict_reports,
    }
    output_report_path.parent.mkdir(parents=True, exist_ok=True)
    output_report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Report written to {output_report_path}")


if __name__ == "__main__":
    main()
