from fastapi import FastAPI, APIRouter, BackgroundTasks, HTTPException, Request, Response, UploadFile, File, Form, Header
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi.responses import StreamingResponse, HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import hmac
import hashlib
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Any, Dict, List, Literal, Optional
import uuid
from datetime import datetime, timezone, date, timedelta
from zoneinfo import ZoneInfo
import anthropic
from pymongo import ReturnDocument

# ── pkg_resources shim ────────────────────────────────────────────────────────
# razorpay==1.3.0 calls `import pkg_resources` at import time.
# python:3.12-slim does not ship setuptools (which provides pkg_resources).
# We inject a minimal stub into sys.modules BEFORE importing razorpay so the
# import succeeds without needing setuptools installed.
import sys as _sys
if "pkg_resources" not in _sys.modules:
    import types as _types
    _pkg = _types.ModuleType("pkg_resources")
    _pkg.get_distribution = lambda name: None
    _pkg.DistributionNotFound = Exception
    _sys.modules["pkg_resources"] = _pkg
# ─────────────────────────────────────────────────────────────────────────────

import razorpay
import httpx
import io
import asyncio
import tempfile
from concurrent.futures import ThreadPoolExecutor

# ── Google / YouTube libraries (optional -- graceful fallback if not installed) ─
try:
    from google.oauth2.credentials import Credentials as GoogleCredentials
    from google.auth.transport.requests import Request as GoogleRequest
    from google_auth_oauthlib.flow import Flow as GoogleFlow
    from googleapiclient.discovery import build as google_build
    from googleapiclient.http import MediaIoBaseUpload
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False
from pdf_generator import generate_birth_chart_pdf, generate_kundali_milan_pdf, generate_brihat_kundli_pdf, generate_report_password
import vedic_calculator as vedic_calculator_module
from vedic_calculator import build_dasha_timeline, calculate_vedic_chart, calculate_ashtakoot, check_mangal_dosha, generate_north_indian_chart_svg
import secrets
from auth_utils import (
    User, UserSession, RegisterRequest, LoginRequest, UserResponse,
    hash_password, verify_password, create_session, get_current_user,
    get_or_create_oauth_user, set_session_cookie, exchange_session_id_for_token
)
from admin_utils import (
    AdminLoginRequest, AdminLoginResponse, DashboardStats, UserListItem, PaymentListItem,
    ChangePasswordRequest, verify_admin_password, create_admin_session, require_admin,
    set_admin_session_cookie, update_admin_password, hash_new_password, ADMIN_USERNAME
)
from models.diagnostics import (
    DiagnosticFlagRequest,
    TelemetryEvent,
    TelemetryLogRequest,
)
from models.gst import GSTLedgerEntry
from models.orders import ForceHealOrderRequest
from remedies_router import router as remedies_router
from crystal_router import router as crystal_router
from compatibility_router import router as compatibility_router
from panchang_router import router as panchang_router
from seo_router import router as seo_router
from seo_m3_router import router as seo_m3_router
from numerology_router import LoveCalculatorRequest, LoveCalculatorResponse, love_calculator, router as numerology_router
from remedy_matching_router import router as remedy_matching_router
from tarot_router import router as tarot_router
from kundali_router import router as kundali_router
from karmic_debt_router import router as karmic_debt_router
from career_blueprint_router import router as career_blueprint_router
from shadow_self_router import router as shadow_self_router
from retrograde_survival_router import router as retrograde_survival_router
from life_cycles_router import router as life_cycles_router
from wealth_blueprint_router import router as wealth_blueprint_router
from romance_creative_router import router as romance_creative_router
from vitality_health_router import router as vitality_health_router
from partnership_window_router import router as partnership_window_router
from dharma_purpose_router import router as dharma_purpose_router
from gains_network_router import router as gains_network_router
from ir_enhancement_router import router as ir_enhancement_router
from encounter_window_router import router as encounter_window_router
from date_night_router import router as date_night_router
from digital_dating_router import router as digital_dating_router
from intimacy_vitality_router import router as intimacy_vitality_router
from lunar_cycle_router import router as lunar_cycle_router
from love_weather_router import router as love_weather_router
from ritual_trigger_router import router as ritual_trigger_router
from soul_connection_router import router as soul_connection_router
from soulmate_timing_router import router as soulmate_timing_router
from venus_retrograde_router import router as venus_retrograde_router
from notification_preferences_router import router as notification_preferences_router
from notification_feed_router import router as notification_feed_router
from notification_push_router import router as notification_push_router
from notification_trigger_router import router as notification_trigger_router
from notification_log_router import router as notification_log_router
from lumina_router import router as lumina_router
from palmistry_router import router as palmistry_router
from rudraksha_router import router as rudraksha_router
from knowledge_engine import (
    ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
    ARC_ANGEL_DOMAIN_LABELS,
    ARC_ANGEL_DOMAIN_SLUGS,
    ARC_ANGEL_ENGINE_LABEL,
    arc_angel_profile_is_fresh,
    build_arc_angel_data_completeness,
    build_arc_angel_profile_doc,
    build_domain_rule_map,
    compute_arc_angel_windows,
    compute_period_quality_now,
    configure_default_knowledge_engine,
    register_arc_angel_report_run,
    run_arc_angel_pillar3_decay_job,
)
from knowledge_router import router as knowledge_router
from knowledge_schema import KnowledgeNarrativeRequest, KnowledgeNarrativeResponse
from lk_remedies_router import router as lk_router
from strategist_router import router as strategist_router
from scriptural_oracle_router import router as kp_router
from live_tv_router import router as live_tv_router
from punya_rewards_router import router as punya_rewards_router
from lo_shu_router import router as lo_shu_router
from zibu_router import router as zibu_router
from angel_numbers_router import router as angel_numbers_router
try:
    from longevity_router import router as longevity_router
    _longevity_router_ok = True
except Exception as _longevity_import_err:
    longevity_router = None
    _longevity_router_ok = False
    logging.warning("longevity_router failed to load: %s", _longevity_import_err)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

razorpay_client = razorpay.Client(auth=(
    os.environ.get('RAZORPAY_KEY_ID'),
    os.environ.get('RAZORPAY_KEY_SECRET')
))
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]

PRICING = {
    "birth_chart": 799,
    "brihat_kundli": 1499,
    "kundali_milan": 1199,
    "premium_monthly": 1599
}

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(
    mongo_url,
    serverSelectionTimeoutMS=8000,
    socketTimeoutMS=10000,
    connectTimeoutMS=8000,
)
db = client[os.environ['DB_NAME']]

app = FastAPI()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
async def health_check():
    """Render health check -- must return 2xx or deploy is marked failed."""
    return {"status": "ok", "service": "EverydayHoroscope API"}

# ── Session middleware -- populates request.state.user for ALL routers ──────────
# Codex routers (Numerology, Tarot) read request.state.user to resolve the
# authenticated user. This middleware bridges our session-cookie auth system
# to that pattern, running before every request reaches any router.

class SessionUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        try:
            session_token = request.cookies.get("session_token")
            if not session_token:
                auth_header = request.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    session_token = auth_header.split("Bearer ", 1)[1].strip()
            if session_token:
                session_doc = await db.user_sessions.find_one(
                    {"session_token": session_token}, {"_id": 0}
                )
                if session_doc:
                    expires_at = session_doc.get("expires_at")
                    if isinstance(expires_at, str):
                        expires_at = datetime.fromisoformat(expires_at)
                    if expires_at and expires_at.tzinfo is None:
                        expires_at = expires_at.replace(tzinfo=timezone.utc)
                    if expires_at and expires_at > datetime.now(timezone.utc):
                        user_doc = await db.users.find_one(
                            {"user_id": session_doc["user_id"]},
                            {"_id": 0, "password_hash": 0}
                        )
                        if user_doc:
                            request.state.user = {
                                "email": user_doc.get("email"),
                                "name": user_doc.get("name"),
                                "user_id": user_doc.get("user_id"),
                                "picture": user_doc.get("picture"),
                            }
        except Exception as e:
            logging.warning("SessionUserMiddleware error (non-fatal): %s", e)
        return await call_next(request)


async def _resolve_request_user_id(request: Request) -> Optional[str]:
    state_user = getattr(request.state, "user", None)
    if isinstance(state_user, dict) and state_user.get("user_id"):
        return state_user["user_id"]

    session_token = request.cookies.get("session_token")
    if not session_token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            session_token = auth_header.split("Bearer ", 1)[1].strip()
    if not session_token:
        return None

    session_doc = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0, "user_id": 1, "expires_at": 1},
    )
    if not session_doc:
        return None

    expires_at = session_doc.get("expires_at")
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at and expires_at <= utc_now():
        return None
    return session_doc.get("user_id")


async def _append_diagnostic_event(user_id: str, payload: Dict[str, Any]) -> None:
    if not user_id:
        return
    event_payload = dict(payload)
    event_payload["timestamp"] = event_payload.get("timestamp") or utc_now()
    try:
        await db["user_diagnostics"].update_one(
            {"_id": user_id},
            {
                "$set": {"last_updated": utc_now()},
                "$push": {"event_stream": {"$each": [event_payload], "$slice": -500}},
                "$setOnInsert": {"is_claim_flagged": False},
            },
            upsert=True,
        )
    except Exception as exc:
        logging.warning("[Diagnostics] DB write failed: %s", exc)


def _serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    def serialize(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, list):
            return [serialize(item) for item in value]
        if isinstance(value, dict):
            return {key: serialize(item) for key, item in value.items()}
        return value

    return serialize(doc)


async def _resolve_diagnostics_lookup(search_value: str) -> tuple[Optional[str], Optional[Dict[str, Any]], Optional[str]]:
    normalized = (search_value or "").strip()
    if not normalized:
        return None, None, None

    user_doc = None
    resolved_user_id = normalized

    if "@" in normalized:
        normalized_email = normalized.lower()
        user_doc = await db.users.find_one(
            {"$or": [{"email": normalized}, {"email": normalized_email}]},
            {"_id": 0, "user_id": 1, "email": 1},
        )
        if user_doc:
            resolved_user_id = user_doc.get("user_id") or normalized
        else:
            resolved_user_id = f"email:{normalized_email}"
    else:
        user_doc = await db.users.find_one({"user_id": normalized}, {"_id": 0, "user_id": 1, "email": 1})

    payment_email = user_doc.get("email") if user_doc else None
    if not payment_email and resolved_user_id.startswith("email:"):
        payment_email = resolved_user_id.split("email:", 1)[1]

    return resolved_user_id, user_doc, payment_email


def _normalize_email(value: str | None) -> str:
    return (value or "").strip().lower()


def _derive_order_user_id(request_user_id: Optional[str], user_email: str) -> str:
    normalized_email = _normalize_email(user_email)
    return request_user_id or f"email:{normalized_email}"


async def _mark_order_state(
    order_id: str,
    state: str,
    *,
    ts_field: Optional[str] = None,
    extra_updates: Optional[Dict[str, Any]] = None,
) -> None:
    updates: Dict[str, Any] = {"current_state": state}
    if ts_field:
        updates[ts_field] = utc_now()
    if extra_updates:
        updates.update(extra_updates)
    await db["orders_ledger"].update_one({"_id": order_id}, {"$set": updates})


async def _mark_order_fulfilled(order_id: str, *, generated_report_id: Optional[str] = None) -> None:
    updates: Dict[str, Any] = {
        "current_state": "FULFILLED",
        "ts_fulfill_done": utc_now(),
        "error_log": None,
        "fulfillment_in_progress": False,
    }
    if generated_report_id:
        updates["generated_report_id"] = generated_report_id
    await db["orders_ledger"].update_one({"_id": order_id}, {"$set": updates})


async def _find_existing_brihat_report(order: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    context = order.get("order_context") or {}
    if not context:
        return None
    query = {
        "user_email": order.get("user_email", ""),
        "full_name": context.get("full_name"),
        "date_of_birth": context.get("date_of_birth"),
        "time_of_birth": context.get("time_of_birth"),
        "place_of_birth": context.get("place_of_birth"),
    }
    return await db.brihat_kundli_reports.find_one(query, {"_id": 0}, sort=[("generated_at", -1)])


def _gmail_client_config(redirect_uri: str) -> Dict[str, Any]:
    client_id = os.environ.get("GMAIL_CLIENT_ID", "")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET", "")
    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri],
        }
    }


def _build_gmail_redirect_uri(request: Request) -> str:
    return str(request.url_for("gmail_callback"))


async def _create_customer_gst_entry(order: Dict[str, Any]) -> Optional[str]:
    order_id = str(order.get("_id") or "")
    if not order_id:
        return None

    amount = round(float(order.get("amount_paise", 0)) / 100, 2)
    if amount <= 0:
        return None

    taxable = round(amount / 1.18, 2)
    context = order.get("order_context") or {}
    customer_state = (context.get("customer_state") or order.get("customer_state") or "OTHER").strip()
    business_state = (os.environ.get("BUSINESS_STATE", "Maharashtra") or "Maharashtra").strip()

    if customer_state and customer_state.lower() == business_state.lower():
        cgst = round(taxable * 0.09, 2)
        sgst = round(taxable * 0.09, 2)
        igst = 0.0
    else:
        cgst = 0.0
        sgst = 0.0
        igst = round(taxable * 0.18, 2)

    transaction_date = order.get("ts_fulfill_done") or order.get("ts_pmt_success") or utc_now()
    if isinstance(transaction_date, str):
        transaction_date = datetime.fromisoformat(transaction_date)
    if getattr(transaction_date, "tzinfo", None) is None:
        transaction_date = transaction_date.replace(tzinfo=timezone.utc)

    invoice_id = f"INV-{transaction_date.strftime('%Y%m%d')}-{order_id[:6].upper()}"
    entry = GSTLedgerEntry(
        _id=invoice_id,
        ledger_type="DEBIT_CUSTOMER_B2C",
        source_order_id=order_id,
        party_name=order.get("user_email", "Unknown"),
        transaction_date=transaction_date,
        taxable_value=taxable,
        cgst=cgst,
        sgst=sgst,
        igst=igst,
        total_invoice_value=amount,
        reconciliation_status="MATCHED",
        notes=order.get("report_type", ""),
    )
    await db["gst_recon_ledger"].update_one(
        {"source_order_id": order_id},
        {"$setOnInsert": entry.model_dump(by_alias=True, mode="json")},
        upsert=True,
    )
    return invoice_id


class SelfHealingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started_at = utc_now()
        user_id = await _resolve_request_user_id(request)
        try:
            response = await call_next(request)
            if response.status_code >= 400 and user_id:
                await _append_diagnostic_event(
                    user_id,
                    {
                        "page_url": str(request.url.path),
                        "event_type": f"API_ERROR_{response.status_code}",
                        "metadata": {
                            "method": request.method,
                            "latency_ms": round((utc_now() - started_at).total_seconds() * 1000, 2),
                        },
                    },
                )
            return response
        except Exception as exc:
            if user_id:
                await _append_diagnostic_event(
                    user_id,
                    {
                        "page_url": str(request.url.path),
                        "event_type": "CRITICAL_BACKEND_CRASH",
                        "metadata": {
                            "method": request.method,
                            "exception_class": exc.__class__.__name__,
                            "error_message": str(exc)[:500],
                        },
                    },
                )
            raise

# CORS must be added before other middleware
cors_origins_env = os.environ.get('CORS_ORIGINS', '')
if cors_origins_env:
    cors_origins = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]
else:
    cors_origins = []

if cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
else:
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

app.add_middleware(SessionUserMiddleware)
app.add_middleware(SelfHealingMiddleware)

api_router = APIRouter(prefix="/api")

ZODIAC_SIGNS = [
    {"id": "aries", "name": "Aries", "symbol": "\u2648", "dates": "Mar 21 - Apr 19", "element": "Fire"},
    {"id": "taurus", "name": "Taurus", "symbol": "\u2649", "dates": "Apr 20 - May 20", "element": "Earth"},
    {"id": "gemini", "name": "Gemini", "symbol": "\u264a", "dates": "May 21 - Jun 20", "element": "Air"},
    {"id": "cancer", "name": "Cancer", "symbol": "\u264b", "dates": "Jun 21 - Jul 22", "element": "Water"},
    {"id": "leo", "name": "Leo", "symbol": "\u264c", "dates": "Jul 23 - Aug 22", "element": "Fire"},
    {"id": "virgo", "name": "Virgo", "symbol": "\u264d", "dates": "Aug 23 - Sep 22", "element": "Earth"},
    {"id": "libra", "name": "Libra", "symbol": "\u264e", "dates": "Sep 23 - Oct 22", "element": "Air"},
    {"id": "scorpio", "name": "Scorpio", "symbol": "\u264f", "dates": "Oct 23 - Nov 21", "element": "Water"},
    {"id": "sagittarius", "name": "Sagittarius", "symbol": "\u2650", "dates": "Nov 22 - Dec 21", "element": "Fire"},
    {"id": "capricorn", "name": "Capricorn", "symbol": "\u2651", "dates": "Dec 22 - Jan 19", "element": "Earth"},
    {"id": "aquarius", "name": "Aquarius", "symbol": "\u2652", "dates": "Jan 20 - Feb 18", "element": "Air"},
    {"id": "pisces", "name": "Pisces", "symbol": "\u2653", "dates": "Feb 19 - Mar 20", "element": "Water"}
]

CELEBRITY_CATEGORY_LABELS = {
    "bollywood": "Bollywood",
    "politics": "Politics",
    "cricket": "Cricket",
    "business": "Business",
    "global": "Global",
    "spiritual": "Spiritual",
    "historical": "Historical",
}

