from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Razorpay configuration
razorpay_client = razorpay.Client(auth=(
    os.environ.get('RAZORPAY_KEY_ID'),
    os.environ.get('RAZORPAY_KEY_SECRET')
))

# Pricing in INR (Indian Rupees)
PRICING = {
    "birth_chart": 799,  # ₹799 - Basic
    "brihat_kundli": 1499,  # ₹1499 - Comprehensive detailed report
    "kundali_milan": 1199,  # ₹1199
    "premium_monthly": 1599  # ₹1599/month
}

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# CORS — must be added immediately after app creation, before any routes
cors_origins_env = os.environ.get('CORS_ORIGINS', '')
if cors_origins_env:
    cors_origins = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]
else:
    cors_origins = []

# allow_credentials=True is required for cookie-based auth, but cannot be used with wildcard origins
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Zodiac signs configuration
ZODIAC_SIGNS = [
    {"id": "aries", "name": "Aries", "symbol": "♈", "dates": "Mar 21 - Apr 19", "element": "Fire"},
    {"id": "taurus", "name": "Taurus", "symbol": "♉", "dates": "Apr 20 - May 20", "element": "Earth"},
    {"id": "gemini", "name": "Gemini", "symbol": "♊", "dates": "May 21 - Jun 20", "element": "Air"},
    {"id": "cancer", "name": "Cancer", "symbol": "♋", "dates": "Jun 21 - Jul 22", "element": "Water"},
    {"id": "leo", "name": "Leo", "symbol": "♌", "dates": "Jul 23 - Aug 22", "element": "Fire"},
    {"id": "virgo", "name": "Virgo", "symbol": "♍", "dates": "Aug 23 - Sep 22", "element": "Earth"},
    {"id": "libra", "name": "Libra", "symbol": "♎", "dates": "Sep 23 - Oct 22", "element": "Air"},
    {"id": "scorpio", "name": "Scorpio", "symbol": "♏", "dates": "Oct 23 - Nov 21", "element": "Water"},
    {"id": "sagittarius", "name": "Sagittarius", "symbol": "♐", "dates": "Nov 22 - Dec 21", "element": "Fire"},
    {"id": "capricorn", "name": "Capricorn", "symbol": "♑", "dates": "Dec 22 - Jan 19", "element": "Earth"},
    {"id": "aquarius", "name": "Aquarius", "symbol": "♒", "dates": "Jan 20 - Feb 18", "element": "Air"},
    {"id": "pisces", "name": "Pisces", "symbol": "♓", "dates": "Feb 19 - Mar 20", "element": "Water"}
]

HoroscopeType = Literal["daily", "weekly", "monthly"]

def get_prediction_date(horoscope_type: str) -> str:
    """Get the cache key date for a horoscope type.
    Daily = today's date
    Weekly = Monday of the current week  
    Monthly = first day of current month
    """
    today = date.today()
    if horoscope_type == "daily":
        return today.isoformat()
    elif horoscope_type == "weekly":
        # Monday of current week
        monday = today - timedelta(days=today.weekday())
        return monday.isoformat()
    elif horoscope_type == "monthly":
        # First day of current month
        return today.replace(day=1).isoformat()
    return today.isoformat()

# Define Models
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
    id: str
    name: str
    symbol: str
    dates: str
    element: str

class BirthProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    date_of_birth: str
    time_of_birth: str
    location: str
    user_email: str = ""   # owner — set on creation for My Reports linking
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BirthProfileCreate(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str
    location: str

class BirthChartReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: str
    report_content: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Structured fields for on-screen display (added alongside plain text)
    lagna: dict = {}        # sign, sign_vedic, lord, element
    moon_sign: dict = {}    # sign, sign_vedic
    nakshatra: dict = {}    # name, pada, lord
    current_dasha: dict = {}# planet, start, end
    chart_svg: str = ""     # North Indian chart SVG for on-screen display
    mangal_dosha: dict = {} # has_dosha, mars_house

class BirthChartRequest(BaseModel):
    profile_id: str

# Blog Models
class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    excerpt: str
    content: str
    author: str = "Cosmic Wisdom"
    category: str = "Astrology"
    tags: list = []
    featured_image: str = ""
    video_url: str = ""
    published: bool = False
    views: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogPostCreate(BaseModel):
    title: str
    slug: str = ""
    excerpt: str
    content: str
    author: str = "Cosmic Wisdom"
    category: str = "Astrology"
    tags: list = []
    featured_image: str = ""
    video_url: str = ""
    published: bool = False

class BlogPostUpdate(BaseModel):
    title: str = None
    slug: str = None
    excerpt: str = None
    content: str = None
    author: str = None
    category: str = None
    tags: list = None
    featured_image: str = None
    video_url: str = None
    published: bool = None

# Brihat Kundli Pro Models
class BrihatKundliRequest(BaseModel):
    full_name: str
    date_of_birth: str  # YYYY-MM-DD format
    time_of_birth: str  # HH:MM format (24hr)
    place_of_birth: str
    gender: str  # male/female
    current_city: str = ""
    marital_status: str = ""  # single/married/divorced/widowed

class BrihatKundliReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    full_name: str
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str
    gender: str
    
    # Core Astrological Data
    ascendant: dict = {}  # sign, degree, characteristics
    moon_sign: dict = {}  # sign, nakshatra, pada
    sun_sign: dict = {}
    planetary_positions: list = []  # [{planet, sign, house, degree, status}]
    
    # Life Predictions (structured)
    career_prediction: dict = {}
    love_prediction: dict = {}
    health_prediction: dict = {}
    wealth_prediction: dict = {}
    family_prediction: dict = {}
    education_prediction: dict = {}
    
    # Dasha Periods with Calendar Years
    current_dasha: dict = {}
    dasha_timeline: list = []  # [{dasha, start_year, end_year, predictions}]
    
    # Doshas
    mangal_dosha: dict = {}
    kalsarp_dosha: dict = {}
    other_doshas: list = []
    
    # Yogas
    benefic_yogas: list = []
    malefic_yogas: list = []
    
    # Remedies
    gemstone_remedies: list = []
    mantra_remedies: list = []
    lifestyle_remedies: list = []
    donation_remedies: list = []
    
    # Lucky Elements
    lucky_numbers: list = []
    lucky_colors: list = []
    lucky_days: list = []
    lucky_direction: str = ""
    
    # Numerology
    numerology: dict = {}

    # Visual chart — SVG string for on-screen display
    chart_svg: str = ""
    
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KundaliMilanReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    person1_id: str
    person2_id: str
    compatibility_score: float
    detailed_analysis: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Structured fields for on-screen display
    ashtakoot_details: dict = {}      # Individual koota scores {varna, vashya, tara...}
    chart_svg_person1: str = ""       # North Indian chart SVG for person 1
    chart_svg_person2: str = ""       # North Indian chart SVG for person 2

class KundaliMilanRequest(BaseModel):
    person1_id: str
    person2_id: str

class UserSubscription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    subscription_type: str  # "premium_monthly" or "per_report"
    status: str  # "active", "cancelled", "expired"
    stripe_subscription_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Payment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_email: str
    report_type: str  # "birth_chart" or "kundali_milan"
    report_id: str
    amount: float
    razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None
    status: str  # "created", "completed", "failed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ShareLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    report_type: str  # "birth_chart" or "kundali_milan"
    report_id: str
    views: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactFormRequest(BaseModel):
    name: str
    email: str
    subject: str = ""
    message: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PaymentIntentRequest(BaseModel):
    report_type: str  # "birth_chart", "kundali_milan", or "premium_monthly"
    report_id: Optional[str] = None
    user_email: str

# Email notification helper (uses Resend API)
async def send_email_notification(to_email: str, subject: str, body: str):
    """Send email notification via Resend API — logs if API key not configured"""
    resend_api_key = os.environ.get('RESEND_API_KEY', '')
    from_email = os.environ.get('FROM_EMAIL', 'noreply@everydayhoroscope.in')
    
    if not resend_api_key:
        logging.info(f"[EMAIL NOT SENT - RESEND_API_KEY not set] To: {to_email} | Subject: {subject}")
        logging.info(f"Email body preview: {body[:200]}")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": f"Everyday Horoscope <{from_email}>",
                    "to": [to_email],
                    "subject": subject,
                    "html": body
                }
            )
            if response.status_code == 200:
                logging.info(f"Email sent via Resend to {to_email}: {subject}")
                return True
            else:
                logging.error(f"Resend API error {response.status_code}: {response.text}")
                return False
    except Exception as e:
        logging.error(f"Email send failed: {str(e)}")
        return False

