from __future__ import annotations

import asyncio
import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import MongoClient

from admin_utils import require_admin
from auth_utils import get_current_user
from knowledge_schema import (
    COLLECTION_CASE_STUDIES,
    COLLECTION_IMPORT_BATCHES,
    COLLECTION_INTERPRETATION_RULES,
    COLLECTION_USER_CONTEXT_PROFILE,
    ApprovalStatus,
    CaseStudyDocument,
    EnginePrediction,
    UserContextProfileDocument,
)
from vedic_calculator import calculate_vedic_chart, calculate_vimshottari_dasha
from knowledge_engine import sync_arc_angel_questionnaire_state


router = APIRouter(tags=["knowledge-library"])


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


DEFAULT_QUESTIONNAIRE_VERSION = "v1"
USER_CONTEXT_MUTABLE_FIELDS = frozenset(
    {
        "questionnaire_version",
        "salary_bracket",
        "family_wealth_tier",
        "siblings_count",
        "current_city",
        "travel_frequency",
        "relationship_status",
        "parents_data",
    }
)
USER_CONTEXT_COMPLETION_FIELDS = (
    "salary_bracket",
    "family_wealth_tier",
    "siblings_count",
    "current_city",
    "travel_frequency",
    "relationship_status",
    "parents_data.father.dob",
    "parents_data.father.place",
    "parents_data.mother.dob",
    "parents_data.mother.place",
)


