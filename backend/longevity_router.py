from __future__ import annotations

import asyncio
import importlib
import inspect
import json
import os
import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from knowledge_engine import register_arc_angel_report_run

try:
    from backend.kp_engine import MEDICAL_DISCLAIMER, ReportInput, compute_longevity_report
except ImportError:  # pragma: no cover
    from kp_engine import MEDICAL_DISCLAIMER, ReportInput, compute_longevity_report  # type: ignore


router = APIRouter(prefix="/api/longevity", tags=["longevity"])

CLAUDE_MODEL = "claude-sonnet-4-6"
COLLECTION_NAME = "longevity_reports"
REPORT_TYPE = "longevity_health"
REPORT_SLUG = "longevity"
_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PricingPlan(StrictModel):
    code: str
    label: str
    price_inr: int


class AccessStatus(StrictModel):
    entitled: bool
    preview_allowed: bool
    reason: str
    pricing: list[PricingPlan] = Field(default_factory=list)
    medical_disclaimer: str


class LongevityGenerateRequest(StrictModel):
    user_email: str | None = None
    place_label: str | None = None
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    reference_date: str | None = None
    preview: bool = False


class LongevityReportDocument(StrictModel):
    id: str
    document_type: str
    report_type: str
    report_slug: str
    user_email: str
    access_mode: str
    created_at: datetime
    updated_at: datetime
    summary: str
    input_payload: dict[str, Any]
    output_payload: dict[str, Any]


class LongevityGenerateResponse(StrictModel):
    report: LongevityReportDocument
    access: AccessStatus


class LongevitySaveRequest(StrictModel):
    report: LongevityReportDocument | None = None
    report_id: str | None = None


class LongevityHistoryItem(StrictModel):
    id: str
    summary: str
    created_at: datetime
    classification: str
    quality_band: str


class LongevityHistoryResponse(StrictModel):
    items: list[LongevityHistoryItem] = Field(default_factory=list)
    page: int
    limit: int
    has_more: bool


class LongevityAlertsItem(StrictModel):
    type: str
    severity: str
    date: str
    detail: str
    support: str


class LongevityAlertsResponse(StrictModel):
    items: list[LongevityAlertsItem] = Field(default_factory=list)
    source_report_id: str | None = None
    generated_for_date: str | None = None


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


def _resolve_user(request: Request) -> dict[str, Any]:
    state_user = getattr(request.state, "user", None)
    return state_user if isinstance(state_user, dict) else {}


def _resolve_user_email(request: Request, explicit_email: str | None = None, *, allow_missing: bool = False) -> str:
    state_user = _resolve_user(request)
    if state_user.get("email"):
        return _normalize_email(str(state_user["email"]))
    email = _normalize_email(explicit_email)
    if email:
        return email
    if allow_missing:
        return ""
    raise HTTPException(status_code=401, detail="Authenticated user email or explicit user_email is required.")


def _entitlement_from_user(user: dict[str, Any]) -> bool:
    if not user:
        return False
    role = str(user.get("role") or "").strip().lower()
    if role in {"admin", "owner"}:
        return True
    truthy_keys = {
        "is_pro",
        "is_premium",
        "premium",
        "has_longevity_access",
        "longevity_unlocked",
        "premium_reports_enabled",
    }
    if any(bool(user.get(key)) for key in truthy_keys):
        return True
    for key in ("plan", "tier", "subscription_plan", "subscription_tier", "membership"):
        value = str(user.get(key) or "").strip().lower()
        if value in {"pro", "premium", "gold", "paid"}:
            return True
    return False


def _access_status(request: Request) -> AccessStatus:
    user = _resolve_user(request)
    entitled = _entitlement_from_user(user)
    reason = "Longevity premium is unlocked on this account." if entitled else "This module is gated to Pro members or one-time purchasers."
    return AccessStatus(
        entitled=entitled,
        preview_allowed=True,
        reason=reason,
        pricing=[
            PricingPlan(code="pro_monthly", label="Pro Monthly", price_inr=499),
            PricingPlan(code="longevity_one_time", label="One-Time Unlock", price_inr=999),
        ],
        medical_disclaimer=MEDICAL_DISCLAIMER,
    )


