from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

try:
    from motor.motor_asyncio import AsyncIOMotorDatabase
except Exception:  # pragma: no cover - local lightweight validation path
    AsyncIOMotorDatabase = Any  # type: ignore[misc, assignment]

from knowledge_schema import (
    COLLECTION_INTERPRETATION_RULES,
    InterpretationRuleDocument,
    KnowledgeRequestContext,
)


logger = logging.getLogger(__name__)

SCIENCE_WEIGHTS = {
    "vedic_astrology": 0.40,
    "palmistry": 0.25,
    "numerology": 0.20,
    "tarot": 0.15,
    "kp": 0.20,
}
STRENGTH_MULTIPLIERS = {"low": 0.70, "medium": 0.85, "high": 1.00, "extreme": 1.15}
MODIFIER_FACTORS = {
    "amplify_positive": 1.15,
    "amplify_negative": 1.15,
    "intensify": 1.10,
    "diminish": 0.85,
    "suppress": 0.75,
}
APPROVED_RULE_FILTER = {"active": True, "approval_status": "approved"}
DEFAULT_BACKBONE = "vedic_astrology"
PLANET_VARIANTS = {
    "Sun (Surya)": "Sun",
    "Moon (Chandra)": "Moon",
    "Mars (Mangal)": "Mars",
    "Mercury (Budha)": "Mercury",
    "Jupiter (Brihaspati)": "Jupiter",
    "Venus (Shukra)": "Venus",
    "Saturn (Shani)": "Saturn",
    "Sun": "Sun",
    "Moon": "Moon",
    "Mars": "Mars",
    "Mercury": "Mercury",
    "Jupiter": "Jupiter",
    "Venus": "Venus",
    "Saturn": "Saturn",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
    "Lagna": "Lagna",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_planet_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = str(value).strip()
    return PLANET_VARIANTS.get(cleaned, cleaned.split("(", 1)[0].strip())


def normalize_sign_name(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = str(value).strip()
    return cleaned[:1].upper() + cleaned[1:].lower() if cleaned else None


def normalize_nakshatra_name(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(part.capitalize() for part in str(value).strip().split())


def normalize_dignity(value: str | None) -> str | None:
    if not value:
        return None
    return str(value).strip().lower()


def canonical_key(condition_type: str, *parts: Any) -> str:
    normalized_parts: list[str] = [condition_type]
    for part in parts:
        if part is None:
            continue
        normalized_parts.append(str(part))
    return "|".join(normalized_parts)


def sorted_planet_list(planets: list[str]) -> list[str]:
    return sorted(filter(None, (normalize_planet_name(planet) for planet in planets)))


@dataclass
class ChartFacts:
    keys: set[str] = field(default_factory=set)
    planet_positions: dict[str, dict[str, Any]] = field(default_factory=dict)
    house_planets: dict[int, list[str]] = field(default_factory=lambda: defaultdict(list))
    house_lords: dict[int, str] = field(default_factory=dict)
    yogas: set[str] = field(default_factory=set)
    dasha_levels: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    aspect_targets: dict[str, set[int]] = field(default_factory=lambda: defaultdict(set))
    aspected_by: dict[int, set[str]] = field(default_factory=lambda: defaultdict(set))


@dataclass
class IndexedRule:
    document: InterpretationRuleDocument
    anchor_keys: set[str]


@dataclass
class KnowledgeIndexSnapshot:
    built_at: datetime
    rule_count: int
    key_to_rule_ids: dict[str, set[str]]
    rules_by_id: dict[str, IndexedRule]


def extract_chart_facts(chart: dict[str, Any]) -> ChartFacts:
    facts = ChartFacts()
    planet_positions = _extract_planet_positions(chart)
    facts.planet_positions = planet_positions

    for planet, payload in planet_positions.items():
        house = payload.get("house")
        sign = payload.get("sign")
        nakshatra = payload.get("nakshatra")
        dignity = payload.get("dignity")
        retrograde = bool(payload.get("retrograde"))

        if house is not None:
            facts.keys.add(canonical_key("planet_in_house", planet, house))
            facts.house_planets[int(house)].append(planet)
        if sign:
            facts.keys.add(canonical_key("planet_in_sign", planet, sign))
        if nakshatra:
            facts.keys.add(canonical_key("planet_in_nakshatra", planet, nakshatra))
        if dignity:
            facts.keys.add(canonical_key("planet_dignity", planet, dignity))
        if retrograde:
            facts.keys.add(canonical_key("planet_retrograde", planet, True))

    _populate_conjunction_facts(facts)
    _populate_house_lord_facts(chart, facts)
    _populate_yoga_facts(chart, facts)
    _populate_dasha_facts(chart, facts)
    _populate_aspect_facts(facts)
    return facts


def _extract_planet_positions(chart: dict[str, Any]) -> dict[str, dict[str, Any]]:
    positions: dict[str, dict[str, Any]] = {}

    if isinstance(chart.get("planets"), dict):
        for raw_name, payload in chart["planets"].items():
            name = normalize_planet_name(raw_name)
            if not name:
                continue
            positions[name] = {
                "house": payload.get("house"),
                "sign": normalize_sign_name(payload.get("sign")),
                "nakshatra": normalize_nakshatra_name(payload.get("nakshatra") if isinstance(payload.get("nakshatra"), str) else (payload.get("nakshatra") or {}).get("name")),
                "retrograde": bool(payload.get("retrograde")),
                "dignity": normalize_dignity(payload.get("dignity")),
            }

    d1_chart = ((chart.get("charts") or {}).get("D1") or {})
    for graha in d1_chart.get("grahas", []):
        raw_name = graha.get("name") or graha.get("code")
        name = normalize_planet_name(raw_name)
        if not name or name == "Lagna":
            continue
        positions[name] = {
            "house": graha.get("house_whole_sign"),
            "sign": normalize_sign_name(graha.get("sign")),
            "nakshatra": normalize_nakshatra_name(graha.get("nakshatra")),
            "retrograde": bool(graha.get("retrograde")),
            "dignity": normalize_dignity(graha.get("dignity")),
        }
    return positions


def _populate_conjunction_facts(facts: ChartFacts) -> None:
    for house, planets in facts.house_planets.items():
        normalized = sorted_planet_list(planets)
        if len(normalized) < 2:
            continue
        facts.keys.add(canonical_key("planet_conjunction", *normalized, house))
        for index, first in enumerate(normalized):
            for second in normalized[index + 1 :]:
                facts.keys.add(canonical_key("planet_conjunction", first, second, house))


def _populate_house_lord_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    if isinstance(chart.get("houses"), dict):
        for house_num, payload in chart["houses"].items():
            try:
                facts.house_lords[int(house_num)] = normalize_planet_name(payload.get("lord")) or str(payload.get("lord"))
            except Exception:
                continue
    d1_chart = ((chart.get("charts") or {}).get("D1") or {})
    for payload in d1_chart.get("houses", []):
        house_num = payload.get("house_num")
        if house_num is None:
            continue
        lord = normalize_planet_name(payload.get("lord"))
        if lord:
            facts.house_lords[int(house_num)] = lord

    for source_house, lord in facts.house_lords.items():
        target_house = (facts.planet_positions.get(lord) or {}).get("house")
        if target_house is None:
            continue
        facts.keys.add(canonical_key("house_lord_in_house", source_house, target_house))


def _populate_yoga_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    yoga_layer = ((chart.get("layers") or {}).get("yoga") or {})
    for item in yoga_layer.get("items", []):
        if not item.get("matched"):
            continue
        name = item.get("name")
        code = item.get("code")
        if name:
            facts.yogas.add(str(name))
            facts.keys.add(canonical_key("yoga", name))
        if code:
            facts.yogas.add(str(code))
            facts.keys.add(canonical_key("yoga", code))


def _populate_dasha_facts(chart: dict[str, Any], facts: ChartFacts) -> None:
    current = chart.get("current_dasha") or {}
    if isinstance(current, dict) and current.get("planet"):
        planet = normalize_planet_name(current.get("planet"))
        if planet:
            facts.dasha_levels[planet].add("Maha")
            facts.keys.add(canonical_key("dasha_period", planet, "Maha"))

    overview = chart.get("overview") or {}
    for level_name, level in (("Maha", overview.get("current_maha_dasha")), ("Antar", overview.get("current_antar_dasha"))):
        planet = normalize_planet_name(level)
        if planet:
            facts.dasha_levels[planet].add(level_name)
            facts.keys.add(canonical_key("dasha_period", planet, level_name))

    dasha_layer = ((chart.get("layers") or {}).get("vimshottari_dasha") or {})
    for key, level_name in (("current_maha", "Maha"), ("current_antar", "Antar"), ("current_pratyantar", "Pratyantar")):
        payload = dasha_layer.get(key) or {}
        planet = normalize_planet_name(payload.get("planet"))
        if planet:
            facts.dasha_levels[planet].add(level_name)
            facts.keys.add(canonical_key("dasha_period", planet, level_name))


def _populate_aspect_facts(facts: ChartFacts) -> None:
    for planet, payload in facts.planet_positions.items():
        house = payload.get("house")
        if house is None:
            continue
        for target_house in _vedic_aspect_targets(planet, int(house)):
            facts.aspect_targets[planet].add(target_house)
            facts.aspected_by[target_house].add(planet)
            facts.keys.add(canonical_key("planet_aspect", planet, target_house))


def _vedic_aspect_targets(planet: str, house: int) -> set[int]:
    offsets = {7}
    if planet == "Mars":
        offsets.update({4, 8})
    elif planet == "Jupiter":
        offsets.update({5, 9})
    elif planet == "Saturn":
        offsets.update({3, 10})
    elif planet in {"Rahu", "Ketu"}:
        offsets.update({5, 9})
    return {((house - 1 + offset - 1) % 12) + 1 for offset in offsets}


def _condition_anchor_keys(condition: dict[str, Any]) -> set[str]:
    condition_type = condition.get("type")
    if condition_type == "planet_in_house":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("house"))}
    if condition_type == "planet_in_sign":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_sign_name(condition.get("sign")))}
    if condition_type == "planet_in_nakshatra":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_nakshatra_name(condition.get("nakshatra")))}
    if condition_type == "planet_aspect":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("aspecting_house"))}
    if condition_type == "planet_conjunction":
        planets = sorted_planet_list(condition.get("planets") or [])
        return {canonical_key(condition_type, *planets, condition.get("house"))}
    if condition_type == "planet_dignity":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), normalize_dignity(condition.get("dignity")))}
    if condition_type == "planet_retrograde":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), True)}
    if condition_type == "house_lord_in_house":
        return {canonical_key(condition_type, condition.get("source_house"), condition.get("target_house"))}
    if condition_type == "yoga":
        return {canonical_key(condition_type, condition.get("yoga_name"))}
    if condition_type == "dasha_period":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("dasha_lord")), condition.get("level"))}
    if condition_type == "kp_sublord":
        return {canonical_key(condition_type, condition.get("cusp_num"), normalize_planet_name(condition.get("sub_lord")))}
    if condition_type == "transit":
        return {canonical_key(condition_type, normalize_planet_name(condition.get("planet")), condition.get("transit_house"))}
    if condition_type == "composite":
        keys: set[str] = set()
        for sub in condition.get("sub_conditions") or []:
            keys.update(_condition_anchor_keys(sub))
        return keys
    return set()


