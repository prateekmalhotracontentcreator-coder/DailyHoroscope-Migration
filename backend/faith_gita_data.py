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

RECITATION_FEATURES = {
    (2, 47): {
        "focus": "Work without panic",
        "why": "Use this when effort feels tangled up with outcome anxiety.",
        "practice_window": "Best for morning resets before work, interviews, or heavy decision blocks.",
        "situation_slug": "career-failure",
    },
    (4, 7): {
        "focus": "Restoring order",
        "why": "Use this when life feels morally noisy and you need to remember that correction can still enter the scene.",
        "practice_window": "Best for threshold moments, conflict-heavy weeks, or spiritual fatigue.",
        "situation_slug": "major-decision",
    },
    (6, 5): {
        "focus": "Lifting the self",
        "why": "Use this when low mood or self-sabotage is turning inward pressure into passivity.",
        "practice_window": "Best for depression, discouragement, or slow-start mornings.",
        "situation_slug": "depression",
    },
    (9, 22): {
        "focus": "Protection and provision",
        "why": "Use this when fear about support, money, or being carried through uncertainty becomes loud.",
        "practice_window": "Best for financial pressure, family stress, and evening calming.",
        "situation_slug": "financial-pressure",
    },
    (12, 15): {
        "focus": "Becoming non-agitating",
        "why": "Use this when relationships are reactive and you need a cleaner emotional field.",
        "practice_window": "Best before hard conversations or after emotional conflict.",
        "situation_slug": "relationship-breakdown",
    },
    (15, 1): {
        "focus": "Seeing the deeper structure",
        "why": "Use this when confusion is high and you need to step back from surface noise.",
        "practice_window": "Best for identity questions, study, and reflective journaling.",
        "situation_slug": "identity-crisis",
    },
    (17, 3): {
        "focus": "Examining faith and inner posture",
        "why": "Use this when your habits are shaping belief more than your ideals are.",
        "practice_window": "Best for devotional recalibration and habit resets.",
        "situation_slug": "anxiety",
    },
    (18, 66): {
        "focus": "Surrender and refuge",
        "why": "Use this when life feels too heavy to solve by control alone.",
        "practice_window": "Best for grief, surrender seasons, and night recitation.",
        "situation_slug": "grief-and-loss",
    },
}

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


