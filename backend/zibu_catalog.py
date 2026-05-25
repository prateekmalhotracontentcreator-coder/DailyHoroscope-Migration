from __future__ import annotations

import re
from copy import deepcopy


CANONICAL_SYMBOL_NAMES = [
    "Abundance",
    "Acceptance of Optimum Health",
    "Authenticity",
    "Awakening",
    "Balance",
    "Beacon of Hope",
    "Beauty",
    "Begin Anew",
    "Blessings",
    "Buoyancy",
    "Celebration",
    "Centeredness",
    "Choose Life",
    "Clarity of Purpose",
    "Compassion",
    "Courage",
    "Creativity",
    "Divine Essence",
    "Effortless Connection",
    "Embrace",
    "Embracing the Possibilities",
    "Encouragement",
    "Evolution",
    "Expansion",
    "Faith",
    "Fluidity",
    "Forgiveness",
    "Fortitude",
    "Freedom",
    "Friendship",
    "Grace",
    "Gratitude",
    "Happiness",
    "Harmony",
    "Healing",
    "Healing Embrace",
    "Heart Song",
    "Honesty",
    "Hope",
    "Illumination",
    "Inner Peace",
    "Integrity",
    "Joy",
    "Kindness",
    "Light Heartedness",
    "Listen Within",
    "Moderation",
    "Nature",
    "Nurture",
    "Order out of Chaos",
    "Passageway",
    "Passion",
    "Patience",
    "Peacekeeper",
    "Persistence",
    "Prosperity",
    "Purity",
    "Receptivity",
    "Reciprocity",
    "Reconnection",
    "Reflection",
    "Release",
    "Release Expectations",
    "Resilience",
    "Right Action",
    "Risk",
    "Sacred Place",
    "Sacred Union",
    "Self Care",
    "Self Knowledge",
    "Serenity",
    "Simplify",
    "Soul Reintegration",
    "Synthesis",
    "Tandem Connection",
    "Thrive",
    "Tranquility",
    "Transition",
    "Trust",
    "Truth",
    "Unconditional Love",
    "Unity",
    "Universal Love",
    "Unlimited Abundance",
    "Vitality",
    "Willingness",
    "Wisdom",
    "World Peace",
]

CATEGORY_META = {
    "love": {
        "label": "Love & Relationships",
        "short_label": "Love",
        "theme": "heart-led connection, tenderness, and relational healing",
        "meta_theme": "heart-led connection and loving reciprocity",
        "chakra": "Heart Chakra",
        "element": "Water",
    },
    "abundance": {
        "label": "Abundance & Money",
        "short_label": "Abundance",
        "theme": "prosperity, momentum, and confident receiving",
        "meta_theme": "prosperity, aligned action, and receptive flow",
        "chakra": "Solar Plexus Chakra",
        "element": "Earth",
    },
    "healing": {
        "label": "Healing & Release",
        "short_label": "Healing",
        "theme": "release, recovery, and emotional renewal",
        "meta_theme": "release, renewal, and emotional restoration",
        "chakra": "Sacral Chakra",
        "element": "Water",
    },
    "protection": {
        "label": "Protection & Guidance",
        "short_label": "Protection",
        "theme": "discernment, protection, and steady guidance",
        "meta_theme": "protection, truth, and guided movement",
        "chakra": "Root Chakra",
        "element": "Earth",
    },
    "spiritual": {
        "label": "Spiritual Growth",
        "short_label": "Spiritual",
        "theme": "awakening, inner listening, and higher perspective",
        "meta_theme": "awakening, intuition, and higher wisdom",
        "chakra": "Third Eye Chakra",
        "element": "Aether",
    },
    "peace": {
        "label": "Peace & Wellbeing",
        "short_label": "Peace",
        "theme": "calm balance, gentle steadiness, and emotional ease",
        "meta_theme": "calm balance and grounded wellbeing",
        "chakra": "Heart Chakra",
        "element": "Air",
    },
    "manifestation": {
        "label": "Manifestation",
        "short_label": "Manifestation",
        "theme": "creative momentum, fresh starts, and intentional change",
        "meta_theme": "intentional change and creative momentum",
        "chakra": "Solar Plexus Chakra",
        "element": "Fire",
    },
}