CELEBRITY_DATA = [
    {"slug": "amitabh-bachchan", "name": "Amitabh Bachchan", "category": "bollywood", "dob": "1942-10-11", "tob": "16:00", "pob": "Allahabad, India", "lat": 25.4358, "lon": 81.8463, "tz": "Asia/Kolkata"},
    {"slug": "shah-rukh-khan", "name": "Shah Rukh Khan", "category": "bollywood", "dob": "1965-11-02", "tob": "02:00", "pob": "New Delhi, India", "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"slug": "deepika-padukone", "name": "Deepika Padukone", "category": "bollywood", "dob": "1986-01-05", "tob": "00:00", "pob": "Copenhagen, Denmark", "lat": 55.6761, "lon": 12.5683, "tz": "Europe/Copenhagen"},
    {"slug": "priyanka-chopra", "name": "Priyanka Chopra", "category": "bollywood", "dob": "1982-07-18", "tob": "10:00", "pob": "Jamshedpur, India", "lat": 22.8046, "lon": 86.2029, "tz": "Asia/Kolkata"},
    {"slug": "narendra-modi", "name": "Narendra Modi", "category": "politics", "dob": "1950-09-17", "tob": "11:00", "pob": "Vadnagar, India", "lat": 23.7869, "lon": 72.6394, "tz": "Asia/Kolkata"},
    {"slug": "rahul-gandhi", "name": "Rahul Gandhi", "category": "politics", "dob": "1970-06-19", "tob": "14:28", "pob": "New Delhi, India", "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"slug": "virat-kohli", "name": "Virat Kohli", "category": "cricket", "dob": "1988-11-05", "tob": "05:00", "pob": "New Delhi, India", "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"slug": "ms-dhoni", "name": "MS Dhoni", "category": "cricket", "dob": "1981-07-07", "tob": "02:30", "pob": "Ranchi, India", "lat": 23.3441, "lon": 85.3096, "tz": "Asia/Kolkata"},
    {"slug": "sachin-tendulkar", "name": "Sachin Tendulkar", "category": "cricket", "dob": "1973-04-24", "tob": "17:45", "pob": "Mumbai, India", "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    {"slug": "rohit-sharma", "name": "Rohit Sharma", "category": "cricket", "dob": "1987-04-30", "tob": "07:00", "pob": "Nagpur, India", "lat": 21.1458, "lon": 79.0882, "tz": "Asia/Kolkata"},
    {"slug": "mukesh-ambani", "name": "Mukesh Ambani", "category": "business", "dob": "1957-04-19", "tob": "06:00", "pob": "Aden, Yemen", "lat": 12.7855, "lon": 45.0187, "tz": "Asia/Aden"},
    {"slug": "ratan-tata", "name": "Ratan Tata", "category": "business", "dob": "1937-12-28", "tob": "06:30", "pob": "Mumbai, India", "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    {"slug": "elon-musk", "name": "Elon Musk", "category": "global", "dob": "1971-06-28", "tob": "07:30", "pob": "Pretoria, South Africa", "lat": -25.7479, "lon": 28.2293, "tz": "Africa/Johannesburg"},
    {"slug": "taylor-swift", "name": "Taylor Swift", "category": "global", "dob": "1989-12-13", "tob": "05:17", "pob": "West Reading, USA", "lat": 40.3362, "lon": -75.9471, "tz": "America/New_York"},
    {"slug": "cristiano-ronaldo", "name": "Cristiano Ronaldo", "category": "global", "dob": "1985-02-05", "tob": "05:25", "pob": "Funchal, Portugal", "lat": 32.6669, "lon": -16.9241, "tz": "Atlantic/Madeira"},
    {"slug": "sadhguru", "name": "Sadhguru", "category": "spiritual", "dob": "1957-09-03", "tob": "09:00", "pob": "Mysore, India", "lat": 12.2958, "lon": 76.6394, "tz": "Asia/Kolkata"},
    {"slug": "baba-ramdev", "name": "Baba Ramdev", "category": "spiritual", "dob": "1965-12-25", "tob": "06:00", "pob": "Mahendragarh, India", "lat": 28.2780, "lon": 76.1514, "tz": "Asia/Kolkata"},
    {"slug": "mahatma-gandhi", "name": "Mahatma Gandhi", "category": "historical", "dob": "1869-10-02", "tob": "07:35", "pob": "Porbandar, India", "lat": 21.6417, "lon": 69.6293, "tz": "Asia/Kolkata"},
    {"slug": "jawaharlal-nehru", "name": "Jawaharlal Nehru", "category": "historical", "dob": "1889-11-14", "tob": "23:15", "pob": "Allahabad, India", "lat": 25.4358, "lon": 81.8463, "tz": "Asia/Kolkata"},
    {"slug": "subhas-chandra-bose", "name": "Subhas Chandra Bose", "category": "historical", "dob": "1897-01-23", "tob": "12:15", "pob": "Cuttack, India", "lat": 20.4625, "lon": 85.8830, "tz": "Asia/Kolkata"},
]

CELEBRITY_INDEX = {item["slug"]: item for item in CELEBRITY_DATA}

HoroscopeType = Literal["daily", "tomorrow", "weekly", "monthly"]

def get_prediction_date(horoscope_type: str) -> str:
    today = date.today()
    if horoscope_type == "daily": return today.isoformat()
    elif horoscope_type == "tomorrow": return (today + timedelta(days=1)).isoformat()
    elif horoscope_type == "weekly": return (today - timedelta(days=today.weekday())).isoformat()
    elif horoscope_type == "monthly": return today.replace(day=1).isoformat()
    return today.isoformat()

# ── Models ────────────────────────────────────────────────────────────────────

class Horoscope(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sign: str
    type: HoroscopeType
    content: str
    prediction_date: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HoroscopeRequest(BaseModel):
    sign: str
    type: HoroscopeType

class ZodiacSign(BaseModel):
    id: str; name: str; symbol: str; dates: str; element: str

class BirthProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str; date_of_birth: str; time_of_birth: str; location: str; user_email: str = ""
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BirthProfileCreate(BaseModel):
    name: str; date_of_birth: str; time_of_birth: str; location: str
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None

class BirthChartReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: str; report_content: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lagna: dict = {}; moon_sign: dict = {}; nakshatra: dict = {}; current_dasha: dict = {}; chart_svg: str = ""; mangal_dosha: dict = {}
    planets: dict = {}; houses: dict = {}

class BirthChartRequest(BaseModel):
    profile_id: str

class BirthChartCalculationRequest(BaseModel):
    date_of_birth: str
    time_of_birth: str | None = None
    place_of_birth: str | None = None
    timezone: str | None = "Asia/Kolkata"

class CelebrityListItem(BaseModel):
    slug: str
    name: str
    category: str
    category_label: str
    dob: str
    tob: str
    pob: str
    birth_time_confirmed: bool = True

class CelebrityChartResponse(BaseModel):
    slug: str
    name: str
    category: str
    category_label: str
    dob: str
    tob: str
    pob: str
    tz: str
    lat: float
    lon: float
    birth_time_confirmed: bool = True
    cached: bool = False
    source: str = "vedic_calculator.py"
    chart_summary: dict = {}
    chart_svg: str = ""
    planet_positions: list = []
    dasha_timeline: list = []
    notable_yogas: list = []
    interpretation_note: str = ""
    generated_at: str = ""

class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str; slug: str; excerpt: str; content: str; author: str = "Cosmic Wisdom"; category: str = "Astrology"
    tags: list = []; featured_image: str = ""; video_url: str = ""; published: bool = False
    scheduled_at: Optional[datetime] = None; views: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogPostCreate(BaseModel):
    title: str; slug: str = ""; excerpt: str; content: str; author: str = "Cosmic Wisdom"; category: str = "Astrology"
    tags: list = []; featured_image: str = ""; video_url: str = ""; published: bool = False; scheduled_at: Optional[datetime] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None; slug: Optional[str] = None; excerpt: Optional[str] = None; content: Optional[str] = None
    author: Optional[str] = None; category: Optional[str] = None; tags: Optional[list] = None
    featured_image: Optional[str] = None; video_url: Optional[str] = None; published: Optional[bool] = None; scheduled_at: Optional[datetime] = None

class AdminReplyRequest(BaseModel):
    to_email: str; to_name: str; subject: str; message: str

class BrihatKundliRequest(BaseModel):
    full_name: str; date_of_birth: str; time_of_birth: str; place_of_birth: str; gender: str; current_city: str = ""; marital_status: str = ""

class BrihatKundliReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str; full_name: str; date_of_birth: str; time_of_birth: str; place_of_birth: str; gender: str
    ascendant: dict = {}; moon_sign: dict = {}; sun_sign: dict = {}; planetary_positions: list = []
    career_prediction: dict = {}; love_prediction: dict = {}; health_prediction: dict = {}; wealth_prediction: dict = {}
    family_prediction: dict = {}; education_prediction: dict = {}; current_dasha: dict = {}; dasha_timeline: list = []
    mangal_dosha: dict = {}; kalsarp_dosha: dict = {}; other_doshas: list = []; benefic_yogas: list = []; malefic_yogas: list = []
    gemstone_remedies: list = []; mantra_remedies: list = []; lifestyle_remedies: list = []; donation_remedies: list = []
    lucky_numbers: list = []; lucky_colors: list = []; lucky_days: list = []; lucky_direction: str = ""; numerology: dict = {}; chart_svg: str = ""
    knowledge_narratives: list = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KundaliMilanReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    person1_id: str; person2_id: str; compatibility_score: float; detailed_analysis: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ashtakoot_details: dict = {}; chart_svg_person1: str = ""; chart_svg_person2: str = ""

class KundaliMilanRequest(BaseModel):
    person1_id: str; person2_id: str

class UserSubscription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str; subscription_type: str; status: str
    stripe_subscription_id: Optional[str] = None; expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Payment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str; report_type: str; report_id: str; amount: float; razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None; status: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ShareLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    report_type: str; report_id: str; views: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactFormRequest(BaseModel):
    name: str; email: str; subject: str = ""; message: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str; new_password: str

class PaymentIntentRequest(BaseModel):
    report_type: str
    report_id: Optional[str] = None
    user_email: str
    order_context: Dict[str, Any] = Field(default_factory=dict)

# ── Notification / Subscriber Models ──────────────────────────────────────────

class Subscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None   # E.164 format for WhatsApp, e.g. +919876543210
    tags: List[str] = []          # e.g. ["premium", "panchang", "horoscope"]
    active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AddSubscriberRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: List[str] = []

class UpdateSubscriberRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: Optional[List[str]] = None
    active: Optional[bool] = None

class NotificationRequest(BaseModel):
    subject: str
    body: str                      # HTML content
    channels: List[str]            # ["email"] -- WhatsApp added when BSP is wired
    audience: str = "all"          # "all" | "tagged"
    tags: List[str] = []           # used when audience == "tagged"
    scheduled_at: Optional[str] = None  # ISO datetime; None = send immediately

class ScheduledNotification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str; body: str; channels: List[str]
    audience: str; tags: List[str]
    scheduled_at: str
    status: str = "pending"        # "pending" | "sent" | "cancelled"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class NotificationLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str; channel: str
    recipient_name: str
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None
    status: str = "pending"        # "sent" | "failed"
    error: Optional[str] = None
    notification_id: Optional[str] = None
    sent_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# ── WhatsApp Cloud API ────────────────────────────────────────────────────────

async def send_whatsapp_message(to_phone: str, message: str, recipient_name: str = "there") -> bool:
    """Send a free-form text message via WhatsApp Cloud API.
    Works for: replies within 24-hr window, or use template for outbound.
    For outbound notifications we use the 'everydayhoroscope_update' utility template.
    Falls back to hello_world template if custom template not approved yet."""
    phone_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
    token    = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
    if not phone_id or not token:
        logging.warning("WhatsApp credentials not configured")
        return False
    # Normalise phone: strip spaces/dashes, ensure no leading +
    to = to_phone.replace(" ", "").replace("-", "").lstrip("+")
    template_name = os.environ.get("WHATSAPP_TEMPLATE_NAME", "hello_world")
    template_lang = os.environ.get("WHATSAPP_TEMPLATE_LANG", "en_US")  # must match approved template lang
    # Build template payload -- hello_world has no variables; custom templates may add body params
    payload: dict = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": template_lang},
        }
    }
    # If using our custom template, inject named variables: {{customer_name}} and {{update_content}}
    if template_name != "hello_world":
        payload["template"]["components"] = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": recipient_name},   # {{customer_name}}
                    {"type": "text", "text": message[:1000]},   # {{update_content}}
                ]
            }
        ]
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                f"https://graph.facebook.com/v22.0/{phone_id}/messages",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=payload,
            )
        data = r.json()
        if data.get("messages"):
            logging.info("WhatsApp sent to %s: %s", to, data["messages"][0].get("id"))
            return True
        err = data.get("error", {}).get("message", str(data))
        logging.error("WhatsApp send failed to %s: %s", to, err)
        return False
    except Exception as e:
        logging.error("WhatsApp exception for %s: %s", to, e)
        return False

# ── Email ─────────────────────────────────────────────────────────────────────

