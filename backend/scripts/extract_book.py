#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from knowledge_schema import InterpretationRuleDocument  # noqa: E402


PLANETS = {
    "sun": "Sun",
    "moon": "Moon",
    "mars": "Mars",
    "mercury": "Mercury",
    "jupiter": "Jupiter",
    "venus": "Venus",
    "saturn": "Saturn",
    "rahu": "Rahu",
    "ketu": "Ketu",
    "shani": "Saturn",
    "guru": "Jupiter",
    "chandra": "Moon",
    "surya": "Sun",
    "budha": "Mercury",
    "mangal": "Mars",
    "shukra": "Venus",
}
SIGNS = {
    "aries": "Aries",
    "taurus": "Taurus",
    "gemini": "Gemini",
    "cancer": "Cancer",
    "leo": "Leo",
    "virgo": "Virgo",
    "libra": "Libra",
    "scorpio": "Scorpio",
    "sagittarius": "Sagittarius",
    "capricorn": "Capricorn",
    "aquarius": "Aquarius",
    "pisces": "Pisces",
}
NAKSHATRAS = {
    "ashwini": "Ashwini",
    "bharani": "Bharani",
    "krittika": "Krittika",
    "rohini": "Rohini",
    "mrigashira": "Mrigashira",
    "ardra": "Ardra",
    "punarvasu": "Punarvasu",
    "pushya": "Pushya",
    "ashlesha": "Ashlesha",
    "magha": "Magha",
    "purva phalguni": "Purva Phalguni",
    "uttara phalguni": "Uttara Phalguni",
    "hasta": "Hasta",
    "chitra": "Chitra",
    "swati": "Swati",
    "vishakha": "Vishakha",
    "anuradha": "Anuradha",
    "jyeshtha": "Jyeshtha",
    "mula": "Mula",
    "purva ashadha": "Purva Ashadha",
    "uttara ashadha": "Uttara Ashadha",
    "shravana": "Shravana",
    "dhanishta": "Dhanishta",
    "shatabhisha": "Shatabhisha",
    "purva bhadrapada": "Purva Bhadrapada",
    "uttara bhadrapada": "Uttara Bhadrapada",
    "revati": "Revati",
}
VOICE_LABELS = {
    "classical": "classical",
    "modern_analytical": "modern analytical",
    "kp_technical": "KP technical",
    "spiritual": "spiritual",
    "popular": "popular",
}
STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "among",
    "been",
    "being",
    "between",
    "chapter",
    "during",
    "from",
    "have",
    "house",
    "houses",
    "into",
    "native",
    "planet",
    "result",
    "results",
    "shall",
    "that",
    "their",
    "there",
    "these",
    "this",
    "those",
    "through",
    "very",
    "with",
    "would",
}
PREDICTIVE_KEYWORDS = (
    "indicates",
    "indicate",
    "shows",
    "show",
    "gives",
    "give",
    "results",
    "result",
    "brings",
    "brings",
    "delayed",
    "delay",
    "marriage",
    "wealth",
    "career",
    "health",
    "fortune",
    "suffers",
    "success",
    "gain",
    "loss",
    "partner",
    "relationship",
    "native",
)
REMEDY_MARKERS = ("remedy", "worship", "chant", "donate", "fast", "wear", "offer", "pooja", "pooja", "mantra")
POSITIVE_MARKERS = ("success", "gain", "wealth", "fortunate", "happy", "stable", "support", "benefit", "prosperity", "strong")
NEGATIVE_MARKERS = ("delay", "loss", "disease", "obstacle", "conflict", "suffers", "difficult", "stress", "coldness", "separation")
EARLY_MARKERS = ("early", "young", "sooner", "before")
LATE_MARKERS = ("delay", "delayed", "later", "late", "postponed", "mature")
CYCLICAL_MARKERS = ("cycle", "cyclical", "repeated", "recurring", "again and again")

