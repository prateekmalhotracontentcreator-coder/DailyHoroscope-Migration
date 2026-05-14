from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

# Dasha computation -- private helpers are stable; imported by name
try:
    from vedic_calculator import (  # type: ignore
        _parse_datetime_to_jd as _vc_jd,
        _calc_planet as _vc_planet,
        calculate_vimshottari_dasha,
        get_current_dasha,
    )
    import swisseph as _swe  # type: ignore
    _DASHA_ENGINE_OK = True
except Exception:
    _DASHA_ENGINE_OK = False

CLAUDE_MODEL = "claude-sonnet-4-6"


router = APIRouter(prefix="/api/oracle/krishna-prashnavali", tags=["krishna-oracle"])

COLLECTION_NAME = "scriptural_oracle_results"
ENGINE_VERSION = "krishna-oracle-v1"
GRID_SIZE = 18
TOTAL_CELLS = 324
JUMP_INTERVAL = 12
SEQUENCE_LENGTH = 9
CANONICAL_ANSWER_COUNT = 36

VerdictTraditional = Literal["Pratibha", "Pratrodha", "Dhairya", "Bhakti"]
VerdictBackend = Literal["SUCCESS", "WARNING", "PATIENCE", "SURRENDER"]
VerdictDisplay = Literal["YES", "NO", "WAIT", "PRAY"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BilingualBlock(StrictModel):
    sanskrit_block: str
    english_block: str


class AstrologyContext(StrictModel):
    current_mahadasha: str | None = None
    antardasha: str | None = None
    transit_planets: dict[str, Any] = Field(default_factory=dict)
    transit_house_map: dict[str, Any] = Field(default_factory=dict)
    yogas: list[str] = Field(default_factory=list)
    shadbala: dict[str, Any] = Field(default_factory=dict)
    biorhythm_bird: str | None = None
    bird_state: str | None = None


class KrishnaCanonicalAnswer(StrictModel):
    answer_id: str
    answer_slot: int = Field(ge=1, le=CANONICAL_ANSWER_COUNT)
    source_category: str
    verdict_traditional: VerdictTraditional
    verdict_backend: VerdictBackend
    verdict_display: VerdictDisplay
    chaupai_phrase: str | None = None
    title: BilingualBlock
    krishna_answer: BilingualBlock
    meaning: BilingualBlock
    what_to_do: BilingualBlock
    remedy: BilingualBlock | None = None          # v1 bundle only; None in v2
    precaution: BilingualBlock
    mantra: BilingualBlock | None = None          # v1 bundle only; None in v2
    duration: BilingualBlock
    krishna_message: BilingualBlock
    theme_tags: list[str] = Field(default_factory=list)
    source_ref: str | None = None
    content_status: str = "provisional_seed"
    behavioral_remedy: BilingualBlock | None = None   # v2 bundle: contemplative practice
    remedy_ref: str | None = None                     # v2 bundle: lookup key → krishna_prashnavali_remedies


class KrishnaSelectionRequest(StrictModel):
    row: int = Field(ge=0, le=GRID_SIZE - 1)
    col: int = Field(ge=0, le=GRID_SIZE - 1)
    question_text: str | None = None
    focus_area: str | None = None
    language_preference: Literal["en", "hi", "bilingual"] = "bilingual"
    reveal_mode: Literal["instant", "ritual"] = "instant"
    # Optional birth fields for live dasha computation
    date_of_birth: str | None = None
    time_of_birth: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone_offset: str = "+05:30"


class KrishnaShareRequest(StrictModel):
    report_id: str | None = None
    row: int | None = Field(default=None, ge=0, le=GRID_SIZE - 1)
    col: int | None = Field(default=None, ge=0, le=GRID_SIZE - 1)


class KrishnaHistoryItem(StrictModel):
    id: str
    report_id: str
    row: int
    col: int
    selected_index: int
    answer_id: str
    answer_slot: int
    verdict_display: VerdictDisplay
    question_text: str | None = None
    summary: str
    created_at: datetime


class KrishnaHistoryResponse(StrictModel):
    items: list[KrishnaHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    has_more: bool


class KrishnaMetadataResponse(StrictModel):
    engine_version: str
    grid_size: int
    total_cells: int
    jump_interval: int
    sequence_length: int
    canonical_answer_count: int
    grid_matrix: list[str]
    content_status: str
    mapping_status: str
    default_mapping_mode: str


class KrishnaReadingDocument(StrictModel):
    id: str
    report_id: str
    doc_type: str = "report"
    report_type: str = "krishna_prashnavali"
    oracle_family: str = "scriptural_oracle"
    oracle_mode: str = "krishna_prashnavali"
    user_email: str
    row: int
    col: int
    selected_index: int
    question_text: str | None = None
    focus_area: str | None = None
    language_preference: str = "bilingual"
    reveal_mode: str = "instant"
    sequence_indices: list[int]
    sequence_glyphs: list[str]
    chaupai_string: BilingualBlock
    answer_id: str
    answer_slot: int
    answer: KrishnaCanonicalAnswer
    astrology: AstrologyContext = Field(default_factory=AstrologyContext)
    summary_report: dict[str, BilingualBlock]
    meta: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class KrishnaReadingResponse(StrictModel):
    reading: KrishnaReadingDocument
    mapping_status: str
    content_status: str


class KrishnaShareResponse(StrictModel):
    report_id: str
    share_title: str
    share_text: str
    share_payload: dict[str, Any]


PROVISIONAL_GRID_MATRIX: list[str] = [
    "सु", "ध", "रे", "म", "स", "ब", "का", "ज", "वि", "चा", "र", "त", "स", "र", "ज", "ब", "म", "न",
    "रा", "म", "ल", "ख", "न", "क", "जु", "प", "स", "प", "न", "बि", "र", "च", "सि", "रि", "ब", "ठ",
    "सु", "न", "वि", "स", "वा", "स", "फ", "ल", "म", "न", "आ", "स", "क", "ल", "क", "ल्या", "ण", "सु",
    "ध", "र", "म", "म", "सु", "ख", "भा", "ष", "त", "ग", "त", "सु", "ख", "द", "स", "र", "व", "सि",
    "धि", "जा", "न", "हु", "सु", "फ", "ल", "म", "नो", "र", "थ", "पु", "रा", "न", "ध", "म", "म", "र",
    "ज", "ह", "म", "न", "रा", "म", "क", "रु", "पा", "स", "ब", "ल", "र", "त", "स", "ब", "क", "र",
    "स", "हि", "त", "सु", "ख", "स", "र", "व", "सि", "धि", "क", "म", "क", "र", "सु", "फ", "ल", "ज",
    "न", "न", "पु", "र", "वि", "ज", "य", "ध", "न", "ला", "भ", "स", "ब", "क", "र", "न", "सु", "फ",
    "ल", "स", "न", "दि", "व", "स", "सु", "ख", "द", "आ", "न", "न", "द", "म", "नो", "र", "थ", "सु",
    "फ", "ल", "व", "र", "ष", "अ", "च", "ल", "स", "र", "व", "सु", "ख", "ह", "रि", "भ", "क्ति", "सु",
    "फ", "ल", "ज", "न", "न", "सु", "ख", "भा", "ष", "त", "ग", "त", "सु", "ख", "द", "ज", "न", "न",
    "वि", "ज", "य", "ध", "न", "ला", "भ", "सु", "फ", "ल", "सु", "म", "ति", "सु", "ख", "र", "च", "अ",
    "ल", "क", "ल्या", "ण", "सु", "फ", "ल", "भ", "व", "न", "सु", "ख", "स", "र", "व", "क", "र", "म",
    "सु", "ध", "रे", "ज", "य", "स", "म", "प", "र", "क", "रि", "सु", "फ", "ल", "ज", "न", "न", "म",
    "नो", "र", "थ", "वि", "ज", "य", "ध", "न", "आ", "श", "सु", "फ", "ल", "ल", "र", "ष", "म", "ति",
    "सु", "ख", "द", "स", "र", "व", "क", "र", "म", "सु", "ध", "रे", "म", "स", "ब", "का", "ज", "क",
    "ल्या", "ण", "सु", "फ", "ल", "भ", "व", "न", "वि", "ज", "य", "सु", "ख", "द", "स", "र", "व", "म",
    "नो", "र", "थ", "वि", "ज", "य", "ध", "न", "आ", "म", "स", "ब", "का", "ज", "वि", "चा", "र", "त",
]


SOURCE_ANSWER_SEEDS: list[dict[str, str]] = [
    {"slot": "1", "category": "positive_success", "title_hi": "कार्य सिद्ध होगा", "title_en": "Work will be successful", "meaning_en": "The path is favorable and your task is likely to succeed."},
    {"slot": "2", "category": "positive_success", "title_hi": "मनोरथ पूर्ण होगा", "title_en": "Desire will be fulfilled", "meaning_en": "Your wish is moving toward completion."},
    {"slot": "3", "category": "positive_success", "title_hi": "लाभ होगा", "title_en": "Profit will occur", "meaning_en": "Gain is indicated in practical or personal terms."},
    {"slot": "4", "category": "positive_success", "title_hi": "विजय प्राप्त होगी", "title_en": "Victory will be achieved", "meaning_en": "You are favored in conflict, competition, or effort."},
    {"slot": "5", "category": "positive_success", "title_hi": "सुख की प्राप्ति", "title_en": "Attainment of happiness", "meaning_en": "Peace and relief are likely to follow."},
    {"slot": "6", "category": "positive_success", "title_hi": "मंगल कार्य होगा", "title_en": "An auspicious event will occur", "meaning_en": "The moment supports sacred or meaningful beginnings."},
    {"slot": "7", "category": "positive_success", "title_hi": "मन की इच्छा पूरी होगी", "title_en": "Heart's desire will be met", "meaning_en": "An inner longing is aligned with fulfillment."},
    {"slot": "8", "category": "positive_success", "title_hi": "शीघ्र कार्य होगा", "title_en": "Work will happen quickly", "meaning_en": "The matter is likely to move without major delay."},
    {"slot": "9", "category": "positive_success", "title_hi": "मित्र से सहायता मिलेगी", "title_en": "Help from a friend", "meaning_en": "Support arrives through goodwill, alliance, or collaboration."},
    {"slot": "10", "category": "positive_success", "title_hi": "ईश्वर की कृपा", "title_en": "God's grace", "meaning_en": "Divine support is strongly indicated in this matter."},
    {"slot": "11", "category": "mixed_uncertain", "title_hi": "कार्य में विलम्ब", "title_en": "Delay in work", "meaning_en": "The outcome may still come, but not at your preferred speed."},
    {"slot": "12", "category": "mixed_uncertain", "title_hi": "परिश्रम से सफलता", "title_en": "Success through hard work", "meaning_en": "Progress depends on sustained effort and discipline."},
    {"slot": "13", "category": "mixed_uncertain", "title_hi": "कुछ समय बाद फल", "title_en": "Fruit after some time", "meaning_en": "Results require patience before becoming visible."},
    {"slot": "14", "category": "mixed_uncertain", "title_hi": "सफलता में संदेह", "title_en": "Doubt in success", "meaning_en": "The matter remains unstable and not fully settled."},
    {"slot": "15", "category": "mixed_uncertain", "title_hi": "सोच-समझकर करें", "title_en": "Do with careful thought", "meaning_en": "Proceed carefully rather than impulsively."},
    {"slot": "16", "category": "mixed_uncertain", "title_hi": "बाधा आएगी", "title_en": "Obstacles will come", "meaning_en": "You may succeed, but only after clearing disruptions."},
    {"slot": "17", "category": "mixed_uncertain", "title_hi": "स्थान परिवर्तन", "title_en": "Change of place", "meaning_en": "Movement, travel, or a shift in environment may change the outcome."},
    {"slot": "18", "category": "mixed_uncertain", "title_hi": "सावधानी आवश्यक", "title_en": "Caution is necessary", "meaning_en": "Hidden risk is present, so restraint is wise."},
    {"slot": "19", "category": "warning_negative", "title_hi": "कार्य सिद्ध नहीं होगा", "title_en": "Work will not be successful", "meaning_en": "The current path is not favorable."},
    {"slot": "20", "category": "warning_negative", "title_hi": "हानि की संभावना", "title_en": "Possibility of loss", "meaning_en": "Loss or depletion is possible if you continue unchanged."},
    {"slot": "21", "category": "warning_negative", "title_hi": "शत्रु भय", "title_en": "Fear of enemies", "meaning_en": "Opposition, rivalry, or hidden resistance is active."},
    {"slot": "22", "category": "warning_negative", "title_hi": "चिंता बढ़ेगी", "title_en": "Anxiety will increase", "meaning_en": "This matter may intensify mental burden if pursued rashly."},
    {"slot": "23", "category": "warning_negative", "title_hi": "असफलता", "title_en": "Failure", "meaning_en": "This direction appears unlikely to bear fruit now."},
    {"slot": "24", "category": "warning_negative", "title_hi": "विवाद होगा", "title_en": "Dispute will occur", "meaning_en": "Conflict, argument, or legal strain may arise."},
    {"slot": "25", "category": "warning_negative", "title_hi": "कष्ट होगा", "title_en": "Trouble will occur", "meaning_en": "Difficulty or discomfort lies on the current path."},
    {"slot": "26", "category": "warning_negative", "title_hi": "व्यर्थ प्रयास", "title_en": "Vain effort", "meaning_en": "This effort may consume energy without meaningful result."},
    {"slot": "27", "category": "spiritual_conditional", "title_hi": "हनुमान जी की कृपा", "title_en": "Grace of Lord Hanuman", "meaning_en": "Devotion and sacred support can shift this matter."},
    {"slot": "28", "category": "spiritual_conditional", "title_hi": "दान-पुण्य करें", "title_en": "Perform charity", "meaning_en": "Selfless action can clear the present blockage."},
    {"slot": "29", "category": "spiritual_conditional", "title_hi": "धैर्य रखें", "title_en": "Keep patience", "meaning_en": "The time is not yet ripe; steadiness is needed."},
    {"slot": "30", "category": "spiritual_conditional", "title_hi": "सत्य की जीत", "title_en": "Truth will win", "meaning_en": "If your intent is righteous, truth will prevail."},
    {"slot": "31", "category": "spiritual_conditional", "title_hi": "अभिमान त्यागें", "title_en": "Leave pride", "meaning_en": "Humility is the condition for progress."},
    {"slot": "32", "category": "spiritual_conditional", "title_hi": "सत्संग से लाभ", "title_en": "Benefit through good company", "meaning_en": "Guidance from the wise will help you."},
    {"slot": "33", "category": "spiritual_conditional", "title_hi": "कुलदेवता का पूजन", "title_en": "Worship of family deity", "meaning_en": "A spiritual duty or lineage obligation may need honoring."},
    {"slot": "34", "category": "spiritual_conditional", "title_hi": "यात्रा सुखद", "title_en": "Pleasant journey", "meaning_en": "Travel or movement is supported."},
    {"slot": "35", "category": "spiritual_conditional", "title_hi": "शुभ समाचार", "title_en": "Good news", "meaning_en": "A favorable message or update is likely to arrive."},
    {"slot": "36", "category": "spiritual_conditional", "title_hi": "मन शांत रखें", "title_en": "Keep mind calm", "meaning_en": "Peace of mind is itself the doorway to the answer."},
]


def _db(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available on request.app.state.db.")
    return db


def _collection(request: Request):
    return getattr(_db(request), COLLECTION_NAME)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(value: str | None) -> str:
    return str(value or "").strip().lower()


def _resolve_user_email(request: Request) -> str:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return _normalize_email(str(state_user["email"]))
    direct_email = getattr(request.state, "user_email", None)
    if direct_email:
        return _normalize_email(str(direct_email))
    raise HTTPException(status_code=401, detail="Authenticated request state with user email is required.")


def _resolve_astrology_context(request: Request) -> AstrologyContext:
    payload = getattr(request.state, "astrology", None)
    if isinstance(payload, dict):
        try:
            return AstrologyContext(**payload)
        except Exception:
            return AstrologyContext(
                current_mahadasha=str(payload.get("current_mahadasha") or "") or None,
                antardasha=str(payload.get("antardasha") or "") or None,
                transit_planets=dict(payload.get("transit_planets") or {}),
                transit_house_map=dict(payload.get("transit_house_map") or {}),
                yogas=list(payload.get("yogas") or []),
                shadbala=dict(payload.get("shadbala") or {}),
                biorhythm_bird=str(payload.get("biorhythm_bird") or "") or None,
                bird_state=str(payload.get("bird_state") or "") or None,
            )
    return AstrologyContext()



async def _resolve_kp_remedy_doc(request: Request, remedy_ref: str) -> dict[str, Any] | None:
    """Fallback: fetch Engine remedy record when bundle fields are empty."""
    try:
        db = request.state.db
        col = db["krishna_prashnavali_remedies"]
        return await col.find_one({"remedy_id": remedy_ref, "approval_status": "approved"})
    except Exception:
        return None


def _source_bundle_path() -> Path:
    env_path = os.getenv("KRISHNA_ORACLE_BUNDLE_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return (Path(__file__).resolve().parent.parent / "assets" / "krishna_oracle" / "krishna_oracle_content.json").resolve()


def _verdict_triplet(category: str) -> tuple[VerdictTraditional, VerdictBackend, VerdictDisplay]:
    if category == "positive_success":
        return ("Pratibha", "SUCCESS", "YES")
    if category == "mixed_uncertain":
        return ("Dhairya", "PATIENCE", "WAIT")
    if category == "warning_negative":
        return ("Pratrodha", "WARNING", "NO")
    return ("Bhakti", "SURRENDER", "PRAY")


def _provisional_pair(sanskrit: str, english: str) -> BilingualBlock:
    return BilingualBlock(sanskrit_block=sanskrit, english_block=english)


def _build_provisional_answer(seed: dict[str, str]) -> KrishnaCanonicalAnswer:
    traditional, backend, display = _verdict_triplet(seed["category"])
    title_hi = seed["title_hi"]
    title_en = seed["title_en"]
    meaning_en = seed["meaning_en"]
    what_to_do_en = {
        "SUCCESS": "Move forward with steadiness and without ego in the result.",
        "PATIENCE": "Slow down, prepare well, and let timing mature.",
        "WARNING": "Avoid forcing this matter; reassess the path before acting.",
        "SURRENDER": "Turn inward, pray, and align your next step with humility.",
    }[backend]
    remedy_en = {
        "SUCCESS": "Offer gratitude before beginning and keep your motive clean.",
        "PATIENCE": "Practice stillness and wait for greater inner alignment.",
        "WARNING": "Pause, protect your energy, and seek wiser counsel.",
        "SURRENDER": "Use prayer, charity, or devotion to soften resistance.",
    }[backend]
    precaution_en = {
        "SUCCESS": "Do not become careless just because the path looks favorable.",
        "PATIENCE": "Do not mistake delay for denial.",
        "WARNING": "Do not push ahead in confusion or anger.",
        "SURRENDER": "Do not cling to control when the answer asks for faith.",
    }[backend]
    duration_en = {
        "SUCCESS": "Act in the current cycle with disciplined momentum.",
        "PATIENCE": "Allow more time before expecting visible results.",
        "WARNING": "Delay action until the situation materially changes.",
        "SURRENDER": "Let prayer and reflection lead before any outer move.",
    }[backend]
    message_en = {
        "SUCCESS": "Krishna supports sincere action when the heart is steady.",
        "PATIENCE": "Krishna asks for calm timing, not restless urgency.",
        "WARNING": "Krishna warns against effort that is misaligned or wasteful.",
        "SURRENDER": "Krishna reminds you that surrender can be higher than force.",
    }[backend]
    return KrishnaCanonicalAnswer(
        answer_id=f"KP36-{int(seed['slot']):02d}",
        answer_slot=int(seed["slot"]),
        source_category=seed["category"],
        verdict_traditional=traditional,
        verdict_backend=backend,
        verdict_display=display,
        title=_provisional_pair(title_hi, title_en),
        krishna_answer=_provisional_pair(title_hi, title_en),
        meaning=_provisional_pair(title_hi, meaning_en),
        what_to_do=_provisional_pair("शांत होकर धर्मानुसार कार्य करें।", what_to_do_en),
        remedy=_provisional_pair("भगवान का स्मरण कर श्रद्धा रखें।", remedy_en),
        precaution=_provisional_pair("अधीरता और भ्रम से बचें।", precaution_en),
        mantra=_provisional_pair("ॐ श्री कृष्णाय नमः", "Om Shri Krishnaya Namah"),
        duration=_provisional_pair("समय को परखकर आगे बढ़ें।", duration_en),
        krishna_message=_provisional_pair("श्रीकृष्ण कहते हैं: मन स्थिर रखो।", message_en),
        theme_tags=[seed["category"], backend.lower(), traditional.lower()],
        source_ref="Answer-Pack Source Confirmation",
        content_status="provisional_seed",
    )


def _default_answer_catalog() -> list[KrishnaCanonicalAnswer]:
    return [_build_provisional_answer(seed) for seed in SOURCE_ANSWER_SEEDS]


def _default_slot_for_cell(row: int, col: int) -> int:
    # Default implementation-safe import matrix.
    # Temple can replace this entirely by providing an explicit cell_answer_map in the content bundle.
    return ((row // 3) * 6) + (col // 3) + 1


def _load_bundle() -> dict[str, Any]:
    bundle_path = _source_bundle_path()
    if bundle_path.exists():
        with bundle_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        grid_matrix = list(payload.get("grid_matrix") or PROVISIONAL_GRID_MATRIX)
        answer_catalog = [KrishnaCanonicalAnswer(**item) for item in payload.get("answers", [])]
        cell_answer_map = payload.get("cell_answer_map") or {}
        if len(grid_matrix) != TOTAL_CELLS:
            raise HTTPException(status_code=500, detail="Krishna grid matrix must contain exactly 324 cells.")
        if not answer_catalog:
            answer_catalog = _default_answer_catalog()
        return {
            "grid_matrix": grid_matrix,
            "answers": answer_catalog,
            "cell_answer_map": {str(key): value for key, value in cell_answer_map.items()},
            "content_status": str(payload.get("content_status") or "temple_import"),
            "mapping_status": "temple_import" if cell_answer_map else "default_slot_matrix",
        }
    return {
        "grid_matrix": PROVISIONAL_GRID_MATRIX,
        "answers": _default_answer_catalog(),
        "cell_answer_map": {},
        "content_status": "provisional_seed",
        "mapping_status": "default_slot_matrix",
    }


def _selected_index(row: int, col: int) -> int:
    return (row * GRID_SIZE) + col


def _extract_indices(selected_index: int) -> list[int]:
    return [int((selected_index + (step * JUMP_INTERVAL)) % TOTAL_CELLS) for step in range(SEQUENCE_LENGTH)]


def _resolve_answer(selected_index: int, row: int, col: int, bundle: dict[str, Any]) -> KrishnaCanonicalAnswer:
    slot_value = bundle["cell_answer_map"].get(str(selected_index))
    if slot_value is None:
        slot_value = _default_slot_for_cell(row, col)
    answer_slot = int(slot_value)
    if answer_slot < 1 or answer_slot > CANONICAL_ANSWER_COUNT:
        raise HTTPException(status_code=500, detail=f"Answer slot out of range for selected index {selected_index}.")
    return bundle["answers"][answer_slot - 1]


def _chaupai_block(sequence_glyphs: list[str]) -> BilingualBlock:
    sanskrit = " ".join(sequence_glyphs)
    english = "12-step Krishna sequence preview"
    return BilingualBlock(sanskrit_block=sanskrit, english_block=english)


def _astrology_context_block(astrology: AstrologyContext, answer: KrishnaCanonicalAnswer) -> BilingualBlock | None:
    # Only surface astro context when there is real data -- suppress the block entirely
    # when no dasha/transit/yoga data is available so the UI doesn't show placeholder text.
    has_data = astrology.current_mahadasha or astrology.transit_house_map or astrology.yogas
    if not has_data:
        return None
    mahadasha = astrology.current_mahadasha
    transit_summary = ", ".join(sorted(astrology.transit_house_map.keys())) if astrology.transit_house_map else "no mapped transit houses"
    yogas = ", ".join(astrology.yogas) if astrology.yogas else "no declared yogas"
    english = (
        f"You are currently moving through {mahadasha}. "
        f"This answer is being read alongside {transit_summary} and {yogas}. "
        f"The Krishna verdict is {answer.verdict_display.lower()}, so the guidance should be read through timing, restraint, and dharmic action."
    )
    return BilingualBlock(
        sanskrit_block="ज्योतिष संदर्भ अनुरोध-स्थिति के अनुसार जोड़ा गया है।",
        english_block=english,
    )


def _dasha_astrology_from_birth(
    date_of_birth: str,
    time_of_birth: str,
    timezone_offset: str,
) -> AstrologyContext | None:
    """Compute current Mahadasha/Antardasha from birth details using Swiss Ephemeris."""
    if not _DASHA_ENGINE_OK:
        return None
    try:
        jd = _vc_jd(date_of_birth, time_of_birth, timezone_offset)
        moon_lon, _ = _vc_planet(jd, _swe.MOON)
        dashas = calculate_vimshottari_dasha(date_of_birth, moon_lon)
        current = get_current_dasha(dashas)
        if not current:
            return None
        maha = current.get("planet") or current.get("maha_dasha", {}).get("planet", "")
        antar = (
            current.get("antardasha_planet")
            or current.get("antar_dasha", {}).get("planet", "")
        )
        mahadasha_label = f"{maha} Mahadasha" if maha else None
        antardasha_label = f"{antar} Antardasha" if antar else None
        return AstrologyContext(
            current_mahadasha=mahadasha_label,
            antardasha=antardasha_label,
        )
    except Exception:
        return None


async def _claude_enrich_summary(
    question_text: str | None,
    focus_area: str | None,
    verdict: str,
    answer: KrishnaCanonicalAnswer,
    astrology: AstrologyContext,
) -> dict[str, str] | None:
    """Call Claude to generate full-length personalised question_response and practical_action."""
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    question = (question_text or "").strip() or "a general life question"
    focus = (focus_area or "guidance").replace("_", " ")
    dasha_context = ""
    if astrology.current_mahadasha:
        dasha_context = f"The seeker is currently in {astrology.current_mahadasha}"
        if astrology.antardasha:
            dasha_context += f" / {astrology.antardasha}"
        dasha_context += ". "

    prompt = f"""You are interpreting a sacred Krishna Prashnavali oracle reading. Your tone is wise, warm, and grounded in Vedic tradition -- never generic or vague.

ORACLE DATA:
- Seeker's question: "{question}"
- Focus area: {focus}
- Krishna's verdict: {verdict} ({answer.verdict_traditional})
- Krishna's answer: {answer.krishna_answer.english_block}
- Meaning: {answer.meaning.english_block}
- What to do: {answer.what_to_do.english_block}
- Precaution: {answer.precaution.english_block}
- Duration: {answer.duration.english_block}
- Sacred message: {answer.krishna_message.english_block}
- {dasha_context}

Generate two sections. Return ONLY valid JSON with these two keys:

"question_response": A 4-5 sentence personalised response to the seeker's specific question.
  - Address the question directly by name at the start
  - Explain what this specific verdict (not generic oracle language) means for their situation
  - Bring in the meaning and Krishna's message with context
  - Close with one clear orienting insight for their next step

"practical_action": 4-6 concrete, actionable steps structured as a short paragraph per step.
  - Each step must be specific and grounded in the oracle's guidance (what_to_do, precaution, duration)
  - Include timing where relevant
  - Step 1 should be immediate (today/this week), later steps should extend over the duration
  - Do not repeat the verdict word -- embody its meaning through the actions

Return ONLY the JSON object, no markdown fences."""

    try:
        client = AsyncAnthropic(api_key=api_key)
        response = await client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1200,
            temperature=0.4,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )
        text = ""
        for block in response.content:
            if hasattr(block, "text"):
                text = block.text.strip()
                break
        if not text:
            return None
        # Strip markdown fences if present
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(text)
        return {
            "question_response": str(parsed.get("question_response", "")),
            "practical_action": str(parsed.get("practical_action", "")),
        }
    except Exception:
        return None


def _practical_action_block(
    answer: KrishnaCanonicalAnswer,
    ritual_remedy_doc: dict[str, Any] | None = None,
) -> BilingualBlock:
    # Bundle first (v1: answer.remedy; v2: None) -- Engine fallback when bundle remedy absent
    remedy_en = answer.remedy.english_block if answer.remedy else ""
    remedy_hi = answer.remedy.sanskrit_block if answer.remedy else ""
    if not remedy_en and ritual_remedy_doc:
        ritual = ritual_remedy_doc.get("ritual_remedy") or {}
        remedy_en = ritual.get("english_block", "")
        remedy_hi = ritual.get("sanskrit_block", "")
    return BilingualBlock(
        sanskrit_block=f"{answer.what_to_do.sanskrit_block} {remedy_hi}".strip(),
        english_block=f"{answer.what_to_do.english_block} {remedy_en}".strip(),
    )


def _question_response_block(
    answer: KrishnaCanonicalAnswer,
    question_text: str | None,
    focus_area: str | None,
) -> BilingualBlock:
    cleaned_question = (question_text or "").strip()
    focus_label = (focus_area or "guidance").replace("_", " ").strip() or "guidance"
    if not cleaned_question:
        return BilingualBlock(
            sanskrit_block="यदि प्रश्न स्पष्ट न हो तो इस उत्तर को सामान्य कृष्ण-मार्गदर्शन की तरह ग्रहण करें।",
            english_block=(
                f"No specific question was provided, so this reading should be taken as general Krishna guidance "
                f"for your current {focus_label} path."
            ),
        )

    return BilingualBlock(
        sanskrit_block=(
            f"आपके प्रश्न \"{cleaned_question}\" के संदर्भ में कृष्ण का संकेत यह है: "
            f"{answer.krishna_answer.sanskrit_block} {answer.meaning.sanskrit_block}"
        ),
        english_block=(
            f"For your question, \"{cleaned_question},\" Krishna's answer is {answer.verdict_display}: "
            f"{answer.krishna_answer.english_block} In this {focus_label} matter, "
            f"{answer.meaning.english_block}"
        ),
    )


async def _summary_report(
    answer: KrishnaCanonicalAnswer,
    astrology: AstrologyContext,
    question_text: str | None,
    focus_area: str | None,
    ritual_remedy_doc: dict[str, Any] | None = None,
) -> dict[str, BilingualBlock | None]:
    q_response = _question_response_block(answer, question_text, focus_area)
    p_action = _practical_action_block(answer, ritual_remedy_doc)

    # Claude enrichment: generates full-length personalised text for both blocks
    enriched = await _claude_enrich_summary(question_text, focus_area, answer.verdict_display, answer, astrology)
    if enriched:
        if enriched.get("question_response"):
            q_response = BilingualBlock(
                sanskrit_block=q_response.sanskrit_block,
                english_block=enriched["question_response"],
            )
        if enriched.get("practical_action"):
            p_action = BilingualBlock(
                sanskrit_block=p_action.sanskrit_block,
                english_block=enriched["practical_action"],
            )

    report: dict[str, BilingualBlock | None] = {
        "sacred_verse": answer.krishna_answer,
        "question_response": q_response,
        "astro_scientific_context": _astrology_context_block(astrology, answer),
        "practical_action": p_action,
    }
    # behavioral_remedy: bundle (v2) first → Engine fallback
    if answer.behavioral_remedy and answer.behavioral_remedy.english_block:
        report["behavioral_remedy"] = answer.behavioral_remedy
    elif ritual_remedy_doc:
        ritual = ritual_remedy_doc.get("ritual_remedy") or {}
        if ritual.get("english_block"):
            report["behavioral_remedy"] = BilingualBlock(
                sanskrit_block=ritual.get("sanskrit_block", ""),
                english_block=ritual.get("english_block", ""),
            )
    # sacred_mantra: bundle (v1) first → Engine fallback
    if answer.mantra and answer.mantra.english_block:
        report["sacred_mantra"] = answer.mantra
    elif ritual_remedy_doc:
        mantra = ritual_remedy_doc.get("mantra") or {}
        if mantra.get("english_block"):
            report["sacred_mantra"] = BilingualBlock(
                sanskrit_block=mantra.get("sanskrit_block", ""),
                english_block=mantra.get("english_block", ""),
            )
    return {k: v for k, v in report.items() if v is not None}


def _serialize_history_item(document: dict[str, Any]) -> KrishnaHistoryItem:
    answer = document.get("answer") or {}
    title = answer.get("title") or {}
    summary = title.get("english_block") or answer.get("verdict_display") or "Krishna guidance"
    return KrishnaHistoryItem(
        id=str(document.get("id") or document.get("_id") or ""),
        report_id=str(document.get("report_id") or ""),
        row=int(document.get("row") or 0),
        col=int(document.get("col") or 0),
        selected_index=int(document.get("selected_index") or 0),
        answer_id=str(document.get("answer_id") or ""),
        answer_slot=int(document.get("answer_slot") or 1),
        verdict_display=str(answer.get("verdict_display") or "WAIT"),
        question_text=document.get("question_text"),
        summary=summary,
        created_at=document.get("created_at") or _now(),
    )


async def _fetch_report(request: Request, report_id: str) -> dict[str, Any]:
    user_email = _resolve_user_email(request)
    collection = _collection(request)
    document = await collection.find_one(
        {
            "user_email": user_email,
            "doc_type": "report",
            "oracle_mode": "krishna_prashnavali",
            "report_id": report_id,
        }
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Krishna oracle report not found.")
    return document


@router.get("/meta", response_model=KrishnaMetadataResponse)
async def get_krishna_oracle_metadata() -> KrishnaMetadataResponse:
    bundle = _load_bundle()
    return KrishnaMetadataResponse(
        engine_version=ENGINE_VERSION,
        grid_size=GRID_SIZE,
        total_cells=TOTAL_CELLS,
        jump_interval=JUMP_INTERVAL,
        sequence_length=SEQUENCE_LENGTH,
        canonical_answer_count=CANONICAL_ANSWER_COUNT,
        grid_matrix=bundle["grid_matrix"],
        content_status=bundle["content_status"],
        mapping_status=bundle["mapping_status"],
        default_mapping_mode="3x3_slot_matrix",
    )


@router.post("/select", response_model=KrishnaReadingResponse)
async def select_krishna_cell(payload: KrishnaSelectionRequest, request: Request) -> KrishnaReadingResponse:
    # Anonymous-safe: resolve email if authenticated; skip DB write if not.
    # Logged-out users receive a full reading; it is not persisted.
    try:
        user_email = _resolve_user_email(request)
        is_authenticated = True
    except HTTPException:
        user_email = "anonymous"
        is_authenticated = False

    # Resolve astrology: payload birth fields take priority over middleware context
    astrology = _resolve_astrology_context(request)
    if payload.date_of_birth and payload.time_of_birth:
        computed = _dasha_astrology_from_birth(
            payload.date_of_birth, payload.time_of_birth, payload.timezone_offset
        )
        if computed:
            astrology = computed

    bundle = _load_bundle()
    selected_index = _selected_index(payload.row, payload.col)
    sequence_indices = _extract_indices(selected_index)
    sequence_glyphs = [bundle["grid_matrix"][index] for index in sequence_indices]
    answer = _resolve_answer(selected_index, payload.row, payload.col, bundle)

    # Engine fallback: only called when bundle behavioral_remedy is absent AND remedy_ref exists
    ritual_remedy_doc: dict[str, Any] | None = None
    bundle_remedy_missing = not (answer.behavioral_remedy and answer.behavioral_remedy.english_block)
    if bundle_remedy_missing and answer.remedy_ref:
        ritual_remedy_doc = await _resolve_kp_remedy_doc(request, answer.remedy_ref)

    now = _now()
    report = KrishnaReadingDocument(
        id=str(uuid4()),
        report_id=f"krishna-{uuid4()}",
        user_email=user_email,
        row=payload.row,
        col=payload.col,
        selected_index=selected_index,
        question_text=payload.question_text,
        focus_area=payload.focus_area,
        language_preference=payload.language_preference,
        reveal_mode=payload.reveal_mode,
        sequence_indices=sequence_indices,
        sequence_glyphs=sequence_glyphs,
        chaupai_string=_chaupai_block(sequence_glyphs),
        answer_id=answer.answer_id,
        answer_slot=answer.answer_slot,
        answer=answer,
        astrology=astrology,
        summary_report=await _summary_report(answer, astrology, payload.question_text, payload.focus_area, ritual_remedy_doc),
        meta={
            "engine_version": ENGINE_VERSION,
            "jump_interval": JUMP_INTERVAL,
            "sequence_length": SEQUENCE_LENGTH,
            "content_status": bundle["content_status"],
            "mapping_status": bundle["mapping_status"],
            "persisted": is_authenticated,
        },
        created_at=now,
        updated_at=now,
    )
    # Only write to DB for authenticated sessions
    if is_authenticated:
        await _collection(request).insert_one(report.model_dump(mode="python"))
    return KrishnaReadingResponse(
        reading=report,
        mapping_status=bundle["mapping_status"],
        content_status=bundle["content_status"],
    )


@router.get("/history", response_model=KrishnaHistoryResponse)
async def get_krishna_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=12, ge=1, le=50),
) -> KrishnaHistoryResponse:
    # Graceful degradation for unauthenticated users -- matches Tarot pattern
    try:
        user_email = _resolve_user_email(request)
    except HTTPException:
        return KrishnaHistoryResponse(items=[], page=page, limit=limit, total=0, has_more=False)
    query = {
        "user_email": user_email,
        "doc_type": "report",
        "oracle_mode": "krishna_prashnavali",
    }
    skip = (page - 1) * limit
    collection = _collection(request)
    total = await collection.count_documents(query)
    documents = await collection.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
    return KrishnaHistoryResponse(
        items=[_serialize_history_item(document) for document in documents],
        page=page,
        limit=limit,
        total=total,
        has_more=(skip + len(documents)) < total,
    )


@router.get("/reports/{report_id}", response_model=KrishnaReadingDocument)
async def get_krishna_report(report_id: str, request: Request) -> KrishnaReadingDocument:
    document = await _fetch_report(request, report_id)
    return KrishnaReadingDocument.model_validate(document)


@router.post("/share", response_model=KrishnaShareResponse)
async def generate_krishna_share(payload: KrishnaShareRequest, request: Request) -> KrishnaShareResponse:
    if payload.report_id:
        document = await _fetch_report(request, payload.report_id)
        report = KrishnaReadingDocument.model_validate(document)
    else:
        if payload.row is None or payload.col is None:
            raise HTTPException(status_code=400, detail="Provide report_id or both row and col for share generation.")
        preview = await select_krishna_cell(
            KrishnaSelectionRequest(row=payload.row, col=payload.col, reveal_mode="instant"),
            request,
        )
        report = preview.reading
    share_title = f"Krishna Oracle • {report.answer.title.english_block}"
    share_text = (
        f"{report.answer.krishna_answer.english_block}\n"
        f"{report.answer.meaning.english_block}\n"
        f"Verdict: {report.answer.verdict_display}"
    )
    return KrishnaShareResponse(
        report_id=report.report_id,
        share_title=share_title,
        share_text=share_text,
        share_payload={
            "report_id": report.report_id,
            "answer_id": report.answer_id,
            "answer_slot": report.answer_slot,
            "verdict": report.answer.verdict_display,
            "krishna_answer": report.answer.krishna_answer.model_dump(),
            "chaupai_string": report.chaupai_string.model_dump(),
        },
    )
