from __future__ import annotations

import calendar
import re
from datetime import date, datetime, timedelta
from typing import Any

import swisseph as swe

try:
    from backend.auspicious_data import (
        ACTIVITY_VECTORS,
        CATEGORY_INTENT_PHRASES,
        CHINESE_ANIMALS,
        CHINESE_RULES,
        DAY_OFFICERS,
        HARD_BLOCK_OFFICERS,
        LUNAR_MANSIONS,
        RETROGRADE_SENSITIVE_CATEGORIES,
        SOLAR_MONTH_BRANCH_OFFSETS,
        VEDIC_RULES,
        ZODIAC_CLASHES,
    )
    from backend.panchang_router import (
        DEFAULT_LOCATIONS,
        KARANA_NAMES,
        LOCATION_LIST,
        NAKSHATRA_NAMES,
        TITHI_NAMES,
        YOGA_NAMES,
        _day_indexes,
        _day_quality_windows,
        _paksha_from_tithi,
    )
    from backend.vedic_shared_utils import build_transit_snapshot
except ImportError:  # pragma: no cover
    from auspicious_data import (  # type: ignore
        ACTIVITY_VECTORS,
        CATEGORY_INTENT_PHRASES,
        CHINESE_ANIMALS,
        CHINESE_RULES,
        DAY_OFFICERS,
        HARD_BLOCK_OFFICERS,
        LUNAR_MANSIONS,
        RETROGRADE_SENSITIVE_CATEGORIES,
        SOLAR_MONTH_BRANCH_OFFSETS,
        VEDIC_RULES,
        ZODIAC_CLASHES,
    )
    from panchang_router import (  # type: ignore
        DEFAULT_LOCATIONS,
        KARANA_NAMES,
        LOCATION_LIST,
        NAKSHATRA_NAMES,
        TITHI_NAMES,
        YOGA_NAMES,
        _day_indexes,
        _day_quality_windows,
        _paksha_from_tithi,
    )
    from vedic_shared_utils import build_transit_snapshot  # type: ignore


DAY_OFFICER_META = {item["slug"]: item["label"] for item in DAY_OFFICERS}
REFERENCE_DAY = date(1984, 2, 2)


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower()).strip("-")


def list_categories() -> list[dict[str, Any]]:
    items = []
    for slug, rule in VEDIC_RULES.items():
        vector = ACTIVITY_VECTORS[rule["default_activity_vector"]]
        items.append(
            {
                "slug": slug,
                "display_name": rule["display_name"],
                "default_activity_vector": rule["default_activity_vector"],
                "default_activity_vector_label": vector["display_name"],
                "risk_toggle_relevance": {
                    "avoid_retrogrades": slug in RETROGRADE_SENSITIVE_CATEGORIES,
                    "exclude_rahu_kalam": True,
                },
                "vedic": {
                    "vara_good": rule["vara_good"],
                    "vara_neutral": rule["vara_neutral"],
                    "tithi_good": rule["tithi_good"],
                    "tithi_neutral": rule["tithi_neutral"],
                    "tithi_blocked": rule["tithi_blocked"],
                    "nakshatra_good": rule["nakshatra_good"],
                    "yoga_blocked": rule["yoga_blocked"],
                },
                "chinese": CHINESE_RULES[slug],
            }
        )
    return items


def resolve_location(city_id: str) -> Any:
    normalized = _slugify(city_id)
    if not normalized:
        raise ValueError("city_id is required.")
    if city_id in DEFAULT_LOCATIONS:
        return DEFAULT_LOCATIONS[city_id]
    if normalized in DEFAULT_LOCATIONS:
        return DEFAULT_LOCATIONS[normalized]

    alias_hits = []
    for location in LOCATION_LIST:
        city_slug = _slugify(location.city_name or "")
        label_slug = _slugify(location.label or "")
        if normalized in {city_slug, label_slug}:
            alias_hits.append(location)
        elif location.slug.startswith(f"{normalized}-") or location.slug == normalized:
            alias_hits.append(location)

    if alias_hits:
        return sorted(alias_hits, key=lambda item: item.slug)[0]
    raise ValueError(f"Unsupported city_id '{city_id}'.")