PLANET_HOUSE_RE = re.compile(
    r"\b(?P<planet>sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu|shani|guru|chandra|surya|budha|mangal|shukra)\b"
    r"(?:\s+is|\s+be|\s+being|\s+when|\s+placed|\s+occupies|\s+in|\s+occupying|\s+located)*"
    r".{0,30}?\b(?P<house>1[0-2]|[1-9])(?:st|nd|rd|th)?\s+(?:house|bhava)\b",
    re.IGNORECASE,
)
PLANET_SIGN_RE = re.compile(
    r"\b(?P<planet>sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu|shani|guru|chandra|surya|budha|mangal|shukra)\b"
    r".{0,30}?\bin\s+(?P<sign>aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)\b",
    re.IGNORECASE,
)
NAKSHATRA_RE = re.compile(
    r"\b(?P<planet>sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu)\b.{0,30}?\b(?P<nakshatra>ashwini|bharani|krittika|rohini|mrigashira|ardra|punarvasu|pushya|ashlesha|magha|purva phalguni|uttara phalguni|hasta|chitra|swati|vishakha|anuradha|jyeshtha|mula|purva ashadha|uttara ashadha|shravana|dhanishta|shatabhisha|purva bhadrapada|uttara bhadrapada|revati)\b",
    re.IGNORECASE,
)
LORD_RE = re.compile(
    r"\b(?P<source_house>1[0-2]|[1-9])(?:st|nd|rd|th)?\s+lord\b.{0,25}?\bin\s+(?P<target_house>1[0-2]|[1-9])(?:st|nd|rd|th)?\s+(?:house|bhava)\b",
    re.IGNORECASE,
)
YOGA_RE = re.compile(r"\b(?P<yoga>[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3}\s+Yoga)\b")
DASHA_RE = re.compile(r"\b(?P<planet>Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\s+(?P<level>Maha|Antar|Pratyantar)\s+Dasha\b", re.IGNORECASE)


@dataclass
class ExtractionArgs:
    input_path: Path
    book: str
    voice: str
    categories: list[str]
    output_path: Path
    report_path: Path
    science_id: str
    batch_id: str
    chapter: str
    max_rules: int
    min_words: int
    paraphrase_mode: str
    model: str


