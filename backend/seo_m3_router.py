from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from panchang_router import DEFAULT_LOCATIONS, _build_daily_response, _build_festival_list
from seo_m3_catalog import (
    CHART_POINT_META,
    ENGINE_FESTIVAL_ALIASES,
    ENGINE_FESTIVAL_SLUGS,
    FESTIVAL_META,
    FESTIVAL_SLUGS,
    HOUSE_META,
    HOUSES,
    PLANET_META,
    PLANET_NAME_MAP,
    PLANET_SLUGS,
    REGION_META,
    REGION_SLUGS,
    SEEDED_FESTIVAL_DATES,
    SIGN_META,
    SIGN_NAME_MAP,
    SIGN_SLUGS,
    ordinal,
)
from vedic_shared_utils import (
    build_transit_snapshot,
    dates_since_sign_entry,
    dates_until_sign_exit,
    next_sign_ingress,
)


router = APIRouter(prefix="/api/seo", tags=["seo-m3"])

SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
PLANET_CYCLE_DAYS = {
    "sun": 400,
    "moon": 60,
    "mars": 900,
    "mercury": 180,
    "jupiter": 5000,
    "venus": 400,
    "saturn": 12000,
    "rahu": 8000,
    "ketu": 8000,
}
HOUSE_TOPICS = [item["topic"] for item in HOUSES]
FESTIVAL_NEIGHBORS = {
    "diwali": ["dhanteras", "govardhan puja", "bhai dooj"],
    "holi": ["holika dahan", "rang panchami", "phalguna purnima"],
    "navratri": ["durga puja", "dussehra", "garba nights"],
    "durga-puja": ["navratri", "maha ashtami", "vijaya dashami"],
    "ganesh-chaturthi": ["ganesh visarjan", "modak offerings", "community aarti"],
    "janmashtami": ["nandotsav", "gokulashtami", "krishna jhulan"],
    "maha-shivaratri": ["pradosh vrat", "rudrabhishek", "night vigil puja"],
    "makar-sankranti": ["uttarayan", "kite festival", "til-gud offerings"],
    "pongal": ["bhogi", "mattu pongal", "kaanum pongal"],
    "onam": ["thiruvonam", "pookalam", "onasadya"],
    "baisakhi": ["harvest fairs", "gurdwara seva", "community dances"],
    "eid-ul-fitr": ["chaand raat", "eid namaz", "family dawat"],
    "christmas": ["midnight mass", "carol service", "family feast"],
    "gurupurab": ["nagar kirtan", "akhand path", "langar seva"],
    "ram-navami": ["sunderkand path", "kirtan", "temple jhanki"],
    "hanuman-jayanti": ["hanuman chalisa", "sindoor offering", "bhandara seva"],
}
TRANSIT_HOOK_TEMPLATES = {
    "sun": "This transit puts visibility, self-respect, and leadership choices under a brighter spotlight.",
    "moon": "This transit changes the emotional weather quickly, making instinct and comfort needs more obvious.",
    "mars": "This transit raises heat, courage, and urgency, so action starts to feel personal.",
    "mercury": "This transit reshapes thought patterns, messaging style, and the way timing decisions are made.",
    "jupiter": "This transit expands faith, growth, and possibility wherever it lands.",
    "venus": "This transit softens the atmosphere around attraction, beauty, money, and harmony.",
    "saturn": "This transit slows the tempo so structure, maturity, and long-term reality can catch up.",
    "rahu": "This transit amplifies hunger, experimentation, and the desire to break a familiar pattern.",
    "ketu": "This transit strips away noise and pushes a more inward, detached response to the sign's themes.",
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TransitWindow(StrictModel):
    active_now: bool
    start_date: str
    end_date: str
    next_occurrence_date: str | None = None
    days_elapsed: int | None = None
    days_remaining: int | None = None


class TransitSignImpact(StrictModel):
    sign_slug: str
    sign: str
    activated_house: str
    message: str


class FaqItem(StrictModel):
    question: str
    answer: str


class TransitProfileResponse(StrictModel):
    planet_slug: str
    sign_slug: str
    planet: str
    sign: str
    title: str
    summary: str
    year: int
    theme_phrase: str
    current_snapshot: dict[str, Any]
    transit_window: TransitWindow
    themes: list[str]
    watch_for: list[str]
    remedies: list[str]
    ritual: str
    for_signs: list[TransitSignImpact]
    faq: list[FaqItem]
    meta_title: str
    meta_description: str


class FestivalTiming(StrictModel):
    sunrise: str
    sunset: str
    tithi: str
    nakshatra: str
    note: str


class FestivalRegionResponse(StrictModel):
    festival_slug: str
    region_slug: str
    festival: str
    region: str
    year: int
    date: str
    date_source: str
    regional_name: str
    title: str
    summary: str
    traditions: list[str]
    celebration_steps: list[str]
    auspicious_timing: FestivalTiming | None = None
    did_you_know: str
    related_pages: list[dict[str, str]]
    faq: list[FaqItem]
    meta_title: str
    meta_description: str


class PlacementPerson(StrictModel):
    name: str
    note: str


class CharacterPlacementResponse(StrictModel):
    sign_slug: str
    chart_point_slug: str
    house_slug: str
    sign: str
    chart_point: str
    house: str
    house_number: int
    title: str
    summary: str
    core_traits: list[str]
    life_areas: list[str]
    strengths: list[str]
    shadow_side: list[str]
    compatible_placements: list[str]
    famous_people: list[PlacementPerson]
    vedic_perspective: list[str]
    faq: list[FaqItem]
    meta_title: str
    meta_description: str


def _get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        return None
    return db


def _safe_slug_label(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def _house_distance(from_sign_slug: str, target_sign_slug: str) -> int:
    start = SIGN_SLUGS.index(from_sign_slug)
    end = SIGN_SLUGS.index(target_sign_slug)
    return ((end - start) % 12) + 1


def _theme_phrase(planet_slug: str, sign_slug: str) -> str:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    return f"{planet_meta['theme']} meets {sign_meta['element'].lower()} {sign_meta['modality'].lower()} momentum"


def _transit_themes(planet_slug: str, sign_slug: str) -> list[str]:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    return [
        f"{PLANET_NAME_MAP[planet_slug]} channels {planet_meta['gift']} through {sign_meta['name']}'s {sign_meta['element'].lower()} style.",
        f"This cycle emphasises {planet_meta['theme']} with a {sign_meta['modality'].lower()} pace that rewards consistency over noise.",
        f"Leadership, timing, and confidence tend to move through {sign_meta['ruler']}-flavoured themes while this transit is active.",
        f"Career and public decisions benefit when you balance boldness with {sign_meta['element'].lower()} awareness.",
        f"Relationships can improve when the transit's appetite for {planet_meta['theme']} is expressed with patience instead of force.",
        f"Spiritual practice works best when it grounds the sign's instinctive response and channels it toward clean action.",
    ]


def _transit_watch_for(planet_slug: str, sign_slug: str) -> list[str]:
    sign_meta = SIGN_META[sign_slug]
    watch = PLANET_META[planet_slug]["watch"]
    return [
        f"Overdoing {watch} when {sign_meta['name']} wants immediate expression.",
        f"Taking temporary confidence swings as permanent truth.",
        f"Ignoring body signals or emotional pacing while chasing results too quickly.",
        f"Letting relationship friction build instead of naming expectations early.",
    ]


def _transit_remedies(planet_slug: str, sign_slug: str) -> tuple[list[str], str]:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    ritual = (
        f"Keep the remedy simple: lean into {planet_meta['remedy']}, and pair it with one weekly practice that steadies "
        f"{sign_meta['name']}'s {sign_meta['element'].lower()} response."
    )
    return (
        [
            f"Set one grounded weekly discipline connected to {PLANET_NAME_MAP[planet_slug]}'s transit lessons.",
            f"Use mantra or prayer around sunrise if you want the transit's clarity without the excess heat.",
            f"Choose timing carefully for big decisions and avoid acting only from the day's strongest mood.",
        ],
        ritual,
    )


def _transit_sign_impacts(planet_slug: str, sign_slug: str) -> list[TransitSignImpact]:
    impacts: list[TransitSignImpact] = []
    for rising_slug in SIGN_SLUGS:
        house_number = _house_distance(rising_slug, sign_slug)
        house_topic = HOUSE_TOPICS[house_number - 1]
        impacts.append(
            TransitSignImpact(
                sign_slug=rising_slug,
                sign=SIGN_NAME_MAP[rising_slug],
                activated_house=f"{ordinal(house_number)} house",
                message=(
                    f"For {SIGN_NAME_MAP[rising_slug]} rising, this transit lights up {house_topic}. "
                    f"Expect {PLANET_NAME_MAP[planet_slug].lower()} lessons to arrive through that area first."
                ),
            )
        )
    return impacts


def _transit_faq(planet_slug: str, sign_slug: str) -> list[FaqItem]:
    planet = PLANET_NAME_MAP[planet_slug]
    sign = SIGN_NAME_MAP[sign_slug]
    return [
        FaqItem(
            question=f"How long does {planet} stay in {sign}?",
            answer=f"The exact duration depends on the planet's speed and retrograde pattern. This page shows the current or next active window for {planet} in {sign}.",
        ),
        FaqItem(
            question=f"Is {planet} in {sign} good or bad?",
            answer=f"It is not purely good or bad. {planet} in {sign} has clear gifts, pressure points, and timing lessons that show up differently in each chart.",
        ),
        FaqItem(
            question=f"What should I avoid during {planet} in {sign}?",
            answer=f"Avoid the transit's excess expression: impatience, overconfidence, scattered timing, or reacting before your chart context is clear.",
        ),
        FaqItem(
            question=f"Will this transit affect all 12 signs?",
            answer="Yes. Everyone feels the transit, but the house it activates depends on the rising sign and full natal chart.",
        ),
        FaqItem(
            question=f"How do I check my personal impact?",
            answer="Use your birth chart to see which house the transit activates, which natal grahas it aspects, and whether current dashas amplify it.",
        ),
    ]


def _build_transit_profile_doc(planet_slug: str, sign_slug: str) -> dict[str, Any]:
    planet = PLANET_NAME_MAP[planet_slug]
    sign = SIGN_NAME_MAP[sign_slug]
    theme_phrase = _theme_phrase(planet_slug, sign_slug)
    remedies, ritual = _transit_remedies(planet_slug, sign_slug)
    return {
        "planet": planet_slug,
        "sign": sign_slug,
        "title": f"{planet} in {sign} - What It Means for You",
        "summary": f"{TRANSIT_HOOK_TEMPLATES[planet_slug]} In {sign}, the story becomes about {theme_phrase}.",
        "themes": _transit_themes(planet_slug, sign_slug),
        "watch_for": _transit_watch_for(planet_slug, sign_slug),
        "remedies": remedies,
        "ritual": ritual,
        "for_signs": [item.model_dump() for item in _transit_sign_impacts(planet_slug, sign_slug)],
        "faq": [item.model_dump() for item in _transit_faq(planet_slug, sign_slug)],
        "meta_title": f"{planet} in {sign} {datetime.now(INDIA_TZ).year} - Dates, Effects & Remedies",
        "meta_description": f"{planet} transits {sign} bringing {theme_phrase}. Dates, effects on all 12 signs, and Vedic remedies. Check your personal impact.",
        "theme_phrase": theme_phrase,
    }


def _regional_name(festival_slug: str, region_slug: str) -> str:
    festival = FESTIVAL_META[festival_slug]["name"]
    if festival_slug == "durga-puja" and region_slug == "west-bengal":
        return "Durga Pujo"
    if festival_slug == "navratri" and region_slug == "gujarat":
        return "Sharad Navratri"
    if festival_slug == "pongal" and region_slug == "tamil-nadu":
        return "Thai Pongal"
    if festival_slug == "diwali" and region_slug in {"tamil-nadu", "kerala"}:
        return "Deepavali"
    if festival_slug == "gurupurab" and region_slug == "punjab":
        return "Gurpurab"
    return festival


def _festival_traditions(festival_slug: str, region_slug: str) -> list[str]:
    festival = FESTIVAL_META[festival_slug]
    region = REGION_META[region_slug]
    return [
        f"In {region['name']}, {festival['name']} is often marked with {region['marker']}.",
        f"Households commonly prepare {region['food']} as part of the celebration mood.",
        f"Families blend the festival's {festival['season']} energy with local community customs and temple visits.",
        f"Neighbourhood greetings often reflect {region['zone']}-region style: warm, community-led, and highly family-oriented.",
        f"Many people plan the main puja around the day's cleanest ritual window rather than rushing the celebration.",
    ]


def _festival_steps(festival_slug: str, region_slug: str) -> list[str]:
    festival = FESTIVAL_META[festival_slug]["name"]
    region = REGION_META[region_slug]
    return [
        f"Begin the {festival} day with cleaning, simple prayer, and preparation of the home altar.",
        f"Bring in local flavour with {region['food']} and region-specific decorations before the main ritual hour.",
        f"Offer the core puja or prayer sequence, then share food, greetings, and visits with family or community.",
        f"Close the day with gratitude, lights, music, or a quiet reflection depending on the festival mood.",
    ]


def _festival_fact(festival_slug: str, region_slug: str) -> str:
    region = REGION_META[region_slug]
    festival = FESTIVAL_META[festival_slug]
    return (
        f"{festival['name']} in {region['name']} often stands out because local celebration style reflects the region's "
        f"{region['zone']} cultural rhythm rather than a single all-India template."
    )


def _festival_related(festival_slug: str, region_slug: str, festival_date: str) -> list[dict[str, str]]:
    related = [
        {
            "label": item.title(),
            "href": f"{SITE_URL}/panchang/{REGION_META[region_slug]['location_slug']}/{festival_date}",
        }
        for item in FESTIVAL_NEIGHBORS.get(festival_slug, [])[:1]
    ]
    for neighbor in [item for item in FESTIVAL_SLUGS if item != festival_slug][:2]:
        related.append(
            {
                "label": f"{FESTIVAL_META[neighbor]['name']} in {REGION_META[region_slug]['name']}",
                "href": f"{SITE_URL}/festivals/{neighbor}/{region_slug}",
            }
        )
    return related


def _festival_faq(festival_slug: str, region_slug: str) -> list[FaqItem]:
    festival = FESTIVAL_META[festival_slug]["name"]
    region = REGION_META[region_slug]["name"]
    return [
        FaqItem(
            question=f"When is {festival} in {region}?",
            answer=f"This page shows the current year's observed date for {festival} in {region}, along with local custom notes and puja context.",
        ),
        FaqItem(
            question=f"Does {festival} look different in {region}?",
            answer=f"Yes. Ritual emphasis, food, naming, and community style often change from one region to another even when the festival date stays the same.",
        ),
        FaqItem(
            question=f"Where can I check the auspicious timing for {festival}?",
            answer="Use the attached Panchang timing section to review sunrise, tithi, nakshatra, and the day's ritual mood before the main puja.",
        ),
    ]


def _build_festival_region_doc(festival_slug: str, region_slug: str) -> dict[str, Any]:
    festival_name = FESTIVAL_META[festival_slug]["name"]
    region_name = REGION_META[region_slug]["name"]
    current_year = datetime.now(INDIA_TZ).year
    return {
        "festival_slug": festival_slug,
        "region_slug": region_slug,
        "regional_name": _regional_name(festival_slug, region_slug),
        "summary": (
            f"{festival_name} in {region_name} brings together local ritual timing, family tradition, and community celebration. "
            f"This page focuses on date, customs, food, and how the region typically gives the festival its own voice."
        ),
        "traditions": _festival_traditions(festival_slug, region_slug),
        "celebration_steps": _festival_steps(festival_slug, region_slug),
        "did_you_know": _festival_fact(festival_slug, region_slug),
        "faq": [item.model_dump() for item in _festival_faq(festival_slug, region_slug)],
        "meta_title": f"{festival_name} in {region_name} {current_year} - Date, Traditions & Celebrations",
        "meta_description": f"See when {festival_name} is celebrated in {region_name}, plus local traditions, customs, and auspicious timing for the day.",
        "dates_by_year": SEEDED_FESTIVAL_DATES.get(festival_slug, {}),
    }


def _placement_traits(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
    sign = SIGN_META[sign_slug]
    chart_point = CHART_POINT_META[chart_point_slug]
    house = HOUSE_META[house_slug]
    summary = (
        f"{sign['name']} {chart_point['name']} in the {house['label']} blends {chart_point['lens']} with themes of {house['topic']}. "
        f"The result is a placement that expresses itself through {sign['element'].lower()} instinct and {sign['modality'].lower()} pacing."
    )
    return {
        "summary": summary,
        "core_traits": [
            f"Expresses {chart_point['lens']} with a distinctly {sign['name']} tone.",
            f"Naturally notices life through the filter of {house['topic']}.",
            f"Carries {sign['element'].lower()} intuition into choices about {house['label'].lower()}.",
            f"Tends to move with a {sign['modality'].lower()} rhythm when this part of life is activated.",
            f"Feels more confident when the ruling planet {sign['ruler']} is supported in the chart.",
        ],
        "life_areas": [
            f"{house['label']} matters become a major stage for identity and decision-making.",
            f"The person often learns important lessons through {house['topic']}.",
            f"This placement colours both personality style and the timing of growth in this house.",
        ],
        "strengths": [
            f"Strong instinct for handling {house['topic']}.",
            f"Can bring {sign['ruler']}-style intelligence to practical life choices.",
            f"Often memorable because the {chart_point['name']} expresses itself clearly in public or close relationships.",
        ],
        "shadow_side": [
            f"May over-identify with challenges linked to {house['topic']}.",
            f"When stressed, the {sign['name']} style can become too fixed or defensive in this area.",
            f"Needs conscious grounding so this placement does not turn one life theme into the whole story.",
        ],
        "compatible_placements": [
            f"People with supportive {sign['element'].lower()} or complementary air/fire-water/earth placements often understand this style more easily.",
            f"Moon or rising signs that stabilise the {house['label'].lower()} topic can feel especially helpful.",
            f"Balanced Venus and Jupiter placements often soften the sharper edges of this combination.",
        ],
        "famous_people": [],
        "vedic_perspective": [
            f"In Vedic reading, the {chart_point['name']} shows how consciousness or temperament expresses itself through the house of {house['topic']}.",
            f"{sign['name']} adds the behaviour of its ruler, element, and modality to that result.",
            f"Strength, aspects, dashas, and dignity of {sign['ruler']} refine whether the placement feels easy, intense, or delayed.",
        ],
        "faq": [
            {
                "question": f"What does {sign['name']} {chart_point['name']} in the {house['label']} mean?",
                "answer": summary,
            },
            {
                "question": "Is this placement good or difficult?",
                "answer": "It depends on chart support. Every placement has strengths and shadows that become clearer through dignity, aspects, and dasha timing.",
            },
            {
                "question": "How do I confirm if this is my placement?",
                "answer": "Run your birth chart with accurate birth time. Rising and house placements especially depend on exact time and location.",
            },
        ],
    }


def _build_character_placement_doc(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
    sign = SIGN_NAME_MAP[sign_slug]
    chart_point = CHART_POINT_META[chart_point_slug]["name"]
    house = HOUSE_META[house_slug]
    traits = _placement_traits(sign_slug, chart_point_slug, house_slug)
    return {
        "sign_slug": sign_slug,
        "chart_point_slug": chart_point_slug,
        "house_slug": house_slug,
        "title": f"{sign} {chart_point} in the {house['label']} - Personality & Life Themes",
        **traits,
        "meta_title": f"{sign} {chart_point} in the {house['label']} - Personality & Life Themes",
        "meta_description": f"Explore {sign} {chart_point} in the {house['label']}: traits, strengths, shadow side, and Vedic interpretation.",
    }


def build_transit_profile_doc(planet_slug: str, sign_slug: str) -> dict[str, Any]:
    return _build_transit_profile_doc(planet_slug, sign_slug)


def build_festival_region_doc(festival_slug: str, region_slug: str) -> dict[str, Any]:
    return _build_festival_region_doc(festival_slug, region_slug)


def build_character_placement_doc(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
    return _build_character_placement_doc(sign_slug, chart_point_slug, house_slug)


async def _fetch_doc(db, collection_name: str, query: dict[str, Any]) -> dict[str, Any] | None:
    if db is None:
        return None
    return await db[collection_name].find_one(query, {"_id": 0})


def _parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def _festival_date_from_engine(festival_slug: str, region_slug: str, year: int) -> str | None:
    region_location = DEFAULT_LOCATIONS.get(REGION_META[region_slug]["location_slug"]) or DEFAULT_LOCATIONS["new-delhi-india"]
    engine_slug = ENGINE_FESTIVAL_ALIASES.get(festival_slug, festival_slug)
    response = _build_festival_list(year, region_location, None, "amanta", "general")
    for item in response.items:
        if item.slug == engine_slug:
            return item.date
    return None


def _festival_timing(festival_date: str, region_slug: str) -> FestivalTiming | None:
    location = DEFAULT_LOCATIONS.get(REGION_META[region_slug]["location_slug"]) or DEFAULT_LOCATIONS["new-delhi-india"]
    daily = _build_daily_response(_parse_iso_date(festival_date), location, "amanta", "general")
    return FestivalTiming(
        sunrise=daily.summary.sunrise,
        sunset=daily.summary.sunset,
        tithi=daily.summary.tithi,
        nakshatra=daily.summary.nakshatra,
        note=f"Use the day's cleanest puja window after sunrise and align key rituals with local temple or family tradition.",
    )


@router.get("/transit/{planet_slug}/{sign_slug}", response_model=TransitProfileResponse)
async def get_transit_profile(planet_slug: str, sign_slug: str, request: Request) -> TransitProfileResponse:
    if planet_slug not in PLANET_SLUGS or sign_slug not in SIGN_SLUGS:
        raise HTTPException(status_code=404, detail="Transit profile not found")

    db = _get_db(request)
    doc = await _fetch_doc(db, "transit_profiles", {"planet": planet_slug, "sign": sign_slug})
    payload = {**_build_transit_profile_doc(planet_slug, sign_slug), **(doc or {})}

    body = PLANET_NAME_MAP[planet_slug]
    sign_name = SIGN_NAME_MAP[sign_slug]
    today = datetime.now(INDIA_TZ).date()
    snapshot = build_transit_snapshot(today, "Asia/Kolkata", bodies=(body,))
    current_sign = snapshot["planets"][body]["sign"]
    active_now = current_sign == sign_name

    if active_now:
        start_date = dates_since_sign_entry(body, today, "Asia/Kolkata", sign_name, max_days=PLANET_CYCLE_DAYS[planet_slug])
        end_date = dates_until_sign_exit(body, today, "Asia/Kolkata", sign_name, max_days=PLANET_CYCLE_DAYS[planet_slug])
        next_ingress = next_sign_ingress(
            body,
            _parse_iso_date(end_date) + timedelta(days=1),
            "Asia/Kolkata",
            sign_name,
            max_days=PLANET_CYCLE_DAYS[planet_slug],
        )
        days_elapsed = (today - _parse_iso_date(start_date)).days
        days_remaining = (_parse_iso_date(end_date) - today).days
    else:
        next_ingress = next_sign_ingress(
            body,
            today,
            "Asia/Kolkata",
            sign_name,
            max_days=PLANET_CYCLE_DAYS[planet_slug],
        )
        if next_ingress is None:
            raise HTTPException(status_code=500, detail="Unable to calculate transit window")
        start_date = str(next_ingress["date"])
        end_date = dates_until_sign_exit(
            body,
            _parse_iso_date(start_date),
            "Asia/Kolkata",
            sign_name,
            max_days=PLANET_CYCLE_DAYS[planet_slug],
        )
        days_elapsed = None
        days_remaining = (_parse_iso_date(start_date) - today).days

    return TransitProfileResponse(
        planet_slug=planet_slug,
        sign_slug=sign_slug,
        planet=body,
        sign=sign_name,
        title=payload["title"],
        summary=payload["summary"],
        year=today.year,
        theme_phrase=payload["theme_phrase"],
        current_snapshot=snapshot["planets"][body],
        transit_window=TransitWindow(
            active_now=active_now,
            start_date=start_date,
            end_date=end_date,
            next_occurrence_date=None if active_now else start_date,
            days_elapsed=days_elapsed,
            days_remaining=days_remaining,
        ),
        themes=list(payload["themes"]),
        watch_for=list(payload["watch_for"]),
        remedies=list(payload["remedies"]),
        ritual=str(payload["ritual"]),
        for_signs=[TransitSignImpact(**item) for item in payload["for_signs"]],
        faq=[FaqItem(**item) for item in payload["faq"]],
        meta_title=str(payload["meta_title"]),
        meta_description=str(payload["meta_description"]),
    )


@router.get("/festivals/{festival_slug}/{region_slug}", response_model=FestivalRegionResponse)
async def get_festival_region_page(festival_slug: str, region_slug: str, request: Request) -> FestivalRegionResponse:
    if festival_slug not in FESTIVAL_SLUGS or region_slug not in REGION_SLUGS:
        raise HTTPException(status_code=404, detail="Festival region page not found")

    db = _get_db(request)
    doc = await _fetch_doc(db, "festival_region_pages", {"festival_slug": festival_slug, "region_slug": region_slug})
    payload = {**_build_festival_region_doc(festival_slug, region_slug), **(doc or {})}
    current_year = datetime.now(INDIA_TZ).year

    if festival_slug in ENGINE_FESTIVAL_SLUGS:
        festival_date = _festival_date_from_engine(festival_slug, region_slug, current_year)
        date_source = "panchang-engine"
    else:
        dates_by_year = payload.get("dates_by_year") or SEEDED_FESTIVAL_DATES.get(festival_slug, {})
        festival_date = dates_by_year.get(str(current_year))
        date_source = "seeded-calendar"

    if not festival_date:
        raise HTTPException(status_code=404, detail="Festival date unavailable for this year")

    return FestivalRegionResponse(
        festival_slug=festival_slug,
        region_slug=region_slug,
        festival=FESTIVAL_META[festival_slug]["name"],
        region=REGION_META[region_slug]["name"],
        year=current_year,
        date=festival_date,
        date_source=date_source,
        regional_name=str(payload["regional_name"]),
        title=f"{FESTIVAL_META[festival_slug]['name']} in {REGION_META[region_slug]['name']} {current_year} - Date, Traditions & Celebrations",
        summary=str(payload["summary"]),
        traditions=list(payload["traditions"]),
        celebration_steps=list(payload["celebration_steps"]),
        auspicious_timing=_festival_timing(festival_date, region_slug),
        did_you_know=str(payload["did_you_know"]),
        related_pages=_festival_related(festival_slug, region_slug, festival_date),
        faq=[FaqItem(**item) for item in payload["faq"]],
        meta_title=str(payload["meta_title"]),
        meta_description=str(payload["meta_description"]),
    )


@router.get("/traits/{sign_slug}/{chart_point_slug}/{house_slug}", response_model=CharacterPlacementResponse)
async def get_character_placement(sign_slug: str, chart_point_slug: str, house_slug: str, request: Request) -> CharacterPlacementResponse:
    if sign_slug not in SIGN_SLUGS or chart_point_slug not in CHART_POINT_META or house_slug not in HOUSE_META:
        raise HTTPException(status_code=404, detail="Character placement page not found")

    db = _get_db(request)
    doc = await _fetch_doc(
        db,
        "character_placements",
        {"sign_slug": sign_slug, "chart_point_slug": chart_point_slug, "house_slug": house_slug},
    )
    payload = {**_build_character_placement_doc(sign_slug, chart_point_slug, house_slug), **(doc or {})}
    house = HOUSE_META[house_slug]

    return CharacterPlacementResponse(
        sign_slug=sign_slug,
        chart_point_slug=chart_point_slug,
        house_slug=house_slug,
        sign=SIGN_NAME_MAP[sign_slug],
        chart_point=CHART_POINT_META[chart_point_slug]["name"],
        house=house["label"],
        house_number=int(house["number"]),
        title=str(payload["title"]),
        summary=str(payload["summary"]),
        core_traits=list(payload["core_traits"]),
        life_areas=list(payload["life_areas"]),
        strengths=list(payload["strengths"]),
        shadow_side=list(payload["shadow_side"]),
        compatible_placements=list(payload["compatible_placements"]),
        famous_people=[PlacementPerson(**item) for item in payload.get("famous_people", [])],
        vedic_perspective=list(payload["vedic_perspective"]),
        faq=[FaqItem(**item) for item in payload["faq"]],
        meta_title=str(payload["meta_title"]),
        meta_description=str(payload["meta_description"]),
    )
