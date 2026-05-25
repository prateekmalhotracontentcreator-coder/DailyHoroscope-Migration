from __future__ import annotations

from datetime import date
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, field_validator


router = APIRouter(prefix="/api/lo-shu", tags=["lo-shu"])

GRID_ROWS: tuple[tuple[int, int, int], ...] = (
    (4, 9, 2),
    (3, 5, 7),
    (8, 1, 6),
)

PYTHAGOREAN_MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8,
}

NUMBER_REFERENCE: dict[int, dict[str, str]] = {
    1: {"planet": "Sun", "day": "Sunday", "archetype": "King"},
    2: {"planet": "Moon", "day": "Monday", "archetype": "Queen"},
    3: {"planet": "Jupiter", "day": "Thursday", "archetype": "Devguru"},
    4: {"planet": "Rahu", "day": "Saturday", "archetype": "Path Breaker"},
    5: {"planet": "Mercury", "day": "Wednesday", "archetype": "Prince"},
    6: {"planet": "Venus", "day": "Friday", "archetype": "Harmoniser"},
    7: {"planet": "Ketu", "day": "Tuesday", "archetype": "Mystic"},
    8: {"planet": "Saturn", "day": "Saturday", "archetype": "Judge"},
    9: {"planet": "Mars", "day": "Tuesday", "archetype": "Warrior"},
}