def _branded_email(recipient_name: str, body_html: str) -> str:
    """Wraps any HTML body in the EverydayHoroscope branded email template."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f1eb;font-family:Georgia,'Times New Roman',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f1eb;padding:32px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#0e0c18;border-radius:12px;overflow:hidden;border:1px solid #2a2440;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#1b1530 0%,#0e0c18 100%);padding:32px 40px;text-align:center;border-bottom:1px solid #C5A05933;">
            <p style="margin:0 0 6px;color:#C5A059;font-size:11px;letter-spacing:5px;text-transform:uppercase;">✦ EverydayHoroscope.in ✦</p>
            <h1 style="margin:0;color:#f5f0e8;font-size:26px;font-weight:700;letter-spacing:0.5px;">Everyday Horoscope</h1>
            <p style="margin:6px 0 0;color:#C5A059aa;font-size:12px;">India's Premium Vedic Astrology Platform</p>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding:28px 40px 0;color:#f5f0e8;">
            <p style="margin:0;font-size:15px;color:#C5A059aa;">Namaste,</p>
            <p style="margin:4px 0 0;font-size:18px;font-weight:600;color:#f5f0e8;">{recipient_name} 🙏</p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:16px 40px;">
            <div style="height:1px;background:linear-gradient(90deg,transparent,#C5A05955,transparent);"></div>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:0 40px 28px;color:#e8e0d0;font-size:15px;line-height:1.8;">
            {body_html}
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:0 40px;">
            <div style="height:1px;background:linear-gradient(90deg,transparent,#C5A05955,transparent);"></div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:20px 40px 28px;text-align:center;">
            <p style="margin:0 0 4px;color:#C5A059;font-size:13px;font-weight:600;letter-spacing:1px;">everydayhoroscope.in</p>
            <p style="margin:0;color:#6b6480;font-size:11px;">SkyHound Studios · Delhi, India</p>
            <p style="margin:8px 0 0;color:#4a4460;font-size:10px;">You're receiving this because you subscribed to EverydayHoroscope updates.</p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""

async def send_email_notification(to_email: str, subject: str, body: str):
    resend_api_key = os.environ.get('RESEND_API_KEY', '')
    from_email = os.environ.get('FROM_EMAIL', 'noreply@everydayhoroscope.in')
    if not resend_api_key:
        logging.info("[EMAIL NOT SENT] To: %s | Subject: %s", to_email, subject)
        return False
    try:
        async with httpx.AsyncClient() as http:
            response = await http.post("https://api.resend.com/emails", headers={"Authorization": "Bearer " + resend_api_key, "Content-Type": "application/json"}, json={"from": "Everyday Horoscope <" + from_email + ">", "to": [to_email], "subject": subject, "html": body})
            if response.status_code == 200: logging.info("Email sent to %s: %s", to_email, subject); return True
            else: logging.error("Resend error %s: %s", response.status_code, response.text); return False
    except Exception as e:
        logging.error("Email send failed: %s", str(e)); return False

# ── Horoscope LLM ─────────────────────────────────────────────────────────────

async def generate_horoscope_with_llm(sign: str, horoscope_type: str) -> str:
    sign_dash = sign + " \u2014"
    daily_prompt = ("You are a Vedic astrologer specialising in Jyotish. Generate a daily horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence of overall energy.\n2. Output EXACTLY these 4 sections with EXACTLY these headings on their own line:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Lucky Number: [number], Lucky Colour: [colour], Lucky Time: [time]\n4. NO markdown (no **, no ##, no ---)\n5. Each section: 2-3 sentences. Total 120-150 words.\n6. Begin with: \"" + sign_dash + "\" as the very first word.")
    tomorrow_prompt = ("You are a Vedic astrologer specialising in Jyotish. Generate a tomorrow's horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence of tomorrow's overall energy.\n2. Output EXACTLY these 4 sections with EXACTLY these headings on their own line:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Lucky Number: [number], Lucky Colour: [colour], Lucky Time: [time]\n4. NO markdown (no **, no ##, no ---)\n5. Each section: 2-3 sentences. Total 120-150 words.\n6. Begin with: \"" + sign_dash + "\"")
    weekly_prompt = ("You are a Vedic astrologer. Generate a weekly horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence summarising the week.\n2. Output EXACTLY these 4 sections:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Lucky Days: [days], Lucky Colour: [colour], Focus Mantra: [mantra]\n4. NO markdown\n5. Each section: 3-4 sentences. Total 180-220 words.\n6. Begin with: \"" + sign_dash + "\"")
    monthly_prompt = ("You are a Vedic astrologer. Generate a monthly horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence summarising the month.\n2. Output EXACTLY these 4 sections:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Power Dates: [3 dates], Lucky Gemstone: [stone], Monthly Mantra: [mantra]\n4. NO markdown\n5. Each section: 4-5 sentences. Total 250-300 words.\n6. Begin with: \"" + sign_dash + "\"")
    system_prompts = {"daily": daily_prompt, "tomorrow": tomorrow_prompt, "weekly": weekly_prompt, "monthly": monthly_prompt}
    user_prompts = {"daily": "Generate today's Vedic horoscope for " + sign + ".", "tomorrow": "Generate tomorrow's Vedic horoscope for " + sign + ".", "weekly": "Generate this week's Vedic horoscope for " + sign + ".", "monthly": "Generate this month's Vedic horoscope for " + sign + "."}
    try:
        llm = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = llm.messages.create(model="claude-sonnet-4-20250514", max_tokens=1024, system=system_prompts[horoscope_type], messages=[{"role": "user", "content": user_prompts[horoscope_type]}])
        return message.content[0].text
    except Exception as e:
        logging.error("Error generating horoscope: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate horoscope: " + str(e))

# ── Routes ────────────────────────────────────────────────────────────────────

@api_router.get("/")
async def root(): return {"message": "Daily Horoscope API"}

@api_router.get("/health")
async def health_check(): return {"status": "ok"}

@api_router.get("/signs", response_model=List[ZodiacSign])
async def get_zodiac_signs(): return ZODIAC_SIGNS

@api_router.post("/horoscope/generate", response_model=Horoscope)
async def generate_horoscope(request: HoroscopeRequest):
    valid_signs = [sign["id"] for sign in ZODIAC_SIGNS]
    if request.sign not in valid_signs: raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    prediction_date = get_prediction_date(request.type)
    existing = await db.horoscopes.find_one({"sign": request.sign, "type": request.type, "prediction_date": prediction_date}, {"_id": 0})
    if existing:
        if isinstance(existing['created_at'], str): existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return Horoscope(**existing)
    content = await generate_horoscope_with_llm(request.sign, request.type)
    horoscope = Horoscope(sign=request.sign, type=request.type, content=content, prediction_date=prediction_date)
    await db.horoscopes.insert_one(horoscope.model_dump(mode='json'))
    return horoscope

@api_router.get("/horoscope/prefetch-status")
async def prefetch_status():
    daily_date = get_prediction_date('daily'); tomorrow_date = get_prediction_date('tomorrow'); weekly_date = get_prediction_date('weekly'); monthly_date = get_prediction_date('monthly')
    daily_count = await db.horoscopes.count_documents({'type': 'daily', 'prediction_date': daily_date})
    tomorrow_count = await db.horoscopes.count_documents({'type': 'tomorrow', 'prediction_date': tomorrow_date})
    weekly_count = await db.horoscopes.count_documents({'type': 'weekly', 'prediction_date': weekly_date})
    monthly_count = await db.horoscopes.count_documents({'type': 'monthly', 'prediction_date': monthly_date})
    return {'daily': {'cached': daily_count, 'total': 12, 'date': daily_date}, 'tomorrow': {'cached': tomorrow_count, 'total': 12, 'date': tomorrow_date}, 'weekly': {'cached': weekly_count, 'total': 12, 'date': weekly_date}, 'monthly': {'cached': monthly_count, 'total': 12, 'date': monthly_date}, 'total_cached': daily_count + tomorrow_count + weekly_count + monthly_count}

@api_router.get("/horoscope/{sign}/{type}", response_model=Horoscope)
async def get_horoscope(sign: str, type: HoroscopeType):
    valid_signs = [s["id"] for s in ZODIAC_SIGNS]
    if sign not in valid_signs: raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    prediction_date = get_prediction_date(type)
    horoscope_doc = await db.horoscopes.find_one({"sign": sign, "type": type, "prediction_date": prediction_date}, {"_id": 0})
    if horoscope_doc:
        if isinstance(horoscope_doc['created_at'], str): horoscope_doc['created_at'] = datetime.fromisoformat(horoscope_doc['created_at'])
        return Horoscope(**horoscope_doc)
    content = await generate_horoscope_with_llm(sign, type)
    horoscope = Horoscope(sign=sign, type=type, content=content, prediction_date=prediction_date)
    await db.horoscopes.insert_one(horoscope.model_dump(mode='json'))
    return horoscope

@api_router.post("/profile/birth", response_model=BirthProfile)
async def create_birth_profile(profile: BirthProfileCreate, request: Request):
    profile_data = profile.model_dump(mode='json')
    try:
        user = await get_current_user(request, db)
        if user and user.get("email"): profile_data["user_email"] = user["email"]
    except Exception: pass
    birth_profile = BirthProfile(**profile_data)
    await db.birth_profiles.insert_one(birth_profile.model_dump(mode='json'))
    return birth_profile

@api_router.get("/profile/birth/{profile_id}", response_model=BirthProfile)
async def get_birth_profile(profile_id: str):
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    if not profile: raise HTTPException(status_code=404, detail="Birth profile not found")
    if isinstance(profile['created_at'], str): profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    return BirthProfile(**profile)

@api_router.get("/profile/birth", response_model=List[BirthProfile])
async def list_birth_profiles():
    profiles = await db.birth_profiles.find({}, {"_id": 0}).to_list(1000)
    for p in profiles:
        if isinstance(p['created_at'], str): p['created_at'] = datetime.fromisoformat(p['created_at'])
    return profiles

def _resolve_birth_timezone_offset(date_of_birth: str, time_of_birth: str, timezone_value: str | None) -> str:
    tz_name = (timezone_value or "Asia/Kolkata").strip()
    if len(tz_name) == 6 and tz_name[0] in {"+", "-"} and tz_name[3] == ":":
        return tz_name
    try:
        naive_dt = datetime.strptime(f"{date_of_birth} {time_of_birth}", "%Y-%m-%d %H:%M")
        offset = naive_dt.replace(tzinfo=ZoneInfo(tz_name)).utcoffset() or timedelta()
        total_minutes = int(offset.total_seconds() // 60)
        sign = "+" if total_minutes >= 0 else "-"
        total_minutes = abs(total_minutes)
        hours, minutes = divmod(total_minutes, 60)
        return f"{sign}{hours:02d}:{minutes:02d}"
    except Exception:
        logging.warning("Falling back to IST offset for timezone value: %s", tz_name)
        return "+05:30"

def _planet_plain_name(label: str) -> str:
    return label.split("(")[0].strip()

def _format_planet_status(planet_data: dict) -> str:
    parts: list[str] = []
    dignity = str(planet_data.get("dignity") or "").replace("_", " ").strip()
    if dignity:
        parts.append(dignity.title())
    if planet_data.get("retrograde"):
        parts.append("Retrograde")
    if planet_data.get("combust"):
        parts.append("Combust")
    return ", ".join(parts) if parts else "Neutral"

def _build_notable_yogas(chart_data: dict) -> list[dict]:
    planets = chart_data.get("planets", {})
    highlights: list[dict] = []

    exalted = [name for name, data in planets.items() if data.get("dignity") == "exalted"]
    own_sign = [name for name, data in planets.items() if data.get("dignity") in {"own_sign", "moolatrikona"}]
    retrograde = [name for name, data in planets.items() if data.get("retrograde")]
    combust = [name for name, data in planets.items() if data.get("combust")]
    mangal = chart_data.get("mangal_dosha", {})

    if exalted:
        highlights.append({
            "name": "Exalted Planet Strength",
            "detail": ", ".join(_planet_plain_name(name) for name in exalted[:3]) + " shows exalted dignity in this chart.",
        })
    if own_sign:
        highlights.append({
            "name": "Own-Sign Support",
            "detail": ", ".join(_planet_plain_name(name) for name in own_sign[:3]) + " occupies an especially supportive dignity placement.",
        })
    if retrograde:
        highlights.append({
            "name": "Retrograde Focus",
            "detail": ", ".join(_planet_plain_name(name) for name in retrograde[:3]) + " adds reflective or intensified karmic themes.",
        })
    if combust:
        highlights.append({
            "name": "Combustion Note",
            "detail": ", ".join(_planet_plain_name(name) for name in combust[:3]) + " is close to the Sun, which can modify its expression.",
        })
    if mangal.get("has_dosha"):
        highlights.append({
            "name": "Mangal Dosha Signature",
            "detail": mangal.get("description") or "Mars creates a classic Mangal Dosha pattern in this chart.",
        })

    if not highlights:
        nakshatra = chart_data.get("nakshatra", {})
        moon_sign = chart_data.get("moon_sign", {})
        highlights.append({
            "name": "Nakshatra Emphasis",
            "detail": f"{nakshatra.get('name', 'The Moon')} in {moon_sign.get('sign', 'its sign')} shapes the strongest public-facing emotional signature here.",
        })

    return highlights[:4]

def _build_celebrity_list_item(celebrity: dict) -> dict:
    return CelebrityListItem(
        slug=celebrity["slug"],
        name=celebrity["name"],
        category=celebrity["category"],
        category_label=CELEBRITY_CATEGORY_LABELS.get(celebrity["category"], celebrity["category"].title()),
        dob=celebrity["dob"],
        tob=celebrity["tob"],
        pob=celebrity["pob"],
        birth_time_confirmed=celebrity["tob"] != "00:00",
    ).model_dump(mode="json")

def _compute_celebrity_chart_payload(celebrity: dict) -> dict:
    time_confirmed = celebrity["tob"] != "00:00"
    chart_time = celebrity["tob"] if time_confirmed else "12:00"
    timezone_offset = _resolve_birth_timezone_offset(celebrity["dob"], chart_time, celebrity["tz"])

    original_geocode = vedic_calculator_module.geocode_place
    vedic_calculator_module.geocode_place = lambda _place: (celebrity["lat"], celebrity["lon"])
    try:
        chart_data = calculate_vedic_chart(
            date_of_birth=celebrity["dob"],
            time_of_birth=chart_time,
            place_of_birth=celebrity["pob"],
            timezone_offset=timezone_offset,
        )
    finally:
        vedic_calculator_module.geocode_place = original_geocode

    moon_longitude = chart_data.get("moon_longitude")
    dasha_timeline = build_dasha_timeline(celebrity["dob"], moon_longitude) if moon_longitude else []
    lagna = chart_data.get("lagna", {}) if time_confirmed else {}
    houses = chart_data.get("houses", {}) if time_confirmed else {}
    chart_svg = ""
    if time_confirmed and houses and lagna.get("sign"):
        try:
            chart_svg = generate_north_indian_chart_svg(houses, lagna["sign"])
        except Exception as exc:
            logging.warning("Celebrity chart SVG generation failed for %s: %s", celebrity["slug"], exc)

    sun_data = chart_data.get("planets", {}).get("Sun (Surya)", {})
    moon_sign = chart_data.get("moon_sign", {})
    nakshatra = chart_data.get("nakshatra", {})
    current_dasha = chart_data.get("current_dasha", {})
    planet_positions = []
    for planet_name, planet_data in chart_data.get("planets", {}).items():
        planet_positions.append({
            "planet": _planet_plain_name(planet_name),
            "sign": planet_data.get("sign", ""),
            "sign_vedic": planet_data.get("sign_vedic", planet_data.get("sign", "")),
            "house": planet_data.get("house") if time_confirmed else None,
            "degree": planet_data.get("degree"),
            "status": _format_planet_status(planet_data),
        })

    planet_positions.sort(key=lambda item: item["planet"])
    interpretation_note = (
        "This chart is computed using Vedic astrology (KP Ayanamsha, Placidus houses). "
        "Time of birth accuracy affects house positions."
    )
    if not time_confirmed:
        interpretation_note = (
            "Time of birth is not confirmed for this celebrity. Lagna and house positions are intentionally omitted, "
            "while sign-based chart factors are shown from a neutral midday reference."
        )

    return CelebrityChartResponse(
        slug=celebrity["slug"],
        name=celebrity["name"],
        category=celebrity["category"],
        category_label=CELEBRITY_CATEGORY_LABELS.get(celebrity["category"], celebrity["category"].title()),
        dob=celebrity["dob"],
        tob=celebrity["tob"],
        pob=celebrity["pob"],
        tz=celebrity["tz"],
        lat=celebrity["lat"],
        lon=celebrity["lon"],
        birth_time_confirmed=time_confirmed,
        cached=False,
        source="vedic_calculator.py",
        chart_summary={
            "lagna": lagna,
            "moon_sign": moon_sign,
            "sun_sign": {
                "sign": sun_data.get("sign", ""),
                "sign_vedic": sun_data.get("sign_vedic", sun_data.get("sign", "")),
            },
            "nakshatra": nakshatra,
            "current_dasha": current_dasha,
            "mangal_dosha": chart_data.get("mangal_dosha", {}),
        },
        chart_svg=chart_svg,
        planet_positions=planet_positions,
        dasha_timeline=dasha_timeline,
        notable_yogas=_build_notable_yogas(chart_data),
        interpretation_note=interpretation_note,
        generated_at=datetime.now(timezone.utc).isoformat(),
    ).model_dump(mode="json")

@api_router.post("/calculate-birth-chart")
async def calculate_birth_chart_public(payload: BirthChartCalculationRequest):
    birth_time = (payload.time_of_birth or "12:00").strip() or "12:00"
    birth_place = (payload.place_of_birth or "New Delhi").strip() or "New Delhi"
    timezone_offset = _resolve_birth_timezone_offset(
        payload.date_of_birth,
        birth_time,
        payload.timezone,
    )

    try:
        chart_data = calculate_vedic_chart(
            date_of_birth=payload.date_of_birth,
            time_of_birth=birth_time,
            place_of_birth=birth_place,
            timezone_offset=timezone_offset,
        )
    except Exception as exc:
        logging.error("Public calculator birth chart failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to calculate the birth chart right now.")

    moon_sign = chart_data.get("moon_sign", {})
    sign_name = moon_sign.get("sign", "")
    moon_longitude = chart_data.get("moon_longitude")
    moon_degree = round(float(moon_longitude) % 30, 2) if isinstance(moon_longitude, (int, float)) else None
    nakshatra = chart_data.get("nakshatra", {})

    return {
        "moon_sign": sign_name,
        "moon_sign_vedic": moon_sign.get("sign_vedic", sign_name),
        "moon_sign_lord": SIGN_LORDS.get(sign_name, ""),
        "moon_degree": moon_degree,
        "moon_nakshatra": nakshatra.get("name", ""),
        "moon_nakshatra_lord": nakshatra.get("lord", ""),
        "moon_nakshatra_pada": nakshatra.get("pada"),
        "current_dasha": chart_data.get("current_dasha", {}),
        "birth_details": chart_data.get("birth_details", {}),
        "chart": {
            "moon_sign": moon_sign,
            "nakshatra": nakshatra,
            "moon_longitude": moon_longitude,
        },
        "source": "vedic_calculator.py",
    }


@api_router.post("/love-calculator", response_model=LoveCalculatorResponse)
async def love_calculator_public(payload: LoveCalculatorRequest) -> LoveCalculatorResponse:
    return await love_calculator(payload)

@api_router.get("/celebrities", response_model=List[CelebrityListItem])
async def get_celebrities():
    return [_build_celebrity_list_item(item) for item in CELEBRITY_DATA]

@api_router.get("/celebrities/{slug}", response_model=CelebrityChartResponse)
async def get_celebrity_chart(slug: str):
    celebrity = CELEBRITY_INDEX.get(slug)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Celebrity not found")

    cached_doc = await db.celebrities.find_one({"slug": slug}, {"_id": 0})
    if cached_doc:
        cached_doc["cached"] = True
        return CelebrityChartResponse(**cached_doc)

    try:
        payload = _compute_celebrity_chart_payload(celebrity)
    except Exception as exc:
        logging.error("Celebrity chart generation failed for %s: %s", slug, exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to load the celebrity chart right now.")

    await db.celebrities.update_one(
        {"slug": slug},
        {"$set": payload},
        upsert=True,
    )
    return CelebrityChartResponse(**payload)

async def generate_birth_chart_with_llm(profile: BirthProfile) -> str:
    try:
        chart_data = calculate_vedic_chart(date_of_birth=profile.date_of_birth, time_of_birth=profile.time_of_birth, place_of_birth=profile.location)
    except Exception as e:
        logging.error("Vedic calculator FAILED: %s", e, exc_info=True); chart_data = None
    if chart_data:
        lagna = chart_data['lagna']; moon = chart_data['moon_sign']; nak = chart_data['nakshatra']
        current_dasha = chart_data.get('current_dasha', {}); mangal = chart_data['mangal_dosha']
        planet_lines = ["  - " + pname + ": " + pdata['sign_vedic'] + ", House " + str(pdata['house']) + ", " + str(pdata['degree']) + "\u00b0" + (" (Retrograde)" if pdata.get('retrograde') else "") for pname, pdata in chart_data['planets'].items()]
        house_lines = ["  House " + str(h_num) + " \u2014 " + h_data['name'] + ": " + h_data['sign_vedic'] + " (Lord: " + h_data['lord'] + ") | Planets: " + (', '.join(h_data['planets']) if h_data['planets'] else 'Empty') for h_num, h_data in chart_data['houses'].items()]
        chart_summary = "\nCALCULATED BIRTH CHART DATA (mathematically verified):\n\nNative: " + profile.name + "\nBirth: " + profile.date_of_birth + " at " + profile.time_of_birth + ", " + profile.location + "\n\nASCENDANT (Lagna): " + lagna['sign_vedic'] + ", " + str(lagna['degree']) + "\u00b0\n  Lagna Lord: " + lagna['lord'] + " | Element: " + lagna['element'] + "\n\nMOON SIGN (Rashi): " + moon['sign_vedic'] + "\nNAKSHATRA: " + nak['name'] + " (Pada " + str(nak.get('pada', '?')) + ") | Lord: " + str(nak.get('lord', '?')) + "\n\nPLANETARY POSITIONS:\n" + "\n".join(planet_lines) + "\n\n12-HOUSE MAP:\n" + "\n".join(house_lines) + "\n\nCURRENT DASHA: " + str(current_dasha.get('planet', 'Unknown')) + " Mahadasha\n  Period: " + str(current_dasha.get('start', '?')) + " to " + str(current_dasha.get('end', '?')) + "\n\nMANGAL DOSHA: " + ("YES" if mangal.get('has_dosha') else "NO") + "\n  " + str(mangal.get('description', '')) + "\n  Mars in House: " + str(mangal.get('mars_house', '?')) + "\n"
    else:
        chart_summary = "Native: " + profile.name + ", Born: " + profile.date_of_birth + " at " + profile.time_of_birth + " in " + profile.location
    system_prompt = "You are an expert Jyotish (Vedic astrology) interpreter. Receive a mathematically calculated birth chart and interpret it.\n\nCRITICAL RULES:\n- Use ONLY the planetary positions provided\n- Every sentence must reference specific planets AND house numbers\n- NO markdown\n- MANDATORY SECTIONS IN ORDER:\n  Overview:\n  Ascendant & Personality:\n  Sun Sign & Core Identity:\n  Moon Sign & Emotional Nature:\n  Planetary Positions & House Analysis:\n  Notable Yogas & Planetary Combinations:\n  Career & Dharma:\n  Relationships & Marriage:\n  Health & Wellness:\n  Dasha Period Analysis:\n  Remedies & Guidance:\n- Each section: 3-4 sentences. Target 800-1000 words total."
    user_prompt = "Write the complete Janma Kundali report for " + profile.name + " using ONLY the calculated data below.\n\n" + chart_summary + "\n\nEvery section must cite specific planets with house numbers."
    try:
        llm = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = llm.messages.create(model="claude-sonnet-4-20250514", max_tokens=2048, system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
        return message.content[0].text
    except Exception as e:
        logging.error("Error generating birth chart: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate birth chart: " + str(e))

@api_router.post("/birthchart/generate", response_model=BirthChartReport)
async def generate_birth_chart(request: BirthChartRequest):
    profile = await db.birth_profiles.find_one({"id": request.profile_id}, {"_id": 0})
    if not profile: raise HTTPException(status_code=404, detail="Birth profile not found")
    if isinstance(profile['created_at'], str): profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    birth_profile = BirthProfile(**profile)
    existing = await db.birth_chart_reports.find_one({"profile_id": request.profile_id}, {"_id": 0})
    if existing:
        needs_structured_backfill = not existing.get("planets") or not existing.get("houses")
        if needs_structured_backfill:
            bc_chart_data = None
            try:
                bc_chart_data = calculate_vedic_chart(
                    date_of_birth=birth_profile.date_of_birth,
                    time_of_birth=birth_profile.time_of_birth,
                    place_of_birth=birth_profile.location,
                )
            except Exception as ce:
                logging.warning("Birth chart structured backfill failed: %s", ce)
            if bc_chart_data:
                bc_chart_svg = existing.get("chart_svg", "")
                if not bc_chart_svg and bc_chart_data.get("houses"):
                    try:
                        bc_chart_svg = generate_north_indian_chart_svg(
                            bc_chart_data["houses"],
                            bc_chart_data["lagna"]["sign"],
                        )
                    except Exception as se:
                        logging.warning("Birth chart backfill SVG generation failed: %s", se)
                backfill = {
                    "lagna": bc_chart_data.get("lagna", {}),
                    "moon_sign": bc_chart_data.get("moon_sign", {}),
                    "nakshatra": bc_chart_data.get("nakshatra", {}),
                    "current_dasha": bc_chart_data.get("current_dasha", {}),
                    "mangal_dosha": bc_chart_data.get("mangal_dosha", {}),
                    "planets": bc_chart_data.get("planets", {}),
                    "houses": bc_chart_data.get("houses", {}),
                    "chart_svg": bc_chart_svg,
                }
                existing.update(backfill)
                await db.birth_chart_reports.update_one(
                    {"profile_id": request.profile_id},
                    {"$set": backfill},
                )
        if isinstance(existing['generated_at'], str): existing['generated_at'] = datetime.fromisoformat(existing['generated_at'])
        return BirthChartReport(**existing)
    content = await generate_birth_chart_with_llm(birth_profile)
    bc_chart_data = None
    try: bc_chart_data = calculate_vedic_chart(date_of_birth=birth_profile.date_of_birth, time_of_birth=birth_profile.time_of_birth, place_of_birth=birth_profile.location)
    except Exception as ce: logging.warning("Chart calc for structured fields: %s", ce)
    bc_chart_svg = ""
    if bc_chart_data and bc_chart_data.get('houses'):
        try: bc_chart_svg = generate_north_indian_chart_svg(bc_chart_data['houses'], bc_chart_data['lagna']['sign'])
        except Exception as se: logging.warning("SVG generation failed: %s", se)
    report = BirthChartReport(profile_id=request.profile_id, report_content=content, lagna=bc_chart_data['lagna'] if bc_chart_data else {}, moon_sign=bc_chart_data['moon_sign'] if bc_chart_data else {}, nakshatra=bc_chart_data['nakshatra'] if bc_chart_data else {}, current_dasha=bc_chart_data.get('current_dasha', {}) if bc_chart_data else {}, mangal_dosha=bc_chart_data.get('mangal_dosha', {}) if bc_chart_data else {}, planets=bc_chart_data.get('planets', {}) if bc_chart_data else {}, houses=bc_chart_data.get('houses', {}) if bc_chart_data else {}, chart_svg=bc_chart_svg)
    import json as _json
    doc = _json.loads(report.model_dump_json())
    await db.birth_chart_reports.insert_one({**doc})
    return report

@api_router.get("/birthchart/{profile_id}", response_model=BirthChartReport)
async def get_birth_chart(profile_id: str):
    report = await db.birth_chart_reports.find_one({"profile_id": profile_id}, {"_id": 0})
    if not report: raise HTTPException(status_code=404, detail="Birth chart report not found")
    if isinstance(report['generated_at'], str): report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    return BirthChartReport(**report)

async def _brihat_ke_pipeline(chart_data: dict, engine) -> list:
    """
    Run scan_chart() + generate_narrative() for the Brihat Kundali report.
    Returns a list of plain dicts (one per Arc Angel domain matched).
    Returns [] on any failure - never raises.
    """
    try:
        raw_planets = chart_data.get("planets") or {}
        ke_planets = {
            pname: {**pdata, "sign": pdata.get("sign") or pdata.get("sign_vedic")}
            for pname, pdata in raw_planets.items()
        }
        ke_chart = {**chart_data, "planets": ke_planets}

        matched_rules = await engine.scan_chart(
            ke_chart,
            categories=["career", "wealth", "relationships", "health"],
            max_rules=30,
        )
        if not matched_rules:
            return []

        narrative_response = await engine.generate_narrative(
            matched_rules=matched_rules,
            chart=ke_chart,
            context={"backbone_science_id": "vedic_astrology"},
        )
        narratives = narrative_response.narratives or []
        return [
            narrative.model_dump() if hasattr(narrative, "model_dump") else dict(narrative)
            for narrative in narratives
        ]
    except Exception as ke_err:
        logging.warning("Knowledge Engine pipeline failed for Brihat Kundali: %s", ke_err)
        return []

async def generate_brihat_kundli_with_llm(request: BrihatKundliRequest) -> dict:
    current_year = datetime.now().year
    birth_year = int(request.date_of_birth.split('-')[0])
    age = current_year - birth_year
    chart_data = None
    try: chart_data = calculate_vedic_chart(date_of_birth=request.date_of_birth, time_of_birth=request.time_of_birth, place_of_birth=request.place_of_birth)
    except Exception as e: logging.warning("Vedic calculator failed for Brihat Kundli: %s", e)
    if chart_data:
        lagna = chart_data['lagna']; moon = chart_data['moon_sign']; nak = chart_data['nakshatra']
        current_dasha = chart_data.get('current_dasha', {}); mangal = chart_data['mangal_dosha']
        planet_lines = ["  " + pname + ": " + pdata['sign_vedic'] + " | House " + str(pdata['house']) + " | " + str(pdata['degree']) + "\u00b0" + (" (R)" if pdata.get('retrograde') else "") + " | Lord: " + str(pdata['lord_of_sign']) for pname, pdata in chart_data['planets'].items()]
        house_lines = ["  H" + str(h_num) + " " + h_data['name'] + ": " + h_data['sign_vedic'] + " | Lord: " + h_data['lord'] + " | " + (', '.join(h_data['planets']) if h_data['planets'] else 'Empty') for h_num, h_data in chart_data['houses'].items()]
        dasha_lines = ["  " + str(d.get('planet', '?')) + " Mahadasha: " + str(d.get('start', '?')) + " \u2014 " + str(d.get('end', '?')) + " (" + str(round(d.get('years', 0), 1)) + " yrs)" for d in chart_data['dashas'][:6]]
        chart_summary = "\nCALCULATED BIRTH CHART:\n\nNative: " + request.full_name + ", Age: " + str(age) + ", Gender: " + request.gender + "\nBorn: " + request.date_of_birth + " at " + request.time_of_birth + ", " + request.place_of_birth + "\n\nLAGNA: " + lagna['sign_vedic'] + " " + str(lagna['degree']) + "\u00b0 | Lord: " + lagna['lord'] + " | Element: " + lagna['element'] + "\nMOON (Rashi): " + moon['sign_vedic'] + "\nNAKSHATRA: " + nak['name'] + " Pada " + str(nak.get('pada', '?')) + " | Lord: " + str(nak.get('lord', '?')) + "\n\nPLANET POSITIONS:\n" + "\n".join(planet_lines) + "\n\n12-HOUSE MAP:\n" + "\n".join(house_lines) + "\n\nVIMSHOTTARI DASHA TIMELINE:\n" + "\n".join(dasha_lines) + "\nCurrent: " + str(current_dasha.get('planet', 'Unknown')) + " Mahadasha (" + str(current_dasha.get('start', '?')) + "-" + str(current_dasha.get('end', '?')) + ")\n\nMANGAL DOSHA: " + ("YES" if mangal.get('has_dosha') else "NO") + "\n  House: " + str(mangal.get('mars_house', '?')) + " | " + str(mangal.get('description', '')) + "\n"
    else:
        chart_summary = "Native: " + request.full_name + ", Born " + request.date_of_birth + " at " + request.time_of_birth + " in " + request.place_of_birth
    system_prompt = ("You are a senior Jyotish astrologer writing a premium Brihat Kundli Pro report. You receive a mathematically calculated birth chart. Interpret ONLY - never recalculate.\n\nRules:\n- Return ONLY valid JSON, no markdown fences, no preamble\n- Use specific calendar years (current year is " + str(current_year) + ")\n- Address native by first name throughout\n- Complete ALL fields - do not omit any keys\n- Plain text only in JSON values, no markdown\n\nReturn this exact JSON structure:\n{\n    \"ascendant\": {\"sign\": \"\", \"degree\": \"\", \"lord\": \"\", \"element\": \"\", \"overview\": \"3 sentences.\", \"key_traits\": [\"...x5\"], \"strengths\": [\"...x5\"], \"challenges\": [\"...x5\"]},\n    \"moon_sign\": {\"sign\": \"\", \"nakshatra\": \"\", \"nakshatra_pada\": \"\", \"nakshatra_lord\": \"\", \"overview\": \"3 sentences.\", \"emotional_nature\": [\"...x5\"], \"mental_tendencies\": [\"...x5\"]},\n    \"sun_sign\": {\"sign\": \"\", \"overview\": \"2 sentences.\", \"core_identity\": [\"...x4\"], \"life_purpose\": [\"...x4\"]},\n    \"planetary_positions\": [{\"planet\": \"\", \"sign\": \"\", \"house\": 1, \"degree\": \"\", \"status\": \"\", \"strength\": \"\", \"effects\": [\"effect1\", \"effect2\"]}],\n    \"career_prediction\": {\"overall_rating\": \"\", \"business_potential\": \"\", \"overview\": \"3 sentences.\", \"best_career_fields\": [\"...x5\"], \"strengths_at_work\": [\"...x5\"], \"career_timeline\": [{\"period\": \"2026-2030\", \"prediction\": \"2 sentences.\", \"advice\": \"1 sentence.\"}]},\n    \"love_prediction\": {\"overall_rating\": \"\", \"overview\": \"3 sentences.\", \"ideal_partner_traits\": [\"...x5\"], \"compatibility_signs\": [\"\",\"\",\"\"], \"challenging_signs\": [\"\",\"\",\"\"], \"marriage_timing\": {\"favorable_years\": [2027,2028], \"marriage_analysis\": \"2 sentences.\"}, \"married_life\": [\"...x4\"]},\n    \"health_prediction\": {\"overall_vitality\": \"\", \"body_constitution\": \"\", \"overview\": \"2 sentences.\", \"vulnerable_areas\": [\"...x5\"], \"preventive_measures\": [\"...x5\"], \"dietary_recommendations\": [\"...x4\"]},\n    \"wealth_prediction\": {\"overall_rating\": \"\", \"overview\": \"3 sentences.\", \"primary_income_sources\": [\"...x5\"], \"good_investments\": [\"...x4\"], \"avoid\": [\"...x3\"], \"peak_periods\": [\"...x3\"]},\n    \"family_prediction\": {\"overview\": \"2 sentences.\", \"parents\": \"2 sentences.\", \"siblings\": \"1 sentence.\", \"children\": \"1 sentence.\"},\n    \"current_dasha\": {\"mahadasha\": \"\", \"period\": \"\", \"overview\": \"3 sentences.\", \"effects\": [\"...x5\"]},\n    \"dasha_timeline\": [{\"planet\": \"\", \"period\": \"\", \"overview\": \"2 sentences.\", \"effects\": [\"...x4\"]}],\n    \"mangal_dosha\": {\"has_dosha\": false, \"severity\": \"\", \"mars_house\": 1, \"effects\": \"2 sentences.\", \"remedies\": [\"...x4\"]},\n    \"kalsarp_dosha\": {\"has_dosha\": false, \"severity\": \"\", \"remedies\": []},\n    \"benefic_yogas\": [{\"name\": \"\", \"type\": \"benefic\", \"planets_involved\": [\"\"], \"effect\": \"2 sentences.\"}],\n    \"gemstone_remedies\": [{\"stone\": \"\", \"planet\": \"\", \"benefit\": \"1 sentence.\", \"how_to_wear\": \"1 sentence.\"}],\n    \"mantra_remedies\": [{\"mantra\": \"\", \"planet\": \"\", \"chanting\": \"When and how many times.\", \"benefit\": \"1 sentence.\"}],\n    \"lifestyle_remedies\": [\"...x5\"],\n    \"lucky_numbers\": [6, 15],\n    \"lucky_colors\": [\"\",\"\",\"\"],\n    \"lucky_days\": [\"\",\"\"],\n    \"lucky_direction\": \"\",\n    \"numerology\": {\"life_path\": \"\", \"destiny_number\": \"\", \"overview\": \"2 sentences.\"}\n}")
    user_prompt = "Generate Brihat Kundli Pro report for " + request.full_name + " using ONLY this chart:\n\n" + chart_summary + "\n\nReturn ONLY valid JSON. Complete ALL fields."
    try:
        llm = anthropic.AsyncAnthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = await llm.messages.create(model="claude-sonnet-4-20250514", max_tokens=16000, system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
        response_text = message.content[0].text
        import re, json
        clean = re.sub(r'```(?:json)?\s*', '', response_text).replace('```', '').strip()
        try: return json.loads(clean)
        except json.JSONDecodeError as je:
            logging.error("Brihat JSON parse failed: %s. Attempting repair...", je)
            try:
                repair = clean
                opens = repair.count('{') - repair.count('}')
                arr_opens = repair.count('[') - repair.count(']')
                repair += ']' * max(0, arr_opens) + '}' * max(0, opens)
                return json.loads(repair)
            except Exception as repair_err: logging.error("JSON repair failed: %s", repair_err)
            return {"ascendant": {}, "moon_sign": {}, "sun_sign": {}, "planetary_positions": [], "career_prediction": {}, "love_prediction": {}, "health_prediction": {}, "wealth_prediction": {}, "family_prediction": {}, "current_dasha": {}, "dasha_timeline": [], "mangal_dosha": {"has_dosha": False}, "kalsarp_dosha": {}, "benefic_yogas": [], "gemstone_remedies": [], "mantra_remedies": [], "lifestyle_remedies": [], "lucky_numbers": [], "lucky_colors": [], "lucky_days": [], "numerology": {}}
    except Exception as e:
        logging.error("Error generating Brihat Kundli: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate Brihat Kundli: " + str(e))

async def _generate_brihat_kundli_report(
    request: BrihatKundliRequest,
    *,
    user_email: str = "",
    knowledge_engine = None,
    request_user_id: Optional[str] = None,
):
    try:
        chart_data = None
        try: chart_data = calculate_vedic_chart(date_of_birth=request.date_of_birth, time_of_birth=request.time_of_birth, place_of_birth=request.place_of_birth)
        except Exception as ce: logging.warning("Vedic calculator failed for Brihat Kundli: %s", ce)
        chart_svg = ""
        if chart_data and chart_data.get('houses'):
            try: chart_svg = generate_north_indian_chart_svg(chart_data['houses'], chart_data['lagna']['sign'])
            except Exception as se: logging.warning("SVG chart generation failed: %s", se)
        if knowledge_engine is not None and chart_data is not None:
            report_data, knowledge_narratives = await asyncio.gather(
                generate_brihat_kundli_with_llm(request),
                _brihat_ke_pipeline(chart_data, knowledge_engine),
            )
        else:
            report_data = await generate_brihat_kundli_with_llm(request)
            knowledge_narratives = []
        remedies = report_data.get("remedies", {}); yogas = report_data.get("yogas", []); dasha = report_data.get("dasha_analysis", {})
        career = report_data.get("career_prediction", {})
        if career and not career.get("best_career_fields") and career.get("best_fields"): career["best_career_fields"] = career.pop("best_fields")
        if career and not career.get("strengths_at_work") and career.get("strengths"): career["strengths_at_work"] = career.pop("strengths")
        if career and not career.get("career_timeline") and career.get("timeline"): career["career_timeline"] = career.pop("timeline")
        health = report_data.get("health_prediction", {})
        if health and not health.get("preventive_measures") and health.get("remedies"): health["preventive_measures"] = health.pop("remedies", [])
        sun_sign = report_data.get("sun_sign", {})
        if not sun_sign.get("sign") and report_data.get("planetary_positions"):
            for p in report_data.get("planetary_positions", []):
                if isinstance(p, dict) and p.get("planet") == "Sun": sun_sign["sign"] = p.get("sign", ""); break
        current_dasha_raw = report_data.get("current_dasha", dasha)
        if isinstance(current_dasha_raw, str): current_dasha = {"mahadasha": current_dasha_raw.replace(" Mahadasha", "").replace(" Dasha", "").strip(), "effects": []}
        elif isinstance(current_dasha_raw, dict):
            cd = dict(current_dasha_raw)
            if not cd.get("mahadasha") and cd.get("current_dasha"): cd["mahadasha"] = cd.pop("current_dasha")
            if not cd.get("mahadasha") and cd.get("planet"): cd["mahadasha"] = cd.pop("planet")
            if not cd.get("effects") and cd.get("current_effects"): cd["effects"] = cd.pop("current_effects")
            if cd.get("mahadasha"): cd["mahadasha"] = cd["mahadasha"].replace(" Mahadasha","").replace(" Dasha","").strip()
            current_dasha = cd
        else: current_dasha = {}
        dasha_timeline_raw = report_data.get("dasha_timeline", dasha.get("upcoming", []) if isinstance(dasha, dict) else [])
        dasha_timeline = []
        for d in dasha_timeline_raw:
            if isinstance(d, dict):
                entry = dict(d)
                if not entry.get("planet") and entry.get("dasha"): entry["planet"] = entry.pop("dasha")
                if not entry.get("period") and entry.get("start_year") and entry.get("end_year"): entry["period"] = str(entry['start_year']) + " \u2013 " + str(entry['end_year'])
                dasha_timeline.append(entry)
        mangal_from_claude = report_data.get("mangal_dosha", {})
        if chart_data and chart_data.get("mangal_dosha"):
            calc_mangal = chart_data["mangal_dosha"]
            mangal = {"has_dosha": calc_mangal.get("has_dosha", calc_mangal.get("present", False)), "present": calc_mangal.get("has_dosha", calc_mangal.get("present", False)), "mars_house": calc_mangal.get("mars_house", ""), "severity": calc_mangal.get("severity", ""), "description": calc_mangal.get("description", calc_mangal.get("note", "")), "remedies": mangal_from_claude.get("remedies", []) if isinstance(mangal_from_claude, dict) else [], "effects": mangal_from_claude.get("effects", "") if isinstance(mangal_from_claude, dict) else ""}
        else:
            mangal = mangal_from_claude
            if isinstance(mangal, dict) and not mangal.get("has_dosha") and mangal.get("present"): mangal["has_dosha"] = mangal["present"]
        report = BrihatKundliReport(user_email=user_email, full_name=request.full_name, date_of_birth=request.date_of_birth, time_of_birth=request.time_of_birth, place_of_birth=request.place_of_birth, gender=request.gender, ascendant=report_data.get("ascendant", {}), moon_sign=report_data.get("moon_sign", {}), sun_sign=sun_sign, planetary_positions=report_data.get("planetary_positions", []), career_prediction=career, love_prediction=(lambda lp: {**lp, "ideal_partner_traits": lp.get("ideal_partner_traits") or lp.get("ideal_partner") or [], "compatibility_signs": lp.get("compatibility_signs") or lp.get("compatible_signs") or [], "challenging_signs": lp.get("challenging_signs") or []})(report_data.get("love_prediction", {})), health_prediction=health, wealth_prediction=(lambda wp: {**wp, "primary_income_sources": wp.get("primary_income_sources") or wp.get("income_sources") or wp.get("wealth_sources") or [], "good_investments": wp.get("good_investments") or wp.get("investments") or wp.get("peak_periods") or ["Real estate", "Gold", "Equity"], "avoid": wp.get("avoid") or wp.get("cautions") or ["High-risk speculation"]})(report_data.get("wealth_prediction", {})), family_prediction=report_data.get("family_prediction", {}), education_prediction=report_data.get("education_prediction", {}), current_dasha=current_dasha, dasha_timeline=dasha_timeline, mangal_dosha=mangal, kalsarp_dosha=report_data.get("kalsarp_dosha", {}), other_doshas=report_data.get("other_doshas", []), benefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "benefic"] or report_data.get("benefic_yogas", []), malefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "malefic"] or report_data.get("malefic_yogas", []), gemstone_remedies=remedies.get("gemstones", report_data.get("gemstone_remedies", [])), mantra_remedies=remedies.get("mantras", report_data.get("mantra_remedies", [])), lifestyle_remedies=remedies.get("general", report_data.get("lifestyle_remedies", [])), donation_remedies=report_data.get("donation_remedies", []), lucky_numbers=report_data.get("lucky_numbers", []), lucky_colors=report_data.get("lucky_colors", []), lucky_days=report_data.get("lucky_days", []), lucky_direction=report_data.get("lucky_direction", ""), numerology=report_data.get("numerology", {}), chart_svg=chart_svg, knowledge_narratives=knowledge_narratives)
        import json
        doc = json.loads(report.model_dump_json())
        await db.brihat_kundli_reports.insert_one({**doc})
        if request_user_id:
            await register_arc_angel_report_run(db, str(request_user_id), "brihat_kundali")
        return {"success": True, "report_id": report.id, "report": doc}
    except Exception as e:
        logging.error("Brihat Kundli generation error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate report: " + str(e))


@api_router.post("/brihat-kundli/generate")
async def generate_brihat_kundli(
    request: BrihatKundliRequest,
    http_request: Request,
    user_email: str = "",
    source_order_id: Optional[str] = None,
):
    result = await _generate_brihat_kundli_report(
        request,
        user_email=user_email,
        knowledge_engine=getattr(http_request.app.state, "knowledge_engine", None),
        request_user_id=(getattr(http_request.state, "user", None) or {}).get("user_id"),
    )
    if source_order_id:
        await _finalize_order_fulfillment(source_order_id, generated_report_id=result["report_id"])
    return result

@api_router.get("/brihat-kundli/{report_id}")
async def get_brihat_kundli(report_id: str):
    report = await db.brihat_kundli_reports.find_one({"id": report_id}, {"_id": 0})
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    return report

@api_router.get("/brihat-kundli/{report_id}/pdf")
async def download_brihat_kundli_pdf(report_id: str, user_email: str = None):
    report = await db.brihat_kundli_reports.find_one({"id": report_id}, {"_id": 0})
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    try:
        chart_data = None
        try: chart_data = calculate_vedic_chart(date_of_birth=report['date_of_birth'], time_of_birth=report['time_of_birth'], place_of_birth=report.get('place_of_birth', 'New Delhi'))
        except Exception as ce: logging.warning("Chart calc for Brihat PDF failed: %s", ce)
        password = generate_report_password(report.get('full_name', ''), report.get('date_of_birth', ''))
        pdf_buffer = generate_brihat_kundli_pdf(report, chart_data=chart_data, password=password)
        safe_name = report.get('full_name', 'report').replace(' ', '_')
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=brihat_kundli_" + safe_name + ".pdf", "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password", "X-PDF-Password": password})
    except Exception as e:
        logging.error("Brihat PDF generation error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate PDF: " + str(e))

async def generate_kundali_milan_with_llm(person1: BirthProfile, person2: BirthProfile) -> tuple:
    chart1, chart2, ashtakoot_data = None, None, None
    compatibility_score = 0; mangal1, mangal2 = {}, {}
    try:
        chart1 = calculate_vedic_chart(date_of_birth=person1.date_of_birth, time_of_birth=person1.time_of_birth, place_of_birth=person1.location)
        chart2 = calculate_vedic_chart(date_of_birth=person2.date_of_birth, time_of_birth=person2.time_of_birth, place_of_birth=person2.location)
        ashtakoot_data = calculate_ashtakoot(chart1['nakshatra']['name'], chart1['moon_sign']['sign'], chart2['nakshatra']['name'], chart2['moon_sign']['sign'])
        compatibility_score = ashtakoot_data.get('total_score', 0)
        mangal1 = chart1['mangal_dosha']; mangal2 = chart2['mangal_dosha']
    except Exception as e: logging.error("Vedic calculator FAILED for Kundali Milan: %s", e, exc_info=True)

    def fmt_chart(name, chart, mangal):
        if not chart: return name + ": chart calculation unavailable"
        lagna = chart['lagna']; moon = chart['moon_sign']; nak = chart['nakshatra']
        dasha_planet = chart.get('current_dasha', {}).get('planet', 'Unknown')
        mangal_str = "YES \u2014 " + mangal.get('description', '') if mangal.get('has_dosha') else "No"
        return (name + ":\n  Ascendant: " + lagna['sign_vedic'] + " (" + str(lagna['degree']) + "\u00b0), Lord: " + lagna['lord'] + "\n  Moon Sign: " + moon['sign_vedic'] + "\n  Nakshatra: " + nak['name'] + " Pada " + str(nak.get('pada', '?')) + " | Lord: " + str(nak.get('lord', '?')) + "\n  Mangal Dosha: " + mangal_str + "\n  Dasha: " + dasha_planet + " Mahadasha")

    def fmt_ashtakoot(data):
        if not data or 'kootas' not in data: return "Score unavailable"
        lines = ["  TOTAL: " + str(data['total_score']) + "/36"]
        for k, v in data['kootas'].items(): lines.append("  " + k.upper() + ": " + str(v['score']) + "/" + str(v['max']) + " \u2014 " + str(v.get('label', '')))
        return '\n'.join(lines)

    chart_text = ("\nCALCULATED CHART DATA:\n\n" + fmt_chart(person1.name, chart1, mangal1) + "\n\n" + fmt_chart(person2.name, chart2, mangal2) + "\n\nASTHAKOOT GUNA MILAN (do NOT change these scores):\n" + fmt_ashtakoot(ashtakoot_data) + "\n")
    system_prompt = ("You are an expert Jyotish astrologer specialising in Vivah Milan. Interpret ONLY \u2014 never recalculate or change scores. NO markdown. Sections: Compatibility Overview, Ashtakoot Analysis, Mangal Dosha Assessment, Planetary Harmony, Relationship Strengths, Challenges, Marriage Timing, Remedies. Target 900-1000 words.")
    user_prompt = "Write Kundali Milan report for " + person1.name + " and " + person2.name + ".\n\n" + chart_text + "\n\nCompatibility score is " + str(compatibility_score) + "/36 \u2014 final. Explain each Koota score for this couple."
    try:
        llm = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = llm.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
        return compatibility_score, message.content[0].text, ashtakoot_data
    except Exception as e:
        logging.error("Error generating Kundali Milan: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate Kundali Milan: " + str(e))

@api_router.post("/kundali-milan/generate", response_model=KundaliMilanReport)
async def generate_kundali_milan(request: KundaliMilanRequest):
    profile1 = await db.birth_profiles.find_one({"id": request.person1_id}, {"_id": 0})
    profile2 = await db.birth_profiles.find_one({"id": request.person2_id}, {"_id": 0})
    if not profile1 or not profile2: raise HTTPException(status_code=404, detail="One or both birth profiles not found")
    for p in [profile1, profile2]:
        if isinstance(p['created_at'], str): p['created_at'] = datetime.fromisoformat(p['created_at'])
    birth_profile1 = BirthProfile(**profile1); birth_profile2 = BirthProfile(**profile2)
    existing = await db.kundali_milan_reports.find_one({"$or": [{"person1_id": request.person1_id, "person2_id": request.person2_id}, {"person1_id": request.person2_id, "person2_id": request.person1_id}]}, {"_id": 0})
    if existing:
        if isinstance(existing['generated_at'], str): existing['generated_at'] = datetime.fromisoformat(existing['generated_at'])
        return KundaliMilanReport(**existing)
    score, analysis, ashtakoot_data = await generate_kundali_milan_with_llm(birth_profile1, birth_profile2)
    km_chart1, km_chart2 = None, None
    try: km_chart1 = calculate_vedic_chart(date_of_birth=birth_profile1.date_of_birth, time_of_birth=birth_profile1.time_of_birth, place_of_birth=birth_profile1.location)
    except Exception as ce: logging.warning("Chart1 KundaliMilan: %s", ce)
    try: km_chart2 = calculate_vedic_chart(date_of_birth=birth_profile2.date_of_birth, time_of_birth=birth_profile2.time_of_birth, place_of_birth=birth_profile2.location)
    except Exception as ce: logging.warning("Chart2 KundaliMilan: %s", ce)
    km_svg1, km_svg2 = "", ""
    try:
        if km_chart1 and km_chart1.get('houses'): km_svg1 = generate_north_indian_chart_svg(km_chart1['houses'], km_chart1['lagna']['sign'])
        if km_chart2 and km_chart2.get('houses'): km_svg2 = generate_north_indian_chart_svg(km_chart2['houses'], km_chart2['lagna']['sign'])
    except Exception as se: logging.warning("SVG KundaliMilan: %s", se)
    km_ashtakoot_details = {}
    if ashtakoot_data and isinstance(ashtakoot_data, dict):
        km_ashtakoot_details = {k: v.get('score', 0) for k, v in ashtakoot_data.get('kootas', {}).items()}
    report = KundaliMilanReport(person1_id=request.person1_id, person2_id=request.person2_id, compatibility_score=score, detailed_analysis=analysis, chart_svg_person1=km_svg1, chart_svg_person2=km_svg2, ashtakoot_details=km_ashtakoot_details)
    import json as _json
    doc = _json.loads(report.model_dump_json())
    await db.kundali_milan_reports.insert_one({**doc})
    return report

@api_router.get("/kundali-milan/{report_id}/pdf")
async def download_kundali_milan_pdf(report_id: str, user_email: str = None):
    report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
    person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
    if not person1 or not person2: raise HTTPException(status_code=404, detail="Profiles not found")
    try:
        password = generate_report_password(person1.get('name', ''), person1.get('date_of_birth', ''))
        pdf_buffer = generate_kundali_milan_pdf(person1, person2, report['compatibility_score'], report['detailed_analysis'], password=password)
        fn = "Kundali_Milan_" + person1['name'].replace(' ', '_') + "_" + person2['name'].replace(' ', '_') + ".pdf"
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=" + fn, "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password", "X-PDF-Password": password})
    except Exception as e:
        logging.error("PDF generation error: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

@api_router.get("/kundali-milan/{person1_id}/{person2_id}", response_model=KundaliMilanReport)
async def get_kundali_milan(person1_id: str, person2_id: str):
    report = await db.kundali_milan_reports.find_one({"$or": [{"person1_id": person1_id, "person2_id": person2_id}, {"person1_id": person2_id, "person2_id": person1_id}]}, {"_id": 0})
    if not report: raise HTTPException(status_code=404, detail="Kundali Milan report not found")
    if isinstance(report['generated_at'], str): report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    return KundaliMilanReport(**report)

async def check_premium_access(user_email: str, report_type: str, report_id: str) -> bool:
    subscription = await db.subscriptions.find_one({"user_email": user_email, "status": "active", "subscription_type": "premium_monthly"})
    if subscription:
        expires_at = subscription.get('expires_at')
        if expires_at is None: return True
        if isinstance(expires_at, str): expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        if expires_at.tzinfo is None: expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at > datetime.now(timezone.utc): return True
    payment = await db.payments.find_one({"user_email": user_email, "report_type": report_type, "report_id": report_id, "status": "completed"})
    if payment: return True
    premium_payment = await db.payments.find_one({"user_email": user_email, "report_type": "premium_monthly", "status": "completed"})
    return premium_payment is not None


async def _activate_premium_subscription(user_email: str, payment_id: Optional[str]) -> None:
    if not user_email:
        raise ValueError("Premium subscription requires user email")
    await db.subscriptions.update_one(
        {"user_email": user_email, "subscription_type": "premium_monthly"},
        {
            "$set": {
                "status": "active",
                "stripe_subscription_id": payment_id,
                "expires_at": utc_now() + timedelta(days=30),
            },
            "$setOnInsert": {
                "id": str(uuid.uuid4()),
                "created_at": utc_now(),
            },
        },
        upsert=True,
    )


async def _lock_order_for_fulfillment(order_id: str) -> Optional[Dict[str, Any]]:
    return await db["orders_ledger"].find_one_and_update(
        {
            "_id": order_id,
            "ts_fulfill_done": None,
            "fulfillment_in_progress": {"$ne": True},
        },
        {
            "$set": {
                "fulfillment_in_progress": True,
                "last_fulfillment_attempt": utc_now(),
                "error_log": None,
            }
        },
        return_document=ReturnDocument.AFTER,
    )


async def _release_fulfillment_lock(order_id: str, error_message: str) -> None:
    await db["orders_ledger"].update_one(
        {"_id": order_id},
        {"$set": {"fulfillment_in_progress": False, "error_log": error_message[:500]}},
    )


async def _finalize_order_fulfillment(order_id: str, *, generated_report_id: Optional[str] = None) -> None:
    await _mark_order_fulfilled(order_id, generated_report_id=generated_report_id)
    finalized_order = await db["orders_ledger"].find_one({"_id": order_id}, {"_id": 0})
    if finalized_order:
        await _create_customer_gst_entry(finalized_order)


async def _fulfil_order(order_id: str):
    locked_order = await _lock_order_for_fulfillment(order_id)
    if not locked_order:
        return

    try:
        report_type = locked_order.get("report_type")

        if report_type == "premium_monthly":
            await _activate_premium_subscription(locked_order.get("user_email", ""), locked_order.get("razorpay_payment_id"))
            await _finalize_order_fulfillment(order_id)
            return

        if report_type == "birth_chart":
            report = await db.birth_chart_reports.find_one({"profile_id": locked_order.get("report_id")}, {"_id": 0, "id": 1})
            if not report:
                raise ValueError("Birth chart report not found for fulfillment")
            await _finalize_order_fulfillment(order_id, generated_report_id=report.get("id"))
            return

        if report_type == "kundali_milan":
            report = await db.kundali_milan_reports.find_one({"id": locked_order.get("report_id")}, {"_id": 0, "id": 1})
            if not report:
                raise ValueError("Kundali Milan report not found for fulfillment")
            await _finalize_order_fulfillment(order_id, generated_report_id=report.get("id"))
            return

        if report_type == "brihat_kundli":
            if locked_order.get("generated_report_id"):
                await _finalize_order_fulfillment(order_id, generated_report_id=locked_order.get("generated_report_id"))
                return

            if locked_order.get("report_id") and locked_order.get("report_id") != "new":
                existing = await db.brihat_kundli_reports.find_one({"id": locked_order.get("report_id")}, {"_id": 0, "id": 1})
                if existing:
                    await _finalize_order_fulfillment(order_id, generated_report_id=existing.get("id"))
                    return

            await asyncio.sleep(20)
            refreshed_order = await db["orders_ledger"].find_one({"_id": order_id}, {"_id": 0})
            if refreshed_order and refreshed_order.get("ts_fulfill_done"):
                return

            existing = await _find_existing_brihat_report(refreshed_order or locked_order)
            if existing:
                await _finalize_order_fulfillment(order_id, generated_report_id=existing.get("id"))
                return

            context = (refreshed_order or locked_order).get("order_context") or {}
            required = ["full_name", "date_of_birth", "time_of_birth", "place_of_birth", "gender"]
            missing = [field for field in required if not context.get(field)]
            if missing:
                raise ValueError(f"Missing Brihat fulfillment context: {', '.join(missing)}")

            result = await _generate_brihat_kundli_report(
                BrihatKundliRequest(**context),
                user_email=(refreshed_order or locked_order).get("user_email", ""),
                knowledge_engine=getattr(app.state, "knowledge_engine", None),
            )
            await _finalize_order_fulfillment(order_id, generated_report_id=result["report_id"])
            return

        raise ValueError(f"Unsupported fulfillment report type: {report_type}")
    except Exception as exc:
        logging.error("Order fulfillment failed for %s: %s", order_id, exc, exc_info=True)
        await _release_fulfillment_lock(order_id, str(exc))

@api_router.post("/payment/create-order")
async def create_payment_order(request: PaymentIntentRequest, http_request: Request):
    if request.report_type not in PRICING: raise HTTPException(status_code=400, detail="Invalid report type")
    try:
        amount_paise = int(PRICING[request.report_type] * 100)
        request_user_id = await _resolve_request_user_id(http_request)
        normalized_email = _normalize_email(request.user_email)
        razorpay_order = razorpay_client.order.create({"amount": amount_paise, "currency": "INR", "payment_capture": 1, "notes": {"report_type": request.report_type, "report_id": request.report_id or "", "user_email": normalized_email}})
        payment = Payment(user_email=normalized_email, report_type=request.report_type, report_id=request.report_id or "", amount=PRICING[request.report_type], razorpay_order_id=razorpay_order["id"], status="created")
        await db.payments.insert_one(payment.model_dump(mode='json'))
        await db["orders_ledger"].insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": _derive_order_user_id(request_user_id, normalized_email),
            "user_email": normalized_email,
            "report_type": request.report_type,
            "report_id": request.report_id or "",
            "amount_paise": amount_paise,
            "current_state": "CART_ADD",
            "razorpay_order_id": razorpay_order["id"],
            "ts_cart_add": utc_now(),
            "ts_checkout_init": utc_now(),
            "order_context": request.order_context or {},
            "generated_report_id": None,
            "error_log": None,
            "fulfillment_in_progress": False,
        })
        return {"order_id": razorpay_order["id"], "amount": PRICING[request.report_type], "currency": "INR", "key_id": os.environ.get('RAZORPAY_KEY_ID')}
    except HTTPException: raise
    except Exception as e: logging.error("Razorpay order creation error: %s", str(e)); raise HTTPException(status_code=500, detail="Payment order creation failed")


@api_router.post("/diagnostics/order/{razorpay_order_id}/gateway-open")
async def mark_gateway_open(razorpay_order_id: str):
    result = await db["orders_ledger"].update_one(
        {"razorpay_order_id": razorpay_order_id},
        {"$set": {"current_state": "GATEWAY_OPEN", "ts_gateway_open": utc_now()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order ledger row not found")
    return {"status": "ok"}


@api_router.post("/webhooks/razorpay", status_code=200)
async def razorpay_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_razorpay_signature: str = Header(...),
):
    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    raw_body = await request.body()
    expected = hmac.new(RAZORPAY_WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_razorpay_signature):
        raise HTTPException(status_code=403, detail="Signature mismatch")

    payload = await request.json()
    if payload.get("event") == "order.paid":
        entity = (((payload.get("payload") or {}).get("payment") or {}).get("entity") or {})
        rzp_order_id = entity.get("order_id")
        rzp_payment_id = entity.get("id")

        updated = await db["orders_ledger"].find_one_and_update(
            {"razorpay_order_id": rzp_order_id},
            {"$set": {"current_state": "PAID", "razorpay_payment_id": rzp_payment_id, "ts_pmt_success": utc_now(), "error_log": None}},
            return_document=ReturnDocument.AFTER,
        )

        if not updated:
            payment_doc = await db.payments.find_one({"razorpay_order_id": rzp_order_id}, {"_id": 0})
            if payment_doc:
                user_email = _normalize_email(payment_doc.get("user_email"))
                fallback_order = {
                    "_id": str(uuid.uuid4()),
                    "user_id": _derive_order_user_id(None, user_email),
                    "user_email": user_email,
                    "report_type": payment_doc.get("report_type", ""),
                    "report_id": payment_doc.get("report_id", ""),
                    "amount_paise": int(float(payment_doc.get("amount", 0)) * 100),
                    "current_state": "PAID",
                    "razorpay_order_id": rzp_order_id,
                    "razorpay_payment_id": rzp_payment_id,
                    "ts_cart_add": payment_doc.get("created_at") or utc_now(),
                    "ts_checkout_init": payment_doc.get("created_at") or utc_now(),
                    "ts_pmt_success": utc_now(),
                    "order_context": {},
                    "generated_report_id": None,
                    "error_log": None,
                    "fulfillment_in_progress": False,
                }
                await db["orders_ledger"].insert_one(fallback_order)
                updated = fallback_order

        await db.payments.update_one(
            {"razorpay_order_id": rzp_order_id},
            {"$set": {"razorpay_payment_id": rzp_payment_id, "status": "completed"}},
        )

        if updated:
            background_tasks.add_task(_fulfil_order, updated["_id"])

    return {"status": "acknowledged"}

@api_router.post("/payment/verify")
async def verify_payment(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str, user_email: str):
    try:
        razorpay_client.utility.verify_payment_signature({'razorpay_order_id': razorpay_order_id, 'razorpay_payment_id': razorpay_payment_id, 'razorpay_signature': razorpay_signature})
        payment_doc = await db.payments.find_one({"razorpay_order_id": razorpay_order_id}, {"_id": 0})
        if not payment_doc: raise HTTPException(status_code=404, detail="Payment record not found")
        await db.payments.update_one({"razorpay_order_id": razorpay_order_id}, {"$set": {"razorpay_payment_id": razorpay_payment_id, "status": "completed"}})
        if payment_doc['report_type'] == "premium_monthly":
            subscription = UserSubscription(user_email=user_email, subscription_type="premium_monthly", status="active", stripe_subscription_id=razorpay_payment_id, expires_at=datetime.now(timezone.utc) + timedelta(days=30))
            await db.subscriptions.insert_one(subscription.model_dump(mode='json'))
        return {"status": "success", "message": "Payment verified successfully", "payment_id": razorpay_payment_id}
    except razorpay.errors.SignatureVerificationError:
        logging.error("Payment signature verification failed")
        await db.payments.update_one({"razorpay_order_id": razorpay_order_id}, {"$set": {"status": "failed"}})
        raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e: logging.error("Payment verification error: %s", str(e)); raise HTTPException(status_code=500, detail="Payment verification failed")

@api_router.get("/premium/check")
async def check_premium(user_email: str, report_type: str, report_id: str):
    return {"has_premium_access": await check_premium_access(user_email, report_type, report_id)}

@api_router.get("/birthchart/{profile_id}/pdf")
async def download_birth_chart_pdf(profile_id: str, user_email: str = None):
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    report = await db.birth_chart_reports.find_one({"profile_id": profile_id}, {"_id": 0})
    if not profile or not report: raise HTTPException(status_code=404, detail="Report not found")
    try:
        chart_data = None
        try: chart_data = calculate_vedic_chart(date_of_birth=profile['date_of_birth'], time_of_birth=profile['time_of_birth'], place_of_birth=profile.get('location', profile.get('place_of_birth', 'New Delhi')))
        except Exception as ce: logging.warning("Chart calc for PDF failed: %s", ce)
        password = generate_report_password(profile.get('name', ''), profile.get('date_of_birth', ''))
        pdf_buffer = generate_birth_chart_pdf(profile, report['report_content'], chart_data=chart_data, password=password)
        fn = "Birth_Chart_Report_" + profile['name'].replace(' ', '_') + ".pdf"
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=" + fn, "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password", "X-PDF-Password": password})
    except Exception as e: logging.error("PDF generation error: %s", str(e)); raise HTTPException(status_code=500, detail="Failed to generate PDF")

@api_router.get("/my-reports")
async def get_my_reports(user_email: str, request: Request):
    await get_current_user(request, db)
    try:
        reports = []
        profiles = await db.birth_profiles.find({"user_email": user_email}, {"_id": 0}).to_list(50)
        profile_ids = [p["id"] for p in profiles]; profile_map = {p["id"]: p for p in profiles}
        if profile_ids:
            for r in await db.birth_chart_reports.find({"profile_id": {"$in": profile_ids}}, {"_id": 0}).sort("generated_at", -1).to_list(50):
                pf = profile_map.get(r.get("profile_id"), {})
                reports.append({"id": r["id"], "type": "birth_chart", "type_label": "Birth Chart", "name": pf.get("name", "Unknown"), "subtitle": pf.get('date_of_birth', '') + " \u00b7 " + pf.get('location', ''), "profile_id": r.get("profile_id"), "generated_at": r.get("generated_at"), "lagna": r.get("lagna", {}), "nakshatra": r.get("nakshatra", {}), "current_dasha": r.get("current_dasha", {})})
        if profile_ids:
            for r in await db.kundali_milan_reports.find({"$or": [{"person1_id": {"$in": profile_ids}}, {"person2_id": {"$in": profile_ids}}]}, {"_id": 0}).sort("generated_at", -1).to_list(50):
                p1 = profile_map.get(r.get("person1_id"), {})
                p2 = await db.birth_profiles.find_one({"id": r.get("person2_id")}, {"_id": 0}) or {}
                reports.append({"id": r["id"], "type": "kundali_milan", "type_label": "Kundali Milan", "name": p1.get('name', '?') + " & " + p2.get('name', '?'), "subtitle": "Compatibility Score: " + str(r.get('compatibility_score', 0)) + "/36", "person1_id": r.get("person1_id"), "person2_id": r.get("person2_id"), "compatibility_score": r.get("compatibility_score", 0), "generated_at": r.get("generated_at")})
        for r in await db.brihat_kundli_reports.find({"user_email": user_email}, {"_id": 0}).sort("generated_at", -1).to_list(20):
            reports.append({"id": r["id"], "type": "brihat_kundli", "type_label": "Brihat Kundli Pro", "name": r.get("full_name", "Unknown"), "subtitle": r.get('date_of_birth', '') + " \u00b7 " + r.get('place_of_birth', ''), "generated_at": r.get("generated_at"), "ascendant": r.get("ascendant", {}), "current_dasha": r.get("current_dasha", {})})
        reports.sort(key=lambda x: str(x.get("generated_at", "")), reverse=True)
        return {"reports": reports, "total": len(reports)}
    except Exception as e:
        logging.error("Error fetching my-reports: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch reports")

@api_router.post("/share/create")
async def create_share_link(report_type: str, report_id: str):
    existing = await db.share_links.find_one({"report_type": report_type, "report_id": report_id}, {"_id": 0})
    if existing:
        if isinstance(existing['created_at'], str): existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return ShareLink(**existing)
    share_link = ShareLink(report_type=report_type, report_id=report_id)
    await db.share_links.insert_one(share_link.model_dump(mode='json'))
    return share_link

@api_router.get("/share/{token}")
async def get_shared_report(token: str):
    share_link = await db.share_links.find_one({"token": token}, {"_id": 0})
    if not share_link: raise HTTPException(status_code=404, detail="Share link not found")
    await db.share_links.update_one({"token": token}, {"$inc": {"views": 1}})
    report_type = share_link['report_type']; report_id = share_link['report_id']
    if report_type == "birth_chart":
        profile = await db.birth_profiles.find_one({"id": report_id}, {"_id": 0})
        report = await db.birth_chart_reports.find_one({"profile_id": report_id}, {"_id": 0})
        if not profile or not report: raise HTTPException(status_code=404, detail="Report not found")
        return {"type": "birth_chart", "profile": profile, "report": report}
    elif report_type == "kundali_milan":
        report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
        if not report: raise HTTPException(status_code=404, detail="Report not found")
        person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
        person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
        return {"type": "kundali_milan", "report": report, "person1": person1, "person2": person2}
    raise HTTPException(status_code=400, detail="Invalid report type")

@api_router.post("/auth/register")
async def register(request: RegisterRequest, response: Response):
    existing = await db.users.find_one({"email": request.email})
    if existing: raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=request.email, name=request.name, password_hash=hash_password(request.password))
    await db.users.insert_one(user.model_dump(mode='json'))
    welcome_body = '<div style="font-family: Arial, sans-serif;"><h2 style="color: #B8960C;">Welcome to Everyday Horoscope! \u2728</h2><p>Hi ' + user.name + ', your account has been created.</p></div>'
    await send_email_notification(user.email, "Welcome to Everyday Horoscope \u2728", welcome_body)
    admin_email = os.environ.get('ADMIN_EMAIL', os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com'))
    await send_email_notification(admin_email, "New Registration: " + user.name, "<p><b>Name:</b> " + user.name + "</p><p><b>Email:</b> " + user.email + "</p>")
    session_token = await create_session(db, user.user_id)
    set_session_cookie(response, session_token)
    return UserResponse(user_id=user.user_id, email=user.email, name=user.name, picture=user.picture)

@api_router.post("/auth/login")
async def login(request: LoginRequest, response: Response):
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user_doc: raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user_doc.get('password_hash'): raise HTTPException(status_code=401, detail="Please login with Google")
    locked_until = user_doc.get('locked_until')
    if locked_until:
        if isinstance(locked_until, str): locked_until = datetime.fromisoformat(locked_until)
        if locked_until.tzinfo is None: locked_until = locked_until.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < locked_until:
            remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds() / 60)
            raise HTTPException(status_code=429, detail="Account locked. Try again in " + str(remaining) + " minutes.")
        else: await db.users.update_one({"email": request.email}, {"$unset": {"locked_until": "", "failed_attempts": ""}})
    if not verify_password(request.password, user_doc['password_hash']):
        failed = user_doc.get('failed_attempts', 0) + 1
        update = {"$set": {"failed_attempts": failed}}
        if failed >= 5:
            lock_until = datetime.now(timezone.utc) + timedelta(hours=24)
            update = {"$set": {"failed_attempts": failed, "locked_until": lock_until.isoformat()}}
            await db.users.update_one({"email": request.email}, update)
            raise HTTPException(status_code=429, detail="Account locked for 24 hours due to too many failed attempts.")
        await db.users.update_one({"email": request.email}, update)
        remaining_attempts = 5 - failed
        s = "s" if remaining_attempts != 1 else ""
        raise HTTPException(status_code=401, detail="Invalid email or password. " + str(remaining_attempts) + " attempt" + s + " remaining.")
    await db.users.update_one({"email": request.email}, {"$unset": {"failed_attempts": "", "locked_until": ""}})
    session_token = await create_session(db, user_doc['user_id'])
    set_session_cookie(response, session_token)
    return UserResponse(user_id=user_doc['user_id'], email=user_doc['email'], name=user_doc['name'], picture=user_doc.get('picture'))

@api_router.post("/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    import secrets as secrets_module
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user_doc or not user_doc.get('password_hash'): return {"message": "If that email exists, a reset link has been sent."}
    reset_token = secrets_module.token_urlsafe(32)
    reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    await db.users.update_one({"email": request.email}, {"$set": {"reset_token": reset_token, "reset_token_expires": reset_expires.isoformat()}})
    frontend_url = os.environ.get('FRONTEND_URL', 'https://everydayhoroscope.in')
    reset_link = frontend_url + "/reset-password?token=" + reset_token
    user_name = user_doc.get("name", "there")
    email_body = '<div style="font-family: Georgia, serif; max-width: 600px; padding: 32px;"><h1 style="color: #C5A059;">\u2726 Everyday Horoscope</h1><h2>Reset your password</h2><p>Hi ' + user_name + ',</p><p>Click below. Link expires in 1 hour.</p><a href="' + reset_link + '" style="background: #C5A059; color: #fff; padding: 14px 32px; border-radius: 4px; text-decoration: none; font-weight: bold;">Reset My Password</a></div>'
    await send_email_notification(request.email, "Reset your Everyday Horoscope password", email_body)
    return {"message": "If that email exists, a reset link has been sent."}

@api_router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    user_doc = await db.users.find_one({"reset_token": request.token}, {"_id": 0})
    if not user_doc: raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    expires = user_doc.get('reset_token_expires')
    if expires:
        if isinstance(expires, str): expires = datetime.fromisoformat(expires)
        if expires.tzinfo is None: expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires: raise HTTPException(status_code=400, detail="Reset token has expired.")
    if len(request.new_password) < 6: raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    await db.users.update_one({"reset_token": request.token}, {"$set": {"password_hash": hash_password(request.new_password)}, "$unset": {"reset_token": "", "reset_token_expires": "", "failed_attempts": "", "locked_until": ""}})
    return {"message": "Password reset successfully."}

@api_router.get("/auth/me")
async def get_me(request: Request):
    user = await get_current_user(request, db)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    now = datetime.now(timezone.utc)
    sub = await db.subscriptions.find_one({"user_email": user.email, "status": "active"})
    is_premium = False
    if sub:
        expires_at = sub.get("expires_at")
        if expires_at is None:
            is_premium = True
        else:
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            is_premium = expires_at > now
    return UserResponse(user_id=user.user_id, email=user.email, name=user.name, picture=user.picture, is_premium=is_premium)

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if session_token: await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

class OAuthCallbackRequest(BaseModel):
    session_id: str

@api_router.post("/auth/oauth/callback")
async def oauth_callback(response: Response, body: OAuthCallbackRequest = None, session_id: str = None):
    code = (body.session_id if body else None) or session_id
    if not code: raise HTTPException(status_code=400, detail="Missing authorization code")
    try:
        user_data = await exchange_session_id_for_token(code)
        user = await get_or_create_oauth_user(db, email=user_data['email'], name=user_data['name'], picture=user_data.get('picture'), google_id=user_data['id'])
        session_token = await create_session(db, user.user_id)
        set_session_cookie(response, session_token)
        return UserResponse(user_id=user.user_id, email=user.email, name=user.name, picture=user.picture)
    except Exception as e: logging.error("OAuth callback error: %s", str(e)); raise HTTPException(status_code=401, detail="Authentication failed")


@api_router.post("/diagnostics/log", status_code=202)
async def log_diagnostics_event(event: TelemetryLogRequest, request: Request):
    user_id = event.user_id or await _resolve_request_user_id(request)
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    telemetry_event = TelemetryEvent(
        page_url=event.page_url,
        event_type=event.event_type,
        metadata=event.metadata,
        timestamp=event.timestamp,
    )
    await _append_diagnostic_event(user_id, telemetry_event.model_dump())
    return {"status": "queued"}

@api_router.get("/policies/{policy_type}")
async def get_policy(policy_type: str):
    valid_types = ['terms', 'privacy', 'subscription-terms', 'refund-policy', 'cookie-policy']
    if policy_type not in valid_types: raise HTTPException(status_code=404, detail="Policy not found")
    policy = await db.policies.find_one({"type": policy_type}, {"_id": 0})
    if not policy: raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@api_router.put("/admin/policies/{policy_type}")
async def update_policy(request: Request, policy_type: str, policy_data: dict):
    await require_admin(request, db)
    valid_types = ['terms', 'privacy', 'subscription-terms', 'refund-policy', 'cookie-policy']
    if policy_type not in valid_types: raise HTTPException(status_code=404, detail="Policy type not found")
    policy_data['type'] = policy_type; policy_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    await db.policies.update_one({"type": policy_type}, {"$set": policy_data}, upsert=True)
    return {"success": True, "message": "Policy '" + policy_type + "' updated"}

@api_router.get("/admin/policies")
async def get_all_policies(request: Request):
    await require_admin(request, db)
    return {"policies": await db.policies.find({}, {"_id": 0}).to_list(100)}

@api_router.post("/contact")
async def submit_contact_form(form: ContactFormRequest):
    contact_doc = {"id": str(uuid.uuid4()), "name": form.name, "email": form.email, "subject": form.subject or "Contact Form Submission", "message": form.message, "created_at": datetime.now(timezone.utc).isoformat()}
    await db.contact_messages.insert_one(contact_doc)
    admin_email = os.environ.get('ADMIN_EMAIL', os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com'))
    await send_email_notification(admin_email, "Contact: " + (form.subject or form.name), "<p><b>From:</b> " + form.name + " (" + form.email + ")</p><p><b>Message:</b> " + form.message + "</p>")
    await send_email_notification(form.email, "We received your message \u2014 Everyday Horoscope", "<p>Hi " + form.name + ", we received your message and will respond within 2 business days.</p>")
    return {"success": True, "message": "Message received."}

@api_router.post("/admin/contact/reply")
async def admin_reply_to_contact(request: Request, body: AdminReplyRequest):
    await require_admin(request, db)
    reply_html = ('<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px;"><h2 style="color: #B8960C;">\u2728 Everyday Horoscope Support</h2><p>Hi ' + body.to_name + ',</p><div style="white-space: pre-wrap; line-height: 1.6; color: #333;">' + body.message + '</div><hr style="margin: 24px 0; border-color: #eee;"/><p style="color: #888; font-size: 12px;">SkyHound Studios \u00b7 Delhi, India</p></div>')
    sent = await send_email_notification(body.to_email, body.subject, reply_html)
    if not sent: raise HTTPException(status_code=500, detail="Failed to send reply. Check RESEND_API_KEY configuration.")
    return {"success": True, "message": "Reply sent to " + body.to_email}

# ── Subscriber Management ─────────────────────────────────────────────────────

@api_router.get("/admin/subscribers")
async def list_subscribers(request: Request, tag: Optional[str] = None, active_only: bool = True):
    await require_admin(request, db)
    query: dict = {}
    if active_only: query["active"] = True
    if tag: query["tags"] = tag
    subs = await db.subscribers.find(query, {"_id": 0}).sort("created_at", -1).to_list(5000)
    return {"subscribers": subs, "total": len(subs)}

@api_router.post("/admin/subscribers")
async def add_subscriber(request: Request, sub: AddSubscriberRequest):
    await require_admin(request, db)
    if sub.email:
        existing = await db.subscribers.find_one({"email": sub.email})
        if existing: raise HTTPException(status_code=400, detail="Subscriber with this email already exists")
    doc = Subscriber(name=sub.name, email=sub.email, phone=sub.phone, tags=sub.tags)
    await db.subscribers.insert_one(doc.model_dump())
    return {"success": True, "subscriber": doc.model_dump()}

@api_router.put("/admin/subscribers/{subscriber_id}")
async def update_subscriber(request: Request, subscriber_id: str, updates: UpdateSubscriberRequest):
    await require_admin(request, db)
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not update_data: raise HTTPException(status_code=400, detail="No update data provided")
    result = await db.subscribers.update_one({"id": subscriber_id}, {"$set": update_data})
    if result.matched_count == 0: raise HTTPException(status_code=404, detail="Subscriber not found")
    return {"success": True}

@api_router.delete("/admin/subscribers/{subscriber_id}")
async def delete_subscriber(request: Request, subscriber_id: str):
    await require_admin(request, db)
    result = await db.subscribers.delete_one({"id": subscriber_id})
    if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Subscriber not found")
    return {"success": True}

# ── Notification Dispatch Helpers ──────────────────────────────────────────────

async def _resolve_audience(audience: str, tags: list) -> list:
    query: dict = {"active": True}
    if audience == "tagged" and tags:
        query["tags"] = {"$in": tags}
    return await db.subscribers.find(query, {"_id": 0}).to_list(10000)

async def _dispatch_notifications(subject: str, body: str, channels: list, subscribers: list, notification_id: Optional[str] = None) -> list:
    logs = []
    for sub in subscribers:
        for channel in channels:
            log = NotificationLog(subject=subject, channel=channel, recipient_name=sub["name"], notification_id=notification_id)
            if channel == "email":
                if not sub.get("email"):
                    log.status = "failed"; log.error = "No email address"
                else:
                    log.recipient_email = sub["email"]
                    branded = _branded_email(sub["name"], body)
                    ok = await send_email_notification(sub["email"], subject, branded)
                    log.status = "sent" if ok else "failed"
                    if not ok: log.error = "Resend API error"
            elif channel == "whatsapp":
                phone = sub.get("phone", "").strip()
                log.recipient_phone = phone
                if not phone:
                    log.status = "failed"; log.error = "No phone number"
                else:
                    ok = await send_whatsapp_message(phone, body, sub.get("name", "there"))
                    log.status = "sent" if ok else "failed"
                    if not ok: log.error = "WhatsApp Cloud API error"
            else:
                log.status = "failed"; log.error = f"Unknown channel: {channel}"
            logs.append(log)
    if logs:
        await db.notification_logs.insert_many([l.model_dump() for l in logs])
    return logs

# ── Notification Endpoints ─────────────────────────────────────────────────────

@api_router.post("/admin/notify/send")
async def send_notification_now(request: Request, payload: NotificationRequest):
    await require_admin(request, db)
    subscribers = await _resolve_audience(payload.audience, payload.tags)
    if not subscribers: raise HTTPException(status_code=400, detail="No active subscribers match the audience filter")
    logs = await _dispatch_notifications(payload.subject, payload.body, payload.channels, subscribers)
    sent  = sum(1 for l in logs if l.status == "sent")
    failed= sum(1 for l in logs if l.status == "failed")
    return {"success": True, "sent": sent, "failed": failed, "total": len(logs)}

@api_router.post("/admin/notify/schedule")
async def schedule_notification(request: Request, payload: NotificationRequest):
    await require_admin(request, db)
    if not payload.scheduled_at: raise HTTPException(status_code=400, detail="scheduled_at is required for scheduling")
    doc = ScheduledNotification(subject=payload.subject, body=payload.body, channels=payload.channels,
                                audience=payload.audience, tags=payload.tags, scheduled_at=payload.scheduled_at)
    await db.scheduled_notifications.insert_one(doc.model_dump())
    return {"success": True, "scheduled": doc.model_dump()}

@api_router.get("/admin/notify/scheduled")
async def list_scheduled_notifications(request: Request):
    await require_admin(request, db)
    docs = await db.scheduled_notifications.find({"status": "pending"}, {"_id": 0}).sort("scheduled_at", 1).to_list(500)
    return {"scheduled": docs}

@api_router.delete("/admin/notify/scheduled/{notification_id}")
async def cancel_scheduled_notification(request: Request, notification_id: str):
    await require_admin(request, db)
    result = await db.scheduled_notifications.update_one(
        {"id": notification_id, "status": "pending"}, {"$set": {"status": "cancelled"}})
    if result.matched_count == 0: raise HTTPException(status_code=404, detail="Notification not found or already sent")
    return {"success": True}

@api_router.get("/admin/notify/logs")
async def get_notification_logs(request: Request, limit: int = 200):
    await require_admin(request, db)
    logs = await db.notification_logs.find({}, {"_id": 0}).sort("sent_at", -1).to_list(limit)
    return {"logs": logs, "total": len(logs)}

# ── Social Media Posting ───────────────────────────────────────────────────────

class SocialPostRequest(BaseModel):
    message: str
    image_url: Optional[str] = None
    channels: List[str] = ["facebook"]   # "facebook" | "instagram" (future)

class SocialPostResult(BaseModel):
    channel: str
    success: bool
    post_id: Optional[str] = None
    error: Optional[str] = None

async def _get_page_access_token(system_token: str, page_id: str) -> str:
    """Exchange a System User token for a Page-scoped access token.
    The /photos and /feed endpoints require a Page token, not a User/System token."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"https://graph.facebook.com/v19.0/{page_id}",
                params={"fields": "access_token", "access_token": system_token},
            )
            data = r.json()
            page_token = data.get("access_token")
            if page_token:
                logging.info("Successfully exchanged system token for page token")
                return page_token
            logging.warning("Could not get page token: %s", data)
    except Exception as e:
        logging.warning("Page token exchange failed: %s", e)
    # Fall back to the system token if exchange fails
    return system_token