def _condition_matches(condition: dict[str, Any], facts: ChartFacts) -> bool:
    condition_type = condition.get("type")
    if condition_type == "planet_in_house":
        planet = normalize_planet_name(condition.get("planet"))
        payload = facts.planet_positions.get(planet or "")
        if not payload or payload.get("house") != condition.get("house"):
            return False
        if condition.get("sign") and payload.get("sign") != normalize_sign_name(condition.get("sign")):
            return False
        if condition.get("dignity") and payload.get("dignity") != normalize_dignity(condition.get("dignity")):
            return False
        if condition.get("retrograde") is not None and bool(payload.get("retrograde")) != bool(condition.get("retrograde")):
            return False
        if condition.get("nakshatra") and payload.get("nakshatra") != normalize_nakshatra_name(condition.get("nakshatra")):
            return False
        if condition.get("conjunct_with"):
            partner = normalize_planet_name(condition.get("conjunct_with"))
            house_planets = facts.house_planets.get(int(condition.get("house") or 0), [])
            if partner not in house_planets:
                return False
        if condition.get("aspected_by"):
            aspected_by = normalize_planet_name(condition.get("aspected_by"))
            if aspected_by not in facts.aspected_by.get(int(condition.get("house") or 0), set()):
                return False
        if condition.get("dasha_active"):
            active = normalize_planet_name(condition.get("dasha_active"))
            if active not in facts.dasha_levels:
                return False
        return True
    if condition_type == "planet_in_sign":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("sign") == normalize_sign_name(condition.get("sign"))
    if condition_type == "planet_in_nakshatra":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("nakshatra") == normalize_nakshatra_name(condition.get("nakshatra"))
    if condition_type == "planet_aspect":
        planet = normalize_planet_name(condition.get("planet"))
        return int(condition.get("aspecting_house") or 0) in facts.aspect_targets.get(planet or "", set())
    if condition_type == "planet_conjunction":
        house = int(condition.get("house") or 0)
        expected = set(sorted_planet_list(condition.get("planets") or []))
        actual = set(facts.house_planets.get(house, []))
        return expected.issubset(actual)
    if condition_type == "planet_dignity":
        planet = normalize_planet_name(condition.get("planet"))
        return (facts.planet_positions.get(planet or "") or {}).get("dignity") == normalize_dignity(condition.get("dignity"))
    if condition_type == "planet_retrograde":
        planet = normalize_planet_name(condition.get("planet"))
        return bool((facts.planet_positions.get(planet or "") or {}).get("retrograde"))
    if condition_type == "house_lord_in_house":
        lord = facts.house_lords.get(int(condition.get("source_house") or 0))
        if not lord:
            return False
        return (facts.planet_positions.get(lord) or {}).get("house") == int(condition.get("target_house") or 0)
    if condition_type == "yoga":
        return str(condition.get("yoga_name")) in facts.yogas
    if condition_type == "dasha_period":
        planet = normalize_planet_name(condition.get("dasha_lord"))
        return str(condition.get("level")) in facts.dasha_levels.get(planet or "", set())
    if condition_type == "composite":
        sub_conditions = condition.get("sub_conditions") or []
        operator = str(condition.get("operator") or "and").lower()
        results = [_condition_matches(sub, facts) for sub in sub_conditions]
        return all(results) if operator == "and" else any(results)
    return False


