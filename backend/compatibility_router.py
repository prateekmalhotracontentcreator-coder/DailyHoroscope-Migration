from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from vedic_calculator import calculate_ashtakoot


router = APIRouter(prefix="/api/compatibility", tags=["compatibility"])

SIGN_SLUGS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]

SLUG_TO_SIGN = {
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

# Sign-level compatibility pages do not have birth-time data, so we aggregate
# the Ashta-Koota engine across the nakshatras that fall within each moon sign.
SIGN_NAKSHATRAS = {
    "Aries": ["Ashwini", "Bharani", "Krittika"],
    "Taurus": ["Krittika", "Rohini", "Mrigashira"],
    "Gemini": ["Mrigashira", "Ardra", "Punarvasu"],
    "Cancer": ["Punarvasu", "Pushya", "Ashlesha"],
    "Leo": ["Magha", "Purva Phalguni", "Uttara Phalguni"],
    "Virgo": ["Uttara Phalguni", "Hasta", "Chitra"],
    "Libra": ["Chitra", "Swati", "Vishakha"],
    "Scorpio": ["Vishakha", "Anuradha", "Jyeshtha"],
    "Sagittarius": ["Mula", "Purva Ashadha", "Uttara Ashadha"],
    "Capricorn": ["Uttara Ashadha", "Shravana", "Dhanishtha"],
    "Aquarius": ["Dhanishtha", "Shatabhisha", "Purva Bhadrapada"],
    "Pisces": ["Purva Bhadrapada", "Uttara Bhadrapada", "Revati"],
}

KOOTA_NAMES = {
    "varna": "Varna",
    "vashya": "Vashya",
    "tara": "Tara",
    "yoni": "Yoni",
    "graha_maitri": "Graha Maitri",
    "gana": "Gana",
    "bhakoot": "Bhakoot",
    "nadi": "Nadi",
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class KootaBreakdown(StrictModel):
    key: str
    name: str
    score: float
    max_score: float
    label: str
    meaning: str
    narrative: str


class CompatibilityResponse(StrictModel):
    sign1_slug: str
    sign2_slug: str
    sign1: str
    sign2: str
    sign_pair: str
    compatibility_score: float
    max_score: float = 36
    verdict: str
    band: str
    summary: str
    marriage_timing_note: str
    sample_size: int = Field(description="Number of nakshatra pairings aggregated for this sign pair.")
    kootas: list[KootaBreakdown]


def _score_label(score: float, max_score: float) -> str:
    ratio = score / max_score if max_score else 0
    if ratio >= 0.8:
        return "Strong"
    if ratio >= 0.55:
        return "Balanced"
    return "Sensitive"


def _compatibility_band(score: float) -> tuple[str, str]:
    if score >= 28:
        return "excellent", "Excellent Match"
    if score >= 24:
        return "very-good", "Very Good Match"
    if score >= 18:
        return "good", "Good Match"
    return "challenging", "Needs Deeper Chart Matching"


def _koota_narrative(name: str, meaning: str, score: float, max_score: float, sign1: str, sign2: str) -> str:
    ratio = score / max_score if max_score else 0
    if ratio >= 0.8:
        return f"{name} is a clear strength for {sign1} and {sign2}, supporting {meaning.lower()}."
    if ratio >= 0.55:
        return f"{name} is workable for {sign1} and {sign2}; the pairing shows support in {meaning.lower()} with some adjustment."
    return f"{name} needs more care for {sign1} and {sign2}, so {meaning.lower()} benefits from conscious effort and full-chart review."


def _build_summary(sign1: str, sign2: str, verdict: str, score: float) -> str:
    return (
        f"This {sign1}-{sign2} Gun Milan page uses averaged nakshatra combinations inside both moon signs. "
        f"The relationship trend lands at {score}/36, which points to a {verdict.lower()} at the sign level."
    )


def _build_timing_note(score: float, kootas: list[KootaBreakdown]) -> str:
    weaker = [item.name for item in kootas if item.score / item.max_score < 0.55]
    if score >= 28:
        return "Marriage timing generally improves when Venus, Jupiter, and the 7th-house periods are supportive in both full charts. This sign pairing starts from a strong baseline."
    if score >= 18:
        return "Marriage timing can work well when both charts show supportive dashas and transit backing. Use the full birth-chart report to check the exact window."
    if weaker:
        focus = ", ".join(weaker[:2])
        return f"This pairing benefits from full-chart timing before commitment, especially around {focus}. A personalised Gun Milan report is the right next step."
    return "This pairing benefits from full-chart timing before commitment. Use a personalised Gun Milan report to confirm the strongest marriage window."


def _canonical_pair(sign_pair: str) -> tuple[str, str, str]:
    parts = [part.strip().lower() for part in sign_pair.split("-and-")]
    if len(parts) != 2 or not all(part in SIGN_SLUGS for part in parts):
        raise HTTPException(status_code=404, detail="Compatibility pair not found")
    sign1_slug, sign2_slug = sorted(parts)
    return sign1_slug, sign2_slug, f"{sign1_slug}-and-{sign2_slug}"


@router.get("/{sign_pair}", response_model=CompatibilityResponse)
async def get_sign_compatibility(sign_pair: str) -> CompatibilityResponse:
    sign1_slug, sign2_slug, canonical_pair = _canonical_pair(sign_pair)
    sign1 = SLUG_TO_SIGN[sign1_slug]
    sign2 = SLUG_TO_SIGN[sign2_slug]
    nakshatras_1 = SIGN_NAKSHATRAS[sign1]
    nakshatras_2 = SIGN_NAKSHATRAS[sign2]

    aggregate_scores: dict[str, float] = {}
    koota_meta: dict[str, dict[str, str | float]] = {}
    total_score = 0.0
    sample_size = 0

    for nakshatra_1 in nakshatras_1:
        for nakshatra_2 in nakshatras_2:
            result = calculate_ashtakoot(nakshatra_1, sign1, nakshatra_2, sign2)
            sample_size += 1
            total_score += float(result.get("total_score", 0))
            for key, payload in result.get("kootas", {}).items():
                aggregate_scores[key] = aggregate_scores.get(key, 0.0) + float(payload.get("score", 0))
                if key not in koota_meta:
                    koota_meta[key] = {
                        "max_score": float(payload.get("max", 0)),
                        "meaning": str(payload.get("meaning", "")),
                    }

    compatibility_score = round(total_score / sample_size, 1) if sample_size else 0.0
    band, verdict = _compatibility_band(compatibility_score)

    kootas = []
    for key in KOOTA_NAMES:
        max_score = float(koota_meta.get(key, {}).get("max_score", 0))
        score = round(aggregate_scores.get(key, 0.0) / sample_size, 1) if sample_size else 0.0
        meaning = str(koota_meta.get(key, {}).get("meaning", "Compatibility analysis"))
        label = _score_label(score, max_score)
        kootas.append(
            KootaBreakdown(
                key=key,
                name=KOOTA_NAMES[key],
                score=score,
                max_score=max_score,
                label=label,
                meaning=meaning,
                narrative=_koota_narrative(KOOTA_NAMES[key], meaning, score, max_score, sign1, sign2),
            )
        )

    return CompatibilityResponse(
        sign1_slug=sign1_slug,
        sign2_slug=sign2_slug,
        sign1=sign1,
        sign2=sign2,
        sign_pair=canonical_pair,
        compatibility_score=compatibility_score,
        verdict=verdict,
        band=band,
        summary=_build_summary(sign1, sign2, verdict, compatibility_score),
        marriage_timing_note=_build_timing_note(compatibility_score, kootas),
        sample_size=sample_size,
        kootas=kootas,
    )
