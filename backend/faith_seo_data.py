from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from zoneinfo import ZoneInfo

from faith_bible_data import (
    get_bible_hub_payload as get_live_bible_hub_payload,
    get_bible_page_count,
    get_bible_sitemap_urls,
)
from faith_gita_data import (
    get_gita_hub_payload as get_live_gita_hub_payload,
    get_gita_page_count,
    get_gita_sitemap_urls,
)
from lumina_prompt_service import DAILY_SCRIPTURES

SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
DEFAULT_PANCHANG_CITY = "new-delhi-india"
FAITH_PATHWAY_SLUGS = [
    "anxiety-reset",
    "career-reset",
    "relationship-healing",
    "grief-and-comfort",
    "fresh-start",
    "mercury-retrograde-faith",
]

SIGNS = [
    {
        "slug": "aries",
        "name": "Aries",
        "element": "Fire",
        "ruler": "Mars",
        "seasonal_focus": "courage without emotional overreaction",
        "growth_edge": "act from conviction instead of pressure",
        "daily_practice": "Begin the day with a spoken intention before you reach for urgency.",
    },
    {
        "slug": "taurus",
        "name": "Taurus",
        "element": "Earth",
        "ruler": "Venus",
        "seasonal_focus": "steady devotion and patient rebuilding",
        "growth_edge": "release comfort that has become stagnation",
        "daily_practice": "Give ten uninterrupted minutes to prayer, chanting, or breath before the world enters your nervous system.",
    },
    {
        "slug": "gemini",
        "name": "Gemini",
        "element": "Air",
        "ruler": "Mercury",
        "seasonal_focus": "clear speech and disciplined thought",
        "growth_edge": "stop scattering attention across too many voices",
        "daily_practice": "Write one grounding sentence you will return to whenever the mind starts splitting into too many directions.",
    },
    {
        "slug": "cancer",
        "name": "Cancer",
        "element": "Water",
        "ruler": "Moon",
        "seasonal_focus": "emotional shelter and spiritual nourishment",
        "growth_edge": "care without disappearing into everyone else's weather",
        "daily_practice": "Create one protective ritual around your home, altar, or evening wind-down.",
    },
    {
        "slug": "leo",
        "name": "Leo",
        "element": "Fire",
        "ruler": "Sun",
        "seasonal_focus": "purpose, dignity, and heart-led leadership",
        "growth_edge": "lead without making every challenge about pride",
        "daily_practice": "Offer one act of visible generosity that strengthens someone else instead of feeding performance.",
    },
    {
        "slug": "virgo",
        "name": "Virgo",
        "element": "Earth",
        "ruler": "Mercury",
        "seasonal_focus": "clean habits and practical service",
        "growth_edge": "exchange perfectionism for faithful completion",
        "daily_practice": "Choose one neglected task and finish it with devotion instead of criticism.",
    },
    {
        "slug": "libra",
        "name": "Libra",
        "element": "Air",
        "ruler": "Venus",
        "seasonal_focus": "relational balance and wise peacemaking",
        "growth_edge": "tell the truth before harmony becomes avoidance",
        "daily_practice": "Name one conversation that needs grace and honesty at the same time.",
    },
    {
        "slug": "scorpio",
        "name": "Scorpio",
        "element": "Water",
        "ruler": "Mars",
        "seasonal_focus": "deep release, truth, and sacred restraint",
        "growth_edge": "transform intensity into devotion instead of control",
        "daily_practice": "Journal one fear honestly, then choose one grounded action that reduces secrecy around it.",
    },
    {
        "slug": "sagittarius",
        "name": "Sagittarius",
        "element": "Fire",
        "ruler": "Jupiter",
        "seasonal_focus": "meaning, study, and long-view faith",
        "growth_edge": "anchor vision in discipline, not just inspiration",
        "daily_practice": "Study one short passage slowly and carry its question with you all day.",
    },
    {
        "slug": "capricorn",
        "name": "Capricorn",
        "element": "Earth",
        "ruler": "Saturn",
        "seasonal_focus": "endurance, responsibility, and inner authority",
        "growth_edge": "stop equating worth with relentless output",
        "daily_practice": "Set a boundary that protects your energy for what is truly essential.",
    },
    {
        "slug": "aquarius",
        "name": "Aquarius",
        "element": "Air",
        "ruler": "Saturn",
        "seasonal_focus": "clarity, conviction, and community purpose",
        "growth_edge": "turn ideals into one lived contribution",
        "daily_practice": "Choose one service-oriented act that puts your values into visible motion.",
    },
    {
        "slug": "pisces",
        "name": "Pisces",
        "element": "Water",
        "ruler": "Jupiter",
        "seasonal_focus": "surrender, imagination, and spiritual trust",
        "growth_edge": "stay porous to grace without drifting from structure",
        "daily_practice": "Pair devotion with a simple timetable so inspiration has a container.",
    },
]

