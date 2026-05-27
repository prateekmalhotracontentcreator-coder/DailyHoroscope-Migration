from __future__ import annotations

import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo


SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
DEFAULT_PANCHANG_CITY = "new-delhi-india"
GITA_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "faith" / "gita_verses.json"

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

CHAPTER_TITLES = {
    1: "Observing the Armies on the Battlefield of Kurukshetra",
    2: "Contents of the Gita Summarized",
    3: "Karma-yoga",
    4: "Transcendental Knowledge",
    5: "Karma-yoga - Action in Krishna Consciousness",
    6: "Dhyana-yoga",
    7: "Knowledge of the Absolute",
    8: "Attaining the Supreme",
    9: "The Most Confidential Knowledge",
    10: "The Opulence of the Absolute",
    11: "The Universal Form",
    12: "Devotional Service",
    13: "Nature, the Enjoyer, and Consciousness",
    14: "The Three Modes of Material Nature",
    15: "The Yoga of the Supreme Person",
    16: "The Divine and Demoniac Natures",
    17: "The Divisions of Faith",
    18: "Conclusion - The Perfection of Renunciation",
}

GITA_SITUATIONS = [
    {
        "slug": "career-failure",
        "label": "Career Failure & Job Loss",
        "hook": "Career failure can make a thoughtful, hardworking person feel suddenly disposable. Rejection emails, stalled interviews, and the shame of explaining a setback to family can turn one bad season into an identity crisis.",
        "hidden_fear": "The real panic is rarely only about money. It is the fear that effort no longer counts and that purpose has gone silent.",
        "practice_shift": "returning to duty before confidence comes back",
        "action_focus": "one honest work task, one conversation, and one disciplined routine instead of spiraling into helpless comparison",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "planet_slug": "saturn",
        "planet_label": "Saturn",
        "sign_slug": "capricorn",
        "month_slug": "january",
    },
    {
        "slug": "relationship-breakdown",
        "label": "Relationship Breakdown",
        "hook": "Relationship breakdown scrambles the nervous system because the future you had been rehearsing no longer exists in the same shape. Even ordinary routines can feel charged when trust, intimacy, and shared language begin collapsing.",
        "hidden_fear": "Under the surface sits the fear that love has become unsafe and that every conversation will now cost more than it heals.",
        "practice_shift": "choosing clarity and boundary over emotional bargaining",
        "action_focus": "naming what is true, refusing mixed signals, and protecting dignity without pretending the grief is small",
        "transit_slug": "venus-in-libra",
        "transit_label": "Venus in Libra",
        "planet_slug": "venus",
        "planet_label": "Venus",
        "sign_slug": "libra",
        "month_slug": "october",
    },
    {
        "slug": "grief-and-loss",
        "label": "Grief and Loss",
        "hook": "Grief rearranges time. Some hours feel dense and wordless, while ordinary responsibilities continue asking for a version of you that no longer feels available.",
        "hidden_fear": "Many people quietly fear that if they stop feeling the ache they will betray what mattered, yet they also fear living forever at the mercy of sorrow.",
        "practice_shift": "letting devotion hold sorrow without demanding immediate resolution",
        "action_focus": "smaller rituals, gentler pacing, and truthful remembrance instead of spiritual performance",
        "transit_slug": "saturn-retrograde",
        "transit_label": "Saturn Retrograde",
        "planet_slug": "saturn",
        "planet_label": "Saturn",
        "sign_slug": "scorpio",
        "month_slug": "november",
    },
    {
        "slug": "anxiety",
        "label": "Anxiety & Overwhelm",
        "hook": "Anxiety often feels less like fear of one event and more like living inside too many unfinished futures at once. The mind races, the body stays braced, and even rest can feel undeserved.",
        "hidden_fear": "The deeper fear is that if vigilance drops for even a moment, something essential will fall apart.",
        "practice_shift": "moving from mental over-control into repeatable steadiness",
        "action_focus": "slowing the loop, naming the next manageable task, and letting disciplined presence replace emergency thinking",
        "transit_slug": "mercury-retrograde",
        "transit_label": "Mercury Retrograde",
        "planet_slug": "mercury",
        "planet_label": "Mercury",
        "sign_slug": "gemini",
        "month_slug": "june",
    },
    {
        "slug": "depression",
        "label": "Depression & Low Energy",
        "hook": "Depression can flatten desire so thoroughly that even basic care begins to feel heavy. It is hard to believe guidance matters when motivation is low and the inner voice has turned sparse or hopeless.",
        "hidden_fear": "What hurts is not only sadness but the suspicion that nothing in you will rise again with strength or interest.",
        "practice_shift": "protecting one small act of life-giving structure each day",
        "action_focus": "gentle repetition, simple nourishment, and choosing one doable responsibility rather than waiting for inspiration to return",
        "transit_slug": "saturn-in-pisces",
        "transit_label": "Saturn in Pisces",
        "planet_slug": "saturn",
        "planet_label": "Saturn",
        "sign_slug": "pisces",
        "month_slug": "december",
    },
    {
        "slug": "identity-crisis",
        "label": "Identity Crisis & Confusion",
        "hook": "An identity crisis shows up when old roles stop fitting but the new shape of life has not become clear yet. You may still be functioning outwardly while inwardly feeling unrecognizable.",
        "hidden_fear": "The hidden terror is that if the old labels fall away, there may be nothing coherent left to stand on.",
        "practice_shift": "finding identity in alignment rather than external role",
        "action_focus": "trading image management for truth, and letting purpose emerge through consistent action rather than dramatic reinvention",
        "transit_slug": "sun-in-leo",
        "transit_label": "Sun in Leo",
        "planet_slug": "sun",
        "planet_label": "Sun",
        "sign_slug": "leo",
        "month_slug": "august",
    },
    {
        "slug": "financial-pressure",
        "label": "Financial Pressure & Debt",
        "hook": "Financial pressure compresses choice. Bills, debt, and delayed income can make every decision feel loaded with threat, especially when responsibility for other people is involved.",
        "hidden_fear": "What makes the strain so sharp is the fear of becoming trapped, dependent, or permanently behind.",
        "practice_shift": "replacing scarcity panic with disciplined stewardship",
        "action_focus": "clear numbers, honest conversations, and one concrete correction that reduces financial confusion today",
        "transit_slug": "jupiter-in-taurus",
        "transit_label": "Jupiter in Taurus",
        "planet_slug": "jupiter",
        "planet_label": "Jupiter",
        "sign_slug": "taurus",
        "month_slug": "may",
    },
    {
        "slug": "divorce",
        "label": "Divorce & Separation",
        "hook": "Divorce carries grief, paperwork, memory, and identity fracture all at once. It is not only the ending of a bond but the exhausting work of reordering home, finances, family expectations, and self-trust.",
        "hidden_fear": "Many people fear becoming emotionally guarded forever or repeating the same fracture in a new form later.",
        "practice_shift": "making decisions from truth and peace instead of retaliation",
        "action_focus": "clean boundaries, slower legal and emotional decisions, and refusing to let conflict become your permanent self-definition",
        "transit_slug": "venus-retrograde",
        "transit_label": "Venus Retrograde",
        "planet_slug": "venus",
        "planet_label": "Venus",
        "sign_slug": "libra",
        "month_slug": "october",
    },
    {
        "slug": "health-crisis",
        "label": "Health Crisis & Recovery",
        "hook": "A health crisis changes the pace of everything. The body becomes the center of attention, uncertainty rises, and the future gets measured in appointments, energy levels, and what can still be trusted physically.",
        "hidden_fear": "Behind the practical questions is often a deep fear of losing agency, dignity, or hope in the face of vulnerability.",
        "practice_shift": "meeting fragility with disciplined care instead of despair",
        "action_focus": "following treatment faithfully, asking better questions, and protecting the inner life while the body heals at its own speed",
        "transit_slug": "mars-in-virgo",
        "transit_label": "Mars in Virgo",
        "planet_slug": "mars",
        "planet_label": "Mars",
        "sign_slug": "virgo",
        "month_slug": "september",
    },
    {
        "slug": "new-beginning",
        "label": "New Beginning & Fresh Start",
        "hook": "A new beginning is exciting until it exposes how much uncertainty comes with starting over. Fresh starts ask for courage, but they also require restraint so momentum does not become self-sabotage.",
        "hidden_fear": "The quieter fear is that hope may outrun foundation, leaving you to repeat old patterns in a new setting.",
        "practice_shift": "starting cleanly without demanding instant mastery",
        "action_focus": "building the first faithful habits, keeping promises small enough to keep, and letting consistency carry the fresh start forward",
        "transit_slug": "sun-in-aries",
        "transit_label": "Sun in Aries",
        "planet_slug": "sun",
        "planet_label": "Sun",
        "sign_slug": "aries",
        "month_slug": "april",
    },
    {
        "slug": "betrayal",
        "label": "Betrayal & Trust Issues",
        "hook": "Betrayal does more than wound affection. It unsettles judgment, memory, and your own ability to know what was real. After trust breaks, even kindness can feel suspicious.",
        "hidden_fear": "Often the deepest fear is not only that someone else lied, but that your own discernment can no longer be relied upon.",
        "practice_shift": "rebuilding discernment without turning hard or vindictive",
        "action_focus": "slower trust, firmer truth, and decisions shaped by wisdom rather than revenge",
        "transit_slug": "eclipse-season",
        "transit_label": "Eclipse Season",
        "planet_slug": "sun",
        "planet_label": "Sun and Moon",
        "sign_slug": "scorpio",
        "month_slug": "november",
    },
    {
        "slug": "loneliness",
        "label": "Loneliness & Isolation",
        "hook": "Loneliness can persist even when life looks full from the outside. It is the ache of going unmirrored, unseen, or emotionally unaccompanied for too long.",
        "hidden_fear": "The hard question beneath it is whether connection is still possible without betraying who you are.",
        "practice_shift": "staying available to relationship while strengthening inner steadiness",
        "action_focus": "small social courage, spiritual companionship, and honest routines that keep isolation from becoming identity",
        "transit_slug": "saturn-in-aquarius",
        "transit_label": "Saturn in Aquarius",
        "planet_slug": "saturn",
        "planet_label": "Saturn",
        "sign_slug": "aquarius",
        "month_slug": "february",
    },
    {
        "slug": "creative-block",
        "label": "Creative Block & Stagnation",
        "hook": "Creative block can feel humiliating because it interrupts the part of you that usually knows how to generate, shape, or imagine. The longer the pause lasts, the easier it becomes to interpret it as permanent.",
        "hidden_fear": "What many people fear most is not slowness itself but the possibility that meaning, originality, or voice has dried up for good.",
        "practice_shift": "returning to craft through structure instead of waiting for emotional permission",
        "action_focus": "short sessions, imperfect drafts, and enough rhythm to let movement restart before confidence does",
        "transit_slug": "mercury-in-gemini",
        "transit_label": "Mercury in Gemini",
        "planet_slug": "mercury",
        "planet_label": "Mercury",
        "sign_slug": "gemini",
        "month_slug": "june",
    },
    {
        "slug": "parenting-challenges",
        "label": "Parenting Challenges",
        "hook": "Parenting challenges stretch both love and stamina because the stakes feel immediate and personal. When a child is struggling, many adults begin carrying guilt, urgency, and helplessness all at the same time.",
        "hidden_fear": "The private fear is that one wrong response today might leave a mark that cannot be easily repaired later.",
        "practice_shift": "leading with steadiness instead of panic",
        "action_focus": "clear limits, warmer repair, and patient repetition that supports growth without turning every hard season into catastrophe",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "planet_slug": "jupiter",
        "planet_label": "Jupiter",
        "sign_slug": "cancer",
        "month_slug": "july",
    },
    {
        "slug": "major-decision",
        "label": "Major Decision & Crossroads",
        "hook": "A major decision can exhaust the mind because the cost of choosing feels high and the cost of waiting feels high too. When several futures stay open at once, clarity often gets buried under overthinking.",
        "hidden_fear": "Usually the fear is not only choosing wrongly but carrying the consequences of one uncertain move for years.",
        "practice_shift": "making a grounded decision from values instead of urgency",
        "action_focus": "sorting facts from fear, identifying the real duty in front of you, and choosing with sobriety rather than pressure",
        "transit_slug": "mercury-in-virgo",
        "transit_label": "Mercury in Virgo",
        "planet_slug": "mercury",
        "planet_label": "Mercury",
        "sign_slug": "virgo",
        "month_slug": "september",
    },
]
SITUATION_INDEX = {item["slug"]: item for item in GITA_SITUATIONS}