@dataclass
class CandidateBlock:
    index: int
    heading: str
    chapter: str
    text: str
    word_count: int
    cleanup_flags: list[str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def parse_categories(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def derive_batch_id(output_path: Path) -> str:
    stem = output_path.stem
    prefix = stem.split("_", 1)[0].strip()
    return prefix or "LOCAL-BATCH-001"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_line(line: str) -> str:
    line = line.replace("\u00a0", " ")
    line = line.replace("\u2013", "-").replace("\u2014", "-")
    line = line.replace("\u2018", "'").replace("\u2019", "'")
    line = line.replace("\u201c", '"').replace("\u201d", '"')
    return line.strip()


def cleanup_ocr_text(raw_text: str) -> tuple[str, dict[str, int]]:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    raw_lines = [normalize_line(line) for line in text.split("\n")]
    counts = Counter(line for line in raw_lines if line)
    repeated_headers = {line for line, count in counts.items() if count >= 3 and len(line) <= 80 and not re.search(r"[.!?]$", line)}

    cleaned_lines: list[str] = []
    stats = {
        "input_lines": len(raw_lines),
        "dropped_headers": 0,
        "dropped_page_markers": 0,
        "joined_lines": 0,
        "empty_lines": 0,
    }
    for line in raw_lines:
        if not line:
            cleaned_lines.append("")
            stats["empty_lines"] += 1
            continue
        if line in repeated_headers:
            stats["dropped_headers"] += 1
            continue
        if re.fullmatch(r"(page\s+)?\d+", line.lower()):
            stats["dropped_page_markers"] += 1
            continue
        cleaned_lines.append(line)

    paragraphs: list[str] = []
    current = ""
    for line in cleaned_lines:
        if not line:
            if current:
                paragraphs.append(current.strip())
                current = ""
            continue
        if not current:
            current = line
            continue
        if re.search(r"[:.!?)]$", current) or re.match(r"^[A-Z0-9][A-Z0-9\s:-]{3,}$", line):
            paragraphs.append(current.strip())
            current = line
            continue
        current += " " + line
        stats["joined_lines"] += 1
    if current:
        paragraphs.append(current.strip())

    text = "\n\n".join(re.sub(r"\s+", " ", para).strip() for para in paragraphs if para.strip())
    return text, stats


def split_candidate_blocks(clean_text: str, min_words: int) -> list[CandidateBlock]:
    paragraphs = [para.strip() for para in clean_text.split("\n\n") if para.strip()]
    blocks: list[CandidateBlock] = []
    current_heading = "General"
    block_index = 0

    for paragraph in paragraphs:
        if re.fullmatch(r"[A-Z0-9][A-Z0-9\s:,\-()]{3,}", paragraph) and len(paragraph.split()) <= 12:
            current_heading = paragraph.title()
            continue
        words = paragraph.split()
        if len(words) < min_words:
            continue
        lowered = paragraph.lower()
        if not any(marker in lowered for marker in PREDICTIVE_KEYWORDS):
            continue
        if not any(token in lowered for token in list(PLANETS) + list(SIGNS) + list(NAKSHATRAS)):
            continue
        blocks.append(
            CandidateBlock(
                index=block_index,
                heading=current_heading,
                chapter=current_heading,
                text=paragraph,
                word_count=len(words),
                cleanup_flags=collect_cleanup_flags(paragraph),
            )
        )
        block_index += 1
    return blocks


def collect_cleanup_flags(text: str) -> list[str]:
    flags: list[str] = []
    if re.search(r"\b[a-z]{1,2}\b", text):
        flags.append("short_tokens_present")
    if re.search(r"[|]{2,}|[_]{2,}", text):
        flags.append("column_artifact_suspected")
    if re.search(r"\b\d{1,2}\s+\d{1,2}\b", text):
        flags.append("number_spacing_noise")
    return flags


def infer_condition(text: str) -> dict[str, Any] | None:
    if match := PLANET_HOUSE_RE.search(text):
        planet = PLANETS[match.group("planet").lower()]
        return {"type": "planet_in_house", "planet": planet, "house": int(match.group("house"))}
    if match := PLANET_SIGN_RE.search(text):
        planet = PLANETS[match.group("planet").lower()]
        sign = SIGNS[match.group("sign").lower()]
        return {"type": "planet_in_sign", "planet": planet, "sign": sign}
    if match := NAKSHATRA_RE.search(text):
        planet = PLANETS[match.group("planet").lower()]
        nakshatra = NAKSHATRAS[match.group("nakshatra").lower()]
        return {"type": "planet_in_nakshatra", "planet": planet, "nakshatra": nakshatra}
    if match := LORD_RE.search(text):
        return {
            "type": "house_lord_in_house",
            "source_house": int(match.group("source_house")),
            "target_house": int(match.group("target_house")),
        }
    if match := YOGA_RE.search(text):
        return {"type": "yoga", "yoga_name": match.group("yoga")}
    if match := DASHA_RE.search(text):
        return {
            "type": "dasha_period",
            "dasha_lord": PLANETS[match.group("planet").lower()],
            "level": match.group("level").capitalize(),
        }
    if "retrograde" in text.lower():
        for key, planet in PLANETS.items():
            if key in text.lower():
                return {"type": "planet_retrograde", "planet": planet, "retrograde": True}
    return None


def infer_categories(text: str, cli_categories: list[str]) -> list[str]:
    inferred = set(cli_categories)
    lowered = text.lower()
    mappings = {
        "relationships": ("marriage", "partner", "relationship", "spouse", "love"),
        "career": ("career", "profession", "work", "status", "authority"),
        "wealth": ("wealth", "finance", "income", "gains", "prosperity", "money"),
        "health": ("health", "disease", "illness", "vitality", "constitution"),
        "education": ("education", "learning", "study", "intellect"),
        "spirituality": ("spiritual", "dharma", "moksha", "devotion"),
        "longevity": ("longevity", "lifespan", "death", "maraka"),
        "general": ("native", "temperament", "nature"),
    }
    for category, terms in mappings.items():
        if any(term in lowered for term in terms):
            inferred.add(category)
    specific_categories = {item for item in inferred if item != "general"}
    if specific_categories and "general" in inferred:
        inferred.remove("general")
    return sorted(inferred)


def infer_life_domain(categories: list[str]) -> str:
    priority = ("relationships", "career", "wealth", "health", "education", "spirituality", "longevity", "general")
    for key in priority:
        if key in categories:
            return key
    return categories[0] if categories else "general"


def infer_claim_axis(text: str, categories: list[str]) -> str:
    lowered = text.lower()
    if "marriage" in lowered or "partner" in lowered:
        if any(marker in lowered for marker in EARLY_MARKERS + LATE_MARKERS):
            return "marriage_timing"
        return "partnership_stability"
    if any(term in lowered for term in ("wealth", "money", "income", "loss", "finance")):
        return "financial_security"
    if any(term in lowered for term in ("career", "profession", "status", "promotion", "authority")):
        return "career_growth"
    if any(term in lowered for term in ("health", "disease", "illness", "vitality", "constitution")):
        return "health_vitality"
    if "travel" in lowered:
        return "travel_pattern"
    if "education" in lowered or "learning" in lowered:
        return "learning_outcome"
    life_domain = infer_life_domain(categories)
    return f"{life_domain}_trend"


def infer_claim_scope(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("timing", "age", "years", "later", "early", "delay")):
        return "event_timing"
    if any(term in lowered for term in ("window", "period", "phase", "during")):
        return "window"
    if any(term in lowered for term in ("nature", "temperament", "character", "disposition")):
        return "trait"
    return "tendency"


def infer_claim_polarity(text: str) -> str:
    lowered = text.lower()
    positive = sum(term in lowered for term in POSITIVE_MARKERS)
    negative = sum(term in lowered for term in NEGATIVE_MARKERS)
    if positive and negative:
        return "mixed"
    if positive:
        return "positive"
    if negative:
        return "negative"
    return "neutral"


def infer_timing_bias(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in CYCLICAL_MARKERS):
        return "cyclical"
    if any(term in lowered for term in LATE_MARKERS):
        return "late"
    if any(term in lowered for term in EARLY_MARKERS):
        return "early"
    if "timely" in lowered or "on time" in lowered:
        return "on_time"
    return "none"


def infer_strength_band(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("extreme", "severe", "extraordinary", "powerful", "exceptional")):
        return "extreme"
    if any(term in lowered for term in ("strong", "marked", "significant", "notable", "great")):
        return "high"
    if any(term in lowered for term in ("moderate", "steady", "balanced")):
        return "medium"
    return "low"


def infer_subject_scope(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("spouse", "partner", "wife", "husband")):
        return "partner"
    if any(term in lowered for term in ("family", "home", "children", "parents")):
        return "family"
    if any(term in lowered for term in ("household", "domestic")):
        return "household"
    return "self"


def extract_remedies(text: str) -> list[str]:
    sentences = split_sentences(text)
    return [sentence for sentence in sentences if any(marker in sentence.lower() for marker in REMEDY_MARKERS)]


def extract_keyword_phrases(text: str, limit: int = 6) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text.lower())
    filtered = [word for word in words if word not in STOPWORDS and word not in PLANETS and word not in SIGNS]
    counts = Counter(filtered)
    return [word.replace("-", " ") for word, _ in counts.most_common(limit)]


def verbalize_condition(condition: dict[str, Any] | None) -> str:
    if not condition:
        return "this configuration appears in the chart"
    if condition["type"] == "planet_in_house":
        return f"{condition['planet']} occupies the {ordinal(condition['house'])} house"
    if condition["type"] == "planet_in_sign":
        return f"{condition['planet']} is placed in {condition['sign']}"
    if condition["type"] == "planet_in_nakshatra":
        return f"{condition['planet']} falls in {condition['nakshatra']}"
    if condition["type"] == "house_lord_in_house":
        return f"the {ordinal(condition['source_house'])} lord moves to the {ordinal(condition['target_house'])} house"
    if condition["type"] == "yoga":
        return f"{condition['yoga_name']} is formed"
    if condition["type"] == "dasha_period":
        return f"{condition['dasha_lord']} {condition['level']} Dasha is active"
    if condition["type"] == "planet_retrograde":
        return f"{condition['planet']} is retrograde"
    return "this configuration appears in the chart"


def ordinal(number: int | None) -> str:
    if number is None:
        return "relevant"
    suffix = "th"
    if number % 10 == 1 and number % 100 != 11:
        suffix = "st"
    elif number % 10 == 2 and number % 100 != 12:
        suffix = "nd"
    elif number % 10 == 3 and number % 100 != 13:
        suffix = "rd"
    return f"{number}{suffix}"


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def build_fallback_paraphrase(text: str, condition: dict[str, Any] | None, voice: str, categories: list[str]) -> tuple[str, str, str]:
    key_phrases = extract_keyword_phrases(text)
    phrase_text = ", ".join(key_phrases[:4]) if key_phrases else "the themes highlighted in the source"
    condition_text = verbalize_condition(condition)
    category_text = format_category_text(categories)
    intro = {
        "classical": f"When {condition_text}, the shastric indication turns the native's attention toward {category_text}.",
        "modern_analytical": f"When {condition_text}, the reading usually concentrates on {category_text}.",
        "kp_technical": f"When {condition_text}, the rule points directly to {category_text}.",
        "spiritual": f"When {condition_text}, the soul is asked to work through lessons connected with {category_text}.",
        "popular": f"When {condition_text}, this placement tends to show up most clearly in {category_text}.",
    }[voice]
    body = {
        "classical": f"The source emphasises {phrase_text}, suggesting that these matters unfold through disciplined cause and effect.",
        "modern_analytical": f"The source material emphasises {phrase_text}, so the lived expression is likely to be practical rather than abstract.",
        "kp_technical": f"The source emphasises {phrase_text}, and those indications should be timed and filtered against supporting chart factors.",
        "spiritual": f"The source emphasises {phrase_text}, framing them as lessons that mature through lived experience and conscious effort.",
        "popular": f"The source emphasises {phrase_text}, so these are the areas most likely to feel noticeable in everyday life.",
    }[voice]
    close = "Fallback paraphrase generated locally because no live model response was available."
    confidence = "MEDIUM" if condition else "LOW"
    return " ".join((intro, body, close)), confidence, close


def format_category_text(categories: list[str]) -> str:
    filtered = [category.replace("_", " ") for category in categories if category != "general"]
    if not filtered:
        return "general life patterns"
    if len(filtered) == 1:
        return filtered[0]
    if len(filtered) == 2:
        return f"{filtered[0]} and {filtered[1]}"
    return f"{', '.join(filtered[:-1])}, and {filtered[-1]}"


def build_paraphrase_prompt(source_text: str, voice: str, book: str, condition: dict[str, Any] | None) -> str:
    condition_text = verbalize_condition(condition)
    return f"""
You are paraphrasing an extracted astrological source passage for EverydayHoroscope.

Follow this policy exactly:
- Preserve the astrological meaning and If-Then logic.
- Do not copy the author's sentence structure.
- Use original prose in a {VOICE_LABELS[voice]} voice.
- Technical vocabulary like planets, houses, yogas, dashas, and nakshatras may be used freely.
- Do not add remedies or predictions not present in the source.
- Return JSON only with keys: text, confidence, paraphrase_notes.

Voice tone: {voice}
Book: {book}
Detected condition: {condition_text}

Source passage:
\"\"\"{source_text}\"\"\"
""".strip()


def extract_json_object(raw_text: str) -> dict[str, Any] | None:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def paraphrase_with_claude(source_text: str, voice: str, book: str, condition: dict[str, Any] | None, model: str) -> dict[str, Any] | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic  # type: ignore
    except Exception:
        return None

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=900,
            temperature=0.35,
            messages=[{"role": "user", "content": build_paraphrase_prompt(source_text, voice, book, condition)}],
        )
    except Exception:
        return None

    text_parts: list[str] = []
    for item in getattr(response, "content", []) or []:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    if not text_parts:
        return None
    return extract_json_object("\n".join(text_parts))