# LLM Integration for horoscope generation using Claude
async def generate_horoscope_with_llm(sign: str, horoscope_type: str) -> str:
    """Generate horoscope using Claude API"""
    
    system_prompts = {
        "daily": f"""You are a Vedic astrologer specialising in Jyotish (Indian astrology). Generate a daily horoscope for {sign} using Vedic astrological principles — Navagraha transits, current Dasha influences, and Nakshatra energy.

CRITICAL FORMATTING RULES — follow exactly:
1. Start with one sentence of overall energy for the day.
2. Then output EXACTLY these 4 sections with EXACTLY these headings on their own line:
   Love & Relationships:
   Career & Finances:
   Health & Wellness:
   Lucky Elements:
3. Under Lucky Elements include: Lucky Number: [number], Lucky Colour: [colour], Lucky Time: [time]
4. NO markdown symbols (no **, no ##, no ---)
5. Each section: 2-3 sentences. Total 120-150 words.
6. Begin with: "{sign} —" as the very first word.""",

        "weekly": f"""You are a Vedic astrologer specialising in Jyotish. Generate a weekly horoscope for {sign} using Vedic principles — weekly planetary transits (Gochar), Vimshottari Dasha phase, and Panchang highlights.

CRITICAL FORMATTING RULES — follow exactly:
1. Start with one sentence summarising the week's overall energy.
2. Then output EXACTLY these 4 sections with EXACTLY these headings on their own line:
   Love & Relationships:
   Career & Finances:
   Health & Wellness:
   Lucky Elements:
3. Under Lucky Elements include: Lucky Days: [days], Lucky Colour: [colour], Focus Mantra: [short mantra]
4. NO markdown symbols (no **, no ##, no ---)
5. Each section: 3-4 sentences. Total 180-220 words.
6. Begin with: "{sign} —" as the very first word.""",

        "monthly": f"""You are a Vedic astrologer specialising in Jyotish. Generate a monthly horoscope for {sign} using Vedic principles — major planetary transits for the month, Mahadasha/Antardasha phase, significant Yoga formations, and auspicious/inauspicious Tithi periods.

CRITICAL FORMATTING RULES — follow exactly:
1. Start with one sentence summarising the month's dominant planetary theme.
2. Then output EXACTLY these 4 sections with EXACTLY these headings on their own line:
   Love & Relationships:
   Career & Finances:
   Health & Wellness:
   Lucky Elements:
3. Under Lucky Elements include: Power Dates: [3 dates], Lucky Gemstone: [stone], Monthly Mantra: [mantra]
4. NO markdown symbols (no **, no ##, no ---)
5. Each section: 4-5 sentences. Total 250-300 words.
6. Begin with: "{sign} —" as the very first word."""
    }

    user_prompts = {
        "daily": f"Generate today's Vedic horoscope for {sign}. Follow the exact format specified.",
        "weekly": f"Generate this week's Vedic horoscope for {sign}. Follow the exact format specified.",
        "monthly": f"Generate this month's Vedic horoscope for {sign}. Follow the exact format specified."
    }
    
    try:
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompts[horoscope_type],
            messages=[
                {"role": "user", "content": user_prompts[horoscope_type]}
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        logging.error(f"Error generating horoscope with LLM: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate horoscope: {str(e)}")

# Routes
@api_router.get("/")
async def root():
    return {"message": "Daily Horoscope API"}

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

@api_router.get("/signs", response_model=List[ZodiacSign])
async def get_zodiac_signs():
    """Get all zodiac signs with their metadata"""
    return ZODIAC_SIGNS

@api_router.post("/horoscope/generate", response_model=Horoscope)
async def generate_horoscope(request: HoroscopeRequest):
    """Generate a new horoscope for a specific sign and type"""
    
    # Validate sign
    valid_signs = [sign["id"] for sign in ZODIAC_SIGNS]
    if request.sign not in valid_signs:
        raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    
    # Get today's date for caching
    today = date.today().isoformat()
    
    # Check if horoscope already exists for today/this week/this month
    existing = await db.horoscopes.find_one(
        {
            "sign": request.sign,
            "type": request.type,
            "prediction_date": today
        },
        {"_id": 0}
    )
    
    if existing:
        if isinstance(existing['created_at'], str):
            existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return Horoscope(**existing)
    
    # Generate new horoscope using LLM
    content = await generate_horoscope_with_llm(request.sign, request.type)
    
    horoscope = Horoscope(
        sign=request.sign,
        type=request.type,
        content=content,
        prediction_date=today
    )
    
    doc = horoscope.model_dump(mode='json')
    await db.horoscopes.insert_one(doc)
    
    return horoscope

@api_router.get("/horoscope/{sign}/{type}", response_model=Horoscope)
async def get_horoscope(sign: str, type: HoroscopeType):
    """Get horoscope for a specific sign and type"""
    
    valid_signs = [s["id"] for s in ZODIAC_SIGNS]
    if sign not in valid_signs:
        raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    
    today = date.today().isoformat()
    
    horoscope_doc = await db.horoscopes.find_one(
        {
            "sign": sign,
            "type": type,
            "prediction_date": today
        },
        {"_id": 0}
    )
    
    if horoscope_doc:
        if isinstance(horoscope_doc['created_at'], str):
            horoscope_doc['created_at'] = datetime.fromisoformat(horoscope_doc['created_at'])
        return Horoscope(**horoscope_doc)
    
    content = await generate_horoscope_with_llm(sign, type)
    
    horoscope = Horoscope(
        sign=sign,
        type=type,
        content=content,
        prediction_date=today
    )
    
    doc = horoscope.model_dump(mode='json')
    await db.horoscopes.insert_one(doc)
    
    return horoscope

# Birth Profile Routes
@api_router.post("/profile/birth", response_model=BirthProfile)
async def create_birth_profile(profile: BirthProfileCreate, request: Request):
    """Create a new birth profile — stores user_email for My Reports linking"""
    profile_data = profile.model_dump(mode='json')
    # Attach user email if logged in (optional — don't fail if not)
    try:
        user = await get_current_user(request, db)
        if user and user.get("email"):
            profile_data["user_email"] = user["email"]
    except Exception:
        pass
    birth_profile = BirthProfile(**profile_data)
    doc = birth_profile.model_dump(mode='json')
    await db.birth_profiles.insert_one(doc)
    return birth_profile

@api_router.get("/profile/birth/{profile_id}", response_model=BirthProfile)
async def get_birth_profile(profile_id: str):
    """Get birth profile by ID"""
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    
    if isinstance(profile['created_at'], str):
        profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    
    return BirthProfile(**profile)

@api_router.get("/profile/birth", response_model=List[BirthProfile])
async def list_birth_profiles():
    """List all birth profiles"""
    profiles = await db.birth_profiles.find({}, {"_id": 0}).to_list(1000)
    
    for profile in profiles:
        if isinstance(profile['created_at'], str):
            profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    
    return profiles

# Birth Chart Generation
async def generate_birth_chart_with_llm(profile: BirthProfile) -> str:
    """
    Generate birth chart report.
    Layer 1: vedic_calculator.py — deterministic planetary positions
    Layer 2: Claude — interprets the calculated positions
    """
    # ── Layer 1: Calculate chart (always deterministic) ──────────────────────
    try:
        chart_data = calculate_vedic_chart(
            date_of_birth=profile.date_of_birth,
            time_of_birth=profile.time_of_birth,
            place_of_birth=profile.location,
        )
        logging.info(f"Vedic chart calculated: Lagna={chart_data['lagna']['sign']}, Moon={chart_data['moon_sign']['sign']}, Nakshatra={chart_data['nakshatra']['name']}")
    except Exception as e:
        logging.error(f"Vedic calculator FAILED for birth chart ({profile.date_of_birth}, {profile.time_of_birth}, {profile.location}): {e}", exc_info=True)
        chart_data = None

    # ── Build structured chart summary for Claude ─────────────────────────────
    if chart_data:
        lagna = chart_data['lagna']
        moon = chart_data['moon_sign']
        nak = chart_data['nakshatra']
        planets = chart_data['planets']
        houses = chart_data['houses']
        current_dasha = chart_data.get('current_dasha', {})
        mangal = chart_data['mangal_dosha']

        # Format planet positions
        planet_lines = []
        for pname, pdata in planets.items():
            retro = " (Retrograde)" if pdata.get('retrograde') else ""
            planet_lines.append(
                f"  - {pname}: {pdata['sign_vedic']}, House {pdata['house']}, "
                f"{pdata['degree']}°{retro}"
            )

        # Format house map
        house_lines = []
        for h_num, h_data in houses.items():
            planets_in = ', '.join(h_data['planets']) if h_data['planets'] else 'Empty'
            house_lines.append(
                f"  House {h_num} — {h_data['name']}: {h_data['sign_vedic']} "
                f"(Lord: {h_data['lord']}) | Planets: {planets_in}"
            )

        chart_summary = f"""
CALCULATED BIRTH CHART DATA (mathematically verified — use these exact values):

Native: {profile.name}
Birth: {profile.date_of_birth} at {profile.time_of_birth}, {profile.location}

ASCENDANT (Lagna): {lagna['sign_vedic']}, {lagna['degree']}°
  Lagna Lord: {lagna['lord']} | Element: {lagna['element']}

MOON SIGN (Rashi): {moon['sign_vedic']}
NAKSHATRA: {nak['name']} (Pada {nak.get('pada', '?')}) | Lord: {nak.get('lord', '?')}

PLANETARY POSITIONS:
{chr(10).join(planet_lines)}

12-HOUSE MAP:
{chr(10).join(house_lines)}

CURRENT DASHA: {current_dasha.get('planet', 'Unknown')} Mahadasha
  Period: {current_dasha.get('start', '?')} to {current_dasha.get('end', '?')}

MANGAL DOSHA: {'YES' if mangal.get('has_dosha') else 'NO'}
  {mangal.get('description', '')}
  Mars in House: {mangal.get('mars_house', '?')}
"""
    else:
        chart_summary = f"Native: {profile.name}, Born: {profile.date_of_birth} at {profile.time_of_birth} in {profile.location}"

    # ── Layer 2: Claude interprets the calculated data ────────────────────────
    system_prompt = """You are an expert Jyotish (Vedic astrology) interpreter. You receive a mathematically calculated birth chart. Your job is ONLY interpretation — never recalculate or change any positions.

CRITICAL RULES:
- Use ONLY the planetary positions and house placements provided — never invent or change them
- EVERY sentence must reference specific planets AND their house numbers (e.g. "Sun in House 1", "Jupiter in House 4")
- Address the native by name throughout
- NO markdown (no **, no ##, no ----)
- Clear section headings followed by a colon, then prose
- MANDATORY SECTIONS IN ORDER:
  Overview:
  Ascendant & Personality:
  Sun Sign & Core Identity:
  Moon Sign & Emotional Nature:
  Planetary Positions & House Analysis:
  Notable Yogas & Planetary Combinations:
  Career & Dharma:
  Relationships & Marriage:
  Health & Wellness:
  Dasha Period Analysis:
  Remedies & Guidance:
- Each section: 3-4 sentences minimum, all grounded in actual house/planet data
- Target 800-1000 words total"""

    user_prompt = f"""Write the complete Janma Kundali (Birth Chart) report for {profile.name} using ONLY the calculated data below.

{chart_summary}

IMPORTANT: Every section must cite specific planets with their house numbers. For example:
- NOT "Saturn's influence brings lessons" 
- YES "Saturn in House 7 indicates lessons through partnerships..."
- NOT "Jupiter blesses you with wisdom"
- YES "Jupiter in House 4 brings wisdom to your home and mother matters..."

Cover all 11 sections in order. Make every statement traceable to the actual chart positions shown above."""

    try:
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text
    except Exception as e:
        logging.error(f"Error generating birth chart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate birth chart: {str(e)}")

@api_router.post("/birthchart/generate", response_model=BirthChartReport)
async def generate_birth_chart(request: BirthChartRequest):
    """Generate comprehensive birth chart report"""
    
    profile = await db.birth_profiles.find_one({"id": request.profile_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    
    if isinstance(profile['created_at'], str):
        profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    
    birth_profile = BirthProfile(**profile)
    
    existing = await db.birth_chart_reports.find_one(
        {"profile_id": request.profile_id},
        {"_id": 0}
    )
    
    if existing:
        if isinstance(existing['generated_at'], str):
            existing['generated_at'] = datetime.fromisoformat(existing['generated_at'])
        return BirthChartReport(**existing)
    
    content = await generate_birth_chart_with_llm(birth_profile)

    # Re-calculate chart data to store structured fields + SVG
    bc_chart_data = None
    try:
        bc_chart_data = calculate_vedic_chart(
            date_of_birth=birth_profile.date_of_birth,
            time_of_birth=birth_profile.time_of_birth,
            place_of_birth=birth_profile.location,
        )
    except Exception as ce:
        logging.warning(f"Chart calc for BirthChartReport structured fields: {ce}")

    bc_chart_svg = ""
    if bc_chart_data and bc_chart_data.get('houses'):
        try:
            from vedic_calculator import generate_north_indian_chart_svg
            bc_chart_svg = generate_north_indian_chart_svg(
                bc_chart_data['houses'],
                bc_chart_data['lagna']['sign']
            )
        except Exception as se:
            logging.warning(f"SVG generation failed for Birth Chart: {se}")

    report = BirthChartReport(
        profile_id=request.profile_id,
        report_content=content,
        lagna=bc_chart_data['lagna'] if bc_chart_data else {},
        moon_sign=bc_chart_data['moon_sign'] if bc_chart_data else {},
        nakshatra=bc_chart_data['nakshatra'] if bc_chart_data else {},
        current_dasha=bc_chart_data.get('current_dasha', {}) if bc_chart_data else {},
        mangal_dosha=bc_chart_data.get('mangal_dosha', {}) if bc_chart_data else {},
        chart_svg=bc_chart_svg,
    )
    
    import json as _json
    doc = _json.loads(report.model_dump_json())
    doc_for_db = {**doc}
    await db.birth_chart_reports.insert_one(doc_for_db)
    
    return report

@api_router.get("/horoscope/prefetch-status")
async def prefetch_status():
    """Check how many horoscopes are pre-cached for today/this week/this month"""
    daily_date = get_prediction_date('daily')
    weekly_date = get_prediction_date('weekly')
    monthly_date = get_prediction_date('monthly')
    
    daily_count = await db.horoscopes.count_documents({'type': 'daily', 'prediction_date': daily_date})
    weekly_count = await db.horoscopes.count_documents({'type': 'weekly', 'prediction_date': weekly_date})
    monthly_count = await db.horoscopes.count_documents({'type': 'monthly', 'prediction_date': monthly_date})
    
    return {
        'daily': {'cached': daily_count, 'total': 12, 'date': daily_date},
        'weekly': {'cached': weekly_count, 'total': 12, 'date': weekly_date},
        'monthly': {'cached': monthly_count, 'total': 12, 'date': monthly_date},
        'total_cached': daily_count + weekly_count + monthly_count
    }

@api_router.get("/birthchart/{profile_id}", response_model=BirthChartReport)
async def get_birth_chart(profile_id: str):
    """Get existing birth chart report"""
    
    report = await db.birth_chart_reports.find_one(
        {"profile_id": profile_id},
        {"_id": 0}
    )
    
    if not report:
        raise HTTPException(status_code=404, detail="Birth chart report not found")
    
    if isinstance(report['generated_at'], str):
        report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    
    return BirthChartReport(**report)

# ============== BRIHAT KUNDLI PRO ==============

async def generate_brihat_kundli_with_llm(request: BrihatKundliRequest) -> dict:
    """
    Generate Brihat Kundli Pro report.
    Layer 1: vedic_calculator.py — full deterministic chart
    Layer 2: Claude — deep interpretation with actual positions
    """
    current_year = datetime.now().year
    birth_year = int(request.date_of_birth.split('-')[0])
    age = current_year - birth_year

    # ── Layer 1: Calculate full chart ───────────────────────────────────────
    chart_data = None
    try:
        chart_data = calculate_vedic_chart(
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            place_of_birth=request.place_of_birth,
        )
    except Exception as e:
        logging.warning(f"Vedic calculator failed for Brihat Kundli: {e}")

    # ── Build detailed chart summary ────────────────────────────────────────
    if chart_data:
        lagna = chart_data['lagna']
        moon = chart_data['moon_sign']
        nak = chart_data['nakshatra']
        planets = chart_data['planets']
        houses = chart_data['houses']
        dashas = chart_data['dashas']
        current_dasha = chart_data.get('current_dasha', {})
        mangal = chart_data['mangal_dosha']

        planet_lines = []
        for pname, pdata in planets.items():
            retro = " (R)" if pdata.get('retrograde') else ""
            planet_lines.append(
                f"  {pname}: {pdata['sign_vedic']} | House {pdata['house']} | "
                f"{pdata['degree']}°{retro} | Lord: {pdata['lord_of_sign']}"
            )

        house_lines = []
        for h_num, h_data in houses.items():
            planets_in = ', '.join(h_data['planets']) if h_data['planets'] else 'Empty'
            house_lines.append(
                f"  H{h_num} {h_data['name']}: {h_data['sign_vedic']} "
                f"| Lord: {h_data['lord']} | {planets_in}"
            )

        dasha_lines = []
        for d in dashas[:6]:
            dasha_lines.append(f"  {d.get('planet','?')} Mahadasha: {d.get('start','?')} — {d.get('end','?')} ({d.get('years',0):.1f} yrs)")

        chart_summary = f"""
CALCULATED BIRTH CHART (mathematically verified — use these exact values):

Native: {request.full_name}, Age: {age}, Gender: {request.gender}
Born: {request.date_of_birth} at {request.time_of_birth}, {request.place_of_birth}

LAGNA: {lagna['sign_vedic']} {lagna['degree']}° | Lord: {lagna['lord']} | Element: {lagna['element']}
MOON (Rashi): {moon['sign_vedic']}
NAKSHATRA: {nak['name']} Pada {nak.get('pada','?')} | Lord: {nak.get('lord','?')} | Deity: {nak.get('deity','?')}

PLANET POSITIONS:
{chr(10).join(planet_lines)}

12-HOUSE MAP:
{chr(10).join(house_lines)}

VIMSHOTTARI DASHA TIMELINE:
{chr(10).join(dasha_lines)}
Current: {current_dasha.get('planet','Unknown')} Mahadasha ({current_dasha.get('start','?')}-{current_dasha.get('end','?')})

MANGAL DOSHA: {'YES' if mangal.get('has_dosha') else 'NO'}
  House: {mangal.get('mars_house','?')} | {mangal.get('description','')}
  Cancellation: {'Yes — ' + mangal.get('cancellation_reason','') if mangal.get('cancelled') else 'No cancellation found'}
"""
    else:
        chart_summary = f"Native: {request.full_name}, Born {request.date_of_birth} at {request.time_of_birth} in {request.place_of_birth}"

    # ── Layer 2: Claude writes comprehensive interpretation ──────────────────
    system_prompt = """You are a senior Jyotish astrologer writing a premium Brihat Kundli Pro report equivalent to a 40-page professional report. You receive a mathematically calculated birth chart. Your job is deep, detailed prose interpretation — never recalculate or change any positions.

CRITICAL RULES:
- Use ONLY the planetary positions and house placements provided — never change them
- Return a VALID JSON object — no text before or after, no markdown fences
- Use specific calendar years in all predictions (current year is """ + str(current_year) + """)
- Address the native by name (""" + request.full_name.split()[0] + """) throughout every section
- EVERY text field must be a detailed prose paragraph of 3-5 sentences minimum
- EVERY array must have at least 5-8 richly detailed items — never return empty arrays
- Write like a professional astrologer, not a bullet-point generator
- NO markdown in JSON string values — plain text only
- house_analysis must cover ALL 12 houses with detailed interpretation for each

Return this EXACT JSON structure with EXACT field names. All string values must be full prose sentences:
{
    "ascendant": {
        "sign": "...", "degree": "...", "lord": "...", "element": "...",
        "overview": "Write 4-5 sentences describing the Lagna, its ruling planet, its effect on personality, appearance, and life approach for this native.",
        "key_traits": ["detailed trait with explanation", "...5 minimum"],
        "strengths": ["detailed strength with context", "...5 minimum"],
        "challenges": ["detailed challenge with advice", "...5 minimum"]
    },
    "moon_sign": {
        "sign": "...", "nakshatra": "...", "nakshatra_pada": "...", "nakshatra_lord": "...",
        "overview": "Write 4-5 sentences on Moon sign effects on emotional nature, mind, mother, and subconscious patterns.",
        "emotional_nature": ["...5 minimum"], "mental_tendencies": ["...5 minimum"]
    },
    "sun_sign": {
        "sign": "...",
        "overview": "Write 3-4 sentences on Sun sign, soul purpose, ego expression, and life theme.",
        "core_identity": ["...4 minimum"], "life_purpose": ["...4 minimum"]
    },
    "planetary_positions": [{"planet": "...", "sign": "...", "house": 1, "degree": "...", "status": "...", "strength": "...", "effects": ["detailed effect 1", "detailed effect 2", "detailed effect 3"]}],
    "house_analysis": [
        {"house": 1, "name": "Lagna — Self & Personality", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "Write 4-5 sentences specific to this house, its sign, lord placement, and any planets in it. Be specific about what it means for this native."},
        {"house": 2, "name": "Dhana — Wealth & Family", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 3, "name": "Sahaja — Siblings & Courage", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 4, "name": "Sukha — Home & Mother", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 5, "name": "Putra — Children & Intellect", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 6, "name": "Ripu — Health & Enemies", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 7, "name": "Kalatra — Marriage & Partnerships", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 8, "name": "Mrityu — Transformation & Longevity", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 9, "name": "Dharma — Fortune & Spirituality", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 10, "name": "Karma — Career & Status", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 11, "name": "Labha — Gains & Aspirations", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."},
        {"house": 12, "name": "Vyaya — Liberation & Foreign Lands", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "4-5 sentences..."}
    ],
    "yogas": [{"name": "...", "type": "benefic", "planets_involved": ["..."], "effect": "Write 2-3 sentences explaining this yoga and its specific effect for this native."}],
    "career_prediction": {
        "overall_rating": "...", "business_potential": "...",
        "overview": "Write 5-6 sentences on career destiny, natural aptitude, best path, and key success periods based on this specific chart.",
        "best_career_fields": ["Field with 2-sentence explanation", "...6 minimum"],
        "strengths_at_work": ["Strength with context", "...6 minimum"],
        "career_timeline": [
            {"period": "2026-2028", "prediction": "Write 3-4 sentences on what this period brings for career.", "advice": "Specific actionable advice for this period."},
            {"period": "2028-2035", "prediction": "...", "advice": "..."},
            {"period": "2035-2047", "prediction": "...", "advice": "..."}
        ]
    },
    "love_prediction": {
        "overall_rating": "...",
        "overview": "Write 5-6 sentences on love life, relationship patterns, marriage destiny, and spouse characteristics based on 7th house analysis.",
        "ideal_partner_traits": ["...6 minimum"],
        "compatibility_signs": ["...", "...", "..."],
        "challenging_signs": ["...", "...", "..."],
        "marriage_timing": {"favorable_years": [2027, 2028, 2029, 2031], "favorable_months": ["..."], "marriage_analysis": "Write 3-4 sentences on marriage timing, likely circumstances of meeting spouse, and married life quality."},
        "married_life": ["...5 minimum"]
    },
    "health_prediction": {
        "overall_vitality": "...", "body_constitution": "...",
        "overview": "Write 4-5 sentences on constitutional health, general vitality, and key health themes for this chart.",
        "vulnerable_areas": ["Area with explanation", "...6 minimum"],
        "preventive_measures": ["Measure with detail", "...6 minimum"],
        "dietary_recommendations": ["...5 minimum"],
        "health_timeline": "Write 3-4 sentences on health patterns across different life stages."
    },
    "wealth_prediction": {
        "overall_rating": "...",
        "overview": "Write 5-6 sentences on wealth destiny, natural wealth-building tendencies, peak prosperity periods, and financial patterns.",
        "primary_income_sources": ["Source with explanation", "...6 minimum"],
        "good_investments": ["Investment with reasoning", "...5 minimum"],
        "avoid": ["...4 minimum"],
        "peak_periods": ["Period with explanation", "...4 minimum"]
    },
    "family_prediction": {
        "overview": "Write 4-5 sentences on family life, relationship with parents, siblings, and children based on the 4th, 3rd, and 5th houses.",
        "parents": "2-3 sentences on parental relationships.",
        "siblings": "2-3 sentences on sibling dynamics.",
        "children": "2-3 sentences on children and progeny."
    },
    "current_dasha": {
        "mahadasha": "Jupiter", "period": "2012 – 2028",
        "overview": "Write 5-6 sentences on what this Mahadasha means overall for this native.",
        "effects": ["...6 minimum"]
    },
    "dasha_timeline": [
        {"planet": "Saturn", "period": "2028 – 2047", "overview": "Write 4-5 sentences on what Saturn Mahadasha will bring for this native.", "effects": ["...5 minimum"]},
        {"planet": "Mercury", "period": "2047 – 2064", "overview": "Write 3-4 sentences.", "effects": ["...4 minimum"]}
    ],
    "mangal_dosha": {"has_dosha": false, "severity": "...", "mars_house": 1, "effects": "Write 3-4 sentences explaining Mangal Dosha effects for this native.", "remedies": ["Detailed remedy with instruction", "...5 minimum"]},
    "kalsarp_dosha": {"has_dosha": false, "severity": "", "remedies": []},
    "benefic_yogas": [{"name": "...", "type": "benefic", "planets_involved": ["..."], "effect": "Write 3 sentences on this yoga and its specific manifestation for this native."}],
    "gemstone_remedies": [{"stone": "...", "planet": "...", "benefit": "2-sentence explanation.", "how_to_wear": "Instructions for wearing."}, "...3 minimum"],
    "mantra_remedies": [{"mantra": "...", "planet": "...", "chanting": "When and how many times.", "benefit": "1-2 sentence benefit."}, "...3 minimum"],
    "lifestyle_remedies": ["Detailed practice with explanation", "...6 minimum"],
    "lucky_numbers": [6, 15, 24],
    "lucky_colors": ["...", "...", "..."],
    "lucky_days": ["...", "...", "..."],
    "lucky_direction": "...",
    "numerology": {
        "life_path": "...", "destiny_number": "...", "soul_number": "...",
        "overview": "Write 4-5 sentences interpreting the numerological profile and how it complements the Vedic chart."
    }
}"""

    user_prompt = f"""Generate a complete Brihat Kundli Pro report for {request.full_name} using ONLY this chart:

{chart_summary}

CRITICAL — TOKEN BUDGET RULES (strictly enforce):
- Return ONLY valid JSON — no markdown, no preamble, no trailing text
- Each "overview" field: 2-3 sentences maximum (not 4-5)
- Each array: 3-5 items maximum (not 8)
- house_analysis: ALL 12 houses, each interpretation 2-3 sentences
- career_timeline: exactly 2 periods
- dasha_timeline: exactly 2 upcoming dashas
- Gemstone remedies: 2-3 stones with brief how-to (1 sentence each)
- Mantra remedies: 2-3 mantras with chanting instruction
- Address {request.full_name.split()[0]} by name throughout
- Complete ALL fields — do not truncate the JSON under any circumstances
- If running low on space, shorten each value rather than omitting keys"""

    try:
        client = anthropic.AsyncAnthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        response_text = message.content[0].text
        import re, json
        clean = re.sub(r'```(?:json)?\s*', '', response_text).replace('```', '').strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError as je:
            logging.error(f"Brihat JSON parse failed: {je}. Attempting repair...")
            try:
                repair = clean
                last_quote = repair.rfind('",')  
                if last_quote > 0:
                    repair = repair[:last_quote+1]
                opens = repair.count('{') - repair.count('}')
                arr_opens = repair.count('[') - repair.count(']')
                repair += ']' * max(0, arr_opens) + '}' * max(0, opens)
                return json.loads(repair)
            except Exception as repair_err:
                logging.error(f"JSON repair also failed: {repair_err}. Raw (first 500): {clean[:500]}")
            return {
                "ascendant": {"sign": "", "key_traits": [], "strengths": [], "challenges": []},
                "moon_sign": {"sign": "", "nakshatra": "", "emotional_nature": [], "mental_tendencies": []},
                "sun_sign": {"sign": "", "core_identity": [], "life_purpose": []},
                "planetary_positions": [],
                "house_analysis": [],
                "yogas": [],
                "career_prediction": {"overall_rating": "", "best_fields": [], "timeline": []},
                "love_prediction": {"overall_rating": "", "marriage_timing": {}, "married_life": []},
                "health_prediction": {"constitution": "", "strong_areas": [], "vulnerable_areas": [], "remedies": []},
                "wealth_prediction": {"overall_rating": "", "wealth_sources": [], "peak_periods": []},
                "dasha_analysis": {"current_dasha": "", "current_effects": [], "upcoming": []},
                "mangal_dosha": {"has_dosha": False, "severity": "", "remedies": []},
                "remedies": {"gemstones": [], "mantras": [], "general": [clean[:2000]]},
            }
    except Exception as e:
        logging.error(f"Error generating Brihat Kundli: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate Brihat Kundli: {str(e)}")

@api_router.post("/brihat-kundli/generate")
async def generate_brihat_kundli(request: BrihatKundliRequest, user_email: str = ""):
    """Generate comprehensive Brihat Kundli Pro report"""
    
    try:
        chart_data = None
        try:
            chart_data = calculate_vedic_chart(
                date_of_birth=request.date_of_birth,
                time_of_birth=request.time_of_birth,
                place_of_birth=request.place_of_birth,
            )
            logging.info(f"Brihat chart calculated: Lagna={chart_data['lagna']['sign']}, Nakshatra={chart_data['nakshatra']['name']}")
        except Exception as ce:
            logging.warning(f"Vedic calculator failed for Brihat Kundli: {ce}")

        chart_svg = ""
        if chart_data and chart_data.get('houses'):
            try:
                from vedic_calculator import generate_north_indian_chart_svg
                chart_svg = generate_north_indian_chart_svg(
                    chart_data['houses'],
                    chart_data['lagna']['sign']
                )
            except Exception as se:
                logging.warning(f"SVG chart generation failed: {se}")

        report_data = await generate_brihat_kundli_with_llm(request)
        
        remedies = report_data.get("remedies", {})
        yogas    = report_data.get("yogas", [])
        dasha    = report_data.get("dasha_analysis", {})

        career = report_data.get("career_prediction", {})
        if career and not career.get("best_career_fields") and career.get("best_fields"):
            career["best_career_fields"] = career.pop("best_fields")
        if career and not career.get("strengths_at_work") and career.get("strengths"):
            career["strengths_at_work"] = career.pop("strengths")
        if career and not career.get("career_timeline") and career.get("timeline"):
            career["career_timeline"] = career.pop("timeline")

        health = report_data.get("health_prediction", {})
        if health and not health.get("overall_vitality") and health.get("constitution"):
            health["overall_vitality"] = health.get("overall_rating", "")
            health["body_constitution"] = health.pop("constitution", "")
        if health and not health.get("preventive_measures") and health.get("remedies"):
            health["preventive_measures"] = health.pop("remedies", [])

        sun_sign = report_data.get("sun_sign", {})
        if not sun_sign.get("sign") and report_data.get("planetary_positions"):
            for p in report_data.get("planetary_positions", []):
                if isinstance(p, dict) and p.get("planet") == "Sun":
                    sun_sign["sign"] = p.get("sign", "")
                    break

        current_dasha_raw = report_data.get("current_dasha", dasha)
        if isinstance(current_dasha_raw, str):
            planet_name = current_dasha_raw.replace(" Mahadasha", "").replace(" Dasha", "").strip()
            current_dasha = {"mahadasha": planet_name, "effects": []}
        elif isinstance(current_dasha_raw, dict):
            cd = dict(current_dasha_raw)
            if not cd.get("mahadasha") and cd.get("current_dasha"):
                cd["mahadasha"] = cd.pop("current_dasha")
            if not cd.get("mahadasha") and cd.get("planet"):
                cd["mahadasha"] = cd.pop("planet")
            if not cd.get("effects") and cd.get("current_effects"):
                cd["effects"] = cd.pop("current_effects")
            if cd.get("mahadasha"):
                cd["mahadasha"] = cd["mahadasha"].replace(" Mahadasha","").replace(" Dasha","").strip()
            current_dasha = cd
        else:
            current_dasha = {}

        dasha_timeline_raw = report_data.get("dasha_timeline",
                             dasha.get("upcoming", []) if isinstance(dasha, dict) else [])
        dasha_timeline = []
        for d in dasha_timeline_raw:
            if isinstance(d, dict):
                entry = dict(d)
                if not entry.get("planet") and entry.get("dasha"):
                    entry["planet"] = entry.pop("dasha")
                if not entry.get("period") and entry.get("start_year") and entry.get("end_year"):
                    entry["period"] = f"{entry['start_year']} – {entry['end_year']}"
                dasha_timeline.append(entry)

        if chart_data and chart_data.get("dashas"):
            calc_dashas = chart_data["dashas"]
            current_planet = current_dasha.get("mahadasha", "")
            curr_idx = next((i for i, d in enumerate(calc_dashas) if d.get("planet","") == current_planet), -1)
            if curr_idx >= 0 and len(dasha_timeline) == 0:
                for d in calc_dashas[curr_idx+1:curr_idx+4]:
                    start = d.get("start","").split("-")[0] if d.get("start") else ""
                    end = d.get("end","").split("-")[0] if d.get("end") else ""
                    dasha_timeline.append({
                        "planet": d.get("planet",""),
                        "period": f"{start} – {end}" if start and end else "",
                        "effects": [f"{d.get('planet','')} Mahadasha period"]
                    })
            elif curr_idx >= 0:
                calc_map = {d.get("planet",""): d for d in calc_dashas}
                for entry in dasha_timeline:
                    if not entry.get("period") and entry.get("planet"):
                        cd = calc_map.get(entry["planet"], {})
                        start = cd.get("start","").split("-")[0] if cd.get("start") else ""
                        end = cd.get("end","").split("-")[0] if cd.get("end") else ""
                        if start and end:
                            entry["period"] = f"{start} – {end}"

        mangal_from_claude = report_data.get("mangal_dosha", {})
        if chart_data and chart_data.get("mangal_dosha"):
            calc_mangal = chart_data["mangal_dosha"]
            mangal = {
                "has_dosha": calc_mangal.get("has_dosha", calc_mangal.get("present", False)),
                "present": calc_mangal.get("has_dosha", calc_mangal.get("present", False)),
                "mars_house": calc_mangal.get("mars_house", ""),
                "severity": calc_mangal.get("severity", ""),
                "description": calc_mangal.get("description", calc_mangal.get("note", "")),
                "remedies": mangal_from_claude.get("remedies", []) if isinstance(mangal_from_claude, dict) else [],
                "effects": mangal_from_claude.get("effects", "") if isinstance(mangal_from_claude, dict) else "",
            }
        else:
            mangal = mangal_from_claude
            if isinstance(mangal, dict) and not mangal.get("has_dosha") and mangal.get("present"):
                mangal["has_dosha"] = mangal["present"]

        report = BrihatKundliReport(
            user_email=user_email,
            full_name=request.full_name,
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            place_of_birth=request.place_of_birth,
            gender=request.gender,
            ascendant=report_data.get("ascendant", {}),
            moon_sign=report_data.get("moon_sign", {}),
            sun_sign=sun_sign,
            planetary_positions=report_data.get("planetary_positions", []),
            career_prediction=career,
            love_prediction=(lambda lp: {
            **lp,
            "ideal_partner_traits": lp.get("ideal_partner_traits") or lp.get("ideal_partner") or [],
            "compatibility_signs": lp.get("compatibility_signs") or lp.get("compatible_signs") or [],
            "challenging_signs": lp.get("challenging_signs") or [],
        })(report_data.get("love_prediction", {})),
            health_prediction=health,
            wealth_prediction=(lambda wp: {
            **wp,
            "primary_income_sources": wp.get("primary_income_sources") or wp.get("income_sources") or wp.get("wealth_sources") or [],
            "good_investments": wp.get("good_investments") or wp.get("investments") or wp.get("peak_periods") or
                ["Real estate and property", "Gold and precious metals", "Equity in partnership businesses", "Luxury and aesthetic sector funds"],
            "avoid": wp.get("avoid") or wp.get("cautions") or wp.get("things_to_avoid") or
                ["High-risk speculative investments", "Impulsive financial decisions", "Partnerships without legal agreements"],
        })(report_data.get("wealth_prediction", {})),
            family_prediction=report_data.get("family_prediction", {}),
            education_prediction=report_data.get("education_prediction", {}),
            current_dasha=current_dasha,
            dasha_timeline=dasha_timeline,
            mangal_dosha=mangal,
            kalsarp_dosha=report_data.get("kalsarp_dosha", {}),
            other_doshas=report_data.get("other_doshas", []),
            benefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "benefic"]
                          or report_data.get("benefic_yogas", []),
            malefic_yogas=[y for y in yogas if isinstance(y, dict) and y.get("type") == "malefic"]
                          or report_data.get("malefic_yogas", []),
            gemstone_remedies=remedies.get("gemstones", report_data.get("gemstone_remedies", [])),
            mantra_remedies=remedies.get("mantras", report_data.get("mantra_remedies", [])),
            lifestyle_remedies=remedies.get("general", report_data.get("lifestyle_remedies", [])),
            donation_remedies=report_data.get("donation_remedies", []),
            lucky_numbers=report_data.get("lucky_numbers", []),
            lucky_colors=report_data.get("lucky_colors", []),
            lucky_days=report_data.get("lucky_days", []),
            lucky_direction=report_data.get("lucky_direction", ""),
            numerology=report_data.get("numerology", {}),
            chart_svg=chart_svg
        )
        
        import json
        doc = json.loads(report.model_dump_json())
        doc_for_db = {**doc}
        await db.brihat_kundli_reports.insert_one(doc_for_db)
        return {"success": True, "report_id": report.id, "report": doc}

    except Exception as e:
        logging.error(f"Brihat Kundli generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@api_router.get("/brihat-kundli/{report_id}")
async def get_brihat_kundli(report_id: str):
    """Get existing Brihat Kundli report"""
    report = await db.brihat_kundli_reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@api_router.get("/brihat-kundli/{report_id}/pdf")
async def download_brihat_kundli_pdf(report_id: str, user_email: str = None):
    """Generate and download Brihat Kundli Pro PDF"""
    report = await db.brihat_kundli_reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    try:
        chart_data = None
        try:
            chart_data = calculate_vedic_chart(
                date_of_birth=report['date_of_birth'],
                time_of_birth=report['time_of_birth'],
                place_of_birth=report.get('place_of_birth', 'New Delhi'),
            )
        except Exception as ce:
            logging.warning(f"Chart calc for Brihat PDF failed: {ce}")
        password = generate_report_password(report.get('full_name', ''), report.get('date_of_birth', ''))
        pdf_buffer = generate_brihat_kundli_pdf(report, chart_data=chart_data, password=password)
        safe_name = report.get('full_name', 'report').replace(' ', '_')
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=brihat_kundli_{safe_name}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password",
                "X-PDF-Password": password,
            }
        )
    except Exception as e:
        logging.error(f"Brihat PDF generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

# ============== END BRIHAT KUNDLI PRO ==============

# Kundali Milan
async def generate_kundali_milan_with_llm(person1: BirthProfile, person2: BirthProfile) -> tuple:
    """
    Generate Kundali Milan report.
    Layer 1: vedic_calculator.py — deterministic Ashtakoot score + chart data
    Layer 2: Claude — interprets the compatibility with real positions
    Score is ALWAYS from Layer 1, never from Claude.
    """
    chart1, chart2, ashtakoot_data = None, None, None
    compatibility_score = 0
    mangal1, mangal2 = {}, {}

    try:
        chart1 = calculate_vedic_chart(
            date_of_birth=person1.date_of_birth,
            time_of_birth=person1.time_of_birth,
            place_of_birth=person1.location,
        )
        chart2 = calculate_vedic_chart(
            date_of_birth=person2.date_of_birth,
            time_of_birth=person2.time_of_birth,
            place_of_birth=person2.location,
        )
        nak1 = chart1['nakshatra']['name']
        sign1 = chart1['moon_sign']['sign']
        nak2 = chart2['nakshatra']['name']
        sign2 = chart2['moon_sign']['sign']
        ashtakoot_data = calculate_ashtakoot(nak1, sign1, nak2, sign2)
        compatibility_score = ashtakoot_data.get('total_score', 0)
        mangal1 = chart1['mangal_dosha']
        mangal2 = chart2['mangal_dosha']
        logging.info(f"Kundali Milan calculated: {nak1}/{sign1} vs {nak2}/{sign2} = {compatibility_score}/36")
    except Exception as e:
        logging.error(f"Vedic calculator FAILED for Kundali Milan: {e}", exc_info=True)

    def fmt_chart(name, chart, mangal):
        if not chart:
            return f"{name}: chart calculation unavailable"
        lagna = chart['lagna']
        moon = chart['moon_sign']
        nak = chart['nakshatra']
        return (
            f"{name}:\n"
            f"  Ascendant: {lagna['sign_vedic']} ({lagna['degree']}°), Lord: {lagna['lord']}\n"
            f"  Moon Sign: {moon['sign_vedic']}\n"
            f"  Nakshatra: {nak['name']} Pada {nak.get('pada','?')} | Lord: {nak.get('lord','?')}\n"
            f"  Mangal Dosha: {'YES — ' + mangal.get('description','') if mangal.get('has_dosha') else 'No'}\n"
            f"  Dasha: {chart.get('current_dasha',{}).get('planet','Unknown')} Mahadasha"
        )

    def fmt_ashtakoot(data):
        if not data or 'kootas' not in data:
            return "Score unavailable"
        lines = [f"  TOTAL: {data['total_score']}/36"]
        for k, v in data['kootas'].items():
            lines.append(f"  {k.upper()}: {v['score']}/{v['max']} — {v.get('label','')}")
        return '\n'.join(lines)

    chart_text = f"""
CALCULATED CHART DATA (mathematically verified):

{fmt_chart(person1.name, chart1, mangal1)}

{fmt_chart(person2.name, chart2, mangal2)}

ASHTAKOOT GUNA MILAN (do NOT change these scores):
{fmt_ashtakoot(ashtakoot_data)}
"""

    system_prompt = """You are an expert Jyotish astrologer specialising in Vivah Milan. You receive mathematically calculated chart data. Interpret ONLY — never recalculate or change any scores.

CRITICAL: The Ashtakoot score is final and mathematically correct — never change it.
NO markdown symbols (no **, no ##, no ---).
Sections: Compatibility Overview, Ashtakoot Analysis (explain each Koota), Mangal Dosha Assessment, Planetary Harmony, Relationship Strengths, Challenges, Marriage Timing, Remedies.
Address both people by name. Target 900-1000 words."""

    user_prompt = f"""Write a Kundali Milan report for {person1.name} and {person2.name}.

{chart_text}

The compatibility score is {compatibility_score}/36 — mathematically calculated and final. Explain what each Koota score means for this couple specifically."""

    try:
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return compatibility_score, message.content[0].text, ashtakoot_data
    except Exception as e:
        logging.error(f"Error generating Kundali Milan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate Kundali Milan: {str(e)}")

@api_router.post("/kundali-milan/generate", response_model=KundaliMilanReport)
async def generate_kundali_milan(request: KundaliMilanRequest):
    """Generate comprehensive Kundali Milan compatibility report"""
    
    profile1 = await db.birth_profiles.find_one({"id": request.person1_id}, {"_id": 0})
    profile2 = await db.birth_profiles.find_one({"id": request.person2_id}, {"_id": 0})
    
    if not profile1 or not profile2:
        raise HTTPException(status_code=404, detail="One or both birth profiles not found")
    
    if isinstance(profile1['created_at'], str):
        profile1['created_at'] = datetime.fromisoformat(profile1['created_at'])
    if isinstance(profile2['created_at'], str):
        profile2['created_at'] = datetime.fromisoformat(profile2['created_at'])
    
    birth_profile1 = BirthProfile(**profile1)
    birth_profile2 = BirthProfile(**profile2)
    
    existing = await db.kundali_milan_reports.find_one(
        {
            "$or": [
                {"person1_id": request.person1_id, "person2_id": request.person2_id},
                {"person1_id": request.person2_id, "person2_id": request.person1_id}
            ]
        },
        {"_id": 0}
    )
    
    if existing:
        if isinstance(existing['generated_at'], str):
            existing['generated_at'] = datetime.fromisoformat(existing['generated_at'])
        return KundaliMilanReport(**existing)
    
    score, analysis, ashtakoot_data = await generate_kundali_milan_with_llm(birth_profile1, birth_profile2)

    km_chart1, km_chart2 = None, None
    try:
        km_chart1 = calculate_vedic_chart(
            date_of_birth=birth_profile1.date_of_birth,
            time_of_birth=birth_profile1.time_of_birth,
            place_of_birth=birth_profile1.location,
        )
    except Exception as ce:
        logging.warning(f"Chart1 calc for KundaliMilan: {ce}")
    try:
        km_chart2 = calculate_vedic_chart(
            date_of_birth=birth_profile2.date_of_birth,
            time_of_birth=birth_profile2.time_of_birth,
            place_of_birth=birth_profile2.location,
        )
    except Exception as ce:
        logging.warning(f"Chart2 calc for KundaliMilan: {ce}")

    km_svg1, km_svg2 = "", ""
    try:
        from vedic_calculator import generate_north_indian_chart_svg
        if km_chart1 and km_chart1.get('houses'):
            km_svg1 = generate_north_indian_chart_svg(km_chart1['houses'], km_chart1['lagna']['sign'])
        if km_chart2 and km_chart2.get('houses'):
            km_svg2 = generate_north_indian_chart_svg(km_chart2['houses'], km_chart2['lagna']['sign'])
    except Exception as se:
        logging.warning(f"SVG generation for KundaliMilan: {se}")

    km_ashtakoot_details = {}
    if ashtakoot_data and isinstance(ashtakoot_data, dict):
        kootas = ashtakoot_data.get('kootas', {})
        km_ashtakoot_details = {
            'varna':        kootas.get('varna', {}).get('score', 0),
            'vashya':       kootas.get('vashya', {}).get('score', 0),
            'tara':         kootas.get('tara', {}).get('score', 0),
            'yoni':         kootas.get('yoni', {}).get('score', 0),
            'graha_maitri': kootas.get('graha_maitri', {}).get('score', 0),
            'gana':         kootas.get('gana', {}).get('score', 0),
            'bhakoot':      kootas.get('bhakoot', {}).get('score', 0),
            'nadi':         kootas.get('nadi', {}).get('score', 0),
        }

    report = KundaliMilanReport(
        person1_id=request.person1_id,
        person2_id=request.person2_id,
        compatibility_score=score,
        detailed_analysis=analysis,
        chart_svg_person1=km_svg1,
        chart_svg_person2=km_svg2,
        ashtakoot_details=km_ashtakoot_details,
    )
    
    import json as _json
    doc = _json.loads(report.model_dump_json())
    doc_for_db = {**doc}
    await db.kundali_milan_reports.insert_one(doc_for_db)
    return report

@api_router.get("/kundali-milan/{report_id}/pdf")
async def download_kundali_milan_pdf(report_id: str, user_email: str = None):
    """Generate and download Kundali Milan PDF"""
    report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
    person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
    if not person1 or not person2:
        raise HTTPException(status_code=404, detail="Profiles not found")
    try:
        password = generate_report_password(person1.get('name', ''), person1.get('date_of_birth', ''))
        pdf_buffer = generate_kundali_milan_pdf(
            person1, person2,
            report['compatibility_score'],
            report['detailed_analysis'],
            password=password
        )
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Kundali_Milan_Report_{person1['name'].replace(' ', '_')}_{person2['name'].replace(' ', '_')}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password",
                "X-PDF-Password": password,
            }
        )
    except Exception as e:
        logging.error(f"PDF generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

@api_router.get("/kundali-milan/{person1_id}/{person2_id}", response_model=KundaliMilanReport)
async def get_kundali_milan(person1_id: str, person2_id: str):
    """Get existing Kundali Milan report"""
    report = await db.kundali_milan_reports.find_one(
        {
            "$or": [
                {"person1_id": person1_id, "person2_id": person2_id},
                {"person1_id": person2_id, "person2_id": person1_id}
            ]
        },
        {"_id": 0}
    )
    if not report:
        raise HTTPException(status_code=404, detail="Kundali Milan report not found")
    if isinstance(report['generated_at'], str):
        report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    return KundaliMilanReport(**report)

# Premium Access Check Helper
async def check_premium_access(user_email: str, report_type: str, report_id: str) -> bool:
    """Check if user has premium access via subscription or one-time payment"""
    subscription = await db.subscriptions.find_one({
        "user_email": user_email,
        "status": "active",
        "subscription_type": "premium_monthly"
    })
    if subscription:
        expires_at = subscription.get('expires_at')
        if expires_at is None:
            return True
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at > datetime.now(timezone.utc):
            return True
    payment = await db.payments.find_one({
        "user_email": user_email,
        "report_type": report_type,
        "report_id": report_id,
        "status": "completed"
    })
    if payment:
        return True
    premium_payment = await db.payments.find_one({
        "user_email": user_email,
        "report_type": "premium_monthly",
        "status": "completed"
    })
    return premium_payment is not None

# Payment Endpoints (Razorpay)
@api_router.post("/payment/create-order")
async def create_payment_order(request: PaymentIntentRequest):
    """Create Razorpay order for premium features"""
    if request.report_type not in PRICING:
        raise HTTPException(status_code=400, detail="Invalid report type")
    try:
        amount_paise = int(PRICING[request.report_type] * 100)
        razorpay_order = razorpay_client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "report_type": request.report_type,
                "report_id": request.report_id or "",
                "user_email": request.user_email
            }
        })
        payment = Payment(
            user_email=request.user_email,
            report_type=request.report_type,
            report_id=request.report_id or "",
            amount=PRICING[request.report_type],
            razorpay_order_id=razorpay_order["id"],
            status="created"
        )
        doc = payment.model_dump(mode='json')
        await db.payments.insert_one(doc)
        return {
            "order_id": razorpay_order["id"],
            "amount": PRICING[request.report_type],
            "currency": "INR",
            "key_id": os.environ.get('RAZORPAY_KEY_ID')
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Razorpay order creation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment order creation failed")

@api_router.post("/payment/verify")
async def verify_payment(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    user_email: str
):
    """Verify Razorpay payment and grant access"""
    try:
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        razorpay_client.utility.verify_payment_signature(params_dict)
        payment_doc = await db.payments.find_one(
            {"razorpay_order_id": razorpay_order_id},
            {"_id": 0}
        )
        if not payment_doc:
            raise HTTPException(status_code=404, detail="Payment record not found")
        await db.payments.update_one(
            {"razorpay_order_id": razorpay_order_id},
            {"$set": {"razorpay_payment_id": razorpay_payment_id, "status": "completed"}}
        )
        if payment_doc['report_type'] == "premium_monthly":
            subscription = UserSubscription(
                user_email=user_email,
                subscription_type="premium_monthly",
                status="active",
                stripe_subscription_id=razorpay_payment_id,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30)
            )
            sub_doc = subscription.model_dump(mode='json')
            await db.subscriptions.insert_one(sub_doc)
        return {"status": "success", "message": "Payment verified successfully", "payment_id": razorpay_payment_id}
    except razorpay.errors.SignatureVerificationError:
        logging.error("Payment signature verification failed")
        await db.payments.update_one(
            {"razorpay_order_id": razorpay_order_id},
            {"$set": {"status": "failed"}}
        )
        raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        logging.error(f"Payment verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment verification failed")