def _modifier_factor(modifiers: list[Any], facts: ChartFacts) -> tuple[float, list[str]]:
    factor = 1.0
    applied: list[str] = []
    for modifier in modifiers:
        condition = getattr(modifier, "condition", None) or modifier.get("condition") or {}
        if not _condition_matches(condition, facts):
            continue
        effect = getattr(modifier, "effect", None) or modifier.get("effect") or ""
        applied.append(effect)
        factor *= MODIFIER_FACTORS.get(str(effect), 1.0)
    return factor, applied


def _backbone_adjusted_weight(science_id: str, backbone_science_id: str | None) -> float:
    base = SCIENCE_WEIGHTS.get(science_id, 0.10)
    if backbone_science_id and backbone_science_id != DEFAULT_BACKBONE and science_id == backbone_science_id:
        return base + 0.10
    return base


def _score_rule(rule: InterpretationRuleDocument, facts: ChartFacts, context: KnowledgeRequestContext) -> tuple[float, float, list[str]]:
    priority_factor = 0.50 + (rule.priority / 10.0)
    intensity = rule.intensity_score if rule.intensity_score > 0 else 1.0
    strength = STRENGTH_MULTIPLIERS.get(rule.strength_band, 0.85)
    science_weight = _backbone_adjusted_weight(rule.science_id, context.backbone_science_id)
    modifier_factor, applied_modifiers = _modifier_factor(rule.modifiers, facts)
    score = round(rule.weight * priority_factor * intensity * (1.0 + science_weight) * strength * modifier_factor, 6)
    effective_confidence = round(min(1.15, science_weight * strength), 4)
    return score, effective_confidence, applied_modifiers