SIGN_INDEX = {item["slug"]: item for item in SIGNS}

MONTHS = [
    {"slug": "january", "name": "January", "seasonal_note": "clean starts and sober priorities", "month_energy": "a reset month that asks for honest ordering"},
    {"slug": "february", "name": "February", "seasonal_note": "heart work and relational honesty", "month_energy": "a relational month that exposes what still needs softening"},
    {"slug": "march", "name": "March", "seasonal_note": "threshold energy and movement", "month_energy": "a turning month that asks for brave but thoughtful action"},
    {"slug": "april", "name": "April", "seasonal_note": "new fire and visible motion", "month_energy": "an activating month that rewards clean initiative"},
    {"slug": "may", "name": "May", "seasonal_note": "stability and nourishment", "month_energy": "a grounding month that matures effort through consistency"},
    {"slug": "june", "name": "June", "seasonal_note": "conversation and adaptability", "month_energy": "a fast-moving month that tests mental flexibility"},
    {"slug": "july", "name": "July", "seasonal_note": "home, memory, and emotional weather", "month_energy": "a feeling-rich month that calls for gentler boundaries"},
    {"slug": "august", "name": "August", "seasonal_note": "visibility and courage", "month_energy": "a bright month that asks what leadership looks like with humility"},
    {"slug": "september", "name": "September", "seasonal_note": "refinement and discernment", "month_energy": "an editing month that sharpens habits and standards"},
    {"slug": "october", "name": "October", "seasonal_note": "equilibrium and recalibration", "month_energy": "a balancing month that reveals what must be renegotiated"},
    {"slug": "november", "name": "November", "seasonal_note": "depth, endings, and inward work", "month_energy": "an intense month that rewards honesty over performance"},
    {"slug": "december", "name": "December", "seasonal_note": "meaning, gratitude, and long-view reflection", "month_energy": "a reflective month that helps faith and wisdom mature together"},
]

MONTH_INDEX = {item["slug"]: item for item in MONTHS}

TRANSIT_FAMILIES = [
    {
        "planet_slug": "sun",
        "planet_name": "Sun",
        "core": "identity, leadership, confidence, and visible responsibility",
        "watch_for": "ego strain, approval hunger, and pride-driven timing",
        "practice": "Offer one act of service without attaching it to recognition.",
    },
    {
        "planet_slug": "mercury",
        "planet_name": "Mercury",
        "core": "speech, thought, planning, learning, and timing decisions",
        "watch_for": "restless thinking, mixed messages, and rushed conclusions",
        "practice": "Slow one conversation down enough that truth becomes cleaner than speed.",
    },
    {
        "planet_slug": "venus",
        "planet_name": "Venus",
        "core": "relationship repair, beauty, receptivity, and value alignment",
        "watch_for": "avoidance, indulgence, and calling comfort the same thing as peace",
        "practice": "Choose one gesture that restores harmony without pretending the deeper issue is gone.",
    },
    {
        "planet_slug": "mars",
        "planet_name": "Mars",
        "core": "action, courage, conflict, and disciplined use of force",
        "watch_for": "reactivity, impatience, and battles you pick to relieve tension rather than serve truth",
        "practice": "Give physical heat a constructive outlet before making an important decision.",
    },
    {
        "planet_slug": "jupiter",
        "planet_name": "Jupiter",
        "core": "growth, meaning, faith, blessing, and larger perspective",
        "watch_for": "overconfidence, excess, and assuming expansion removes the need for structure",
        "practice": "Study one teaching deeply instead of collecting five new ones superficially.",
    },
    {
        "planet_slug": "saturn",
        "planet_name": "Saturn",
        "core": "structure, endurance, accountability, and time-tested maturity",
        "watch_for": "heaviness, fear, withdrawal, and mistaking delay for rejection",
        "practice": "Honor one repetitive duty as sacred discipline rather than punishment.",
    },
]