CATEGORY_SLUGS = {
    "love": {
        "compassion",
        "effortless-connection",
        "embrace",
        "friendship",
        "healing-embrace",
        "heart-song",
        "kindness",
        "nurture",
        "reconnection",
        "sacred-union",
        "tandem-connection",
        "unconditional-love",
        "unity",
        "universal-love",
    },
    "abundance": {
        "abundance",
        "blessings",
        "expansion",
        "persistence",
        "prosperity",
        "right-action",
        "risk",
        "thrive",
        "unlimited-abundance",
        "vitality",
    },
    "healing": {
        "acceptance-of-optimum-health",
        "buoyancy",
        "forgiveness",
        "healing",
        "purity",
        "reflection",
        "release",
        "release-expectations",
        "resilience",
        "self-care",
        "soul-reintegration",
    },
    "protection": {
        "authenticity",
        "beacon-of-hope",
        "choose-life",
        "clarity-of-purpose",
        "courage",
        "encouragement",
        "faith",
        "fortitude",
        "honesty",
        "integrity",
        "order-out-of-chaos",
        "sacred-place",
        "trust",
        "truth",
        "wisdom",
    },
    "spiritual": {
        "awakening",
        "divine-essence",
        "illumination",
        "listen-within",
        "nature",
        "passageway",
        "self-knowledge",
        "synthesis",
    },
    "peace": {
        "balance",
        "beauty",
        "centeredness",
        "fluidity",
        "grace",
        "gratitude",
        "happiness",
        "harmony",
        "hope",
        "inner-peace",
        "joy",
        "light-heartedness",
        "moderation",
        "patience",
        "peacekeeper",
        "receptivity",
        "reciprocity",
        "serenity",
        "simplify",
        "tranquility",
        "world-peace",
    },
    "manifestation": {
        "begin-anew",
        "celebration",
        "creativity",
        "embracing-the-possibilities",
        "evolution",
        "freedom",
        "passion",
        "transition",
        "willingness",
    },
}

CATEGORY_BY_SLUG = {
    slug: category
    for category, slugs in CATEGORY_SLUGS.items()
    for slug in slugs
}


def slugify(value: str) -> str:
    cleaned = value.lower().replace("&", " and ")
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    return cleaned.strip("-")


def _resolve_category(slug: str) -> str:
    return CATEGORY_BY_SLUG[slug]


def _resolve_chakra_element(symbol: dict) -> tuple[str, str]:
    slug = symbol["slug"]
    category_meta = CATEGORY_META[symbol["category"]]

    if slug in {
        "authenticity",
        "honesty",
        "truth",
        "clarity-of-purpose",
    }:
        return "Throat Chakra", "Air"
    if slug in {
        "awakening",
        "divine-essence",
        "illumination",
        "listen-within",
        "nature",
        "passageway",
        "self-knowledge",
        "synthesis",
        "wisdom",
    }:
        return "Third Eye Chakra", "Aether"
    if slug in {
        "acceptance-of-optimum-health",
        "healing",
        "release",
        "release-expectations",
        "resilience",
        "self-care",
        "soul-reintegration",
        "vitality",
    }:
        return "Sacral Chakra", "Water"
    if slug in {
        "compassion",
        "effortless-connection",
        "friendship",
        "heart-song",
        "sacred-union",
        "unconditional-love",
        "universal-love",
    }:
        return "Heart Chakra", "Water"
    if slug in {
        "begin-anew",
        "celebration",
        "creativity",
        "freedom",
        "passion",
        "transition",
        "willingness",
    }:
        return "Sacral Chakra", "Fire"
    return category_meta["chakra"], category_meta["element"]


def _build_best_for(name: str, category: str) -> list[str]:
    lower = name.lower()
    templates = {
        "love": [
            f"heart work around {lower}",
            "deepening emotional trust",
            "softening relationship tension",
            "self-love and connection rituals",
        ],
        "abundance": [
            f"calling in {lower}",
            "money mindset and prosperity rituals",
            "career momentum and confident action",
            "receiving support without force",
        ],
        "healing": [
            f"working gently with {lower}",
            "stress release and reset rituals",
            "emotional processing with compassion",
            "recovery-focused journaling or meditation",
        ],
        "protection": [
            f"grounding into {lower}",
            "clear decision-making",
            "energetic boundaries and discernment",
            "asking for steady spiritual guidance",
        ],
        "spiritual": [
            f"meditating on {lower}",
            "reconnecting with intuition",
            "contemplative prayer or journaling",
            "opening to higher perspective",
        ],
        "peace": [
            f"returning to {lower}",
            "nervous-system calming rituals",
            "restoring harmony at home or work",
            "bedtime reflection and breathwork",
        ],
        "manifestation": [
            f"activating {lower}",
            "new beginning rituals",
            "visioning and creative focus",
            "aligned follow-through on goals",
        ],
    }
    return templates[category]


def _build_tagline(name: str, category: str) -> str:
    lower = name.lower()
    theme = CATEGORY_META[category]["theme"]
    return f"A contemplative symbol for {lower}, supported by {theme}."


def _build_meaning(name: str, category: str) -> str:
    lower = name.lower()
    theme = CATEGORY_META[category]["theme"]
    return (
        f"The Zibu symbol for {name} is used as a visual prayer focus when you want to bring {lower} "
        f"more fully into your thoughts, emotions, and actions. In angelic-symbol practice it points "
        f"you back toward {theme}, so the symbol becomes a steady reminder of the quality you are "
        f"choosing to embody. Rather than promising instant results, it works best as a ritual anchor "
        f"that helps you stay consistent with your intention."
    )


def _build_when_to_use(name: str, category: str) -> str:
    lower = name.lower()
    theme = CATEGORY_META[category]["theme"]
    return (
        f"Use this symbol when you want your next season, decision, or ritual to revolve around {lower} "
        f"instead of distraction or urgency. It is especially supportive when you need a simple visual "
        f"cue for {theme}."
    )


