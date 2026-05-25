from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from seo_m3_catalog import (
    CHART_POINT_META,
    FESTIVAL_META,
    HOUSES,
    HOUSE_META,
    PLANET_META,
    PLANET_NAME_MAP,
    REGION_META,
    SEEDED_FESTIVAL_DATES,
    SIGN_META,
    SIGN_NAME_MAP,
    SIGN_SLUGS,
)


INDIA_TZ = ZoneInfo("Asia/Kolkata")
HOUSE_TOPICS = [item["topic"] for item in HOUSES]
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


def ordinal(number: int) -> str:
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"


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


def _transit_sign_impacts(planet_slug: str, sign_slug: str) -> list[dict[str, str]]:
    impacts: list[dict[str, str]] = []
    for rising_slug in SIGN_SLUGS:
        house_number = _house_distance(rising_slug, sign_slug)
        house_topic = HOUSE_TOPICS[house_number - 1]
        impacts.append(
            {
                "sign_slug": rising_slug,
                "sign": SIGN_NAME_MAP[rising_slug],
                "activated_house": f"{ordinal(house_number)} house",
                "message": (
                    f"For {SIGN_NAME_MAP[rising_slug]} rising, this transit lights up {house_topic}. "
                    f"Expect {PLANET_NAME_MAP[planet_slug].lower()} lessons to arrive through that area first."
                ),
            }
        )
    return impacts


def _transit_faq(planet_slug: str, sign_slug: str) -> list[dict[str, str]]:
    planet = PLANET_NAME_MAP[planet_slug]
    sign = SIGN_NAME_MAP[sign_slug]
    return [
        {
            "question": f"How long does {planet} stay in {sign}?",
            "answer": f"The exact duration depends on the planet's speed and retrograde pattern. This page shows the current or next active window for {planet} in {sign}.",
        },
        {
            "question": f"Is {planet} in {sign} good or bad?",
            "answer": f"It is not purely good or bad. {planet} in {sign} has clear gifts, pressure points, and timing lessons that show up differently in each chart.",
        },
        {
            "question": f"What should I avoid during {planet} in {sign}?",
            "answer": "Avoid the transit's excess expression: impatience, overconfidence, scattered timing, or reacting before your chart context is clear.",
        },
        {
            "question": "Will this transit affect all 12 signs?",
            "answer": "Yes. Everyone feels the transit, but the house it activates depends on the rising sign and full natal chart.",
        },
        {
            "question": "How do I check my personal impact?",
            "answer": "Use your birth chart to see which house the transit activates, which natal grahas it aspects, and whether current dashas amplify it.",
        },
    ]


def build_transit_profile_doc(planet_slug: str, sign_slug: str) -> dict[str, Any]:
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
        "for_signs": _transit_sign_impacts(planet_slug, sign_slug),
        "faq": _transit_faq(planet_slug, sign_slug),
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


def _festival_summary(festival_slug: str, region_slug: str) -> str:
    festival = FESTIVAL_META[festival_slug]
    region = REGION_META[region_slug]
    zone_tone = {
        "south": "a warm, ritual-led rhythm",
        "north": "an open, high-energy community style",
        "east": "an artistic, devotional public mood",
        "west": "a bright, socially expressive festive tempo",
        "northeast": "a close-knit, community-first celebration style",
        "central": "a grounded, family-centred observance pattern",
        "diaspora": "a weekend-friendly diaspora community rhythm",
    }
    return (
        f"{festival['name']} in {region['name']} centres on {festival['season']}, expressed through {region['marker']} and the local instinct to celebrate together. "
        f"In {region['zone']} observance, families often gather around {region['food']}, giving {festival['name']} in {region['name']} {zone_tone.get(region['zone'], 'a distinct regional rhythm')} that feels unmistakably local."
    )


def _festival_faq(festival_slug: str, region_slug: str) -> list[dict[str, str]]:
    festival = FESTIVAL_META[festival_slug]["name"]
    region = REGION_META[region_slug]["name"]
    return [
        {
            "question": f"When is {festival} in {region}?",
            "answer": f"This page shows the current year's observed date for {festival} in {region}, along with local custom notes and puja context.",
        },
        {
            "question": f"Does {festival} look different in {region}?",
            "answer": "Yes. Ritual emphasis, food, naming, and community style often change from one region to another even when the festival date stays the same.",
        },
        {
            "question": f"Where can I check the auspicious timing for {festival}?",
            "answer": "Use the attached Panchang timing section to review sunrise, tithi, nakshatra, and the day's ritual mood before the main puja.",
        },
    ]


def build_festival_region_doc(festival_slug: str, region_slug: str) -> dict[str, Any]:
    festival_name = FESTIVAL_META[festival_slug]["name"]
    region_name = REGION_META[region_slug]["name"]
    current_year = datetime.now(INDIA_TZ).year
    return {
        "festival_slug": festival_slug,
        "region_slug": region_slug,
        "regional_name": _regional_name(festival_slug, region_slug),
        "summary": _festival_summary(festival_slug, region_slug),
        "traditions": _festival_traditions(festival_slug, region_slug),
        "celebration_steps": _festival_steps(festival_slug, region_slug),
        "did_you_know": _festival_fact(festival_slug, region_slug),
        "faq": _festival_faq(festival_slug, region_slug),
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


def build_character_placement_doc(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
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