def _clean_json_text(text: str) -> str:
    stripped = text.strip()
    stripped = _CODE_FENCE_PATTERN.sub("", stripped)
    return stripped.strip()


def _extract_text_from_claude_response(response: Any) -> str | None:
    content = getattr(response, "content", None)
    if not content:
        return None
    text_parts: list[str] = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    return "\n".join(text_parts).strip() if text_parts else None


async def _anthropic_client():
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return AsyncAnthropic(api_key=api_key)


async def _call_claude_json(prompt: str, *, max_tokens: int = 1800, temperature: float = 0.35, timeout_secs: float = 12.0) -> dict[str, Any] | None:
    client = await _anthropic_client()
    if client is None:
        return None
    try:
        response = await asyncio.wait_for(
            client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            ),
            timeout=timeout_secs,
        )
    except BaseException:
        # Catches asyncio.CancelledError, asyncio.TimeoutError, and all network errors.
        # Always fall through to deterministic fallback -- never let narrative generation
        # kill the report.
        return None
    text = _extract_text_from_claude_response(response)
    if not text:
        return None
    try:
        return json.loads(_clean_json_text(text))
    except Exception:
        return None


async def _try_scan_chart(payload: LongevityGenerateRequest) -> dict[str, Any] | None:
    # KE rules layer (interpretation_rules) is NOT wired here.
    # Zero `approved` rules in production -- only `approved` rules may reach live users.
    # The Longevity Report runs entirely on kp_engine.py (computational engine).
    # Re-enable scan_chart() only after TT approves health-category KE rules.
    return None
    candidates = (  # noqa: unreachable
        "backend.knowledge_engine",
        "knowledge_engine",
        "backend.scan_chart",
        "scan_chart",
    )
    for module_name in candidates:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        scan_chart = getattr(module, "scan_chart", None)
        if not callable(scan_chart):
            continue
        kwargs = {
            "categories": ["health"],
            "date_of_birth": payload.date_of_birth,
            "time_of_birth": payload.time_of_birth,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "timezone": payload.timezone,
            "place_label": payload.place_label,
        }
        attempts = (
            lambda: scan_chart(**kwargs),
            lambda: scan_chart(kwargs),
            lambda: scan_chart(categories=["health"]),
        )
        for attempt in attempts:
            try:
                result = attempt()
                if inspect.isawaitable(result):
                    result = await asyncio.wait_for(result, timeout=8.0)
                if result is not None:
                    return {"source_module": module_name, "result": result}
            except TypeError:
                continue
            except BaseException:
                # Catches asyncio.TimeoutError, CancelledError, and scan errors.
                # KE scan is best-effort -- never block report generation.
                break
    return None


def _fallback_narrative(output_payload: dict[str, Any], knowledge_context: dict[str, Any] | None) -> dict[str, Any]:
    longevity = output_payload["longevity_classification"]
    prakriti = output_payload["constitutional_health_profile"]
    windows = output_payload["disease_susceptibility_windows"]
    first_window = windows[0] if windows else None
    knowledge_items = []
    if isinstance(knowledge_context, dict):
        result = knowledge_context.get("result")
        if isinstance(result, dict):
            for key in ("summary", "health_summary", "insights"):
                value = result.get(key)
                if isinstance(value, str) and value.strip():
                    knowledge_items.append(value.strip())
                elif isinstance(value, list):
                    knowledge_items.extend(str(item).strip() for item in value if str(item).strip())
    executive_summary = (
        f"{longevity['label']} longevity signatures dominate this chart. The constitutional profile is {prakriti['primary_prakriti']}-first, "
        f"so health protection improves when the lifestyle matches that doshic load instead of relying on brute stamina."
    )
    timing_summary = (
        f"The current timing runs through {output_payload['current_dasha']['maha_dasha']['planet']} / "
        f"{output_payload['current_dasha']['antar_dasha']['planet']}."
    )
    if first_window:
        timing_summary += f" The next major watch window runs from {first_window['start_date']} to {first_window['end_date']}."
    return {
        "executive_summary": executive_summary,
        "constitution_narrative": prakriti["summary"],
        "timing_narrative": timing_summary,
        "prevention_narrative": output_payload["remedial_guidance"]["body_focus"],
        "knowledge_engine_notes": knowledge_items[:4],
        "full_report_markdown": _report_summary_markdown(output_payload),
    }