GLOSSARY_STOP_TERMS = {
    "arjuna",
    "sañjaya",
    "saïjaya",
    "bhagavän",
    "çré",
    "uväca",
    "ca",
    "eva",
    "tu",
    "hi",
    "na",
    "tat",
    "yat",
    "idam",
    "etad",
}


def _today_iso() -> str:
    return datetime.now(INDIA_TZ).date().isoformat()


def _current_month_slug() -> str:
    return datetime.now(INDIA_TZ).strftime("%B").lower()


def _hash_index(*values: str, modulus: int) -> int:
    total = 0
    for value in values:
        for char in value:
            total += ord(char)
    return total % modulus


@lru_cache(maxsize=1)
def _load_gita_verses() -> list[dict]:
    return json.loads(GITA_ASSET_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _gita_index() -> dict[tuple[int, int], dict]:
    return {(item["chapter"], item["verse"]): item for item in _load_gita_verses()}


@lru_cache(maxsize=1)
def _chapter_map() -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = {}
    for item in _load_gita_verses():
        grouped.setdefault(item["chapter"], []).append(item)
    return grouped


def _select_glossary_terms(verse: dict, limit: int = 3) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for item in verse.get("glossary", []):
        term = item.get("term", "").strip()
        gloss = item.get("gloss", "").strip()
        lowered = term.lower()
        if not term or not gloss:
            continue
        if any(stop in lowered for stop in GLOSSARY_STOP_TERMS):
            continue
        selected.append({"term": term, "gloss": gloss})
        if len(selected) == limit:
            return selected

    fallback_words: list[str] = []
    for token in verse.get("iast", "").replace("'", " ").replace("-", " ").split():
        cleaned = token.strip(".,;:!?[]()").lower()
        if len(cleaned) < 4 or cleaned in GLOSSARY_STOP_TERMS or cleaned in fallback_words:
            continue
        fallback_words.append(cleaned)
        if len(fallback_words) == limit:
            break

    for token in fallback_words:
        selected.append({"term": token, "gloss": "a key Sanskrit term in this verse"})
    return selected[:limit]


def _build_etymology_items(verse: dict, situation: dict) -> list[dict[str, str]]:
    items = []
    for item in _select_glossary_terms(verse):
        items.append(
            {
                "term": item["term"],
                "gloss": item["gloss"],
                "application": (
                    f"In {situation['label'].lower()}, this word matters because it redirects attention toward "
                    f"{situation['practice_shift']} instead of feeding {situation['hidden_fear'].lower()}"
                ),
            }
        )
    return items


def _top_situations_for_verse(chapter: int, verse: int, limit: int = 5) -> list[dict]:
    start = _hash_index(str(chapter), str(verse), modulus=len(GITA_SITUATIONS))
    items: list[dict] = []
    for offset in range(limit):
        situation = GITA_SITUATIONS[(start + offset) % len(GITA_SITUATIONS)]
        items.append(
            {
                "slug": situation["slug"],
                "label": situation["label"],
                "href": f"/faith/gita/{chapter}-{verse}/{situation['slug']}",
            }
        )
    return items


def get_gita_page(chapter: int, verse_number: int, situation_slug: str) -> dict | None:
    verse = _gita_index().get((chapter, verse_number))
    situation = SITUATION_INDEX.get(situation_slug)
    if verse is None or situation is None:
        return None

    route = f"/faith/gita/{chapter}-{verse_number}/{situation_slug}"
    today = _today_iso()
    current_month = _current_month_slug()
    etymology_items = _build_etymology_items(verse, situation)
    chapter_title = verse["chapter_title"]
    related_situations = [
        {
            "slug": item["slug"],
            "label": item["label"],
            "href": f"/faith/gita/{chapter}-{verse_number}/{item['slug']}",
        }
        for item in GITA_SITUATIONS
    ]
    top_situations = [item for item in related_situations if item["slug"] != situation_slug][:5]

    return {
        "id": f"faith-gita-{chapter}-{verse_number}-{situation_slug}",
        "route": route,
        "title": f"Bhagavad Gita {chapter}:{verse_number} for {situation['label']}",
        "meta_title": f"Bhagavad Gita {chapter}:{verse_number} for {situation['label']}"[:60],
        "meta_description": (
            f"Bhagavad Gita {chapter}:{verse_number} for {situation['label'].lower()} with verse meaning, practical guidance, and transit insight."
        )[:155],
        "chapter": chapter,
        "chapter_title": chapter_title,
        "verse": verse_number,
        "reference": verse["reference"],
        "verse_iast": verse["iast"],
        "transliteration": verse["transliteration"],
        "translation": verse["translation"],
        "source": verse["source"],
        "situation_slug": situation_slug,
        "situation_label": situation["label"],
        "summary": (
            f"This page reads Bhagavad Gita {chapter}:{verse_number} through the lived reality of {situation['label'].lower()}, "
            f"keeping the verse grounded in action, emotional honesty, and a specific spiritual response."
        ),
        "hook": (
            f"{situation['hook']} {situation['hidden_fear']} Bhagavad Gita {chapter}:{verse_number} helps by interrupting that spiral "
            f"and re-centering the reader around {situation['practice_shift']}. The verse does not ask for denial. "
            f"It asks for a truer next step, which is why it becomes especially useful when a situation feels too emotionally loud to think through cleanly."
        ),
        "etymology_intro": (
            f"The language of the verse slows the mind down. Instead of rushing toward relief, it sharpens the exact posture "
            f"needed when {situation['label'].lower()} is active."
        ),
        "etymology_items": etymology_items,
        "application": (
            f"In practical terms, this verse pushes against the most expensive habit in {situation['label'].lower()}: reacting as though emotional intensity must make the decision. "
            f"Today, apply it through {situation['action_focus']}. That may sound simple, but simplicity is precisely what restores traction here. "
            f"The point is not to solve the whole story before sunset. It is to stop handing the next faithful move over to fear, shame, exhaustion, or resentment. "
            f"Once the next clean action is named, the situation loses some of its power to define your identity."
        ),
        "practice_prompts": [
            f"Write one sentence naming what {situation['label'].lower()} is trying to make you believe.",
            f"Choose the next duty that matches {situation['practice_shift']}, even if the result is still unknown.",
            f"End the day by noting whether your choices came from pressure or from alignment.",
        ],
        "transit_layer": (
            f"This verse often becomes more vivid during {situation['transit_label'].lower()}, when {situation['planet_label']} themes press on the same nerves this situation already exposes. "
            f"In dasha language, seasons ruled by {situation['planet_label']} can magnify the demand for maturity, timing, and inner steadiness. "
            f"That is why the companion transit page matters here: it helps translate the verse from timeless teaching into the emotional weather of the moment."
        ),
        "faq": [
            {
                "q": f"What does Bhagavad Gita {chapter}:{verse_number} mean for {situation['label'].lower()}?",
                "a": (
                    f"It means the verse should be read as guidance for {situation['practice_shift']}. "
                    f"The teaching does not erase the pain of the situation, but it does challenge the false story that panic should decide what happens next."
                ),
            },
            {
                "q": f"How can I apply this Gita verse today if I am facing {situation['label'].lower()}?",
                "a": (
                    f"Use the verse to choose one concrete action before chasing emotional certainty. "
                    f"In this situation, disciplined movement matters more than dramatic motivation because it starts restoring agency immediately."
                ),
            },
            {
                "q": f"Which transit or season makes Bhagavad Gita {chapter}:{verse_number} especially relevant here?",
                "a": (
                    f"{situation['transit_label']} is a strong companion because it highlights the same growth edge. "
                    f"If life already feels pressured in that direction, the verse becomes a steadier way to respond than guesswork or fear."
                ),
            },
        ],
        "related_situations": related_situations,
        "top_situations": top_situations,
        "links": {
            "faith_hub_href": "/faith",
            "gita_hub_href": "/faith/gita",
            "chapter_hub_href": f"/faith/gita/chapter/{chapter}",
            "faith_transit_href": f"/faith/transit/{situation['transit_slug']}/gita",
            "transit_href": f"/transits/{situation['transit_slug']}",
            "daily_href": f"/faith/daily/{situation['sign_slug']}/{situation['month_slug']}",
            "current_month_href": f"/faith/daily/{situation['sign_slug']}/{current_month}",
            "panchang_href": f"/panchang/{DEFAULT_PANCHANG_CITY}/{today}",
        },
    }


def get_gita_chapter_payload(chapter: int) -> dict | None:
    verses = _chapter_map().get(chapter)
    if verses is None:
        return None

    items = []
    for verse in verses:
        items.append(
            {
                "chapter": chapter,
                "verse": verse["verse"],
                "reference": verse["reference"],
                "translation": verse["translation"],
                "preview_href": f"/faith/gita/{chapter}-{verse['verse']}/{_top_situations_for_verse(chapter, verse['verse'], 1)[0]['slug']}",
                "top_situations": _top_situations_for_verse(chapter, verse["verse"]),
            }
        )

    return {
        "title": f"Bhagavad Gita Chapter {chapter}",
        "meta_title": f"Bhagavad Gita Chapter {chapter} - Situation Index",
        "meta_description": (
            f"Browse Bhagavad Gita Chapter {chapter} verse pages and the top life-situation links for each verse."
        )[:155],
        "hero_title": f"Bhagavad Gita Chapter {chapter}: {CHAPTER_TITLES[chapter]}",
        "hero_body": (
            f"This chapter hub groups every verse in Chapter {chapter} and highlights five life-situation paths for each one. "
            f"It is meant for readers who want both canonical chapter order and practical search entry points."
        ),
        "chapter": chapter,
        "chapter_title": CHAPTER_TITLES[chapter],
        "verse_count": len(verses),
        "situations": [{"slug": item["slug"], "label": item["label"]} for item in GITA_SITUATIONS],
        "verses": items,
    }


def get_gita_hub_payload() -> dict:
    verses = _load_gita_verses()
    chapter_cards = []
    for chapter in range(1, 19):
        chapter_verses = _chapter_map().get(chapter, [])
        sample_verse = chapter_verses[0] if chapter_verses else None
        chapter_cards.append(
            {
                "chapter": chapter,
                "title": CHAPTER_TITLES[chapter],
                "verse_count": len(chapter_verses),
                "href": f"/faith/gita/chapter/{chapter}",
                "sample_href": (
                    f"/faith/gita/{chapter}-{sample_verse['verse']}/{_top_situations_for_verse(chapter, sample_verse['verse'], 1)[0]['slug']}"
                    if sample_verse
                    else "/faith/gita"
                ),
            }
        )

    featured_refs = [(2, 47), (6, 5), (12, 15), (18, 66)]
    featured_verses = []
    for chapter, verse_number in featured_refs:
        verse = _gita_index().get((chapter, verse_number))
        if verse is None:
            continue
        featured_verses.append(
            {
                "reference": verse["reference"],
                "translation": verse["translation"],
                "href": f"/faith/gita/{chapter}-{verse_number}/{_top_situations_for_verse(chapter, verse_number, 1)[0]['slug']}",
            }
        )

    return {
        "title": "Faith Gita Hub",
        "meta_title": "Bhagavad Gita Verse Library",
        "meta_description": "Explore all 700 Bhagavad Gita verses across 15 life situations, chapter hubs, and evergreen practice pathways.",
        "hero_title": "Bhagavad Gita Verse Library for Real-Life Situations",
        "hero_body": (
            "This hub moves beyond a preview. Every verse in the Bhagavad Gita can now be explored through fifteen high-intent life situations, "
            "so readers can enter through chapter study, emotional need, or practical search language without losing the integrity of the text."
        ),
        "counts": {
            "verses": len(verses),
            "situations": len(GITA_SITUATIONS),
            "pages": len(verses) * len(GITA_SITUATIONS),
            "chapters": 18,
        },
        "chapters": chapter_cards,
        "situations": [{"slug": item["slug"], "label": item["label"]} for item in GITA_SITUATIONS],
        "featured_verses": featured_verses,
        "phase_note": "Phase 2 is live for the Gita layer. Bible promise pages remain the next major build phase.",
    }


def build_gita_pages() -> list[dict]:
    pages = []
    for verse in _load_gita_verses():
        for situation in GITA_SITUATIONS:
            pages.append(get_gita_page(verse["chapter"], verse["verse"], situation["slug"]))
    return [page for page in pages if page is not None]


def get_gita_page_count() -> int:
    return len(_load_gita_verses()) * len(GITA_SITUATIONS)


def get_gita_sitemap_urls() -> list[str]:
    urls = [f"{SITE_URL}/faith/gita"]
    urls.extend(f"{SITE_URL}/faith/gita/chapter/{chapter}" for chapter in range(1, 19))
    for verse in _load_gita_verses():
        for situation in GITA_SITUATIONS:
            urls.append(f"{SITE_URL}/faith/gita/{verse['chapter']}-{verse['verse']}/{situation['slug']}")
    return urls
