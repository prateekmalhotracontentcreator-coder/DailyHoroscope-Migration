from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field

from palmistry_prompt_service import generate_hasta_rekha_report


router = APIRouter(prefix="/api/palmistry", tags=["palmistry"])

DERIVED_HAND_SHAPES = {"EARTH", "AIR", "FIRE", "WATER"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PalmistryAnswers(StrictModel):
    dominant_hand: str
    palm_shape: str
    finger_length: str
    life_line: str
    heart_line: str
    head_line: str
    fate_line: str
    dominant_mount: str
    thumb_type: str
    finger_style: str
    hand_texture: str
    special_marks: str


class PalmistryRemedies(StrictModel):
    gemstone: str
    mantra: str
    colour: str
    practice: str


class PalmistrySections(StrictModel):
    overview: str
    personality: str
    career_purpose: str
    love_relationships: str
    health_vitality: str
    wealth_prosperity: str
    spiritual_karmic: str
    remedies: PalmistryRemedies


class HastaRekhaReportDocument(StrictModel):
    id: str
    user_email: str
    user_name: str
    dominant_hand: str
    hand_shape: str
    answers: PalmistryAnswers
    report: PalmistrySections
    created_at: datetime


class PalmistryAnalyseRequest(StrictModel):
    user_email: str | None = ""
    user_name: str | None = ""
    dominant_hand: str
    palm_shape: str | None = None
    hand_shape: str | None = None
    life_line: str
    heart_line: str
    head_line: str
    fate_line: str
    dominant_mount: str
    thumb_type: str
    finger_length: str
    finger_style: str | None = None
    finger_appearance: str | None = None
    hand_texture: str
    special_marks: str | None = None
    scripture_mode: str | None = None


class PalmistryHistoryItem(StrictModel):
    id: str
    user_name: str
    dominant_hand: str
    hand_shape: str
    created_at: datetime
    overview: str


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _db(request: Request):
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available on request.app.state.db.")
    return db


def _collection(request: Request):
    return _db(request).palmistry_reports


def _normalize_email(value: str | None) -> str:
    return str(value or "").strip().lower()


def _clean_name(value: str | None) -> str:
    return str(value or "").strip()


def _resolve_user_email(request: Request, explicit_email: str | None = None, *, allow_missing: bool = False) -> str:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        return _normalize_email(str(state_user["email"]))
    email = _normalize_email(explicit_email)
    if email:
        return email
    if allow_missing:
        return ""
    raise HTTPException(status_code=401, detail="Authenticated user email or explicit user_email is required.")


def _resolve_user_name(request: Request, explicit_name: str | None = None) -> str:
    cleaned = _clean_name(explicit_name)
    if cleaned:
        return cleaned
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict):
        for key in ("name", "full_name", "given_name"):
            value = _clean_name(state_user.get(key))
            if value:
                return value
    return "Guest"


def _resolve_finger_style(payload: PalmistryAnalyseRequest) -> str:
    value = str(payload.finger_style or payload.finger_appearance or "").strip()
    if not value:
        raise HTTPException(status_code=422, detail="finger_style is required.")
    return value


def _resolve_special_marks(payload: PalmistryAnalyseRequest) -> str:
    return str(payload.special_marks or "None visible").strip() or "None visible"


def _resolve_palm_shape(payload: PalmistryAnalyseRequest) -> str:
    raw = str(payload.palm_shape or "").strip()
    if raw:
        return raw
    fallback = str(payload.hand_shape or "").strip()
    if fallback.lower() in {"square", "rectangular"}:
        return fallback
    return ""


def _derive_hand_shape(palm_shape: str, finger_length: str, supplied_hand_shape: str | None) -> str:
    normalized_supplied = str(supplied_hand_shape or "").strip().upper()
    if normalized_supplied in DERIVED_HAND_SHAPES:
        return normalized_supplied.title()

    palm = palm_shape.strip().lower()
    fingers = finger_length.strip().lower()
    if palm == "square" and fingers.startswith("short"):
        return "Earth"
    if palm == "square" and fingers.startswith("long"):
        return "Air"
    if palm == "rectangular" and fingers.startswith("short"):
        return "Fire"
    if palm == "rectangular" and fingers.startswith("long"):
        return "Water"
    raise HTTPException(status_code=422, detail="Unable to derive hand_shape from palm_shape and finger_length.")