class KnowledgeIndexStore:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self._snapshot = KnowledgeIndexSnapshot(
            built_at=utc_now(),
            rule_count=0,
            key_to_rule_ids={},
            rules_by_id={},
        )
        self._refresh_task: asyncio.Task[KnowledgeIndexSnapshot] | None = None

    @property
    def snapshot(self) -> KnowledgeIndexSnapshot:
        return self._snapshot

    @property
    def refresh_in_progress(self) -> bool:
        return self._refresh_task is not None and not self._refresh_task.done()

    async def refresh(self) -> KnowledgeIndexSnapshot:
        cursor = self.db[COLLECTION_INTERPRETATION_RULES].find(APPROVED_RULE_FILTER, {"_id": 0})
        raw_rules = await cursor.to_list(length=None)
        key_to_rule_ids: dict[str, set[str]] = defaultdict(set)
        rules_by_id: dict[str, IndexedRule] = {}

        for payload in raw_rules:
            try:
                rule = InterpretationRuleDocument(**payload)
            except Exception as exc:
                logger.warning("Skipping invalid knowledge rule during index refresh: %s", exc)
                continue
            anchor_keys = _condition_anchor_keys(rule.condition.model_dump(mode="python", exclude_none=True))
            indexed = IndexedRule(document=rule, anchor_keys=anchor_keys)
            rules_by_id[rule.rule_id] = indexed
            for key in anchor_keys:
                key_to_rule_ids[key].add(rule.rule_id)

        snapshot = KnowledgeIndexSnapshot(
            built_at=utc_now(),
            rule_count=len(rules_by_id),
            key_to_rule_ids=dict(key_to_rule_ids),
            rules_by_id=rules_by_id,
        )
        self._snapshot = snapshot
        logger.info("Knowledge index refreshed with %d approved active rules", snapshot.rule_count)
        return snapshot

    def schedule_refresh(self) -> asyncio.Task[KnowledgeIndexSnapshot]:
        if self.refresh_in_progress:
            return self._refresh_task  # type: ignore[return-value]
        self._refresh_task = asyncio.create_task(self.refresh())

        def _clear(task: asyncio.Task[KnowledgeIndexSnapshot]) -> None:
            if task.cancelled():
                logger.warning("Knowledge index refresh task cancelled")
            elif task.exception():
                logger.exception("Knowledge index refresh failed", exc_info=task.exception())
            self._refresh_task = None

        self._refresh_task.add_done_callback(_clear)
        return self._refresh_task

    def refresh_status(self) -> dict[str, Any]:
        return {
            "index_refreshed": not self.refresh_in_progress,
            "rule_count": self._snapshot.rule_count,
            "built_at": self._snapshot.built_at.isoformat(),
        }