async def _require_authenticated_user(request: Request, db: AsyncIOMotorDatabase):
    user = await get_current_user(request, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def _serialize_user_context_profile(payload: dict[str, Any]) -> dict[str, Any]:
    return UserContextProfileDocument(**payload).model_dump(
        mode="json",
        by_alias=True,
        exclude_none=False,
    )


def _score_or_default(value: Any, default: float = 1.0) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = default
    return max(0.0, numeric)


def _recompute_context_profile_scores(profile: dict[str, Any]) -> tuple[float, float]:
    # Commission I-Q owns the eventual questionnaire-derived scoring logic. Until
    # then, the backend preserves neutral/default values and any previously
    # computed server-side scores rather than accepting client-written ones.
    return (
        _score_or_default(profile.get("beta_score"), default=1.0),
        _score_or_default(profile.get("gamma_score"), default=1.0),
    )


def _get_path_value(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _context_field_complete(profile: dict[str, Any], field_name: str) -> bool:
    value = _get_path_value(profile, field_name)
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None


def _context_profile_completion(profile: dict[str, Any]) -> tuple[int, list[str]]:
    missing_fields = [
        field_name
        for field_name in USER_CONTEXT_COMPLETION_FIELDS
        if not _context_field_complete(profile, field_name)
    ]
    completed = len(USER_CONTEXT_COMPLETION_FIELDS) - len(missing_fields)
    completion_pct = round((completed / len(USER_CONTEXT_COMPLETION_FIELDS)) * 100)
    return completion_pct, missing_fields


async def _ensure_user_context_profile(db: AsyncIOMotorDatabase, user_id: str) -> dict[str, Any]:
    existing = await db[COLLECTION_USER_CONTEXT_PROFILE].find_one({"user_id": user_id}, {"_id": 0})
    if existing is not None:
        return _serialize_user_context_profile(existing)

    default_document = UserContextProfileDocument(
        user_id=user_id,
        questionnaire_version=DEFAULT_QUESTIONNAIRE_VERSION,
    ).model_dump(mode="json", by_alias=True, exclude_none=False)
    await db[COLLECTION_USER_CONTEXT_PROFILE].insert_one(default_document)
    return default_document


POSITIVE_HINTS = {
    "success",
    "wealth",
    "gain",
    "growth",
    "marriage",
    "stable",
    "healthy",
    "recovery",
    "improvement",
    "support",
    "auspicious",
    "progress",
    "spiritual",
    "rise",
}
NEGATIVE_HINTS = {
    "loss",
    "delay",
    "problem",
    "difficult",
    "ill",
    "disease",
    "unstable",
    "separation",
    "debt",
    "struggle",
    "inauspicious",
    "decline",
    "fall",
    "stress",
    "conflict",
}
CASE_STUDY_DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
CASE_STUDY_DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}


@router.get("/api/user/context-profile")
async def get_user_context_profile(request: Request):
    db = _db_from_request(request)
    user = await _require_authenticated_user(request, db)
    profile = await _ensure_user_context_profile(db, user.user_id)
    return profile


@router.put("/api/user/context-profile")
async def update_user_context_profile(request: Request, payload: dict[str, Any]):
    db = _db_from_request(request)
    user = await _require_authenticated_user(request, db)

    existing_profile = await _ensure_user_context_profile(db, user.user_id)
    raw_updates = payload if isinstance(payload, dict) else {}
    allowed_updates = {
        key: value
        for key, value in raw_updates.items()
        if key in USER_CONTEXT_MUTABLE_FIELDS
    }

    merged_profile = {**existing_profile, **allowed_updates}
    merged_profile["user_id"] = user.user_id
    merged_profile["questionnaire_version"] = (
        str(merged_profile.get("questionnaire_version") or DEFAULT_QUESTIONNAIRE_VERSION)
    )
    beta_score, gamma_score = _recompute_context_profile_scores(existing_profile)
    merged_profile["beta_score"] = beta_score
    merged_profile["gamma_score"] = gamma_score
    merged_profile["last_updated"] = utc_now()

    serialized_profile = _serialize_user_context_profile(merged_profile)
    await db[COLLECTION_USER_CONTEXT_PROFILE].update_one(
        {"user_id": user.user_id},
        {
            "$set": serialized_profile,
            "$setOnInsert": {"user_id": user.user_id},
        },
        upsert=True,
    )
    arc_angel_profile = await sync_arc_angel_questionnaire_state(db, user.user_id, serialized_profile)
    completion_pct, missing_fields = _context_profile_completion(serialized_profile)
    return {
        "profile": serialized_profile,
        "completion_pct": completion_pct,
        "missing_fields": missing_fields,
        "arc_angel_confidence_pct": arc_angel_profile.get("overall_confidence_pct", 40),
    }


@router.get("/api/user/context-profile/completion")
async def get_user_context_profile_completion(request: Request):
    db = _db_from_request(request)
    user = await _require_authenticated_user(request, db)
    profile = await _ensure_user_context_profile(db, user.user_id)
    completion_pct, missing_fields = _context_profile_completion(profile)
    return {
        "completion_pct": completion_pct,
        "missing_fields": missing_fields,
    }


def _case_outcome_text(outcome: dict[str, Any]) -> str:
    return " ".join(
        part.strip()
        for part in [str(outcome.get("outcome") or ""), str(outcome.get("notes") or "")]
        if part and part.strip()
    ).lower()


def _infer_sign_from_text(text: str) -> int:
    positives = sum(1 for token in POSITIVE_HINTS if token in text)
    negatives = sum(1 for token in NEGATIVE_HINTS if token in text)
    if positives > negatives:
        return 1
    if negatives > positives:
        return -1
    return 0


def _infer_rule_sign(rule: dict[str, Any]) -> int:
    polarity = str(rule.get("claim_polarity") or "").lower()
    if polarity == "positive":
        return 1
    if polarity == "negative":
        return -1
    period_quality = str(rule.get("period_quality") or "").lower()
    if period_quality == "auspicious":
        return 1
    if period_quality == "inauspicious":
        return -1
    return 0


def _rule_summary(rule: dict[str, Any]) -> str:
    interpretation = rule.get("interpretation") or {}
    return str(interpretation.get("summary") or interpretation.get("detailed") or "").strip()


def _rule_domain_matches(rule: dict[str, Any], life_domain: str, claim_axis: str) -> bool:
    if claim_axis and str(rule.get("claim_axis") or "") == claim_axis:
        return True
    if life_domain and str(rule.get("life_domain") or "") == life_domain:
        return True
    categories = {str(item) for item in (rule.get("categories") or [])}
    return bool(life_domain and life_domain in categories)


def _select_case_rules(outcome: dict[str, Any], matched_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    life_domain = str(outcome.get("life_domain") or "")
    claim_axis = str(outcome.get("claim_axis") or "")
    relevant = [
        rule for rule in matched_rules if _rule_domain_matches(rule, life_domain=life_domain, claim_axis=claim_axis)
    ]
    if not relevant:
        relevant = matched_rules[:]
    relevant.sort(
        key=lambda rule: (
            float(rule.get("effective_confidence") or 0.0),
            float(rule.get("score") or 0.0),
        ),
        reverse=True,
    )
    return relevant


def _build_case_predictions(
    known_outcomes: list[dict[str, Any]],
    matched_rules: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], float | None]:
    predictions: list[dict[str, Any]] = []
    alignment_scores: list[float] = []

    for outcome in known_outcomes:
        selected_rules = _select_case_rules(outcome, matched_rules)
        top_rule = selected_rules[0] if selected_rules else {}
        prediction = EnginePrediction(
            life_domain=str(outcome.get("life_domain") or ""),
            claim_axis=str(outcome.get("claim_axis") or ""),
            predicted_outcome=_rule_summary(top_rule) or str(top_rule.get("claim_polarity") or "No matching rule"),
            period_quality=top_rule.get("period_quality") or None,
            confidence=float(top_rule.get("effective_confidence")) if top_rule.get("effective_confidence") is not None else None,
            matched_rule_ids=[
                str(rule.get("rule_id") or "")
                for rule in selected_rules[:5]
                if str(rule.get("rule_id") or "")
            ],
        ).model_dump(mode="json", by_alias=True, exclude_none=True)
        predictions.append(prediction)

        outcome_sign = _infer_sign_from_text(_case_outcome_text(outcome))
        rule_sign = _infer_rule_sign(top_rule)
        if outcome_sign == 0 or rule_sign == 0:
            alignment_scores.append(0.5)
        elif outcome_sign == rule_sign:
            alignment_scores.append(1.0)
        else:
            alignment_scores.append(0.0)

    accuracy_score = round(sum(alignment_scores) / len(alignment_scores), 4) if alignment_scores else None
    return predictions, accuracy_score


def _approximate_moon_longitude(chart_data: dict[str, Any]) -> float:
    moon_longitude = chart_data.get("moon_longitude")
    if isinstance(moon_longitude, (int, float)):
        return float(moon_longitude)

    nakshatra = chart_data.get("nakshatra") or {}
    try:
        nak_index = int(nakshatra.get("index"))
        pada = int(nakshatra.get("pada", 2))
    except (TypeError, ValueError):
        return 0.0

    nak_span = 360.0 / 27.0
    pada = min(4, max(1, pada))
    pada_fraction = ((pada - 1) + 0.5) / 4.0
    return (nak_index * nak_span) + (nak_span * pada_fraction)


def _case_study_cycle_sequence(start_lord: str) -> list[str]:
    if start_lord not in CASE_STUDY_DASHA_ORDER:
        return list(CASE_STUDY_DASHA_ORDER)
    start_index = CASE_STUDY_DASHA_ORDER.index(start_lord)
    return CASE_STUDY_DASHA_ORDER[start_index:] + CASE_STUDY_DASHA_ORDER[:start_index]


def _build_case_study_sub_dashas(parent_lord: str, start_iso: str, end_iso: str) -> list[dict[str, Any]]:
    start = datetime.fromisoformat(f"{start_iso}T00:00:00")
    end = datetime.fromisoformat(f"{end_iso}T00:00:00")
    total_seconds = max(0.0, (end - start).total_seconds())
    cursor = start
    sub_dashas: list[dict[str, Any]] = []
    for lord in _case_study_cycle_sequence(parent_lord):
        share = CASE_STUDY_DASHA_YEARS.get(lord, 0) / 120.0
        duration = total_seconds * share
        item_end = cursor + timedelta(seconds=duration)
        sub_dashas.append(
            {
                "planet": lord,
                "start": cursor.date().isoformat(),
                "end": item_end.date().isoformat(),
            }
        )
        cursor = item_end
    if sub_dashas:
        sub_dashas[-1]["end"] = end.date().isoformat()
    return sub_dashas


def _build_case_study_dasha_timeline(birth_date: str, moon_longitude: float) -> list[dict[str, Any]]:
    maha_dashas = calculate_vimshottari_dasha(birth_date, moon_longitude)
    timeline: list[dict[str, Any]] = []
    for maha in maha_dashas:
        planet = str(maha.get("planet") or "")
        start = str(maha.get("start") or "")
        end = str(maha.get("end") or "")
        if not planet or not start or not end:
            continue
        timeline.append(
            {
                "planet": planet,
                "start": start,
                "end": end,
                "antardashas": _build_case_study_sub_dashas(planet, start, end),
            }
        )
    return timeline


@router.get("/api/knowledge/rules")
async def list_rules(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    science_id: str | None = None,
    category: str | None = None,
    approval_status: ApprovalStatus | None = None,
    strength_band: str | None = None,
    batch_id: str | None = None,
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
    if batch_id:
        filters["source.batch_id"] = batch_id

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
        "source": 1,
        "interpretation": 1,
        "condition": 1,
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


@router.get("/api/knowledge/rules/{rule_id}")
async def get_rule(request: Request, rule_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    rule = await db[COLLECTION_INTERPRETATION_RULES].find_one({"rule_id": rule_id}, {"_id": 0})
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.patch("/api/knowledge/rules/{rule_id}/approve")
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


@router.patch("/api/knowledge/rules/{rule_id}/reject")
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


@router.get("/api/knowledge/import-batches")
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


@router.get("/api/knowledge/import-batches/{batch_id}")
async def get_import_batch(request: Request, batch_id: str):
    db = _db_from_request(request)
    await require_admin(request, db)

    batch = await db[COLLECTION_IMPORT_BATCHES].find_one({"batch_id": batch_id}, {"_id": 0})
    if batch is None:
        raise HTTPException(status_code=404, detail="Import batch not found")
    return batch


@router.post("/api/knowledge/import-batches/{batch_id}/approve-all")
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


@router.post("/api/knowledge/validate-batch")
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


@router.get("/api/knowledge/index/status")
async def knowledge_index_status(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)
    return engine.index_refresh_status()


@router.post("/api/knowledge/index/refresh")
async def trigger_knowledge_index_refresh(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)
    engine.schedule_index_refresh()
    return {"index_refresh_triggered": True}


@router.get("/api/knowledge-engine/case-studies")
async def list_case_studies(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)

    cases = await (
        db[COLLECTION_CASE_STUDIES]
        .find({}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(length=None)
    )
    return {"cases": cases}


@router.post("/api/knowledge-engine/case-studies/import")
async def import_case_studies(request: Request, payload: dict[str, Any]):
    db = _db_from_request(request)
    await require_admin(request, db)

    raw_cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(raw_cases, list) or not raw_cases:
        raise HTTPException(status_code=400, detail="Request body must include a non-empty 'cases' array")

    imported = 0
    errors: list[str] = []
    timestamp = utc_now()

    for index, item in enumerate(raw_cases, start=1):
        if not isinstance(item, dict):
            errors.append(f"Row {index}: case payload must be an object")
            continue
        try:
            case_doc = CaseStudyDocument(
                **{
                    **item,
                    "created_at": item.get("created_at") or timestamp,
                    "updated_at": timestamp,
                }
            )
        except Exception as exc:
            errors.append(f"Row {index}: {exc}")
            continue

        document = case_doc.model_dump(mode="json", by_alias=True, exclude_none=True)
        await db[COLLECTION_CASE_STUDIES].update_one(
            {"case_id": case_doc.case_id},
            {
                "$set": {
                    **document,
                    "updated_at": timestamp.isoformat(),
                },
                "$setOnInsert": {"created_at": document.get("created_at", timestamp.isoformat())},
            },
            upsert=True,
        )
        imported += 1

    if imported == 0:
        raise HTTPException(
            status_code=400,
            detail=errors[0] if errors else "No valid case studies were provided",
        )

    return {
        "cases_imported": imported,
        "errors": errors,
        "message": f"{imported} cases imported",
    }


@router.post("/api/knowledge-engine/case-studies/validate-batch")
async def validate_case_studies_batch(request: Request):
    db = _db_from_request(request)
    await require_admin(request, db)
    engine = _engine_from_request(request)

    async def _run() -> None:
        try:
            case_payloads = await (
                db[COLLECTION_CASE_STUDIES]
                .find({"validated": False}, {"_id": 0})
                .to_list(length=None)
            )
            for payload in case_payloads:
                try:
                    case_doc = CaseStudyDocument(**payload)
                except Exception:
                    logging.exception("Skipping invalid case study payload during validation")
                    continue

                try:
                    chart_data = await asyncio.to_thread(
                        calculate_vedic_chart,
                        date_of_birth=case_doc.birth_data.date,
                        time_of_birth=case_doc.birth_data.time,
                        place_of_birth=case_doc.birth_data.place,
                    )
                    moon_longitude = _approximate_moon_longitude(chart_data)
                    dasha_timeline = _build_case_study_dasha_timeline(
                        case_doc.birth_data.date,
                        moon_longitude,
                    )
                    matched_rules = await engine.scan_chart(
                        chart=chart_data,
                        max_rules=200,
                        context={"backbone_science_id": "vedic_astrology"},
                        dasha_timeline=dasha_timeline,
                    )
                    predictions, accuracy_score = _build_case_predictions(
                        [item.model_dump(mode="json", by_alias=True, exclude_none=True) for item in case_doc.known_outcomes],
                        matched_rules,
                    )
                    await db[COLLECTION_CASE_STUDIES].update_one(
                        {"case_id": case_doc.case_id},
                        {
                            "$set": {
                                "engine_predictions": predictions,
                                "accuracy_score": accuracy_score,
                                "validated": True,
                                "updated_at": utc_now(),
                            }
                        },
                    )
                except Exception:
                    logging.exception("Case study validation failed for %s", case_doc.case_id)
        except Exception:
            logging.exception("Case study batch validation background task failed")

    asyncio.create_task(_run())
    return {
        "status": "validation_started",
        "message": "Batch validation started. Check back in a few minutes.",
    }
