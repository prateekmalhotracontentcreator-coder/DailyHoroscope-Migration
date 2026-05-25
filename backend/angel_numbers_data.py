from __future__ import annotations

from functools import lru_cache
from math import ceil


SITE_URL = "https://www.everydayhoroscope.in"
PAGE_SIZE = 1000

INTENT_ORDER = [
    "love",
    "career",
    "twin-flame",
    "manifestation",
    "health",
    "spiritual-growth",
    "family",
    "protection",
    "new-beginnings",
]

INTENT_CONFIG = {
    "love": {
        "display": "Love & Relationships",
        "theme": "heart-led honesty, emotional safety, and soulful reciprocity",
        "cta": "Choose clarity over mixed signals.",
        "strong_numbers": ["222", "444", "666", "1212", "2222"],
    },
    "career": {
        "display": "Career & Money",
        "theme": "purpose-led work, timing, and grounded progress",
        "cta": "Make the next smart move, not just the loudest one.",
        "strong_numbers": ["111", "555", "888", "1234", "4444"],
    },
    "twin-flame": {
        "display": "Twin Flame",
        "theme": "mirroring, healing, reunion cycles, and soul recognition",
        "cta": "Focus on inner alignment before outer chasing.",
        "strong_numbers": ["1111", "1212", "222", "7171", "7777"],
    },
    "manifestation": {
        "display": "Manifestation",
        "theme": "thought hygiene, aligned action, and energetic momentum",
        "cta": "Anchor the vision with one practical step.",
        "strong_numbers": ["111", "333", "555", "888", "9999"],
    },
    "health": {
        "display": "Health & Wellbeing",
        "theme": "nervous-system balance, routine, rest, and embodied healing",
        "cta": "Support the body before pushing the schedule.",
        "strong_numbers": ["444", "666", "777", "1010", "2424"],
    },
    "spiritual-growth": {
        "display": "Spiritual Growth",
        "theme": "inner guidance, awakening, discernment, and trust",
        "cta": "Create enough quiet to hear the deeper message.",
        "strong_numbers": ["333", "777", "999", "1111", "3333"],
    },
    "family": {
        "display": "Family & Home",
        "theme": "roots, belonging, repair, and supportive structure",
        "cta": "Strengthen the home base one honest conversation at a time.",
        "strong_numbers": ["222", "444", "666", "1000", "2626"],
    },
    "protection": {
        "display": "Protection & Guidance",
        "theme": "boundaries, reassurance, timing, and divine cover",
        "cta": "Move steadily and let wisdom set the pace.",
        "strong_numbers": ["444", "777", "999", "1414", "4444"],
    },
    "new-beginnings": {
        "display": "New Beginnings",
        "theme": "fresh starts, courage, release, and forward momentum",
        "cta": "Honor the ending, then step into the opening.",
        "strong_numbers": ["111", "555", "999", "1000", "2020"],
    },
}