async def _post_to_facebook(message: str, image_url: Optional[str] = None) -> SocialPostResult:
    page_id      = os.environ.get("FACEBOOK_PAGE_ID", "")
    system_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    if not page_id or not system_token:
        return SocialPostResult(channel="facebook", success=False, error="Facebook credentials not configured")
    # Exchange system user token → page access token (required for posting)
    page_token = await _get_page_access_token(system_token, page_id)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if image_url:
                r = await client.post(
                    f"https://graph.facebook.com/v19.0/{page_id}/photos",
                    params={"access_token": page_token},
                    json={"url": image_url, "caption": message, "published": True},
                )
            else:
                r = await client.post(
                    f"https://graph.facebook.com/v19.0/{page_id}/feed",
                    params={"access_token": page_token},
                    json={"message": message},
                )
        data = r.json()
        if "id" in data:
            return SocialPostResult(channel="facebook", success=True, post_id=data["id"])
        err = data.get("error", {}).get("message", "Unknown error")
        return SocialPostResult(channel="facebook", success=False, error=err)
    except Exception as e:
        return SocialPostResult(channel="facebook", success=False, error=str(e))

async def _post_to_instagram(message: str, image_url: Optional[str] = None) -> SocialPostResult:
    ig_id      = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
    page_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    if not ig_id or not page_token:
        return SocialPostResult(channel="instagram", success=False, error="Instagram credentials not configured")
    if not image_url:
        return SocialPostResult(channel="instagram", success=False, error="Instagram requires an image")
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Step 1: create media container
            r1 = await client.post(
                f"https://graph.facebook.com/v19.0/{ig_id}/media",
                params={"access_token": page_token},
                json={"image_url": image_url, "caption": message},
            )
            d1 = r1.json()
            if "id" not in d1:
                err = d1.get("error", {}).get("message", "Failed to create media container")
                return SocialPostResult(channel="instagram", success=False, error=err)
            container_id = d1["id"]
            # Step 2: publish
            r2 = await client.post(
                f"https://graph.facebook.com/v19.0/{ig_id}/media_publish",
                params={"access_token": page_token},
                json={"creation_id": container_id},
            )
            d2 = r2.json()
            if "id" in d2:
                return SocialPostResult(channel="instagram", success=True, post_id=d2["id"])
            err = d2.get("error", {}).get("message", "Failed to publish")
            return SocialPostResult(channel="instagram", success=False, error=err)
    except Exception as e:
        return SocialPostResult(channel="instagram", success=False, error=str(e))