MISSING_NUMBER_BLUEPRINTS: dict[int, dict[str, Any]] = {
    1: {
        "effect_summary": "Missing 1 usually points to a softer sense of self-direction. People may hesitate before taking the lead or may wait for outside validation before acting.",
        "traits_affected": ["leadership", "self-confidence", "decision-making", "personal identity"],
        "life_areas_impacted": ["career direction", "self-expression", "public presence"],
        "remedies": [
            "Start Sundays with a clear personal intention instead of reacting to the day.",
            "Spend time in early sunlight or offer a simple gratitude practice at sunrise.",
            "Choose one independent decision each week and follow through without over-seeking approval.",
            "Use warm gold, copper, or saffron accents when you need confidence and visibility.",
        ],
        "affirmation": "I trust my voice, my timing, and my ability to lead my own life.",
        "related_missing": [4, 9],
        "focus_trait": "confidence and leadership",
    },
    2: {
        "effect_summary": "Missing 2 can show up as emotional over-sensitivity on some days and emotional distance on others. Cooperation, patience, and intuition may need conscious nurturing.",
        "traits_affected": ["emotional balance", "intuition", "cooperation", "patience"],
        "life_areas_impacted": ["relationships", "teamwork", "inner calm"],
        "remedies": [
            "Use Mondays for softer pacing, hydration, and emotional check-ins.",
            "Wear white, pearl, or silver tones when you want more calm and receptivity.",
            "Pause before responding in charged situations so instinct can settle into clarity.",
            "Keep a moon journal or evening reflection habit to strengthen emotional awareness.",
        ],
        "affirmation": "I respond with calm, softness, and emotional wisdom.",
        "related_missing": [5, 8],
        "focus_trait": "emotional steadiness",
    },
    3: {
        "effect_summary": "Missing 3 often reduces optimism and expressive warmth. The person may know a lot internally but struggle to share insight with confidence or joy.",
        "traits_affected": ["optimism", "communication", "creative expression", "faith"],
        "life_areas_impacted": ["learning", "mentorship", "public speaking"],
        "remedies": [
            "Reserve Thursdays for study, teaching, or sharing one idea clearly.",
            "Wear yellow or gold when you want to feel brighter and more expressive.",
            "Practice speaking one honest thought instead of editing yourself too early.",
            "Create something small each week so inspiration turns into a visible habit.",
        ],
        "affirmation": "My voice carries wisdom, warmth, and generous expression.",
        "related_missing": [4, 8],
        "focus_trait": "expression and optimism",
    },
    4: {
        "effect_summary": "Missing 4 can make life feel less structured than it needs to be. Discipline, consistency, and the ability to build steady systems may require extra attention.",
        "traits_affected": ["discipline", "structure", "consistency", "practical planning"],
        "life_areas_impacted": ["work routines", "planning", "long-term stability"],
        "remedies": [
            "Break big goals into repeatable weekly systems instead of depending on mood.",
            "Use Saturdays for decluttering, grounding, and catching up on unfinished tasks.",
            "Add earthy greens or muted neutrals to workspaces that need focus and steadiness.",
            "Track one habit for 40 days to build rhythm instead of chasing quick results.",
        ],
        "affirmation": "I create stability through steady action and clear structure.",
        "related_missing": [3, 8],
        "focus_trait": "discipline and order",
    },
    5: {
        "effect_summary": "Missing 5 may create mental restlessness, inconsistent communication, or difficulty adapting smoothly to change. Flexibility improves when the mind is grounded first.",
        "traits_affected": ["adaptability", "communication", "mental balance", "versatility"],
        "life_areas_impacted": ["decision-making", "travel", "daily coordination"],
        "remedies": [
            "Use Wednesdays for planning, writing, and finishing open loops.",
            "Keep your schedule simple when too many choices begin to scatter your energy.",
            "Wear fresh green or light mercurial tones when you need clarity and adaptability.",
            "Practice one-minute pauses before speaking so communication becomes cleaner and calmer.",
        ],
        "affirmation": "My mind is flexible, clear, and balanced under change.",
        "related_missing": [2, 6],
        "focus_trait": "adaptability and communication",
    },
    6: {
        "effect_summary": "Missing 6 can show as uneven relationship harmony or discomfort around responsibility, beauty, and emotional reciprocity. Balance grows when care becomes intentional.",
        "traits_affected": ["harmony", "responsibility", "relationship care", "aesthetic balance"],
        "life_areas_impacted": ["love life", "family duties", "home environment"],
        "remedies": [
            "Use Fridays to restore your environment and make one relationship gesture with care.",
            "Bring more softness into daily routines through music, fragrance, or visual order.",
            "Wear cream, rose, or gentle pastel tones when you want relational ease.",
            "Choose one responsibility to complete beautifully rather than many things halfway.",
        ],
        "affirmation": "I give and receive care with grace, steadiness, and love.",
        "related_missing": [5, 9],
        "focus_trait": "harmony and responsibility",
    },
    7: {
        "effect_summary": "Missing 7 may reduce trust in inner guidance. The person can become overly practical, impatient with reflection, or disconnected from the quieter meaning behind events.",
        "traits_affected": ["intuition", "inner reflection", "faith", "spiritual depth"],
        "life_areas_impacted": ["inner life", "healing", "long-term perspective"],
        "remedies": [
            "Protect time for silence, prayer, journaling, or reflective walking every week.",
            "Use Tuesdays for disciplined spiritual practice rather than scattered effort.",
            "Notice repeated patterns in life instead of dismissing every nudge as coincidence.",
            "Choose indigo, sea green, or muted spiritual tones when you want deeper calm.",
        ],
        "affirmation": "I trust the quiet wisdom rising from within me.",
        "related_missing": [2, 3],
        "focus_trait": "intuition and reflection",
    },
    8: {
        "effect_summary": "Missing 8 often weakens endurance, patience, and strategic realism. Opportunities may be present, but long-range discipline can be harder to sustain.",
        "traits_affected": ["endurance", "patience", "material discipline", "strategic maturity"],
        "life_areas_impacted": ["finances", "career growth", "long-term commitments"],
        "remedies": [
            "Treat Saturdays as a reset for budgeting, planning, and reality-checking priorities.",
            "Avoid fast-money temptations and reward yourself for slow, consistent progress.",
            "Use dark blue, charcoal, or grounding tones when you need restraint and seriousness.",
            "Commit to one long game instead of restarting every time results feel delayed.",
        ],
        "affirmation": "I build success through patience, integrity, and steady endurance.",
        "related_missing": [4, 2],
        "focus_trait": "endurance and discipline",
    },
    9: {
        "effect_summary": "Missing 9 can show up as reduced courage, weak follow-through under pressure, or discomfort with direct action. Energy improves when purpose becomes emotionally meaningful.",
        "traits_affected": ["courage", "drive", "assertiveness", "protective strength"],
        "life_areas_impacted": ["conflict handling", "leadership under pressure", "execution"],
        "remedies": [
            "Use Tuesdays for action-oriented tasks you have been postponing.",
            "Move the body regularly so stored frustration turns into healthy momentum.",
            "Wear maroon, red, or copper accents when you need bravery and momentum.",
            "Define the reason behind your action first so courage connects to purpose, not impulse.",
        ],
        "affirmation": "I act with courage, purpose, and clean inner strength.",
        "related_missing": [1, 6],
        "focus_trait": "courage and initiative",
    },
}