TRANSIT_SPECIALS = [
    {
        "slug": "mercury-retrograde",
        "label": "Mercury Retrograde",
        "planet_slug": "mercury",
        "planet_name": "Mercury",
        "sign_slug": None,
        "sign_name": None,
        "core": "review, revision, and wiser speech under slowed timing",
        "watch_for": "mixed signals, paperwork drift, and impulsive replies",
        "practice": "Edit before sending, pray before answering, and review before agreeing.",
    },
    {
        "slug": "venus-retrograde",
        "label": "Venus Retrograde",
        "planet_slug": "venus",
        "planet_name": "Venus",
        "sign_slug": None,
        "sign_name": None,
        "core": "relationship reflection, value revision, and heart-level honesty",
        "watch_for": "nostalgia, blurry standards, and beauty without truth",
        "practice": "Return to the relationships and promises that still need mature clarity.",
    },
    {
        "slug": "mars-retrograde",
        "label": "Mars Retrograde",
        "planet_slug": "mars",
        "planet_name": "Mars",
        "sign_slug": None,
        "sign_name": None,
        "core": "paused assertion, redirected effort, and a deeper audit of motivation",
        "watch_for": "frustrated anger and force without strategy",
        "practice": "Turn intensity into training, planning, and honest self-observation.",
    },
    {
        "slug": "jupiter-retrograde",
        "label": "Jupiter Retrograde",
        "planet_slug": "jupiter",
        "planet_name": "Jupiter",
        "sign_slug": None,
        "sign_name": None,
        "core": "inner teaching, belief review, and a quieter form of expansion",
        "watch_for": "inflated certainty or waiting for wisdom without practicing it",
        "practice": "Return to the teachings you already know but have not embodied yet.",
    },
    {
        "slug": "saturn-retrograde",
        "label": "Saturn Retrograde",
        "planet_slug": "saturn",
        "planet_name": "Saturn",
        "sign_slug": None,
        "sign_name": None,
        "core": "inner accountability, karmic review, and disciplined restructuring",
        "watch_for": "discouragement, paralysis, and harsh self-judgment",
        "practice": "Repair one neglected responsibility instead of trying to fix your whole life in one move.",
    },
    {
        "slug": "eclipse-season",
        "label": "Eclipse Season",
        "planet_slug": "sun",
        "planet_name": "Sun and Moon",
        "sign_slug": None,
        "sign_name": None,
        "core": "sudden clarity, emotional volatility, and accelerated turning points",
        "watch_for": "drama, projection, and decisions made inside temporary turbulence",
        "practice": "Stay observant, keep rituals simple, and resist forcing certainty too early.",
    },
]

TRANSIT_SLUGS: list[dict[str, str | None]] = []
for family in TRANSIT_FAMILIES:
    for sign in SIGNS:
        TRANSIT_SLUGS.append(
            {
                "slug": f"{family['planet_slug']}-in-{sign['slug']}",
                "label": f"{family['planet_name']} in {sign['name']}",
                "planet_slug": family["planet_slug"],
                "planet_name": family["planet_name"],
                "sign_slug": sign["slug"],
                "sign_name": sign["name"],
                "core": family["core"],
                "watch_for": family["watch_for"],
                "practice": family["practice"],
            }
        )
TRANSIT_SLUGS.extend(TRANSIT_SPECIALS)
TRANSIT_INDEX = {item["slug"]: item for item in TRANSIT_SLUGS}

GITA_REFERENCES = DAILY_SCRIPTURES["GITA"]
BIBLE_REFERENCES = DAILY_SCRIPTURES["BIBLE"]
TRADITION_META = {
    "gita": {
        "label": "Bhagavad Gita",
        "intro": "Gita guidance reads the transit as a training ground for dharma, disciplined effort, and inner steadiness.",
        "verses": GITA_REFERENCES,
        "prayer_prefix": "Transit mantra",
    },
    "bible": {
        "label": "Bible",
        "intro": "Bible guidance reads the transit as a season for faithful response, wise surrender, and scripture-led courage.",
        "verses": BIBLE_REFERENCES,
        "prayer_prefix": "Transit prayer",
    },
}


def _today_iso() -> str:
    return datetime.now(INDIA_TZ).date().isoformat()


