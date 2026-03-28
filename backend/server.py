from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, UploadFile, File, Form
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Literal, Optional
import uuid
from datetime import datetime, timezone, date, timedelta
import anthropic

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
from pdf_generator import generate_birth_chart_pdf, generate_kundali_milan_pdf, generate_brihat_kundli_pdf, generate_report_password
from vedic_calculator import calculate_vedic_chart, calculate_ashtakoot, check_mangal_dosha, generate_north_indian_chart_svg
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
from panchang_router import router as panchang_router
from numerology_router import router as numerology_router
from tarot_router import router as tarot_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

razorpay_client = razorpay.Client(auth=(
    os.environ.get('RAZORPAY_KEY_ID'),
    os.environ.get('RAZORPAY_KEY_SECRET')
))

PRICING = {
    "birth_chart": 799,
    "brihat_kundli": 1499,
    "kundali_milan": 1199,
    "premium_monthly": 1599
}

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()

# ── Session middleware — populates request.state.user for ALL routers ──────────
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

HoroscopeType = Literal["daily", "weekly", "monthly"]

def get_prediction_date(horoscope_type: str) -> str:
    today = date.today()
    if horoscope_type == "daily": return today.isoformat()
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BirthProfileCreate(BaseModel):
    name: str; date_of_birth: str; time_of_birth: str; location: str

class BirthChartReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: str; report_content: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lagna: dict = {}; moon_sign: dict = {}; nakshatra: dict = {}; current_dasha: dict = {}; chart_svg: str = ""; mangal_dosha: dict = {}

class BirthChartRequest(BaseModel):
    profile_id: str

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
    report_type: str; report_id: Optional[str] = None; user_email: str

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
    channels: List[str]            # ["email"] — WhatsApp added when BSP is wired
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
    # Build template payload — hello_world has no variables; custom templates may add body params
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
    weekly_prompt = ("You are a Vedic astrologer. Generate a weekly horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence summarising the week.\n2. Output EXACTLY these 4 sections:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Lucky Days: [days], Lucky Colour: [colour], Focus Mantra: [mantra]\n4. NO markdown\n5. Each section: 3-4 sentences. Total 180-220 words.\n6. Begin with: \"" + sign_dash + "\"")
    monthly_prompt = ("You are a Vedic astrologer. Generate a monthly horoscope for " + sign + ".\n\nCRITICAL FORMATTING RULES:\n1. Start with one sentence summarising the month.\n2. Output EXACTLY these 4 sections:\n   Love & Relationships:\n   Career & Finances:\n   Health & Wellness:\n   Lucky Elements:\n3. Under Lucky Elements include: Power Dates: [3 dates], Lucky Gemstone: [stone], Monthly Mantra: [mantra]\n4. NO markdown\n5. Each section: 4-5 sentences. Total 250-300 words.\n6. Begin with: \"" + sign_dash + "\"")
    system_prompts = {"daily": daily_prompt, "weekly": weekly_prompt, "monthly": monthly_prompt}
    user_prompts = {"daily": "Generate today's Vedic horoscope for " + sign + ".", "weekly": "Generate this week's Vedic horoscope for " + sign + ".", "monthly": "Generate this month's Vedic horoscope for " + sign + "."}
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
    today = date.today().isoformat()
    existing = await db.horoscopes.find_one({"sign": request.sign, "type": request.type, "prediction_date": today}, {"_id": 0})
    if existing:
        if isinstance(existing['created_at'], str): existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return Horoscope(**existing)
    content = await generate_horoscope_with_llm(request.sign, request.type)
    horoscope = Horoscope(sign=request.sign, type=request.type, content=content, prediction_date=today)
    await db.horoscopes.insert_one(horoscope.model_dump(mode='json'))
    return horoscope

@api_router.get("/horoscope/prefetch-status")
async def prefetch_status():
    daily_date = get_prediction_date('daily'); weekly_date = get_prediction_date('weekly'); monthly_date = get_prediction_date('monthly')
    daily_count = await db.horoscopes.count_documents({'type': 'daily', 'prediction_date': daily_date})
    weekly_count = await db.horoscopes.count_documents({'type': 'weekly', 'prediction_date': weekly_date})
    monthly_count = await db.horoscopes.count_documents({'type': 'monthly', 'prediction_date': monthly_date})
    return {'daily': {'cached': daily_count, 'total': 12, 'date': daily_date}, 'weekly': {'cached': weekly_count, 'total': 12, 'date': weekly_date}, 'monthly': {'cached': monthly_count, 'total': 12, 'date': monthly_date}, 'total_cached': daily_count + weekly_count + monthly_count}