async def _post_image_to_facebook(image_bytes: bytes, filename: str, caption: str) -> SocialPostResult:
    """Upload raw image bytes directly to Facebook Page -- no third-party hosting needed."""
    page_id      = os.environ.get("FACEBOOK_PAGE_ID", "")
    system_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    if not page_id or not system_token:
        return SocialPostResult(channel="facebook", success=False, error="Facebook credentials not configured")
    # Exchange system user token → page access token (required for posting)
    page_token = await _get_page_access_token(system_token, page_id)
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"https://graph.facebook.com/v19.0/{page_id}/photos",
                params={"access_token": page_token},
                data={"caption": caption},
                files={"source": (filename, image_bytes, "image/png")},
            )
        data = r.json()
        if "id" in data:
            return SocialPostResult(channel="facebook", success=True, post_id=data["id"])
        err = data.get("error", {}).get("message", "Unknown error")
        return SocialPostResult(channel="facebook", success=False, error=err)
    except Exception as e:
        return SocialPostResult(channel="facebook", success=False, error=str(e))

async def _youtube_upload_task(image_bytes: bytes, message: str):
    """Background task: encode + upload to YouTube, then save to post log."""
    result = await _post_image_to_youtube(image_bytes, title=message[:100], description=message)
    log_doc = {"channel": result.channel, "success": result.success, "post_id": result.post_id,
               "error": result.error, "message_preview": message[:100],
               "posted_at": datetime.now(timezone.utc).isoformat()}
    await db.social_post_logs.insert_one(log_doc)
    logging.info(f"[YouTube] Background task complete -- success={result.success} post_id={result.post_id} error={result.error}")