def _chapter_verse_from_reference(reference: str) -> tuple[int, int] | tuple[None, None]:
    try:
        value = reference.rsplit(" ", 1)[-1]
        chapter_str, verse_str = value.split(":")
        return int(chapter_str), int(verse_str)
    except Exception:
        return None, None


def _hash_index(*values: str, modulus: int) -> int:
    total = 0
    for value in values:
        for char in value:
            total += ord(char)
    return total % modulus


def _title_case_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("-"))


def _month_position(month_slug: str) -> int:
    for index, month in enumerate(MONTHS, start=1):
        if month["slug"] == month_slug:
            return index
    return 1


def _select_gita_pair(seed: str) -> list[dict[str, str]]:
    index = _hash_index(seed, modulus=len(GITA_REFERENCES))
    second = (index + 3) % len(GITA_REFERENCES)
    return [deepcopy(GITA_REFERENCES[index]), deepcopy(GITA_REFERENCES[second])]


def _select_bible_pair(seed: str) -> list[dict[str, str]]:
    index = _hash_index(seed, modulus=len(BIBLE_REFERENCES))
    second = (index + 2) % len(BIBLE_REFERENCES)
    return [deepcopy(BIBLE_REFERENCES[index]), deepcopy(BIBLE_REFERENCES[second])]


def _transit_seed_content(transit_slug: str, tradition: str) -> dict:
    transit = TRANSIT_INDEX[transit_slug]
    tradition_meta = TRADITION_META[tradition]
    sign_name = transit["sign_name"]
    label = transit["label"]
    is_special = sign_name is None
    heading = (
        f"{label} - {tradition_meta['label']} Guidance for This Transit"
        if is_special
        else f"{transit['planet_name']} in {sign_name} - {tradition_meta['label']} Guidance for This Transit"
    )
    verse_items = _select_gita_pair(transit_slug) if tradition == "gita" else _select_bible_pair(transit_slug)
    article_slug = transit_slug
    today = _today_iso()
    transit_href = f"/transits/{article_slug}"
    panchang_href = f"/panchang/{DEFAULT_PANCHANG_CITY}/{today}"
    traits_href = f"/traits/{(transit['sign_slug'] or 'aries')}/sun/1st-house"

    scripture_cards = []
    for offset, verse in enumerate(verse_items, start=1):
        scripture_cards.append(
            {
                "reference": verse["reference"],
                "text": verse["text"],
                "why_it_fits": (
                    f"Verse {offset} is used here because {label.lower()} places pressure on {transit['core']}. "
                    f"This teaching keeps the seeker focused on disciplined response instead of getting lost in {transit['watch_for']}."
                ),
            }
        )

    prayer_body = (
        f"{tradition_meta['prayer_prefix']}: During {label.lower()}, keep my motives clean, my speech measured, "
        f"and my effort aligned with what is true. Let this season train patience instead of panic, and devotion instead of noise."
    )
    page_path = f"/faith/transit/{transit_slug}/{tradition}"

    return {
        "id": f"faith-transit-{transit_slug}-{tradition}",
        "route": page_path,
        "title": heading,
        "meta_title": heading[:60],
        "meta_description": (
            f"Spiritual guidance for {label.lower()} with {tradition_meta['label']} references, practice ideas, and panchang timing."
        )[:155],
        "tradition": tradition,
        "tradition_label": tradition_meta["label"],
        "transit_slug": transit_slug,
        "transit_label": label,
        "planet_name": transit["planet_name"],
        "sign_name": sign_name,
        "summary": (
            f"{label} highlights {transit['core']}. This page pairs that transit energy with {tradition_meta['label']} teaching, "
            f"steadying the reader through a specific spiritual practice instead of generic encouragement."
        ),
        "energy_intro": (
            f"{label} tends to surface themes around {transit['core']}. The gift of the transit is clarity about what must mature; "
            f"the strain comes when {transit['watch_for']} starts driving the atmosphere. {tradition_meta['intro']} "
            f"That makes this page less about prediction and more about how to move through the season with clean intention."
        ),
        "scripture_cards": scripture_cards,
        "practice_title": f"Practice during {label}",
        "practice_body": (
            f"Use the transit as a season of disciplined repetition rather than emotional improvisation. {transit['practice']} "
            f"Choose one consistent window for reflection, ideally after checking the day's panchang for a calmer rhythm. "
            f"If the transit is making you restless, shorten the practice rather than abandoning it. The aim is to turn insight into habit."
        ),
        "prayer_title": prayer_body.split(":")[0],
        "prayer_body": prayer_body,
        "faq": [
            {
                "q": f"What does {label} mean spiritually?",
                "a": f"It usually points to a season where {transit['core']} becomes impossible to ignore. The healthiest response is thoughtful practice, not dramatic overreaction.",
            },
            {
                "q": f"Which scripture helps during {label}?",
                "a": f"This page highlights {tradition_meta['label']} references that speak to the transit's emotional weather, especially when {transit['watch_for']} starts crowding out clarity.",
            },
            {
                "q": f"What should I do during {label} day to day?",
                "a": f"Keep one repeatable discipline. A small prayer, reading, journal line, or panchang-timed pause does more than a burst of intensity followed by burnout.",
            },
        ],
        "links": {
            "transit_href": transit_href,
            "panchang_href": panchang_href,
            "traits_href": traits_href,
            "faith_hub_href": "/faith",
            "tradition_hub_href": "/faith/transit",
        },
    }