@api_router.get("/horoscope/{sign}/{type}", response_model=Horoscope)
async def get_horoscope(sign: str, type: HoroscopeType):
    valid_signs = [s["id"] for s in ZODIAC_SIGNS]
    if sign not in valid_signs: raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    today = date.today().isoformat()
    horoscope_doc = await db.horoscopes.find_one({"sign": sign, "type": type, "prediction_date": today}, {"_id": 0})
    if horoscope_doc:
        if isinstance(horoscope_doc['created_at'], str): horoscope_doc['created_at'] = datetime.fromisoformat(horoscope_doc['created_at'])
        return Horoscope(**horoscope_doc)
    content = await generate_horoscope_with_llm(sign, type)
    horoscope = Horoscope(sign=sign, type=type, content=content, prediction_date=today)
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
    report = BirthChartReport(profile_id=request.profile_id, report_content=content, lagna=bc_chart_data['lagna'] if bc_chart_data else {}, moon_sign=bc_chart_data['moon_sign'] if bc_chart_data else {}, nakshatra=bc_chart_data['nakshatra'] if bc_chart_data else {}, current_dasha=bc_chart_data.get('current_dasha', {}) if bc_chart_data else {}, mangal_dosha=bc_chart_data.get('mangal_dosha', {}) if bc_chart_data else {}, chart_svg=bc_chart_svg)
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

@api_router.post("/brihat-kundli/generate")
async def generate_brihat_kundli(request: BrihatKundliRequest, user_email: str = ""):
    try:
        chart_data = None
        try: chart_data = calculate_vedic_chart(date_of_birth=request.date_of_birth, time_of_birth=request.time_of_birth, place_of_birth=request.place_of_birth)
        except Exception as ce: logging.warning("Vedic calculator failed for Brihat Kundli: %s", ce)
        chart_svg = ""
        if chart_data and chart_data.get('houses'):
            try: chart_svg = generate_north_indian_chart_svg(chart_data['houses'], chart_data['lagna']['sign'])
            except Exception as se: logging.warning("SVG chart generation failed: %s", se)
        report_data = await generate_brihat_kundli_with_llm(request)
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
        report = BrihatKundliReport(user_email=user_email, full_name=request.full_name, date_of_birth=request.date_of_birth, time_of_birth=request.time_of_birth, place_of_birth=request.place_of_birth, gender=request.gender, ascendant=report_data.get("ascendant", {}), moon_sign=report_data.get("moon_sign", {}), sun_sign=sun_sign, planetary_positions=report_data.get("planetary_positions", []), career_prediction=career, love_prediction=(lambda lp: {**lp, "ideal_partner_traits": lp.get("ideal_partner_traits") or lp.get("ideal_partner") or [], "compatibility_signs": lp.get("compatibility_signs") or lp.get("compatible_signs") or [], "challenging_signs": lp.get("challenging_signs") or []})(report_data.get("love_prediction", {})), health_prediction=health, wealth_prediction=(lambda wp: {**wp, "primary_income_sources": wp.get("primary_income_sources") or wp.get("income_sources") or wp.get("wealth_sources") or [], "good_investments": wp.get("good_investments") or wp.get("investments") or wp.get("peak_periods") or ["Real estate", "Gold", "Equity"], "avoid": wp.get("avoid") or wp.get("cautions") or ["High-risk speculation"]})(report_data.get("wealth_prediction", {})), family_prediction=report_data.get("family_prediction", {}), education_prediction=report_data.get("education_prediction", {}), current_dasha=current_dasha, dasha_timeline=dasha_timeline, mangal_dosha=mangal, kalsarp_dosha=report_data.get("kalsarp_dosha", {}), other_doshas=report_data.get("other_doshas", []), benefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "benefic"] or report_data.get("benefic_yogas", []), malefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "malefic"] or report_data.get("malefic_yogas", []), gemstone_remedies=remedies.get("gemstones", report_data.get("gemstone_remedies", [])), mantra_remedies=remedies.get("mantras", report_data.get("mantra_remedies", [])), lifestyle_remedies=remedies.get("general", report_data.get("lifestyle_remedies", [])), donation_remedies=report_data.get("donation_remedies", []), lucky_numbers=report_data.get("lucky_numbers", []), lucky_colors=report_data.get("lucky_colors", []), lucky_days=report_data.get("lucky_days", []), lucky_direction=report_data.get("lucky_direction", ""), numerology=report_data.get("numerology", {}), chart_svg=chart_svg)
        import json
        doc = json.loads(report.model_dump_json())
        await db.brihat_kundli_reports.insert_one({**doc})
        return {"success": True, "report_id": report.id, "report": doc}
    except Exception as e:
        logging.error("Brihat Kundli generation error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate report: " + str(e))

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

