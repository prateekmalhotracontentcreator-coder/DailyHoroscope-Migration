from __future__ import annotations

# ENGINE_VERSION: lumina-router-1.1.0
# Host app wiring:
# from backend.lumina_router import router as lumina_router
# app.include_router(lumina_router)

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from lumina_prompt_service import (
    compose_prayer_declaration,
    generate_chaplain_response,
    generate_confession,
    generate_daily_verse_breakdown,
    generate_glory_scrolls,
    generate_kingdom_vision,
    generate_scripture_paragraphs,
    generate_situation_insight,
    get_daily_scripture,
    normalize_scripture_mode,
)


router = APIRouter(prefix="/api/lumina", tags=["lumina"])

ScriptureMode = Literal["BIBLE", "GITA"]
PrayerAction = Literal["STRENGTHEN", "REALIZE"]

MANIFESTATION_DAYS = [
    {"day": 1, "title": "The Power of Belief", "verse": "Mark 11:24", "prompt": "Write down three things you are asking God for today, believing He has already provided them."},
    {"day": 2, "title": "Walking in Faith", "verse": "Hebrews 11:1", "prompt": "Describe how you would move today if your biggest prayer were already on the way."},
    {"day": 3, "title": "Abundance Mentality", "verse": "Philippians 4:19", "prompt": "List five ways provision has already reached your life, even in quiet forms."},
    {"day": 4, "title": "Speaking the Word", "verse": "Proverbs 18:21", "prompt": "Replace one fearful sentence with a faith-filled declaration you can repeat today."},
    {"day": 5, "title": "The Promised Land", "verse": "Hebrews 11:8", "prompt": "Write a vivid picture of the future you believe God is leading you toward."},
    {"day": 6, "title": "Inner Agreement", "verse": "Amos 3:3", "prompt": "Journal where your desires and your discipline still need to come into agreement."},
    {"day": 7, "title": "Guarding the Heart", "verse": "Proverbs 4:23", "prompt": "Name the emotional pattern that most often drains your faith and write its replacement."},
    {"day": 8, "title": "Holy Focus", "verse": "Matthew 6:33", "prompt": "Identify the one thing you need to seek first before chasing ten lesser things."},
    {"day": 9, "title": "Courage Under Pressure", "verse": "Joshua 1:9", "prompt": "Record one brave action that would honor your calling this week."},
    {"day": 10, "title": "Renewed Mind", "verse": "Romans 12:2", "prompt": "Write the old story you are leaving and the renewed story you are stepping into."},
    {"day": 11, "title": "Receiving Wisdom", "verse": "James 1:5", "prompt": "Ask for wisdom about one decision and write what faithful patience would look like."},
    {"day": 12, "title": "The Seed of Speech", "verse": "Mark 4:20", "prompt": "Choose one sentence you want to sow into your future every morning this week."},
    {"day": 13, "title": "Stewarding Small Beginnings", "verse": "Zechariah 4:10", "prompt": "List the small assignments you may have underestimated and how you will honor them."},
    {"day": 14, "title": "Peace as Governance", "verse": "Colossians 3:15", "prompt": "Write about where peace is leading you and where anxiety has been making decisions for you."},
    {"day": 15, "title": "Faithful Labor", "verse": "Colossians 3:23", "prompt": "Describe how excellence and devotion can work together in your current responsibilities."},
    {"day": 16, "title": "Open Hands", "verse": "Ecclesiastes 3:11", "prompt": "Release one timeline you have been gripping and write a more surrendered response."},
    {"day": 17, "title": "The Language of Gratitude", "verse": "1 Thessalonians 5:18", "prompt": "Write a gratitude list that names both visible blessings and hidden protection."},
    {"day": 18, "title": "Vision With Structure", "verse": "Habakkuk 2:2", "prompt": "Turn one dream into a plan with three practical next steps."},
    {"day": 19, "title": "Strength for the Waiting", "verse": "Isaiah 40:31", "prompt": "Describe how waiting can become preparation instead of stagnation."},
    {"day": 20, "title": "Joyful Endurance", "verse": "Nehemiah 8:10", "prompt": "Write how joy can become a strength source in the part of life that feels heavy."},
    {"day": 21, "title": "Consecrated Momentum", "verse": "Proverbs 16:3", "prompt": "Summarize what you are now ready to commit, release, and build with fresh clarity."},
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SourceLink(StrictModel):
    title: str
    uri: str


class DailyVerseResponse(StrictModel):
    scripture_mode: ScriptureMode
    verse_reference: str
    verse_text: str
    revelation_context: str
    speak_it: str
    think_it: str
    do_it: str
    prophets_promise: str
    daily_application: str


class ChaplainRequest(StrictModel):
    question: str
    image_base64: str | None = None
    scripture_mode: ScriptureMode = "BIBLE"


class ChaplainResponse(StrictModel):
    text: str
    sources: list[SourceLink] = Field(default_factory=list)


class ScriptureVerse(StrictModel):
    ref: str
    text: str


class ScriptureParagraph(StrictModel):
    verses: list[ScriptureVerse]
    interpretation: str


class ScriptureResponse(StrictModel):
    scripture_mode: ScriptureMode
    book: str
    chapter: int
    version: str
    paragraphs: list[ScriptureParagraph]


class PrayerCreateRequest(StrictModel):
    user_email: str
    title: str | None = None
    petition_seed: str
    content: str | None = None
    is_ai_composed: bool = False
    scripture_mode: ScriptureMode = "BIBLE"


class PrayerRecord(StrictModel):
    id: str
    user_email: str
    title: str
    petition_seed: str
    content: str
    strength: int
    is_realized: bool
    timestamp: datetime
    is_ai_composed: bool


class PrayerActionRequest(StrictModel):
    action: PrayerAction


class ManifestationDay(StrictModel):
    day: int
    title: str
    verse: str
    prompt: str


class ManifestationResponse(StrictModel):
    days: list[ManifestationDay]
    completed_days: list[int] = Field(default_factory=list)


class ManifestationProgressResponse(StrictModel):
    completed_days: list[int] = Field(default_factory=list)


class ConfessionRequest(StrictModel):
    category: str
    user_name: str
    scripture_mode: ScriptureMode = "BIBLE"


class ConfessionResponse(StrictModel):
    text: str


class SituationRequest(StrictModel):
    situation: str
    scripture_mode: ScriptureMode = "BIBLE"


class SituationResponse(StrictModel):
    analysis: str
    miracle_story: str
    narrative: str


class KingdomVisionRequest(StrictModel):
    goal: str
    user_name: str


class KingdomVisionResponse(StrictModel):
    mandate: str
    scripture: str
    action_plan: list[str] = Field(default_factory=list)
    blueprint_prompt: str


class GloryScroll(StrictModel):
    category: Literal["WORD", "WALK", "MARKETPLACE"]
    title: str
    content: str
    verse: str


def _db(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available on request.app.state.db.")
    return db


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(value: str | None) -> str:
    return str(value or "").strip().lower()


def _resolve_user_email(request: Request, explicit_email: str | None = None) -> str:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return _normalize_email(str(state_user["email"]))
    email = _normalize_email(explicit_email)
    if email:
        return email
    raise HTTPException(status_code=401, detail="Authenticated user email or explicit user_email is required.")


def _prayer_collection(request: Request):
    return _db(request).lumina_prayers


def _users_collection(request: Request):
    return _db(request).users


def _manifestation_doc_filter(user_email: str) -> dict[str, Any]:
    return {"$or": [{"email": user_email}, {"user_email": user_email}]}


def _manifestation_progress(doc: dict[str, Any] | None) -> list[int]:
    raw = []
    if isinstance(doc, dict):
        raw = doc.get("lumina_progress") or doc.get("manifestationProgress") or []
    values = sorted({int(item) for item in raw if isinstance(item, int) or str(item).isdigit()})
    return [value for value in values if 1 <= value <= 21]


def _derive_title(title: str | None, petition_seed: str) -> str:
    cleaned = str(title or "").strip()
    if cleaned:
        return cleaned
    words = petition_seed.strip().split()
    return " ".join(words[:4]).title() or "Sacred Declaration"


def _serialize_prayer(document: dict[str, Any]) -> PrayerRecord:
    return PrayerRecord(
        id=str(document["id"]),
        user_email=str(document["user_email"]),
        title=str(document["title"]),
        petition_seed=str(document["petition_seed"]),
        content=str(document["content"]),
        strength=int(document.get("strength", 1)),
        is_realized=bool(document.get("is_realized", False)),
        timestamp=document.get("timestamp") or _now(),
        is_ai_composed=bool(document.get("is_ai_composed", False)),
    )


def _verse_cache_key(scripture_mode: str, reference: str) -> str:
    """Matches the key format used by seed_faith_daily_haiku.py."""
    slug = reference.lower().replace(" ", "-").replace(":", "-")
    return f"{scripture_mode}_{slug}"


@router.get("/daily-verse", response_model=DailyVerseResponse)
async def get_daily_verse(
    scripture_mode: ScriptureMode = Query("BIBLE"),
    request: Request = None,
) -> DailyVerseResponse:
    normalized = normalize_scripture_mode(scripture_mode)

    # ── Check pre-seeded verse cache (no API cost) ───────────────────────────
    if request is not None:
        try:
            db = getattr(getattr(request.app, "state", None), "db", None)
            if db is not None:
                verse = get_daily_scripture(normalized)
                cache_key = _verse_cache_key(normalized, verse["reference"])
                cached = await db.lumina_verse_cache.find_one({"cache_key": cache_key})
                if cached:
                    cached.pop("_id", None)
                    cached.pop("cache_key", None)
                    cached.pop("scripture_mode", None)
                    cached.pop("ai_generated", None)
                    cached.pop("model", None)
                    return DailyVerseResponse(scripture_mode=normalized, **cached)
        except Exception:
            pass  # fall through to live API call on any cache error

    # ── Fall back to live Anthropic API call ─────────────────────────────────
    content = await generate_daily_verse_breakdown(normalized)
    return DailyVerseResponse(scripture_mode=normalized, **content)


@router.post("/chaplain", response_model=ChaplainResponse)
async def ai_chaplain(payload: ChaplainRequest) -> ChaplainResponse:
    content = await generate_chaplain_response(payload.question, payload.image_base64, payload.scripture_mode)
    return ChaplainResponse(
        text=str(content.get("text") or ""),
        sources=[SourceLink(**item) for item in content.get("sources") or []],
    )


@router.get("/scripture", response_model=ScriptureResponse)
async def get_scripture(
    book: str = Query(..., min_length=1),
    chapter: int = Query(..., ge=1),
    version: str = Query("KJV"),
    scripture_mode: ScriptureMode = Query("BIBLE"),
) -> ScriptureResponse:
    normalized = normalize_scripture_mode(scripture_mode)
    paragraphs = await generate_scripture_paragraphs(book=book, chapter=chapter, version=version, scripture_mode=normalized)
    return ScriptureResponse(
        scripture_mode=normalized,
        book=book,
        chapter=chapter,
        version=version,
        paragraphs=[ScriptureParagraph(**paragraph) for paragraph in paragraphs],
    )


@router.post("/prayers", response_model=PrayerRecord)
async def create_prayer(payload: PrayerCreateRequest, request: Request) -> PrayerRecord:
    user_email = _resolve_user_email(request, payload.user_email)
    title = _derive_title(payload.title, payload.petition_seed)
    content = str(payload.content or "").strip()
    if payload.is_ai_composed and not content:
        content = await compose_prayer_declaration(title=title, petition_seed=payload.petition_seed, scripture_mode=payload.scripture_mode)
    if not content:
        content = payload.petition_seed.strip()

    document = {
        "id": str(uuid4()),
        "user_email": user_email,
        "title": title,
        "petition_seed": payload.petition_seed.strip(),
        "content": content,
        "strength": 1,
        "is_realized": False,
        "timestamp": _now(),
        "is_ai_composed": payload.is_ai_composed,
    }
    await _prayer_collection(request).insert_one(document)
    return _serialize_prayer(document)


@router.get("/prayers", response_model=list[PrayerRecord])
async def list_prayers(request: Request, user_email: str = Query(..., min_length=3)) -> list[PrayerRecord]:
    resolved_email = _resolve_user_email(request, user_email)
    documents = await _prayer_collection(request).find({"user_email": resolved_email}).sort("timestamp", -1).to_list(length=200)
    return [_serialize_prayer(document) for document in documents]


@router.patch("/prayers/{prayer_id}", response_model=PrayerRecord)
async def update_prayer(prayer_id: str, payload: PrayerActionRequest, request: Request) -> PrayerRecord:
    collection = _prayer_collection(request)
    state_user = getattr(request.state, "user", None)
    filters: dict[str, Any] = {"id": prayer_id}
    if isinstance(state_user, dict) and state_user.get("email"):
        filters["user_email"] = _normalize_email(str(state_user["email"]))

    if payload.action == "STRENGTHEN":
        await collection.update_one(filters, {"$inc": {"strength": 1}})
    else:
        await collection.update_one(filters, {"$set": {"is_realized": True}})

    document = await collection.find_one(filters)
    if not document:
        raise HTTPException(status_code=404, detail="Prayer declaration not found.")
    return _serialize_prayer(document)


@router.get("/manifestation", response_model=ManifestationResponse)
async def get_manifestation(request: Request, user_email: str = Query(..., min_length=3)) -> ManifestationResponse:
    resolved_email = _resolve_user_email(request, user_email)
    document = await _users_collection(request).find_one(_manifestation_doc_filter(resolved_email), {"lumina_progress": 1, "manifestationProgress": 1})
    return ManifestationResponse(
        days=[ManifestationDay(**item) for item in MANIFESTATION_DAYS],
        completed_days=_manifestation_progress(document),
    )


@router.post("/manifestation/{day}", response_model=ManifestationProgressResponse)
async def complete_manifestation_day(day: int, request: Request, user_email: str = Query(..., min_length=3)) -> ManifestationProgressResponse:
    if not 1 <= day <= 21:
        raise HTTPException(status_code=400, detail="Manifestation day must be between 1 and 21.")

    resolved_email = _resolve_user_email(request, user_email)
    await _users_collection(request).update_one(
        _manifestation_doc_filter(resolved_email),
        {
            "$set": {"updated_at": _now(), "email": resolved_email, "user_email": resolved_email},
            "$setOnInsert": {"created_at": _now()},
            "$addToSet": {"lumina_progress": day},
        },
        upsert=True,
    )
    document = await _users_collection(request).find_one(_manifestation_doc_filter(resolved_email), {"lumina_progress": 1, "manifestationProgress": 1})
    return ManifestationProgressResponse(completed_days=_manifestation_progress(document))


@router.post("/confessions", response_model=ConfessionResponse)
async def create_confession(payload: ConfessionRequest) -> ConfessionResponse:
    text = await generate_confession(payload.category, payload.user_name, payload.scripture_mode)
    return ConfessionResponse(text=text)


@router.post("/situation", response_model=SituationResponse)
async def analyze_situation(payload: SituationRequest) -> SituationResponse:
    content = await generate_situation_insight(payload.situation, payload.scripture_mode)
    return SituationResponse(**content)


@router.post("/kingdom-vision", response_model=KingdomVisionResponse)
async def create_kingdom_vision(payload: KingdomVisionRequest) -> KingdomVisionResponse:
    content = await generate_kingdom_vision(payload.goal, payload.user_name)
    return KingdomVisionResponse(**content)


@router.get("/glory-scrolls", response_model=list[GloryScroll])
async def get_glory_scrolls(
    user_name: str = Query(..., min_length=1),
    scripture_mode: ScriptureMode = Query("BIBLE"),
) -> list[GloryScroll]:
    content = await generate_glory_scrolls(user_name, scripture_mode)
    return [GloryScroll(**item) for item in content]
