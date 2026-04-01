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
    doc_type: DocType
    user_email: str
    focus_area: FocusArea | None = None
    question: str | None = None
    depth_level: DepthLevel
    cards: list[TarotCard]
    scenes: list[TarotScene]
    affirmation: str | None = None
    spread_type: str | None = None
    xp_earned: int = 0
    bookmarked: bool = False
    created_at: str


class TarotSpread(BaseModel):
    model_config = ConfigDict(extra="ignore")

    spread_id: str
    name: str
    description: str
    card_count: int
    positions: list[str]
    premium: bool = False


class DailyDrawRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    focus_area: FocusArea = "guidance"
    question: str | None = None
    depth_level: DepthLevel = "detailed"


class SpreadDrawRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    spread_id: str
    focus_area: FocusArea = "guidance"
    question: str | None = None


class BookmarkRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    report_id: str
    bookmarked: bool


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    report_id: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


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


DEFAULT_CARDS: list[dict] = [
    # ── Major Arcana (22) ────────────────────────────────────────────────────
    {"id": "the-fool",          "name": "The Fool",           "suit": "major", "rank": "0",
     "upright_keywords": ["new beginnings","spontaneity","free spirit"],
     "reversed_keywords": ["recklessness","risk","naivety"]},
    {"id": "the-magician",      "name": "The Magician",       "suit": "major", "rank": "I",
     "upright_keywords": ["manifestation","resourcefulness","power"],
     "reversed_keywords": ["manipulation","untapped potential","poor planning"]},
    {"id": "the-high-priestess","name": "The High Priestess", "suit": "major", "rank": "II",
     "upright_keywords": ["intuition","mystery","inner knowledge"],
     "reversed_keywords": ["secrets","disconnection","withdrawal"]},
    {"id": "the-empress",       "name": "The Empress",        "suit": "major", "rank": "III",
     "upright_keywords": ["femininity","beauty","nature","abundance"],
     "reversed_keywords": ["creative block","dependence","smothering"]},
    {"id": "the-emperor",       "name": "The Emperor",        "suit": "major", "rank": "IV",
     "upright_keywords": ["authority","structure","control","fatherhood"],
     "reversed_keywords": ["domination","inflexibility","loss of control"]},
    {"id": "the-hierophant",    "name": "The Hierophant",     "suit": "major", "rank": "V",
     "upright_keywords": ["tradition","conformity","morality","ethics"],
     "reversed_keywords": ["rebellion","subversiveness","unconventionality"]},
    {"id": "the-lovers",        "name": "The Lovers",         "suit": "major", "rank": "VI",
     "upright_keywords": ["love","harmony","relationships","values alignment"],
     "reversed_keywords": ["disharmony","imbalance","misaligned values"]},
    {"id": "the-chariot",       "name": "The Chariot",        "suit": "major", "rank": "VII",
     "upright_keywords": ["control","willpower","success","determination"],
     "reversed_keywords": ["lack of control","opposition","lack of direction"]},
    {"id": "strength",          "name": "Strength",           "suit": "major", "rank": "VIII",
     "upright_keywords": ["strength","courage","patience","inner power"],
     "reversed_keywords": ["inner strength doubts","low energy","self-doubt"]},
    {"id": "the-hermit",        "name": "The Hermit",         "suit": "major", "rank": "IX",
     "upright_keywords": ["soul searching","introspection","being alone","inner guidance"],
     "reversed_keywords": ["isolation","loneliness","withdrawal"]},
    {"id": "wheel-of-fortune",  "name": "Wheel of Fortune",   "suit": "major", "rank": "X",
     "upright_keywords": ["good luck","karma","life cycles","destiny"],
     "reversed_keywords": ["bad luck","resistance to change","breaking cycles"]},
    {"id": "justice",           "name": "Justice",            "suit": "major", "rank": "XI",
     "upright_keywords": ["justice","fairness","truth","cause and effect"],
     "reversed_keywords": ["unfairness","lack of accountability","dishonesty"]},
    {"id": "the-hanged-man",    "name": "The Hanged Man",     "suit": "major", "rank": "XII",
     "upright_keywords": ["pause","surrender","letting go","new perspectives"],
     "reversed_keywords": ["delays","resistance","stalling","indecision"]},
    {"id": "death",             "name": "Death",              "suit": "major", "rank": "XIII",
     "upright_keywords": ["endings","change","transformation","transition"],
     "reversed_keywords": ["resistance to change","personal transformation","inner purging"]},
    {"id": "temperance",        "name": "Temperance",         "suit": "major", "rank": "XIV",
     "upright_keywords": ["balance","moderation","patience","purpose"],
     "reversed_keywords": ["imbalance","excess","self-healing","re-alignment"]},
    {"id": "the-devil",         "name": "The Devil",          "suit": "major", "rank": "XV",
     "upright_keywords": ["shadow self","attachment","addiction","restriction"],
     "reversed_keywords": ["releasing limiting beliefs","exploring dark thoughts","detachment"]},
    {"id": "the-tower",         "name": "The Tower",          "suit": "major", "rank": "XVI",
     "upright_keywords": ["sudden change","upheaval","chaos","revelation"],
     "reversed_keywords": ["personal transformation","fear of change","averting disaster"]},
    {"id": "the-star",          "name": "The Star",           "suit": "major", "rank": "XVII",
     "upright_keywords": ["hope","faith","purpose","renewal","spirituality"],
     "reversed_keywords": ["lack of faith","despair","self-trust","disconnection"]},
    {"id": "the-moon",          "name": "The Moon",           "suit": "major", "rank": "XVIII",
     "upright_keywords": ["illusion","fear","the unconscious","confusion"],
     "reversed_keywords": ["release of fear","repressed emotion","inner confusion"]},
    {"id": "the-sun",           "name": "The Sun",            "suit": "major", "rank": "XIX",
     "upright_keywords": ["positivity","fun","warmth","success","vitality"],
     "reversed_keywords": ["inner child","feeling down","overly optimistic"]},
    {"id": "judgement",         "name": "Judgement",          "suit": "major", "rank": "XX",
     "upright_keywords": ["judgement","rebirth","inner calling","absolution"],
     "reversed_keywords": ["self-doubt","inner critic","ignoring the call"]},
    {"id": "the-world",         "name": "The World",          "suit": "major", "rank": "XXI",
     "upright_keywords": ["completion","integration","accomplishment","travel"],
     "reversed_keywords": ["seeking personal closure","short-cuts","delays"]},

    # ── Wands (14) ───────────────────────────────────────────────────────────
    {"id": "wands-ace",  "name": "Ace of Wands",    "suit": "wands", "rank": "ace",
     "upright_keywords": ["inspiration","new opportunities","growth","potential"],
     "reversed_keywords": ["delays","lack of motivation","weighed down"]},
    {"id": "wands-02",   "name": "Two of Wands",    "suit": "wands", "rank": "02",
     "upright_keywords": ["planning","making decisions","leaving home"],
     "reversed_keywords": ["fear of unknown","lack of planning","playing it safe"]},
    {"id": "wands-03",   "name": "Three of Wands",  "suit": "wands", "rank": "03",
     "upright_keywords": ["expansion","foresight","overseas opportunities"],
     "reversed_keywords": ["playing small","lack of foresight","setbacks"]},
    {"id": "wands-04",   "name": "Four of Wands",   "suit": "wands", "rank": "04",
     "upright_keywords": ["celebration","harmony","marriage","home"],
     "reversed_keywords": ["breakdown in communication","transition"]},
    {"id": "wands-05",   "name": "Five of Wands",   "suit": "wands", "rank": "05",
     "upright_keywords": ["conflict","disagreements","competition"],
     "reversed_keywords": ["avoiding conflict","respecting differences"]},
    {"id": "wands-06",   "name": "Six of Wands",    "suit": "wands", "rank": "06",
     "upright_keywords": ["success","public recognition","progress"],
     "reversed_keywords": ["private achievement","egotism","fall from grace"]},
    {"id": "wands-07",   "name": "Seven of Wands",  "suit": "wands", "rank": "07",
     "upright_keywords": ["challenge","competition","perseverance"],
     "reversed_keywords": ["exhaustion","giving up","overwhelmed"]},
    {"id": "wands-08",   "name": "Eight of Wands",  "suit": "wands", "rank": "08",
     "upright_keywords": ["movement","fast paced change","action"],
     "reversed_keywords": ["delays","frustration","resisting change"]},
    {"id": "wands-09",   "name": "Nine of Wands",   "suit": "wands", "rank": "09",
     "upright_keywords": ["resilience","courage","persistence"],
     "reversed_keywords": ["exhaustion","stubbornness","defensive"]},
    {"id": "wands-10",   "name": "Ten of Wands",    "suit": "wands", "rank": "10",
     "upright_keywords": ["burden","extra responsibility","hard work"],
     "reversed_keywords": ["doing it all","collapse","inability to delegate"]},
    {"id": "wands-page", "name": "Page of Wands",   "suit": "wands", "rank": "page",
     "upright_keywords": ["exploration","excitement","freedom"],
     "reversed_keywords": ["newly formed ideas","redirecting energy"]},
    {"id": "wands-knight","name": "Knight of Wands", "suit": "wands", "rank": "knight",
     "upright_keywords": ["energy","passion","adventure","impulsiveness"],
     "reversed_keywords": ["haste","delays","scattered energy"]},
    {"id": "wands-queen","name": "Queen of Wands",  "suit": "wands", "rank": "queen",
     "upright_keywords": ["courage","determination","joy","vibrancy"],
     "reversed_keywords": ["selfishness","jealousy","insecurities"]},
    {"id": "wands-king", "name": "King of Wands",   "suit": "wands", "rank": "king",
     "upright_keywords": ["natural-born leader","vision","entrepreneur"],
     "reversed_keywords": ["impulsiveness","haste","ruthless"]},

    # ── Cups (14) ────────────────────────────────────────────────────────────
    {"id": "cups-ace",   "name": "Ace of Cups",     "suit": "cups",  "rank": "ace",
     "upright_keywords": ["new feelings","spirituality","intuition"],
     "reversed_keywords": ["emotional loss","blocked creativity","emptiness"]},
    {"id": "cups-02",    "name": "Two of Cups",     "suit": "cups",  "rank": "02",
     "upright_keywords": ["unified love","partnership","mutual attraction"],
     "reversed_keywords": ["self-love","break-ups","disharmony"]},
    {"id": "cups-03",    "name": "Three of Cups",   "suit": "cups",  "rank": "03",
     "upright_keywords": ["celebration","friendship","creativity"],
     "reversed_keywords": ["gossip","overindulgence","isolation"]},
    {"id": "cups-04",    "name": "Four of Cups",    "suit": "cups",  "rank": "04",
     "upright_keywords": ["meditation","contemplation","apathy"],
     "reversed_keywords": ["sudden awareness","choosing happiness"]},
    {"id": "cups-05",    "name": "Five of Cups",    "suit": "cups",  "rank": "05",
     "upright_keywords": ["regret","failure","disappointment"],
     "reversed_keywords": ["personal setbacks","self-forgiveness","moving on"]},
    {"id": "cups-06",    "name": "Six of Cups",     "suit": "cups",  "rank": "06",
     "upright_keywords": ["revisiting past","childhood memories","innocence"],
     "reversed_keywords": ["living in the past","forgiveness","lacking playfulness"]},
    {"id": "cups-07",    "name": "Seven of Cups",   "suit": "cups",  "rank": "07",
     "upright_keywords": ["opportunities","choices","wishful thinking"],
     "reversed_keywords": ["alignment","personal values","overwhelmed by choices"]},
    {"id": "cups-08",    "name": "Eight of Cups",   "suit": "cups",  "rank": "08",
     "upright_keywords": ["disappointment","abandonment","withdrawal"],
     "reversed_keywords": ["trying one more time","indecision","fear of loss"]},
    {"id": "cups-09",    "name": "Nine of Cups",    "suit": "cups",  "rank": "09",
     "upright_keywords": ["contentment","satisfaction","gratitude"],
     "reversed_keywords": ["inner happiness","materialism","dissatisfaction"]},
    {"id": "cups-10",    "name": "Ten of Cups",     "suit": "cups",  "rank": "10",
     "upright_keywords": ["divine love","blissful relationships","harmony"],
     "reversed_keywords": ["broken home","family conflict","lack of harmony"]},
    {"id": "cups-page",  "name": "Page of Cups",    "suit": "cups",  "rank": "page",
     "upright_keywords": ["creative opportunities","curiosity","possibility"],
     "reversed_keywords": ["emotional immaturity","insecurity","disappointment"]},
    {"id": "cups-knight","name": "Knight of Cups",  "suit": "cups",  "rank": "knight",
     "upright_keywords": ["creativity","romance","charm","imagination"],
     "reversed_keywords": ["overactive imagination","unrealistic","jealousy"]},
    {"id": "cups-queen", "name": "Queen of Cups",   "suit": "cups",  "rank": "queen",
     "upright_keywords": ["compassionate","calm","intuitive","healer"],
     "reversed_keywords": ["inner feelings","self-care","co-dependency"]},
    {"id": "cups-king",  "name": "King of Cups",    "suit": "cups",  "rank": "king",
     "upright_keywords": ["emotionally balanced","compassionate","diplomatic"],
     "reversed_keywords": ["emotionally manipulative","moodiness","volatility"]},

    # ── Swords (14) ──────────────────────────────────────────────────────────
    {"id": "swords-ace",   "name": "Ace of Swords",    "suit": "swords", "rank": "ace",
     "upright_keywords": ["breakthrough","clarity","sharp mind"],
     "reversed_keywords": ["confusion","chaos","lack of clarity"]},
    {"id": "swords-02",    "name": "Two of Swords",    "suit": "swords", "rank": "02",
     "upright_keywords": ["difficult choices","indecision","stalemate"],
     "reversed_keywords": ["lesser of two evils","no right choice","confusion"]},
    {"id": "swords-03",    "name": "Three of Swords",  "suit": "swords", "rank": "03",
     "upright_keywords": ["heartbreak","emotional pain","sorrow","grief"],
     "reversed_keywords": ["recovery","forgiveness","moving on"]},
    {"id": "swords-04",    "name": "Four of Swords",   "suit": "swords", "rank": "04",
     "upright_keywords": ["rest","restoration","contemplation"],
     "reversed_keywords": ["exhaustion","burnout","deep contemplation"]},
    {"id": "swords-05",    "name": "Five of Swords",   "suit": "swords", "rank": "05",
     "upright_keywords": ["conflict","defeat","win at all costs"],
     "reversed_keywords": ["reconciliation","making amends","past resentment"]},
    {"id": "swords-06",    "name": "Six of Swords",    "suit": "swords", "rank": "06",
     "upright_keywords": ["transition","change","rite of passage"],
     "reversed_keywords": ["personal transition","resistance to change","running away"]},
    {"id": "swords-07",    "name": "Seven of Swords",  "suit": "swords", "rank": "07",
     "upright_keywords": ["deception","trickery","tactics","strategy"],
     "reversed_keywords": ["imposter syndrome","self-deceit","keeping secrets"]},
    {"id": "swords-08",    "name": "Eight of Swords",  "suit": "swords", "rank": "08",
     "upright_keywords": ["negative thinking","restriction","feeling trapped"],
     "reversed_keywords": ["self-limiting beliefs","inner critic","releasing"]},
    {"id": "swords-09",    "name": "Nine of Swords",   "suit": "swords", "rank": "09",
     "upright_keywords": ["anxiety","worry","fear","nightmares"],
     "reversed_keywords": ["inner turmoil","deep-seated fears","releasing worry"]},
    {"id": "swords-10",    "name": "Ten of Swords",    "suit": "swords", "rank": "10",
     "upright_keywords": ["painful endings","deep wounds","betrayal"],
     "reversed_keywords": ["recovery","regeneration","resisting an inevitable end"]},
    {"id": "swords-page",  "name": "Page of Swords",   "suit": "swords", "rank": "page",
     "upright_keywords": ["new ideas","curiosity","thirst for knowledge"],
     "reversed_keywords": ["all talk no action","haste","deception"]},
    {"id": "swords-knight","name": "Knight of Swords", "suit": "swords", "rank": "knight",
     "upright_keywords": ["action","impulsiveness","defending beliefs"],
     "reversed_keywords": ["no direction","disregard for consequences"]},
    {"id": "swords-queen", "name": "Queen of Swords",  "suit": "swords", "rank": "queen",
     "upright_keywords": ["independent","unbiased judgement","clear boundaries"],
     "reversed_keywords": ["cold-hearted","cruel","bitterness"]},
    {"id": "swords-king",  "name": "King of Swords",   "suit": "swords", "rank": "king",
     "upright_keywords": ["mental clarity","intellectual power","authority"],
     "reversed_keywords": ["manipulative","cruel","weakness"]},

    # ── Pentacles (14) ───────────────────────────────────────────────────────
    {"id": "pentacles-ace",   "name": "Ace of Pentacles",    "suit": "pentacles", "rank": "ace",
     "upright_keywords": ["opportunity","prosperity","new venture"],
     "reversed_keywords": ["lost opportunity","lack of planning","missed chance"]},
    {"id": "pentacles-02",    "name": "Two of Pentacles",    "suit": "pentacles", "rank": "02",
     "upright_keywords": ["multiple priorities","time management","adaptability"],
     "reversed_keywords": ["over-committed","disorganisation","reprioritisation"]},
    {"id": "pentacles-03",    "name": "Three of Pentacles",  "suit": "pentacles", "rank": "03",
     "upright_keywords": ["teamwork","collaboration","building"],
     "reversed_keywords": ["lack of teamwork","disorganised","group conflict"]},
    {"id": "pentacles-04",    "name": "Four of Pentacles",   "suit": "pentacles", "rank": "04",
     "upright_keywords": ["saving money","security","conservatism"],
     "reversed_keywords": ["over-spending","greed","materialism"]},
    {"id": "pentacles-05",    "name": "Five of Pentacles",   "suit": "pentacles", "rank": "05",
     "upright_keywords": ["financial loss","poverty","isolation"],
     "reversed_keywords": ["recovery from financial loss","spiritual poverty"]},
    {"id": "pentacles-06",    "name": "Six of Pentacles",    "suit": "pentacles", "rank": "06",
     "upright_keywords": ["giving","receiving","sharing","generosity"],
     "reversed_keywords": ["self-care","unpaid debts","one-sided charity"]},
    {"id": "pentacles-07",    "name": "Seven of Pentacles",  "suit": "pentacles", "rank": "07",
     "upright_keywords": ["long-term view","sustainable results","perseverance"],
     "reversed_keywords": ["lack of long-term vision","limited success"]},
    {"id": "pentacles-08",    "name": "Eight of Pentacles",  "suit": "pentacles", "rank": "08",
     "upright_keywords": ["apprenticeship","repetitive tasks","mastery"],
     "reversed_keywords": ["self-development","perfectionism","misdirected activity"]},
    {"id": "pentacles-09",    "name": "Nine of Pentacles",   "suit": "pentacles", "rank": "09",
     "upright_keywords": ["abundance","luxury","self-sufficiency"],
     "reversed_keywords": ["self-worth","over-investment in work","hustling"]},
    {"id": "pentacles-10",    "name": "Ten of Pentacles",    "suit": "pentacles", "rank": "10",
     "upright_keywords": ["wealth","financial security","family","long-term success"],
     "reversed_keywords": ["the dark side of wealth","financial failure","loss"]},
    {"id": "pentacles-page",  "name": "Page of Pentacles",   "suit": "pentacles", "rank": "page",
     "upright_keywords": ["ambition","desire","diligence","new beginning"],
     "reversed_keywords": ["lack of progress","procrastination","learn from failure"]},
    {"id": "pentacles-knight","name": "Knight of Pentacles", "suit": "pentacles", "rank": "knight",
     "upright_keywords": ["efficiency","routine","conservatism","methodical"],
     "reversed_keywords": ["self-discipline","boredom","feeling stuck"]},
    {"id": "pentacles-queen", "name": "Queen of Pentacles",  "suit": "pentacles", "rank": "queen",
     "upright_keywords": ["practical","homely","motherly","down-to-earth"],
     "reversed_keywords": ["financial independence","self-care","work-home conflict"]},
    {"id": "pentacles-king",  "name": "King of Pentacles",   "suit": "pentacles", "rank": "king",
     "upright_keywords": ["wealth","business","leadership","security","discipline"],
     "reversed_keywords": ["financially inept","obsessed with wealth","stubborn"]},
]