def _sunday_first_vara(target_date: date) -> int:
    iso_value = target_date.isoweekday()
    return 1 if iso_value == 7 else iso_value + 1


def _clamp(score: int | float, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, int(round(score))))


def _format_time(iso_value: str | None) -> str | None:
    if not iso_value:
        return None
    try:
        return datetime.fromisoformat(iso_value).strftime("%H:%M")
    except ValueError:
        return iso_value[-8:-3]


def _extract_window(windows: list[Any], label: str) -> dict[str, str] | None:
    for window in windows:
        if getattr(window, "label", "") == label:
            return {
                "start": _format_time(getattr(window, "start", None)) or "--",
                "end": _format_time(getattr(window, "end", None)) or "--",
            }
    return None


def _windows_overlap(first: dict[str, str] | None, second: dict[str, str] | None) -> bool:
    if not first or not second:
        return False
    return not (first["end"] <= second["start"] or second["end"] <= first["start"])


def _mercury_retrograde(target_date: date, timezone_name: str) -> bool:
    snapshot = build_transit_snapshot(target_date, timezone_name, bodies=("Mercury",))
    return bool(snapshot["planets"]["Mercury"]["retrograde"])


def _base_chinese_context(target_date: date, birth_date: date | None) -> dict[str, Any]:
    day_delta = (target_date - REFERENCE_DAY).days
    month_offset = SOLAR_MONTH_BRANCH_OFFSETS[target_date.month]
    officer_slug = DAY_OFFICERS[(day_delta + month_offset) % 12]["slug"]
    day_animal = CHINESE_ANIMALS[day_delta % 12]
    user_animal = CHINESE_ANIMALS[(birth_date.year - 4) % 12] if birth_date else None
    clash_animal = ZODIAC_CLASHES.get(user_animal or "")
    return {
        "day_delta": day_delta,
        "officer_slug": officer_slug,
        "officer_label": f"{DAY_OFFICER_META[officer_slug]} ({officer_slug})",
        "day_animal": day_animal,
        "user_animal": user_animal,
        "is_personal_clash": bool(user_animal and clash_animal == day_animal),
        "lunar_mansion": LUNAR_MANSIONS[day_delta % len(LUNAR_MANSIONS)],
    }


def _vedic_score_for_day(
    target_date: date,
    location: Any,
    activity_category: str,
    avoid_retrogrades: bool,
    exclude_rahu_kalam: bool,
) -> dict[str, Any]:
    rules = VEDIC_RULES[activity_category]
    indexes, context = _day_indexes(target_date, location, "amanta")
    astro = context["astro"]
    windows = _day_quality_windows(astro.sunrise, astro.sunset, target_date.isoweekday(), astro.moon_longitude)

    tithi_num = indexes["tithi"] + 1
    nakshatra_num = indexes["nakshatra"] + 1
    yoga_num = indexes["yoga"] + 1
    karana_num = indexes["karana"] + 1
    vara_num = _sunday_first_vara(target_date)

    score = 40
    reasons: list[str] = []
    blockers: list[str] = []

    if vara_num in rules["vara_good"]:
        score += 20
        reasons.append(f"{target_date.strftime('%A')} supports this intent.")
    elif vara_num in rules["vara_neutral"]:
        score += 10

    if tithi_num in rules["tithi_good"]:
        score += 20
        reasons.append(f"{TITHI_NAMES[indexes['tithi']]} Tithi is favorable.")
    elif tithi_num in rules["tithi_neutral"]:
        score += 10

    if nakshatra_num in rules["nakshatra_good"]:
        score += 20
        reasons.append(f"{NAKSHATRA_NAMES[indexes['nakshatra']]} Nakshatra aligns well.")

    is_blocked = False
    if tithi_num in rules["tithi_blocked"]:
        score -= 30
        blockers.append(f"{TITHI_NAMES[indexes['tithi']]} is blocked for this category.")
        if activity_category not in {"litigation", "debt_clearance"}:
            is_blocked = True

    if yoga_num in rules["yoga_blocked"]:
        score -= 20
        blockers.append(f"{YOGA_NAMES[indexes['yoga']]} Yoga reduces strength.")

    karana_name = KARANA_NAMES[indexes["karana"]]
    if karana_name == "Vishti":
        blockers.append("Vishti (Bhadra) Karana is active as a soft blocker.")
        score -= 10

    rahu_kalam = _extract_window(windows, "Rahu Kaal")
    abhijit_muhurta = _extract_window(windows, "Abhijit Muhurta")

    if avoid_retrogrades and activity_category in RETROGRADE_SENSITIVE_CATEGORIES:
        if _mercury_retrograde(target_date, location.timezone):
            score -= 15
            blockers.append("Mercury retrograde filter is active on this date.")

    if exclude_rahu_kalam and _windows_overlap(abhijit_muhurta, rahu_kalam):
        score -= 12
        blockers.append("Abhijit Muhurta overlaps Rahu Kaal for this location.")

    return {
        "score": _clamp(score),
        "is_blocked": is_blocked,
        "blockers": blockers,
        "reasons": reasons,
        "details": {
            "tithi": tithi_num,
            "tithi_name": f"{_paksha_from_tithi(indexes['tithi'])} {TITHI_NAMES[indexes['tithi']]}",
            "nakshatra": nakshatra_num,
            "nakshatra_name": NAKSHATRA_NAMES[indexes["nakshatra"]],
            "vara": vara_num,
            "vara_name": target_date.strftime("%A"),
            "yoga": yoga_num,
            "yoga_name": YOGA_NAMES[indexes["yoga"]],
            "karana": karana_num,
            "karana_name": karana_name,
            "abhijit_muhurta": abhijit_muhurta,
            "rahu_kalam": rahu_kalam,
        },
    }