def paraphrase_block(block: CandidateBlock, args: ExtractionArgs, condition: dict[str, Any] | None, categories: list[str]) -> tuple[str, str, str]:
    response: dict[str, Any] | None = None
    if args.paraphrase_mode in {"claude", "hybrid"}:
        response = paraphrase_with_claude(block.text, args.voice, args.book, condition, args.model)
    if response and isinstance(response.get("text"), str) and response["text"].strip():
        confidence = str(response.get("confidence") or "MEDIUM").upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            confidence = "MEDIUM"
        notes = str(response.get("paraphrase_notes") or "").strip()
        return response["text"].strip(), confidence, notes
    if args.paraphrase_mode == "claude":
        raise RuntimeError("Claude paraphrase was requested, but no valid model response was returned.")
    return build_fallback_paraphrase(block.text, condition, args.voice, categories)


def build_rule_id(book: str, condition: dict[str, Any] | None, index: int) -> str:
    book_part = slugify(book).replace("-", "").upper()[:6] or "BOOK"
    if condition and condition["type"] == "planet_in_house":
        return f"R-{book_part}-{condition['planet'][:3].upper()}-{condition['house']}H-{index:03d}"
    if condition and condition["type"] == "planet_in_sign":
        return f"R-{book_part}-{condition['planet'][:3].upper()}-{condition['sign'][:3].upper()}-{index:03d}"
    if condition and condition["type"] == "house_lord_in_house":
        return f"R-{book_part}-{condition['source_house']}L-{condition['target_house']}H-{index:03d}"
    if condition and condition["type"] == "yoga":
        yoga = slugify(condition["yoga_name"]).replace("-", "").upper()[:6]
        return f"R-{book_part}-{yoga}-{index:03d}"
    return f"R-{book_part}-GEN-{index:03d}"