BASE_ARCHETYPES = {
    1: {
        "label": "Initiator",
        "essence": "initiative, self-trust, and the courage to begin",
        "gift": "clear direction",
        "lesson": "moving before doubt hardens into delay",
        "themes": ["new beginnings", "leadership", "focus", "self-belief", "momentum"],
        "actions": ["claim the first step", "simplify the priority", "act with conviction"],
        "affirmation": "I trust the beginning that is opening for me.",
    },
    2: {
        "label": "Bridge",
        "essence": "cooperation, patience, and emotional intelligence",
        "gift": "harmonising people and timing",
        "lesson": "staying receptive without becoming passive",
        "themes": ["partnership", "balance", "patience", "intuition", "trust"],
        "actions": ["slow the pace", "listen deeply", "choose mutuality"],
        "affirmation": "I let trust and timing work together in my favor.",
    },
    3: {
        "label": "Messenger",
        "essence": "expression, joy, and inspired expansion",
        "gift": "creative momentum",
        "lesson": "turning insight into voice and action",
        "themes": ["creativity", "joy", "communication", "growth", "inspiration"],
        "actions": ["say what matters", "create something tangible", "follow the spark"],
        "affirmation": "My voice carries wisdom, warmth, and direction.",
    },
    4: {
        "label": "Builder",
        "essence": "stability, order, and dependable structure",
        "gift": "making support feel practical",
        "lesson": "building foundations before chasing scale",
        "themes": ["stability", "discipline", "protection", "routine", "grounding"],
        "actions": ["strengthen the base", "stay consistent", "protect your energy"],
        "affirmation": "I build my path with steadiness, patience, and grace.",
    },
    5: {
        "label": "Catalyst",
        "essence": "change, freedom, and adaptive intelligence",
        "gift": "unlocking movement where life has stalled",
        "lesson": "choosing conscious change over restless escape",
        "themes": ["change", "freedom", "adaptability", "movement", "curiosity"],
        "actions": ["release rigidity", "welcome the pivot", "choose growth over fear"],
        "affirmation": "I move with change and let it refine me.",
    },
    6: {
        "label": "Caretaker",
        "essence": "care, harmony, and the healing power of presence",
        "gift": "restoring warmth and connection",
        "lesson": "nurturing others without abandoning yourself",
        "themes": ["healing", "home", "beauty", "care", "responsibility"],
        "actions": ["restore balance", "care for the home", "lead with compassion"],
        "affirmation": "I create harmony by honoring care, truth, and tenderness.",
    },
    7: {
        "label": "Mystic",
        "essence": "reflection, intuition, and soul-level discernment",
        "gift": "deep spiritual clarity",
        "lesson": "trusting the inner signal more than external noise",
        "themes": ["intuition", "awakening", "wisdom", "reflection", "faith"],
        "actions": ["seek stillness", "trust the deeper knowing", "study the pattern"],
        "affirmation": "I trust the wisdom that rises in stillness.",
    },
    8: {
        "label": "Steward",
        "essence": "abundance, mastery, and karmic return",
        "gift": "turning effort into visible result",
        "lesson": "receiving success without losing integrity",
        "themes": ["abundance", "authority", "results", "discipline", "karma"],
        "actions": ["own your value", "lead responsibly", "stabilize the flow"],
        "affirmation": "I receive and circulate abundance with integrity.",
    },
    9: {
        "label": "Closer",
        "essence": "completion, compassion, and release",
        "gift": "helping life close one chapter cleanly",
        "lesson": "letting go before the next cycle arrives",
        "themes": ["completion", "release", "compassion", "service", "transformation"],
        "actions": ["finish the chapter", "forgive what is complete", "make room for renewal"],
        "affirmation": "I release with grace and welcome the wiser next chapter.",
    },
}

PRIORITY_SPECIAL_NUMBERS = [
    "1000",
    "1001",
    "1010",
    "1011",
    "1100",
    "1101",
    "1110",
    "1111",
    "1112",
    "1122",
    "1144",
    "1155",
    "1166",
    "1177",
    "1188",
    "1199",
    "1200",
    "1212",
    "1221",
    "1234",
    "1313",
    "1414",
    "1515",
    "1616",
    "1717",
    "1818",
    "1919",
    "2020",
    "2121",
    "2222",
    "2323",
    "2424",
    "2525",
    "2626",
    "2727",
    "2828",
    "2929",
    "3030",
    "3131",
    "3232",
    "3333",
    "3434",
    "3535",
    "3636",
    "3737",
    "3838",
    "3939",
    "4040",
    "4141",
    "4242",
    "4343",
    "4444",
    "4545",
    "4646",
    "4747",
    "4848",
    "4949",
    "5050",
    "5151",
    "5252",
    "5353",
    "5454",
    "5555",
    "5656",
    "5757",
    "5858",
    "5959",
    "6060",
    "6161",
    "6262",
    "6363",
    "6464",
    "6565",
    "6666",
    "6767",
    "6868",
    "6969",
    "7070",
    "7171",
    "7272",
    "7777",
    "8888",
    "9999",
    "10000",
]