ARROW_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "intellect": {
        "name": "Arrow of Intellect",
        "numbers": [4, 9, 2],
        "theme": "Mind plane",
        "effect_present": "A complete 4-9-2 line suggests sharp thinking, strong recall, and the ability to study patterns quickly. This arrow usually supports analysis, mental stamina, and clear situational reading.",
        "effect_missing": "When 4, 9, and 2 are all absent, mental steadiness can feel inconsistent. Focus, retention, and confident analysis usually improve only after deliberate practice and routine.",
        "real_life_traits": ["strong memory", "analytical thinking", "quick pattern recognition", "clear mental framing"],
        "shadow_trait": "Can become mentally rigid or quietly superior when intellect is over-identified with self-worth.",
        "strength_band": "high",
        "aliases": ["mind", "thought-mind", "arrow-of-intellect"],
    },
    "spirituality": {
        "name": "Arrow of Spirituality",
        "numbers": [3, 5, 7],
        "theme": "Soul plane",
        "effect_present": "A complete 3-5-7 line brings emotional depth, intuition, and a stronger pull toward meaning. It often supports empathy, reflection, creativity, and a quieter spiritual intelligence.",
        "effect_missing": "If 3, 5, and 7 are all absent, emotional isolation can build over time. Joy, empathy, and inner connection may need to be developed intentionally rather than arriving naturally.",
        "real_life_traits": ["intuition", "compassion", "emotional sensitivity", "creative depth"],
        "shadow_trait": "Can feel too porous or idealistic if emotional boundaries are weak.",
        "strength_band": "high",
        "aliases": ["spiritual", "soul", "willpower", "body-soul", "arrow-of-spirituality"],
    },
    "prosperity": {
        "name": "Arrow of Prosperity",
        "numbers": [8, 1, 6],
        "theme": "Practical plane",
        "effect_present": "A complete 8-1-6 line supports work ethic, completion energy, and stronger material execution. It often appears in people who can organise effort and build visible results over time.",
        "effect_missing": "When 8, 1, and 6 are all absent, ambition may fade or scatter. Financial decisions can become reactive, and shortcuts may look more attractive than patient progress.",
        "real_life_traits": ["practical effort", "business instinct", "task completion", "material organisation"],
        "shadow_trait": "Can become overly status-driven or too focused on outcomes over inner balance.",
        "strength_band": "high",
        "aliases": ["activity", "physical", "prosperity-plane", "arrow-of-prosperity"],
    },
    "planner": {
        "name": "Arrow of Planner",
        "numbers": [4, 3, 8],
        "theme": "Thought column",
        "effect_present": "A full 4-3-8 column is excellent for systems thinking, preparation, and planning ahead. It gives a strategic mindset that prefers structure, sequencing, and long-range positioning.",
        "effect_missing": "If 4, 3, and 8 are missing together, life can feel disorganised or directionless. Ideas may appear, but the system required to hold them is usually underdeveloped.",
        "real_life_traits": ["discipline", "strategic planning", "organisation", "future focus"],
        "shadow_trait": "Can turn shrewd, overly controlling, or politically calculating when balance is lost.",
        "strength_band": "high",
        "aliases": ["thought", "thought-plane", "arrow-of-planner"],
    },
    "will-power": {
        "name": "Arrow of Will Power",
        "numbers": [9, 5, 1],
        "theme": "Will column",
        "effect_present": "A complete 9-5-1 line is one of the clearest markers of determination. It supports persistence, expressive clarity, and the ability to keep moving until the work is finished.",
        "effect_missing": "When 9, 5, and 1 are all absent, decisions can be delayed for too long. People-pleasing, hesitation, and difficulty voicing a firm position tend to increase.",
        "real_life_traits": ["persistence", "goal focus", "communication strength", "inner authority"],
        "shadow_trait": "Can become stubborn, inflexible, or too attached to winning the argument.",
        "strength_band": "high",
        "aliases": ["will", "willpower", "arrow-of-will", "arrow-of-will-power"],
    },
    "action": {
        "name": "Arrow of Action",
        "numbers": [2, 7, 6],
        "theme": "Action column",
        "effect_present": "A full 2-7-6 line helps ideas move into lived action. This arrow supports practical execution, embodied learning, and a hands-on style that prefers doing over endless theorising.",
        "effect_missing": "When the 2-7-6 action column is empty, motivation can feel uneven and opportunities may be missed through delay. Momentum improves when action is broken into immediate, tangible steps.",
        "real_life_traits": ["execution", "hands-on learning", "active effort", "practical follow-through"],
        "shadow_trait": "Can act too quickly or stay busy without enough reflection if the line becomes overactive.",
        "strength_band": "high",
        "aliases": ["activity-column", "planner-action", "arrow-of-action"],
    },
    "emotional-balance": {
        "name": "Arrow of Emotional Balance",
        "numbers": [4, 5, 6],
        "theme": "Rajayoga diagonal",
        "effect_present": "The 4-5-6 diagonal is treated as a Rajayoga indicator in the decoded source. It suggests strong inner balance between sensitivity, communication, and worldly functioning, which can translate into visible life success.",
        "effect_missing": "When 4, 5, and 6 are all absent, suspicion and mental negativity can color relationships and choices. Trust, emotional regulation, and grounded interpretation of events become central growth areas.",
        "real_life_traits": ["balanced responses", "social ease", "measured judgment", "stable success drive"],
        "shadow_trait": "Can become image-conscious or over-managing when success and composure become identity armor.",
        "strength_band": "extreme",
        "rajayoga": True,
        "aliases": ["rajayoga-1", "suspicion", "arrow-of-emotional-balance"],
    },
    "determination": {
        "name": "Arrow of Determination",
        "numbers": [2, 5, 8],
        "theme": "Rajayoga diagonal",
        "effect_present": "The 2-5-8 diagonal is the second Rajayoga pattern in this system. It points to disciplined resolve, honest effort, and the ability to keep sight of a goal even when conditions are slow or demanding.",
        "effect_missing": "If 2, 5, and 8 are all absent, frustration and instability can repeat until patience and foresight are strengthened. Reactive choices usually create more losses than direct obstacles do.",
        "real_life_traits": ["resolve", "honesty", "long-range focus", "steadiness under pressure"],
        "shadow_trait": "Can become severe, overly self-pressured, or emotionally tight when determination loses softness.",
        "strength_band": "extreme",
        "rajayoga": True,
        "aliases": ["rajayoga-2", "frustration", "instability", "compassion", "arrow-of-determination"],
    },
}

