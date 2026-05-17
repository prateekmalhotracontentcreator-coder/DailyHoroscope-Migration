from __future__ import annotations

import random
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from knowledge_engine import log_ritual_event, register_arc_angel_report_run


router = APIRouter(prefix="/api/tarot", tags=["tarot"])

READINGS_COLLECTION = "tarot_readings"
MANIFESTATIONS_COLLECTION = "tarot_manifestations"
ENGINE_VERSION = "tarot-router-v4"

DepthLevel = Literal["simple", "detailed", "comprehensive"]
FocusArea = Literal["guidance", "love", "career", "healing", "clarity"]
SceneType = Literal["intro", "ritual", "card_reveal", "guidance", "closing"]
SpreadTier = Literal["monthly", "tarot_premium"]
SpreadCategory = Literal["oracle", "relationship", "career", "timing", "spiritual", "deep", "healing"]
SpreadLayout = Literal["single", "grid3", "grid2", "strip7", "celtic_cross", "mirror", "arc"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class TarotScene(StrictModel):
    scene_id: str
    scene_type: SceneType
    title: str | None = None
    text: str
    duration_ms: int = 2500
    meta: dict[str, Any] = Field(default_factory=dict)


class TarotCard(StrictModel):
    card_id: str
    name: str
    position_code: str
    position_label: str
    orientation: Literal["upright", "reversed"]
    meaning_snippet: str
    suit: str | None = None
    rank: str | None = None
    image_url: str | None = None


class TarotSpread(StrictModel):
    spread_id: str
    name: str
    description: str
    card_count: int
    positions: list[str]
    tier: SpreadTier
    category: SpreadCategory
    layout: SpreadLayout
    scenario_ids: list[str] = Field(default_factory=list)
    ritual_note: str
    best_timing: str


class TarotReading(StrictModel):
    id: str
    report_id: str
    doc_type: str = "report"
    user_email: str
    reading_type: str
    spread_id: str
    spread_name: str
    focus_area: str
    layout: str
    language: str = "en"
    depth_level: DepthLevel = "simple"
    prediction_date: str
    is_premium: bool = False
    bookmarked: bool = False
    summary: str
    guidance: str
    affirmation: str
    question: str | None = None
    ritual_note: str | None = None
    best_timing: str | None = None
    yes_no_verdict: str | None = None
    yes_no_upright: int | None = None
    yes_no_reversed: int | None = None
    cards: list[TarotCard] = Field(default_factory=list)
    scenes: list[TarotScene] = Field(default_factory=list)
    meta: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str


class TarotDailyDrawRequest(StrictModel):
    focus_area: FocusArea = "guidance"
    language: str = "en"
    depth_level: DepthLevel = "simple"
    question: str | None = None
    linked_manifestation_id: str | None = None


class TarotSpreadGenerateRequest(StrictModel):
    spread_id: str
    question: str | None = None
    language: str = "en"
    depth_level: DepthLevel = "detailed"


class TarotFeedbackRequest(StrictModel):
    report_id: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = ""


class TarotBookmarkRequest(StrictModel):
    report_id: str
    bookmarked: bool


class TarotGamification(StrictModel):
    xp_awarded: int = 0
    coins_awarded: int = 0
    daily_streak: int = 0
    level: int = 1
    new_badges: list[str] = Field(default_factory=list)


class TarotReadingResponse(StrictModel):
    reading: TarotReading
    gamification: TarotGamification
    cached: bool = False


class TarotTodayResponse(StrictModel):
    has_reading: bool
    reading: TarotReading | None = None
    gamification: TarotGamification | None = None


class TarotHistoryItem(StrictModel):
    id: str
    report_id: str
    reading_type: str
    spread_id: str
    spread_name: str
    focus_area: str
    prediction_date: str
    depth_level: str
    summary: str
    bookmarked: bool = False
    created_at: str
    cards: list[TarotCard] = Field(default_factory=list)


class TarotHistoryResponse(StrictModel):
    items: list[TarotHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    has_more: bool


class TarotSpreadAccess(StrictModel):
    spread_id: str
    tier: SpreadTier
    has_access: bool
    reason: str | None = None


class TarotSpreadsResponse(StrictModel):
    spreads: list[TarotSpread]


class FavorablePeriodItem(StrictModel):
    id: str
    report_id: str
    type: str
    window_label: str
    confidence: float
    summary: str
    recommendation: str | None = None
    starts_on: str | None = None
    ends_on: str | None = None


class FavorablePeriodsResponse(StrictModel):
    periods: list[FavorablePeriodItem] = Field(default_factory=list)


class PersonalizedOfferItem(StrictModel):
    id: str
    offer_code: str
    title: str
    description: str
    target_theme: str | None = None
    cta_label: str = "Explore"
    destination: str | None = None
    priority: int = 0


class PersonalizedOffersResponse(StrictModel):
    offers: list[PersonalizedOfferItem] = Field(default_factory=list)


class ManifestationCreateRequest(StrictModel):
    date: str
    intention_text: str
    linked_reading_id: str | None = None
    card_name: str | None = None


class ManifestationReminderRequest(StrictModel):
    date: str
    reminder_time: str
    reminder_text: str


class ManifestationTaskRequest(StrictModel):
    date: str
    task_text: str
    task_done: bool


class ManifestationBookmarkResponse(StrictModel):
    success: bool = True
    id: str
    bookmarked: bool


class ManifestationEntry(StrictModel):
    id: str
    date: str
    type: Literal["intention", "reminder", "task"]
    intention_text: str | None = None
    linked_reading_id: str | None = None
    card_name: str | None = None
    reminder_time: str | None = None
    reminder_text: str | None = None
    task_text: str | None = None
    task_done: bool | None = None
    bookmarked: bool = False
    created_at: str


class ManifestationMonthDay(StrictModel):
    date: str
    moon_phase: str
    intention: ManifestationEntry | None = None
    reminders: list[ManifestationEntry] = Field(default_factory=list)
    tasks: list[ManifestationEntry] = Field(default_factory=list)
    linked_reading: dict[str, Any] | None = None


class ManifestationMonthResponse(StrictModel):
    month: str
    items: list[ManifestationMonthDay] = Field(default_factory=list)


class ManifestationJournalItem(StrictModel):
    id: str
    date: str
    moon_phase: str
    intention_text: str
    linked_reading_id: str | None = None
    card_name: str | None = None
    bookmarked: bool = False
    tasks_total: int = 0
    tasks_done: int = 0
    reminders_count: int = 0
    created_at: str


class ManifestationJournalResponse(StrictModel):
    items: list[ManifestationJournalItem] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    has_more: bool


class ManifestationStatsResponse(StrictModel):
    streak_days: int
    total_intentions: int
    most_drawn_card: str | None = None


MAJOR_ARCANA: list[tuple[str, str]] = [
    ("the-fool", "The Fool"),
    ("the-magician", "The Magician"),
    ("the-high-priestess", "The High Priestess"),
    ("the-empress", "The Empress"),
    ("the-emperor", "The Emperor"),
    ("the-hierophant", "The Hierophant"),
    ("the-lovers", "The Lovers"),
    ("the-chariot", "The Chariot"),
    ("strength", "Strength"),
    ("the-hermit", "The Hermit"),
    ("wheel-of-fortune", "Wheel of Fortune"),
    ("justice", "Justice"),
    ("the-hanged-man", "The Hanged Man"),
    ("death", "Death"),
    ("temperance", "Temperance"),
    ("the-devil", "The Devil"),
    ("the-tower", "The Tower"),
    ("the-star", "The Star"),
    ("the-moon", "The Moon"),
    ("the-sun", "The Sun"),
    ("judgement", "Judgement"),
    ("the-world", "The World"),
]

MAJOR_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "the-fool": {"upright": ["fresh possibility", "innocence", "a leap of faith"], "reversed": ["hesitation", "naivety", "misread timing"]},
    "the-magician": {"upright": ["manifesting power", "focused will", "skill meeting timing"], "reversed": ["scattered power", "self-doubt", "misdirection"]},
    "the-high-priestess": {"upright": ["intuition", "inner knowing", "mystery"], "reversed": ["withheld truth", "emotional fog", "uncertain signals"]},
    "the-empress": {"upright": ["abundance", "nourishment", "fertile growth"], "reversed": ["overgiving", "creative blockage", "imbalance"]},
    "the-emperor": {"upright": ["structure", "stability", "wise control"], "reversed": ["rigidity", "control issues", "power strain"]},
    "the-hierophant": {"upright": ["tradition", "guidance", "sacred learning"], "reversed": ["rebellion", "restlessness", "misfit values"]},
    "the-lovers": {"upright": ["alignment", "soulful choice", "bonding"], "reversed": ["misalignment", "distance", "conflicted desire"]},
    "the-chariot": {"upright": ["direction", "victory", "disciplined motion"], "reversed": ["drift", "friction", "wavering focus"]},
    "strength": {"upright": ["heart-led courage", "resilience", "inner calm"], "reversed": ["doubt", "burnout", "shaken confidence"]},
    "the-hermit": {"upright": ["solitude", "wisdom", "inner guidance"], "reversed": ["withdrawal", "loneliness", "avoidance"]},
    "wheel-of-fortune": {"upright": ["turning point", "destined change", "movement"], "reversed": ["delays", "stuck cycles", "resistance to change"]},
    "justice": {"upright": ["truth", "clarity", "balanced consequence"], "reversed": ["imbalance", "avoidance", "unclear accountability"]},
    "the-hanged-man": {"upright": ["pause", "new perspective", "surrender"], "reversed": ["stalling", "martyrdom", "resistance"]},
    "death": {"upright": ["deep release", "transformation", "ending to begin again"], "reversed": ["holding on", "fear of change", "unfinished closure"]},
    "temperance": {"upright": ["healing balance", "integration", "patience"], "reversed": ["imbalance", "excess", "disharmony"]},
    "the-devil": {"upright": ["attachment", "temptation", "shadow desire"], "reversed": ["release", "awakening", "breaking patterns"]},
    "the-tower": {"upright": ["disruption", "truth breaking through", "sudden awakening"], "reversed": ["avoided change", "lingering tension", "internal collapse"]},
    "the-star": {"upright": ["hope", "healing light", "renewal"], "reversed": ["discouragement", "dimmed faith", "energetic drain"]},
    "the-moon": {"upright": ["dream logic", "intuition", "the unseen"], "reversed": ["confusion", "fear", "half-seen truth"]},
    "the-sun": {"upright": ["joy", "clarity", "life force"], "reversed": ["temporary clouds", "ego heat", "muted radiance"]},
    "judgement": {"upright": ["awakening", "calling", "truth returning"], "reversed": ["self-judgement", "hesitation", "avoided reckoning"]},
    "the-world": {"upright": ["completion", "fulfilment", "arrival"], "reversed": ["unfinished cycle", "delay", "lingering threshold"]},
}

SUIT_THEMES = {
    "wands": {
        "upright": ["bold action", "creative fire", "forward motion"],
        "reversed": ["burnout", "restless energy", "misdirected passion"],
        "label": "Wands",
    },
    "cups": {
        "upright": ["emotional truth", "connection", "heart-opening"],
        "reversed": ["emotional overwhelm", "withdrawal", "mixed feelings"],
        "label": "Cups",
    },
    "swords": {
        "upright": ["mental clarity", "truth", "decisive insight"],
        "reversed": ["overthinking", "inner conflict", "sharp tension"],
        "label": "Swords",
    },
    "pentacles": {
        "upright": ["practical grounding", "material growth", "steady progress"],
        "reversed": ["stagnation", "scarcity fear", "practical delays"],
        "label": "Pentacles",
    },
}

RANK_LABELS = {
    "ace": "Ace",
    "02": "Two",
    "03": "Three",
    "04": "Four",
    "05": "Five",
    "06": "Six",
    "07": "Seven",
    "08": "Eight",
    "09": "Nine",
    "10": "Ten",
    "page": "Page",
    "knight": "Knight",
    "queen": "Queen",
    "king": "King",
}


def _build_default_cards() -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for slug, name in MAJOR_ARCANA:
        keywords = MAJOR_KEYWORDS[slug]
        cards.append(
            {
                "id": slug,
                "name": name,
                "suit": "major",
                "rank": None,
                "upright_keywords": keywords["upright"],
                "reversed_keywords": keywords["reversed"],
                "image_url": None,
            }
        )

    ordered_ranks = ["ace", "02", "03", "04", "05", "06", "07", "08", "09", "10", "page", "knight", "queen", "king"]
    for suit, theme in SUIT_THEMES.items():
        for rank in ordered_ranks:
            rank_label = RANK_LABELS[rank]
            cards.append(
                {
                    "id": f"{suit}-{rank}",
                    "name": f"{rank_label} of {theme['label']}",
                    "suit": suit,
                    "rank": rank,
                    "upright_keywords": [f"{rank_label.lower()} energy", *theme["upright"]],
                    "reversed_keywords": [f"blocked {rank_label.lower()} energy", *theme["reversed"]],
                    "image_url": None,
                }
            )
    return cards


DEFAULT_CARDS = _build_default_cards()

DEFAULT_SPREADS: list[TarotSpread] = [
    TarotSpread(
        spread_id="daily-draw",
        name="Daily Cosmic Draw",
        description="A single-card oracle for your present atmosphere and daily guidance.",
        card_count=1,
        positions=["Your Cosmic Message"],
        tier="monthly",
        category="oracle",
        layout="single",
        scenario_ids=["daily-guidance", "quick-answer"],
        ritual_note="Still your mind. Place your hand over your heart. Ask: 'What does the universe want me to know today?'",
        best_timing="Each morning before the world rushes in",
    ),
    TarotSpread(
        spread_id="past-present-future",
        name="Past Hurts · Present Gifts · Future Rewards",
        description="A 3-card reading for emotional context, present blessings, and what is ripening next.",
        card_count=3,
        positions=["Past Hurts", "Present Gifts", "Future Rewards"],
        tier="monthly",
        category="deep",
        layout="grid3",
        scenario_ids=["need-clarity", "life-review"],
        ritual_note="Breathe in the past, exhale it with love. You carry only what serves you forward.",
        best_timing="Sunday evenings or any moment of reflection",
    ),
    TarotSpread(
        spread_id="love-triangle",
        name="Love Triangle",
        description="A 3-card relationship reading for where you stand, where they stand, and where this is going.",
        card_count=3,
        positions=["Where You Stand", "Where They Stand", "Where This Is Going"],
        tier="monthly",
        category="relationship",
        layout="grid3",
        scenario_ids=["love-questions", "relationship-check"],
        ritual_note="Hold the image of this person gently in your mind -- without longing, without fear. Simply with curiosity.",
        best_timing="Friday -- the day of Venus and all matters of love",
    ),
    TarotSpread(
        spread_id="mind-body-spirit",
        name="Mind · Body · Spirit",
        description="A 3-card reading for your thoughts, embodied wisdom, and spiritual call.",
        card_count=3,
        positions=["Your Mind's Truth", "Your Body's Wisdom", "Your Spirit's Call"],
        tier="monthly",
        category="healing",
        layout="grid3",
        scenario_ids=["healing-needed", "daily-guidance"],
        ritual_note="This reading speaks to your whole self -- not just the question, but the questioner.",
        best_timing="Any time -- this spread meets you exactly where you are",
    ),
    TarotSpread(
        spread_id="crossroads",
        name="The Crossroads",
        description="A 5-card spread for decisions, transitions, and the counsel of the universe.",
        card_count=5,
        positions=["What to Leave Behind", "What to Carry Forward", "Path A", "Path B", "The Universe's Counsel"],
        tier="monthly",
        category="career",
        layout="grid3",
        scenario_ids=["big-decision", "life-change"],
        ritual_note="Every crossroads is a gift. Both paths exist because you are ready for change. Let the cards show what the mind cannot yet see.",
        best_timing="Wednesday -- the day of choices and communication",
    ),
    TarotSpread(
        spread_id="hidden-forces",
        name="Hidden Forces",
        description="A 5-card spread for the hidden layer beneath a situation.",
        card_count=5,
        positions=["Recent Past", "Present Situation", "What Is Hidden From You", "Guidance", "Likely Outcome"],
        tier="monthly",
        category="deep",
        layout="grid3",
        scenario_ids=["blocked-feeling", "need-clarity"],
        ritual_note="The cards reveal what the conscious mind protects you from seeing. Receive this with openness, not resistance.",
        best_timing="Waxing moon -- when what is hidden begins to show itself",
    ),
    TarotSpread(
        spread_id="healing-journey",
        name="The Healing Journey",
        description="A 5-card healing map for release, resilience, and a softer new beginning.",
        card_count=5,
        positions=["The Wound", "Your Inner Strength", "What to Release", "What to Receive", "Your New Beginning"],
        tier="monthly",
        category="healing",
        layout="grid3",
        scenario_ids=["healing-needed", "grief-loss"],
        ritual_note="Healing is not linear. The cards show the direction, not the destination. Be patient with yourself.",
        best_timing="Waning moon -- the time of release and letting go",
    ),
    TarotSpread(
        spread_id="soul-activation",
        name="Soul Activation",
        description="A 4-card spiritual spread for archetype, pattern, becoming, and activation.",
        card_count=4,
        positions=["Your Soul Archetype", "Your Pattern From the Past", "Who You Are Becoming", "The Activation -- Your Next Step"],
        tier="tarot_premium",
        category="spiritual",
        layout="grid2",
        scenario_ids=["spiritual-growth", "life-purpose"],
        ritual_note="This is not a reading about events. It is a reading about you -- the eternal, evolving you. Sit with each card for a full breath before moving to the next.",
        best_timing="New Moon or your birthday -- moments of new beginning",
    ),
    TarotSpread(
        spread_id="relationship-mirror",
        name="The Relationship Mirror",
        description="A 4-card spread for relational reflection and unseen chemistry.",
        card_count=4,
        positions=["What you bring to this bond", "What they bring to this bond", "The unseen force between you", "What this relationship is here to teach you"],
        tier="tarot_premium",
        category="relationship",
        layout="grid2",
        scenario_ids=["relationship-check", "love-questions"],
        ritual_note="Every relationship is a mirror. What you see in another is always, somehow, a reflection of yourself.",
        best_timing="Any day -- love has no preferred timing",
    ),
    TarotSpread(
        spread_id="celtic-cross",
        name="Celtic Cross",
        description="The full ancient map -- ten positions revealing the heart of a question and its deeper truth.",
        card_count=10,
        positions=["The Heart of the Matter", "What Crosses You", "The Foundation Beneath", "The Recent Past", "The Crown -- Best Possible Outcome", "What Approaches", "How You See Yourself", "How Others See You", "Your Hopes and Fears", "The Final Outcome"],
        tier="tarot_premium",
        category="deep",
        layout="celtic_cross",
        scenario_ids=["big-decision", "life-review", "need-clarity", "life-purpose"],
        ritual_note="The Celtic Cross is the ancient map -- ten faces of your truth laid bare. Take a full breath before each reveal. This reading holds everything.",
        best_timing="Any time -- the Celtic Cross meets every question with the same depth",
    ),
    TarotSpread(
        spread_id="full-relationship",
        name="The Full Relationship Spread",
        description="An 11-card relational mirror revealing both sides, shared space, and destiny.",
        card_count=11,
        positions=["You Now", "Your Vulnerability", "Your Gift to This Bond", "Your View of This Connection", "Them Now", "Their Vulnerability", "Their Gift to This Bond", "Their View of This Connection", "Where You Are Together", "The Road Ahead", "The Destiny of This Bond"],
        tier="tarot_premium",
        category="relationship",
        layout="mirror",
        scenario_ids=["relationship-check", "love-questions"],
        ritual_note="Two souls. Eleven cards. An honest portrait of what exists between you -- beyond hope, beyond fear.",
        best_timing="Friday evenings -- Venus rules bonds between people",
    ),
    TarotSpread(
        spread_id="week-ahead",
        name="Week Ahead",
        description="Seven cards for seven days -- a timing forecast you can revisit morning by morning.",
        card_count=7,
        positions=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        tier="tarot_premium",
        category="timing",
        layout="strip7",
        scenario_ids=["timing-forecast"],
        ritual_note="Seven cards. Seven days. Let each morning begin with the card the universe placed there for you.",
        best_timing="Sunday evening -- set the energy for the week ahead",
    ),
    TarotSpread(
        spread_id="month-ahead",
        name="Month Ahead",
        description="An 8-card month map with theme and watch-for guidance for each week.",
        card_count=8,
        positions=["Week 1 -- The Theme", "Week 1 -- Watch For This", "Week 2 -- The Theme", "Week 2 -- Watch For This", "Week 3 -- The Theme", "Week 3 -- Watch For This", "Week 4 -- The Theme", "The Month's Great Teaching"],
        tier="tarot_premium",
        category="timing",
        layout="grid2",
        scenario_ids=["timing-forecast"],
        ritual_note="A month is a full cycle of the moon. Eight cards to map its terrain. Draw this at the beginning, revisit at the end.",
        best_timing="New Moon -- the first day of the lunar month",
    ),
    TarotSpread(
        spread_id="goal-spread",
        name="The Seven-Day Goal Spread",
        description="A 7-card ambition and purpose spread for action, challenge, help, and outcome.",
        card_count=7,
        positions=["Your True Focus", "What Lies Hidden", "The Action Called For", "The Challenge to Face", "The Helpful Force", "Your Source of Inspiration", "The Outcome if You Act"],
        tier="tarot_premium",
        category="career",
        layout="arc",
        scenario_ids=["career-growth", "big-decision", "life-purpose"],
        ritual_note="Every goal has seven faces. The cards reveal which are visible to you -- and which have been waiting for your attention.",
        best_timing="Tuesday -- the day of Mars, action, and ambition",
    ),
    TarotSpread(
        spread_id="year-ahead",
        name="The Year Ahead",
        description="A 12-card annual map revealing the predominant energy of each month.",
        card_count=12,
        positions=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        tier="tarot_premium",
        category="timing",
        layout="grid3",
        scenario_ids=["life-review", "life-purpose", "timing-forecast"],
        ritual_note="Twelve months. Twelve cards. Not fate -- but possibility. One card holds the predominant energy of each month.",
        best_timing="New Year · your birthday · any personal moment of renewal",
    ),
    TarotSpread(
        spread_id="yes-no-oracle",
        name="Yes / No Oracle",
        description="A 3-card oracle that reads the balance of upright and reversed energy for a direct answer.",
        card_count=3,
        positions=["First Reading", "Second Reading", "Third Reading"],
        tier="monthly",
        category="oracle",
        layout="grid3",
        scenario_ids=["quick-answer", "big-decision"],
        ritual_note="Ask your question once, clearly, then release it. The cards do not respond to desperation -- only to honest enquiry.",
        best_timing="Thursday -- the day of truth and Jupiter's clarity",
    ),
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now().isoformat()


def _db(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available on request.app.state.db.")
    return db


def _readings_collection(request: Request):
    return getattr(_db(request), READINGS_COLLECTION)


def _manifestations_collection(request: Request):
    return getattr(_db(request), MANIFESTATIONS_COLLECTION)


def _resolve_user(request: Request) -> dict[str, Any]:
    state_user = getattr(request.state, "user", None)
    return state_user if isinstance(state_user, dict) else {}


def _normalize_email(value: str | None) -> str:
    return str(value or "").strip().lower()


def _resolve_user_email(request: Request, explicit_email: str | None = None, *, allow_missing: bool = False) -> str:
    user = _resolve_user(request)
    if user.get("email"):
        return _normalize_email(str(user["email"]))
    email = _normalize_email(explicit_email)
    if email:
        return email
    if allow_missing:
        return ""
    raise HTTPException(status_code=401, detail="Authenticated user email or explicit user_email is required.")


def _slug_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.replace("-", " ").split())


def _moon_phase_emoji(day_value: date) -> str:
    known_new_moon = date(2024, 1, 11)
    days = (day_value - known_new_moon).days
    cycle = (days % 29.53058867) / 29.53058867
    if cycle < 0.0625:
        return "🌑"
    if cycle < 0.1875:
        return "🌒"
    if cycle < 0.3125:
        return "🌓"
    if cycle < 0.4375:
        return "🌔"
    if cycle < 0.5625:
        return "🌕"
    if cycle < 0.6875:
        return "🌖"
    if cycle < 0.8125:
        return "🌗"
    if cycle < 0.9375:
        return "🌘"
    return "🌑"


def _serialize_datetime(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return _now_iso()


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _extract_card_name(card_id: str) -> str:
    for card in DEFAULT_CARDS:
        if card["id"] == card_id:
            return str(card["name"])
    return _slug_to_title(card_id)


def _pick_card(exclude_ids: set[str] | None = None) -> dict[str, Any]:
    exclude = exclude_ids or set()
    available = [card for card in DEFAULT_CARDS if card["id"] not in exclude]
    if not available:
        raise HTTPException(status_code=400, detail="No tarot cards available for selection.")
    return random.choice(available)


def _pick_cards(count: int, exclude_ids: set[str] | None = None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    used = set(exclude_ids or set())
    for _ in range(count):
        card = _pick_card(used)
        selected.append(card)
        used.add(card["id"])
    return selected


def _pick_orientation() -> Literal["upright", "reversed"]:
    return random.choice(["upright", "reversed"])


def _focus_phrase(focus_area: str) -> str:
    return {
        "guidance": "the path you are walking now",
        "love": "the emotional field around love and connection",
        "career": "the momentum around work, ambition, and direction",
        "healing": "the place in you asking for gentleness and repair",
        "clarity": "the truth waiting to become easier to see",
    }.get(focus_area, "the truth waiting to emerge")


def _build_affirmation(card_name: str, orientation: str, focus_area: str) -> str:
    if orientation == "upright":
        return f"I welcome the wisdom of {card_name} and trust what it reveals about my {focus_area} path."
    return f"I soften my resistance, honour my timing, and let {card_name} guide me through deeper {focus_area} clarity."


def _build_scenes(focus_area: str, card_name: str, orientation: str, question: str | None, ritual_note: str | None = None) -> list[TarotScene]:
    prompt_line = f"Your question lingers beneath the ritual: {question}" if question else "Your breath becomes the first prayer of the reading."
    ritual_text = ritual_note or "The deck responds when the heart grows still enough to listen."
    return [
        TarotScene(
            scene_id="intro",
            scene_type="intro",
            title="The veil opens",
            text=f"The oracle awakens around {_focus_phrase(focus_area)}.",
            duration_ms=2100,
        ),
        TarotScene(
            scene_id="ritual",
            scene_type="ritual",
            title="Setting the intention",
            text=f"{ritual_text} {prompt_line}",
            duration_ms=2600,
        ),
        TarotScene(
            scene_id="card_reveal",
            scene_type="card_reveal",
            title=card_name,
            text=f"{card_name} arrives {orientation}, asking you to receive its message without hurry.",
            duration_ms=3200,
            meta={"orientation": orientation},
        ),
        TarotScene(
            scene_id="guidance",
            scene_type="guidance",
            title="Ancient Wisdom",
            text=f"This card speaks into {focus_area} with a tone of patience, presence, and aligned timing.",
            duration_ms=2900,
        ),
        TarotScene(
            scene_id="closing",
            scene_type="closing",
            title="The reading closes",
            text="Carry only the next true step. The cards never ask you to carry the whole future at once.",
            duration_ms=2200,
        ),
    ]


def _meaning_text(card: dict[str, Any], orientation: str, position_label: str) -> str:
    keywords = card["upright_keywords"] if orientation == "upright" else card["reversed_keywords"]
    return f"{position_label}: {random.choice(keywords)}"


def _build_summary(spread: TarotSpread, focus_area: str, cards: list[TarotCard], question: str | None = None) -> str:
    names = ", ".join(card.name for card in cards[:3])
    base = f"{spread.name} reveals {names} as the strongest energies moving through your {focus_area} path."
    if question:
        base += " Your question remains active beneath every card."
    return base


def _build_guidance(spread: TarotSpread, focus_area: str, cards: list[TarotCard]) -> str:
    highlighted = cards[0].name if cards else "the deck"
    if spread.card_count == 1:
        return f"{highlighted} suggests a single clear movement: trust what is ripening around your {focus_area} life without rushing its timing."
    return f"This spread shows layered motion rather than a single answer. Let {highlighted} anchor the reading while the remaining cards reveal sequence, timing, and emotional texture."


def _build_reading_doc(
    *,
    user_email: str,
    spread: TarotSpread,
    focus_area: str,
    language: str,
    depth_level: DepthLevel,
    question: str | None,
    cards: list[TarotCard],
    scenes: list[TarotScene],
    summary: str,
    guidance: str,
    affirmation: str,
    linked_manifestation_id: str | None = None,
) -> dict[str, Any]:
    now = _now_iso()
    report_id = str(uuid4())
    return {
        "id": str(uuid4()),
        "report_id": report_id,
        "doc_type": "report",
        "user_email": user_email,
        "reading_type": "daily_draw" if spread.spread_id == "daily-draw" else "spread",
        "spread_id": spread.spread_id,
        "spread_name": spread.name,
        "focus_area": focus_area,
        "layout": spread.layout,
        "language": language,
        "depth_level": depth_level,
        "prediction_date": date.today().isoformat(),
        "is_premium": spread.tier == "tarot_premium",
        "bookmarked": False,
        "summary": summary,
        "guidance": guidance,
        "affirmation": affirmation,
        "question": question,
        "ritual_note": spread.ritual_note,
        "best_timing": spread.best_timing,
        "cards": [card.model_dump() for card in cards],
        "scenes": [scene.model_dump() for scene in scenes],
        "linked_manifestation_id": linked_manifestation_id,
        "created_at": now,
        "updated_at": now,
        "meta": {"engine_version": ENGINE_VERSION, "category": spread.category},
    }


async def _compute_xp(collection, user_email: str, base_xp: int) -> TarotGamification:
    docs = await collection.find(
        {"user_email": user_email, "doc_type": "report"},
        projection={"prediction_date": 1},
    ).sort("prediction_date", -1).to_list(length=365)
    unique_days = sorted({doc.get("prediction_date") for doc in docs if doc.get("prediction_date")}, reverse=True)
    streak = 0
    cursor = date.today()
    for day_str in unique_days:
        if not day_str:
            continue
        day_value = _parse_date(day_str)
        if day_value == cursor:
            streak += 1
            cursor = cursor - timedelta(days=1)
        elif day_value > cursor:
            continue
        else:
            break
    total_reports = len(docs) + 1
    total_xp = total_reports * 10 + base_xp
    return TarotGamification(
        xp_awarded=base_xp,
        coins_awarded=max(1, min(5, 1 + streak // 3)),
        daily_streak=max(1, streak),
        level=max(1, int((total_xp / 25) ** 0.5) + 1),
        new_badges=[],
    )


def _normalize_reading_doc(doc: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(doc)
    if "story_scenes" in normalized and "scenes" not in normalized:
        normalized["scenes"] = normalized.pop("story_scenes")
    return normalized


def _spread_by_id(spread_id: str) -> TarotSpread:
    for spread in DEFAULT_SPREADS:
        if spread.spread_id == spread_id:
            return spread
    raise HTTPException(status_code=404, detail="Tarot spread not found.")


def _entitlement_from_user(user: dict[str, Any], tier: SpreadTier) -> bool:
    if not user:
        return False
    role = str(user.get("role") or "").strip().lower()
    if role in {"admin", "owner"}:
        return True
    truthy_keys = {
        "is_pro",
        "is_premium",
        "premium",
        "has_tarot_access",
        "tarot_unlocked",
        "premium_reports_enabled",
    }
    if tier == "tarot_premium":
        truthy_keys.add("tarot_premium")
        truthy_keys.add("has_tarot_premium")
    if any(bool(user.get(key)) for key in truthy_keys):
        return True
    for key in ("plan", "tier", "subscription_plan", "subscription_tier", "membership"):
        value = str(user.get(key) or "").strip().lower()
        if tier == "monthly" and value in {"pro", "premium", "gold", "paid", "monthly"}:
            return True
        if tier == "tarot_premium" and value in {"tarot_premium", "premium_plus", "premium"}:
            return True
    return False


def _is_local_tarot_unlock() -> bool:
    frontend_url = str(__import__("os").environ.get("FRONTEND_URL", "")).strip().lower()
    explicit_flag = str(__import__("os").environ.get("ENABLE_LOCAL_TAROT_UNLOCK", "")).strip().lower()
    if explicit_flag in {"1", "true", "yes", "on"}:
        return True
    return "localhost" in frontend_url or "127.0.0.1" in frontend_url


def _access_for_spread(request: Request, spread: TarotSpread) -> TarotSpreadAccess:
    if _is_local_tarot_unlock():
        return TarotSpreadAccess(
            spread_id=spread.spread_id,
            tier=spread.tier,
            has_access=True,
            reason=None,
        )
    user = _resolve_user(request)
    if spread.tier == "monthly":
        has_access = _entitlement_from_user(user, "monthly")
        return TarotSpreadAccess(
            spread_id=spread.spread_id,
            tier=spread.tier,
            has_access=has_access,
            reason=None if has_access else "monthly_subscription_required",
        )
    has_access = _entitlement_from_user(user, "tarot_premium")
    return TarotSpreadAccess(
        spread_id=spread.spread_id,
        tier=spread.tier,
        has_access=has_access,
        reason=None if has_access else "tarot_premium_required",
    )


def _suggest_tasks(card_name: str) -> list[str]:
    lower = card_name.lower()
    if "cups" in lower:
        return ["Reach out to someone you love today"]
    if "wands" in lower:
        return ["Take one bold action toward your goal"]
    if "pentacles" in lower:
        return ["Review your finances or make one practical step forward"]
    if "swords" in lower:
        return ["Write down one thought that is holding you back, then cross it out"]
    return ["Spend 5 minutes in silence. Let the card's image speak to you."]


def _journal_projection(doc: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> ManifestationJournalItem:
    related = grouped.get(doc["date"], [])
    tasks = [item for item in related if item.get("type") == "task"]
    reminders = [item for item in related if item.get("type") == "reminder"]
    return ManifestationJournalItem(
        id=str(doc["id"]),
        date=str(doc["date"]),
        moon_phase=_moon_phase_emoji(_parse_date(str(doc["date"]))),
        intention_text=str(doc.get("intention_text") or ""),
        linked_reading_id=doc.get("linked_reading_id"),
        card_name=doc.get("card_name"),
        bookmarked=bool(doc.get("bookmarked")),
        tasks_total=len(tasks),
        tasks_done=sum(1 for task in tasks if task.get("task_done")),
        reminders_count=len(reminders),
        created_at=_serialize_datetime(doc.get("created_at")),
    )


@router.get("/daily/today", response_model=TarotTodayResponse)
async def get_today_tarot_reading(request: Request) -> TarotTodayResponse:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    today = date.today().isoformat()
    doc = await collection.find_one(
        {"user_email": user_email, "doc_type": "report", "prediction_date": today, "spread_id": "daily-draw"},
        sort=[("created_at", -1)],
    )
    if not doc:
        return TarotTodayResponse(has_reading=False)
    normalized = _normalize_reading_doc(doc)
    gamification = await _compute_xp(collection, user_email, 10)
    return TarotTodayResponse(has_reading=True, reading=TarotReading(**normalized), gamification=gamification)


@router.post("/daily/draw", response_model=TarotReadingResponse)
async def draw_daily_tarot(payload: TarotDailyDrawRequest, request: Request) -> TarotReadingResponse:
    user_email = _resolve_user_email(request)
    spread = _spread_by_id("daily-draw")
    access = _access_for_spread(request, spread)
    if not access.has_access:
        raise HTTPException(status_code=402, detail=access.reason or "subscription_required")

    collection = _readings_collection(request)
    today = date.today().isoformat()
    existing = await collection.find_one(
        {"user_email": user_email, "doc_type": "report", "prediction_date": today, "spread_id": "daily-draw"},
        sort=[("created_at", -1)],
    )
    if existing:
        normalized = _normalize_reading_doc(existing)
        gamification = await _compute_xp(collection, user_email, 10)
        return TarotReadingResponse(reading=TarotReading(**normalized), gamification=gamification, cached=True)

    picked = _pick_card()
    orientation = _pick_orientation()
    card = TarotCard(
        card_id=picked["id"],
        name=picked["name"],
        position_code="message",
        position_label="Your Cosmic Message",
        orientation=orientation,
        meaning_snippet=_meaning_text(picked, orientation, "Your Cosmic Message"),
        suit=picked.get("suit"),
        rank=picked.get("rank"),
        image_url=picked.get("image_url"),
    )
    scenes = _build_scenes(payload.focus_area, picked["name"], orientation, payload.question, spread.ritual_note)
    summary = f"{picked['name']} arrives {orientation} with a message for {payload.focus_area}: {card.meaning_snippet.split(': ',1)[-1]}."
    guidance = _build_guidance(spread, payload.focus_area, [card])
    affirmation = _build_affirmation(picked["name"], orientation, payload.focus_area)
    doc = _build_reading_doc(
        user_email=user_email,
        spread=spread,
        focus_area=payload.focus_area,
        language=payload.language,
        depth_level=payload.depth_level,
        question=payload.question,
        cards=[card],
        scenes=scenes,
        summary=summary,
        guidance=guidance,
        affirmation=affirmation,
        linked_manifestation_id=payload.linked_manifestation_id,
    )
    await collection.insert_one(doc)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await log_ritual_event(_db(request), str(state_user["user_id"]), "tarot_love")
    if payload.linked_manifestation_id:
        await _manifestations_collection(request).update_many(
            {"user_email": user_email, "id": payload.linked_manifestation_id, "type": "intention"},
            {"$set": {"linked_reading_id": doc["report_id"], "card_name": picked["name"]}},
        )
    gamification = await _compute_xp(collection, user_email, 12)
    return TarotReadingResponse(reading=TarotReading(**doc), gamification=gamification, cached=False)


@router.get("/spreads", response_model=TarotSpreadsResponse)
async def list_tarot_spreads() -> TarotSpreadsResponse:
    return TarotSpreadsResponse(spreads=DEFAULT_SPREADS)


@router.get("/spreads/{spread_id}/access", response_model=TarotSpreadAccess)
async def tarot_spread_access(spread_id: str, request: Request) -> TarotSpreadAccess:
    spread = _spread_by_id(spread_id)
    return _access_for_spread(request, spread)


@router.post("/spread/generate", response_model=TarotReadingResponse)
async def generate_tarot_spread(payload: TarotSpreadGenerateRequest, request: Request) -> TarotReadingResponse:
    user_email = _resolve_user_email(request)
    spread = _spread_by_id(payload.spread_id)
    access = _access_for_spread(request, spread)
    if not access.has_access:
        raise HTTPException(status_code=402, detail=access.reason or "subscription_required")

    picked_cards = _pick_cards(spread.card_count)
    built_cards: list[TarotCard] = []
    scenes: list[TarotScene] = [
        TarotScene(
            scene_id="intro",
            scene_type="intro",
            title=spread.name,
            text=f"The {spread.name} opens around your question with {spread.card_count} ceremonial positions.",
            duration_ms=2400,
        ),
        TarotScene(
            scene_id="ritual",
            scene_type="ritual",
            title="The spread forms",
            text=f"{spread.ritual_note} Best timing: {spread.best_timing}.",
            duration_ms=2600,
        ),
    ]
    for index, card in enumerate(picked_cards):
        orientation = _pick_orientation()
        position_label = spread.positions[index]
        built_card = TarotCard(
            card_id=card["id"],
            name=card["name"],
            position_code=f"position_{index + 1}",
            position_label=position_label,
            orientation=orientation,
            meaning_snippet=_meaning_text(card, orientation, position_label),
            suit=card.get("suit"),
            rank=card.get("rank"),
            image_url=card.get("image_url"),
        )
        built_cards.append(built_card)
        scenes.append(
            TarotScene(
                scene_id=f"card_{index + 1}",
                scene_type="card_reveal",
                title=f"{position_label} · {card['name']}",
                text=f"{position_label}: {built_card.meaning_snippet.split(': ', 1)[-1]}",
                duration_ms=max(900, min(1400, 1200)),
                meta={"orientation": orientation, "position_label": position_label},
            )
        )
    scenes.append(
        TarotScene(
            scene_id="guidance",
            scene_type="guidance",
            title="Ancient Wisdom",
            text=_build_guidance(spread, "guidance", built_cards),
            duration_ms=2800,
        )
    )
    scenes.append(
        TarotScene(
            scene_id="closing",
            scene_type="closing",
            title="The reading closes",
            text="Return to what resonated most. A spread is not an order from fate, but a map of living possibility.",
            duration_ms=2200,
        )
    )
    summary = _build_summary(spread, "guidance", built_cards, payload.question)
    guidance = _build_guidance(spread, "guidance", built_cards)
    affirmation = _build_affirmation(built_cards[0].name, built_cards[0].orientation, "guidance")
    doc = _build_reading_doc(
        user_email=user_email,
        spread=spread,
        focus_area="guidance",
        language=payload.language,
        depth_level=payload.depth_level,
        question=payload.question,
        cards=built_cards,
        scenes=scenes,
        summary=summary,
        guidance=guidance,
        affirmation=affirmation,
    )

    if spread.spread_id == "yes-no-oracle":
        upright_count = sum(1 for card in built_cards if card.orientation == "upright")
        reversed_count = len(built_cards) - upright_count
        verdict = "Yes" if upright_count >= 2 else "No" if reversed_count >= 2 else "Unclear"
        doc["yes_no_verdict"] = verdict
        doc["yes_no_upright"] = upright_count
        doc["yes_no_reversed"] = reversed_count

    collection = _readings_collection(request)
    await collection.insert_one(doc)
    state_user = getattr(request.state, "user", None) or {}
    if state_user.get("user_id"):
        await register_arc_angel_report_run(_db(request), str(state_user["user_id"]), "tarot_spread")
        await log_ritual_event(_db(request), str(state_user["user_id"]), "tarot_love")
    gamification = await _compute_xp(collection, user_email, 18 if spread.tier == "monthly" else 28)
    return TarotReadingResponse(reading=TarotReading(**doc), gamification=gamification, cached=False)


@router.get("/reading/{report_id}", response_model=TarotReading)
async def get_tarot_reading(report_id: str, request: Request) -> TarotReading:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    doc = await collection.find_one({"user_email": user_email, "doc_type": "report", "report_id": report_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Tarot reading not found.")
    return TarotReading(**_normalize_reading_doc(doc))


@router.post("/feedback")
async def save_tarot_feedback(payload: TarotFeedbackRequest, request: Request) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    now = _now_iso()
    doc = {
        "id": str(uuid4()),
        "report_id": payload.report_id,
        "doc_type": "feedback",
        "user_email": user_email,
        "rating": payload.rating,
        "comment": (payload.comment or "").strip(),
        "created_at": now,
        "updated_at": now,
        "meta": {"engine_version": ENGINE_VERSION},
    }
    await collection.insert_one(doc)
    return {"success": True, "message": "Feedback recorded."}


@router.get("/history", response_model=TarotHistoryResponse)
async def get_tarot_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    bookmarked: bool | None = Query(default=None),
) -> TarotHistoryResponse:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    query: dict[str, Any] = {"user_email": user_email, "doc_type": "report"}
    if bookmarked is not None:
        query["bookmarked"] = bookmarked
    total = await collection.count_documents(query)
    skip = (page - 1) * limit
    docs = await collection.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
    items = [
        TarotHistoryItem(
            id=str(doc["id"]),
            report_id=str(doc["report_id"]),
            reading_type=str(doc.get("reading_type") or "spread"),
            spread_id=str(doc.get("spread_id") or ""),
            spread_name=str(doc.get("spread_name") or _slug_to_title(str(doc.get("spread_id") or ""))),
            focus_area=str(doc.get("focus_area") or "guidance"),
            prediction_date=str(doc.get("prediction_date") or ""),
            depth_level=str(doc.get("depth_level") or "simple"),
            summary=str(doc.get("summary") or ""),
            bookmarked=bool(doc.get("bookmarked")),
            created_at=_serialize_datetime(doc.get("created_at")),
            cards=[TarotCard(**card) for card in doc.get("cards", [])],
        )
        for doc in docs
    ]
    return TarotHistoryResponse(items=items, page=page, limit=limit, total=total, has_more=skip + limit < total)


@router.post("/bookmark")
async def toggle_tarot_bookmark(payload: TarotBookmarkRequest, request: Request) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    result = await collection.update_one(
        {"user_email": user_email, "doc_type": "report", "report_id": payload.report_id},
        {"$set": {"bookmarked": payload.bookmarked, "updated_at": _now_iso()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarot reading not found.")
    return {"success": True, "report_id": payload.report_id, "bookmarked": payload.bookmarked}


@router.get("/favorable-periods", response_model=FavorablePeriodsResponse)
async def get_favorable_periods(request: Request) -> FavorablePeriodsResponse:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    docs = await collection.find({"user_email": user_email, "doc_type": "report"}).sort("created_at", -1).limit(8).to_list(length=8)
    if not docs:
        today = date.today()
        return FavorablePeriodsResponse(
            periods=[
                FavorablePeriodItem(
                    id=str(uuid4()),
                    report_id=str(uuid4()),
                    type="guidance",
                    window_label="Next 7 days",
                    confidence=0.72,
                    summary="A quiet but favorable period for guidance, reflection, and aligned choices is opening now.",
                    recommendation="Use your daily draw consistently this week.",
                    starts_on=today.isoformat(),
                    ends_on=(today + timedelta(days=7)).isoformat(),
                )
            ]
        )

    latest = docs[0]
    focus = str(latest.get("focus_area") or "guidance")
    today = date.today()
    periods = [
        FavorablePeriodItem(
            id=str(uuid4()),
            report_id=str(latest.get("report_id") or uuid4()),
            type=focus,
            window_label="Next 7 days",
            confidence=0.74,
            summary=f"A favorable window is opening around {focus}, especially if you act from calm intention rather than pressure.",
            recommendation="Return to your chosen spread before making the next major move.",
            starts_on=today.isoformat(),
            ends_on=(today + timedelta(days=7)).isoformat(),
        ),
        FavorablePeriodItem(
            id=str(uuid4()),
            report_id=str(latest.get("report_id") or uuid4()),
            type="timing",
            window_label="Next 21 days",
            confidence=0.66,
            summary="The larger pattern suggests momentum through patience, review, and well-timed commitment.",
            recommendation="If a decision feels urgent, revisit it after one more reading cycle.",
            starts_on=today.isoformat(),
            ends_on=(today + timedelta(days=21)).isoformat(),
        ),
    ]
    return FavorablePeriodsResponse(periods=periods)


@router.get("/offers", response_model=PersonalizedOffersResponse)
async def get_tarot_offers(request: Request) -> PersonalizedOffersResponse:
    user_email = _resolve_user_email(request)
    collection = _readings_collection(request)
    latest = await collection.find_one({"user_email": user_email, "doc_type": "report"}, sort=[("created_at", -1)])
    focus = str((latest or {}).get("focus_area") or "guidance")
    offers = [
        PersonalizedOfferItem(
            id=str(uuid4()),
            offer_code="premium_spreads_unlock",
            title="Unlock Premium Tarot Spreads",
            description="Move beyond the daily draw into deeper relationship, timing, and life-purpose readings.",
            target_theme=focus,
            cta_label="Unlock Premium",
            destination="/pricing?source=tarot-premium",
            priority=95,
        ),
        PersonalizedOfferItem(
            id=str(uuid4()),
            offer_code="manifestation_calendar",
            title="Activate your manifestation calendar",
            description="Turn your intentions, reminders, and card draws into a sacred monthly practice.",
            target_theme="timing",
            cta_label="Open Manifestation",
            destination="/tarot#manifestation",
            priority=88,
        ),
    ]
    return PersonalizedOffersResponse(offers=offers)


@router.post("/manifestation")
async def save_manifestation(payload: ManifestationCreateRequest, request: Request) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _manifestations_collection(request)
    now = _now()
    document = {
        "id": str(uuid4()),
        "user_email": user_email,
        "date": payload.date,
        "type": "intention",
        "intention_text": payload.intention_text.strip(),
        "linked_reading_id": payload.linked_reading_id,
        "card_name": payload.card_name,
        "bookmarked": False,
        "created_at": now,
    }
    existing = await collection.find_one({"user_email": user_email, "date": payload.date, "type": "intention"})
    if existing:
        await collection.update_one(
            {"id": existing["id"]},
            {"$set": {"intention_text": document["intention_text"], "linked_reading_id": document["linked_reading_id"], "card_name": document["card_name"], "created_at": now}},
        )
        document["id"] = existing["id"]
    else:
        await collection.insert_one(document)
    return {"success": True, "id": document["id"]}


@router.get("/manifestations")
async def get_manifestations(
    request: Request,
    month: str | None = Query(default=None),
    page: int | None = Query(default=None, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
) -> ManifestationMonthResponse | ManifestationJournalResponse:
    user_email = _resolve_user_email(request)
    collection = _manifestations_collection(request)

    if month:
        start = datetime.strptime(f"{month}-01", "%Y-%m-%d").date()
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        docs = await collection.find(
            {
                "user_email": user_email,
                "date": {"$gte": start.isoformat(), "$lt": next_month.isoformat()},
            }
        ).sort("date", 1).to_list(length=500)
        docs_by_date: dict[str, list[dict[str, Any]]] = {}
        for doc in docs:
            docs_by_date.setdefault(str(doc["date"]), []).append(doc)
        readings = _readings_collection(request)
        reading_docs = await readings.find(
            {"user_email": user_email, "doc_type": "report", "prediction_date": {"$gte": start.isoformat(), "$lt": next_month.isoformat()}},
            projection={"prediction_date": 1, "report_id": 1, "cards": 1},
        ).to_list(length=200)
        readings_by_date = {str(doc["prediction_date"]): doc for doc in reading_docs if doc.get("prediction_date")}

        days: list[ManifestationMonthDay] = []
        current = start
        while current < next_month:
            key = current.isoformat()
            day_docs = docs_by_date.get(key, [])
            intention_doc = next((doc for doc in day_docs if doc.get("type") == "intention"), None)
            reminder_docs = [doc for doc in day_docs if doc.get("type") == "reminder"]
            task_docs = [doc for doc in day_docs if doc.get("type") == "task"]
            linked_reading = readings_by_date.get(key)
            days.append(
                ManifestationMonthDay(
                    date=key,
                    moon_phase=_moon_phase_emoji(current),
                    intention=ManifestationEntry(
                        id=str(intention_doc["id"]),
                        date=key,
                        type="intention",
                        intention_text=intention_doc.get("intention_text"),
                        linked_reading_id=intention_doc.get("linked_reading_id"),
                        card_name=intention_doc.get("card_name"),
                        bookmarked=bool(intention_doc.get("bookmarked")),
                        created_at=_serialize_datetime(intention_doc.get("created_at")),
                    ) if intention_doc else None,
                    reminders=[
                        ManifestationEntry(
                            id=str(doc["id"]),
                            date=key,
                            type="reminder",
                            reminder_time=doc.get("reminder_time"),
                            reminder_text=doc.get("reminder_text"),
                            bookmarked=bool(doc.get("bookmarked")),
                            created_at=_serialize_datetime(doc.get("created_at")),
                        )
                        for doc in reminder_docs
                    ],
                    tasks=[
                        ManifestationEntry(
                            id=str(doc["id"]),
                            date=key,
                            type="task",
                            task_text=doc.get("task_text"),
                            task_done=bool(doc.get("task_done")),
                            bookmarked=bool(doc.get("bookmarked")),
                            created_at=_serialize_datetime(doc.get("created_at")),
                        )
                        for doc in task_docs
                    ],
                    linked_reading={
                        "report_id": linked_reading.get("report_id"),
                        "card_name": (linked_reading.get("cards") or [{}])[0].get("name"),
                        "orientation": (linked_reading.get("cards") or [{}])[0].get("orientation"),
                    } if linked_reading else None,
                )
            )
            current += timedelta(days=1)
        return ManifestationMonthResponse(month=month, items=days)

    current_page = page or 1
    skip = (current_page - 1) * limit
    query = {"user_email": user_email, "type": "intention"}
    total = await collection.count_documents(query)
    intention_docs = await collection.find(query).sort("date", -1).skip(skip).limit(limit).to_list(length=limit)
    date_keys = [str(doc["date"]) for doc in intention_docs]
    related_docs = await collection.find({"user_email": user_email, "date": {"$in": date_keys}}).to_list(length=500) if date_keys else []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for doc in related_docs:
        grouped.setdefault(str(doc["date"]), []).append(doc)
    items = [_journal_projection(doc, grouped) for doc in intention_docs]
    return ManifestationJournalResponse(items=items, page=current_page, limit=limit, total=total, has_more=skip + limit < total)


@router.post("/manifestation/reminder")
async def save_manifestation_reminder(payload: ManifestationReminderRequest, request: Request) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _manifestations_collection(request)
    now = _now()
    query = {
        "user_email": user_email,
        "date": payload.date,
        "type": "reminder",
        "reminder_time": payload.reminder_time,
    }
    existing = await collection.find_one(query)
    if existing:
        await collection.update_one({"id": existing["id"]}, {"$set": {"reminder_text": payload.reminder_text.strip(), "created_at": now}})
        reminder_id = str(existing["id"])
    else:
        reminder_id = str(uuid4())
        await collection.insert_one(
            {
                "id": reminder_id,
                "user_email": user_email,
                "date": payload.date,
                "type": "reminder",
                "reminder_time": payload.reminder_time,
                "reminder_text": payload.reminder_text.strip(),
                "bookmarked": False,
                "created_at": now,
            }
        )
    return {"success": True, "id": reminder_id}


@router.get("/manifestation/reminders")
async def get_manifestation_reminders(request: Request, month: str = Query(...)) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    start = datetime.strptime(f"{month}-01", "%Y-%m-%d").date()
    next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    docs = await _manifestations_collection(request).find(
        {
            "user_email": user_email,
            "type": "reminder",
            "date": {"$gte": start.isoformat(), "$lt": next_month.isoformat()},
        }
    ).sort("date", 1).to_list(length=300)
    return {
        "items": [
            ManifestationEntry(
                id=str(doc["id"]),
                date=str(doc["date"]),
                type="reminder",
                reminder_time=doc.get("reminder_time"),
                reminder_text=doc.get("reminder_text"),
                bookmarked=bool(doc.get("bookmarked")),
                created_at=_serialize_datetime(doc.get("created_at")),
            ).model_dump()
            for doc in docs
        ]
    }


@router.patch("/manifestation/task")
async def toggle_manifestation_task(payload: ManifestationTaskRequest, request: Request) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _manifestations_collection(request)
    query = {"user_email": user_email, "date": payload.date, "type": "task", "task_text": payload.task_text.strip()}
    existing = await collection.find_one(query)
    if existing:
        await collection.update_one({"id": existing["id"]}, {"$set": {"task_done": payload.task_done}})
        task_id = str(existing["id"])
    else:
        task_id = str(uuid4())
        await collection.insert_one(
            {
                "id": task_id,
                "user_email": user_email,
                "date": payload.date,
                "type": "task",
                "task_text": payload.task_text.strip(),
                "task_done": payload.task_done,
                "bookmarked": False,
                "created_at": _now(),
            }
        )
    return {"success": True, "id": task_id, "task_done": payload.task_done}


@router.patch("/manifestation/{entry_id}/bookmark", response_model=ManifestationBookmarkResponse)
async def bookmark_manifestation(entry_id: str, request: Request, bookmarked: bool = Body(embed=True)) -> ManifestationBookmarkResponse:
    user_email = _resolve_user_email(request)
    result = await _manifestations_collection(request).update_one(
        {"id": entry_id, "user_email": user_email},
        {"$set": {"bookmarked": bookmarked}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Manifestation entry not found.")
    return ManifestationBookmarkResponse(id=entry_id, bookmarked=bookmarked)


@router.get("/manifestation/stats", response_model=ManifestationStatsResponse)
async def manifestation_stats(request: Request) -> ManifestationStatsResponse:
    user_email = _resolve_user_email(request)
    manifestations = _manifestations_collection(request)
    intentions = await manifestations.find({"user_email": user_email, "type": "intention"}, projection={"date": 1}).sort("date", -1).to_list(length=1000)
    intention_dates = sorted({_parse_date(str(doc["date"])) for doc in intentions if doc.get("date")}, reverse=True)
    streak = 0
    cursor = date.today()
    for day_value in intention_dates:
        if day_value == cursor:
            streak += 1
            cursor = cursor - timedelta(days=1)
        elif day_value > cursor:
            continue
        else:
            break

    readings = _readings_collection(request)
    reading_docs = await readings.find(
        {"user_email": user_email, "doc_type": "report"},
        projection={"cards.name": 1},
    ).to_list(length=1000)
    card_counter: Counter[str] = Counter()
    for doc in reading_docs:
        cards = doc.get("cards") or []
        if cards:
            name = cards[0].get("name")
            if name:
                card_counter[name] += 1

    most_drawn_card = card_counter.most_common(1)[0][0] if card_counter else None
    return ManifestationStatsResponse(
        streak_days=streak,
        total_intentions=len(intentions),
        most_drawn_card=most_drawn_card,
    )