SPECIAL_NUMBER_OVERRIDES = {
    "111": {"vibe": "manifestation portal", "tagline": "alignment, fresh momentum, and fast-moving intention"},
    "222": {"vibe": "relationship harmoniser", "tagline": "balance, patience, and trusted timing"},
    "333": {"vibe": "creative amplifier", "tagline": "expression, joy, and spiritual encouragement"},
    "444": {"vibe": "protection code", "tagline": "stability, support, and grounded reassurance"},
    "555": {"vibe": "transition trigger", "tagline": "change, movement, and liberating redirection"},
    "666": {"vibe": "restoration signal", "tagline": "care, home, and emotional rebalancing"},
    "777": {"vibe": "awakening beacon", "tagline": "intuition, study, and sacred confirmation"},
    "888": {"vibe": "abundance current", "tagline": "results, karmic return, and material flow"},
    "999": {"vibe": "completion bell", "tagline": "release, closure, and compassionate endings"},
    "1111": {"vibe": "master portal", "tagline": "awakening, synchronicity, and amplified intention"},
    "1212": {"vibe": "alignment ladder", "tagline": "faith, progress, and balanced momentum"},
    "1234": {"vibe": "ordered ascent", "tagline": "stepwise progress, structure, and clean advancement"},
    "2222": {"vibe": "master balance code", "tagline": "lasting partnership, patience, and sturdy trust"},
    "3333": {"vibe": "expansion chorus", "tagline": "creative abundance and supported growth"},
    "4444": {"vibe": "guardian wall", "tagline": "protection, discipline, and sacred structure"},
    "5555": {"vibe": "destiny pivot", "tagline": "bold change and accelerated reinvention"},
    "6666": {"vibe": "hearth keeper", "tagline": "healing, beauty, and the return to what matters"},
    "7777": {"vibe": "mystic mirror", "tagline": "deep spiritual verification and inner mastery"},
    "8888": {"vibe": "legacy builder", "tagline": "power, prosperity, and sustainable achievement"},
    "9999": {"vibe": "threshold closer", "tagline": "final release before a major rebirth"},
    "1000": {"vibe": "reset gate", "tagline": "clean beginnings, divine order, and renewed trust"},
    "10000": {"vibe": "magnified reset gate", "tagline": "scale, stewardship, and long-horizon beginnings"},
}


def reduce_to_root(number: str) -> int:
    total = sum(int(ch) for ch in number)
    while total > 9:
        total = sum(int(ch) for ch in str(total))
    return total


def is_repeating(number: str) -> bool:
    return len(set(number)) == 1


