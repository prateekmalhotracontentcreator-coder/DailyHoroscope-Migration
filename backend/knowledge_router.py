from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

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