DEFAULT_SPREADS: list[TarotSpread] = [
    TarotSpread(spread_id="love-spread",     name="Love & Relationship Spread",  description="Explore the energies around your romantic connections.",        card_count=3, positions=["Past Influence","Current Energy","Future Potential"],  premium=True),
    TarotSpread(spread_id="career-spread",   name="Career & Purpose Spread",     description="Illuminate your professional path and life purpose.",           card_count=3, positions=["Your Strengths","Current Challenge","Opportunity Ahead"], premium=True),
    TarotSpread(spread_id="guidance-spread", name="Spiritual Guidance Spread",   description="Receive higher guidance on your spiritual journey.",            card_count=3, positions=["Soul Message","Lesson to Learn","Divine Guidance"],      premium=True),
]

XP_DAILY_DRAW   = 10
XP_SPREAD_DRAW  = 25
XP_BOOKMARK     = 5
XP_STREAK_BONUS = 15


def _resolve_user_email(request: Request, user_email: str | None = None, x_user_email: str | None = None) -> str:
    user = getattr(request.state, "user", None)
    if user:
        email = user.get("email")
        if email:
            return email
    if user_email:
        return user_email
    if x_user_email:
        return x_user_email
    raise HTTPException(status_code=401, detail="Authentication required.")


def _get_collection(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable.")
    return db[COLLECTION_NAME]


def _pick_card(exclude_ids: list[str] | None = None) -> dict:
    pool = [c for c in DEFAULT_CARDS if not exclude_ids or c["id"] not in exclude_ids]
    if not pool:
        pool = DEFAULT_CARDS
    card = random.choice(pool)
    orientation: Literal["upright", "reversed"] = random.choice(["upright", "reversed"])
    keywords = card["upright_keywords"] if orientation == "upright" else card["reversed_keywords"]
    return {
        "card_id": card["id"],
        "name": card["name"],
        "orientation": orientation,
        "meaning_snippet": ", ".join(keywords[:2]),
        "suit": card.get("suit", "major"),
        "rank": card.get("rank", ""),
    }


def _build_scenes(focus_area: FocusArea, card_name: str, orientation: str, question: str | None) -> list[TarotScene]:
    focus_map = {
        "guidance": ("The cosmic web stirs...", "A question hangs in the air between worlds."),
        "love":     ("The heart's compass spins...", "Love's mysteries await."),
        "career":   ("Ambition's flame flickers...", "Purpose seeks its vessel."),
        "healing":  ("Ancient waters still...", "Wounds seek the light."),
        "clarity":  ("The veil thins...", "Truth approaches."),
    }
    intro_text, ritual_text = focus_map.get(focus_area, focus_map["guidance"])
    q_text = f'Your question: "{question}"' if question else "You seek understanding."
    return [
        TarotScene(scene_id="s1", scene_type="intro",       title="The Reading Begins",   text=intro_text,                                        duration_ms=2500),
        TarotScene(scene_id="s2", scene_type="ritual",      title="Setting the Intention", text=f"{ritual_text} {q_text}",                        duration_ms=3000),
        TarotScene(scene_id="s3", scene_type="card_reveal", title=f"The Card Speaks",      text=f"{card_name} appears — {orientation}.",           duration_ms=3500),
        TarotScene(scene_id="s4", scene_type="guidance",    title="Your Guidance",         text=f"Reflect on what {card_name} reveals for you.",   duration_ms=3000),
        TarotScene(scene_id="s5", scene_type="closing",     title="The Reading Closes",    text="Carry this wisdom as you move through your day.", duration_ms=2000),
    ]


def _build_affirmation(card_name: str, orientation: str, focus_area: FocusArea) -> str:
    affirmations = {
        "guidance": f"I trust the wisdom of {card_name} to guide my path forward.",
        "love":     f"I open my heart to the lessons {card_name} offers.",
        "career":   f"I align my actions with the energy of {card_name}.",
        "healing":  f"I welcome the healing vibration of {card_name}.",
        "clarity":  f"I see clearly through the lens of {card_name}.",
    }
    return affirmations.get(focus_area, affirmations["guidance"])


def _build_reading_doc(
    user_email: str,
    card_data: dict,
    position_label: str,
    scenes: list[TarotScene],
    affirmation: str,
    focus_area: FocusArea,
    question: str | None,
    depth_level: DepthLevel,
    spread_type: str | None,
    xp_earned: int,
    extra_cards: list[dict] | None = None,
) -> dict:
    report_id = str(uuid4())
    cards = [
        TarotCard(
            card_id=card_data["card_id"], name=card_data["name"],
            position_code="card_1", position_label=position_label,
            orientation=card_data["orientation"],
            meaning_snippet=card_data["meaning_snippet"],
        ).model_dump()
    ]
    if extra_cards:
        for i, ec in enumerate(extra_cards, start=2):
            cards.append(TarotCard(
                card_id=ec["card_id"], name=ec["name"],
                position_code=f"card_{i}", position_label=ec.get("position_label", f"Card {i}"),
                orientation=ec["orientation"], meaning_snippet=ec["meaning_snippet"],
            ).model_dump())
    return {
        "id": str(uuid4()),
        "report_id": report_id,
        "doc_type": "report",
        "user_email": user_email,
        "focus_area": focus_area,
        "question": question,
        "depth_level": depth_level,
        "cards": cards,
        "scenes": [s.model_dump() for s in scenes],
        "affirmation": affirmation,
        "spread_type": spread_type,
        "xp_earned": xp_earned,
        "bookmarked": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


async def _compute_xp(collection, user_email: str, base_xp: int) -> int:
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    drew_yesterday = await collection.count_documents({
        "user_email": user_email, "doc_type": "report",
        "created_at": {"$gte": yesterday_start.isoformat(), "$lt": today_start.isoformat()},
    }) > 0
    return base_xp + (XP_STREAK_BONUS if drew_yesterday else 0)


@router.get("/daily/today")
async def get_daily_card_preview(request: Request, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    today = date.today().isoformat()
    existing = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "spread_type": None, "created_at": {"$gte": today}})
    if existing:
        existing.pop("_id", None)
        return {"already_drawn": True, "reading": existing}
    return {"already_drawn": False, "reading": None}


@router.post("/daily/draw")
async def draw_daily_card(request: Request, body: DailyDrawRequest, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    today = date.today().isoformat()
    existing = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "spread_type": None, "created_at": {"$gte": today}})
    if existing:
        existing.pop("_id", None)
        return {"reading": existing, "xp_earned": 0, "message": "Already drawn today."}
    card_data = _pick_card()
    scenes = _build_scenes(body.focus_area, card_data["name"], card_data["orientation"], body.question)
    affirmation = _build_affirmation(card_data["name"], card_data["orientation"], body.focus_area)
    xp = await _compute_xp(collection, resolved_email, XP_DAILY_DRAW)
    doc = _build_reading_doc(resolved_email, card_data, "Daily Draw", scenes, affirmation, body.focus_area, body.question, body.depth_level, None, xp)
    await collection.insert_one(doc)
    doc.pop("_id", None)
    return {"reading": doc, "xp_earned": xp, "message": f"+{xp} XP earned!"}