def _slim_payload_for_prompt(output_payload: dict[str, Any]) -> dict[str, Any]:
    """Return a trimmed payload for the Claude prompt -- omits raw longitudes and
    degree-level data that inflate the prompt without adding narrative value."""
    snap = output_payload.get("birth_snapshot") or {}
    planets_slim = {
        p: {"sign": v.get("sign"), "house": v.get("whole_sign_house"), "retrograde": v.get("retrograde"),
            "nakshatra": (v.get("kp") or {}).get("nakshatra")}
        for p, v in (snap.get("planets") or {}).items()
    }
    return {
        "summary": output_payload.get("summary"),
        "ayanamsha": snap.get("ayanamsha"),
        "ascendant": (snap.get("angles") or {}).get("ascendant_sign"),
        "planets": planets_slim,
        "current_dasha": output_payload.get("current_dasha"),
        "longevity_classification": output_payload.get("longevity_classification"),
        "constitutional_health_profile": output_payload.get("constitutional_health_profile"),
        "vulnerable_systems": output_payload.get("vulnerable_systems"),
        "disease_susceptibility_windows": output_payload.get("disease_susceptibility_windows"),
        "critical_period_alerts": output_payload.get("critical_period_alerts"),
        "remedial_guidance": output_payload.get("remedial_guidance"),
    }


def _narrative_prompt(output_payload: dict[str, Any], knowledge_context: dict[str, Any] | None) -> str:
    knowledge_json = json.dumps(knowledge_context or {}, ensure_ascii=True)
    report_json = json.dumps(_slim_payload_for_prompt(output_payload), ensure_ascii=True)
    return f"""
You are writing a premium Ayur Jyotish Longevity & Health narrative for Everyday Horoscope.

Rules:
- The deterministic KP and Vedic calculations are already complete. Do not change classifications, dates, scores, houses, or dashas.
- Keep the tone professional, spiritual, calm, and medically responsible.
- Never claim diagnosis, cure, or certainty of death.
- Reinforce the disclaimer spirit without sounding alarming.
- Work with KP as the primary interpretive lens and Vedic support as the secondary layer.
- If Knowledge Engine notes are present, weave them in lightly as grounded support, not as citations.
- Return valid JSON only.

Output keys:
- executive_summary
- constitution_narrative
- timing_narrative
- prevention_narrative
- knowledge_engine_notes
- full_report_markdown

Knowledge engine context:
{knowledge_json}

Deterministic report payload:
{report_json}
""".strip()


def _apply_narrative(output_payload: dict[str, Any], narrative: dict[str, Any], knowledge_context: dict[str, Any] | None) -> dict[str, Any]:
    payload = dict(output_payload)
    payload["narrative"] = {
        "executive_summary": str(narrative.get("executive_summary") or ""),
        "constitution_narrative": str(narrative.get("constitution_narrative") or ""),
        "timing_narrative": str(narrative.get("timing_narrative") or ""),
        "prevention_narrative": str(narrative.get("prevention_narrative") or ""),
        "knowledge_engine_notes": narrative.get("knowledge_engine_notes") if isinstance(narrative.get("knowledge_engine_notes"), list) else [],
        "full_report_markdown": str(narrative.get("full_report_markdown") or _report_summary_markdown(output_payload)),
    }
    payload["knowledge_engine"] = {
        "available": bool(knowledge_context),
        "source": knowledge_context.get("source_module") if isinstance(knowledge_context, dict) else None,
    }
    payload["medical_disclaimer"] = MEDICAL_DISCLAIMER
    return payload


def _build_report_document(*, user_email: str, access_mode: str, input_payload: dict[str, Any], output_payload: dict[str, Any]) -> LongevityReportDocument:
    now = _now()
    return LongevityReportDocument(
        id=str(uuid4()),
        document_type="report",
        report_type=REPORT_TYPE,
        report_slug=REPORT_SLUG,
        user_email=user_email,
        access_mode=access_mode,
        created_at=now,
        updated_at=now,
        summary=str(output_payload["summary"]),
        input_payload=input_payload,
        output_payload=output_payload,
    )