@api_router.post("/payment/create-order")
async def create_payment_order(request: PaymentIntentRequest):
    if request.report_type not in PRICING: raise HTTPException(status_code=400, detail="Invalid report type")
    try:
        amount_paise = int(PRICING[request.report_type] * 100)
        razorpay_order = razorpay_client.order.create({"amount": amount_paise, "currency": "INR", "payment_capture": 1, "notes": {"report_type": request.report_type, "report_id": request.report_id or "", "user_email": request.user_email}})
        payment = Payment(user_email=request.user_email, report_type=request.report_type, report_id=request.report_id or "", amount=PRICING[request.report_type], razorpay_order_id=razorpay_order["id"], status="created")
        await db.payments.insert_one(payment.model_dump(mode='json'))
        return {"order_id": razorpay_order["id"], "amount": PRICING[request.report_type], "currency": "INR", "key_id": os.environ.get('RAZORPAY_KEY_ID')}
    except HTTPException: raise
    except Exception as e: logging.error("Razorpay order creation error: %s", str(e)); raise HTTPException(status_code=500, detail="Payment order creation failed")

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
                reports.append({"id": r["id"], "type": "birth_chart", "type_label": "Birth Chart", "name": pf.get("name", "Unknown"), "subtitle": pf.get('date_of_birth', '') + " \u00b7 " + pf.get('location', ''), "profile_id": r.get("profile_id"), "generated_at": r.get("generated_at"), "lagna": r.get("lagna", {}), "nakshatra": r.get("nakshatra", {})})
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
    return user

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
    """Upload raw image bytes directly to Facebook Page — no third-party hosting needed."""
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

@api_router.post("/admin/social/post-image")
async def post_image_to_social(
    request: Request,
    image: UploadFile = File(...),
    message: str = Form(""),
    channels: str = Form("facebook"),
):
    """Accept a binary image from the browser (html2canvas output) and post it to social channels."""
    await require_admin(request, db)
    image_bytes = await image.read()
    channel_list = [c.strip() for c in channels.split(",") if c.strip()]
    results = []
    for channel in channel_list:
        if channel == "facebook":
            results.append(await _post_image_to_facebook(image_bytes, image.filename or "card.png", message))
        elif channel == "instagram":
            results.append(SocialPostResult(channel="instagram", success=False, error="Direct image upload for Instagram coming soon"))
        else:
            results.append(SocialPostResult(channel=channel, success=False, error="Channel not supported"))
    log_docs = [{"channel": r.channel, "success": r.success, "post_id": r.post_id,
                 "error": r.error, "message_preview": message[:100],
                 "posted_at": datetime.now(timezone.utc).isoformat()} for r in results]
    if log_docs:
        await db.social_post_logs.insert_many(log_docs)
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

app.include_router(api_router)
app.include_router(panchang_router)
app.include_router(numerology_router)
app.include_router(tarot_router)

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

async def prefetch_all_horoscopes():
    logging.info("Starting scheduled horoscope prefetch...")
    signs = [s["id"] for s in ZODIAC_SIGNS]; types = ["daily", "weekly", "monthly"]; generated = skipped = 0
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

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    app.state.db = db
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(hour=18, minute=30, timezone="UTC"), id="daily_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(day_of_week="sun", hour=18, minute=0, timezone="UTC"), id="weekly_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(prefetch_all_horoscopes, CronTrigger(day=1, hour=17, minute=30, timezone="UTC"), id="monthly_horoscope_prefetch", replace_existing=True)
    scheduler.add_job(send_scheduled_notifications, CronTrigger(minute="*/5"), id="scheduled_notifications", replace_existing=True)
    scheduler.start()
    logging.info("Horoscope prefetch scheduler started")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown(); client.close()
