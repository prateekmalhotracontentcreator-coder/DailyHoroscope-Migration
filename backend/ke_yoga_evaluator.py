from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from knowledge_engine import ChartFacts


NATURAL_BENEFICS = {"Moon", "Mercury", "Venus", "Jupiter"}
NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
ANGULAR_HOUSES = {1, 4, 7, 10}
TRINAL_HOUSES = {1, 5, 9}
SEVEN_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
SIGN_QUALITY = {
    "movable": {"Aries", "Cancer", "Libra", "Capricorn"},
    "fixed": {"Taurus", "Leo", "Scorpio", "Aquarius"},
    "dual": {"Gemini", "Virgo", "Sagittarius", "Pisces"},
}
ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
EVEN_SIGNS = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}
NABHASA_QUALITY_MAP = {
    "Rajju Yoga": "movable",
    "Musala Yoga": "fixed",
    "Nala Yoga": "dual",
}
CH41_COMBINATIONS = {
    "Venus-Mars Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Capricorn", "Gemini"],
        "planets_in_houses": [("Venus", 5), ("Mars", 11)],
    },
    "Mercury-Jupiter-Moon-Mars Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Aquarius", "Taurus"],
        "planets_in_houses": [("Mercury", 5), ("Moon", 11), ("Mars", 11), ("Jupiter", 11)],
    },
    "Sun-Saturn-Moon-Jupiter Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Aries"],
        "planets_in_houses": [("Sun", 5), ("Saturn", 11), ("Moon", 11), ("Jupiter", 11)],
    },
    "Saturn-Sun-Moon Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Virgo", "Libra"],
        "planets_in_houses": [("Saturn", 5), ("Sun", 11), ("Moon", 11)],
    },
    "Jupiter-Mercury Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Leo", "Scorpio"],
        "planets_in_houses": [("Jupiter", 5), ("Mercury", 11)],
    },
    "Mars-Venus Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Cancer", "Sagittarius"],
        "planets_in_houses": [("Mars", 5), ("Venus", 11)],
    },
    "Moon-Saturn Wealth Axis - 5th/11th Own-Sign": {
        "ascendant_filter": ["Pisces"],
        "planets_in_houses": [("Moon", 5), ("Saturn", 11)],
    },
    "Sun Wealth Engine - Leo Ascendant Own-Sign": {
        "ascendant_filter": ["Leo"],
        "planets_in_houses": [("Sun", 1)],
        "activation_planets": ["Mars", "Jupiter"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Moon Wealth Engine - Cancer Ascendant Own-Sign": {
        "ascendant_filter": ["Cancer"],
        "planets_in_houses": [("Moon", 1)],
        "activation_planets": ["Mercury", "Jupiter"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Mars Wealth Engine - Aries/Scorpio Ascendant Own-Sign": {
        "ascendant_filter": ["Aries", "Scorpio"],
        "planets_in_houses": [("Mars", 1)],
        "activation_planets": ["Mercury", "Venus", "Saturn"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Mercury Wealth Engine - Gemini/Virgo Ascendant Own-Sign": {
        "ascendant_filter": ["Gemini", "Virgo"],
        "planets_in_houses": [("Mercury", 1)],
        "activation_planets": ["Saturn", "Jupiter"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Jupiter Wealth Engine - Sagittarius/Pisces Ascendant Own-Sign": {
        "ascendant_filter": ["Sagittarius", "Pisces"],
        "planets_in_houses": [("Jupiter", 1)],
        "activation_planets": ["Mercury", "Mars"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Venus Wealth Engine - Taurus/Libra Ascendant Own-Sign": {
        "ascendant_filter": ["Taurus", "Libra"],
        "planets_in_houses": [("Venus", 1)],
        "activation_planets": ["Saturn", "Mercury"],
        "activation_mode": "conjunction_or_aspect",
    },
    "Saturn Wealth Engine - Capricorn/Aquarius Ascendant Own-Sign": {
        "ascendant_filter": ["Capricorn", "Aquarius"],
        "planets_in_houses": [("Saturn", 1)],
        "activation_planets": ["Mars", "Jupiter"],
        "activation_mode": "conjunction_or_aspect",
    },
}
EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
}
DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
}
VIMSHOPAKA_TIERS = {
    2: "Parijatamsa",
    3: "Uttamamsa",
    4: "Gopuramsa",
    5: "Simhasanamsa",
    6: "Paravatamsa",
    7: "Devalokamsa",
    8: "Suralokamsa",
    9: "Iravatamsa",
    10: "Iravatamsa",
}
TIER_RANK = {
    "Parijatamsa": 1,
    "Uttamamsa": 2,
    "Gopuramsa": 3,
    "Simhasanamsa": 4,
    "Paravatamsa": 5,
    "Devalokamsa": 6,
    "Suralokamsa": 7,
    "Iravatamsa": 8,
}
TIER_ALIASES = {"Brahmalokamsa": "Suralokamsa"}
PLANET_ROLE_HOUSES = {
    "angular_lord": [10, 7, 4, 1],
    "fifth_lord": [5],
    "ninth_lord": [9],
}


@dataclass
class YogaCheckResult:
    matched: bool
    confidence: float
    evidence: list[str]
    yoga_check_type: str
    checkable: bool = True


def evaluate_yoga_check(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    yoga_check = _yoga_check_payload(condition)
    yoga_type = str(yoga_check.get("type") or "")
    if yoga_check.get("checkable") is False:
        return YogaCheckResult(
            matched=False,
            confidence=0.0,
            evidence=["Rule not yet checkable"],
            yoga_check_type=yoga_type,
            checkable=False,
        )
    evaluator = EVALUATOR_DISPATCH.get(yoga_type)
    if evaluator is None:
        return YogaCheckResult(False, 0.0, [f"Unsupported yoga_check type: {yoga_type or 'missing'}"], yoga_type)
    return evaluator(condition, facts)


def _yoga_check_payload(condition: dict[str, Any]) -> dict[str, Any]:
    payload = condition.get("yoga_check") or {}
    return payload if isinstance(payload, dict) else {}


def _result(yoga_type: str, matched: bool, evidence: list[str], confidence: float | None = None) -> YogaCheckResult:
    score = confidence if confidence is not None else (1.0 if matched else 0.0)
    return YogaCheckResult(matched=matched, confidence=round(max(0.0, min(1.0, score)), 4), evidence=evidence, yoga_check_type=yoga_type)


def _position(facts: ChartFacts, planet: str) -> dict[str, Any]:
    return facts.planet_positions.get(planet, {})


def _planet_house(facts: ChartFacts, planet: str) -> int | None:
    house = _position(facts, planet).get("house")
    return int(house) if house is not None else None


def _planet_sign(facts: ChartFacts, planet: str) -> str | None:
    sign = _position(facts, planet).get("sign")
    return str(sign) if sign else None


def _lagna_sign(facts: ChartFacts) -> str | None:
    return _planet_sign(facts, "Lagna")


def _to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _distinct_sign_count(facts: ChartFacts) -> int:
    return len({_planet_sign(facts, planet) for planet in SEVEN_PLANETS if _planet_sign(facts, planet)})


def _relative_house(house: int, reference_house: int) -> int:
    return ((house - reference_house + 12) % 12) + 1


def _target_house(reference_house: int, distance: int) -> int:
    return ((reference_house + distance - 2) % 12) + 1


def _resolve_reference_house(facts: ChartFacts, reference: str) -> int | None:
    if reference.lower() in {"lagna", "ascendant"}:
        return 1
    return _planet_house(facts, reference)


def _relative_targets(facts: ChartFacts, reference: str | None, houses: list[int]) -> set[int]:
    if not reference:
        return {int(house) for house in houses}
    ref_house = _resolve_reference_house(facts, reference)
    return set() if ref_house is None else {_target_house(ref_house, int(house)) for house in houses}


def _planets_for_type(planet_type: str) -> set[str]:
    if planet_type == "benefic":
        return NATURAL_BENEFICS
    if planet_type == "malefic":
        return NATURAL_MALEFICS
    return set()


def _houses_with_planet_type(facts: ChartFacts, planet_type: str) -> set[int]:
    planets = _planets_for_type(planet_type)
    return {house for house, occupants in facts.house_planets.items() if any(planet in planets for planet in occupants)}


def _candidate_planets(facts: ChartFacts, payload: dict[str, Any]) -> list[str]:
    planet = payload.get("planet")
    if isinstance(planet, str) and planet not in {"any_except_sun", "any_benefic"}:
        return [planet]
    if planet == "any_benefic":
        return [item for item in NATURAL_BENEFICS if item in facts.planet_positions]
    excluded = set(_to_list(payload.get("exclude_planets"))) | {"Lagna"}
    return [item for item in facts.planet_positions if item not in excluded and item != "Moon"]


def _normalize_ch41_name(name: str | None) -> str:
    return str(name or "").replace("—", "-").strip()


def _aspect_or_conjunction(facts: ChartFacts, planet: str, target_house: int) -> bool:
    house = _planet_house(facts, planet)
    if house is None:
        return False
    return house == target_house or target_house in facts.aspect_targets.get(planet, set())


def _benefic_support(facts: ChartFacts, house: int, primary_planet: str) -> bool:
    conjunction = set(facts.house_planets.get(house, [])) - {primary_planet}
    if conjunction & NATURAL_BENEFICS:
        return True
    return any(house in facts.aspect_targets.get(planet, set()) for planet in NATURAL_BENEFICS if planet != primary_planet)


def _no_malefic_pressure(facts: ChartFacts, houses: set[int]) -> bool:
    for house in houses:
        occupants = set(facts.house_planets.get(house, []))
        if occupants & NATURAL_MALEFICS:
            return False
        if set(facts.aspected_by.get(house, set())) & NATURAL_MALEFICS:
            return False
    return True


def _unsupported_note(payload: dict[str, Any], evidence: list[str]) -> None:
    if "free_from_combustion" in _to_list(payload.get("conditions")):
        evidence.append("Combustion is not exposed in ChartFacts; skipped")


def _reference_target_houses(facts: ChartFacts, references: list[str], distance: int) -> list[int]:
    targets: list[int] = []
    for reference in references:
        reference_house = _resolve_reference_house(facts, reference)
        if reference_house is not None:
            targets.append(_target_house(reference_house, distance))
    return targets


def _reference_distances(facts: ChartFacts, references: list[str], planet_house: int | None) -> list[int]:
    if planet_house is None:
        return []
    distances: list[int] = []
    for reference in references:
        reference_house = _resolve_reference_house(facts, reference)
        if reference_house is not None:
            distances.append(_relative_house(planet_house, reference_house))
    return distances


def _eval_planetary_combination(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _planetary_payload(condition)
    if not payload:
        return _result("planetary_combination", False, ["Parameters not yet structured for this yoga_name"])
    evidence, passed, total = [], 0, 0
    if payload.get("ascendant_filter"):
        total += 1
        lagna = _lagna_sign(facts)
        allowed = set(payload["ascendant_filter"])
        ok = lagna in allowed
        evidence.append(f"Lagna sign {lagna or 'missing'} {'matched' if ok else 'did not match'} {sorted(allowed)}")
        passed += int(ok)
    pairs = [(item["planet"], int(item["house"])) for item in payload.get("planets_in_houses", [])]
    for planet, house in pairs:
        total += 1
        actual = _planet_house(facts, planet)
        ok = actual == house
        evidence.append(f"{planet} in house {actual or 'missing'} {'matched' if ok else 'did not match'} required house {house}")
        passed += int(ok)
    primary_house = pairs[0][1] if pairs else None
    for planet in payload.get("activation_planets", []):
        total += 1
        ok = bool(primary_house and _aspect_or_conjunction(facts, planet, primary_house))
        evidence.append(f"{planet} {'activates' if ok else 'does not activate'} house {primary_house}")
        passed += int(ok)
    return _result("planetary_combination", passed == total and total > 0, evidence, passed / total if total else 0.0)


def _planetary_payload(condition: dict[str, Any]) -> dict[str, Any]:
    payload = dict(_yoga_check_payload(condition))
    if payload.get("planets_in_houses"):
        pairs = []
        for item in payload["planets_in_houses"]:
            if isinstance(item, dict):
                pairs.append({"planet": item.get("planet"), "house": item.get("house")})
        payload["planets_in_houses"] = pairs
        return payload
    fallback = CH41_COMBINATIONS.get(_normalize_ch41_name(condition.get("yoga_name")))
    if not fallback:
        return {}
    payload.update(fallback)
    payload["planets_in_houses"] = [{"planet": planet, "house": house} for planet, house in fallback.get("planets_in_houses", [])]
    return payload


def _canonical_tier(value: str | None) -> str | None:
    if not value:
        return None
    return TIER_ALIASES.get(value, value)


def _role_candidates(facts: ChartFacts, role: str) -> list[tuple[int, str]]:
    candidates: list[tuple[int, str]] = []
    for house in PLANET_ROLE_HOUSES.get(role, []):
        planet = facts.house_lords.get(house)
        if planet:
            candidates.append((house, planet))
    return candidates


def _tier_matches(actual_tier: str | None, required_tier: str | None) -> bool:
    actual_rank = TIER_RANK.get(_canonical_tier(actual_tier), 0)
    required_rank = TIER_RANK.get(_canonical_tier(required_tier), 0)
    return actual_rank >= required_rank > 0


def _eval_varga_dignity_tier(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    role = str(payload.get("planet_role") or "")
    required_tier = _canonical_tier(str(payload.get("required_tier") or ""))
    candidates = _role_candidates(facts, role)
    if not candidates:
        return _result("varga_dignity_tier", False, ["House lords not available in ChartFacts"])
    evidence, matched = [], False
    for house, planet in candidates:
        actual_tier = _canonical_tier((facts.varga_dignities.get(planet) or {}).get("tier"))
        ok = _tier_matches(actual_tier, required_tier)
        evidence.append(f"House {house} lord {planet}: tier {actual_tier or 'None'} vs required {required_tier or 'None'} -> {'matched' if ok else 'not matched'}")
        matched = matched or ok
    confidence = 1.0 if matched else 0.0
    return _result("varga_dignity_tier", matched, evidence, confidence)


def _eval_planet_in_house(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    planet = str(payload.get("planet") or "")
    houses = [int(item) for item in _to_list(payload.get("houses") or payload.get("house"))]
    actual_house = _planet_house(facts, planet)
    matched_house = actual_house in houses
    evidence = [f"{planet} is in house {actual_house or 'missing'}; required one of {houses}"]
    aspect_ok = all(actual_house in facts.aspect_targets.get(str(other), set()) for other in _to_list(payload.get("aspected_by"))) if actual_house else False
    sign_ok = not payload.get("sign") or _planet_sign(facts, planet) == payload.get("sign")
    matched = matched_house and sign_ok and (aspect_ok or not payload.get("aspected_by"))
    if payload.get("aspected_by"):
        evidence.append(f"Aspect requirements {'passed' if aspect_ok else 'failed'} for {list(payload.get('aspected_by') or [])}")
    if payload.get("sign"):
        evidence.append(f"Sign requirement {'passed' if sign_ok else 'failed'} for {payload.get('sign')}")
    confidence = sum(int(flag) for flag in [matched_house, sign_ok, aspect_ok or not payload.get("aspected_by")]) / 3.0
    return _result("planet_in_house", matched, evidence, confidence)


def _eval_multi_house_requirements(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    if payload.get("requirements"):
        checks = [(_planet_house(facts, str(item.get("planet") or "")) == int(item.get("house")), f"{item.get('planet')} in house {item.get('house')}") for item in payload.get("requirements", [])]
    else:
        checks = [(_house_requirement_matches(facts, item), _house_requirement_note(item)) for item in payload.get("house_requirements", [])]
    evidence = [f"{note}: {'passed' if ok else 'failed'}" for ok, note in checks]
    passed = sum(int(ok) for ok, _ in checks)
    return _result("multi_house_requirements", passed == len(checks) and bool(checks), evidence, passed / len(checks) if checks else 0.0)


def _house_requirement_matches(facts: ChartFacts, requirement: dict[str, Any]) -> bool:
    houses = [int(item) for item in requirement.get("houses", [])]
    planets = _planets_for_type(str(requirement.get("planet_type") or ""))
    occupants = {house: set(facts.house_planets.get(house, [])) for house in houses}
    if requirement.get("constraint") == "absent":
        return all(not (items & planets) for items in occupants.values())
    return all(items & planets for items in occupants.values())


def _house_requirement_note(requirement: dict[str, Any]) -> str:
    return f"{requirement.get('planet_type')} planets {requirement.get('constraint')} in houses {requirement.get('houses', [])}"


def _eval_benefics_in_houses(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    return _eval_planets_in_target_houses(_yoga_check_payload(condition), facts, "benefics_in_houses", NATURAL_BENEFICS)


def _eval_malefics_in_houses(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    return _eval_planets_in_target_houses(_yoga_check_payload(condition), facts, "malefics_in_houses", NATURAL_MALEFICS)


def _eval_planets_in_target_houses(payload: dict[str, Any], facts: ChartFacts, yoga_type: str, target_planets: set[str]) -> YogaCheckResult:
    targets = _relative_targets(facts, _reference_name(payload), [int(item) for item in payload.get("houses", [])])
    count = sum(1 for planet in target_planets if _planet_house(facts, planet) in targets)
    min_count = payload.get("minimum_count", payload.get("min_count"))
    max_count = payload.get("maximum_count")
    required = len(target_planets) if min_count is None and str(payload.get("operator") or "and").lower() != "or" else int(min_count or 1)
    matched = count >= required and (max_count is None or count <= int(max_count))
    evidence = [f"{count} target planets found in houses {sorted(targets)}; required at least {required}"]
    if payload.get("no_malefic_aspect") and targets:
        pressure_ok = _no_malefic_pressure(facts, {house for house in targets if set(facts.house_planets.get(house, [])) & target_planets})
        matched = matched and pressure_ok
        evidence.append(f"Malefic aspect/conjunction guard {'passed' if pressure_ok else 'failed'}")
    confidence = min(1.0, count / max(required, 1))
    return _result(yoga_type, matched, evidence, confidence)


def _reference_name(payload: dict[str, Any]) -> str | None:
    reference = payload.get("reference")
    if isinstance(reference, list):
        return None
    if reference in {"ascendant", "Ascendant"}:
        return "Lagna"
    return str(reference) if reference else None


def _eval_benefic_only_in_house(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    references = [item if item != "ascendant" else "Lagna" for item in _to_list(payload.get("reference") or "Lagna")]
    targets = _reference_target_houses(facts, references, int(payload.get("house", 10)))
    matches = []
    for house in targets:
        occupants = set(facts.house_planets.get(house, []))
        matches.append(any(planet in NATURAL_BENEFICS for planet in occupants) and not (occupants & NATURAL_MALEFICS))
    evidence = [f"House {house} occupants: {facts.house_planets.get(house, [])}" for house in targets]
    confidence = sum(int(item) for item in matches) / len(matches) if matches else 0.0
    return _result("benefic_only_in_house", any(matches), evidence, confidence)


def _eval_planet_in_kendra_from(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    planet = str(payload.get("planet") or "")
    planet_house = _planet_house(facts, planet)
    references = [item if item != "ascendant" else "Lagna" for item in _to_list(payload.get("reference") or "Lagna")]
    positions = [int(item) for item in _to_list(payload.get("positions") or payload.get("houses") or [1, 4, 7, 10])]
    distances = _reference_distances(facts, references, planet_house)
    matched = any(distance in positions for distance in distances)
    evidence = [f"Relative positions from {references}: {distances or ['missing']}"]
    matched = matched and _planet_in_kendra_conditions_ok(payload, facts, planet, planet_house, evidence)
    return _result("planet_in_kendra_from", matched, evidence, 1.0 if matched else 0.0)


def _planet_in_kendra_conditions_ok(payload: dict[str, Any], facts: ChartFacts, planet: str, planet_house: int | None, evidence: list[str]) -> bool:
    sign_ok = not payload.get("sign") or _planet_sign(facts, planet) == payload.get("sign")
    conds = set(_to_list(payload.get("conditions")))
    deb_ok = "free_from_debilitation" not in conds or _planet_sign(facts, planet) != DEBILITATION_SIGNS.get(planet)
    exalt_ok = "exalted_sign" not in conds or _planet_sign(facts, planet) == EXALTATION_SIGNS.get(planet)
    support_ok = "aspected_by_benefic" not in conds or bool(planet_house and _benefic_support(facts, planet_house, planet))
    _unsupported_note(payload, evidence)
    evidence.extend([
        f"Specific sign requirement {'passed' if sign_ok else 'failed'}",
        f"Debilitation guard {'passed' if deb_ok else 'failed'}",
        f"Exaltation requirement {'passed' if exalt_ok else 'failed'}",
        f"Benefic support {'passed' if support_ok else 'failed'}",
    ])
    return sign_ok and deb_ok and exalt_ok and support_ok


def _eval_sign_quality_all(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    quality = str(payload.get("quality") or payload.get("sign_quality") or NABHASA_QUALITY_MAP.get(condition.get("yoga_name"), ""))
    target = SIGN_QUALITY.get(quality, set())
    signs = {_planet_sign(facts, planet) for planet in SEVEN_PLANETS}
    matched = bool(target) and all(sign in target for sign in signs if sign)
    evidence = [f"All seven-planet signs {sorted(sign for sign in signs if sign)} compared with {quality or 'missing'} target"]
    return _result("sign_quality_all", matched, evidence)


def _eval_angles_by_planet_type(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    houses = {int(item) for item in payload.get("required_houses") or payload.get("houses") or ANGULAR_HOUSES}
    occupied = _houses_with_planet_type(facts, str(payload.get("planet_type") or ""))
    if payload.get("kendra_count") is not None:
        required = int(payload.get("kendra_count"))
        matched = len(occupied & houses) >= required
        evidence = [f"{len(occupied & houses)} angular houses occupied; required {required}"]
        return _result("angles_by_planet_type", matched, evidence, len(occupied & houses) / max(required, 1))
    requires_all = bool(payload.get("requires_all"))
    planets = _planets_for_type(str(payload.get("planet_type") or ""))
    matched = all(_planet_house(facts, planet) in houses for planet in planets) if requires_all else bool(occupied & houses)
    evidence = [f"Target houses occupied by {payload.get('planet_type')}: {sorted(occupied & houses)}"]
    return _result("angles_by_planet_type", matched, evidence)


def _eval_planets_in_n_signs(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    required = int(payload.get("n") or payload.get("sign_count") or 0)
    count = _distinct_sign_count(facts)
    return _result("planets_in_n_signs", count == required, [f"Distinct occupied signs: {count}; required {required}"], 1.0 if count == required else 0.0)


def _eval_all_planets_in_alt_signs(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    parity = str(payload.get("sign_parity") or payload.get("parity") or "")
    target = ODD_SIGNS if parity == "odd" else EVEN_SIGNS if parity == "even" else set()
    signs = [_planet_sign(facts, planet) for planet in SEVEN_PLANETS]
    matched = bool(target) and all(sign in target for sign in signs if sign)
    evidence = [f"Seven-planet signs: {[sign for sign in signs if sign]} against {parity or 'missing'} parity"]
    return _result("all_planets_in_alt_signs", matched, evidence)


def _eval_all_planets_in_houses(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    house_sets = payload.get("house_sets") or [payload.get("houses") or []]
    candidates = [{int(house) for house in item} for item in house_sets if item]
    occupied = {_planet_house(facts, planet) for planet in SEVEN_PLANETS}
    matched = any(all(house in candidate for house in occupied if house) for candidate in candidates)
    evidence = [f"Seven-planet houses: {sorted(house for house in occupied if house)} compared with {house_sets}"]
    return _result("all_planets_in_houses", matched, evidence)


def _eval_planet_in_house_from_moon(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    moon_house = _planet_house(facts, "Moon")
    target_houses = [int(item) for item in _to_list(payload.get("houses") or payload.get("house") or payload.get("distance_from_moon"))]
    if moon_house is None or not target_houses:
        return _result("planet_in_house_from_moon", False, ["Moon house or target house is missing"])
    candidates = _candidate_planets(facts, payload)
    operator = str(payload.get("operator") or "or").lower()
    present = {target: any(_relative_house(_planet_house(facts, planet), moon_house) == target for planet in candidates if _planet_house(facts, planet)) for target in target_houses}
    matched = all(present.values()) if operator == "and" else any(present.values())
    evidence = [f"Moon-relative houses satisfied: {present} with candidates {candidates}"]
    confidence = sum(int(flag) for flag in present.values()) / len(present)
    return _result("planet_in_house_from_moon", matched, evidence, confidence)


def _eval_kemadruma_check(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    moon_house = _planet_house(facts, "Moon")
    if moon_house is None:
        return _result("kemadruma_check", False, ["Moon house is missing"])
    occupants = set(facts.house_planets.get(moon_house, [])) - {"Moon", "Sun"}
    second_house, twelfth_house = _target_house(moon_house, 2), _target_house(moon_house, 12)
    second = set(facts.house_planets.get(second_house, [])) - {"Sun"}
    twelfth = set(facts.house_planets.get(twelfth_house, [])) - {"Sun"}
    angle_planets = {planet for house in ANGULAR_HOUSES for planet in facts.house_planets.get(house, [])}
    base_match = not occupants and not second and not twelfth
    strict_ok = moon_house not in ANGULAR_HOUSES if payload.get("strict") else True
    absent_ok = True if not payload.get("absent_conditions") else base_match and not angle_planets
    evidence = [f"Moon conjunction occupants: {sorted(occupants)}", f"2nd/12th from Moon occupants: {sorted(second)} / {sorted(twelfth)}", f"Angular-house occupants: {sorted(angle_planets)}"]
    return _result("kemadruma_check", base_match and strict_ok and absent_ok, evidence)


def _eval_moon_from_sun_position(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    sun_house, moon_house = _planet_house(facts, "Sun"), _planet_house(facts, "Moon")
    if sun_house is None or moon_house is None:
        return _result("moon_from_sun_position", False, ["Sun or Moon house is missing"])
    houses_from_sun = [int(item) for item in _to_list(payload.get("houses_from_sun") or payload.get("target_distances"))]
    if houses_from_sun:
        distance = _relative_house(moon_house, sun_house)
        matched = distance in houses_from_sun
        return _result("moon_from_sun_position", matched, [f"Moon is {distance} houses from Sun; targets {houses_from_sun}"])
    matched = _target_house(sun_house, int(payload.get("target_distances", [0])[0])) in facts.house_planets
    return _result("moon_from_sun_position", matched, ["Fallback Sun-reference occupancy check applied"])


def _eval_dosha(condition: dict[str, Any], facts: ChartFacts) -> YogaCheckResult:
    payload = _yoga_check_payload(condition)
    planet = str(payload.get("planet") or "")
    house = int(payload.get("house") or (_to_list(payload.get("houses")) or [0])[0])
    actual = _planet_house(facts, planet)
    return _result("dosha", actual == house, [f"{planet} is in house {actual or 'missing'}; required {house}"])


EVALUATOR_DISPATCH: dict[str, Callable[[dict[str, Any], ChartFacts], YogaCheckResult]] = {
    "planetary_combination": _eval_planetary_combination,
    "planet_in_house": _eval_planet_in_house,
    "multi_house_requirements": _eval_multi_house_requirements,
    "benefics_in_houses": _eval_benefics_in_houses,
    "malefics_in_houses": _eval_malefics_in_houses,
    "benefic_only_in_house": _eval_benefic_only_in_house,
    "planet_in_kendra_from": _eval_planet_in_kendra_from,
    "sign_quality_all": _eval_sign_quality_all,
    "angles_by_planet_type": _eval_angles_by_planet_type,
    "planets_in_n_signs": _eval_planets_in_n_signs,
    "all_planets_in_alt_signs": _eval_all_planets_in_alt_signs,
    "all_planets_in_houses": _eval_all_planets_in_houses,
    "planet_in_house_from_moon": _eval_planet_in_house_from_moon,
    "kemadruma_check": _eval_kemadruma_check,
    "moon_from_sun_position": _eval_moon_from_sun_position,
    "dosha": _eval_dosha,
    "varga_dignity_tier": _eval_varga_dignity_tier,
}