# The decoded source labels the missing action arrow as 8-7-6 in one place, but
# the Lo Shu grid geometry and the commission's own calculation logic make the
# inverse action column 2-7-6. Runtime logic follows the grid geometry.
MISSING_ARROW_LABELS = {
    "intellect": "Arrow of Poor Memory",
    "spirituality": "Arrow of Loneliness",
    "prosperity": "Arrow of Losses",
    "planner": "Arrow of Confusion",
    "will-power": "Arrow of Indecision",
    "action": "Arrow of Apathy",
    "emotional-balance": "Arrow of Suspicion",
    "determination": "Arrow of Frustration",
}

ARROW_DISPLAY_ORDER = [
    "intellect",
    "spirituality",
    "prosperity",
    "planner",
    "will-power",
    "action",
    "emotional-balance",
    "determination",
]

ARROW_ALIAS_TO_SLUG: dict[str, str] = {}
for _slug, _payload in ARROW_BLUEPRINTS.items():
    ARROW_ALIAS_TO_SLUG[_slug] = _slug
    for _alias in _payload.get("aliases", []):
        ARROW_ALIAS_TO_SLUG[_alias] = _slug


class LoShuCalculateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str
    dob: date
    gender: Literal["male", "female"]

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("full_name is required")
        if not any(char.isalpha() for char in value):
            raise ValueError("full_name must contain alphabetic characters")
        return value

    @field_validator("gender", mode="before")
    @classmethod
    def normalize_gender(cls, value: Any) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value