class KnowledgeEngine:
    def __init__(self, db: AsyncIOMotorDatabase, index_store: KnowledgeIndexStore | None = None):
        self.db = db
        self.index_store = index_store or KnowledgeIndexStore(db)

    async def refresh_index(self) -> KnowledgeIndexSnapshot:
        return await self.index_store.refresh()

    def schedule_index_refresh(self) -> asyncio.Task[KnowledgeIndexSnapshot]:
        return self.index_store.schedule_refresh()

    def index_refresh_status(self) -> dict[str, Any]:
        return self.index_store.refresh_status()

    async def scan_chart(
        self,
        chart: dict[str, Any],
        categories: list[str] | None = None,
        max_rules: int = 50,
        context: dict[str, Any] | KnowledgeRequestContext | None = None,
    ) -> list[dict[str, Any]]:
        snapshot = self.index_store.snapshot
        facts = extract_chart_facts(chart)
        request_context = context if isinstance(context, KnowledgeRequestContext) else KnowledgeRequestContext(**(context or {}))

        candidate_rule_ids: set[str] = set()
        for key in facts.keys:
            candidate_rule_ids.update(snapshot.key_to_rule_ids.get(key, set()))

        requested_categories = set(categories or [])
        matches: list[dict[str, Any]] = []
        for rule_id in candidate_rule_ids:
            indexed_rule = snapshot.rules_by_id.get(rule_id)
            if indexed_rule is None:
                continue
            rule = indexed_rule.document
            if requested_categories and not requested_categories.intersection(rule.categories):
                continue
            if not _condition_matches(rule.condition.model_dump(mode="python", exclude_none=True), facts):
                continue
            score, effective_confidence, applied_modifiers = _score_rule(rule, facts, request_context)
            payload = rule.model_dump(mode="json", by_alias=True, exclude_none=True)
            payload.update(
                {
                    "score": score,
                    "effective_confidence": effective_confidence,
                    "backbone_science_id": request_context.backbone_science_id,
                    "applied_modifiers": applied_modifiers,
                    "matched_anchor_keys": sorted(indexed_rule.anchor_keys.intersection(facts.keys)),
                }
            )
            matches.append(payload)

        matches.sort(key=lambda item: (item["score"], item.get("priority", 0), item.get("effective_confidence", 0)), reverse=True)
        return matches[: max_rules]


_default_engine: KnowledgeEngine | None = None


async def configure_default_knowledge_engine(db: AsyncIOMotorDatabase) -> KnowledgeEngine:
    global _default_engine
    if _default_engine is None or _default_engine.db is not db:
        _default_engine = KnowledgeEngine(db)
    await _default_engine.refresh_index()
    return _default_engine


def get_default_knowledge_engine(db: AsyncIOMotorDatabase | None = None) -> KnowledgeEngine:
    global _default_engine
    if _default_engine is None:
        if db is None:
            raise RuntimeError("Knowledge engine is not configured")
        _default_engine = KnowledgeEngine(db)
    return _default_engine


async def scan_chart(
    chart: dict[str, Any],
    categories: list[str] | None = None,
    max_rules: int = 50,
    context: dict[str, Any] | KnowledgeRequestContext | None = None,
    db: AsyncIOMotorDatabase | None = None,
) -> list[dict[str, Any]]:
    engine = get_default_knowledge_engine(db)
    return await engine.scan_chart(chart=chart, categories=categories, max_rules=max_rules, context=context)