def _chinese_score_for_day(
    target_date: date,
    activity_category: str,
    birth_date: date | None,
    activity_vector: str | None,
    filter_personal_clash: bool,
) -> dict[str, Any]:
    rules = CHINESE_RULES[activity_category]
    vector_slug = activity_vector or rules["default_activity_vector"]
    vector_rules = ACTIVITY_VECTORS.get(vector_slug, ACTIVITY_VECTORS[rules["default_activity_vector"]])
    context = _base_chinese_context(target_date, birth_date)

    good_officers = set(rules["officer_good"]) | set(vector_rules["officer_good"])
    bad_officers = set(rules["officer_bad"]) | set(vector_rules["officer_bad"])

    score = 60
    blockers: list[str] = []
    reasons: list[str] = []
    officer_slug = context["officer_slug"]
    is_blocked = False

    if officer_slug in good_officers:
        score += 30
        reasons.append(f"{DAY_OFFICER_META[officer_slug]} day officer supports the action.")
    if officer_slug in bad_officers:
        score -= 35
        blockers.append(f"{DAY_OFFICER_META[officer_slug]} officer is adverse for this intent.")
        if officer_slug in HARD_BLOCK_OFFICERS:
            is_blocked = True

    if context["is_personal_clash"] and filter_personal_clash:
        score = 10
        is_blocked = True
        blockers.append("Personal zodiac clash shield blocked this date.")

    return {
        "score": _clamp(score),
        "is_blocked": is_blocked,
        "blockers": blockers,
        "reasons": reasons,
        "details": {
            "day_officer": context["officer_label"],
            "day_animal": context["day_animal"],
            "user_animal": context["user_animal"],
            "is_personal_clash": context["is_personal_clash"],
            "lunar_mansion": context["lunar_mansion"],
        },
    }


def _tier_for_score(unified_score: int, is_blocked: bool) -> str:
    if is_blocked or unified_score < 40:
        return "blocked"
    if unified_score >= 80:
        return "excellent"
    if unified_score >= 60:
        return "good"
    return "neutral"


def _recommendation(activity_category: str, tier: str, reasons: list[str]) -> str:
    phrase = CATEGORY_INTENT_PHRASES[activity_category]
    if tier == "blocked":
        lead = "Avoid major commitments on this date."
    elif tier == "excellent":
        lead = f"Highly auspicious for {phrase}."
    elif tier == "good":
        lead = f"A supportive date for {phrase}."
    else:
        lead = f"A workable but mixed date for {phrase}."

    if not reasons:
        return lead
    return f"{lead} {reasons[0]}"