def reduce_to_single(value: int) -> int:
    if value <= 0:
        return 0
    while value > 9:
        value = sum(int(char) for char in str(value))
    return value


def build_name_number(full_name: str) -> int:
    total = sum(PYTHAGOREAN_MAP[char.upper()] for char in full_name if char.isalpha())
    return reduce_to_single(total)


def build_kua_number(birth_date: date, gender: Literal["male", "female"]) -> int:
    year_sum = reduce_to_single(sum(int(char) for char in str(birth_date.year)))
    if gender == "female":
        return reduce_to_single(year_sum + 10)
    return reduce_to_single(11 - year_sum)


def build_number_counts(full_name: str, birth_date: date, gender: Literal["male", "female"]) -> tuple[dict[int, int], dict[str, int]]:
    dob_digits = [int(char) for char in birth_date.strftime("%d%m%Y") if char != "0"]
    day_digits = [int(char) for char in str(birth_date.day)] if birth_date.day > 9 else []
    basic_number = reduce_to_single(birth_date.day)
    destiny_number = reduce_to_single(sum(int(char) for char in birth_date.strftime("%d%m%Y") if char != "0"))
    kua_number = build_kua_number(birth_date, gender)
    name_number = build_name_number(full_name)

    digits = [*dob_digits, *day_digits, destiny_number, kua_number, name_number]
    counts = {number: 0 for number in range(1, 10)}
    for digit in digits:
        if 1 <= digit <= 9:
            counts[digit] += 1

    return counts, {
        "basic_number": basic_number,
        "destiny_number": destiny_number,
        "kua_number": kua_number,
        "name_number": name_number,
    }


def build_grid_rows(counts: dict[int, int]) -> list[list[dict[str, Any]]]:
    return [
        [{"number": number, "count": counts.get(number, 0), "present": counts.get(number, 0) > 0} for number in row]
        for row in GRID_ROWS
    ]