def _daily_seed_content(sign_slug: str, month_slug: str) -> dict:
    sign = SIGN_INDEX[sign_slug]
    month = MONTH_INDEX[month_slug]
    month_number = _month_position(month_slug)
    gita = deepcopy(GITA_REFERENCES[(month_number + len(sign_slug)) % len(GITA_REFERENCES)])
    bible = deepcopy(BIBLE_REFERENCES[(month_number + len(month_slug)) % len(BIBLE_REFERENCES)])
    chapter, verse = _chapter_verse_from_reference(gita["reference"])
    gita_cross_link = f"/faith/gita/{chapter}-{verse}/{sign_slug}-season" if chapter and verse else "/faith/gita"
    transit_choice = TRANSIT_SLUGS[_hash_index(sign_slug, month_slug, modulus=len(TRANSIT_SLUGS))]
    title = f"{sign['name']} Spiritual Guide - {month['name']}"
    today = _today_iso()

    practices = [
        f"Begin {month['name']} by naming the one emotional pattern {sign['name']} needs to stop negotiating with.",
        f"Use {sign['ruler']}-ruled discipline: {sign['daily_practice']}",
        f"Read one short scripture passage before the busiest part of the day so {month['month_energy']} does not become pure reactivity.",
        f"Check the panchang before a major decision when the month feels spiritually noisy or unusually pressured.",
        f"Close the evening by writing one line about where {sign['growth_edge']} became visible in real life.",
    ]

    return {
        "id": f"faith-daily-{sign_slug}-{month_slug}",
        "route": f"/faith/daily/{sign_slug}/{month_slug}",
        "sign_slug": sign_slug,
        "sign_name": sign["name"],
        "month_slug": month_slug,
        "month_name": month["name"],
        "title": title,
        "meta_title": title[:60],
        "meta_description": (
            f"{sign['name']} spiritual guidance for {month['name']} with a Gita verse, a Bible promise, and practical daily steps."
        )[:155],
        "summary": (
            f"This evergreen guide gives {sign['name']} readers a spiritual lens for {month['name']}, using sign archetype, seasonal mood, and scripture-led action."
        ),
        "energy_intro": (
            f"For {sign['name']}, {month['name']} tends to emphasize {sign['seasonal_focus']}. The month carries {month['seasonal_note']}, "
            f"so the deeper question is not what will happen next, but how this sign can live {month['month_energy']} without abandoning its center. "
            f"This is not a horoscope prediction. It is a spiritual guide for how {sign['element'].lower()} energy, {sign['ruler']}-ruled instincts, and the month itself interact."
        ),
        "gita_reference": gita["reference"],
        "gita_text": gita["text"],
        "gita_application": (
            f"{gita['reference']} speaks to {sign['name']} in {month['name']} because this sign grows when effort becomes cleaner than impulse. "
            f"The verse trains {sign['growth_edge']}. In practice, that means moving through the month with intentional repetition, steady speech, and fewer emotionally expensive detours."
        ),
        "bible_reference": bible["reference"],
        "bible_text": bible["text"],
        "bible_application": (
            f"{bible['reference']} steadies the month by addressing the fear pattern hiding underneath {month['month_energy']}. "
            f"For {sign['name']}, the promise is not passive comfort. It is a call to trust, alignment, and practical obedience under pressure."
        ),
        "daily_practice_title": f"{month['name']} practice rhythm for {sign['name']}",
        "daily_practices": practices,
        "faq": [
            {
                "q": f"What scripture should {sign['name']} read in {month['name']}?",
                "a": f"This page pairs {gita['reference']} and {bible['reference']} because they speak to {month['month_energy']} through the lens of {sign['name']}'s spiritual growth edge.",
            },
            {
                "q": f"Is this a monthly horoscope for {sign['name']}?",
                "a": f"No. It is an evergreen spiritual guide for how {sign['name']} can move through {month['name']} with cleaner devotion, better timing, and more grounded choices.",
            },
            {
                "q": f"What should {sign['name']} practice daily in {month['name']}?",
                "a": f"Keep the practice simple and repeatable: one scripture, one reflection, one panchang-aware pause, and one concrete behavioral shift that addresses the month's real tension.",
            },
        ],
        "cta": {
            "label": "Receive a personalized 21-day scripture plan matched to your Vedic birth chart.",
            "href": "/birth-chart",
        },
        "links": {
            "faith_hub_href": "/faith",
            "daily_hub_href": "/faith/daily",
            "sign_hub_href": f"/faith/daily/{sign_slug}",
            "transit_href": f"/faith/transit/{transit_choice['slug']}/gita",
            "panchang_href": f"/panchang/{DEFAULT_PANCHANG_CITY}/{today}",
            "gita_cross_link": gita_cross_link,
        },
    }