def _inactive_vedic_details() -> dict[str, Any] | None:
    return None


def _inactive_chinese_details() -> dict[str, Any] | None:
    return None


def score_day(
    *,
    target_date: date,
    location: Any,
    activity_category: str,
    avoid_retrogrades: bool = False,
    exclude_rahu_kalam: bool = False,
    birth_date: date | None = None,
    activity_vector: str | None = None,
    filter_personal_clash: bool = True,
    system: str = "dual",
) -> dict[str, Any]:
    vedic_result = _vedic_score_for_day(
        target_date=target_date,
        location=location,
        activity_category=activity_category,
        avoid_retrogrades=avoid_retrogrades,
        exclude_rahu_kalam=exclude_rahu_kalam,
    )
    chinese_result = _chinese_score_for_day(
        target_date=target_date,
        activity_category=activity_category,
        birth_date=birth_date,
        activity_vector=activity_vector,
        filter_personal_clash=filter_personal_clash,
    )
    uses_vedic = system != "chinese"
    uses_chinese = system != "vedic"

    if system == "vedic":
        chinese_score = 0
        unified_score = vedic_result["score"]
        is_blocked = vedic_result["is_blocked"]
    elif system == "chinese":
        chinese_score = chinese_result["score"]
        vedic_result["score"] = 0
        unified_score = chinese_score
        is_blocked = chinese_result["is_blocked"]
    else:
        chinese_score = chinese_result["score"]
        unified_score = round((vedic_result["score"] * 0.55) + (chinese_score * 0.45))
        is_blocked = vedic_result["is_blocked"] or chinese_result["is_blocked"]

    blockers: list[str] = []
    reasons: list[str] = []
    if uses_vedic:
        blockers.extend(vedic_result["blockers"])
        reasons.extend(vedic_result["reasons"])
    if uses_chinese:
        blockers.extend(chinese_result["blockers"])
        reasons.extend(chinese_result["reasons"])
    tier = _tier_for_score(unified_score, is_blocked)

    return {
        "date": target_date.isoformat(),
        "day_name": target_date.strftime("%A"),
        "vedic_score": vedic_result["score"],
        "chinese_score": chinese_score,
        "unified_score": _clamp(unified_score),
        "tier": tier,
        "is_blocked": is_blocked,
        "blockers": blockers,
        "vedic_details": vedic_result["details"] if uses_vedic else _inactive_vedic_details(),
        "chinese_details": chinese_result["details"] if uses_chinese else _inactive_chinese_details(),
        "recommendation": _recommendation(activity_category, tier, reasons),
    }


def calculate_month(
    *,
    city_id: str,
    activity_category: str,
    target_month: date,
    avoid_retrogrades: bool = False,
    exclude_rahu_kalam: bool = False,
    birth_date: date | None = None,
    activity_vector: str | None = None,
    filter_personal_clash: bool = True,
    system: str = "dual",
) -> list[dict[str, Any]]:
    if activity_category not in VEDIC_RULES:
        raise ValueError(f"Unsupported activity_category '{activity_category}'.")
    location = resolve_location(city_id)
    month_start = target_month.replace(day=1)
    _, total_days = calendar.monthrange(month_start.year, month_start.month)
    return [
        score_day(
            target_date=month_start + timedelta(days=offset),
            location=location,
            activity_category=activity_category,
            avoid_retrogrades=avoid_retrogrades,
            exclude_rahu_kalam=exclude_rahu_kalam,
            birth_date=birth_date,
            activity_vector=activity_vector,
            filter_personal_clash=filter_personal_clash,
            system=system,
        )
        for offset in range(total_days)
    ]


def top_days(days: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    ranked = sorted(
        days,
        key=lambda item: (
            item["is_blocked"],
            -item["unified_score"],
            -item["vedic_score"],
            item["date"],
        ),
    )
    return ranked[: max(1, limit)]