@api_router.post("/admin/social/post-image")
async def post_image_to_social(
    request: Request,
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    message: str = Form(""),
    channels: str = Form("facebook"),
):
    """Accept a binary image from the browser (html2canvas output) and post it to social channels.
    Facebook/Instagram run synchronously; YouTube runs as a background task to avoid request timeouts."""
    await require_admin(request, db)
    image_bytes = await image.read()
    channel_list = [c.strip() for c in channels.split(",") if c.strip()]
    results = []
    yt_queued = False
    for channel in channel_list:
        if channel == "facebook":
            results.append(await _post_image_to_facebook(image_bytes, image.filename or "card.png", message))
        elif channel == "youtube":
            # YouTube encode + upload can take 2-4 minutes -- run in background to avoid browser timeout
            background_tasks.add_task(_youtube_upload_task, image_bytes, message)
            results.append(SocialPostResult(channel="youtube", success=True,
                                            post_id="queued",
                                            error="Uploading in background (~2 min) -- check Post History to confirm"))
            yt_queued = True
        elif channel == "instagram":
            results.append(SocialPostResult(channel="instagram", success=False, error="Direct image upload for Instagram coming soon"))
        else:
            results.append(SocialPostResult(channel=channel, success=False, error="Channel not supported"))
    # Log sync results immediately; YouTube background task logs itself when done
    log_docs = [{"channel": r.channel, "success": r.success, "post_id": r.post_id,
                 "error": r.error, "message_preview": message[:100],
                 "posted_at": datetime.now(timezone.utc).isoformat()} for r in results if r.post_id != "queued"]
    if log_docs:
        await db.social_post_logs.insert_many(log_docs)
    if yt_queued:
        logging.info("[YouTube] Upload queued as background task -- response returned immediately")
    return {"results": [r.model_dump() for r in results]}

@api_router.post("/admin/social/post")
async def post_to_social(request: Request, payload: SocialPostRequest):
    await require_admin(request, db)
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")
    results = []
    for channel in payload.channels:
        if channel == "facebook":
            results.append(await _post_to_facebook(payload.message, payload.image_url))
        elif channel == "instagram":
            results.append(await _post_to_instagram(payload.message, payload.image_url))
        else:
            results.append(SocialPostResult(channel=channel, success=False, error="Channel not yet supported"))
    # Log to DB
    log_docs = [{"channel": r.channel, "success": r.success, "post_id": r.post_id,
                 "error": r.error, "message_preview": payload.message[:100],
                 "posted_at": datetime.now(timezone.utc).isoformat()} for r in results]
    await db.social_post_logs.insert_many(log_docs)
    return {"results": [r.model_dump() for r in results]}

@api_router.get("/admin/social/logs")
async def get_social_logs(request: Request, limit: int = 100):
    await require_admin(request, db)
    logs = await db.social_post_logs.find({}, {"_id": 0}).sort("posted_at", -1).to_list(limit)
    return {"logs": logs, "total": len(logs)}

# ── YouTube Integration ────────────────────────────────────────────────────────
YOUTUBE_SCOPES   = ["https://www.googleapis.com/auth/youtube.upload"]
_yt_executor     = ThreadPoolExecutor(max_workers=2)

async def _get_youtube_service():
    """Return (service, error_str). Loads refresh token from MongoDB then env."""
    if not GOOGLE_LIBS_AVAILABLE:
        return None, "Google API libraries not installed on server"
    client_id     = os.environ.get("YOUTUBE_CLIENT_ID", "")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return None, "YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET not set on Render"
    token_doc     = await db.app_settings.find_one({"key": "youtube_refresh_token"})
    refresh_token = (token_doc or {}).get("value") or os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
    if not refresh_token:
        return None, "YouTube not connected -- click 'Connect YouTube Channel' in Admin Console"
    def _build():
        creds = GoogleCredentials(
            token=None, refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id, client_secret=client_secret,
            scopes=YOUTUBE_SCOPES,
        )
        creds.refresh(GoogleRequest())
        return google_build("youtube", "v3", credentials=creds)
    try:
        loop = asyncio.get_event_loop()
        svc  = await loop.run_in_executor(_yt_executor, _build)
        return svc, None
    except Exception as e:
        return None, f"YouTube auth error: {e}"

async def _image_bytes_to_mp4(image_bytes: bytes, duration: int = 30) -> bytes:
    """Convert PNG image to MP4 (static image video) using ffmpeg."""
    img_fd, img_path = tempfile.mkstemp(suffix=".png")
    vid_fd, vid_path = tempfile.mkstemp(suffix=".mp4")
    try:
        with os.fdopen(img_fd, "wb") as f:
            f.write(image_bytes)
        os.close(vid_fd)
        logging.info(f"[YouTube] ffmpeg encoding started -- input {len(image_bytes)//1024} KB, duration {duration}s")
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-c:v", "libx264",
            "-preset", "veryfast",    # fast encode + good compression → small file → fast upload
            "-crf", "18",             # high quality (0=lossless · 18=near-lossless · 23=default)
            "-tune", "stillimage",    # optimised for static image input
            "-threads", "1",          # cap CPU so health-checks stay responsive
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-movflags", "+faststart",
            vid_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            err_msg = stderr.decode()[-500:]
            logging.error(f"[YouTube] ffmpeg failed (rc={proc.returncode}): {err_msg}")
            raise RuntimeError(f"ffmpeg failed: {err_msg}")
        with open(vid_path, "rb") as f:
            video_bytes = f.read()
        logging.info(f"[YouTube] ffmpeg encoding complete -- output {len(video_bytes)//1024} KB")
        return video_bytes
    finally:
        try: os.unlink(img_path)
        except: pass
        try: os.unlink(vid_path)
        except: pass