@api_router.get("/premium/check")
async def check_premium(user_email: str, report_type: str, report_id: str):
    """Check if user has premium access"""
    has_access = await check_premium_access(user_email, report_type, report_id)
    return {"has_premium_access": has_access}

# PDF Generation Endpoints
@api_router.get("/birthchart/{profile_id}/pdf")
async def download_birth_chart_pdf(profile_id: str, user_email: str = None):
    """Generate and download Birth Chart PDF"""
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    report = await db.birth_chart_reports.find_one({"profile_id": profile_id}, {"_id": 0})
    if not profile or not report:
        raise HTTPException(status_code=404, detail="Report not found")
    try:
        chart_data = None
        try:
            chart_data = calculate_vedic_chart(
                date_of_birth=profile['date_of_birth'],
                time_of_birth=profile['time_of_birth'],
                place_of_birth=profile.get('location', profile.get('place_of_birth', 'New Delhi')),
            )
        except Exception as ce:
            logging.warning(f"Chart calc for PDF failed: {ce}")
        password = generate_report_password(profile.get('name', ''), profile.get('date_of_birth', ''))
        pdf_buffer = generate_birth_chart_pdf(
            profile, report['report_content'],
            chart_data=chart_data, password=password
        )
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Birth_Chart_Report_{profile['name'].replace(' ', '_')}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition, X-PDF-Password",
                "X-PDF-Password": password,
            }
        )
    except Exception as e:
        logging.error(f"PDF generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

# ── My Reports ──────────────────────────────────────────────────────────────

@api_router.get("/my-reports")
async def get_my_reports(user_email: str, request: Request):
    """Return all reports for the logged-in user across all 3 report types."""
    await get_current_user(request, db)
    try:
        reports = []
        profiles = await db.birth_profiles.find({"user_email": user_email}, {"_id": 0}).to_list(50)
        profile_ids = [p["id"] for p in profiles]
        profile_map = {p["id"]: p for p in profiles}

        if profile_ids:
            bc_reports = await db.birth_chart_reports.find(
                {"profile_id": {"$in": profile_ids}}, {"_id": 0}
            ).sort("generated_at", -1).to_list(50)
            for r in bc_reports:
                profile = profile_map.get(r.get("profile_id"), {})
                reports.append({
                    "id": r["id"], "type": "birth_chart", "type_label": "Birth Chart",
                    "name": profile.get("name", "Unknown"),
                    "subtitle": f"{profile.get('date_of_birth','')} · {profile.get('location','')}",
                    "profile_id": r.get("profile_id"),
                    "generated_at": r.get("generated_at"),
                    "lagna": r.get("lagna", {}), "nakshatra": r.get("nakshatra", {}),
                })

        if profile_ids:
            km_reports = await db.kundali_milan_reports.find(
                {"$or": [
                    {"person1_id": {"$in": profile_ids}},
                    {"person2_id": {"$in": profile_ids}},
                ]}, {"_id": 0}
            ).sort("generated_at", -1).to_list(50)
            for r in km_reports:
                p1 = profile_map.get(r.get("person1_id"), {})
                p2 = await db.birth_profiles.find_one({"id": r.get("person2_id")}, {"_id": 0}) or {}
                reports.append({
                    "id": r["id"], "type": "kundali_milan", "type_label": "Kundali Milan",
                    "name": f"{p1.get('name','?')} & {p2.get('name','?')}",
                    "subtitle": f"Compatibility Score: {r.get('compatibility_score', 0)}/36",
                    "person1_id": r.get("person1_id"), "person2_id": r.get("person2_id"),
                    "compatibility_score": r.get("compatibility_score", 0),
                    "generated_at": r.get("generated_at"),
                })

        bk_reports = await db.brihat_kundli_reports.find(
            {"user_email": user_email}, {"_id": 0}
        ).sort("generated_at", -1).to_list(20)
        for r in bk_reports:
            reports.append({
                "id": r["id"], "type": "brihat_kundli", "type_label": "Brihat Kundli Pro",
                "name": r.get("full_name", "Unknown"),
                "subtitle": f"{r.get('date_of_birth','')} · {r.get('place_of_birth','')}",
                "generated_at": r.get("generated_at"),
                "ascendant": r.get("ascendant", {}), "current_dasha": r.get("current_dasha", {}),
            })

        reports.sort(key=lambda x: str(x.get("generated_at", "")), reverse=True)
        return {"reports": reports, "total": len(reports)}
    except Exception as e:
        logging.error(f"Error fetching my-reports: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch reports")

# Share Link Endpoints
@api_router.post("/share/create")
async def create_share_link(report_type: str, report_id: str):
    """Create shareable link for report"""
    existing = await db.share_links.find_one({"report_type": report_type, "report_id": report_id}, {"_id": 0})
    if existing:
        if isinstance(existing['created_at'], str):
            existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return ShareLink(**existing)
    share_link = ShareLink(report_type=report_type, report_id=report_id)
    doc = share_link.model_dump(mode='json')
    await db.share_links.insert_one(doc)
    return share_link

@api_router.get("/share/{token}")
async def get_shared_report(token: str):
    """Get report via share link (public access)"""
    share_link = await db.share_links.find_one({"token": token}, {"_id": 0})
    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")
    await db.share_links.update_one({"token": token}, {"$inc": {"views": 1}})
    report_type = share_link['report_type']
    report_id = share_link['report_id']
    if report_type == "birth_chart":
        profile = await db.birth_profiles.find_one({"id": report_id}, {"_id": 0})
        report = await db.birth_chart_reports.find_one({"profile_id": report_id}, {"_id": 0})
        if not profile or not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return {"type": "birth_chart", "profile": profile, "report": report}
    elif report_type == "kundali_milan":
        report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
        person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
        return {"type": "kundali_milan", "report": report, "person1": person1, "person2": person2}
    raise HTTPException(status_code=400, detail="Invalid report type")

# Authentication Endpoints
@api_router.post("/auth/register")
async def register(request: RegisterRequest, response: Response):
    """Register new user with email/password"""
    existing = await db.users.find_one({"email": request.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password)
    )
    doc = user.model_dump(mode='json')
    await db.users.insert_one(doc)
    welcome_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #B8960C;">Welcome to Everyday Horoscope! ✨</h2>
        <p>Hi {user.name},</p>
        <p>Your account has been created successfully. Here's what you can explore:</p>
        <ul>
            <li>🌟 Daily, Weekly & Monthly Horoscopes for all 12 signs</li>
            <li>📊 Birth Chart Analysis</li>
            <li>💑 Kundali Milan Compatibility</li>
            <li>📖 Astrology Blog</li>
        </ul>
        <p>Visit us at: <a href="{os.environ.get('FRONTEND_URL', 'https://everydayhoroscope.in')}">everydayhoroscope.in</a></p>
        <p>For support, contact us at: prateekmalhotra.contentcreator@gmail.com</p>
        <hr/>
        <p style="color: #888; font-size: 12px;">SkyHound Studios · Delhi, India</p>
    </div>
    """
    await send_email_notification(user.email, "Welcome to Everyday Horoscope ✨", welcome_body)
    admin_email = os.environ.get('ADMIN_EMAIL', os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com'))
    admin_body = f"""
    <div style="font-family: Arial, sans-serif;">
        <h3>New User Registration</h3>
        <p><b>Name:</b> {user.name}</p>
        <p><b>Email:</b> {user.email}</p>
        <p><b>Time:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
    </div>
    """
    await send_email_notification(admin_email, f"New Registration: {user.name}", admin_body)
    session_token = await create_session(db, user.user_id)
    set_session_cookie(response, session_token)
    return UserResponse(user_id=user.user_id, email=user.email, name=user.name, picture=user.picture)

@api_router.post("/auth/login")
async def login(request: LoginRequest, response: Response):
    """Login with email/password — with brute force protection"""
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user_doc.get('password_hash'):
        raise HTTPException(status_code=401, detail="Please login with Google")
    locked_until = user_doc.get('locked_until')
    if locked_until:
        if isinstance(locked_until, str):
            locked_until = datetime.fromisoformat(locked_until)
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < locked_until:
            remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds() / 60)
            raise HTTPException(status_code=429, detail=f"Account locked due to too many failed attempts. Try again in {remaining} minutes.")
        else:
            await db.users.update_one({"email": request.email}, {"$unset": {"locked_until": "", "failed_attempts": ""}})
    if not verify_password(request.password, user_doc['password_hash']):
        failed = user_doc.get('failed_attempts', 0) + 1
        update = {"$set": {"failed_attempts": failed}}
        if failed >= 5:
            lock_until = datetime.now(timezone.utc) + timedelta(hours=24)
            update = {"$set": {"failed_attempts": failed, "locked_until": lock_until.isoformat()}}
            await db.users.update_one({"email": request.email}, update)
            raise HTTPException(status_code=429, detail="Account locked for 24 hours due to too many failed login attempts. Please check your email.")
        await db.users.update_one({"email": request.email}, update)
        remaining_attempts = 5 - failed
        raise HTTPException(status_code=401, detail=f"Invalid email or password. {remaining_attempts} attempt{'s' if remaining_attempts != 1 else ''} remaining before account lockout.")
    await db.users.update_one({"email": request.email}, {"$unset": {"failed_attempts": "", "locked_until": ""}})
    session_token = await create_session(db, user_doc['user_id'])
    set_session_cookie(response, session_token)
    return UserResponse(user_id=user_doc['user_id'], email=user_doc['email'], name=user_doc['name'], picture=user_doc.get('picture'))

@api_router.post("/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Send password reset email"""
    import secrets as secrets_module
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    if not user_doc:
        return {"message": "If that email exists, a reset link has been sent."}
    if not user_doc.get('password_hash'):
        return {"message": "If that email exists, a reset link has been sent."}
    reset_token = secrets_module.token_urlsafe(32)
    reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    await db.users.update_one(
        {"email": request.email},
        {"$set": {"reset_token": reset_token, "reset_token_expires": reset_expires.isoformat()}}
    )
    frontend_url = os.environ.get('FRONTEND_URL', 'https://everydayhoroscope.in')
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"
    user_name = user_doc.get('name', 'there')
    email_body = f"""
    <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 32px; background: #fff;">
      <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="color: #C5A059; font-size: 28px; margin: 0;">✦ Everyday Horoscope</h1>
      </div>
      <h2 style="color: #1a1a1a; font-size: 22px;">Reset your password</h2>
      <p style="color: #444; font-size: 15px; line-height: 1.6;">Hi {user_name},</p>
      <p style="color: #444; font-size: 15px; line-height: 1.6;">
        We received a request to reset your password. Click the button below to choose a new one.
        This link expires in <strong>1 hour</strong>.
      </p>
      <div style="text-align: center; margin: 32px 0;">
        <a href="{reset_link}" style="background: #C5A059; color: #fff; padding: 14px 32px; border-radius: 4px; text-decoration: none; font-size: 15px; font-weight: bold; display: inline-block;">
          Reset My Password
        </a>
      </div>
      <p style="color: #888; font-size: 13px; line-height: 1.6;">
        If you didn't request this, you can safely ignore this email. Your password will remain unchanged.
      </p>
      <p style="color: #888; font-size: 12px;">Or copy this link into your browser:<br/>
        <a href="{reset_link}" style="color: #C5A059;">{reset_link}</a>
      </p>
      <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;" />
      <p style="color: #aaa; font-size: 12px; text-align: center;">SkyHound Studios · Delhi, India</p>
    </div>
    """
    await send_email_notification(request.email, "Reset your Everyday Horoscope password", email_body)
    logging.info(f"Password reset email sent to {request.email}")
    return {"message": "If that email exists, a reset link has been sent."}

@api_router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset password using token"""
    user_doc = await db.users.find_one({"reset_token": request.token}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    expires = user_doc.get('reset_token_expires')
    if expires:
        if isinstance(expires, str):
            expires = datetime.fromisoformat(expires)
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(status_code=400, detail="Reset token has expired. Please request a new one.")
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    new_hash = hash_password(request.new_password)
    await db.users.update_one(
        {"reset_token": request.token},
        {"$set": {"password_hash": new_hash},
         "$unset": {"reset_token": "", "reset_token_expires": "", "failed_attempts": "", "locked_until": ""}}
    )
    return {"message": "Password reset successfully. You can now login with your new password."}

@api_router.get("/auth/me")
async def get_me(request: Request):
    """Get current authenticated user"""
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user"""
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

class OAuthCallbackRequest(BaseModel):
    session_id: str

@api_router.post("/auth/oauth/callback")
async def oauth_callback(response: Response, body: OAuthCallbackRequest = None, session_id: str = None):
    """Handle Google OAuth callback — accepts code from body or query param"""
    code = (body.session_id if body else None) or session_id
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    # REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    try:
        user_data = await exchange_session_id_for_token(code)
        user = await get_or_create_oauth_user(
            db, email=user_data['email'], name=user_data['name'],
            picture=user_data.get('picture'), google_id=user_data['id']
        )
        session_token = await create_session(db, user.user_id)
        set_session_cookie(response, session_token)
        return UserResponse(user_id=user.user_id, email=user.email, name=user.name, picture=user.picture)
    except Exception as e:
        logging.error(f"OAuth callback error: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# ============== POLICY ENDPOINTS ==============

@api_router.get("/policies/{policy_type}")
async def get_policy(policy_type: str):
    """Get a policy document by type"""
    valid_types = ['terms', 'privacy', 'subscription-terms', 'refund-policy', 'cookie-policy']
    if policy_type not in valid_types:
        raise HTTPException(status_code=404, detail="Policy not found")
    policy = await db.policies.find_one({"type": policy_type}, {"_id": 0})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@api_router.put("/admin/policies/{policy_type}")
async def update_policy(request: Request, policy_type: str, policy_data: dict):
    """Update a policy document (admin only)"""
    await require_admin(request, db)
    valid_types = ['terms', 'privacy', 'subscription-terms', 'refund-policy', 'cookie-policy']
    if policy_type not in valid_types:
        raise HTTPException(status_code=404, detail="Policy type not found")
    policy_data['type'] = policy_type
    policy_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    await db.policies.update_one({"type": policy_type}, {"$set": policy_data}, upsert=True)
    return {"success": True, "message": f"Policy '{policy_type}' updated successfully"}

@api_router.get("/admin/policies")
async def get_all_policies(request: Request):
    """Get all policies for admin"""
    await require_admin(request, db)
    policies = await db.policies.find({}, {"_id": 0}).to_list(100)
    return {"policies": policies}

# ============== CONTACT FORM ==============

@api_router.post("/contact")
async def submit_contact_form(form: ContactFormRequest):
    """Handle contact form submission"""
    contact_doc = {
        "id": str(uuid.uuid4()),
        "name": form.name, "email": form.email,
        "subject": form.subject or "Contact Form Submission",
        "message": form.message,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.contact_messages.insert_one(contact_doc)
    admin_email = os.environ.get('ADMIN_EMAIL', os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com'))
    body = f"""
    <div style="font-family: Arial, sans-serif;">
        <h3>New Contact Form Message</h3>
        <p><b>From:</b> {form.name} ({form.email})</p>
        <p><b>Subject:</b> {form.subject or 'No subject'}</p>
        <p><b>Message:</b></p>
        <p style="background: #f5f5f5; padding: 12px; border-radius: 4px;">{form.message}</p>
    </div>
    """
    await send_email_notification(admin_email, f"Contact: {form.subject or form.name}", body)
    reply_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px;">
        <h2 style="color: #B8960C;">We received your message ✨</h2>
        <p>Hi {form.name},</p>
        <p>Thank you for reaching out to Everyday Horoscope. We've received your message and will respond within 2 business days.</p>
        <p><b>Your message:</b></p>
        <p style="background: #f9f9f9; padding: 12px; border-radius: 4px; color: #555;">{form.message}</p>
        <p>For urgent queries, email us directly at: prateekmalhotra.contentcreator@gmail.com</p>
        <hr/>
        <p style="color: #888; font-size: 12px;">SkyHound Studios · Delhi, India</p>
    </div>
    """
    await send_email_notification(form.email, "We received your message — Everyday Horoscope", reply_body)
    return {"success": True, "message": "Message received. We'll get back to you within 2 business days."}

# ============== ADMIN ENDPOINTS ==============

@api_router.post("/admin/login")
async def admin_login(request: AdminLoginRequest, response: Response):
    if request.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_admin_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_token = await create_admin_session(db)
    set_admin_session_cookie(response, session_token)
    return AdminLoginResponse(success=True, token=session_token, message="Login successful")

@api_router.post("/admin/logout")
async def admin_logout(request: Request, response: Response):
    session_token = request.cookies.get("admin_session")
    if session_token:
        await db.admin_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("admin_session", path="/")
    return {"message": "Logged out successfully"}

@api_router.post("/admin/change-password")
async def change_admin_password(request: Request, password_request: ChangePasswordRequest):
    await require_admin(request, db)
    if not verify_admin_password(password_request.current_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(password_request.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
    update_admin_password(password_request.new_password)
    new_hash = hash_new_password(password_request.new_password)
    await db.admin_settings.update_one(
        {"key": "admin_password_hash"},
        {"$set": {"value": new_hash}},
        upsert=True
    )
    return {"success": True, "message": "Password changed successfully"}

@api_router.get("/admin/verify")
async def verify_admin(request: Request):
    is_admin = await require_admin(request, db)
    return {"authenticated": is_admin}

@api_router.get("/admin/dashboard")
async def get_dashboard_stats(request: Request):
    await require_admin(request, db)
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_iso = today_start.isoformat()
    total_users = await db.users.count_documents({})
    total_payments = await db.payments.count_documents({})
    total_birth_charts = await db.birth_chart_reports.count_documents({})
    total_kundali_milans = await db.kundali_milan_reports.count_documents({})
    active_subscriptions = await db.subscriptions.count_documents({"status": "active"})
    revenue_pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    revenue_result = await db.payments.aggregate(revenue_pipeline).to_list(1)
    total_revenue = revenue_result[0]['total'] if revenue_result else 0
    users_today = await db.users.count_documents({"created_at": {"$gte": today_iso}})
    payments_today = await db.payments.count_documents({"created_at": {"$gte": today_iso}})
    return DashboardStats(
        total_users=total_users, total_payments=total_payments, total_revenue=total_revenue,
        total_birth_charts=total_birth_charts, total_kundali_milans=total_kundali_milans,
        active_subscriptions=active_subscriptions, users_today=users_today, payments_today=payments_today
    )

@api_router.get("/admin/users")
async def get_all_users(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.users.count_documents({})
    user_list = []
    for user in users:
        created_at = user.get('created_at', '')
        if hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        user_list.append(UserListItem(
            user_id=user.get('user_id', ''), email=user.get('email', ''), name=user.get('name', ''),
            picture=user.get('picture'), google_id=user.get('google_id'), created_at=str(created_at),
            has_password=bool(user.get('password_hash')), is_restricted=bool(user.get('is_restricted', False)),
            is_suspended=bool(user.get('is_suspended', False)),
            suspended_until=str(user['suspended_until']) if user.get('suspended_until') else None,
            locked_until=str(user['locked_until']) if user.get('locked_until') else None,
            failed_attempts=int(user.get('failed_attempts', 0))
        ))
    return {"users": user_list, "total": total, "skip": skip, "limit": limit}

@api_router.get("/admin/payments")
async def get_all_payments(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    payments = await db.payments.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.payments.count_documents({})
    payment_list = []
    for payment in payments:
        created_at = payment.get('created_at', '')
        if hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        payment_list.append(PaymentListItem(
            id=payment.get('id', ''), user_email=payment.get('user_email', ''),
            report_type=payment.get('report_type', ''), amount=payment.get('amount', 0),
            status=payment.get('status', ''), razorpay_order_id=payment.get('razorpay_order_id', ''),
            razorpay_payment_id=payment.get('razorpay_payment_id'), created_at=str(created_at)
        ))
    return {"payments": payment_list, "total": total, "skip": skip, "limit": limit}

@api_router.get("/admin/reports")
async def get_all_reports(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    birth_charts = await db.birth_chart_reports.find({}, {"_id": 0}).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    kundali_milans = await db.kundali_milan_reports.find({}, {"_id": 0}).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    total_birth_charts = await db.birth_chart_reports.count_documents({})
    total_kundali_milans = await db.kundali_milan_reports.count_documents({})
    return {"birth_charts": birth_charts, "kundali_milans": kundali_milans, "total_birth_charts": total_birth_charts, "total_kundali_milans": total_kundali_milans}

@api_router.delete("/admin/user/{user_id}")
async def delete_user(request: Request, user_id: str):
    await require_admin(request, db)
    result = await db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    await db.user_sessions.delete_many({"user_id": user_id})
    return {"message": "User deleted successfully"}

class UserActionRequest(BaseModel):
    action: str

@api_router.post("/admin/user/{user_id}/action")
async def user_action(request: Request, user_id: str, body: UserActionRequest):
    await require_admin(request, db)
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    action = body.action
    if action == "restrict":
        update = {"$set": {"is_restricted": True}}
        msg = "User restricted successfully"
    elif action == "unrestrict":
        update = {"$unset": {"is_restricted": ""}}
        msg = "User restriction removed"
    elif action == "suspend":
        suspend_until = datetime.now(timezone.utc) + timedelta(hours=24)
        update = {"$set": {"is_suspended": True, "suspended_until": suspend_until.isoformat()}}
        msg = "User suspended for 24 hours"
        await send_email_notification(
            user.get('email', ''),
            "Your Everyday Horoscope account has been suspended",
            f"""<div style="font-family: Arial, sans-serif;">
            <h3>Account Suspended</h3>
            <p>Hi {user.get('name', 'User')},</p>
            <p>Your account has been temporarily suspended for 24 hours due to a policy violation.</p>
            <p>If you believe this is an error, please contact us at prateekmalhotra.contentcreator@gmail.com</p>
            <hr/><p style="color:#888;font-size:12px;">SkyHound Studios</p>
            </div>"""
        )
    elif action == "unsuspend":
        update = {"$unset": {"is_suspended": "", "suspended_until": ""}}
        msg = "User unsuspended successfully"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    await db.users.update_one({"user_id": user_id}, update)
    return {"success": True, "message": msg}

@api_router.get("/admin/contacts")
async def get_contact_messages(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    messages = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.contact_messages.count_documents({})
    return {"messages": messages, "total": total}

# ============== BLOG ENDPOINTS ==============

def generate_slug(title: str) -> str:
    import re
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    slug = slug.replace(' ', '-')
    return slug if slug else 'post'

@api_router.post("/admin/blog")
async def create_blog_post(request: Request, post: BlogPostCreate):
    await require_admin(request, db)
    slug = post.slug if post.slug else generate_slug(post.title)
    existing = await db.blog_posts.find_one({"slug": slug})
    if existing:
        slug = f"{slug}-{str(uuid.uuid4())[:8]}"
    blog_post = BlogPost(
        title=post.title, slug=slug, excerpt=post.excerpt, content=post.content,
        author=post.author, category=post.category, tags=post.tags,
        featured_image=post.featured_image, video_url=post.video_url, published=post.published
    )
    doc = blog_post.model_dump(mode='json')
    await db.blog_posts.insert_one(doc)
    return {"success": True, "post": doc}

@api_router.get("/admin/blog")
async def get_all_blog_posts_admin(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request, db)
    posts = await db.blog_posts.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.blog_posts.count_documents({})
    return {"posts": posts, "total": total, "skip": skip, "limit": limit}

@api_router.put("/admin/blog/{post_id}")
async def update_blog_post(request: Request, post_id: str, post: BlogPostUpdate):
    await require_admin(request, db)
    update_data = {k: v for k, v in post.model_dump(mode='json').items() if v is not None}
    if 'title' in update_data and 'slug' not in update_data:
        update_data['slug'] = generate_slug(update_data['title'])
    result = await db.blog_posts.update_one({"id": post_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"success": True, "message": "Post updated"}

@api_router.delete("/admin/blog/{post_id}")
async def delete_blog_post(request: Request, post_id: str):
    await require_admin(request, db)
    result = await db.blog_posts.delete_one({"id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"success": True, "message": "Post deleted"}

@api_router.get("/blog")
async def get_published_blog_posts(skip: int = 0, limit: int = 10, category: str = None):
    query = {"published": True}
    if category:
        query["category"] = category
    posts = await db.blog_posts.find(query, {"_id": 0, "content": 0}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.blog_posts.count_documents(query)
    return {"posts": posts, "total": total, "skip": skip, "limit": limit}

@api_router.get("/blog/{slug}")
async def get_blog_post_by_slug(slug: str):
    post = await db.blog_posts.find_one({"slug": slug, "published": True}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    await db.blog_posts.update_one({"slug": slug}, {"$inc": {"views": 1}})
    return post

@api_router.get("/blog/categories/list")
async def get_blog_categories():
    categories = await db.blog_posts.distinct("category", {"published": True})
    return {"categories": categories}

# ============== USER ACCOUNT ENDPOINTS ==============

class UpdateProfileRequest(BaseModel):
    name: str

class ChangeUserPasswordRequest(BaseModel):
    current_password: str
    new_password: str

@api_router.put("/auth/profile")
async def update_profile(request: Request, body: UpdateProfileRequest):
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    name = body.name.strip()
    if not name or len(name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    await db.users.update_one({"user_id": user.user_id}, {"$set": {"name": name}})
    return {"message": "Profile updated successfully", "name": name}

@api_router.put("/auth/change-password")
async def change_user_password(request: Request, body: ChangeUserPasswordRequest):
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_doc = await db.users.find_one({"user_id": user.user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_doc.get("password_hash"):
        raise HTTPException(status_code=400, detail="Password change not available for Google sign-in accounts")
    if not verify_password(body.current_password, user_doc["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(body.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
    new_hash = hash_password(body.new_password)
    await db.users.update_one({"user_id": user.user_id}, {"$set": {"password_hash": new_hash}})
    return {"message": "Password changed successfully"}

@api_router.get("/auth/my-payments")
async def get_my_payments(request: Request):
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payments = await db.payments.find({"user_email": user.email}, {"_id": 0}).sort("created_at", -1).limit(50).to_list(50)
    result = []
    for p in payments:
        created_at = p.get("created_at", "")
        if hasattr(created_at, "isoformat"):
            created_at = created_at.isoformat()
        result.append({
            "id": p.get("id", ""), "report_type": p.get("report_type", ""),
            "amount": p.get("amount", 0), "status": p.get("status", ""),
            "created_at": str(created_at)
        })
    return {"payments": result}

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Background job: pre-generate all horoscopes daily at midnight IST (18:30 UTC)
async def prefetch_all_horoscopes():
    """Pre-generate all 36 horoscopes (12 signs x 3 types) and cache in MongoDB"""
    logging.info("Starting scheduled horoscope prefetch for all signs...")
    signs = [s["id"] for s in ZODIAC_SIGNS]
    types = ["daily", "weekly", "monthly"]
    generated = 0
    skipped = 0
    for horoscope_type in types:
        prediction_date = get_prediction_date(horoscope_type)
        for sign in signs:
            try:
                existing = await db.horoscopes.find_one({
                    "sign": sign, "type": horoscope_type, "prediction_date": prediction_date
                })
                if existing:
                    skipped += 1
                    continue
                content = await generate_horoscope_with_llm(sign, horoscope_type)
                horoscope = Horoscope(sign=sign, type=horoscope_type, content=content, prediction_date=prediction_date)
                doc = horoscope.model_dump(mode='json')
                await db.horoscopes.insert_one(doc)
                generated += 1
                logging.info(f"Generated {horoscope_type} horoscope for {sign}")
            except Exception as e:
                logging.error(f"Failed to generate {horoscope_type} for {sign}: {str(e)}")
    logging.info(f"Horoscope prefetch complete: {generated} generated, {skipped} already cached")

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(hour=18, minute=30, timezone="UTC"),
        id="daily_horoscope_prefetch", replace_existing=True
    )
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(day_of_week="sun", hour=18, minute=0, timezone="UTC"),
        id="weekly_horoscope_prefetch", replace_existing=True
    )
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(day=1, hour=17, minute=30, timezone="UTC"),
        id="monthly_horoscope_prefetch", replace_existing=True
    )
    scheduler.start()
    logging.info("Horoscope prefetch scheduler started")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown()
    client.close()