def build_daily_pages() -> list[dict]:
    pages = []
    for sign in SIGNS:
        for month in MONTHS:
            pages.append(_daily_seed_content(sign["slug"], month["slug"]))
    return pages


def build_transit_pages() -> list[dict]:
    pages = []
    for transit in TRANSIT_SLUGS:
        for tradition in ("gita", "bible"):
            pages.append(_transit_seed_content(transit["slug"], tradition))
    return pages


def get_daily_page(sign_slug: str, month_slug: str) -> dict | None:
    if sign_slug not in SIGN_INDEX or month_slug not in MONTH_INDEX:
        return None
    return _daily_seed_content(sign_slug, month_slug)


def get_transit_page(transit_slug: str, tradition: str) -> dict | None:
    if transit_slug not in TRANSIT_INDEX or tradition not in TRADITION_META:
        return None
    return _transit_seed_content(transit_slug, tradition)


def get_faith_hub_payload() -> dict:
    gita_pages = get_gita_page_count()
    bible_pages = get_bible_page_count()
    return {
        "title": "Faith Hubs - Gita, Bible, Transit and Daily Scripture",
        "meta_title": "Faith Hubs - Gita, Bible and Daily Scripture",
        "meta_description": "Explore Faith Hubs for daily scripture, transit guidance, the live Bhagavad Gita verse library, and Bible promise pathways by transition.",
        "hero_title": "Faith Hubs for Scripture, Transit Wisdom and Daily Practice",
        "hero_body": (
            "Faith Hubs is EverydayHoroscope's public scripture layer. It connects spiritual practice with the rhythms people actually live through: "
            "monthly emotional seasons, planetary pressure, and daily choices that need steadier guidance than generic inspiration."
        ),
        "counts": {
            "transit_pages": len(TRANSIT_SLUGS) * 2,
            "daily_pages": len(SIGNS) * len(MONTHS),
            "gita_pages": gita_pages,
            "bible_pages": bible_pages,
            "phase_total": len(TRANSIT_SLUGS) * 2 + len(SIGNS) * len(MONTHS) + gita_pages + bible_pages,
        },
        "collections": [
            {
                "slug": "transit",
                "title": "Transit and Scripture",
                "href": "/faith/transit",
                "count_label": f"{len(TRANSIT_SLUGS) * 2} pages",
                "description": "Planetary seasons paired with Gita and Bible guidance, plus practice suggestions rooted in timing and discipline.",
            },
            {
                "slug": "daily",
                "title": "Daily Scripture by Sign and Month",
                "href": "/faith/daily",
                "count_label": f"{len(SIGNS) * len(MONTHS)} pages",
                "description": "Evergreen monthly spiritual guides for every zodiac sign, designed as practice pages rather than prediction pages.",
            },
            {
                "slug": "gita",
                "title": "Gita Verse Hubs",
                "href": "/faith/gita",
                "count_label": f"{gita_pages} pages",
                "description": "All 700 Bhagavad Gita verses mapped across 15 life situations, with chapter hubs and verse-specific guidance.",
            },
            {
                "slug": "bible",
                "title": "Bible Promise Hubs",
                "href": "/faith/bible",
                "count_label": f"{bible_pages} pages",
                "description": "A Bible promise library organized by 120 themes and 50 real-life transitions, with parallel Gita bridges.",
            },
        ],
        "featured_transits": [deepcopy(item) for item in TRANSIT_SLUGS[:6]],
        "featured_signs": [deepcopy(item) for item in SIGNS[:6]],
    }