def _coerce_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return _now()
    return _now()


def _first_sentence(text: str) -> str:
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""
    match = re.match(r"^.*?[.!?](?:\s|$)", cleaned)
    return (match.group(0).strip() if match else cleaned).strip()


def _serialize_document(document: dict[str, Any]) -> HastaRekhaReportDocument:
    return HastaRekhaReportDocument(
        id=str(document["id"]),
        user_email=str(document.get("user_email") or ""),
        user_name=str(document.get("user_name") or "Guest"),
        dominant_hand=str(document["dominant_hand"]),
        hand_shape=str(document["hand_shape"]),
        answers=PalmistryAnswers(**document["answers"]),
        report=PalmistrySections(**document["report"]),
        created_at=_coerce_datetime(document.get("created_at")),
    )


@router.post("/analyse", response_model=HastaRekhaReportDocument)
async def analyse_palmistry(payload: PalmistryAnalyseRequest, request: Request) -> HastaRekhaReportDocument:
    palm_shape = _resolve_palm_shape(payload)
    finger_style = _resolve_finger_style(payload)
    special_marks = _resolve_special_marks(payload)
    hand_shape = _derive_hand_shape(palm_shape, payload.finger_length, payload.hand_shape)
    user_email = _resolve_user_email(request, payload.user_email, allow_missing=True)
    user_name = _resolve_user_name(request, payload.user_name)

    answers = PalmistryAnswers(
        dominant_hand=payload.dominant_hand,
        palm_shape=palm_shape,
        finger_length=payload.finger_length,
        life_line=payload.life_line,
        heart_line=payload.heart_line,
        head_line=payload.head_line,
        fate_line=payload.fate_line,
        dominant_mount=payload.dominant_mount,
        thumb_type=payload.thumb_type,
        finger_style=finger_style,
        hand_texture=payload.hand_texture,
        special_marks=special_marks,
    )

    report = await generate_hasta_rekha_report(
        user_name=user_name,
        dominant_hand=answers.dominant_hand,
        palm_shape=answers.palm_shape,
        hand_shape=hand_shape,
        life_line=answers.life_line,
        heart_line=answers.heart_line,
        head_line=answers.head_line,
        fate_line=answers.fate_line,
        dominant_mount=answers.dominant_mount,
        thumb_type=answers.thumb_type,
        finger_length=answers.finger_length,
        finger_style=answers.finger_style,
        hand_texture=answers.hand_texture,
        special_marks=answers.special_marks,
        scripture_mode=payload.scripture_mode,
    )

    document = {
        "id": str(uuid4()),
        "user_email": user_email,
        "user_name": user_name,
        "dominant_hand": answers.dominant_hand,
        "hand_shape": hand_shape,
        "answers": answers.model_dump(),
        "report": report,
        "created_at": _now(),
    }

    if user_email:
        await _collection(request).insert_one(document)

    return _serialize_document(document)


@router.get("/reports", response_model=list[PalmistryHistoryItem])
async def list_palmistry_reports(request: Request, user_email: str | None = Query(default=None)) -> list[PalmistryHistoryItem]:
    resolved_email = _resolve_user_email(request, user_email)
    documents = await _collection(request).find({"user_email": resolved_email}).sort("created_at", -1).limit(10).to_list(length=10)
    items: list[PalmistryHistoryItem] = []
    for document in documents:
        items.append(
            PalmistryHistoryItem(
                id=str(document["id"]),
                user_name=str(document.get("user_name") or "Guest"),
                dominant_hand=str(document.get("dominant_hand") or ""),
                hand_shape=str(document.get("hand_shape") or ""),
                created_at=_coerce_datetime(document.get("created_at")),
                overview=_first_sentence(str((document.get("report") or {}).get("overview") or "")),
            )
        )
    return items


@router.get("/reports/{report_id}", response_model=HastaRekhaReportDocument)
async def get_palmistry_report(report_id: str, request: Request) -> HastaRekhaReportDocument:
    filters: dict[str, Any] = {"id": report_id}
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("email"):
        filters["user_email"] = _normalize_email(str(state_user["email"]))

    document = await _collection(request).find_one(filters)
    if document is None and "user_email" in filters:
        document = await _collection(request).find_one({"id": report_id})
    if document is None:
        raise HTTPException(status_code=404, detail="Palmistry report not found.")
    return _serialize_document(document)