def _build_affirmation(name: str) -> str:
    return (
        f"I welcome the energy of {name} into my life. I move with trust, clarity, and aligned action."
    )


def _build_faq(symbol: dict) -> list[dict[str, str]]:
    name = symbol["intention"]
    lower = name.lower()
    return [
        {
            "q": f"What is the Zibu symbol for {lower}?",
            "a": (
                f"The Zibu symbol for {name} is a spiritual focus point used in meditation, journaling, "
                f"or intention work when you want to cultivate {lower} more consciously."
            ),
        },
        {
            "q": f"How do I use the Zibu symbol for {lower}?",
            "a": "Set an intention, draw or trace the symbol slowly, breathe with it for a few moments, and pair it with a simple affirmation or prayer.",
        },
        {
            "q": "Can I draw Zibu symbols myself?",
            "a": "Yes. Many people work with Zibu symbols by drawing them in a journal, on a card, or in the air during meditation so the act of tracing becomes part of the ritual.",
        },
        {
            "q": f"What chakra is associated with the Zibu symbol for {lower}?",
            "a": (
                f"This page pairs the symbol with the {symbol['chakra']} as a practical meditation anchor, "
                f"so you have a body-based place to focus while working with its intention."
            ),
        },
        {
            "q": f"When should I work with the Zibu symbol for {lower}?",
            "a": symbol["when_to_use"],
        },
    ]


def _build_how_to_use(name: str) -> list[str]:
    lower = name.lower()
    return [
        f"Set a clear intention around {lower} and take a few steady breaths before you begin.",
        f"Draw or trace the symbol in your journal, on a small card, or in the air while focusing on {lower}.",
        "Visualise warm gold light moving through the symbol and settling into your body, your home, or the situation you are praying over.",
        "Repeat the affirmation below, then release the outcome and stay available for the next aligned action.",
    ]


def _build_symbol_record(symbol_number: int, name: str) -> dict:
    slug = slugify(name)
    category = _resolve_category(slug)
    category_meta = CATEGORY_META[category]
    chakra, element = _resolve_chakra_element({"slug": slug, "category": category})
    record = {
        "slug": slug,
        "display_name": f"Zibu Symbol for {name}",
        "symbol_number": symbol_number,
        "intention": name,
        "category": category,
        "category_label": category_meta["label"],
        "category_short_label": category_meta["short_label"],
        "tagline": _build_tagline(name, category),
        "meaning": _build_meaning(name, category),
        "how_to_use": _build_how_to_use(name),
        "best_for": _build_best_for(name, category),
        "affirmation": _build_affirmation(name),
        "when_to_use": _build_when_to_use(name, category),
        "chakra": chakra,
        "element": element,
        "meta_title": f"Zibu Symbol for {name} - Meaning, How to Use & Affirmation",
        "meta_description": (
            f"The Zibu symbol for {name} is an angelic symbol for {category_meta['meta_theme']}. "
            "Discover its meaning, how to draw and use it, and an affirmation to amplify its energy."
        ),
    }
    record["faq"] = _build_faq(record)
    return record


def _build_complements(symbols: list[dict]) -> dict[str, list[str]]:
    symbols_by_category: dict[str, list[str]] = {}
    for symbol in symbols:
        symbols_by_category.setdefault(symbol["category"], []).append(symbol["slug"])

    complements: dict[str, list[str]] = {}
    for symbol in symbols:
        same_category = symbols_by_category[symbol["category"]]
        index = same_category.index(symbol["slug"])
        chosen: list[str] = []
        for offset in (1, 2, -1, 3, -2, 4):
            candidate_index = index + offset
            if 0 <= candidate_index < len(same_category):
                candidate = same_category[candidate_index]
                if candidate != symbol["slug"] and candidate not in chosen:
                    chosen.append(candidate)
            if len(chosen) == 3:
                break
        complements[symbol["slug"]] = chosen
    return complements


ZIBU_SYMBOLS = [_build_symbol_record(index, name) for index, name in enumerate(CANONICAL_SYMBOL_NAMES, start=1)]
_COMPLEMENTS = _build_complements(ZIBU_SYMBOLS)
for _symbol in ZIBU_SYMBOLS:
    _symbol["complement_symbols"] = _COMPLEMENTS[_symbol["slug"]]

ZIBU_SYMBOLS_BY_SLUG = {symbol["slug"]: symbol for symbol in ZIBU_SYMBOLS}


def list_symbol_summaries() -> list[dict]:
    fields = (
        "slug",
        "display_name",
        "symbol_number",
        "intention",
        "category",
        "category_label",
        "category_short_label",
        "tagline",
        "meta_title",
        "meta_description",
    )
    return [{field: symbol[field] for field in fields} for symbol in ZIBU_SYMBOLS]


def get_symbol(slug: str) -> dict | None:
    symbol = ZIBU_SYMBOLS_BY_SLUG.get(slug)
    return deepcopy(symbol) if symbol else None


def get_all_symbols() -> list[dict]:
    return deepcopy(ZIBU_SYMBOLS)