def build_missing_number_document(number: int) -> dict[str, Any]:
    if number not in MISSING_NUMBER_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Missing number not found")

    ref = NUMBER_REFERENCE[number]
    blueprint = MISSING_NUMBER_BLUEPRINTS[number]
    faq_items = [
        {
            "question": f"What does missing number {number} mean in Lo Shu Grid?",
            "answer": blueprint["effect_summary"],
        },
        {
            "question": f"Which planet rules number {number} in Lo Shu Grid?",
            "answer": f"Number {number} is linked with {ref['planet']} and is traditionally supported through {ref['day']} routines and symbolic balancing practices.",
        },
        {
            "question": f"Is missing {number} always bad?",
            "answer": f"Missing {number} does not mean failure. It usually points to an area that develops through practice rather than arriving as a natural default.",
        },
        {
            "question": f"How can I balance missing number {number}?",
            "answer": "Start with consistent habits, symbolic color or day alignment, and practical behavior shifts that strengthen the missing trait in daily life.",
        },
        {
            "question": f"What life area is most affected by missing number {number}?",
            "answer": f"The strongest impact is usually felt around {blueprint['focus_trait']}, with ripple effects in {', '.join(blueprint['life_areas_impacted'][:2])}.",
        },
    ]
    related_missing = blueprint["related_missing"]
    return {
        "number": number,
        "slug": f"missing-{number}",
        "title": f"Missing Number {number} in Lo Shu Grid - What It Means and How to Balance It",
        "ruling_planet": ref["planet"],
        "ruling_day": ref["day"],
        "archetype": ref["archetype"],
        "effect_summary": blueprint["effect_summary"],
        "traits_affected": blueprint["traits_affected"],
        "life_areas_impacted": blueprint["life_areas_impacted"],
        "remedies": blueprint["remedies"],
        "affirmation": blueprint["affirmation"],
        "faq": faq_items,
        "related_missing": related_missing,
        "related_pages": [
            {
                "number": related,
                "slug": f"missing-{related}",
                "title": f"Missing Number {related}",
            }
            for related in related_missing
        ],
        "meta_title": f"Missing Number {number} in Lo Shu Grid - {ref['planet']} Energy and Remedies",
        "meta_description": f"Number {number} missing from your Lo Shu Grid may affect {blueprint['focus_trait']}. Discover its meaning, practical remedies, and the life areas it influences.",
    }


def build_arrow_document(slug: str) -> dict[str, Any]:
    canonical_slug = ARROW_ALIAS_TO_SLUG.get(slug)
    if not canonical_slug:
        raise HTTPException(status_code=404, detail="Arrow not found")

    payload = ARROW_BLUEPRINTS[canonical_slug]
    faq_items = [
        {
            "question": f"What is the {payload['name']} in Lo Shu Grid?",
            "answer": f"It is the {payload['theme'].lower()} formed by numbers {', '.join(str(number) for number in payload['numbers'])} appearing together in the chart.",
        },
        {
            "question": f"What happens when the {payload['name']} is present?",
            "answer": payload["effect_present"],
        },
        {
            "question": f"What happens when the {payload['name']} is missing?",
            "answer": payload["effect_missing"],
        },
        {
            "question": f"Which traits are linked with the {payload['name']}?",
            "answer": f"It is most often linked with {', '.join(payload['real_life_traits'][:3])}.",
        },
        {
            "question": f"Is the {payload['name']} a Rajayoga?",
            "answer": "Yes. This arrow is treated as a Rajayoga pattern in the decoded Lo Shu source and is associated with heightened success potential." if payload.get("rajayoga") else "No. This arrow is important, but it is not one of the two Rajayoga diagonals.",
        },
    ]
    one_word_theme = payload["theme"].split()[0]
    return {
        "slug": canonical_slug,
        "name": payload["name"],
        "title": f"{payload['name']} - What This Lo Shu Arrow Reveals About You",
        "numbers": payload["numbers"],
        "theme": payload["theme"],
        "effect_present": payload["effect_present"],
        "effect_missing": payload["effect_missing"],
        "real_life_traits": payload["real_life_traits"],
        "shadow_trait": payload["shadow_trait"],
        "strength_band": payload["strength_band"],
        "rajayoga": bool(payload.get("rajayoga")),
        "faq": faq_items,
        "meta_title": f"{payload['name']} in Lo Shu Grid - {one_word_theme} Energy",
        "meta_description": f"Discover what the {payload['name']} means in Lo Shu Grid, what numbers {', '.join(str(number) for number in payload['numbers'])} reveal, and how this pattern shapes personality and action.",
    }


def build_active_arrow_result(slug: str) -> dict[str, Any]:
    doc = build_arrow_document(slug)
    return {
        "slug": doc["slug"],
        "name": doc["name"],
        "numbers": doc["numbers"],
        "theme": doc["theme"],
        "effect_summary": doc["effect_present"],
        "strength_band": doc["strength_band"],
        "rajayoga": doc["rajayoga"],
    }