async def _post_image_to_youtube(image_bytes: bytes, title: str, description: str) -> SocialPostResult:
    """Convert image to 30-second video and upload to YouTube."""
    logging.info("[YouTube] Starting upload pipeline")
    svc, err = await _get_youtube_service()
    if not svc:
        logging.error(f"[YouTube] Auth failed: {err}")
        return SocialPostResult(channel="youtube", success=False, error=err)
    try:
        video_bytes = await _image_bytes_to_mp4(image_bytes, duration=30)
        body = {
            "snippet": {
                "title": (title or "Daily Panchang | EverydayHoroscope")[:100],
                "description": description or "",
                "tags": ["Panchang", "VedicAstrology", "EverydayHoroscope",
                         "HinduCalendar", "DailyHoroscope", "Nakshatra"],
                "categoryId": "22",           # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
                "madeForKids": False,
            },
        }
        def _upload():
            logging.info(f"[YouTube] Uploading {len(video_bytes)//1024} KB MP4 to YouTube API")
            media = MediaIoBaseUpload(
                io.BytesIO(video_bytes), mimetype="video/mp4",
                resumable=True, chunksize=5 * 1024 * 1024,
            )
            req = svc.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                status, resp = req.next_chunk()
                if status:
                    logging.info(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")
            return resp
        loop    = asyncio.get_event_loop()
        resp    = await loop.run_in_executor(_yt_executor, _upload)
        vid_id  = resp.get("id", "")
        logging.info(f"[YouTube] Upload complete -- video ID: {vid_id}")
        return SocialPostResult(channel="youtube", success=True, post_id=vid_id)
    except Exception as e:
        logging.error(f"[YouTube] Upload failed: {e}", exc_info=True)
        return SocialPostResult(channel="youtube", success=False, error=str(e))

# YouTube OAuth endpoints ──────────────────────────────────────────────────────
@api_router.get("/admin/youtube/status")
async def youtube_status(request: Request):
    await require_admin(request, db)
    token_doc  = await db.app_settings.find_one({"key": "youtube_refresh_token"})
    has_token  = bool((token_doc or {}).get("value") or os.environ.get("YOUTUBE_REFRESH_TOKEN", ""))
    has_creds  = bool(os.environ.get("YOUTUBE_CLIENT_ID") and os.environ.get("YOUTUBE_CLIENT_SECRET"))
    return {
        "connected":      has_token and has_creds,
        "has_credentials": has_creds,
        "connected_at":   (token_doc or {}).get("updated_at"),
        "libs_available": GOOGLE_LIBS_AVAILABLE,
    }

@api_router.get("/admin/youtube/auth-url")
async def youtube_auth_url(request: Request):
    await require_admin(request, db)
    client_id    = os.environ.get("YOUTUBE_CLIENT_ID", "")
    client_secret= os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    redirect_uri = os.environ.get("YOUTUBE_REDIRECT_URI", "")
    if not client_id or not client_secret:
        raise HTTPException(400, "YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET not set on Render")
    if not redirect_uri:
        raise HTTPException(400, "YOUTUBE_REDIRECT_URI not set on Render")
    if not GOOGLE_LIBS_AVAILABLE:
        raise HTTPException(500, "Google API libraries not installed on server")
    flow = GoogleFlow.from_client_config(
        {"web": {
            "client_id": client_id, "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri],
        }},
        scopes=YOUTUBE_SCOPES,
        redirect_uri=redirect_uri,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent",
    )
    return {"auth_url": auth_url}

@api_router.get("/admin/youtube/callback")
async def youtube_callback(code: str = "", error: str = ""):
    if error:
        return HTMLResponse(f"""<html><body style="font-family:sans-serif;text-align:center;
        padding:40px;background:#111;color:#fff;">
        <h2>❌ Authorization Failed</h2><p style="color:#f87171">{error}</p>
        <script>setTimeout(()=>window.close(),3000);</script></body></html>""")
    client_id     = os.environ.get("YOUTUBE_CLIENT_ID", "")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    redirect_uri  = os.environ.get("YOUTUBE_REDIRECT_URI", "")
    if not GOOGLE_LIBS_AVAILABLE:
        return HTMLResponse("<html><body>Google libraries not available on server</body></html>")
    try:
        flow = GoogleFlow.from_client_config(
            {"web": {
                "client_id": client_id, "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }},
            scopes=YOUTUBE_SCOPES,
            redirect_uri=redirect_uri,
        )
        flow.fetch_token(code=code)
        creds         = flow.credentials
        refresh_token = creds.refresh_token
        if refresh_token:
            await db.app_settings.update_one(
                {"key": "youtube_refresh_token"},
                {"$set": {"key": "youtube_refresh_token", "value": refresh_token,
                          "updated_at": datetime.now(timezone.utc).isoformat()}},
                upsert=True,
            )
            return HTMLResponse("""<html><body style="font-family:sans-serif;text-align:center;
            padding:40px;background:#111;color:#fff;">
            <h2 style="color:#4ade80">✅ YouTube Connected!</h2>
            <p>Your channel is now linked to EverydayHoroscope.</p>
            <p style="color:#9ca3af">This tab will close automatically...</p>
            <script>
            if(window.opener){window.opener.postMessage({type:'youtube_connected'},'*');}
            setTimeout(()=>window.close(),2000);
            </script></body></html>""")
        else:
            return HTMLResponse("""<html><body style="font-family:sans-serif;text-align:center;
            padding:40px;background:#111;color:#fff;">
            <h2 style="color:#fbbf24">⚠️ No Refresh Token</h2>
            <p>Try revoking access at
            <a href="https://myaccount.google.com/permissions" style="color:#facc15">
            myaccount.google.com/permissions</a> then reconnect.</p>
            <script>setTimeout(()=>window.close(),5000);</script></body></html>""")
    except Exception as e:
        return HTMLResponse(f"""<html><body style="font-family:sans-serif;text-align:center;
        padding:40px;background:#111;color:#fff;">
        <h2>❌ Error</h2><p style="color:#f87171">{e}</p>
        <script>setTimeout(()=>window.close(),4000);</script></body></html>""")

@api_router.post("/admin/youtube/disconnect")
async def youtube_disconnect(request: Request):
    await require_admin(request, db)
    await db.app_settings.delete_one({"key": "youtube_refresh_token"})
    return {"message": "YouTube disconnected"}


@api_router.get("/admin/gmail/status")
async def gmail_status(request: Request):
    await require_admin(request, db)
    token_doc = await db.app_settings.find_one({"key": "gmail_refresh_token"})
    has_token = bool((token_doc or {}).get("value") or os.environ.get("GMAIL_REFRESH_TOKEN", ""))
    has_creds = bool(os.environ.get("GMAIL_CLIENT_ID") and os.environ.get("GMAIL_CLIENT_SECRET"))
    support_email = os.environ.get("SUPPORT_EMAIL", "")
    business_state = os.environ.get("BUSINESS_STATE", "")
    return {
        "connected": has_token and has_creds,
        "has_credentials": has_creds,
        "connected_at": (token_doc or {}).get("updated_at"),
        "support_email": support_email,
        "business_state": business_state,
        "libs_available": GOOGLE_LIBS_AVAILABLE,
    }


@api_router.get("/admin/gmail/auth-url")
async def gmail_auth_url(request: Request):
    await require_admin(request, db)
    client_id = os.environ.get("GMAIL_CLIENT_ID", "")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        raise HTTPException(400, "GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET not set on Render")
    if not GOOGLE_LIBS_AVAILABLE:
        raise HTTPException(500, "Google API libraries not installed on server")

    redirect_uri = _build_gmail_redirect_uri(request)
    flow = GoogleFlow.from_client_config(
        _gmail_client_config(redirect_uri),
        scopes=GMAIL_SCOPES,
        redirect_uri=redirect_uri,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return {"auth_url": auth_url}


@api_router.get("/admin/gmail/callback", name="gmail_callback")
async def gmail_callback(request: Request, code: str = "", error: str = ""):
    if error:
        return HTMLResponse(f"""<html><body style="font-family:sans-serif;text-align:center;
        padding:40px;background:#111;color:#fff;">
        <h2>Authorization Failed</h2><p style="color:#f87171">{error}</p>
        <script>setTimeout(()=>window.close(),3000);</script></body></html>""")

    if not GOOGLE_LIBS_AVAILABLE:
        return HTMLResponse("<html><body>Google libraries not available on server</body></html>")

    try:
        redirect_uri = _build_gmail_redirect_uri(request)
        flow = GoogleFlow.from_client_config(
            _gmail_client_config(redirect_uri),
            scopes=GMAIL_SCOPES,
            redirect_uri=redirect_uri,
        )
        flow.fetch_token(code=code)
        creds = flow.credentials
        refresh_token = creds.refresh_token
        if refresh_token:
            await db.app_settings.update_one(
                {"key": "gmail_refresh_token"},
                {
                    "$set": {
                        "key": "gmail_refresh_token",
                        "value": refresh_token,
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
                upsert=True,
            )
            return HTMLResponse("""<html><body style="font-family:sans-serif;text-align:center;
            padding:40px;background:#111;color:#fff;">
            <h2 style="color:#4ade80">Connected!</h2>
            <p>Gmail access is now linked to EverydayHoroscope.</p>
            <p style="color:#9ca3af">This tab will close automatically...</p>
            <script>
            if(window.opener){window.opener.postMessage({type:'gmail_connected'},'*');}
            setTimeout(()=>window.close(),2000);
            </script></body></html>""")

        return HTMLResponse("""<html><body style="font-family:sans-serif;text-align:center;
        padding:40px;background:#111;color:#fff;">
        <h2 style="color:#fbbf24">No Refresh Token</h2>
        <p>Revoke the previous grant and reconnect to issue a fresh offline token.</p>
        <script>setTimeout(()=>window.close(),5000);</script></body></html>""")
    except Exception as exc:
        return HTMLResponse(f"""<html><body style="font-family:sans-serif;text-align:center;
        padding:40px;background:#111;color:#fff;">
        <h2>Error</h2><p style="color:#f87171">{exc}</p>
        <script>setTimeout(()=>window.close(),4000);</script></body></html>""")


@api_router.post("/admin/gmail/disconnect")
async def gmail_disconnect(request: Request):
    await require_admin(request, db)
    await db.app_settings.delete_one({"key": "gmail_refresh_token"})
    return {"message": "Gmail disconnected"}

@api_router.post("/admin/login")
async def admin_login(request: AdminLoginRequest, response: Response):
    if request.username != ADMIN_USERNAME: raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_admin_password(request.password): raise HTTPException(status_code=401, detail="Invalid credentials")
    session_token = await create_admin_session(db)
    set_admin_session_cookie(response, session_token)
    return AdminLoginResponse(success=True, token=session_token, message="Login successful")

@api_router.post("/admin/logout")
async def admin_logout(request: Request, response: Response):
    session_token = request.cookies.get("admin_session")
    if session_token: await db.admin_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("admin_session", path="/")
    return {"message": "Logged out successfully"}

@api_router.post("/admin/change-password")
async def change_admin_password(request: Request, password_request: ChangePasswordRequest):
    await require_admin(request, db)
    if not verify_admin_password(password_request.current_password): raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(password_request.new_password) < 8: raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
    update_admin_password(password_request.new_password)
    new_hash = hash_new_password(password_request.new_password)
    await db.admin_settings.update_one({"key": "admin_password_hash"}, {"$set": {"value": new_hash}}, upsert=True)
    return {"success": True, "message": "Password changed successfully"}

@api_router.get("/admin/verify")
async def verify_admin(request: Request): return {"authenticated": await require_admin(request, db)}


@api_router.get("/admin/diagnostics/{search_value}")
async def get_user_diagnostics(request: Request, search_value: str):
    await require_admin(request, db)

    resolved_user_id, user_doc, payment_email = await _resolve_diagnostics_lookup(search_value)
    if not resolved_user_id:
        raise HTTPException(status_code=400, detail="Search value is required")

    doc = await db["user_diagnostics"].find_one({"_id": resolved_user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No telemetry found for this user")

    events = doc.get("event_stream", [])
    unique_pages = len({event.get("page_url") for event in events if event.get("page_url")})
    error_count = sum(
        1
        for event in events
        if "ERROR" in event.get("event_type", "") or "CRASH" in event.get("event_type", "")
    )

    last_payment = None
    if payment_email:
        last_payment = await db.payments.find_one(
            {"user_email": payment_email},
            {"_id": 0, "status": 1, "report_type": 1, "created_at": 1, "amount": 1, "razorpay_order_id": 1},
            sort=[("created_at", -1)],
        )

    response = _serialize_document(doc)
    response["user_id"] = resolved_user_id
    response["user_email"] = payment_email or (user_doc.get("email") if user_doc else None)
    response["quick_stats"] = {
        "total_events": len(events),
        "unique_pages": unique_pages,
        "error_count": error_count,
        "last_payment_status": last_payment.get("status") if last_payment else None,
    }
    response["last_payment"] = _serialize_document(last_payment) if last_payment else None
    return response


@api_router.patch("/admin/diagnostics/{search_value}/flag")
async def flag_diagnostics_dispute(request: Request, search_value: str, payload: DiagnosticFlagRequest):
    await require_admin(request, db)

    resolved_user_id, _, _ = await _resolve_diagnostics_lookup(search_value)
    if not resolved_user_id:
        raise HTTPException(status_code=400, detail="Search value is required")

    result = await db["user_diagnostics"].update_one(
        {"_id": resolved_user_id},
        {"$set": {"is_claim_flagged": payload.flagged, "last_updated": utc_now()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="No telemetry found for this user")
    return {"status": "updated", "flagged": payload.flagged}


@api_router.get("/admin/orders/{search_value}")
async def get_user_orders(request: Request, search_value: str):
    await require_admin(request, db)

    resolved_user_id, _, payment_email = await _resolve_diagnostics_lookup(search_value)
    if not resolved_user_id:
        raise HTTPException(status_code=400, detail="Search value is required")

    query: Dict[str, Any] = {"user_id": resolved_user_id}
    if payment_email:
        query = {"$or": [{"user_id": resolved_user_id}, {"user_email": payment_email}]}

    orders = await db["orders_ledger"].find(query).sort("ts_cart_add", -1).to_list(50)
    return [_serialize_document(order) for order in orders]


@api_router.post("/admin/self-heal/force-trigger")
async def force_heal_order(
    request: Request,
    payload: ForceHealOrderRequest,
    background_tasks: BackgroundTasks,
):
    await require_admin(request, db)
    background_tasks.add_task(_fulfil_order, payload.order_id)
    return {"status": "re-queued", "order_id": payload.order_id}


@api_router.get("/admin/gst/ledger")
async def get_gst_ledger(
    request: Request,
    type: str,
    page: int = 1,
    page_size: int = 20,
):
    await require_admin(request, db)
    page = max(page, 1)
    page_size = max(1, min(page_size, 100))
    skip = (page - 1) * page_size
    query = {"ledger_type": type}
    items = await db["gst_recon_ledger"].find(query).sort("transaction_date", -1).skip(skip).limit(page_size).to_list(page_size)
    total = await db["gst_recon_ledger"].count_documents(query)
    return {
        "entries": [_serialize_document(item) for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@api_router.get("/admin/gst/summary")
async def get_gst_summary(request: Request):
    await require_admin(request, db)
    summary = await db["app_settings"].find_one({"_id": "gst_daily_summary"}, {"_id": 0}) or {}
    return _serialize_document(summary)


@api_router.patch("/admin/gst/ledger/{entry_id}/status")
async def update_gst_recon_status(request: Request, entry_id: str, status: str):
    await require_admin(request, db)
    allowed = {"MATCHED", "DISCREPANCY_FOUND", "PENDING_RECON"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail=f"Status must be one of {sorted(allowed)}")
    result = await db["gst_recon_ledger"].update_one(
        {"_id": entry_id},
        {"$set": {"reconciliation_status": status}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="GST ledger entry not found")
    return {"status": "updated"}

@api_router.get("/admin/dashboard")
async def get_dashboard_stats(request: Request):
    await require_admin(request, db)
    today_iso = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    revenue_result = await db.payments.aggregate([{"$match": {"status": "completed"}}, {"$group": {"_id": None, "total": {"$sum": "$amount"}}}]).to_list(1)
    return DashboardStats(total_users=await db.users.count_documents({}), total_payments=await db.payments.count_documents({}), total_revenue=revenue_result[0]['total'] if revenue_result else 0, total_birth_charts=await db.birth_chart_reports.count_documents({}), total_kundali_milans=await db.kundali_milan_reports.count_documents({}), active_subscriptions=await db.subscriptions.count_documents({"status": "active"}), users_today=await db.users.count_documents({"created_at": {"$gte": today_iso}}), payments_today=await db.payments.count_documents({"created_at": {"$gte": today_iso}}))

@api_router.get("/admin/users")
async def get_all_users(request: Request, skip: int = 0, limit: int = 100):
    await require_admin(request, db)
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    user_list = []
    for user in users:
        created_at = user.get('created_at', '')
        if hasattr(created_at, 'isoformat'): created_at = created_at.isoformat()
        user_list.append(UserListItem(user_id=user.get('user_id', ''), email=user.get('email', ''), name=user.get('name', ''), picture=user.get('picture'), google_id=user.get('google_id'), created_at=str(created_at), has_password=bool(user.get('password_hash')), is_restricted=bool(user.get('is_restricted', False)), is_suspended=bool(user.get('is_suspended', False)), suspended_until=str(user['suspended_until']) if user.get('suspended_until') else None, locked_until=str(user['locked_until']) if user.get('locked_until') else None, failed_attempts=int(user.get('failed_attempts', 0))))
    return {"users": user_list, "total": await db.users.count_documents({}), "skip": skip, "limit": limit}

@api_router.get("/admin/payments")
async def get_all_payments(request: Request, skip: int = 0, limit: int = 100):
    await require_admin(request, db)
    payments = await db.payments.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    payment_list = []
    for payment in payments:
        created_at = payment.get('created_at', '')
        if hasattr(created_at, 'isoformat'): created_at = created_at.isoformat()
        payment_list.append(PaymentListItem(id=payment.get('id', ''), user_email=payment.get('user_email', ''), report_type=payment.get('report_type', ''), amount=payment.get('amount', 0), status=payment.get('status', ''), razorpay_order_id=payment.get('razorpay_order_id', ''), razorpay_payment_id=payment.get('razorpay_payment_id'), created_at=str(created_at)))
    return {"payments": payment_list, "total": await db.payments.count_documents({}), "skip": skip, "limit": limit}

@api_router.get("/admin/reports")
async def get_all_reports(request: Request, skip: int = 0, limit: int = 100):
    await require_admin(request, db)
    birth_charts = await db.birth_chart_reports.find({}, {"_id": 0}).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    kundali_milans = await db.kundali_milan_reports.find({}, {"_id": 0}).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    def serialize_doc(doc): return {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in doc.items()}
    return {"birth_charts": [serialize_doc(r) for r in birth_charts], "kundali_milans": [serialize_doc(r) for r in kundali_milans], "total_birth_charts": await db.birth_chart_reports.count_documents({}), "total_kundali_milans": await db.kundali_milan_reports.count_documents({})}

@api_router.delete("/admin/user/{user_id}")
async def delete_user(request: Request, user_id: str):
    await require_admin(request, db)
    result = await db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0: raise HTTPException(status_code=404, detail="User not found")
    await db.user_sessions.delete_many({"user_id": user_id})
    return {"message": "User deleted successfully"}

class UserActionRequest(BaseModel):
    action: str

@api_router.post("/admin/user/{user_id}/action")
async def user_action(request: Request, user_id: str, body: UserActionRequest):
    await require_admin(request, db)
    user = await db.users.find_one({"user_id": user_id})
    if not user: raise HTTPException(status_code=404, detail="User not found")
    action = body.action
    if action == "restrict": update = {"$set": {"is_restricted": True}}; msg = "User restricted"
    elif action == "unrestrict": update = {"$unset": {"is_restricted": ""}}; msg = "Restriction removed"
    elif action == "suspend":
        suspend_until = datetime.now(timezone.utc) + timedelta(hours=24)
        update = {"$set": {"is_suspended": True, "suspended_until": suspend_until.isoformat()}}; msg = "User suspended 24hrs"
        await send_email_notification(user.get('email', ''), "Your account has been suspended", "<p>Hi " + user.get('name', 'User') + ", your account has been suspended for 24 hours.</p>")
    elif action == "unsuspend": update = {"$unset": {"is_suspended": "", "suspended_until": ""}}; msg = "User unsuspended"
    else: raise HTTPException(status_code=400, detail="Invalid action")
    await db.users.update_one({"user_id": user_id}, update)
    return {"success": True, "message": msg}

@api_router.get("/admin/contacts")
async def get_contact_messages(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    messages = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    return {"messages": messages, "total": await db.contact_messages.count_documents({})}

def generate_slug(title: str) -> str:
    import re
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-') or 'post'

@api_router.post("/admin/blog")
async def create_blog_post(request: Request, post: BlogPostCreate):
    await require_admin(request, db)
    slug = post.slug if post.slug else generate_slug(post.title)
    if await db.blog_posts.find_one({"slug": slug}): slug = slug + "-" + str(uuid.uuid4())[:8]
    blog_post = BlogPost(title=post.title, slug=slug, excerpt=post.excerpt, content=post.content, author=post.author, category=post.category, tags=post.tags, featured_image=post.featured_image, video_url=post.video_url, published=post.published, scheduled_at=post.scheduled_at)
    doc = blog_post.model_dump(mode='json')
    await db.blog_posts.insert_one(doc)
    return {"success": True, "post": doc}

@api_router.get("/admin/blog")
async def get_all_blog_posts_admin(request: Request, skip: int = 0, limit: int = 100):
    await require_admin(request, db)
    posts = await db.blog_posts.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    for p in posts:
        for field in ['created_at', 'updated_at', 'scheduled_at']:
            if field in p and hasattr(p[field], 'isoformat'): p[field] = p[field].isoformat()
    return {"posts": posts, "total": await db.blog_posts.count_documents({}), "skip": skip, "limit": limit}

@api_router.put("/admin/blog/{post_id}")
async def update_blog_post(request: Request, post_id: str, post: BlogPostUpdate):
    await require_admin(request, db)
    update_data = {k: v for k, v in post.model_dump(mode='json').items() if v is not None}
    if 'title' in update_data and 'slug' not in update_data: update_data['slug'] = generate_slug(update_data['title'])
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.blog_posts.update_one({"id": post_id}, {"$set": update_data})
    if result.matched_count == 0: raise HTTPException(status_code=404, detail="Blog post not found")
    return {"success": True, "message": "Post updated"}

@api_router.delete("/admin/blog/{post_id}")
async def delete_blog_post(request: Request, post_id: str):
    await require_admin(request, db)
    result = await db.blog_posts.delete_one({"id": post_id})
    if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Blog post not found")
    return {"success": True, "message": "Post deleted"}

@api_router.get("/blog")
async def get_published_blog_posts(skip: int = 0, limit: int = 10, category: str = None):
    query = {"published": True}
    if category: query["category"] = category
    posts = await db.blog_posts.find(query, {"_id": 0, "content": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    return {"posts": posts, "total": await db.blog_posts.count_documents(query), "skip": skip, "limit": limit}

@api_router.get("/blog/{slug}")
async def get_blog_post_by_slug(slug: str):
    post = await db.blog_posts.find_one({"slug": slug, "published": True}, {"_id": 0})
    if not post: raise HTTPException(status_code=404, detail="Blog post not found")
    await db.blog_posts.update_one({"slug": slug}, {"$inc": {"views": 1}})
    return post

@api_router.get("/blog/categories/list")
async def get_blog_categories(): return {"categories": await db.blog_posts.distinct("category", {"published": True})}

class UpdateProfileRequest(BaseModel):
    name: str

class ChangeUserPasswordRequest(BaseModel):
    current_password: str; new_password: str

@api_router.put("/auth/profile")
async def update_profile(request: Request, body: UpdateProfileRequest):
    user = await get_current_user(request, db)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    name = body.name.strip()
    if not name or len(name) < 2: raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    await db.users.update_one({"user_id": user.user_id}, {"$set": {"name": name}})
    return {"message": "Profile updated", "name": name}

@api_router.put("/auth/change-password")
async def change_user_password(request: Request, body: ChangeUserPasswordRequest):
    user = await get_current_user(request, db)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    user_doc = await db.users.find_one({"user_id": user.user_id})
    if not user_doc: raise HTTPException(status_code=404, detail="User not found")
    if not user_doc.get("password_hash"): raise HTTPException(status_code=400, detail="Password change not available for Google sign-in accounts")
    if not verify_password(body.current_password, user_doc["password_hash"]): raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(body.new_password) < 8: raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
    await db.users.update_one({"user_id": user.user_id}, {"$set": {"password_hash": hash_password(body.new_password)}})
    return {"message": "Password changed successfully"}

@api_router.get("/auth/my-payments")
async def get_my_payments(request: Request):
    user = await get_current_user(request, db)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    payments = await db.payments.find({"user_email": user.email}, {"_id": 0}).sort("created_at", -1).limit(50).to_list(50)
    result = []
    for p in payments:
        created_at = p.get("created_at", "")
        if hasattr(created_at, "isoformat"): created_at = created_at.isoformat()
        result.append({"id": p.get("id", ""), "report_type": p.get("report_type", ""), "amount": p.get("amount", 0), "status": p.get("status", ""), "created_at": str(created_at)})
    return {"payments": result}


@api_router.post("/knowledge/generate-narrative", response_model=KnowledgeNarrativeResponse)
async def generate_knowledge_narrative(payload: KnowledgeNarrativeRequest, request: Request):
    try:
        engine = getattr(request.app.state, "knowledge_engine", None)
        if engine is None:
            engine = await configure_default_knowledge_engine(db)
            request.app.state.knowledge_engine = engine
            request.app.state.knowledge_index_store = engine.index_store

        matched_rules = await engine.scan_chart(
            chart=payload.chart,
            categories=payload.categories or None,
            max_rules=payload.max_rules,
            context=payload.context,
        )
        return await engine.generate_narrative(
            matched_rules=matched_rules,
            chart=payload.chart,
            context=payload.context,
            user_context=payload.user_context,
            author_voice_id=payload.author_voice_id,
            tension_blocks=payload.tension_blocks,
            model=payload.model,
        )
    except Exception as exc:
        logging.error("Knowledge narrative endpoint failed: %s", exc)
        return KnowledgeNarrativeResponse(
            rule_count=0,
            matched_domains=[],
            narratives=[],
            author_voice_id=payload.author_voice_id,
            model=payload.model,
            error=f"Knowledge narrative request failed: {exc}",
        )


async def upsert_arc_angel_profile(db, user_id: str, profile_data: dict) -> None:
    await db.user_arc_angel_profile.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True,
    )


def _arc_angel_windows_response(profile: dict, *, cached: bool) -> dict:
    domains = profile.get("domains") or []
    overall_confidence = int(profile.get("overall_confidence_pct") or ARC_ANGEL_BASELINE_CONFIDENCE_PCT)
    return {
        "overall_confidence_pct": overall_confidence,
        "engine_label": profile.get("engine_label") or ARC_ANGEL_ENGINE_LABEL,
        "domain_quality_now": {
            str(domain.get("domain_id") or ""): str(domain.get("period_quality") or "neutral")
            for domain in domains
            if domain.get("domain_id")
        },
        "arc_angel_windows": [
            {
                "domain_id": domain.get("domain_id"),
                "domain_label": domain.get("domain_label"),
                "auspicious_periods": domain.get("auspicious_periods", []),
                "inauspicious_periods": domain.get("inauspicious_periods", []),
                "period_quality_now": domain.get("period_quality", "neutral"),
                "confidence_pct": int(domain.get("confidence_pct") or overall_confidence),
                "domain_confidence_pct": int(domain.get("domain_confidence_pct") or ARC_ANGEL_BASELINE_CONFIDENCE_PCT),
                "has_quality_badge": bool(domain.get("has_quality_badge")),
            }
            for domain in domains
        ],
        "cached": cached,
    }


async def _questionnaire_runtime_state(user_id: str | None) -> dict:
    if not user_id:
        return {"completed": False, "beta": 1.0, "gamma": 1.0, "focus_domains": [], "modules_used": 0}
    profile = await db.user_questionnaire_profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not profile or not profile.get("completed"):
        return {"completed": False, "beta": 1.0, "gamma": 1.0, "focus_domains": [], "modules_used": 0}
    return {
        "completed": True,
        "beta": float(profile.get("beta") or 1.0),
        "gamma": float(profile.get("gamma") or 1.0),
        "focus_domains": list(profile.get("focus_domains") or []),
        "modules_used": int(profile.get("modules_used") or 0),
    }


def _arc_angel_confidence_breakdown(profile: dict) -> dict:
    return {
        "birth_data": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
        "questionnaire": int(round(float((profile.get("pillar_1") or {}).get("score") or 0))),
        "module_usage": int((profile.get("pillar_2") or {}).get("score") or 0),
    }


@api_router.get("/knowledge-engine/arc-angel-windows")
async def get_arc_angel_windows(
    birth_date: str,
    birth_time: str,
    birth_place: str,
    request: Request,
    horizon_years: int = 10,
    user_id: str | None = None,
):
    if horizon_years < 1 or horizon_years > 20:
        raise HTTPException(status_code=400, detail="horizon_years must be between 1 and 20")
    try:
        engine = getattr(request.app.state, "knowledge_engine", None)
        if engine is None:
            engine = await configure_default_knowledge_engine(db)
            request.app.state.knowledge_engine = engine
            request.app.state.knowledge_index_store = engine.index_store

        chart_data = calculate_vedic_chart(
            date_of_birth=birth_date,
            time_of_birth=birth_time,
            place_of_birth=birth_place,
        )
        session_user = getattr(request.state, "user", None) or {}
        effective_user_id = user_id or session_user.get("user_id")
        questionnaire_state = await _questionnaire_runtime_state(effective_user_id)
        existing_profile = None
        data_completeness = build_arc_angel_data_completeness()
        if effective_user_id:
            existing_profile = await db.user_arc_angel_profile.find_one({"user_id": effective_user_id}, {"_id": 0})
            if existing_profile:
                data_completeness = build_arc_angel_data_completeness(
                    questionnaire_areas=((existing_profile.get("pillar_1") or {}).get("areas_completed") or []),
                    modules_run=((existing_profile.get("pillar_2") or {}).get("reports_run") or []),
                    parents_data=bool(((existing_profile.get("data_completeness") or {}).get("parents_data"))),
                )
                if arc_angel_profile_is_fresh(existing_profile, data_completeness):
                    response = _arc_angel_windows_response(existing_profile, cached=True)
                    response["questionnaire_completed"] = questionnaire_state["completed"]
                    response["confidence_breakdown"] = _arc_angel_confidence_breakdown(existing_profile)
                    return response
        moon_longitude = chart_data.get("moon_longitude")
        if not isinstance(moon_longitude, (int, float)):
            raise HTTPException(status_code=500, detail="Chart payload missing moon_longitude")
        dasha_timeline = build_dasha_timeline(birth_date, float(moon_longitude))
        matched_rules = await engine.scan_chart(
            chart=chart_data,
            max_rules=2000,
            context={
                "backbone_science_id": "vedic_astrology",
                "beta": questionnaire_state["beta"],
                "gamma": questionnaire_state["gamma"],
            },
            dasha_timeline=dasha_timeline,
        )
        domain_rule_map = build_domain_rule_map(matched_rules)
        domain_quality_now = compute_period_quality_now(
            dasha_timeline=dasha_timeline,
            domain_matched_rules=domain_rule_map,
        )
        raw_windows = compute_arc_angel_windows(
            dasha_timeline=dasha_timeline,
            domain_matched_rules=domain_rule_map,
            horizon_years=horizon_years,
        )
        # Build enriched list (TD-29 Integrated Approach -- Legacy Model baseline active).
        arc_angel_list = [
            {
                "domain_id": domain_id,
                "domain_label": ARC_ANGEL_DOMAIN_LABELS.get(domain_id, domain_id),
                "auspicious_periods": raw_windows.get(domain_id, {}).get("auspicious_periods", []),
                "inauspicious_periods": raw_windows.get(domain_id, {}).get("inauspicious_periods", []),
                "period_quality_now": domain_quality_now.get(domain_id, "neutral"),
                "confidence_pct": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
            }
            for domain_id in ARC_ANGEL_DOMAIN_SLUGS
        ]
        response = {
            "overall_confidence_pct": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
            "engine_label": ARC_ANGEL_ENGINE_LABEL,
            "domain_quality_now": domain_quality_now,
            "arc_angel_windows": arc_angel_list,
            "questionnaire_completed": questionnaire_state["completed"],
            "confidence_breakdown": {
                "birth_data": ARC_ANGEL_BASELINE_CONFIDENCE_PCT,
                "questionnaire": 0,
                "module_usage": 0,
            },
            "cached": False,
        }
        if not effective_user_id:
            return response
        profile_doc = build_arc_angel_profile_doc(
            user_id=effective_user_id,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            domain_quality_now=domain_quality_now,
            raw_windows=raw_windows,
            data_completeness=data_completeness,
            existing_profile=existing_profile,
        )
        await upsert_arc_angel_profile(db, effective_user_id, profile_doc)
        response = _arc_angel_windows_response(profile_doc, cached=False)
        response["questionnaire_completed"] = questionnaire_state["completed"]
        response["confidence_breakdown"] = _arc_angel_confidence_breakdown(profile_doc)
        return response
    except HTTPException:
        raise
    except Exception as exc:
        logging.error("Arc Angel windows endpoint failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to compute Arc Angel windows: {exc}")


@api_router.get("/knowledge-engine/arc-angel-profile/{user_id}")
async def get_arc_angel_profile(user_id: str):
    profile = await db.user_arc_angel_profile.find_one({"user_id": user_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Arc Angel profile not found")
    return profile

app.include_router(api_router)
app.include_router(panchang_router)
app.include_router(crystal_router, prefix="/api")
app.include_router(seo_router)
app.include_router(seo_m3_router)
app.include_router(compatibility_router)
app.include_router(numerology_router)
app.include_router(tarot_router)
app.include_router(kundali_router)
app.include_router(karmic_debt_router)
app.include_router(career_blueprint_router)
app.include_router(shadow_self_router)
app.include_router(retrograde_survival_router)
app.include_router(life_cycles_router)
app.include_router(wealth_blueprint_router)
app.include_router(romance_creative_router)
app.include_router(vitality_health_router)
app.include_router(partnership_window_router)
app.include_router(dharma_purpose_router)
app.include_router(gains_network_router)
app.include_router(ir_enhancement_router)
app.include_router(encounter_window_router)
app.include_router(love_weather_router)
app.include_router(date_night_router)
app.include_router(digital_dating_router)
app.include_router(intimacy_vitality_router)
app.include_router(lunar_cycle_router)
app.include_router(soul_connection_router)
app.include_router(venus_retrograde_router)
app.include_router(soulmate_timing_router)
app.include_router(ritual_trigger_router)
app.include_router(notification_preferences_router)
app.include_router(notification_feed_router)
app.include_router(notification_push_router)
app.include_router(notification_trigger_router)
app.include_router(notification_log_router)
app.include_router(lumina_router)
app.include_router(palmistry_router)
app.include_router(rudraksha_router)
app.include_router(knowledge_router)
app.include_router(lk_router)
app.include_router(strategist_router)
app.include_router(kp_router)
app.include_router(remedies_router)
app.include_router(remedy_matching_router)
app.include_router(live_tv_router)
app.include_router(punya_rewards_router)
app.include_router(lo_shu_router)
app.include_router(zibu_router, prefix="/api/seo")
app.include_router(angel_numbers_router, prefix="/api/seo")
if _longevity_router_ok and longevity_router is not None:
    app.include_router(longevity_router)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_scheduled_notifications():
    """Dispatches any pending scheduled notifications whose time has arrived."""
    now_iso = datetime.now(timezone.utc).isoformat()
    pending = await db.scheduled_notifications.find(
        {"status": "pending", "scheduled_at": {"$lte": now_iso}}, {"_id": 0}
    ).to_list(100)
    for notif in pending:
        try:
            subs = await _resolve_audience(notif["audience"], notif.get("tags", []))
            await _dispatch_notifications(notif["subject"], notif["body"], notif["channels"], subs, notif["id"])
            await db.scheduled_notifications.update_one({"id": notif["id"]}, {"$set": {"status": "sent"}})
            logging.info("Scheduled notification sent: %s", notif["id"])
        except Exception as e:
            logging.error("Failed to send scheduled notification %s: %s", notif["id"], str(e))

async def _call_notification_trigger(trigger_path: str, payload: dict) -> None:
    """Internal helper -- calls a notification trigger endpoint from APScheduler."""
    trigger_key = os.getenv("TEMPLE_TRIGGER_KEY", "")
    if not trigger_key:
        logging.warning("TEMPLE_TRIGGER_KEY not set -- skipping notification trigger: %s", trigger_path)
        return
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:8000/api/notifications/trigger/{trigger_path}",
                headers={"X-Temple-Trigger-Key": trigger_key, "Content-Type": "application/json"},
                json=payload,
                timeout=120,
            )
        logging.info("Notification trigger %s → %s", trigger_path, response.status_code)
    except Exception as exc:
        logging.error("Notification trigger %s failed: %s", trigger_path, str(exc))


async def notification_trigger_panchang_daily():
    """Daily Panchang digest -- runs at 00:00 UTC (5:30 AM IST)."""
    await _call_notification_trigger("panchang-daily", {"audience": "all"})


async def notification_trigger_encounter_window():
    """Encounter window check -- runs at 01:00 UTC (6:30 AM IST) daily."""
    await _call_notification_trigger("encounter-window", {"audience": "all"})


async def notification_trigger_love_weather_weekly():
    """Weekly Love Weather summary -- runs every Sunday at 02:00 UTC (7:30 AM IST)."""
    await _call_notification_trigger("love-weather-weekly", {"audience": "all"})


async def notification_trigger_date_night_score():
    """Date Night score -- runs at 12:30 UTC (6:00 PM IST) daily."""
    await _call_notification_trigger("date-night-score", {"audience": "all"})


async def arc_angel_pillar3_decay_scheduler():
    updated = await run_arc_angel_pillar3_decay_job(db)
    logging.info("Arc Angel pillar 3 decay job updated %d profiles", updated)


async def prefetch_all_horoscopes():
    logging.info("Starting scheduled horoscope prefetch...")
    signs = [s["id"] for s in ZODIAC_SIGNS]; types = ["daily", "tomorrow", "weekly", "monthly"]; generated = skipped = 0
    for horoscope_type in types:
        prediction_date = get_prediction_date(horoscope_type)
        for sign in signs:
            try:
                if await db.horoscopes.find_one({"sign": sign, "type": horoscope_type, "prediction_date": prediction_date}): skipped += 1; continue
                content = await generate_horoscope_with_llm(sign, horoscope_type)
                horoscope = Horoscope(sign=sign, type=horoscope_type, content=content, prediction_date=prediction_date)
                await db.horoscopes.insert_one(horoscope.model_dump(mode='json')); generated += 1
            except Exception as e: logging.error("Failed to generate %s for %s: %s", horoscope_type, sign, str(e))
    logging.info("Horoscope prefetch complete: %d generated, %d already cached", generated, skipped)


async def ensure_diagnostics_indexes():
    await db["user_diagnostics"].create_index(
        [("_id", 1), ("last_updated", -1)],
        name="idx_user_lookup_timeline",
    )
    await db["user_diagnostics"].create_index(
        [("event_stream.timestamp", -1)],
        name="idx_event_time",
    )


async def ensure_orders_ledger_indexes():
    await db["orders_ledger"].create_index(
        [("current_state", 1), ("ts_cart_add", -1)],
        name="idx_funnel_state",
    )
    await db["orders_ledger"].create_index(
        [("razorpay_order_id", 1)],
        unique=True,
        sparse=True,
        name="idx_razorpay_webhook_match",
    )
    await db["orders_ledger"].create_index(
        [("current_state", 1)],
        partialFilterExpression={"current_state": "PAID"},
        name="idx_stuck_fulfillment",
    )
    await db["orders_ledger"].create_index(
        [("user_id", 1), ("ts_cart_add", -1)],
        name="idx_user_orders",
    )


async def ensure_gst_ledger_indexes():
    await db["gst_recon_ledger"].create_index(
        [("reconciliation_status", 1), ("transaction_date", -1)],
        name="idx_gst_recon_status",
    )
    await db["gst_recon_ledger"].create_index(
        [("ledger_type", 1), ("transaction_date", -1)],
        name="idx_gst_type_date",
    )


async def evict_stale_carts():
    threshold = utc_now() - timedelta(hours=48)
    await db["orders_ledger"].delete_many({
        "current_state": {"$in": ["CART_ADD", "CHECKOUT_INIT"]},
        "ts_cart_add": {"$lt": threshold},
    })


async def heal_stuck_orders():
    threshold = utc_now() - timedelta(minutes=30)
    cursor = db["orders_ledger"].find({
        "current_state": "PAID",
        "ts_pmt_success": {"$lt": threshold},
        "ts_fulfill_done": None,
    })
    async for order in cursor:
        await _fulfil_order(order["_id"])


async def ingest_vendor_emails():
    from services.gmail_ingest import fetch_vendor_emails
    from services.gst_parser import extract_gst_from_pdf

    emails = await fetch_vendor_emails(db)
    for email in emails:
        extracted = extract_gst_from_pdf(email["pdf_bytes"])
        if extracted["total_value"] <= 0:
            continue

        total_value = round(float(extracted["total_value"]), 2)
        taxable_value = round(total_value / 1.18, 2)
        igst = round(total_value * 0.18 / 1.18, 2)
        entry_id = f"SUP-{utc_now().strftime('%Y%m%d')}-{email['message_id'][:6]}"
        await db["gst_recon_ledger"].update_one(
            {"source_email_id": email["message_id"]},
            {
                "$setOnInsert": {
                    "_id": entry_id,
                    "ledger_type": "CREDIT_SUPPLIER_B2B",
                    "party_name": email["sender"],
                    "party_gstin": extracted["vendor_gstin"],
                    "transaction_date": utc_now(),
                    "taxable_value": taxable_value,
                    "cgst": 0.0,
                    "sgst": 0.0,
                    "igst": igst,
                    "total_invoice_value": total_value,
                    "reconciliation_status": "PENDING_RECON",
                    "source_email_id": email["message_id"],
                    "notes": email["subject"],
                }
            },
            upsert=True,
        )


async def generate_gst_summary():
    today = utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
    pipeline = [
        {"$match": {"transaction_date": {"$gte": today - timedelta(days=1), "$lt": today}}},
        {"$group": {
            "_id": "$ledger_type",
            "total_taxable": {"$sum": "$taxable_value"},
            "total_cgst": {"$sum": "$cgst"},
            "total_sgst": {"$sum": "$sgst"},
            "total_igst": {"$sum": "$igst"},
            "total_invoice": {"$sum": "$total_invoice_value"},
            "count": {"$sum": 1},
        }},
    ]
    summary_rows = await db["gst_recon_ledger"].aggregate(pipeline).to_list(10)
    totals = {
        row["_id"]: {
            "count": row.get("count", 0),
            "total_taxable": round(row.get("total_taxable", 0.0), 2),
            "total_cgst": round(row.get("total_cgst", 0.0), 2),
            "total_sgst": round(row.get("total_sgst", 0.0), 2),
            "total_igst": round(row.get("total_igst", 0.0), 2),
            "total_invoice": round(row.get("total_invoice", 0.0), 2),
        }
        for row in summary_rows
    }
    await db["app_settings"].update_one(
        {"_id": "gst_daily_summary"},
        {"$set": {"last_run": utc_now(), "summary": totals}},
        upsert=True,
    )


async def triage_support_tickets():
    from services.gmail_ingest import fetch_support_emails

    emails = await fetch_support_emails(db)
    for email in emails:
        sender_email = _normalize_email(email.get("sender_email"))
        user_doc = await db.users.find_one({"email": sender_email}, {"_id": 0, "user_id": 1, "email": 1})
        diagnostic_doc = None
        if user_doc and user_doc.get("user_id"):
            diagnostic_doc = await db["user_diagnostics"].find_one({"_id": user_doc["user_id"]}, {"_id": 0, "is_claim_flagged": 1})
        await db["support_tickets"].update_one(
            {"source_email_id": email["message_id"]},
            {
                "$setOnInsert": {
                    "source_email_id": email["message_id"],
                    "subject": email.get("subject", ""),
                    "sender": email.get("sender", ""),
                    "sender_email": sender_email,
                    "snippet": email.get("snippet", ""),
                    "matched_user_id": (user_doc or {}).get("user_id"),
                    "matched_user_email": (user_doc or {}).get("email"),
                    "diagnostic_flagged": bool((diagnostic_doc or {}).get("is_claim_flagged")),
                    "status": "PENDING_REVIEW",
                    "created_at": utc_now(),
                }
            },
            upsert=True,
        )


scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    app.state.db = db
    try:
        app.state.knowledge_engine = await configure_default_knowledge_engine(db)
        app.state.knowledge_index_store = app.state.knowledge_engine.index_store
    except Exception as exc:
        logging.warning("knowledge engine startup refresh failed: %s", exc)
    await ensure_diagnostics_indexes()
    await ensure_orders_ledger_indexes()
    await ensure_gst_ledger_indexes()
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(hour=18, minute=30, timezone="UTC"), id="daily_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(day_of_week="sun", hour=18, minute=0, timezone="UTC"), id="weekly_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(day=1, hour=17, minute=30, timezone="UTC"), id="monthly_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(send_scheduled_notifications, CronTrigger(minute="*/5"), id="scheduled_notifications", replace_existing=True)
    scheduler.add_job(notification_trigger_panchang_daily, CronTrigger(hour=0, minute=0, timezone="UTC"), id="notif_panchang_daily", replace_existing=True)
    scheduler.add_job(notification_trigger_encounter_window, CronTrigger(hour=1, minute=0, timezone="UTC"), id="notif_encounter_window", replace_existing=True)
    scheduler.add_job(notification_trigger_love_weather_weekly, CronTrigger(day_of_week="sun", hour=2, minute=0, timezone="UTC"), id="notif_love_weather_weekly", replace_existing=True)
    scheduler.add_job(notification_trigger_date_night_score, CronTrigger(hour=12, minute=30, timezone="UTC"), id="notif_date_night_score", replace_existing=True)
    scheduler.add_job(arc_angel_pillar3_decay_scheduler, CronTrigger(hour=20, minute=30, timezone="UTC"), id="arc_angel_pillar3_decay", replace_existing=True)
    scheduler.add_job(evict_stale_carts, CronTrigger(hour=0, minute=0, timezone="UTC"), id="shc_stale_cart_eviction", replace_existing=True)
    scheduler.add_job(heal_stuck_orders, CronTrigger(hour=2, minute=0, timezone="UTC"), id="shc_stuck_order_heal", replace_existing=True)
    scheduler.add_job(ingest_vendor_emails, CronTrigger(hour=4, minute=0, timezone="UTC"), id="shc_vendor_email_ingest", replace_existing=True)
    scheduler.add_job(generate_gst_summary, CronTrigger(hour=6, minute=0, timezone="UTC"), id="shc_gst_daily_summary", replace_existing=True)
    scheduler.add_job(triage_support_tickets, CronTrigger(hour=8, minute=0, timezone="UTC"), id="shc_support_triage", replace_existing=True)
    scheduler.start()
    logging.info("Horoscope prefetch scheduler started")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown(); client.close()
