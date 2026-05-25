from __future__ import annotations

import asyncio
import io
import os
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field
from pymongo import DESCENDING

from admin_utils import require_admin
from echo_pace_engine import EchoPaceEngine


router = APIRouter(prefix="/api/admin/echo-pace", tags=["echo-pace"])
AUDIT_COLLECTION = "echo_pace_audit_log"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EchoPaceProcessRequest(StrictModel):
    raw_text: str
    seo_keywords: list[str] = Field(default_factory=list)
    threshold: float = Field(default=0.20, ge=0.0, le=1.0)


class EchoPacePdfRequest(StrictModel):
    copyright_passed: bool
    similarity_score: float
    matched_sources: list[dict[str, Any]] = Field(default_factory=list)
    humanised_content: str
    meta_title: str
    meta_desc: str
    input_metrics: dict[str, Any] = Field(default_factory=dict)
    output_metrics: dict[str, Any] = Field(default_factory=dict)
    keyword_check: str
    missing_keywords: list[str] = Field(default_factory=list)
    scanned_sentences: int | None = None


def _db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database is not available")
    return db


def _engine() -> EchoPaceEngine:
    return EchoPaceEngine(
        serper_api_key=os.getenv("SERPER_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalise_log(document: dict[str, Any]) -> dict[str, Any]:
    payload = dict(document)
    payload["id"] = str(payload.pop("_id"))
    timestamp = payload.get("timestamp")
    if isinstance(timestamp, datetime):
        payload["timestamp"] = timestamp.isoformat()
    return payload


def _history_projection(include_content: bool = False) -> dict[str, int]:
    projection = {
        "timestamp": 1,
        "input_word_count": 1,
        "seo_keywords": 1,
        "copyright_passed": 1,
        "similarity_score": 1,
        "matched_sources": 1,
        "meta_title": 1,
        "meta_desc": 1,
        "input_metrics": 1,
        "output_metrics": 1,
        "keyword_check": 1,
    }
    if include_content:
        projection["humanised_content"] = 1
    return projection


async def ensure_echo_pace_indexes(db) -> None:
    await db[AUDIT_COLLECTION].create_index([("timestamp", DESCENDING)], name="echo_pace_timestamp_desc")


@router.post("/process")
async def process_echo_pace(payload: EchoPaceProcessRequest, request: Request) -> dict[str, Any]:
    db = _db(request)
    await require_admin(request, db)

    try:
        result = await asyncio.to_thread(
            _engine().process,
            payload.raw_text,
            payload.seo_keywords,
            payload.threshold,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    audit_entry = {
        "timestamp": _utc_now(),
        "input_word_count": int((result.get("input_metrics") or {}).get("word_count", 0)),
        "seo_keywords": payload.seo_keywords,
        "copyright_passed": result["copyright_passed"],
        "similarity_score": result["similarity_score"],
        "matched_sources": result["matched_sources"],
        "meta_title": result["meta_title"],
        "meta_desc": result["meta_desc"],
        "input_metrics": result["input_metrics"],
        "output_metrics": result["output_metrics"],
        "keyword_check": result["keyword_check"],
        "humanised_content": result["humanised_content"],
    }
    inserted = await db[AUDIT_COLLECTION].insert_one(audit_entry)

    return {
        **result,
        "log_id": str(inserted.inserted_id),
        "timestamp": audit_entry["timestamp"].isoformat(),
    }


@router.get("/history")
async def get_echo_pace_history(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    db = _db(request)
    await require_admin(request, db)

    skip = (page - 1) * page_size
    cursor = db[AUDIT_COLLECTION].find(
        {},
        _history_projection(include_content=False),
    ).sort("timestamp", -1).skip(skip).limit(page_size)
    documents = await cursor.to_list(length=page_size)
    total = await db[AUDIT_COLLECTION].count_documents({})

    return {
        "items": [_normalise_log(item) for item in documents],
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_more": skip + page_size < total,
    }


@router.get("/history/{log_id}")
async def get_echo_pace_history_item(log_id: str, request: Request) -> dict[str, Any]:
    db = _db(request)
    await require_admin(request, db)

    try:
        object_id = ObjectId(log_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid log ID") from exc

    document = await db[AUDIT_COLLECTION].find_one({"_id": object_id}, _history_projection(include_content=True))
    if document is None:
        raise HTTPException(status_code=404, detail="Audit log entry not found")
    return _normalise_log(document)


@router.delete("/history/{log_id}")
async def delete_echo_pace_history_item(log_id: str, request: Request) -> dict[str, Any]:
    db = _db(request)
    await require_admin(request, db)

    try:
        object_id = ObjectId(log_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid log ID") from exc

    result = await db[AUDIT_COLLECTION].delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audit log entry not found")
    return {"deleted": True, "id": log_id}


@router.post("/export-pdf")
async def export_echo_pace_pdf(payload: EchoPacePdfRequest, request: Request) -> StreamingResponse:
    db = _db(request)
    await require_admin(request, db)

    try:
        pdf_bytes = await asyncio.to_thread(_engine().build_pdf_report, payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {exc}") from exc

    filename = f"echo_pace_report_{_utc_now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