def _report_summary_markdown(output_payload: dict[str, Any]) -> str:
    longevity = output_payload.get("longevity_classification") or {}
    prakriti = output_payload.get("constitutional_health_profile") or {}
    windows = output_payload.get("disease_susceptibility_windows") or []
    alerts = output_payload.get("critical_period_alerts") or []
    remedies = output_payload.get("remedial_guidance") or {}
    decades = output_payload.get("decade_quality_forecast") or []
    parts = [
        "## Longevity Overview",
        str(longevity.get("summary") or output_payload.get("summary") or ""),
        "",
        "## Constitutional Health Profile",
        str(prakriti.get("summary") or ""),
        "",
        "## Vulnerable Body Systems",
    ]
    for item in (output_payload.get("vulnerable_systems") or [])[:4]:
        parts.append(f"- **{item.get('title', 'System')}**: {item.get('prevention_focus', '')}")
    parts.extend(["", "## Disease Susceptibility Windows"])
    for item in windows[:3]:
        parts.append(f"- **{item.get('start_date')} to {item.get('end_date')}**: {item.get('headline', '')}")
    parts.extend(["", "## Critical Period Alerts"])
    for item in alerts[:3]:
        parts.append(f"- **{item.get('date')} · {item.get('type')}**: {item.get('detail', '')}")
    parts.extend(["", "## Remedial & Preventive Guidance"])
    for item in (remedies.get("preventive_guidance") or [])[:3]:
        parts.append(f"- {item}")
    parts.extend(["", "## Quality of Life Forecast"])
    for item in decades[:3]:
        parts.append(f"- **Age {item.get('age_band')}**: {item.get('note', '')}")
    return "\n".join(part for part in parts if part is not None).strip()


def _history_query(user_email: str) -> dict[str, Any]:
    return {"user_email": user_email, "document_type": "report", "report_type": REPORT_TYPE}


def _serialize_report_document(document: dict[str, Any]) -> LongevityReportDocument:
    payload = dict(document)
    payload.pop("_id", None)
    return LongevityReportDocument(**payload)


async def _persist_report_document(request: Request, report: LongevityReportDocument) -> LongevityReportDocument:
    payload = report.model_dump(mode="python")
    payload["updated_at"] = _now()
    await _collection(request).update_one(
        {"id": report.id, "report_type": REPORT_TYPE},
        {"$set": payload},
        upsert=True,
    )
    return LongevityReportDocument(**payload)


async def _load_report_document(request: Request, report_id: str) -> LongevityReportDocument:
    collection = _collection(request)
    filters: dict[str, Any] = {"id": report_id, "report_type": REPORT_TYPE}
    user = _resolve_user(request)
    if user.get("email"):
        filters["user_email"] = _normalize_email(str(user["email"]))
    document = await collection.find_one(filters)
    if document is None and "user_email" in filters:
        document = await collection.find_one({"id": report_id, "report_type": REPORT_TYPE})
    if document is None:
        raise HTTPException(status_code=404, detail="Longevity report not found.")
    return _serialize_report_document(document)


@router.get("/eligibility", response_model=AccessStatus)
async def get_longevity_eligibility(request: Request) -> AccessStatus:
    return _access_status(request)