@router.get("/spreads")
async def list_spreads():
    return {"spreads": [s.model_dump() for s in DEFAULT_SPREADS]}


@router.post("/spread/generate")
async def generate_spread(request: Request, body: SpreadDrawRequest, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    spread = next((s for s in DEFAULT_SPREADS if s.spread_id == body.spread_id), None)
    if not spread:
        raise HTTPException(status_code=404, detail=f"Spread '{body.spread_id}' not found.")
    used_ids: list[str] = []
    cards_data = []
    for pos_label in spread.positions:
        c = _pick_card(exclude_ids=used_ids)
        used_ids.append(c["card_id"])
        c["position_label"] = pos_label
        cards_data.append(c)
    primary = cards_data[0]
    extra = cards_data[1:]
    scenes = _build_scenes(body.focus_area, primary["name"], primary["orientation"], body.question)
    affirmation = _build_affirmation(primary["name"], primary["orientation"], body.focus_area)
    xp = await _compute_xp(collection, resolved_email, XP_SPREAD_DRAW)
    doc = _build_reading_doc(resolved_email, primary, spread.positions[0], scenes, affirmation, body.focus_area, body.question, "detailed", body.spread_id, xp, extra_cards=extra)
    await collection.insert_one(doc)
    doc.pop("_id", None)
    return {"reading": doc, "spread": spread.model_dump(), "xp_earned": xp}


@router.get("/history")
async def get_reading_history(request: Request, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None), limit: int = Query(default=20, le=50)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    cursor = collection.find({"user_email": resolved_email, "doc_type": "report"}).sort("created_at", -1).limit(limit)
    docs = [doc async for doc in cursor]
    for doc in docs:
        doc.pop("_id", None)
    return {"history": docs, "count": len(docs)}


@router.post("/bookmark")
async def toggle_bookmark(request: Request, body: BookmarkRequest, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    result = await collection.update_one({"report_id": body.report_id, "user_email": resolved_email}, {"$set": {"bookmarked": body.bookmarked}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reading not found.")
    xp_delta = XP_BOOKMARK if body.bookmarked else 0
    return {"success": True, "bookmarked": body.bookmarked, "xp_earned": xp_delta}


@router.get("/bookmarks")
async def get_bookmarks(request: Request, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    cursor = collection.find({"user_email": resolved_email, "bookmarked": True, "doc_type": "report"}).sort("created_at", -1)
    docs = [doc async for doc in cursor]
    for doc in docs:
        doc.pop("_id", None)
    return {"bookmarks": docs, "count": len(docs)}


@router.post("/feedback")
async def submit_feedback(request: Request, body: FeedbackRequest, user_email: str | None = Query(default=None), x_user_email: str | None = Header(default=None)):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    doc = {
        "id": str(uuid4()), "report_id": body.report_id, "doc_type": "feedback",
        "user_email": resolved_email, "rating": body.rating, "comment": body.comment,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await collection.insert_one(doc)
    return {"success": True, "message": "Thank you for your feedback."}


def _build_reminder_doc(user_email: str, reminder_time: str, frequency: str, timezone_name: str, enabled: bool) -> dict[str, Any]:
    return {
        "id": str(uuid4()),
        "doc_type": "reminder",
        "user_email": user_email,
        "reminder_time": reminder_time,
        "frequency": frequency,
        "timezone": timezone_name,
        "enabled": enabled,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/reminder/set")
async def set_tarot_reminder(
    request: Request,
    reminder_time: str = Body(...),
    frequency: str = Body(default="daily"),
    timezone_name: str = Body(default="Asia/Kolkata", alias="timezone"),
    enabled: bool = Body(default=True),
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    existing = await collection.find_one({"user_email": resolved_email, "doc_type": "reminder"})
    if existing:
        await collection.update_one(
            {"id": existing["id"], "doc_type": "reminder"},
            {"$set": {
                "reminder_time": reminder_time,
                "frequency": frequency,
                "timezone": timezone_name,
                "enabled": enabled,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }},
        )
        return {"success": True, "message": "Reminder updated.", "reminder_time": reminder_time}
    doc = _build_reminder_doc(resolved_email, reminder_time, frequency, timezone_name, enabled)
    await collection.insert_one(doc)
    return {"success": True, "message": "Reminder set.", "reminder_time": reminder_time}


@router.get("/reminder")
async def get_tarot_reminder(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    doc = await collection.find_one({"user_email": resolved_email, "doc_type": "reminder"})
    if doc:
        doc.pop("_id", None)
    return {"reminder": doc}


@router.delete("/reminder")
async def delete_tarot_reminder(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
):
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    result = await collection.delete_many({"user_email": resolved_email, "doc_type": "reminder"})
    return {"success": True, "deleted_count": result.deleted_count}


# ── Tarot remediation pack v1 ─────────────────────────────────────────────────

def _normalize_reading_doc(doc: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(doc)
    if "story_scenes" in normalized and "scenes" not in normalized:
        normalized["scenes"] = normalized.pop("story_scenes")
    return normalized


def _fallback_period(user_email: str, theme: str, days: int, summary: str, recommendation: str, confidence: float) -> dict[str, Any]:
    now = datetime.now(timezone.utc).date()
    return {
        "id": str(uuid4()),
        "report_id": str(uuid4()),
        "type": theme,
        "window_label": f"Next {days} days",
        "confidence": confidence,
        "summary": summary,
        "recommendation": recommendation,
        "starts_on": now.isoformat(),
        "ends_on": (now + timedelta(days=days)).isoformat(),
        "user_email": user_email,
    }


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


@router.get("/reading/{report_id}")
async def get_tarot_reading(
    request: Request,
    report_id: str,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> dict[str, Any]:
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    doc = await collection.find_one({"user_email": resolved_email, "doc_type": "report", "report_id": report_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Reading not found")
    return _normalize_reading_doc(doc)


@router.get("/favorable-periods", response_model=FavorablePeriodsResponse)
async def get_favorable_periods(
    request: Request,
    user_email: str | None = Query(default=None),
    x_user_email: str | None = Header(default=None),
) -> FavorablePeriodsResponse:
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    docs = await collection.find(
        {"user_email": resolved_email, "doc_type": "lifecycle", "status": "active"}
    ).sort("created_at", -1).to_list(length=20)

    if not docs:
        docs = [
            _fallback_period(
                resolved_email,
                "love",
                45,
                "A favorable romantic phase may be drawing closer, with more emotional openness than usual.",
                "A deeper love spread can help you understand the shape of this opening.",
                0.78,
            ),
            _fallback_period(
                resolved_email,
                "guidance",
                21,
                "This is a good period for reflective choices, inner clarity, and gentle realignment.",
                "Use your daily ritual consistently to track how this energy develops.",
                0.69,
            ),
        ]

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
    resolved_email = _resolve_user_email(request, user_email, x_user_email)
    collection = _get_collection(request)
    latest_report = await collection.find_one(
        {"user_email": resolved_email, "doc_type": "report"},
        sort=[("created_at", -1)],
    )
    latest_theme = (latest_report or {}).get("focus_area") or "guidance"

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

    if latest_theme in {"guidance", "career"}:
        offers.append(
            PersonalizedOfferItem(
                id=str(uuid4()),
                offer_code="astro_tarot_upgrade",
                title="See the astrology behind your cards",
                description="Unlock richer Astro + Tarot interpretation for timing, clarity, and emotional movement.",
                target_theme=latest_theme,
                cta_label="Unlock",
                destination="/pricing",
                priority=95,
            )
        )

    offers.sort(key=lambda item: item.priority, reverse=True)
    return PersonalizedOffersResponse(offers=offers)
