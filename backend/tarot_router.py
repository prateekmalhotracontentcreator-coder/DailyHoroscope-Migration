from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, Body, Header, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix="/api/tarot", tags=["tarot"])

COLLECTION_NAME = "tarot_readings"
ENGINE_VERSION = "tarot-router-v1"

DepthLevel = Literal["simple", "detailed", "comprehensive"]
FocusArea = Literal["guidance", "love", "career", "healing", "clarity"]
SceneType = Literal["intro", "ritual", "card_reveal", "guidance", "closing"]
DocType = Literal["report", "feedback", "bookmark", "lifecycle"]


class TarotScene(BaseModel):
    model_config = ConfigDict(extra="ignore")

    scene_id: str
    scene_type: SceneType
    title: str | None = None
    text: str
    duration_ms: int = 2500
    meta: dict[str, Any] = Field(default_factory=dict)


class TarotCard(BaseModel):
    model_config = ConfigDict(extra="ignore")

    card_id: str
    name: str
    position_code: str
    position_label: str
    orientation: Literal["upright", "reversed"]
    meaning_snippet: str
    image_url: str | None = None


class TarotReading(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    report_id: str
    doc_type: DocType = "report"
    user_email: str
    reading_type: str
    spread_code: str
    focus_area: str
    language: str = "en"
    depth_level: DepthLevel = "simple"
    prediction_date: str
    is_premium: bool = False
    bookmarked: bool = False
    summary: str
    guidance: str
    affirmation: str
    vedic_context_note: str | None = None
    cards: list[TarotCard] = Field(default_factory=list)
    story_scenes: list[TarotScene] = Field(default_factory=list)
    source_context: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str


class TarotDailyDrawRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_email: str | None = None
    focus_area: FocusArea = "guidance"
    language: str = "en"
    depth_level: DepthLevel = "simple"
    question: str | None = None


class TarotSpreadGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_email: str | None = None
    spread_code: str
    question: str | None = None
    language: str = "en"
    depth_level: DepthLevel = "detailed"


class TarotFeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_email: str | None = None
    report_id: str
    feedback_type: Literal["depth_preference", "resonance", "theme_interest"]
    value: str


class TarotBookmarkRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_email: str | None = None
    bookmarked: bool = True


class TarotGamification(BaseModel):
    model_config = ConfigDict(extra="ignore")

    xp_awarded: int = 0
    coins_awarded: int = 0
    daily_streak: int = 0
    level: int = 1
    new_badges: list[str] = Field(default_factory=list)


class TarotReadingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    reading: TarotReading
    gamification: TarotGamification
    cached: bool = False


class TarotTodayResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    has_reading: bool
    reading: TarotReading | None = None
    gamification: TarotGamification | None = None


class TarotHistoryItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    report_id: str
    reading_type: str
    spread_code: str
    focus_area: str
    prediction_date: str
    depth_level: str
    summary: str
    bookmarked: bool = False
    created_at: str
    cards: list[TarotCard] = Field(default_factory=list)


class TarotHistoryResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[TarotHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    has_more: bool


class TarotFeedbackResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    success: bool = True
    preferred_depth: str | None = None
    message: str


class TarotBookmarkResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    success: bool = True
    report_id: str
    bookmarked: bool


class TarotSpreadPreview(BaseModel):
    model_config = ConfigDict(extra="ignore")

    spread_code: str
    name: str
    description: str
    card_count: int
    is_premium: bool = True
    estimated_duration_sec: int = 120
    depth_access: str = "detailed"


class TarotSpreadListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    spreads: list[TarotSpreadPreview]


class TarotPremiumCheckResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    spread_code: str
    has_access: bool
    reason: str | None = None


class FavorablePeriodItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    report_id: str
    type: str
    window_label: str
    confidence: float
    summary: str
    recommendation: str | None = None
    starts_on: str | None = None
    ends_on: str | None = None


class FavorablePeriodsResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    periods: list[FavorablePeriodItem] = Field(default_factory=list)


class PersonalizedOfferItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    offer_code: str
    title: str
    description: str
    target_theme: str | None = None
    cta_label: str = "Explore"
    destination: str | None = None
    priority: int = 0


class PersonalizedOffersResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    offers: list[PersonalizedOfferItem] = Field(default_factory=list)


DEFAULT_SPREADS = [
    {
        "code": "three_card_love",
        "name": "Love Spread",
        "description": "Explore the emotional movement shaping your next romantic chapter.",
        "card_count": 3,
        "positions": [
            {"code": "past", "label": "Past"},
            {"code": "present", "label": "Present"},
            {"code": "future", "label": "Future"},
        ],
        "estimated_duration_sec": 150,
        "depth_access": "detailed",
    },
    {
        "code": "three_card_career",
        "name": "Career Spread",
        "description": "See how your present momentum is shaping work and direction.",
        "card_count": 3,
        "positions": [
            {"code": "current", "label": "Current Energy"},
            {"code": "obstacle", "label": "Challenge"},
            {"code": "path", "label": "Path Forward"},
        ],
        "estimated_duration_sec": 150,
        "depth_access": "detailed",
    },
    {
        "code": "three_card_guidance",
        "name": "Guidance Spread",
        "description": "Receive a wider message about your unfolding path.",
        "card_count": 3,
        "positions": [
            {"code": "mind", "label": "Mind"},
            {"code": "heart", "label": "Heart"},
            {"code": "spirit", "label": "Spirit"},
        ],
        "estimated_duration_sec": 150,
        "depth_access": "detailed",
    },
]

DEFAULT_CARDS = [
    {
        "id": "the-star",
        "name": "The Star",
        "upright_keywords": ["hope", "renewal", "trust"],
        "reversed_keywords": ["doubt", "fatigue", "delay"],
        "image_url": None,
    },
    {
        "id": "the-lovers",
        "name": "The Lovers",
        "upright_keywords": ["union", "choice", "alignment"],
        "reversed_keywords": ["distance", "conflict", "misalignment"],
        "image_url": None,
    },
    {
        "id": "the-magician",
        "name": "The Magician",
        "upright_keywords": ["manifestation", "skill", "movement"],
        "reversed_keywords": ["confusion", "scattered energy", "delay"],
        "image_url": None,
    },
    {
        "id": "the-moon",
        "name": "The Moon",
        "upright_keywords": ["intuition", "mystery", "unfolding"],
        "reversed_keywords": ["uncertainty", "fog", "mixed signals"],
        "image_url": None,
    },
    {
        "id": "the-empress",
        "name": "The Empress",
        "upright_keywords": ["abundance", "warmth", "growth"],
        "reversed_keywords": ["stalling", "imbalance", "overgiving"],
        "image_url": None,
    },
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_iso() -> str:
    return date.today().isoformat()


def _compute_level(total_xp: int) -> int:
    if total_xp <= 0:
        return 1
    return int((total_xp / 25) ** 0.5) + 1


async def _get_collection(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")
    return getattr(db, COLLECTION_NAME)


async def _resolve_user_email(
    request: Request,
    fallback_email: str | None = None,
    x_user_email: str | None = None,
) -> str:
    if fallback_email:
        return fallback_email.strip().lower()
    if x_user_email:
        return x_user_email.strip().lower()

    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return str(state_user["email"]).strip().lower()

    raise HTTPException(status_code=401, detail="user_email is required")


def _select_card() -> dict[str, Any]:
    return random.choice(DEFAULT_CARDS)


def _select_cards(count: int) -> list[dict[str, Any]]:
    if count >= len(DEFAULT_CARDS):
        return random.sample(DEFAULT_CARDS, len(DEFAULT_CARDS))
    return random.sample(DEFAULT_CARDS, count)


def _build_daily_content(card: dict[str, Any], focus_area: str, depth_level: str) -> dict[str, Any]:
    orientation = random.choice(["upright", "reversed"])
    keywords = card["upright_keywords"] if orientation == "upright" else card["reversed_keywords"]
    snippet = random.choice(keywords)
    summary = f"{card['name']} suggests {snippet} around your {focus_area} energy today."
    guidance = "Move gently and observe what shifts before forcing a decision."
    if depth_level != "simple":
        guidance += " Timing, inner rhythm, and emotional pattern all matter more than speed right now."
    vedic_note = "This card can be read as part of a wider astrological rhythm rather than in isolation."
    affirmation = "I trust aligned timing and clear inner guidance."
    scenes = [
        TarotScene(scene_id="intro", scene_type="intro", title="The veil opens", text="Take a breath. Today's card rises with a message shaped for this moment."),
        TarotScene(scene_id="ritual", scene_type="ritual", title="The deck stirs", text="Let the card that seeks you come forward.", duration_ms=2200),
        TarotScene(scene_id="card_reveal", scene_type="card_reveal", title=card["name"], text=summary, duration_ms=3200, meta={"orientation": orientation}),
        TarotScene(scene_id="guidance", scene_type="guidance", title="Guidance", text=guidance, duration_ms=3200),
        TarotScene(scene_id="closing", scene_type="closing", title="Affirmation", text=affirmation, duration_ms=2200),
    ]
    return {
        "orientation": orientation,
        "summary": summary,
        "guidance": guidance,
        "affirmation": affirmation,
        "vedic_context_note": vedic_note,
        "story_scenes": scenes,
    }


def _build_spread_content(spread: dict[str, Any], cards: list[dict[str, Any]], question: str | None) -> dict[str, Any]:
    card_payloads: list[TarotCard] = []
    scenes: list[TarotScene] = [
        TarotScene(
            scene_id="intro",
            scene_type="intro",
            title=spread["name"],
            text="A deeper tarot spread opens now, revealing the movement around your question.",
            duration_ms=2800,
        ),
        TarotScene(
            scene_id="ritual",
            scene_type="ritual",
            title="The spread forms",
            text="Three cards rise to reveal the path beneath the surface.",
            duration_ms=2400,
        ),
    ]
    for index, card in enumerate(cards):
        position = spread["positions"][index]
        orientation = random.choice(["upright", "reversed"])
        keywords = card["upright_keywords"] if orientation == "upright" else card["reversed_keywords"]
        snippet = random.choice(keywords)
        card_payloads.append(
            TarotCard(
                card_id=card["id"],
                name=card["name"],
                position_code=position["code"],
                position_label=position["label"],
                orientation=orientation,
                meaning_snippet=f"{position['label']}: {snippet}",
                image_url=card.get("image_url"),
            )
        )
        scenes.append(
            TarotScene(
                scene_id=f"card_{index + 1}",
                scene_type="card_reveal",
                title=f"{position['label']} \u00b7 {card['name']}",
                text=f"{card['name']} highlights {snippet} within the {position['label'].lower()} of this spread.",
                duration_ms=3400,
                meta={"orientation": orientation, "position_code": position["code"]},
            )
        )
    guidance = "Rather than forcing a result, follow the strongest present signal and let the next step emerge with timing."
    summary = "This spread suggests movement through reflection, timing, and emotional clarity."
    if question:
        summary += " Your question remains active beneath this pattern."
    vedic_note = "This spread can be read alongside a broader astrological rhythm, adding depth to timing and emotional movement."
    scenes.append(TarotScene(scene_id="guidance", scene_type="guidance", title="Synthesis", text=guidance, duration_ms=3600))
    scenes.append(TarotScene(scene_id="closing", scene_type="closing", title="Vedic Lens", text=vedic_note, duration_ms=2800))
    return {
        "cards": card_payloads,
        "summary": summary,
        "guidance": guidance,
        "affirmation": "I trust aligned timing, deeper clarity, and the path unfolding with wisdom.",
        "vedic_context_note": vedic_note,
        "story_scenes": scenes,
    }


def _report_doc_to_model(doc: dict[str, Any]) -> TarotReading:
    return TarotReading(**doc)


def _gamification_from_history(history_count: int, xp_awarded: int, coins_awarded: int) -> TarotGamification:
    total_xp = history_count * 10 + xp_awarded
    return TarotGamification(
        xp_awarded=xp_awarded,
        coins_awarded=coins_awarded,
        daily_streak=min(history_count + (1 if xp_awarded else 0), 30),
        level=_compute_level(total_xp),
        new_badges=[],
    )


async def _history_count(collection, user_email: str) -> int:
    return await collection.count_documents({"user_email": user_email, "doc_type": "report"})


def _build_feedback_doc(user_email: str, report_id: str, feedback_type: str, value: str) -> dict[str, Any]:
    now = _now_iso()
    preferred_depth = None
    if feedback_type == "depth_preference":
        preferred_depth = {
            "keep_it_simple": "simple",
            "go_deeper_next_time": "detailed",
            "show_the_astrology_behind_this": "comprehensive",
        }.get(value)
    return {
        "id": str(uuid4()),
        "report_id": report_id,
        "doc_type": "feedback",
        "user_email": user_email,
        "feedback_type": feedback_type,
        "value": value,
        "preferred_depth": preferred_depth,
        "created_at": now,
        "updated_at": now,
        "meta": {"engine_version": ENGINE_VERSION},
    }


def _build_bookmark_doc(user_email: str, report_id: str, bookmarked: bool) -> dict[str, Any]:
    now = _now_iso()
    return {
        "id": str(uuid4()),
        "report_id": report_id,
        "doc_type": "bookmark",
        "user_email": user_email,
        "bookmarked": bookmarked,
        "created_at": now,
        "updated_at": now,
        "meta": {"engine_version": ENGINE_VERSION},
    }


def _build_lifecycle_doc(user_email: str, theme: str, summary: str, recommendation: str, days: int, confidence: float) -> dict[str, Any]:
    now_date = date.today()
    now = _now_iso()
    report_id = str(uuid4())
    return {
        "id": str(uuid4()),
        "report_id": report_id,
        "doc_type": "lifecycle",
        "user_email": user_email,
        "type": theme,
        "window_label": f"Next {days} days",
        "confidence": confidence,
        "summary": summary,
        "recommendation": recommendation,
        "starts_on": now_date.isoformat(),
        "ends_on": (now_date + timedelta(days=days)).isoformat(),
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "meta": {"engine_version": ENGINE_VERSION},
    }


@router.get("/daily/today", response_model=TarotTodayResponse)
async def get_today_tarot_reading(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> TarotTodayResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    today = _today_iso()
    doc = await collection.find_one(
        {
            "user_email": resolved_email,
            "doc_type": "report",
            "reading_type": "daily_single",
            "prediction_date": today,
        }
    )
    if not doc:
        return TarotTodayResponse(has_reading=False)
    history_count = await _history_count(collection, resolved_email)
    return TarotTodayResponse(
        has_reading=True,
        reading=_report_doc_to_model(doc),
        gamification=_gamification_from_history(history_count, xp_awarded=0, coins_awarded=0),
    )


@router.post("/daily/draw", response_model=TarotReadingResponse)
async def draw_daily_tarot(
    request: Request,
    payload: TarotDailyDrawRequest,
    x_user_email: str | None = Header(default=None),
) -> TarotReadingResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=payload.user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    today = _today_iso()
    existing = await collection.find_one(
        {
            "user_email": resolved_email,
            "doc_type": "report",
            "reading_type": "daily_single",
            "prediction_date": today,
        }
    )
    history_count = await _history_count(collection, resolved_email)
    if existing:
        return TarotReadingResponse(
            reading=_report_doc_to_model(existing),
            gamification=_gamification_from_history(history_count, xp_awarded=0, coins_awarded=0),
            cached=True,
        )

    card = _select_card()
    content = _build_daily_content(card, payload.focus_area, payload.depth_level)
    now = _now_iso()
    report_id = str(uuid4())
    reading = TarotReading(
        id=str(uuid4()),
        report_id=report_id,
        user_email=resolved_email,
        reading_type="daily_single",
        spread_code="daily_single",
        focus_area=payload.focus_area,
        language=payload.language,
        depth_level=payload.depth_level,
        prediction_date=today,
        summary=content["summary"],
        guidance=content["guidance"],
        affirmation=content["affirmation"],
        vedic_context_note=content["vedic_context_note"],
        cards=[
            TarotCard(
                card_id=card["id"],
                name=card["name"],
                position_code="daily_focus",
                position_label="Daily Focus",
                orientation=content["orientation"],
                meaning_snippet=content["summary"],
                image_url=card.get("image_url"),
            )
        ],
        story_scenes=content["story_scenes"],
        source_context={"question": payload.question or "", "engine_version": ENGINE_VERSION},
        meta={"engine_version": ENGINE_VERSION},
        created_at=now,
        updated_at=now,
    )
    await collection.insert_one(reading.model_dump())
    reward = _gamification_from_history(history_count, xp_awarded=10, coins_awarded=3)
    return TarotReadingResponse(reading=reading, gamification=reward, cached=False)


@router.get("/spreads", response_model=TarotSpreadListResponse)
async def list_tarot_spreads() -> TarotSpreadListResponse:
    return TarotSpreadListResponse(
        spreads=[
            TarotSpreadPreview(
                spread_code=item["code"],
                name=item["name"],
                description=item["description"],
                card_count=item["card_count"],
                is_premium=True,
                estimated_duration_sec=item["estimated_duration_sec"],
                depth_access=item["depth_access"],
            )
            for item in DEFAULT_SPREADS
        ]
    )


@router.get("/spreads/{spread_code}/access", response_model=TarotPremiumCheckResponse)
async def get_spread_access(
    spread_code: str,
    has_premium_access: bool = Query(default=True),
) -> TarotPremiumCheckResponse:
    return TarotPremiumCheckResponse(
        spread_code=spread_code,
        has_access=has_premium_access,
        reason=None if has_premium_access else "Premium access required",
    )


@router.post("/spread/generate", response_model=TarotReadingResponse)
async def generate_tarot_spread(
    request: Request,
    payload: TarotSpreadGenerateRequest,
    x_user_email: str | None = Header(default=None),
    has_premium_access: bool = Query(default=True),
) -> TarotReadingResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=payload.user_email, x_user_email=x_user_email)
    if not has_premium_access:
        raise HTTPException(status_code=403, detail="Premium access required")
    collection = await _get_collection(request)
    spread = next((item for item in DEFAULT_SPREADS if item["code"] == payload.spread_code), None)
    if not spread:
        raise HTTPException(status_code=404, detail="Spread not found")
    selected_cards = _select_cards(spread["card_count"])
    content = _build_spread_content(spread, selected_cards, payload.question)
    now = _now_iso()
    report_id = str(uuid4())
    reading = TarotReading(
        id=str(uuid4()),
        report_id=report_id,
        user_email=resolved_email,
        reading_type=payload.spread_code,
        spread_code=payload.spread_code,
        focus_area=payload.spread_code.replace("three_card_", ""),
        language=payload.language,
        depth_level=payload.depth_level,
        prediction_date=_today_iso(),
        is_premium=True,
        summary=content["summary"],
        guidance=content["guidance"],
        affirmation=content["affirmation"],
        vedic_context_note=content["vedic_context_note"],
        cards=content["cards"],
        story_scenes=content["story_scenes"],
        source_context={"question": payload.question or "", "engine_version": ENGINE_VERSION},
        meta={"engine_version": ENGINE_VERSION},
        created_at=now,
        updated_at=now,
    )
    await collection.insert_one(reading.model_dump())
    history_count = await _history_count(collection, resolved_email)
    reward = _gamification_from_history(history_count, xp_awarded=25, coins_awarded=5)
    return TarotReadingResponse(reading=reading, gamification=reward, cached=False)


@router.get("/reading/{report_id}", response_model=TarotReading)
async def get_tarot_reading(
    request: Request,
    report_id: str,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> TarotReading:
    resolved_email = await _resolve_user_email(request, fallback_email=user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    doc = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "report_id": report_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Reading not found")
    return _report_doc_to_model(doc)


@router.post("/feedback", response_model=TarotFeedbackResponse)
async def submit_tarot_feedback(
    request: Request,
    payload: TarotFeedbackRequest,
    x_user_email: str | None = Header(default=None),
) -> TarotFeedbackResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=payload.user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    report = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "report_id": payload.report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Reading not found")
    feedback_doc = _build_feedback_doc(resolved_email, payload.report_id, payload.feedback_type, payload.value)
    await collection.insert_one(feedback_doc)
    return TarotFeedbackResponse(
        preferred_depth=feedback_doc.get("preferred_depth"),
        message="Your future readings will adapt to this preference." if feedback_doc.get("preferred_depth") else "Feedback received.",
    )


@router.get("/history", response_model=TarotHistoryResponse)
async def get_tarot_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    bookmarked: bool | None = Query(default=None),
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> TarotHistoryResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)

    bookmark_report_ids: set[str] | None = None
    if bookmarked is not None:
        bookmark_docs = await collection.find(
            {"user_email": resolved_email, "doc_type": "bookmark", "bookmarked": bookmarked}
        ).to_list(length=1000)
        bookmark_report_ids = {doc["report_id"] for doc in bookmark_docs}

    query: dict[str, Any] = {"user_email": resolved_email, "doc_type": "report"}
    if bookmark_report_ids is not None:
        if not bookmark_report_ids:
            return TarotHistoryResponse(items=[], page=page, limit=limit, total=0, has_more=False)
        query["report_id"] = {"$in": list(bookmark_report_ids)}

    skip = (page - 1) * limit
    docs = await collection.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
    total = await collection.count_documents(query)
    bookmark_docs = await collection.find({"user_email": resolved_email, "doc_type": "bookmark", "bookmarked": True}).to_list(length=1000)
    active_bookmarks = {doc["report_id"] for doc in bookmark_docs}
    items = [
        TarotHistoryItem(
            id=doc["id"],
            report_id=doc["report_id"],
            reading_type=doc["reading_type"],
            spread_code=doc["spread_code"],
            focus_area=doc["focus_area"],
            prediction_date=doc["prediction_date"],
            depth_level=doc["depth_level"],
            summary=doc["summary"],
            bookmarked=doc["report_id"] in active_bookmarks,
            created_at=doc["created_at"],
            cards=[TarotCard(**card) for card in doc.get("cards", [])],
        )
        for doc in docs
    ]
    return TarotHistoryResponse(items=items, page=page, limit=limit, total=total, has_more=skip + limit < total)


@router.post("/history/{report_id}/bookmark", response_model=TarotBookmarkResponse)
async def bookmark_tarot_reading(
    request: Request,
    report_id: str,
    payload: TarotBookmarkRequest,
    x_user_email: str | None = Header(default=None),
) -> TarotBookmarkResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=payload.user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    report = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "report_id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Reading not found")
    bookmark_doc = _build_bookmark_doc(resolved_email, report_id, payload.bookmarked)
    await collection.insert_one(bookmark_doc)
    return TarotBookmarkResponse(report_id=report_id, bookmarked=payload.bookmarked)


@router.get("/favorable-periods", response_model=FavorablePeriodsResponse)
async def get_favorable_periods(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> FavorablePeriodsResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    docs = await collection.find(
        {"user_email": resolved_email, "doc_type": "lifecycle", "status": "active"}
    ).sort("created_at", -1).to_list(length=20)
    if not docs:
        fallback_docs = [
            _build_lifecycle_doc(
                resolved_email,
                "love",
                "A favorable romantic phase may be drawing closer, with more emotional openness than usual.",
                "A deeper love spread can help you understand the shape of this opening.",
                45,
                0.78,
            ),
            _build_lifecycle_doc(
                resolved_email,
                "guidance",
                "This is a good period for reflective choices, inner clarity, and gentle realignment.",
                "Use your daily ritual consistently to track how this energy develops.",
                21,
                0.69,
            ),
        ]
        periods = [
            FavorablePeriodItem(
                id=doc["id"],
                report_id=doc["report_id"],
                type=doc["type"],
                window_label=doc["window_label"],
                confidence=float(doc["confidence"]),
                summary=doc["summary"],
                recommendation=doc.get("recommendation"),
                starts_on=doc.get("starts_on"),
                ends_on=doc.get("ends_on"),
            )
            for doc in fallback_docs
        ]
        return FavorablePeriodsResponse(periods=periods)
    return FavorablePeriodsResponse(
        periods=[
            FavorablePeriodItem(
                id=doc["id"],
                report_id=doc["report_id"],
                type=doc["type"],
                window_label=doc["window_label"],
                confidence=float(doc["confidence"]),
                summary=doc["summary"],
                recommendation=doc.get("recommendation"),
                starts_on=doc.get("starts_on"),
                ends_on=doc.get("ends_on"),
            )
            for doc in docs
        ]
    )


@router.get("/offers", response_model=PersonalizedOffersResponse)
async def get_personalized_offers(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> PersonalizedOffersResponse:
    resolved_email = await _resolve_user_email(request, fallback_email=user_email, x_user_email=x_user_email)
    collection = await _get_collection(request)
    feedback_docs = await collection.find(
        {"user_email": resolved_email, "doc_type": "feedback", "preferred_depth": {"$ne": None}}
    ).sort("created_at", -1).to_list(length=10)
    preferred_depth = feedback_docs[0]["preferred_depth"] if feedback_docs else "simple"
    offers = [
        PersonalizedOfferItem(
            id=str(uuid4()),
            offer_code="premium_love_spread",
            title="Unlock a deeper love spread",
            description="Step into a cinematic 3-card reading focused on your next romantic phase.",
            target_theme="love",
            cta_label="Explore",
            destination="/tarot/spreads",
            priority=90,
        )
    ]
    if preferred_depth in {"detailed", "comprehensive"}:
        offers.append(
            PersonalizedOfferItem(
                id=str(uuid4()),
                offer_code="astro_tarot_upgrade",
                title="See the astrology behind your cards",
                description="Unlock richer Astro + Tarot interpretation for timing, love, and emotional movement.",
                target_theme="guidance",
                cta_label="Unlock",
                destination="/pricing",
                priority=95,
            )
        )
    offers.sort(key=lambda item: item.priority, reverse=True)
    return PersonalizedOffersResponse(offers=offers)
