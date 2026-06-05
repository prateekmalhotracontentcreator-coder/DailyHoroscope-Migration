#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any


GARBAGE_RE = re.compile(
    r"(.)\1{6,}|"
    r"[^\x00-\x7F]{15,}|"
    r"\b[A-Z]{20,}\b"
)

VALIDATION_SYSTEM = (
    "You are a senior Vedic astrology scholar and knowledge engineer. "
    "You evaluate extracted interpretation rules for correctness, coherence, "
    "and faithfulness to classical Vedic texts including BPHS, Phaladeepika, "
    "Lal Kitab, and other authoritative sources."
)

VALIDATION_PROMPT = """\
Evaluate each rule below and return a JSON array - one object per rule.

For each rule assess:
1. CORRECTNESS - consistent with classical Vedic astrology?
2. QUALITY - coherent, specific, usable as a prediction statement?
3. FAITHFULNESS - does it faithfully paraphrase what a classical source would say?

IMPORTANT -- condition field guidance:
- Many rules have condition: {{"type": "composite", "sub_conditions": [], "operator": "and"}}
  This means the rule is a GENERAL astrological principle (e.g. a planet's nature, a house
  signification, a yoga, or a general interpretive statement). This is VALID -- do NOT flag
  a rule solely because its condition is empty or composite.
- Rules with condition: {{"type": "dosha", "sub_type": "mangalik", ...}} are Lal Kitab
  Mangalik dosha rules. They contain extra fields (ascendant, aspect_houses, dosha_type,
  ascendant_filter) which are schema extensions -- VALID. Evaluate only the interpretation
  text (summary / detailed / remedies) on its astrological merits.
- Evaluate the "summary" and "detailed" interpretation text on its own merits.
- Only flag if the interpretation text itself is wrong, incoherent, or garbled.

Verdict options:
  "approve"     - correct and ready for production
  "spot_check"  - probably fine but borderline; flag for quick human glance
  "flag"        - incorrect, incoherent, or suspicious (base this on the TEXT, not the condition)

Return ONLY valid JSON - no markdown fences, no commentary:
[
  {{
    "rule_id": "<rule_id>",
    "verdict": "approve" | "spot_check" | "flag",
    "reason": "<one sentence - required for spot_check and flag, empty for approve>",
    "corrected_confidence": "HIGH" | "MEDIUM" | "LOW"
  }}
]

Rules to evaluate:
{rules_json}
"""

CONTRADICTION_PROMPT = """\
Check whether any rules below directly contradict each other.
Different emphasis or wording across books is NOT a contradiction.
A true contradiction is when two rules make opposite factual claims about
the same planetary placement (e.g. one says "gives wealth", another says
"destroys wealth" for identical conditions).

Return ONLY valid JSON - no markdown fences:
[
  {{
    "rule_id_a": "...",
    "rule_id_b": "...",
    "contradiction_summary": "<one sentence>"
  }}
]
Return an empty array [] if no contradictions found.

Rules to compare:
{rules_json}
"""


class RuleValidator:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic  # type: ignore
            except ImportError as exc:
                raise RuntimeError("anthropic package not installed") from exc
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    @staticmethod
    def _current_confidence(rule: dict) -> str:
        validation = rule.get("validation") or {}
        if validation.get("corrected_confidence"):
            return str(validation["corrected_confidence"]).upper()
        passages = ((rule.get("interpretation") or {}).get("full_text_passages") or [])
        if passages:
            confidence = passages[0].get("confidence")
            if confidence:
                return str(confidence).upper()
        return "MEDIUM"

    # Condition types that use the structured yoga schema
    # (yoga_name / yoga_check / planets_involved / houses_involved).
    # These types come from TBA-style extractions where the "detailed" field
    # follows a fixed "Yoga/Category ... Condition ... Effect" template rather than
    # being a direct prose passage.  The truncated_text guard (last-character
    # punctuation check) is designed for OCR-extracted BPHS passages and must
    # not be applied to structured yoga descriptors whose effect text naturally
    # ends without a terminal period.
    YOGA_SCHEMA_TYPES: frozenset[str] = frozenset({
        "yoga_combination",
        "general_principle",
        "dosha",
    })

    def structural_check(self, rule: dict) -> tuple[bool, str]:
        interp = rule.get("interpretation") or {}
        detailed = (interp.get("detailed") or "").strip()
        summary = (interp.get("summary") or "").strip()
        if not detailed and not summary:
            return False, "empty_interpretation"
        text = detailed or summary
        if GARBAGE_RE.search(text):
            return False, "ocr_garbage_detected"
        cond_type = (rule.get("condition") or {}).get("type", "")
        min_words = 3 if cond_type in ("planet_in_house_in_sign", "planet_in_house_special") else 8
        if len(text.split()) < min_words:
            return False, "interpretation_too_short"
        # Detect mid-sentence truncation -- text ending without punctuation.
        # Skip for yoga-schema types: their "Effect:" clause ends naturally
        # without a period and the Claude quality check (Stage 2) handles
        # content quality for those rules.
        if cond_type not in self.YOGA_SCHEMA_TYPES:
            last_char = text.strip()[-1] if text.strip() else ""
            if last_char not in ".!?\"')":
                return False, "truncated_text"
        condition = rule.get("condition")
        if not condition or not isinstance(condition, dict):
            return False, "missing_condition"
        return True, "ok"

    def _rule_to_prompt_item(self, rule: dict) -> dict:
        interp = rule.get("interpretation") or {}
        source = rule.get("source") or {}
        return {
            "rule_id": rule.get("rule_id", ""),
            "source_book": source.get("book", source.get("primary", "")),
            "chapter": source.get("chapter", ""),
            "condition": rule.get("condition", {}),
            "summary": (interp.get("summary") or "")[:400],
            "detailed": (interp.get("detailed") or "")[:800],
            "current_confidence": self._current_confidence(rule),
        }

    def _call_claude(self, prompt: str) -> list[dict]:
        client = self._get_client()
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0.1,
            system=VALIDATION_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.content[0].text.strip() if response.content else "[]"
        content = re.sub(r"^```[a-z]*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)
        try:
            result = json.loads(content)
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            return []

    def validate_batch(self, rules: list[dict]) -> list[dict]:
        if not rules:
            return []
        items = [self._rule_to_prompt_item(rule) for rule in rules]
        prompt = VALIDATION_PROMPT.format(rules_json=json.dumps(items, indent=2))
        return self._call_claude(prompt)

    def detect_contradictions(self, rules: list[dict]) -> list[dict]:
        if len(rules) < 2:
            return []
        items = [self._rule_to_prompt_item(rule) for rule in rules]
        prompt = CONTRADICTION_PROMPT.format(rules_json=json.dumps(items, indent=2))
        return self._call_claude(prompt)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