def summarise_paraphrase(paraphrase_text: str) -> str:
    sentences = split_sentences(paraphrase_text)
    if not sentences:
        return paraphrase_text[:180].strip()
    return sentences[0][:240].strip()


def build_rule_document(block: CandidateBlock, args: ExtractionArgs, sequence: int) -> tuple[InterpretationRuleDocument, dict[str, Any]]:
    condition = infer_condition(block.text)
    categories = infer_categories(block.text, args.categories)
    paraphrase_text, confidence, notes = paraphrase_block(block, args, condition, categories)
    summary = summarise_paraphrase(paraphrase_text)
    remedies = extract_remedies(block.text)
    rule_payload = {
        "rule_id": build_rule_id(args.book, condition, sequence),
        "version": 1,
        "science_id": args.science_id,
        "approval_status": "pending_review",
        "life_domain": infer_life_domain(categories),
        "claim_axis": infer_claim_axis(block.text, categories),
        "claim_scope": infer_claim_scope(block.text),
        "claim_polarity": infer_claim_polarity(block.text),
        "timing_bias": infer_timing_bias(block.text),
        "strength_band": infer_strength_band(block.text),
        "subject_scope": infer_subject_scope(block.text),
        "authority_override": None,
        "mutually_exclusive_with": [],
        "passage_ref_id": None,
        "condition": condition or {"type": "composite", "sub_conditions": [], "operator": "and"},
        "interpretation": {
            "summary": summary,
            "detailed": paraphrase_text,
            "full_text_passages": [
                {
                    "text": paraphrase_text,
                    "source": args.book,
                    "chapter": block.chapter or args.chapter,
                    "word_count": len(paraphrase_text.split()),
                    "voice_tone": args.voice,
                    "confidence": confidence,
                    "paraphrase_notes": notes or None,
                }
            ],
            "positive_aspects": [],
            "challenging_aspects": [],
            "remedies": remedies,
        },
        "categories": categories,
        "priority": 5,
        "intensity_score": 0.0,
        "source": {
            "primary": args.book,
            "chapter": block.chapter or args.chapter,
            "author_voice": args.voice,
            "secondary_sources": [],
            "batch_id": args.batch_id,
        },
        "modifiers": [],
        "conflicts_with": [],
        "weight": 1.0,
        "tags": build_tags(block.text, condition, categories),
        "active": True,
    }
    rule = InterpretationRuleDocument(**rule_payload)
    meta = {
        "confidence": confidence,
        "review_action": review_action_for_confidence(confidence),
        "cleanup_flags": block.cleanup_flags,
        "raw_word_count": block.word_count,
        "paraphrase_notes": notes,
        "condition_detected": condition is not None,
    }
    return rule, meta