def build_missing_arrow_result(slug: str) -> dict[str, Any]:
    doc = build_arrow_document(slug)
    return {
        "slug": doc["slug"],
        "name": MISSING_ARROW_LABELS[doc["slug"]],
        "base_arrow_name": doc["name"],
        "numbers": doc["numbers"],
        "theme": doc["theme"],
        "effect_summary": doc["effect_missing"],
        "strength_band": "high" if doc["strength_band"] == "extreme" else doc["strength_band"],
    }


async def resolve_missing_number_document(request: Request, number: int) -> dict[str, Any]:
    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_missing_numbers.find_one({"number": number}, {"_id": 0})
        if doc:
            return doc
    return build_missing_number_document(number)


async def resolve_arrow_document(request: Request, slug: str) -> dict[str, Any]:
    canonical_slug = ARROW_ALIAS_TO_SLUG.get(slug)
    if not canonical_slug:
        raise HTTPException(status_code=404, detail="Arrow not found")

    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_arrows.find_one({"slug": canonical_slug}, {"_id": 0})
        if doc:
            return doc
    return build_arrow_document(canonical_slug)


@router.post("/calculate")
async def calculate_lo_shu(payload: LoShuCalculateRequest) -> dict[str, Any]:
    counts, core_numbers = build_number_counts(payload.full_name, payload.dob, payload.gender)
    present_numbers = [number for number in range(1, 10) if counts[number] > 0]
    missing_numbers = [number for number in range(1, 10) if counts[number] == 0]
    present_set = set(present_numbers)
    missing_set = set(missing_numbers)

    active_arrows = [
        build_active_arrow_result(slug)
        for slug in ARROW_DISPLAY_ORDER
        if all(number in present_set for number in ARROW_BLUEPRINTS[slug]["numbers"])
    ]
    missing_arrows = [
        build_missing_arrow_result(slug)
        for slug in ARROW_DISPLAY_ORDER
        if all(number in missing_set for number in ARROW_BLUEPRINTS[slug]["numbers"])
    ]
    rajayoga_present = [arrow for arrow in active_arrows if arrow["rajayoga"]]

    return {
        "grid": {str(number): counts[number] > 0 for number in range(1, 10)},
        "grid_rows": build_grid_rows(counts),
        "number_counts": {str(number): counts[number] for number in range(1, 10)},
        "missing_numbers": missing_numbers,
        "present_numbers": present_numbers,
        "active_arrows": active_arrows,
        "missing_arrows": missing_arrows,
        "basic_number": core_numbers["basic_number"],
        "destiny_number": core_numbers["destiny_number"],
        "kua_number": core_numbers["kua_number"],
        "name_number": core_numbers["name_number"],
        "missing_number_details": [build_missing_number_document(number) for number in missing_numbers],
        "rajayoga_present": rajayoga_present,
        "rajayoga_level": "dual" if len(rajayoga_present) == 2 else ("single" if len(rajayoga_present) == 1 else "none"),
    }


@router.get("/missing/{number}")
async def get_missing_number_page(number: int, request: Request) -> dict[str, Any]:
    if number < 1 or number > 9:
        raise HTTPException(status_code=404, detail="Missing number not found")
    return await resolve_missing_number_document(request, number)


@router.get("/arrow/{slug}")
async def get_arrow_page(slug: str, request: Request) -> dict[str, Any]:
    return await resolve_arrow_document(request, slug)


LO_SHU_SITEMAP_URLS = [
    "https://www.everydayhoroscope.in/lo-shu-grid",
    "https://www.everydayhoroscope.in/lo-shu-grid/calculator",
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/missing-{number}" for number in range(1, 10)],
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/arrow/{slug}" for slug in ARROW_DISPLAY_ORDER],
]

MISSING_NUMBER_DOCUMENTS = [build_missing_number_document(number) for number in range(1, 10)]
ARROW_DOCUMENTS = [build_arrow_document(slug) for slug in ARROW_DISPLAY_ORDER]
