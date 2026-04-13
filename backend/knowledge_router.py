from __future__ import annotations

import asyncio
import logging
import os
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import MongoClient

from admin_utils import require_admin
from knowledge_schema import (
    COLLECTION_IMPORT_BATCHES,
    COLLECTION_INTERPRETATION_RULES,
    ApprovalStatus,
)


router = APIRouter(prefix="/api/knowledge", tags=["knowledge-library"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _db_from_request(request: Request) -> AsyncIOMotorDatabase:
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database is not available")
    return db


def _engine_from_request(request: Request):
    engine = getattr(request.app.state, "knowledge_engine", None)
    if engine is None:
        raise HTTPException(status_code=503, detail="Knowledge engine is not available")
    return engine


@router.get("/rules")
async def list_rules(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    science_id: str | None = None,
    category: str | None = None,
    approval_status: ApprovalStatus | None = None,
    strength_band: str | None = None,
):
    db = _db_from_request(request)
    await require_admin(request, db)

    filters: dict[str, object] = {}
    if science_id:
        filters["science_id"] = science_id
    if category:
        filters["categories"] = category
    if approval_status:
        filters["approval_status"] = approval_status
    if strength_band:
        filters["strength_band"] = strength_band

    projection = {
        "_id": 0,
        "rule_id": 1,
        "science_id": 1,
        "life_domain": 1,
        "categories": 1,
        "strength_band": 1,
        "approval_status": 1,
        "claim_axis": 1,
        "claim_polarity": 1,
        "claim_scope": 1,
        "priority": 1,
        "intensity_score": 1,
        "active": 1,
        "validation": 1,
        "created_at": 1,
        "updated_at": 1,
    }
    skip = (page - 1) * page_size
    total = await db[COLLECTION_INTERPRETATION_RULES].count_documents(filters)
    pages = max(1, (total + page_size - 1) // page_size)
    rules = await (
        db[COLLECTION_INTERPRETATION_RULES]
        .find(filters, projection)
        .sort("updated_at", -1)
        .skip(skip)
        .limit(page_size)
        .to_list(length=page_size)
    )
    return {
        "rules": rules,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


@router.get("/rules/{rule_id}")
async def get_rule(request: Request, rule_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    rule = await db[COLLECTION_INTERPRETATION_RULES].find_one({"rule_id": rule_id}, {"_id": 0})
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.patch("/rules/{rule_id}/approve")
async def approve_rule(request: Request, rule_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    result = await db[COLLECTION_INTERPRETATION_RULES].update_one(
        {"rule_id": rule_id},
        {"$set": {"approval_status": "approved", "updated_at": utc_now()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"rule_id": rule_id, "approval_status": "approved"}


@router.patch("/rules/{rule_id}/reject")
async def reject_rule(request: Request, rule_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    result = await db[COLLECTION_INTERPRETATION_RULES].update_one(
        {"rule_id": rule_id},
        {"$set": {"approval_status": "rejected", "updated_at": utc_now()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"rule_id": rule_id, "approval_status": "rejected"}


@router.get("/import-batches")
async def list_import_batches(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)

    batches = await (
        db[COLLECTION_IMPORT_BATCHES]
        .find(
            {},
            {
                "_id": 0,
                "batch_id": 1,
                "source_book": 1,
                "import_status": 1,
                "approval_status": 1,
                "rules_submitted": 1,
                "rules_imported": 1,
                "duplicate_count": 1,
                "error_count": 1,
                "index_refreshed": 1,
                "created_at": 1,
                "updated_at": 1,
            },
        )
        .sort("created_at", -1)
        .to_list(length=None)
    )
    return {"batches": batches}


@router.get("/import-batches/{batch_id}")
async def get_import_batch(request: Request, batch_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    batch = await db[COLLECTION_IMPORT_BATCHES].find_one({"batch_id": batch_id}, {"_id": 0})
    if batch is None:
        raise HTTPException(status_code=404, detail="Import batch not found")
    return batch


@router.post("/import-batches/{batch_id}/approve-all")
async def approve_all_batch_rules(request: Request, batch_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    batch = await db[COLLECTION_IMPORT_BATCHES].find_one({"batch_id": batch_id}, {"_id": 0, "batch_id": 1})
    if batch is None:
        raise HTTPException(status_code=404, detail="Import batch not found")

    timestamp = utc_now()
    rules_result = await db[COLLECTION_INTERPRETATION_RULES].update_many(
        {
            "source.batch_id": batch_id,
            "approval_status": {"$ne": "approved"},
        },
        {
            "$set": {
                "approval_status": "approved",
                "updated_at": timestamp,
            }
        },
    )
    await db[COLLECTION_IMPORT_BATCHES].update_one(
        {"batch_id": batch_id},
        {
            "$set": {
                "approval_status": "approved",
                "updated_at": timestamp,
            }
        },
    )
    return {"batch_id": batch_id, "rules_approved": rules_result.modified_count}


@router.post("/validate-batch")
async def validate_batch_endpoint(
    request: Request,
    batch_id: str | None = None,
    science_id: str | None = None,
):
    """
    Trigger Claude validation on pending_review rules.
    Optional: filter by batch_id or science_id.
    Runs as a background task and returns immediately.
    """
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)

    query: dict[str, object] = {"approval_status": "pending_review"}
    if batch_id:
        query["source.batch_id"] = batch_id
    if science_id:
        query["science_id"] = science_id

    mongo_url = os.getenv("MONGO_URL", "")
    db_name = os.getenv("DB_NAME") or getattr(db, "name", None) or "EverydayHoroscope"

    def _run_sync(active_query: dict[str, object], mongo_uri: str, database_name: str) -> None:
        from knowledge_validator import RuleValidator

        if not mongo_uri:
            raise RuntimeError("MONGO_URL is not set in the environment")

        sync_client = MongoClient(mongo_uri)
        try:
            sync_db = sync_client[database_name]
            rules = list(sync_db[COLLECTION_INTERPRETATION_RULES].find(active_query, {"_id": 0}))
            validator = RuleValidator(model="claude-haiku-4-5")

            all_verdicts: dict[str, dict[str, object]] = {}
            ok_rules: list[dict] = []
            now = utc_now().isoformat()

            for rule in rules:
                passed, reason = validator.structural_check(rule)
                if not passed:
                    all_verdicts[rule["rule_id"]] = {
                        "verdict": "structural_fail",
                        "reason": reason,
                        "corrected_confidence": "LOW",
                    }
                    continue
                ok_rules.append(rule)

            batch_size = 20
            for index in range(0, len(ok_rules), batch_size):
                batch = ok_rules[index : index + batch_size]
                try:
                    results = validator.validate_batch(batch)
                except Exception as exc:  # pragma: no cover - network/runtime dependent
                    results = [
                        {
                            "rule_id": rule["rule_id"],
                            "verdict": "spot_check",
                            "reason": str(exc),
                            "corrected_confidence": "MEDIUM",
                        }
                        for rule in batch
                    ]

                result_map = {result["rule_id"]: result for result in results if result.get("rule_id")}
                for rule in batch:
                    rid = rule["rule_id"]
                    all_verdicts[rid] = result_map.get(
                        rid,
                        {
                            "rule_id": rid,
                            "verdict": "spot_check",
                            "reason": "no_response_from_model",
                            "corrected_confidence": "MEDIUM",
                        },
                    )

            groups: dict[str, list[dict]] = defaultdict(list)
            for rule in ok_rules:
                cond = rule.get("condition") or {}
                key = f"{cond.get('type', '')}|{cond.get('planet', '')}|{cond.get('house', cond.get('sign', ''))}"
                groups[key].append(rule)

            contradiction_map: dict[str, list[str]] = defaultdict(list)
            contradiction_summary_map: dict[str, str] = {}
            for group_rules in groups.values():
                if len(group_rules) < 2:
                    continue
                try:
                    pairs = validator.detect_contradictions(group_rules)
                except Exception:  # pragma: no cover - network/runtime dependent
                    pairs = []
                for pair in pairs:
                    rule_id_a = pair.get("rule_id_a", "")
                    rule_id_b = pair.get("rule_id_b", "")
                    if not rule_id_a or not rule_id_b:
                        continue
                    contradiction_map[rule_id_a].append(rule_id_b)
                    contradiction_map[rule_id_b].append(rule_id_a)
                    summary = pair.get("contradiction_summary", "")
                    if summary:
                        contradiction_summary_map.setdefault(rule_id_a, summary)
                        contradiction_summary_map.setdefault(rule_id_b, summary)

            status_map = {
                "approve": "auto_approved",
                "spot_check": "pending_human_review",
                "flag": "flagged",
                "structural_fail": "rejected",
            }
            for rule in rules:
                rid = rule["rule_id"]
                verdict_info = all_verdicts.get(
                    rid,
                    {"verdict": "spot_check", "reason": "", "corrected_confidence": "MEDIUM"},
                )
                verdict = str(verdict_info.get("verdict", "spot_check"))
                reason = str(verdict_info.get("reason", ""))
                corrected_confidence = str(verdict_info.get("corrected_confidence", "MEDIUM"))
                contradiction_ids = contradiction_map.get(rid, [])
                if verdict == "approve" and contradiction_ids:
                    verdict = "spot_check"
                    reason = f"Contradicts: {', '.join(contradiction_ids)}"
                sync_db[COLLECTION_INTERPRETATION_RULES].update_one(
                    {"rule_id": rid},
                    {
                        "$set": {
                            "approval_status": status_map.get(verdict, "pending_review"),
                            "validation": {
                                "verdict": verdict,
                                "flag_reason": reason,
                                "corrected_confidence": corrected_confidence,
                                "validated_by": "claude-haiku-4-5",
                                "validated_at": now,
                                "contradiction_ids": contradiction_ids,
                                "contradiction_summary": contradiction_summary_map.get(rid, ""),
                            },
                            "updated_at": utc_now(),
                        }
                    },
                )
        finally:
            sync_client.close()

    async def _run() -> None:
        try:
            await asyncio.to_thread(_run_sync, dict(query), mongo_url, db_name)
            engine.schedule_index_refresh()
        except Exception:
            logging.exception("Knowledge rule validation background task failed")

    asyncio.create_task(_run())
    return {
        "status": "validation_started",
        "message": "Validation running in background. Check Rules Browser in ~3 minutes.",
    }


@router.get("/index/status")
async def knowledge_index_status(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)
    return engine.index_refresh_status()


@router.post("/index/refresh")
async def trigger_knowledge_index_refresh(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)
    engine.schedule_index_refresh()
    return {"index_refresh_triggered": True}