def build_tags(text: str, condition: dict[str, Any] | None, categories: list[str]) -> list[str]:
    tags = set(categories)
    if condition:
        tags.add(condition["type"])
        for key in ("planet", "sign", "nakshatra", "yoga_name"):
            value = condition.get(key)
            if value:
                tags.add(slugify(str(value)).replace("-", "_"))
        if condition.get("house") is not None:
            tags.add(f"{condition['house']}th_house")
    for phrase in extract_keyword_phrases(text, limit=4):
        tags.add(slugify(phrase).replace("-", "_"))
    return sorted(tag for tag in tags if tag)


def review_action_for_confidence(confidence: str) -> str:
    if confidence == "HIGH":
        return "stage_for_import_review"
    if confidence == "MEDIUM":
        return "claude_spot_check_sample"
    return "claude_review_required"


def write_json_output(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def write_report(path: Path, report: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def build_report_markdown(args: ExtractionArgs, clean_stats: dict[str, int], candidates: list[CandidateBlock], extracted: list[tuple[InterpretationRuleDocument, dict[str, Any]]]) -> str:
    confidence_counts = Counter(meta["confidence"] for _, meta in extracted)
    review_counts = Counter(meta["review_action"] for _, meta in extracted)
    lines = [
        f"# Import Report — {args.book}",
        "",
        f"- Generated at: `{utc_now_iso()}`",
        f"- Input file: `{args.input_path}`",
        f"- Batch ID: `{args.batch_id}`",
        f"- Voice: `{args.voice}`",
        f"- Categories: `{', '.join(args.categories)}`",
        f"- Candidate blocks scanned: `{len(candidates)}`",
        f"- Rules extracted: `{len(extracted)}`",
        "",
        "## OCR Cleanup",
        "",
        f"- Input lines: `{clean_stats['input_lines']}`",
        f"- Repeated headers removed: `{clean_stats['dropped_headers']}`",
        f"- Page markers removed: `{clean_stats['dropped_page_markers']}`",
        f"- Mid-sentence joins: `{clean_stats['joined_lines']}`",
        "",
        "## Confidence Summary",
        "",
        f"- HIGH: `{confidence_counts.get('HIGH', 0)}`",
        f"- MEDIUM: `{confidence_counts.get('MEDIUM', 0)}`",
        f"- LOW: `{confidence_counts.get('LOW', 0)}`",
        "",
        "## Review Routing",
        "",
        f"- Stage for import review: `{review_counts.get('stage_for_import_review', 0)}`",
        f"- Claude spot-check sample: `{review_counts.get('claude_spot_check_sample', 0)}`",
        f"- Claude review required: `{review_counts.get('claude_review_required', 0)}`",
        "",
        "## Extracted Rules",
        "",
    ]
    for rule, meta in extracted:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- Chapter: `{rule.source.chapter}`",
                f"- Condition type: `{rule.condition.type}`",
                f"- Life domain: `{rule.life_domain}`",
                f"- Claim axis: `{rule.claim_axis}`",
                f"- Confidence: `{meta['confidence']}`",
                f"- Review action: `{meta['review_action']}`",
                f"- Cleanup flags: `{', '.join(meta['cleanup_flags']) if meta['cleanup_flags'] else 'none'}`",
                f"- Summary: {rule.interpretation.summary}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def parse_args(argv: list[str]) -> ExtractionArgs:
    parser = argparse.ArgumentParser(description="Extract structured interpretation rules from OCR text.")
    parser.add_argument("--input", dest="input_path", required=True)
    parser.add_argument("--book", required=True)
    parser.add_argument("--voice", required=True, choices=sorted(VOICE_LABELS))
    parser.add_argument("--categories", required=True)
    parser.add_argument("--output", dest="output_path", required=True)
    parser.add_argument("--report", dest="report_path", required=True)
    parser.add_argument("--science-id", default="vedic_astrology")
    parser.add_argument("--batch-id", default="")
    parser.add_argument("--chapter", default="General")
    parser.add_argument("--max-rules", type=int, default=100)
    parser.add_argument("--min-words", type=int, default=45)
    parser.add_argument("--paraphrase-mode", choices=("hybrid", "claude", "local"), default="hybrid")
    parser.add_argument("--model", default=os.getenv("EXTRACT_BOOK_CLAUDE_MODEL", "claude-sonnet-4-6"))
    ns = parser.parse_args(argv)
    output_path = Path(ns.output_path).expanduser().resolve()
    return ExtractionArgs(
        input_path=Path(ns.input_path).expanduser().resolve(),
        book=ns.book.strip(),
        voice=ns.voice,
        categories=parse_categories(ns.categories),
        output_path=output_path,
        report_path=Path(ns.report_path).expanduser().resolve(),
        science_id=ns.science_id.strip() or "vedic_astrology",
        batch_id=ns.batch_id.strip() or derive_batch_id(output_path),
        chapter=ns.chapter.strip() or "General",
        max_rules=max(1, ns.max_rules),
        min_words=max(20, ns.min_words),
        paraphrase_mode=ns.paraphrase_mode,
        model=ns.model.strip(),
    )


def extract_rules(args: ExtractionArgs) -> tuple[dict[str, Any], str]:
    raw_text = read_text(args.input_path)
    clean_text, clean_stats = cleanup_ocr_text(raw_text)
    candidates = split_candidate_blocks(clean_text, args.min_words)

    extracted: list[tuple[InterpretationRuleDocument, dict[str, Any]]] = []
    for candidate in candidates[: args.max_rules]:
        try:
            extracted.append(build_rule_document(candidate, args, len(extracted) + 1))
        except Exception as exc:
            fallback_payload = {
                "confidence": "LOW",
                "review_action": "claude_review_required",
                "cleanup_flags": candidate.cleanup_flags + [f"build_error:{type(exc).__name__}"],
                "raw_word_count": candidate.word_count,
                "paraphrase_notes": str(exc),
                "condition_detected": False,
            }
            summary = f"Extraction failed for candidate {candidate.index}: {exc}"
            error_rule = InterpretationRuleDocument(
                rule_id=build_rule_id(args.book, None, len(extracted) + 1),
                version=1,
                science_id=args.science_id,
                approval_status="pending_review",
                life_domain="general",
                claim_axis="general_trend",
                claim_scope="tendency",
                claim_polarity="neutral",
                timing_bias="none",
                strength_band="low",
                subject_scope="self",
                condition={"type": "composite", "sub_conditions": [], "operator": "and"},
                interpretation={
                    "summary": summary,
                    "detailed": summary,
                    "full_text_passages": [
                        {
                            "text": summary,
                            "source": args.book,
                            "chapter": candidate.chapter,
                            "word_count": len(summary.split()),
                            "voice_tone": args.voice,
                            "confidence": "LOW",
                            "paraphrase_notes": str(exc),
                        }
                    ],
                    "positive_aspects": [],
                    "challenging_aspects": [],
                    "remedies": [],
                },
                categories=args.categories or ["general"],
                source={
                    "primary": args.book,
                    "chapter": candidate.chapter,
                    "author_voice": args.voice,
                    "secondary_sources": [],
                    "batch_id": args.batch_id,
                },
                modifiers=[],
                conflicts_with=[],
                weight=1.0,
                tags=["needs_review"],
                active=True,
            )
            extracted.append((error_rule, fallback_payload))

    payload = {
        "batch_id": args.batch_id,
        "source_book": args.book,
        "science_id": args.science_id,
        "voice": args.voice,
        "categories": args.categories,
        "generated_at": utc_now_iso(),
        "stats": {
            "candidate_blocks": len(candidates),
            "rules_extracted": len(extracted),
            "cleanup": clean_stats,
        },
        "rules": [
            {
                **rule.model_dump(mode="json", by_alias=True, exclude_none=True),
                "_extraction_meta": meta,
            }
            for rule, meta in extracted
        ],
    }
    report = build_report_markdown(args, clean_stats, candidates, extracted)
    return payload, report


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload, report = extract_rules(args)
    write_json_output(args.output_path, payload)
    write_report(args.report_path, report)
    print(f"Extracted {len(payload['rules'])} rules from {args.input_path.name} into {args.output_path}")
    print(f"Review report written to {args.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