@router.post("/generate", response_model=LongevityGenerateResponse)
async def generate_longevity_report(payload: LongevityGenerateRequest, request: Request) -> LongevityGenerateResponse:
    access = _access_status(request)
    user_email = _resolve_user_email(request, payload.user_email, allow_missing=True)
    if not access.entitled and not payload.preview:
        raise HTTPException(status_code=402, detail="Longevity premium access is required before generating a full report.")

    try:
        engine_payload = ReportInput(
            date_of_birth=payload.date_of_birth,
            time_of_birth=payload.time_of_birth,
            latitude=payload.latitude,
            longitude=payload.longitude,
            timezone_name=payload.timezone,
            place_label=payload.place_label,
            reference_date=payload.reference_date,
        )
        output_payload = compute_longevity_report(engine_payload)
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail="Longevity report generation failed.") from err

    try:
        knowledge_context = await _try_scan_chart(payload)
        narrative = await _call_claude_json(_narrative_prompt(output_payload, knowledge_context))
    except BaseException:
        knowledge_context = None
        narrative = None
    if not isinstance(narrative, dict):
        narrative = _fallback_narrative(output_payload, knowledge_context)
    output_payload = _apply_narrative(output_payload, narrative, knowledge_context)

    access_mode = "preview" if payload.preview or not access.entitled else "full"
    report = _build_report_document(
        user_email=user_email,
        access_mode=access_mode,
        input_payload=payload.model_dump(mode="python"),
        output_payload=output_payload,
    )

    should_persist = bool(user_email) and access_mode == "full"
    if should_persist:
        report = await _persist_report_document(request, report)
        state_user = getattr(request.state, "user", None) or {}
        if state_user.get("user_id"):
            await register_arc_angel_report_run(_db(request), str(state_user["user_id"]), REPORT_SLUG)

    return LongevityGenerateResponse(report=report, access=access)


@router.post("/report", response_model=LongevityGenerateResponse)
async def generate_longevity_report_contract(payload: LongevityGenerateRequest, request: Request) -> LongevityGenerateResponse:
    return await generate_longevity_report(payload, request)


@router.post("/save", response_model=LongevityReportDocument)
async def save_longevity_report(payload: LongevitySaveRequest, request: Request) -> LongevityReportDocument:
    user_email = _resolve_user_email(request)
    access = _access_status(request)
    if not access.entitled:
        raise HTTPException(status_code=402, detail="Longevity premium access is required before saving a report.")

    if payload.report is not None:
        report = payload.report
    elif payload.report_id:
        report = await _load_report_document(request, payload.report_id)
    else:
        raise HTTPException(status_code=422, detail="Provide either report or report_id.")

    if report.access_mode != "full":
        report = report.model_copy(update={"access_mode": "full"})
    report = report.model_copy(update={"user_email": user_email})
    return await _persist_report_document(request, report)


@router.get("/history", response_model=LongevityHistoryResponse)
async def get_longevity_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=25),
) -> LongevityHistoryResponse:
    user_email = _resolve_user_email(request)
    collection = _collection(request)
    query = _history_query(user_email)
    skip = (page - 1) * limit
    cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    documents = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)
    items = [
        LongevityHistoryItem(
            id=str(document["id"]),
            summary=str(document.get("summary") or ""),
            created_at=document["created_at"],
            classification=str((((document.get("output_payload") or {}).get("longevity_classification") or {}).get("label")) or "Unknown"),
            quality_band=str((((document.get("output_payload") or {}).get("longevity_classification") or {}).get("range_label")) or "Unknown"),
        )
        for document in documents
    ]
    return LongevityHistoryResponse(items=items, page=page, limit=limit, has_more=skip + limit < total)


@router.get("/my-reports", response_model=LongevityHistoryResponse)
async def get_longevity_my_reports(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=25),
) -> LongevityHistoryResponse:
    return await get_longevity_history(request=request, page=page, limit=limit)


@router.get("/alerts", response_model=LongevityAlertsResponse)
async def get_longevity_alerts(request: Request) -> LongevityAlertsResponse:
    user_email = _resolve_user_email(request)
    document = await _collection(request).find_one(_history_query(user_email), sort=[("created_at", -1)])
    if not document:
        return LongevityAlertsResponse(items=[], source_report_id=None, generated_for_date=None)
    report = _serialize_report_document(document)
    output_payload = report.output_payload
    alert_items = output_payload.get("critical_period_alerts")
    items = [LongevityAlertsItem(**item) for item in alert_items] if isinstance(alert_items, list) else []
    return LongevityAlertsResponse(
        items=items,
        source_report_id=report.id,
        generated_for_date=str(output_payload.get("generated_for_date") or ""),
    )


@router.get("/reports/{report_id}", response_model=LongevityReportDocument)
async def get_longevity_report(report_id: str, request: Request) -> LongevityReportDocument:
    return await _load_report_document(request, report_id)


@router.get("/report/{report_id}", response_model=LongevityReportDocument)
async def get_longevity_report_contract(report_id: str, request: Request) -> LongevityReportDocument:
    return await _load_report_document(request, report_id)