def get_transit_hub_payload() -> dict:
    return {
        "title": "Faith Transit Hub",
        "meta_title": "Faith Transit Hub - Gita and Bible Guidance",
        "meta_description": "Explore transit-based scripture guidance across 78 transit themes and 2 faith traditions.",
        "hero_title": "Transit and Scripture Guidance",
        "hero_body": (
            "These pages are built for the moments when a transit changes the emotional weather before you can explain why. "
            "Each transit entry pairs a planetary pattern with either Bhagavad Gita or Bible guidance so the season becomes actionable instead of abstract."
        ),
        "traditions": [
            {"slug": "gita", "label": "Bhagavad Gita", "description": TRADITION_META["gita"]["intro"]},
            {"slug": "bible", "label": "Bible", "description": TRADITION_META["bible"]["intro"]},
        ],
        "transits": [deepcopy(item) for item in TRANSIT_SLUGS],
    }


def get_daily_hub_payload() -> dict:
    return {
        "title": "Faith Daily Hub",
        "meta_title": "Daily Scripture by Sign and Month",
        "meta_description": "Browse evergreen daily scripture guides by zodiac sign and month across all 144 sign-month combinations.",
        "hero_title": "Daily Scripture by Sign and Month",
        "hero_body": (
            "This daily layer is evergreen on purpose. Instead of expiring with a date stamp, each guide answers the deeper pattern a sign meets in a given month "
            "and offers scripture-backed practices that can be returned to year after year."
        ),
        "signs": [deepcopy(item) for item in SIGNS],
        "months": [deepcopy(item) for item in MONTHS],
    }


def get_daily_sign_payload(sign_slug: str) -> dict | None:
    sign = SIGN_INDEX.get(sign_slug)
    if sign is None:
        return None
    items = []
    for month in MONTHS:
        page = _daily_seed_content(sign_slug, month["slug"])
        items.append(
            {
                "month_slug": month["slug"],
                "month_name": month["name"],
                "href": page["route"],
                "summary": page["summary"],
            }
        )
    return {
        "title": f"{sign['name']} Daily Scripture Hub",
        "meta_title": f"{sign['name']} Spiritual Guides by Month",
        "meta_description": f"Browse all 12 evergreen monthly spiritual guides for {sign['name']} with Gita and Bible references.",
        "hero_title": f"{sign['name']} Spiritual Guides by Month",
        "hero_body": (
            f"This sign hub gathers every {sign['name']} monthly guide in one place. Use it when you want the spiritual rhythm of the month without reading a generic forecast."
        ),
        "sign": deepcopy(sign),
        "months": items,
    }


def get_gita_hub_payload() -> dict:
    return get_live_gita_hub_payload()


def get_bible_hub_payload() -> dict:
    return get_live_bible_hub_payload()


def get_faith_sitemap_urls() -> list[str]:
    urls = [
        f"{SITE_URL}/faith",
        f"{SITE_URL}/faith/pathways",
        f"{SITE_URL}/faith/transit",
        f"{SITE_URL}/faith/daily",
    ]
    urls.extend(f"{SITE_URL}/faith/pathways/{slug}" for slug in FAITH_PATHWAY_SLUGS)
    urls.extend(get_gita_sitemap_urls())
    urls.extend(get_bible_sitemap_urls())
    urls.extend(f"{SITE_URL}/faith/daily/{sign['slug']}" for sign in SIGNS)
    urls.extend(f"{SITE_URL}{page['route']}" for page in build_daily_pages())
    urls.extend(f"{SITE_URL}{page['route']}" for page in build_transit_pages())
    return urls