def is_mirrored(number: str) -> bool:
    return len(number) >= 4 and number[: len(number) // 2] == number[len(number) // 2 :]


def is_ascending(number: str) -> bool:
    digits = [int(ch) for ch in number]
    return all(digits[index] + 1 == digits[index + 1] for index in range(len(digits) - 1))


def is_alternating(number: str) -> bool:
    return len(number) >= 4 and len(set(number[::2])) == 1 and len(set(number[1::2])) == 1


def number_pattern(number: str) -> str:
    if is_repeating(number):
        return "pure amplification"
    if is_ascending(number):
        return "stepwise progress"
    if is_mirrored(number):
        return "mirrored reinforcement"
    if is_alternating(number):
        return "rhythmic alternation"
    if "0" in number:
        return "reset and recalibration"
    return "layered guidance"


@lru_cache(maxsize=1)
def get_core_numbers() -> tuple[str, ...]:
    numbers: list[str] = [str(value) for value in range(1, 10)]
    numbers.extend(str(value) for value in range(11, 100, 11))
    numbers.extend(str(value) for value in range(100, 1000))

    seen = set(numbers)
    reserved_tail = ["7777", "8888", "9999", "10000"]
    specials = [value for value in PRIORITY_SPECIAL_NUMBERS if value not in reserved_tail][:78]
    specials.extend(reserved_tail)

    for value in specials:
        if value not in seen:
            numbers.append(value)
            seen.add(value)
        if len(numbers) == 1000:
            break

    if len(numbers) != 1000:
        raise ValueError(f"Expected 1000 angel numbers, found {len(numbers)}")
    return tuple(numbers)


@lru_cache(maxsize=1)
def get_number_index() -> dict[str, int]:
    return {number: index for index, number in enumerate(get_core_numbers())}


def normalize_number(raw_number: str) -> str | None:
    digits = "".join(ch for ch in raw_number if ch.isdigit())
    if not digits:
        return None
    normalized = str(int(digits))
    return normalized if normalized in get_number_index() else None


def number_family_members(root: int) -> list[str]:
    return [number for number in get_core_numbers() if reduce_to_root(number) == root]


def related_numbers(number: str, root: int) -> list[str]:
    index = get_number_index()[number]
    matches: list[str] = []

    for candidate in number_family_members(root):
        if candidate != number:
            matches.append(candidate)
        if len(matches) == 2:
            break

    for offset in (-1, 1, -2, 2):
        if 0 <= index + offset < len(get_core_numbers()):
            candidate = get_core_numbers()[index + offset]
            if candidate != number and candidate not in matches:
                matches.append(candidate)
        if len(matches) == 4:
            break

    return matches[:4]


def number_label(number: str, root: int) -> str:
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return override["tagline"]
    base = BASE_ARCHETYPES[root]
    return f"{base['label'].lower()} energy with {number_pattern(number)}"


def build_key_themes(number: str, root: int) -> list[str]:
    base = list(BASE_ARCHETYPES[root]["themes"])
    extras = []
    if is_repeating(number):
        extras.extend(["amplification", "clarity"])
    if is_ascending(number):
        extras.extend(["progress", "momentum"])
    if is_mirrored(number):
        extras.extend(["balance", "echoed support"])
    if is_alternating(number):
        extras.extend(["rhythm", "course correction"])
    if "0" in number:
        extras.extend(["reset", "trust"])

    unique = []
    for value in base + extras:
        if value not in unique:
            unique.append(value)
    return unique[:6]


def build_vibration(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return (
            f"{number} carries a {override['vibe']} wrapped in the root-{root} current of "
            f"{archetype['essence']}. It tends to show up when life wants decisive awareness, not passive drifting."
        )
    return (
        f"Angel number {number} carries the root-{root} current of {archetype['essence']}, expressed through "
        f"a pattern of {pattern}. It asks you to notice what is ready to shift, stabilize, or begin."
    )


def build_summary(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    return (
        f"Angel number {number} highlights {archetype['essence']}. When this sequence keeps repeating, "
        f"it usually means your next step becomes easier once you respond with {archetype['gift']}."
    )


def build_seeing_it_means(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    return (
        f"Seeing {number} repeatedly is often a timing signal rather than random coincidence. "
        f"It draws your attention back to {archetype['essence']} and asks where life is inviting you into "
        f"{archetype['lesson']}. If the number appears during stress, it is a reminder to regulate first and respond second. "
        f"If it appears during momentum, it is a nudge to keep moving with intention instead of scattering your focus."
    )


def build_core_actions(number: str, root: int) -> list[str]:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    return [
        f"Name the one situation where {number} is asking for {archetype['gift']}.",
        f"Use this {pattern} phase to {archetype['actions'][0]} before the window passes.",
        f"End the day by choosing one concrete way to {archetype['actions'][2]}.",
    ]


def build_core_affirmation(number: str, root: int) -> str:
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return f"I receive the {override['vibe']} of {number} and act in alignment with it."
    return BASE_ARCHETYPES[root]["affirmation"]


@lru_cache(maxsize=1)
def build_intent_base_matrix() -> dict[str, dict[int, dict[str, object]]]:
    matrix: dict[str, dict[int, dict[str, object]]] = {}
    for intent, config in INTENT_CONFIG.items():
        matrix[intent] = {}
        for root, archetype in BASE_ARCHETYPES.items():
            matrix[intent][root] = {
                "opening": (
                    f"In {config['display'].lower()}, the root-{root} {archetype['label'].lower()} current emphasizes "
                    f"{config['theme']}."
                ),
                "message": (
                    f"This vibration is strongest when you meet the moment with {archetype['gift']}. "
                    f"The lesson is less about forcing the answer and more about {archetype['lesson']}."
                ),
                "actions": [
                    f"{config['cta']}",
                    f"Lean into {archetype['actions'][0]} in this area of life.",
                    f"Let {archetype['actions'][1]} guide your next decision.",
                ],
            }
    return matrix


def build_intent_subtitle(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    if is_repeating(number):
        return f"a magnified message about {config['display'].lower()} and {base['gift']}"
    if is_ascending(number):
        return f"step-by-step guidance for {config['display'].lower()}"
    if is_mirrored(number):
        return f"a balance check for {config['display'].lower()}"
    return f"what this sequence is pointing out in {config['display'].lower()}"


def build_intent_teaser(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return (
        f"{number} brings the root-{root} energy of {base['essence']} into {config['display'].lower()}, "
        f"highlighting {config['theme']}."
    )


def build_intent_affirmation(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return (
        f"I welcome the guidance of {number} and allow {base['gift']} to shape my "
        f"{config['display'].lower()} journey."
    )


def build_intent_related_numbers(intent: str, number: str, root: int) -> list[str]:
    preferred = [candidate for candidate in INTENT_CONFIG[intent]["strong_numbers"] if candidate != number]
    family = [candidate for candidate in related_numbers(number, root) if candidate not in preferred]
    return (preferred + family)[:3]


def build_core_faq(number: str, root: int) -> list[dict[str, str]]:
    base = BASE_ARCHETYPES[root]
    return [
        {
            "q": f"What does angel number {number} mean?",
            "a": f"{number} points to {base['essence']}. Its message is usually about responding with {base['gift']} instead of staying stuck in hesitation.",
        },
        {
            "q": f"Why do I keep seeing {number} everywhere?",
            "a": f"Repeating contact with {number} usually shows up when one life lesson is trying to get your full attention. It is a cue to notice the pattern, the timing, and your emotional state in the moment.",
        },
        {
            "q": f"Is {number} a good sign?",
            "a": f"Yes. Even when {number} arrives during pressure, it is still a supportive sign because it helps you recognize the wiser response before the situation hardens.",
        },
        {
            "q": f"What should I do when I see {number}?",
            "a": f"Pause, ground yourself, and take one action that honors {base['gift']}. Angel numbers work best as prompts for aligned movement, not passive superstition.",
        },
        {
            "q": f"Which numbers are related to {number}?",
            "a": f"Numbers that reduce to {root} often carry a similar lesson. Neighboring sequences can also matter because they show how the message is evolving around you.",
        },
    ]


def build_intent_faq(number: str, intent: str, root: int) -> list[dict[str, str]]:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return [
        {
            "q": f"What does {number} mean for {config['display'].lower()}?",
            "a": f"In {config['display'].lower()}, {number} emphasizes {config['theme']}. The healthiest response is to meet that area with {base['gift']}.",
        },
        {
            "q": f"Is {number} a strong {intent.replace('-', ' ')} angel number?",
            "a": f"Yes. The root-{root} current naturally supports {config['display'].lower()} through {base['essence']}, which is why the sequence tends to feel personally relevant in this domain.",
        },
        {
            "q": f"What should I do after seeing {number} for {config['display'].lower()}?",
            "a": f"Use the sighting as a prompt to make one honest, grounded move. Angel number guidance becomes clearer when insight is paired with action.",
        },
        {
            "q": f"Does {number} promise an outcome in {config['display'].lower()}?",
            "a": f"No angel number bypasses free will. {number} is better understood as guidance about the energy available to you and the lesson asking for participation.",
        },
        {
            "q": f"Which other numbers support this same message?",
            "a": f"Sequences with a similar root number or intent emphasis often echo this lesson. Related numbers can show whether the message is deepening, widening, or preparing for closure.",
        },
    ]


def build_core_record(number: str) -> dict[str, object]:
    root = reduce_to_root(number)
    display = number
    headline = f"{display} Angel Number - Meaning, Message & What To Do"
    record = {
        "number": number,
        "display": display,
        "headline": headline,
        "summary": build_summary(number, root),
        "numerology_base": str(root),
        "key_themes": build_key_themes(number, root),
        "vibration": build_vibration(number, root),
        "seeing_it_means": build_seeing_it_means(number, root),
        "what_to_do": build_core_actions(number, root),
        "affirmation": build_core_affirmation(number, root),
        "meta_title": f"{display} Angel Number Meaning - Signs, Love, Career & More | EverydayHoroscope",
        "meta_description": (
            f"Seeing {display} everywhere? Discover the meaning of angel number {display} and what it signals for love, career, manifestation, and spiritual growth."
        ),
        "faq": build_core_faq(number, root),
        "related_numbers": related_numbers(number, root),
        "canonical_url": f"{SITE_URL}/angel-numbers/{display}",
        "tagline": number_label(number, root),
    }
    record["intent_summaries"] = [build_intent_summary(number, intent) for intent in INTENT_ORDER]
    return record


def build_intent_summary(number: str, intent: str) -> dict[str, object]:
    root = reduce_to_root(number)
    config = INTENT_CONFIG[intent]
    return {
        "intent": intent,
        "display_name": config["display"],
        "headline": f"{number} Angel Number {config['display']} - {build_intent_subtitle(number, intent, root).capitalize()}",
        "teaser": build_intent_teaser(number, intent, root),
        "url": f"/angel-numbers/{number}/{intent}",
    }


def build_intent_record(number: str, intent: str) -> dict[str, object]:
    root = reduce_to_root(number)
    config = INTENT_CONFIG[intent]
    template = build_intent_base_matrix()[intent][root]
    subtitle = build_intent_subtitle(number, intent, root)
    return {
        "number": number,
        "intent": intent,
        "display_name": config["display"],
        "headline": f"{number} Angel Number {config['display']} - {subtitle.capitalize()}",
        "subtitle": subtitle,
        "opening": (
            f"{number} often appears when {config['display'].lower()} needs a clearer rhythm. "
            f"{template['opening']}"
        ),
        "message": (
            f"Angel number {number} does not ask for panic or fantasy. {template['message']} "
            f"In practice, this means choosing the response that feels both spiritually clean and practically sustainable."
        ),
        "action_steps": list(template["actions"]),
        "affirmation": build_intent_affirmation(number, intent, root),
        "faq": build_intent_faq(number, intent, root),
        "related_numbers": build_intent_related_numbers(intent, number, root),
        "meta_title": f"{number} Angel Number {config['display']} Meaning | EverydayHoroscope",
        "meta_description": (
            f"Discover what angel number {number} means for {config['display'].lower()}. "
            f"Read the message, action steps, affirmation, and related signs."
        ),
        "canonical_url": f"{SITE_URL}/angel-numbers/{number}/{intent}",
        "all_intents": [{"slug": slug, "display_name": INTENT_CONFIG[slug]["display"]} for slug in INTENT_ORDER],
    }


def build_hub_intro() -> str:
    return (
        "Angel numbers are repeating or symbolically charged number sequences that many people notice during turning points, decisions, and seasons of growth. "
        "This hub brings together 1,000 angel number meanings, from the classic repeating patterns to deeper mirrored and sequence-based codes. "
        "Each number can also be explored through nine life intents so the message feels practical, not abstract. "
        "Use the search, popular numbers grid, and numerology families below to follow the number that keeps finding you."
    )


@lru_cache(maxsize=1)
def build_hub_payload() -> dict[str, object]:
    popular_numbers = [
        {"number": "111", "display": "111", "theme": "Manifestation gate"},
        {"number": "222", "display": "222", "theme": "Trust the timing"},
        {"number": "333", "display": "333", "theme": "Creative support"},
        {"number": "444", "display": "444", "theme": "Protected and grounded"},
        {"number": "555", "display": "555", "theme": "Change is here"},
        {"number": "666", "display": "666", "theme": "Return to balance"},
        {"number": "777", "display": "777", "theme": "Awakening signal"},
        {"number": "888", "display": "888", "theme": "Abundance current"},
        {"number": "999", "display": "999", "theme": "Cycle closing"},
        {"number": "1111", "display": "1111", "theme": "Portal energy"},
        {"number": "1212", "display": "1212", "theme": "Aligned progress"},
        {"number": "2222", "display": "2222", "theme": "Master partnership"},
        {"number": "3333", "display": "3333", "theme": "Expansion chorus"},
        {"number": "4444", "display": "4444", "theme": "Guardian support"},
        {"number": "5555", "display": "5555", "theme": "Destiny pivot"},
        {"number": "6666", "display": "6666", "theme": "Healing the home"},
        {"number": "7777", "display": "7777", "theme": "Mystic confirmation"},
        {"number": "8888", "display": "8888", "theme": "Legacy abundance"},
        {"number": "9999", "display": "9999", "theme": "Final release"},
        {"number": "1000", "display": "000", "theme": "Zero-point reset"},
    ]

    families = []
    for root in range(1, 10):
        members = number_family_members(root)
        families.append(
            {
                "root": root,
                "label": f"Base {root} - {BASE_ARCHETYPES[root]['label']}",
                "theme": BASE_ARCHETYPES[root]["essence"],
                "numbers": members,
                "preview": members[:18],
            }
        )

    faq = [
        {
            "q": "What are angel numbers?",
            "a": "Angel numbers are number patterns people interpret as meaningful timing cues or spiritual nudges. They are less about superstition and more about noticing where life is asking for awareness.",
        },
        {
            "q": "Do angel numbers have different meanings in love and career?",
            "a": "Yes. The same number can point to different applications depending on the area of life in focus, which is why this module includes intent-specific pages for each core number.",
        },
        {
            "q": "How do I find my angel number meaning fast?",
            "a": "Use the search bar if you already know the sequence, or browse popular numbers and numerology families if you want to understand the wider pattern behind it.",
        },
        {
            "q": "What is a numerology root?",
            "a": "A numerology root is the single-digit sum of a number. It helps group numbers into energetic families so patterns like 111, 444, and 777 can be understood at both the sequence and base-vibration level.",
        },
        {
            "q": "Should I act every time I see an angel number?",
            "a": "You do not need to overreact to every sighting. The healthiest approach is to notice the repeating context, reflect honestly, and then take one grounded action if the message feels relevant.",
        },
    ]

    return {
        "headline": "Angel Numbers - Meanings, Messages & What They Mean for You",
        "intro": build_hub_intro(),
        "popular_numbers": popular_numbers,
        "intent_categories": [
            {
                "slug": slug,
                "display_name": config["display"],
                "theme": config["theme"],
                "strong_numbers": config["strong_numbers"],
            }
            for slug, config in INTENT_CONFIG.items()
        ],
        "numerology_families": families,
        "how_to_work_with_angel_numbers": [
            "Notice the exact number, the time, and the life situation around the sighting.",
            "Read both the core meaning and the intent page that matches your current concern.",
            "Look for the practical invitation in the message rather than treating it like a fixed prediction.",
            "Repeat the affirmation and follow through with one concrete action the same day.",
        ],
        "faq": faq,
        "counts": {"core_numbers": 1000, "intent_pages": 9000, "total_pages": 10001},
    }


def get_core_record(number: str) -> dict[str, object]:
    return build_core_record(number)


def get_intent_record(number: str, intent: str) -> dict[str, object]:
    return build_intent_record(number, intent)


def iter_core_records() -> list[dict[str, object]]:
    return [get_core_record(number) for number in get_core_numbers()]


def iter_intent_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for number in get_core_numbers():
        for intent in INTENT_ORDER:
            records.append(get_intent_record(number, intent))
    return records


def build_sitemap_paths() -> list[str]:
    paths = ["/angel-numbers"]
    for number in get_core_numbers():
        paths.append(f"/angel-numbers/{number}")
        for intent in INTENT_ORDER:
            paths.append(f"/angel-numbers/{number}/{intent}")
    return paths


def sitemap_page_count() -> int:
    return ceil(len(build_sitemap_paths()) / PAGE_SIZE)


def get_sitemap_page(page: int) -> dict[str, object]:
    paths = build_sitemap_paths()
    page_count = sitemap_page_count()
    if page < 1 or page > page_count:
        raise ValueError(f"page must be between 1 and {page_count}")
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    return {
        "page": page,
        "page_count": page_count,
        "urls": [f"{SITE_URL}{path}" for path in paths[start:end]],
    }