def _recitation_lines(verse: dict, max_lines: int = 3) -> list[str]:
    source = verse.get("transliteration") or verse.get("iast") or ""
    words = source.split()
    if not words:
        return []

    target = max(4, len(words) // max_lines)
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        current.append(word)
        if len(current) >= target and len(lines) < max_lines - 1:
            lines.append(" ".join(current))
            current = []
    if current:
        lines.append(" ".join(current))
    return lines[:max_lines]


def _verse_recitation_payload(verse: dict) -> dict:
    feature = RECITATION_FEATURES.get((verse["chapter"], verse["verse"]))
    lines = _recitation_lines(verse)
    return {
        "is_featured": feature is not None,
        "collection_href": "/faith/gita/recitation",
        "focus": feature["focus"] if feature else "Slow recitation and reflective repetition",
        "why": feature["why"] if feature else "Use slow repetition to let the verse settle before interpretation rushes in.",
        "practice_window": feature["practice_window"] if feature else "Best for three slow rounds before journaling, prayer, or meditation.",
        "display_lines": lines,
        "rounds": 3 if feature else 2,
        "cadence_note": "Read one line per breath and pause briefly at the end of each round.",
    }


def _featured_recitation_cards() -> list[dict]:
    cards: list[dict] = []
    for (chapter, verse_number), meta in RECITATION_FEATURES.items():
        verse = _gita_index().get((chapter, verse_number))
        if verse is None:
            continue
        cards.append(
            {
                "reference": verse["reference"],
                "chapter": chapter,
                "verse": verse_number,
                "focus": meta["focus"],
                "why": meta["why"],
                "practice_window": meta["practice_window"],
                "translation": verse["translation"],
                "display_lines": _recitation_lines(verse),
                "href": f"/faith/gita/{chapter}-{verse_number}/{meta['situation_slug']}",
            }
        )
    return cards


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


def _verse_focus_fragment(verse: dict) -> str:
    translation = verse.get("translation", "")
    words = [word.strip(" ,.;:!?()[]") for word in translation.split() if len(word.strip(" ,.;:!?()[]")) > 4]
    return " ".join(words[:4]).lower() if words else "the verse's central instruction"


GITA_TRANSLATION_SKIP = {
    "dhritarashtra", "sanjaya", "being", "place", "after", "their", "there", "which", "would",
    "these", "those", "shall", "unto", "with", "from", "your", "have", "were", "this",
}


def _translation_keywords(verse: dict, limit: int = 3) -> list[str]:
    cleaned: list[str] = []
    for raw in verse.get("translation", "").replace("--", " ").replace("-", " ").split():
        word = raw.strip(" ,.;:!?()[]'\"").lower()
        word = "".join(char for char in word if char.isalpha())
        if len(word) < 5 or word in GITA_TRANSLATION_SKIP or word in cleaned:
            continue
        cleaned.append(word)
        if len(cleaned) == limit:
            break
    if not cleaned:
        cleaned = ["discipline", "alignment", "steadiness"][:limit]
    while len(cleaned) < limit:
        cleaned.append(cleaned[-1])
    return cleaned


def _gita_seed(chapter: int, verse_number: int, situation_slug: str, modulus: int) -> int:
    return _hash_index(str(chapter), str(verse_number), situation_slug, modulus=modulus)


def _gita_summary(verse: dict, situation: dict) -> str:
    keywords = _translation_keywords(verse, limit=2)
    seed = _gita_seed(verse["chapter"], verse["verse"], situation["slug"], modulus=8)
    options = [
        f"Bhagavad Gita {verse['reference']} reads {situation['label'].lower()} through {keywords[0]} and {keywords[1]}, giving the page a verse-led frame instead of a generic encouragement layer.",
        f"For {situation['label'].lower()}, Bhagavad Gita {verse['reference']} turns on the words {keywords[0]} and {keywords[1]}, so the guidance comes from this verse's own pressure points.",
        f"This reading of Bhagavad Gita {verse['reference']} uses {keywords[0]} and {keywords[1]} to interpret {situation['label'].lower()} with more specificity than a fixed situation template can provide.",
        f"Bhagavad Gita {verse['reference']} becomes a distinct page for {situation['label'].lower()} by anchoring the guidance in {keywords[0]} and {keywords[1]} rather than in reusable boilerplate.",
        f"In this Faith route, Bhagavad Gita {verse['reference']} meets {situation['label'].lower()} by pressing the language of {keywords[0]} and {keywords[1]} into the lived problem itself.",
        f"Rather than repeating one situation paragraph, this page lets Bhagavad Gita {verse['reference']} speak through {keywords[0]} and {keywords[1]} inside {situation['label'].lower()}.",
        f"For readers facing {situation['label'].lower()}, Bhagavad Gita {verse['reference']} is summarized here through {keywords[0]} and {keywords[1]}, which changes the center of gravity verse by verse.",
        f"This page treats Bhagavad Gita {verse['reference']} as a unique response to {situation['label'].lower()}, built around the translation words {keywords[0]} and {keywords[1]}.",
    ]
    return options[seed]


def _gita_hook(verse: dict, situation: dict) -> str:
    keywords = _translation_keywords(verse, limit=3)
    focus = _verse_focus_fragment(verse)
    sit = _situation_vocabulary(situation)
    seed = _gita_seed(verse["chapter"], verse["verse"], situation["slug"], modulus=8)
    options = [
        f"In {situation['label'].lower()}, the mind is often pulled toward {sit[0]}. Bhagavad Gita {verse['reference']} answers through {keywords[0]} and {keywords[1]}, redirecting attention toward {sit[1]}.",
        f"{situation['label']} becomes harder when the inner story is ruled by {sit[0]}. Here the verse uses {keywords[0]}, {keywords[1]}, and {keywords[2]} to produce a cleaner version of {focus}.",
        f"When {situation['label'].lower()} gets emotionally loud, Bhagavad Gita {verse['reference']} brings in {keywords[0]} and {keywords[1]} so the heart is not governed by {sit[0]}.",
        f"This verse does not treat {situation['label'].lower()} as a generic struggle. It uses {keywords[0]} and {keywords[1]} to redirect the reader toward {sit[1]}.",
        f"In this reading, {keywords[0]} and {keywords[1]} expose the exact pressure hiding inside {situation['label'].lower()}, especially when {sit[0]} starts steering attention.",
        f"The force of Bhagavad Gita {verse['reference']} lies in how {keywords[0]} and {keywords[1]} steady a reader who is drifting away from {sit[1]}.",
        f"When this life pressure begins scripting the future, Bhagavad Gita {verse['reference']} pushes back with {keywords[0]}, {keywords[1]}, and {keywords[2]}.",
        f"Bhagavad Gita {verse['reference']} meets {situation['label'].lower()} through {keywords[0]} and {keywords[1]}, giving the page a verse-shaped rather than {sit[0]}-shaped center.",
    ]
    return options[seed]


def _gita_application(verse: dict, situation: dict) -> str:
    keywords = _translation_keywords(verse, limit=5)
    sit = _situation_vocabulary(situation)
    seed = _gita_seed(verse["chapter"], verse["verse"], situation["slug"], modulus=8)
    options = [
        f"Applied today, the verse asks you to practice {keywords[0]} through {sit[2]}. Let {keywords[1]} define the next task instead of letting {sit[0]} define the whole day.",
        f"In practical use, Bhagavad Gita {verse['reference']} makes {keywords[0]} concrete: {sit[2]}. Work the next duty in that spirit, and let {keywords[1]} replace reflexive overreaction.",
        f"The application here is not broad inspiration but disciplined use of {keywords[0]}. In {situation['label'].lower()}, that means {sit[2]} while {keywords[1]} keeps the pace cleaner than {sit[0]}.",
        f"To apply this verse, translate {keywords[0]} into one act: {sit[2]}. Then hold to {keywords[1]} long enough that {sit[0]} stops dictating every inner conclusion.",
        f"Bhagavad Gita {verse['reference']} becomes practical when {keywords[0]} is moved into behavior. Use it by choosing {sit[2]}, and let {keywords[1]} interrupt the {sit[0]} loop.",
        f"One faithful use of this verse is to treat {keywords[0]} as the rule for the next decision. In {situation['label'].lower()}, that looks like {sit[2]} while {keywords[2]} keeps the response steady.",
        f"The verse is applied well when {keywords[0]} and {keywords[1]} become visible in the next hours, not merely admired. Start with {sit[2]} and let the emotional temperature settle.",
        f"For this situation, the verse turns practical when {keywords[0]} shapes the next duty and {keywords[1]} narrows attention. Use {keywords[2]} to carry out {sit[2]}.",
    ]
    return options[seed]


def _situation_vocabulary(situation: dict) -> list[str]:
    """Returns 3 high-specificity tokens unique to this situation."""
    def _pick(text: str) -> str:
        words = [w.strip(".,;:").lower() for w in text.split() if len(w) > 4]
        candidates = [w for w in words if w not in {
            "when", "that", "this", "from", "with", "into", "their", "which",
            "about", "toward", "through", "instead", "without", "become"
        }]
        return candidates[0] if candidates else words[0] if words else "steadiness"

    return [
        _pick(situation["hidden_fear"]),
        _pick(situation["practice_shift"]),
        _pick(situation["action_focus"]),
    ]


def _how_to_apply_steps(verse: dict, situation: dict) -> list[str]:
    verse_focus = _verse_focus_fragment(verse)
    return [
        f"Name the exact place where {situation['label'].lower()} is pushing you away from {situation['practice_shift']}.",
        f"Read {verse['reference']} once slowly and ask how '{verse_focus}' changes the next duty in front of you.",
        f"Take one action that matches {situation['action_focus']} before you ask the situation to feel easier.",
    ]


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
    recitation = _verse_recitation_payload(verse)
    how_to_apply = _how_to_apply_steps(verse, situation)
    verse_focus = _verse_focus_fragment(verse)
    summary = _gita_summary(verse, situation)
    hook = _gita_hook(verse, situation)
    application = _gita_application(verse, situation)
    focus_words = _translation_keywords(verse, limit=3)
    sit_vocab = _situation_vocabulary(situation)
    seed = _gita_seed(chapter, verse_number, situation_slug, modulus=4)
    etymology_options = [
        f"{focus_words[0].capitalize()}: that word in {verse['reference']} carries more weight for {situation['label'].lower()} than it does read in isolation. It names the internal posture the situation is actually demanding.",
        f"When {situation['label'].lower()} tightens, the temptation is to reach for reassurance. This verse offers {focus_words[0]} instead - a more demanding word, and a more honest one.",
        f"The problem in {situation['label'].lower()} is rarely the circumstance itself. It is usually the loss of {focus_words[0]} that makes the circumstance unmanageable. This verse restores that word to the center.",
        f"What does {focus_words[0]} mean inside {situation['label'].lower()}? {verse['reference']} answers that exactly: not as philosophy, but as a practical description of what the next steady act looks like.",
        f"Without {focus_words[0]}, {sit_vocab[0]} fills the gap. {verse['reference']} is chosen here because it names the alternative precisely, not broadly.",
        f"In the dharmic reading of this verse, {focus_words[0]} is not a feeling to be cultivated but a posture to be chosen. {situation['label'].lower()} is where that choice becomes unavoidable.",
        f"{sit_vocab[0].capitalize()} is the inner pattern {situation['label'].lower()} reliably produces. {focus_words[0]} in {verse['reference']} is what interrupts it - not by removing the difficulty, but by changing the reader's relationship to it.",
        f"If {situation['label'].lower()} is active today, this verse asks for one thing: {focus_words[0]}. Not patience, not optimism, not strategy - specifically {focus_words[0]}, as the verse names it.",
    ]
    etymology_intro = etymology_options[_gita_seed(chapter, verse_number, situation_slug, modulus=8)]
    transit_options = [
        f"This verse often becomes more vivid during {situation['transit_label'].lower()}, when {situation['planet_label']} themes press on the same nerves this situation already exposes. In dasha language, seasons ruled by {situation['planet_label']} can magnify the demand for maturity, timing, and inner steadiness. That is why the linked transit reading helps here: it translates {verse_focus} into the emotional weather of the moment.",
        f"{situation['transit_label']} tends to light up the same part of life that this verse is already disciplining. When {situation['planet_label']} periods intensify the atmosphere, the companion transit page helps move {verse_focus} from timeless teaching into timely practice.",
        f"In transit work, {situation['transit_label']} often exposes the same weak seam that Bhagavad Gita {verse['reference']} is correcting. That makes the linked transit page useful because it carries {verse_focus} into the current emotional climate rather than leaving it on the page.",
        f"Readers often feel this verse more sharply during {situation['transit_label'].lower()}, especially when {situation['planet_label']} themes amplify urgency or pressure. The transit companion shows how {verse_focus} behaves when timing itself becomes part of the lesson.",
    ]
    transit_layer = transit_options[seed]
    prompt_seed = _gita_seed(chapter, verse_number, situation_slug, modulus=8)
    practice_prompts = [
        [
            f"Name the exact moment today when {focus_words[0]} was available but went unused.",
            f"Before the next decision arrives, ask: does this choice reflect {focus_words[1]} or does it avoid the difficulty {situation['label'].lower()} is producing?",
            f"Tonight, record whether {focus_words[2]} appeared in behavior or only in intention.",
        ],
        [
            f"Write one sentence defining what {focus_words[0]} actually looks like in your current circumstances - not in general, but today.",
            f"Choose one act before the day peaks that demonstrates {focus_words[1]} in the face of {situation['label'].lower()}.",
            f"At day's end: was {focus_words[0]} something you practiced, or something you planned to practice?",
        ],
        [
            f"Ask: where is {focus_words[0]} being crowded out by urgency or avoidance right now?",
            f"Take the next available duty and apply {focus_words[1]} to it directly, before the moment passes.",
            f"Close the day by noting one place where {focus_words[2]} shaped a choice more than reaction did.",
        ],
        [
            f"Reframe the hardest part of {situation['label'].lower()} through the lens of {focus_words[0]}: what does it look like from that angle?",
            f"Make {focus_words[1]} the rule for the next hour - not the aspiration for the day, just the rule for the next hour.",
            f"Before sleep: did {focus_words[2]} become visible in action today, or did it stay in the realm of understanding only?",
        ],
        [
            f"{focus_words[0].capitalize()} -- where is it being practiced right now, not where it is being hoped for?",
            f"The next available act: can {focus_words[1]} be the shape it takes rather than the outcome it seeks?",
            f"{focus_words[2].capitalize()} in behavior today -- note one instance, however small.",
        ],
        [
            f"{focus_words[0].capitalize()} expressed in the next ten minutes: what would that look like, concretely?",
            f"Where is {focus_words[1]} absent from {situation['label'].lower()} right now -- the exact gap, not the general one?",
            f"{focus_words[2].capitalize()} before sleep: practiced in a single act, or carried only as awareness?",
        ],
        [
            f"In {situation['label'].lower()}, {focus_words[0]} is either growing or shrinking -- which is true right now?",
            f"{focus_words[1].capitalize()} applied once before the day closes: name the act, not the intention.",
            f"Did {focus_words[2]} govern any decision today, or did something else take its place?",
        ],
        [
            f"{focus_words[0].capitalize()} as the standard for the next single choice: does the choice meet it?",
            f"Where would {focus_words[1]} change the outcome of {situation['label'].lower()} most if it were applied now?",
            f"End the day by noting whether {focus_words[2]} was present in one act, absent from all, or somewhere between.",
        ],
    ][prompt_seed]
    faq_seed = _gita_seed(chapter, verse_number, situation_slug, modulus=7)
    if faq_seed == 0:
        faq = [
            {
                "q": f"What does Bhagavad Gita {chapter}:{verse_number} mean for {situation['label'].lower()} through {focus_words[0]}?",
                "a": f"{focus_words[0].capitalize()} is the verse's central offering for this situation. Not as sentiment, but as the specific discipline the circumstance is asking for. Without it, {situation['label'].lower()} stays emotionally loud. With it, the next act becomes clearer.",
            },
            {
                "q": f"How can I apply {focus_words[0]} from this Gita verse if I am facing {situation['label'].lower()}?",
                "a": f"Start with {focus_words[0]}. Not as an ideal but as an action: name one choice today where {focus_words[0]} is the rule instead of the outcome. That is the verse made practical.",
            },
            {
                "q": f"Which timing season makes Bhagavad Gita {chapter}:{verse_number} especially vivid for {focus_words[1]}?",
                "a": f"The {sit_vocab[1]} season is the strongest companion. It amplifies the same pressure {focus_words[1]} is designed to steady, which is why the linked transit reading reinforces this verse.",
            },
        ]
    elif faq_seed == 1:
        faq = [
            {
                "q": f"Why is Bhagavad Gita {chapter}:{verse_number} a strong verse for {situation['label'].lower()} around {focus_words[0]}?",
                "a": f"Because it names {focus_words[0]} in a context that matches {situation['label'].lower()} rather than offering a general encouragement that could apply anywhere. The specificity is the point.",
            },
            {
                "q": f"What should I do first with this verse if {focus_words[0]} is being tested inside {situation['label'].lower()} today?",
                "a": f"Find where {focus_words[0]} is being tested right now - the specific place, not the general pattern. Then let the verse speak to that exact point before widening back out to interpretation.",
            },
            {
                "q": f"When does {focus_words[1]} in this verse feel hardest to hold?",
                "a": f"The {sit_vocab[1]} cycle is when {focus_words[1]} stops being theoretical. Once that window is active, the verse becomes a working reference rather than background reading.",
            },
        ]
    elif faq_seed == 2:
        faq = [
            {
                "q": f"What inner shift does Bhagavad Gita {chapter}:{verse_number} ask for in {situation['label'].lower()} through {focus_words[0]}?",
                "a": f"A move toward {focus_words[0]}, which sounds abstract until it is made into a single next action. The verse is asking for the behavior, not the feeling that would make the behavior easier.",
            },
            {
                "q": f"How can {focus_words[0]} from this verse become practical before the day ends?",
                "a": f"Carry {focus_words[0]} into one choice before the day closes. Not the most important choice - any choice. The verse becomes real in practice, not in comprehension.",
            },
            {
                "q": f"When does this verse become especially vivid in timing work around {focus_words[1]}?",
                "a": f"During the {sit_vocab[1]} season, when {focus_words[1]} is precisely what the timing pressure makes hardest. That friction is what makes the verse feel less theoretical and more necessary.",
            },
        ]
    elif faq_seed == 3:
        faq = [
            {
                "q": f"Why does Bhagavad Gita {chapter}:{verse_number} use {focus_words[2]} alongside {focus_words[0]} for {situation['label'].lower()}?",
                "a": f"{focus_words[0].capitalize()} addresses what is visible in the situation; {focus_words[2]} addresses what is interior. This verse moves from one to the other, which is why it stays usable even after the outer circumstances shift.",
            },
            {
                "q": f"What does this verse name that is easy to overlook in {situation['label'].lower()}?",
                "a": f"It names {focus_words[2]} as the quality {situation['label'].lower()} requires before the mind can settle. Without that interior move, the situation stays complicated even when the external pressure eases.",
            },
            {
                "q": f"When does this verse carry the most weight in {situation['label'].lower()}?",
                "a": f"When {sit_vocab[2]} is the undercurrent of the moment and {focus_words[2]} is the answer that keeps getting deferred. That gap is where this verse becomes most direct.",
            },
        ]
    elif faq_seed == 4:
        faq = [
            {
                "q": f"What is the opening move this verse teaches for {situation['label'].lower()} through {focus_words[0]}?",
                "a": f"Stop treating {focus_words[0]} as something to feel and start treating it as something to do. The verse is clearest when carried into the first available act of the day.",
            },
            {
                "q": f"How does {focus_words[1]} help when {situation['label'].lower()} creates pressure to react?",
                "a": f"It creates a gap between the pressure and the reaction. The verse is asking for {focus_words[1]} not as a permanent quality but as the next deliberate response.",
            },
            {
                "q": f"When is the {sit_vocab[0]} frame most useful for reading this verse?",
                "a": f"When {focus_words[0]} is what {situation['label'].lower()} is pulling away from rather than toward. The {sit_vocab[0]} frame holds the verse steady in that exact pull.",
            },
        ]
    elif faq_seed == 5:
        faq = [
            {
                "q": f"Why does this verse stay usable across repeated encounters with {situation['label'].lower()}?",
                "a": f"Because it is not addressing the event but the quality required to navigate it. {focus_words[0].capitalize()} does not expire when the situation changes; it becomes more refined with each return.",
            },
            {
                "q": f"What happens when {focus_words[1]} slips during {situation['label'].lower()}?",
                "a": f"The situation narrows. Return to the verse: not to feel {focus_words[1]} again, but to repeat the smallest act that embodies it, even imperfectly.",
            },
            {
                "q": f"How does the transit layer build on what this verse is training in {focus_words[2]}?",
                "a": f"The transit layer shows when {focus_words[2]} is under seasonal pressure. The verse supplies the same discipline through a different grammar, so both routes reinforce a single aim.",
            },
        ]
    else:
        faq = [
            {
                "q": f"What makes Bhagavad Gita {chapter}:{verse_number} a better fit for {situation['label'].lower()} than a comfort passage?",
                "a": f"A comfort passage offers reassurance; this verse offers a discipline. It names {focus_words[0]} as the correct answer to {situation['label'].lower()}: not a feeling to seek but a practice to begin.",
            },
            {
                "q": f"How small should the first step be when applying {focus_words[1]} from this verse?",
                "a": f"Small enough to complete today regardless of how {situation['label'].lower()} is going. One named act that embodies {focus_words[1]} is sufficient. Build from there.",
            },
            {
                "q": f"When does the practice suggested by this verse appear to fail in {situation['label'].lower()}?",
                "a": f"When {focus_words[1]} is treated as a destination rather than a direction. The verse is not measuring outcome; it is maintaining orientation through the {sit_vocab[2]} stage.",
            },
        ]
    title = (
        f"Bhagavad Gita c{chapter}v{verse_number} - "
        f"{focus_words[0].capitalize()} {focus_words[1].capitalize()} {focus_words[2].capitalize()} "
        f"for {situation['label']}"
    )

    return {
        "id": f"faith-gita-{chapter}-{verse_number}-{situation_slug}",
        "route": route,
        "title": title,
        "meta_title": title[:60],
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
        "summary": summary,
        "hook": hook,
        "etymology_intro": etymology_intro,
        "etymology_items": etymology_items,
        "application": application,
        "how_to_apply_title": f"How to apply Bhagavad Gita {chapter}:{verse_number} in {situation['label']}",
        "how_to_apply": how_to_apply,
        "practice_prompts": practice_prompts,
        "transit_layer": transit_layer,
        "faq": faq,
        "recitation": recitation,
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
        "recitation_collection": {
            "count": len(RECITATION_FEATURES),
            "href": "/faith/gita/recitation",
            "preview_refs": [card["reference"] for card in _featured_recitation_cards()[:4]],
        },
        "chapters": chapter_cards,
        "situations": [{"slug": item["slug"], "label": item["label"]} for item in GITA_SITUATIONS],
        "featured_verses": featured_verses,
        "phase_note": "Phase 2 is live for the Gita layer. Bible promise pages remain the next major build phase.",
    }


def get_gita_recitation_payload() -> dict:
    cards = _featured_recitation_cards()
    return {
        "title": "Bhagavad Gita Recitation Mode",
        "meta_title": "Bhagavad Gita Recitation Mode",
        "meta_description": "A featured set of Bhagavad Gita verses prepared for slow recitation, repetition, and devotional reflection.",
        "hero_title": "Bhagavad Gita Recitation Mode",
        "hero_body": (
            "This page curates a smaller set of Gita verses that work especially well for repetition. "
            "Instead of reading for volume, the goal is to stay with one verse long enough for its rhythm, language, and discipline to reshape the inner atmosphere."
        ),
        "intro_steps": [
            "Read one verse slowly for three rounds before interpreting it.",
            "Use one breath per line and pause briefly at the end of each round.",
            "After the third round, journal one sentence about the shift in mental state rather than trying to solve the whole problem.",
        ],
        "featured_verses": cards,
        "faq": [
            {
                "q": "How is recitation mode different from the regular Gita verse pages?",
                "a": "The regular pages explain and apply a verse by situation. Recitation mode slows that down and prioritizes repetition, pacing, and devotional absorption first.",
            },
            {
                "q": "Do I need Sanskrit pronunciation mastery to use this?",
                "a": "No. The transliteration lines are here to help you move steadily and respectfully. Clean pacing matters more than perfect pronunciation for this mode.",
            },
            {
                "q": "Which verses are included in the featured recitation set?",
                "a": "The current set focuses on work, surrender, protection, emotional steadiness, identity, and self-lift so the practice has immediate everyday use.",
            },
        ],
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
    urls = [f"{SITE_URL}/faith/gita", f"{SITE_URL}/faith/gita/recitation"]
    urls.extend(f"{SITE_URL}/faith/gita/chapter/{chapter}" for chapter in range(1, 19))
    for verse in _load_gita_verses():
        for situation in GITA_SITUATIONS:
            urls.append(f"{SITE_URL}/faith/gita/{verse['chapter']}-{verse['verse']}/{situation['slug']}")
    return urls
