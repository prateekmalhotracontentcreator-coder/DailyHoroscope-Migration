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
from pdf_generator import generate_birth_chart_pdf, generate_kundali_milan_pdf
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
    
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KundaliMilanReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    person1_id: str
    person2_id: str
    compatibility_score: int
    detailed_analysis: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
async def create_birth_profile(profile: BirthProfileCreate):
    """Create a new birth profile"""
    birth_profile = BirthProfile(**profile.model_dump(mode='json'))
    
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
    except Exception as e:
        logging.warning(f"Vedic calculator failed, proceeding without chart data: {e}")
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
    system_prompt = """You are an expert Jyotish (Vedic astrology) interpreter. You will receive a mathematically calculated birth chart. Your job is ONLY interpretation — do NOT recalculate or change any positions.

CRITICAL RULES:
- Use ONLY the planetary positions provided — never invent or change them
- Address the native by name throughout the report
- NO markdown symbols (no **, no ##, no ---)
- Write in clean prose with clear section headings followed by a colon
- Structure: Overview, Ascendant & Personality, Sun & Moon Signs, Planetary Positions, House Analysis, Notable Yogas, Career & Dharma, Relationships & Marriage, Health & Wellness, Dasha Period Analysis, Remedies & Guidance
- Each section: 3-5 sentences of specific, personalised insight
- Target 700-800 words total
- Ground every statement in the actual chart data provided"""

    user_prompt = f"""Write a comprehensive Janma Kundali (Birth Chart) report for {profile.name} using this calculated chart data:

{chart_summary}

Interpret each section using the exact positions above. Make every insight specific to the actual house placements and planetary positions shown."""

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
    
    report = BirthChartReport(
        profile_id=request.profile_id,
        report_content=content
    )
    
    doc = report.model_dump(mode='json')
    await db.birth_chart_reports.insert_one(doc)
    
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

    # ── Layer 1: Calculate full chart ─────────────────────────────────────────
    chart_data = None
    try:
        chart_data = calculate_vedic_chart(
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            place_of_birth=request.place_of_birth,
        )
    except Exception as e:
        logging.warning(f"Vedic calculator failed for Brihat Kundli: {e}")

    # ── Build detailed chart summary ──────────────────────────────────────────
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

    # ── Layer 2: Claude writes comprehensive interpretation ────────────────────
    system_prompt = """You are a senior Jyotish astrologer writing a premium Brihat Kundli Pro report. You receive a mathematically calculated chart. Your job is deep interpretation — never recalculate or change any positions.

CRITICAL RULES:
- Use ONLY the planetary positions and house placements provided — never change them
- Return a VALID JSON object — no text before or after the JSON
- Use specific calendar years in all predictions (current year is """ + str(current_year) + """)
- Be specific and personalised — address the native by name
- NO markdown in JSON string values

Return this EXACT JSON structure:
{
    "ascendant": {"sign": "...", "degree": "...", "lord": "...", "element": "...", "key_traits": ["..."], "strengths": ["..."], "challenges": ["..."]},
    "moon_sign": {"sign": "...", "nakshatra": "...", "nakshatra_pada": "...", "nakshatra_lord": "...", "emotional_nature": ["..."], "mental_tendencies": ["..."]},
    "planetary_positions": [{"planet": "...", "sign": "...", "house": 1, "degree": "...", "status": "...", "strength": "...", "effects": ["..."]}],
    "house_analysis": [{"house": 1, "name": "...", "sign": "...", "lord": "...", "planets": ["..."], "interpretation": "..."}],
    "yogas": [{"name": "...", "type": "benefic/malefic", "planets_involved": ["..."], "effect": "..."}],
    "career_prediction": {"overall_rating": "...", "best_fields": ["..."], "peak_years": ["..."], "timeline": [{"period": "...", "prediction": "...", "advice": "..."}], "job_vs_business": "..."},
    "love_prediction": {"overall_rating": "...", "love_nature": ["..."], "ideal_partner": ["..."], "marriage_timing": {"favorable_years": ["..."], "favorable_months": ["..."]}, "married_life": ["..."]},
    "health_prediction": {"constitution": "...", "strong_areas": ["..."], "vulnerable_areas": ["..."], "remedies": ["..."]},
    "wealth_prediction": {"overall_rating": "...", "wealth_sources": ["..."], "peak_periods": ["..."], "cautions": ["..."]},
    "dasha_analysis": {"current_dasha": "...", "current_period": "...", "current_effects": ["..."], "upcoming": [{"period": "...", "planet": "...", "effects": ["..."]}]},
    "mangal_dosha": {"has_dosha": false, "severity": "...", "effects": "...", "remedies": ["..."]},
    "remedies": {"gemstones": [{"stone": "...", "planet": "...", "benefit": "..."}], "mantras": [{"mantra": "...", "planet": "...", "chanting": "..."}], "general": ["..."]}
}"""

    user_prompt = f"""Generate a premium Brihat Kundli Pro report for {request.full_name} using this calculated chart:

{chart_summary}

Use the exact house placements and planetary positions above. Make every prediction specific to the actual chart data."""

    try:
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        response_text = message.content[0].text
        import re, json
        clean = re.sub(r'```(?:json)?\s*', '', response_text).replace('```', '').strip()
        return json.loads(clean)
    except Exception as e:
        logging.error(f"Error generating Brihat Kundli: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate Brihat Kundli: {str(e)}")

@api_router.post("/brihat-kundli/generate")
async def generate_brihat_kundli(request: BrihatKundliRequest, user_email: str = ""):
    """Generate comprehensive Brihat Kundli Pro report"""
    
    try:
        # Generate the report using AI
        report_data = await generate_brihat_kundli_with_llm(request)
        
        # Create report document
        report = BrihatKundliReport(
            user_email=user_email,
            full_name=request.full_name,
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            place_of_birth=request.place_of_birth,
            gender=request.gender,
            ascendant=report_data.get("ascendant", {}),
            moon_sign=report_data.get("moon_sign", {}),
            sun_sign=report_data.get("sun_sign", {}),
            planetary_positions=report_data.get("planetary_positions", []),
            career_prediction=report_data.get("career_prediction", {}),
            love_prediction=report_data.get("love_prediction", {}),
            health_prediction=report_data.get("health_prediction", {}),
            wealth_prediction=report_data.get("wealth_prediction", {}),
            family_prediction=report_data.get("family_prediction", {}),
            education_prediction=report_data.get("education_prediction", {}),
            current_dasha=report_data.get("current_dasha", {}),
            dasha_timeline=report_data.get("dasha_timeline", []),
            mangal_dosha=report_data.get("mangal_dosha", {}),
            kalsarp_dosha=report_data.get("kalsarp_dosha", {}),
            other_doshas=report_data.get("other_doshas", []),
            benefic_yogas=report_data.get("benefic_yogas", []),
            malefic_yogas=report_data.get("malefic_yogas", []),
            gemstone_remedies=report_data.get("gemstone_remedies", []),
            mantra_remedies=report_data.get("mantra_remedies", []),
            lifestyle_remedies=report_data.get("lifestyle_remedies", []),
            donation_remedies=report_data.get("donation_remedies", []),
            lucky_numbers=report_data.get("lucky_numbers", []),
            lucky_colors=report_data.get("lucky_colors", []),
            lucky_days=report_data.get("lucky_days", []),
            lucky_direction=report_data.get("lucky_direction", ""),
            numerology=report_data.get("numerology", {})
        )
        
        # Store in database
        doc = report.model_dump(mode='json')
        await db.brihat_kundli_reports.insert_one(doc)
        
        return {"success": True, "report_id": report.id, "report": doc}
        
    except Exception as e:
        logging.error(f"Brihat Kundli generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@api_router.get("/brihat-kundli/{report_id}")
async def get_brihat_kundli(report_id: str):
    """Get existing Brihat Kundli report"""
    
    report = await db.brihat_kundli_reports.find_one(
        {"id": report_id},
        {"_id": 0}
    )
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report

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
    except Exception as e:
        logging.warning(f"Vedic calculator failed for Kundali Milan: {e}")

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
        return compatibility_score, message.content[0].text
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
    
    score, analysis = await generate_kundali_milan_with_llm(birth_profile1, birth_profile2)
    
    report = KundaliMilanReport(
        person1_id=request.person1_id,
        person2_id=request.person2_id,
        compatibility_score=score,
        detailed_analysis=analysis
    )
    
    doc = report.model_dump(mode='json')
    await db.kundali_milan_reports.insert_one(doc)
    
    return report

@api_router.get("/kundali-milan/{report_id}/pdf")
async def download_kundali_milan_pdf(report_id: str, user_email: str = None):
    """Generate and download Kundali Milan PDF"""
    
    # Get report
    report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Get both profiles
    person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
    person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
    
    if not person1 or not person2:
        raise HTTPException(status_code=404, detail="Profiles not found")
    
    try:
        pdf_buffer = generate_kundali_milan_pdf(
            person1, 
            person2, 
            report['compatibility_score'], 
            report['detailed_analysis']
        )
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=kundali_milan_{person1['name']}_{person2['name']}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
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
    
    # Check active subscription
    subscription = await db.subscriptions.find_one({
        "user_email": user_email,
        "status": "active",
        "subscription_type": "premium_monthly"
    })
    
    if subscription:
        expires_at = subscription.get('expires_at')
        if expires_at is None:
            # No expiry set — treat as valid (manually created / lifetime test record)
            return True
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        # Make expires_at timezone-aware if it isn't
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at > datetime.now(timezone.utc):
            return True
    
    # Check one-time payment for specific report
    payment = await db.payments.find_one({
        "user_email": user_email,
        "report_type": report_type,
        "report_id": report_id,
        "status": "completed"
    })
    
    if payment:
        return True

    # Also grant access if user has active premium_monthly payment (covers all reports)
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
    
    # Validate report type first (outside try-catch to return proper 400)
    if request.report_type not in PRICING:
        raise HTTPException(status_code=400, detail="Invalid report type")
    
    try:
        amount_paise = int(PRICING[request.report_type] * 100)  # Convert to paise
        
        # Create Razorpay order
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
        
        # Store order in database
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
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Get payment record
        payment_doc = await db.payments.find_one(
            {"razorpay_order_id": razorpay_order_id},
            {"_id": 0}
        )
        
        if not payment_doc:
            raise HTTPException(status_code=404, detail="Payment record not found")
        
        # Update payment status
        await db.payments.update_one(
            {"razorpay_order_id": razorpay_order_id},
            {
                "$set": {
                    "razorpay_payment_id": razorpay_payment_id,
                    "status": "completed"
                }
            }
        )
        
        # If monthly subscription, create subscription record
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
        
        return {
            "status": "success",
            "message": "Payment verified successfully",
            "payment_id": razorpay_payment_id
        }
        
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
    
    # For demo mode, allow PDF download without strict premium check
    # In production, uncomment the premium check below
    # has_access = await check_premium_access(user_email, "birth_chart", profile_id)
    # if not has_access:
    #     raise HTTPException(status_code=403, detail="Premium access required")
    
    # Get profile and report
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    report = await db.birth_chart_reports.find_one({"profile_id": profile_id}, {"_id": 0})
    
    if not profile or not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        # Generate PDF
        pdf_buffer = generate_birth_chart_pdf(profile, report['report_content'])
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=birth_chart_{profile['name'].replace(' ', '_')}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        logging.error(f"PDF generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

# Share Link Endpoints
@api_router.post("/share/create")
async def create_share_link(report_type: str, report_id: str):
    """Create shareable link for report"""
    
    # Check if share link already exists
    existing = await db.share_links.find_one({
        "report_type": report_type,
        "report_id": report_id
    }, {"_id": 0})
    
    if existing:
        if isinstance(existing['created_at'], str):
            existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return ShareLink(**existing)
    
    # Create new share link
    share_link = ShareLink(
        report_type=report_type,
        report_id=report_id
    )
    
    doc = share_link.model_dump(mode='json')
    await db.share_links.insert_one(doc)
    
    return share_link

@api_router.get("/share/{token}")
async def get_shared_report(token: str):
    """Get report via share link (public access)"""
    
    share_link = await db.share_links.find_one({"token": token}, {"_id": 0})
    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")
    
    # Increment view count
    await db.share_links.update_one(
        {"token": token},
        {"$inc": {"views": 1}}
    )
    
    report_type = share_link['report_type']
    report_id = share_link['report_id']
    
    if report_type == "birth_chart":
        profile = await db.birth_profiles.find_one({"id": report_id}, {"_id": 0})
        report = await db.birth_chart_reports.find_one({"profile_id": report_id}, {"_id": 0})
        
        if not profile or not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "type": "birth_chart",
            "profile": profile,
            "report": report
        }
    
    elif report_type == "kundali_milan":
        report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
        person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
        
        return {
            "type": "kundali_milan",
            "report": report,
            "person1": person1,
            "person2": person2
        }
    
    raise HTTPException(status_code=400, detail="Invalid report type")

# Authentication Endpoints
@api_router.post("/auth/register")
async def register(request: RegisterRequest, response: Response):
    """Register new user with email/password"""
    
    # Check if user exists
    existing = await db.users.find_one({"email": request.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password)
    )
    
    doc = user.model_dump(mode='json')
    await db.users.insert_one(doc)
    
    # Send welcome email
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
    
    # Notify admin of new registration
    admin_email = os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com')
    admin_body = f"""
    <div style="font-family: Arial, sans-serif;">
        <h3>New User Registration</h3>
        <p><b>Name:</b> {user.name}</p>
        <p><b>Email:</b> {user.email}</p>
        <p><b>Time:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
    </div>
    """
    await send_email_notification(admin_email, f"New Registration: {user.name}", admin_body)
    
    # Create session
    session_token = await create_session(db, user.user_id)
    set_session_cookie(response, session_token)
    
    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        picture=user.picture
    )

@api_router.post("/auth/login")
async def login(request: LoginRequest, response: Response):
    """Login with email/password — with brute force protection"""
    
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user_doc.get('password_hash'):
        raise HTTPException(status_code=401, detail="Please login with Google")
    
    # Check if account is locked
    locked_until = user_doc.get('locked_until')
    if locked_until:
        if isinstance(locked_until, str):
            locked_until = datetime.fromisoformat(locked_until)
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < locked_until:
            remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds() / 60)
            raise HTTPException(
                status_code=429,
                detail=f"Account locked due to too many failed attempts. Try again in {remaining} minutes."
            )
        else:
            # Lock expired — reset attempts
            await db.users.update_one(
                {"email": request.email},
                {"$unset": {"locked_until": "", "failed_attempts": ""}}
            )
    
    if not verify_password(request.password, user_doc['password_hash']):
        # Increment failed attempts
        failed = user_doc.get('failed_attempts', 0) + 1
        update = {"$set": {"failed_attempts": failed}}
        
        if failed >= 5:
            # Lock account for 24 hours
            lock_until = datetime.now(timezone.utc) + timedelta(hours=24)
            update = {"$set": {"failed_attempts": failed, "locked_until": lock_until.isoformat()}}
            await db.users.update_one({"email": request.email}, update)
            raise HTTPException(
                status_code=429,
                detail="Account locked for 24 hours due to too many failed login attempts. Please check your email."
            )
        
        await db.users.update_one({"email": request.email}, update)
        remaining_attempts = 5 - failed
        raise HTTPException(
            status_code=401,
            detail=f"Invalid email or password. {remaining_attempts} attempt{'s' if remaining_attempts != 1 else ''} remaining before account lockout."
        )
    
    # Successful login — reset failed attempts
    await db.users.update_one(
        {"email": request.email},
        {"$unset": {"failed_attempts": "", "locked_until": ""}}
    )
    
    # Create session
    session_token = await create_session(db, user_doc['user_id'])
    set_session_cookie(response, session_token)
    
    return UserResponse(
        user_id=user_doc['user_id'],
        email=user_doc['email'],
        name=user_doc['name'],
        picture=user_doc.get('picture')
    )

@api_router.post("/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Send password reset email"""
    import secrets as secrets_module
    
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    
    # Always return success to prevent email enumeration
    if not user_doc:
        return {"message": "If that email exists, a reset link has been sent."}
    
    if not user_doc.get('password_hash'):
        return {"message": "If that email exists, a reset link has been sent."}
    
    # Generate reset token
    reset_token = secrets_module.token_urlsafe(32)
    reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    
    await db.users.update_one(
        {"email": request.email},
        {"$set": {
            "reset_token": reset_token,
            "reset_token_expires": reset_expires.isoformat()
        }}
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
    
    await send_email_notification(
        request.email,
        "Reset your Everyday Horoscope password",
        email_body
    )
    
    logging.info(f"Password reset email sent to {request.email}")
    
    return {"message": "If that email exists, a reset link has been sent."}

@api_router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset password using token"""
    
    user_doc = await db.users.find_one({"reset_token": request.token}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    # Check token expiry
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
    
    # Update password and clear reset token
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
    # Support both JSON body and query param
    code = (body.session_id if body else None) or session_id
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    # REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    
    try:
        # Exchange session_id for user data
        user_data = await exchange_session_id_for_token(code)
        
        # Get or create user
        user = await get_or_create_oauth_user(
            db,
            email=user_data['email'],
            name=user_data['name'],
            picture=user_data.get('picture'),
            google_id=user_data['id']
        )
        
        # Create session
        session_token = await create_session(db, user.user_id)
        set_session_cookie(response, session_token)
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            picture=user.picture
        )
        
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
    
    await db.policies.update_one(
        {"type": policy_type},
        {"$set": policy_data},
        upsert=True
    )
    
    return {"success": True, "message": f"Policy '{policy_type}' updated successfully"}

@api_router.get("/admin/policies")
async def get_all_policies(request: Request):
    """Get all policies for admin"""
    await require_admin(request, db)
    policies = await db.policies.find({}, {"_id": 0}).to_list(100)
    return {"policies": policies}

# ============== END POLICY ENDPOINTS ==============

@api_router.post("/admin/policies/seed")
async def seed_policies(request: Request):
    """Seed initial policy documents into database (run once)"""
    await require_admin(request, db)
    
    policies_data = {
  "terms": {
    "type": "terms",
    "title": "Terms of Service",
    "effective_date": "18th February 2026",
    "last_updated": "18th February 2026",
    "company": "SkyHound Studios",
    "sections": [
      {
        "heading": "TERMS OF SERVICE",
        "content": "Effective Date: 18 February 2026 Last Updated: 18 February 2026 These Terms of Service (\"Terms\") govern your access to and use of: • Website: www.everydayhoroscope.in • Mobile Application: Celestial AI • All related services, artificial intelligence systems, digital content, personalized reports, consultations, subscription features, and marketplace offerings (collectively referred to as the \"Services\") These Services are provided by: SkyHound Studios (\"Company\", \"we\", \"us\", \"our\"). By accessing, registering, purchasing, downloading, installing, or otherwise using any part of the Services, you (\"User\", \"Member\", \"you\", or \"your\") acknowledge that you have read, understood, and agreed to be legally bound by these Terms. If you do not agree with these Terms, you must immediately discontinue use of the Services."
      },
      {
        "heading": "DEFINITIONS",
        "content": "For the purpose of clarity within these Terms: • \"Services\" refers to all digital and physical offerings provided through the Platform, including AI-generated insights, spiritual guidance tools, reports, subscriptions, consultations, and marketplace products. • \"Platform\" refers to the website, mobile applications, APIs, software systems, and digital infrastructure operated by the Company. • \"Content\" includes all reports, AI-generated outputs, text, graphics, data, audio, video, design elements, and informational material made available through the Services. • \"AI Services\" refers to automated guidance, predictions, or recommendations generated using algorithmic models, machine learning systems, or artificial intelligence technologies. • \"User Data\" means any information submitted, uploaded, or generated by Users while interacting with the Platform. • \"Remedies\" refers to traditional spiritual, cultural, or metaphysical practices suggested through the Services. • \"Marketplace Products\" refers to goods or services offered for sale via the Platform, including physical and digital items."
      },
      {
        "heading": "NATURE OF SERVICES",
        "content": "The Platform provides AI-assisted spiritual, astrological, and behavioral insights intended to support: • Personal reflection • Emotional awareness • Spiritual exploration • Personal growth and self-development The Services are interpretive, experiential, and belief-based in nature. They are not scientific or deterministic in their outcomes. The Company does not guarantee accuracy, completeness, or specific life outcomes resulting from the use of the Services."
      },
      {
        "heading": "3.1 Not Professional Advice",
        "content": "The Services are provided for informational, reflective, and experiential purposes only and do not constitute: • Medical advice or diagnosis • Psychological therapy or mental health counseling • Financial or investment advice • Legal advice Users are strongly encouraged to seek guidance from licensed professionals for matters involving health, legal rights, or financial decisions."
      },
      {
        "heading": "3.2 AI Output & Hallucination Risk",
        "content": "AI-generated outputs are produced using probabilistic computational models. As such, they: • May be incomplete, inaccurate, or outdated • May contain interpretive or speculative content • Should not be relied upon as definitive statements of fact Users acknowledge and accept that reliance on AI-generated insights is undertaken at their own discretion."
      },
      {
        "heading": "3.3 Remedies & Physical Risk",
        "content": "Any remedies or spiritual practices suggested through the Platform: • Are derived from cultural or traditional belief systems • May involve physical actions, environmental changes, or lifestyle modifications Users assume full responsibility for evaluating the suitability, safety, and potential consequences of adopting such remedies."
      },
      {
        "heading": "3.4 Spiritual Neutrality",
        "content": "The Platform does not promote or impose any particular belief system. Users engage with spiritual or astrological content voluntarily and may accept or disregard such guidance at their discretion."
      },
      {
        "heading": "3.5 Psychological Reliance",
        "content": "Users acknowledge that spiritual or predictive content may influence emotional perceptions. The Company does not assume responsibility for emotional reactions, psychological reliance, or personal interpretations of the Services."
      },
      {
        "heading": "ELIGIBILITY",
        "content": "To use the Services, Users must: • Be at least 18 years of age • Possess legal capacity to enter into binding agreements • Not be restricted from accessing the Services under applicable law The Company reserves the right to restrict access in certain jurisdictions to comply with legal or regulatory requirements."
      },
      {
        "heading": "ACCOUNT REGISTRATION, CREDENTIALS & SECURITY",
        "content": "Upon registration, Users may be required to provide certain personal or account-related information (\"Registration Data\"). Users agree that all Registration Data provided shall be accurate, complete, and kept up to date. Users are solely responsible for maintaining the confidentiality of their account credentials, including email ID, password, authentication methods, and access devices. Users agree: • Not to transfer, sell, assign, or share account credentials • To immediately notify the Company of unauthorized use or security breach • To take reasonable precautions to prevent misuse All activity conducted through a User's account shall be deemed authorized by that User unless proven otherwise under applicable law. The Company shall not be liable for losses arising from failure to safeguard account credentials. Accounts are personal and non-transferable. Unauthorized sharing or transfer may result in suspension."
      },
      {
        "heading": "ADMINISTRATIVE ACCESS TO USER ACCOUNTS",
        "content": "To ensure proper functioning of the Services, maintain security, investigate complaints, prevent misuse, comply with legal obligations, or protect platform integrity, the Company and its authorized personnel may access User accounts and related records on a limited and case-by-case basis. Such access shall be conducted: • In accordance with applicable laws • Subject to internal security and confidentiality controls • Solely for legitimate operational, compliance, or safety purposes This access does not grant the Company ownership over User-generated content beyond what is necessary to provide Services. USER-GENERATED CONTENT Users are solely responsible for any content they submit, share, or communicate through the Platform. The Company does not endorse or assume liability for: • Statements made by Users • Advice exchanged between Users • Misuse of platform communication features THIRD-PARTY SERVICES & MARKETPLACE The Platform may integrate services or products provided by third parties. The Company does not assume responsibility for: • Product quality or defects • Payment gateway interruptions • External service provider actions Users interact with third-party services at their own risk."
      },
      {
        "heading": "PAYMENTS, SUBSCRIPTIONS & WALLET",
        "content": "Certain Services may require payment. • Subscriptions may renew automatically unless cancelled. • Digital services are generally non-refundable after delivery. Refer Subscription terms document for more information. • Wallet balances are non-transferable and non-interest bearing. Chargebacks initiated without prior communication may result in account suspension."
      },
      {
        "heading": "ACCEPTABLE USE",
        "content": "Users must not: • Extract or scrape platform data • Use platform content to train AI models • Attempt unauthorized system access • Engage in unlawful or harmful activities Violation may result in termination and legal action."
      },
      {
        "heading": "INTELLECTUAL PROPERTY",
        "content": "All intellectual property rights in and to the Platform and the Services, including but not limited to software code, algorithms, AI models, system architecture, databases, design elements, user interfaces, visual assets, audio-visual content, written materials, spiritual interpretations, predictive frameworks, remedy methodologies, and proprietary analytical systems (collectively, the \"Company IP\"), are owned by or licensed to SkyHound Studios. Nothing in these Terms grants Users any ownership interest in the Company IP. Users are granted a limited, non-exclusive, non-transferable, revocable license to access and use the Services solely for personal, non-commercial purposes and in accordance with these Terms. Users must not, without prior written consent of the Company: • Copy, reproduce, distribute, publish, display, or commercially exploit any part of the Services or Content • Reverse engineer, decompile, disassemble, or attempt to derive source code or underlying models • Extract or systematically collect data from the Platform • Use any Content or system outputs to develop competing products or services • Use automated tools, bots, or scraping mechanisms to access the Platform • Use platform data, outputs, or content for training, fine-tuning, or improving artificial intelligence or machine learning systems All trademarks, service marks, logos, trade names, and branding elements displayed on the Platform are the property of the Company or its licensors. Unauthorized use is strictly prohibited. User feedback, suggestions, or ideas provided to the Company may be used without restriction or compensation unless otherwise agreed."
      },
      {
        "heading": "DATA PROCESSING & AI TRAINING",
        "content": "The Company processes User Data in accordance with applicable privacy laws and its Privacy Policy. To improve the quality, safety, and effectiveness of the Services, the Company may process: • Aggregated data • Anonymized data • De-identified behavioral insights • Platform interaction metrics Such data may be used for purposes including: • Enhancing AI model performance • Improving personalization accuracy • Developing new features • Conducting internal research and analytics • Ensuring system reliability and safety The Company does not sell personal data to third parties without lawful basis or user consent. Users acknowledge that AI systems may learn from generalized patterns derived from anonymized or aggregated platform usage. However, the Company implements safeguards designed to prevent identification of individual Users through AI training processes. Where required by law, explicit consent mechanisms may be provided for specific categories of data processing. Users may exercise rights related to access, correction, deletion, or restriction of their personal data as described in the Privacy Policy."
      },
      {
        "heading": "SERVICE AVAILABILITY",
        "content": "The Services are provided on an \"as-is\" and \"as-available\" basis. We do not guarantee: • Continuous availability • Error-free operation • Uninterrupted access"
      },
      {
        "heading": "LIMITATION OF LIABILITY",
        "content": "The Company shall not be liable for: • Indirect or consequential damages • Financial losses arising from decisions based on platform insights • Emotional or psychological outcomes • Outcomes related to remedies or spiritual practices Total liability shall not exceed the greater of: • Fees paid by the User in the preceding 12 months • INR equivalent of USD $100"
      },
      {
        "heading": "INDEMNIFICATION",
        "content": "You agree to indemnify and hold harmless SkyHound Studios and its affiliates from any claims, damages, liabilities, losses, costs, or expenses (including legal fees) arising from: • Your violation of these Terms • Your violation of any applicable law or regulation • Your infringement of any third-party rights, including intellectual property rights • Content submitted or shared by you • Your reliance on AI outputs or remedies • Misuse of Services or marketplace products"
      },
      {
        "heading": "FORCE MAJEURE",
        "content": "The Company shall not be liable for delays or failures due to events beyond reasonable control, including: • Natural disasters • Infrastructure outages • Government actions • Cyber incidents"
      },
      {
        "heading": "ACCOUNT SUSPENSION",
        "content": "The Company shall have the absolute right, exercisable at its sole and exclusive discretion, to suspend, restrict, limit, deactivate, or permanently terminate a User's access to the Services, in whole or in part, at any time, with or without prior notice, and without obligation to provide justification, where the Company determines such action is necessary or appropriate. Such action may be taken for reasons including, but not limited to: • Suspected fraud, misuse, or abuse of the Services • Violation of Terms, Supplemental Terms, or Platform policies • Attempts to manipulate or exploit AI systems or platform infrastructure • Use of Services for unlawful, harmful, or deceptive purposes • Chargebacks, payment disputes, or payment irregularities • Submission of false or misleading registration information • Activities exposing the Company or Users to legal, reputational, or security risks • Conduct detrimental to the integrity, safety, or commercial interests of the Platform The Company shall not be liable for losses arising from enforcement actions taken under this Clause. Upon suspension or termination: • Access to Services may be revoked immediately • Outstanding financial obligations remain enforceable • User data may be retained as required by law or legitimate business purposes • Future access may be restricted The Company retains sole, final, and binding authority regarding reinstatement or permanent deactivation."
      },
      {
        "heading": "DISPUTE RESOLUTION",
        "content": "The Company aims to resolve disputes in a fair, efficient, and user-focused manner. Users are encouraged to first contact customer support to seek an amicable resolution of any concern, complaint, or dispute arising from use of the Services. If a dispute cannot be resolved informally, the matter shall be resolved through binding arbitration, in accordance with applicable Indian arbitration laws. Key principles: • Arbitration shall be conducted by a single arbitrator • The seat and venue of arbitration shall be Delhi, India • Proceedings shall be conducted in the English language • Arbitration decisions shall be final and binding on both parties Nothing in this clause prevents either party from seeking interim relief, including injunctive remedies, from courts of competent jurisdiction where necessary to protect legal rights. To the extent permitted by law, Users agree to resolve disputes on an individual basis, and not as part of a class or collective proceeding."
      },
      {
        "heading": "CHANGES TO TERMS",
        "content": "The Company may update or modify these Terms from time to time to reflect: • Changes in laws or regulatory requirements • Updates to Services or features • Technological developments • Business or operational adjustments Where changes are material, reasonable efforts will be made to notify Users through: • Platform notifications • Email communication • Updated publication on the Website or Application Continued use of the Services after updated Terms become effective shall constitute acceptance of such changes. Users who do not agree with revised Terms must discontinue use of the Services prior to the effective date of the updated Terms. The latest version of the Terms shall always be available on the Platform."
      },
      {
        "heading": "20.1. Entire Agreement",
        "content": "These Terms of Service, together with any applicable Supplemental Terms, policies, or agreements referenced herein, constitute the entire agreement between the User and the Company regarding access to and use of the Services and supersede all prior or contemporaneous communications, understandings, or agreements, whether written or oral. No oral statements or representations shall modify these Terms unless expressly agreed in writing by the Company."
      },
      {
        "heading": "20.2. Supplemental Terms",
        "content": "Certain features, services, or offerings may be governed by additional terms, policies, or agreements (\"Supplemental Terms\"), including but not limited to: • Privacy Policy • Subscription Terms • Refund & Cancellation Policy • Marketplace Terms • Seller Agreements • AI Transparency or Safety Policies • Feature-specific terms presented within the Platform In the event of any inconsistency between these Terms of Service and any Supplemental Terms, the provisions of the relevant Supplemental Terms shall prevail only with respect to the specific subject matter governed by such Supplemental Terms and solely to the extent of such inconsistency. All other provisions of these Terms shall remain in full force."
      },
      {
        "heading": "20.3. Amendments & Updates",
        "content": "The Company reserves the right to modify or update these Terms or any Supplemental Terms from time to time to reflect: • Changes in law or regulation • Technological developments • Service enhancements • Business or operational changes Where required, reasonable notice will be provided. Continued use of the Services after updates constitutes acceptance."
      },
      {
        "heading": "20.4. Assignment",
        "content": "The User may not assign, transfer, sublicense, or otherwise delegate any rights or obligations under these Terms without prior written consent of the Company. The Company may assign or transfer its rights and obligations: • To affiliates • In connection with mergers, acquisitions, restructuring, or asset transfers • As part of financing or corporate reorganization These Terms shall bind successors and permitted assigns."
      },
      {
        "heading": "20.5. Waiver",
        "content": "Failure by the Company to enforce any provision of these Terms shall not constitute a waiver of that provision or any other provision. Any waiver must be: • Explicit • In writing • Signed by an authorized representative"
      },
      {
        "heading": "20.6. Severability",
        "content": "If any provision of these Terms is held to be invalid, unlawful, or unenforceable by a court or tribunal of competent jurisdiction: • Such provision shall be modified to the minimum extent necessary to make it enforceable • The remaining provisions shall remain valid and enforceable"
      },
      {
        "heading": "20.7. No Agency or Partnership",
        "content": "Nothing in these Terms creates: • Partnership • Joint venture • Employment relationship • Agency relationship Users act solely in their individual capacity."
      },
      {
        "heading": "20.8. Force Majeure",
        "content": "The Company shall not be liable for failure or delay in performance due to events beyond reasonable control, including: • Natural disasters • Government actions • Infrastructure outages • Cyber incidents • Third-party service failures"
      },
      {
        "heading": "20.9. Interpretation",
        "content": "Headings are for convenience only and do not affect interpretation. Words such as \"including\" shall be interpreted as \"including without limitation.\""
      },
      {
        "heading": "20.10. Governing Law",
        "content": "These Terms shall be governed by and construed in accordance with the laws of India."
      },
      {
        "heading": "20.11. Dispute Resolution & Jurisdiction",
        "content": "Subject to any arbitration clause set forth herein, Users agree to submit to the exclusive jurisdiction of courts located in Delhi, India."
      },
      {
        "heading": "20.12. Limitation Interaction with Supplemental Terms",
        "content": "The limitation of liability provisions contained in these Terms shall apply to all Services unless a Supplemental Term expressly provides otherwise for a specific service or feature. No Supplemental Term shall be interpreted as expanding the Company's liability beyond the limits set forth herein unless explicitly stated."
      },
      {
        "heading": "20.13. Survival",
        "content": "Provisions that by their nature should survive termination shall remain in effect, including but not limited to: • Intellectual Property • Limitation of Liability • Indemnification • Dispute Resolution • Data Processing • AI Usage • Payment obligations"
      },
      {
        "heading": "CONTACT",
        "content": "SkyHound Studios Email: prateekmalhotra.contentcreator@gmail.com"
      }
    ]
  },
  "privacy": {
    "type": "privacy",
    "title": "Privacy Policy",
    "effective_date": "18th February 2026",
    "last_updated": "18th February 2026",
    "company": "SkyHound Studios",
    "sections": [
      {
        "heading": "PRIVACY POLICY",
        "content": "Effective Date: 18 February 2026 Last Updated: 18 February 2026 This Privacy Policy describes how SkyHound Studios (\"Company\", \"we\", \"us\", or \"our\") collects, uses, stores, processes, shares, and safeguards personal data when you access or use: • Website: www.everydayhoroscope.in • Mobile Application: Celestial AI • Any related services, digital features, AI systems, consultations, subscriptions, marketplace offerings, or communication channels (collectively referred to as the \"Services\") By accessing or using the Services, you acknowledge that you have read and understood this Privacy Policy and consent to the data practices described herein."
      },
      {
        "heading": "SCOPE OF THIS POLICY",
        "content": "This Privacy Policy applies to all individuals interacting with our Services, including: • Registered users • Website visitors • Mobile application users • Customers purchasing reports, subscriptions, or products • Individuals interacting with AI-driven tools or consultations • Users engaging with spiritual, behavioral, manifestation, or wellness features This Policy governs both online and in-app interactions."
      },
      {
        "heading": "2.1 Identity & Contact Information",
        "content": "This may include: • Name • Email address • Phone number • Country or general location • Profile information voluntarily provided This information helps us manage accounts, deliver services, and communicate effectively."
      },
      {
        "heading": "2.2 Astrological & Spiritual Data",
        "content": "To provide personalized insights, we may collect: • Date, time, and place of birth • Personal reflections or journaling inputs • Spiritual preferences or belief indicators • Manifestation goals or intentions Depending on applicable law, this category may be treated as sensitive personal data, and we apply appropriate safeguards."
      },
      {
        "heading": "2.3 Behavioural & Interaction Data",
        "content": "We may automatically collect information regarding how Users interact with the Platform, including: • App usage patterns • Clickstream data • Session duration • Notification engagement behavior • Emotional inputs or mood-tracking indicators • Feature interaction history This data enables personalization, service optimization, and AI model improvement."
      },
      {
        "heading": "2.4 AI Interaction Data",
        "content": "When Users interact with AI-driven features, we may process: • User queries and prompts • Generated responses • Contextual signals used to improve interactions • Behavioral inference outputs This data helps refine AI performance and enhance user experience."
      },
      {
        "heading": "2.5 Transaction & Payment Data",
        "content": "Payments are processed through secure third-party payment providers. We do not store: • Full credit or debit card numbers • Payment authentication credentials However, we may retain limited transactional metadata for accounting, fraud prevention, and legal compliance."
      },
      {
        "heading": "2.6 Device & Technical Data",
        "content": "• We may collect technical information such as: ``` <!-- -- ``` • IP address • Device type and identifiers • Operating system version • Network information • Cookies or tracking identifiers This supports platform functionality, security, and analytics. LEGAL BASIS FOR PROCESSING (GDPR) Where applicable, we process personal data based on: • User consent • Contractual necessity for service delivery • Legitimate business interests • Compliance with legal obligations Sensitive personal data is processed only with explicit consent or other lawful basis."
      },
      {
        "heading": "PURPOSES OF PROCESSING",
        "content": "We process personal data to: • Provide personalized spiritual and astrological insights • Generate AI-driven recommendations and reports • Improve behavioral models and predictive systems • Deliver notifications, content, and updates • Process transactions and subscriptions • Prevent fraud, misuse, or security incidents • Conduct analytics, research, and product development • Enhance overall service quality and user experience AUTOMATED DECISION-MAKING & PROFILING Our Services may use automated systems for: • Predictive insights • Behavioral pattern analysis • Recommendation generation These systems: • Do not make legally binding or life-altering decisions • Are intended for informational, reflective, and experiential purposes Users may request human review or clarification where applicable."
      },
      {
        "heading": "AI MODEL TRAINING & DATA USE",
        "content": "To enhance the quality, safety, accuracy, and effectiveness of our Services, the Company may use certain categories of data to improve artificial intelligence and machine learning systems that power the Platform. This may include the use of: • Aggregated data that does not identify individual Users • Anonymized or de-identified datasets • Pseudonymized interaction patterns • Generalized behavioral trends • System performance metrics • Error correction signals • Content quality evaluation data Such processing enables the Company to: • Improve AI recommendation accuracy • Enhance personalization relevance • Reduce system errors and hallucinations • Strengthen safety and ethical safeguards • Develop new features or analytical capabilities • Improve user experience and platform performance The Company does not use identifiable personal data for external AI training, commercialization, or sale to third parties without a lawful basis or explicit user consent, where required under applicable law. Where feasible and appropriate, the Company implements safeguards to: • Prevent re-identification of Users from AI training datasets • Minimize exposure of sensitive personal information • Limit training data access to authorized systems or personnel • Apply data minimization and purpose limitation principles AI systems are trained on patterns and statistical relationships rather than individual user identities. Outputs generated by AI systems are not intended to reproduce or reveal personal data of any specific User. Users acknowledge that interactions with AI systems may contribute, in aggregated or anonymized form, to ongoing system improvement. Where legally required, Users may be provided with options to: • Object to certain categories of automated processing • Withdraw consent for specific data uses • Request deletion of personal data from active datasets, subject to technical feasibility and legal obligations The Company continuously evaluates AI training practices to align with evolving regulatory frameworks, including data protection laws and emerging AI governance standards. DATA SHARING & THIRD-PARTY PROCESSORS We may share personal data with trusted service providers, including: • Cloud infrastructure providers • Payment processors • Analytics platforms • Customer support tools • Legal or regulatory authorities where required All third-party partners are subject to contractual data protection obligations."
      },
      {
        "heading": "INTERNATIONAL DATA TRANSFERS",
        "content": "Personal data may be processed or stored in jurisdictions outside your country of residence. Where such transfers occur, we implement safeguards such as: • Standard contractual clauses • Adequacy mechanisms • Industry-standard security measures"
      },
      {
        "heading": "DATA RETENTION",
        "content": "We retain personal data only for as long as necessary to: • Provide Services • Comply with legal obligations • Prevent fraud or misuse • Improve platform functionality Users may request deletion, subject to legal retention requirements. USER RIGHTS (GDPR & GLOBAL RIGHTS) Depending on jurisdiction, Users may have rights to: • Access their personal data ``` <!-- -- ``` • Correct inaccuracies • Request deletion • Restrict or object to processing • Withdraw consent • Request data portability Requests may be submitted to: prateekmalhotra.contentcreator@gmail.com"
      },
      {
        "heading": "DATA SECURITY",
        "content": "We implement technical and organizational safeguards including: • Encryption technologies • Access controls • Monitoring and incident detection systems • Secure hosting infrastructure Despite these measures, no digital system can be guaranteed completely secure."
      },
      {
        "heading": "COOKIES & TRACKING TECHNOLOGIES",
        "content": "We use cookies and similar technologies to: • Maintain user sessions • Analyze usage trends • Personalize user experiences Users may control cookie settings through browser or device preferences. CHILDREN'S PRIVACY Our Services are not intended for individuals under the age of 18. We do not knowingly collect personal data from minors."
      },
      {
        "heading": "SENSITIVE SPIRITUAL & BEHAVIOURAL DATA",
        "content": "Certain data (such as birth details, emotional inputs, or manifestation goals) may be sensitive. We process such data: • Only where necessary for service functionality • With appropriate safeguards and legal basis THIRD-PARTY LINKS & SERVICES Our Platform may contain links to third-party services. We are not responsible for: • External privacy practices • Content or data handling by third parties Users should review third-party policies independently."
      },
      {
        "heading": "POLICY UPDATES",
        "content": "We may update this Privacy Policy periodically to reflect: • Changes in laws or regulations • Technological or operational developments • Updates to Services Material changes will be communicated via platform notices or email."
      },
      {
        "heading": "CONTACT & DATA PROTECTION REQUESTS",
        "content": "SkyHound Studios Email: prateekmalhotra.contentcreator@gmail.com"
      }
    ]
  },
  "subscription-terms": {
    "type": "subscription-terms",
    "title": "Subscription Terms",
    "effective_date": "18th February 2026",
    "last_updated": "18th February 2026",
    "company": "SkyHound Studios",
    "sections": [
      {
        "heading": "SUBSCRIPTION TERMS",
        "content": "Effective Date: 18th February 2026 Last Updated: 18th February 2026 These Subscription Terms (\"Subscription Terms\") govern all recurring paid services and subscription-based offerings provided by SkyHound Studios (\"Company\", \"we\", \"us\", \"our\") through: • Website: www.everydayhoroscope.in • Mobile Application: Celestial AI These Subscription Terms form an integral part of and must be read together with: • Terms of Service • Privacy Policy • Marketplace Terms • Refund Policy (where applicable) By purchasing, activating, or continuing to use any subscription plan, you (\"User\", \"Member\", \"Subscriber\", \"you\") acknowledge that you have read, understood, and agreed to be legally bound by these Subscription Terms."
      },
      {
        "heading": "SUBSCRIPTION SERVICES",
        "content": "Subscription plans may provide access to a range of premium features and digital content, including but not limited to: • Daily or periodic astrological insights • AI-generated spiritual or behavioral guidance • Career Plus or similar personalized reports • Manifestation programs or guided practices • Emotional or behavioral trend analysis • Compatibility or relationship insights • Premium spiritual or educational content • Advanced notification and personalization features All subscription content is intended for informational, experiential, and reflective purposes. The Company does not guarantee any specific personal, professional, emotional, or spiritual outcomes arising from subscription usage."
      },
      {
        "heading": "BILLING & PAYMENT",
        "content": "Subscription fees may be charged on a recurring basis depending on the plan selected, including: • Monthly billing cycles • Quarterly billing cycles • Annual billing cycles Payments may be processed through: • Third-party payment gateways • Mobile platform billing systems (such as app store providers) • In-app wallet mechanisms By subscribing, Users authorize the Company or its payment partners to charge the applicable subscription fees automatically in accordance with the selected billing cycle. Users are responsible for ensuring valid payment methods are maintained at all times. AUTO-RENEWAL Unless cancelled before the end of the applicable billing period, subscriptions will automatically renew for successive periods of the same duration. Users are responsible for: • Monitoring their subscription status • Managing renewal settings • Cancelling subscriptions prior to the next billing cycle if they do not wish to continue Failure to cancel before renewal will result in automatic billing for the subsequent period."
      },
      {
        "heading": "FREE TRIALS",
        "content": "From time to time, the Company may offer free trial access to certain subscription features. Where free trials are provided: • The duration of the trial will be clearly disclosed at the time of activation • The subscription will automatically convert into a paid plan upon expiry of the trial period unless cancelled in advance • Each User may be eligible for only one free trial per subscription offering unless otherwise stated Users are responsible for cancelling prior to trial expiration if they do not wish to continue."
      },
      {
        "heading": "PRICE CHANGES",
        "content": "The Company reserves the right to modify subscription pricing to reflect: • Changes in service offerings • Technological or operational costs • Market conditions • Regulatory requirements Any price changes will typically take effect from the next renewal cycle and may be communicated through: • In-app notifications • Email communication • Platform announcements Continued use of the subscription following a price change constitutes acceptance of the revised pricing."
      },
      {
        "heading": "CANCELLATION",
        "content": "Users may cancel subscriptions at any time through: • Account or profile settings • App store subscription management tools • Customer support requests Cancellation will prevent future billing but will not entitle the User to refunds for the current billing period unless otherwise required by law or expressly stated in a specific offer. Access to subscription features will continue until the end of the paid billing cycle."
      },
      {
        "heading": "REFUNDS",
        "content": "Subscription fees are generally non-refundable once charged, except: • Where required by applicable consumer protection laws • In cases of verified billing errors • Where substantial service outages prevent access for a material period Refund requests must be submitted in accordance with the Company's Refund Policy."
      },
      {
        "heading": "SERVICE AVAILABILITY",
        "content": "Subscription services depend on: • Platform performance and technical infrastructure • Internet connectivity and device compatibility • Third-party service providers While the Company endeavors to maintain reliable access, temporary interruptions, maintenance downtime, or technical issues may occur. Such interruptions do not typically constitute grounds for refunds or compensation unless required by law."
      },
      {
        "heading": "AI & PREDICTION DISCLAIMER",
        "content": "Subscription content may include AI-generated insights or predictive interpretations that are: • Probabilistic and interpretive in nature • Subject to limitations inherent in computational models • Not intended to replace professional advice Users acknowledge that reliance on such insights is undertaken at their own discretion and risk."
      },
      {
        "heading": "ACCOUNT SHARING",
        "content": "Subscriptions are: • Personal to the subscribing User • Non-transferable and non-assignable Unauthorized sharing, resale, or commercial use of subscription access may result in suspension or termination without refund."
      },
      {
        "heading": "TERMINATION",
        "content": "The Company may suspend or terminate subscription access in circumstances including: • Violation of these Subscription Terms or related policies • Fraudulent activity or payment disputes • Failure to maintain valid payment methods • Legal or regulatory risk exposure Termination may occur with or without prior notice depending on the nature of the violation."
      },
      {
        "heading": "LIMITATION OF LIABILITY",
        "content": "To the maximum extent permitted by law, the Company shall not be liable for: • Emotional reliance on subscription content • Financial or personal decisions influenced by insights • Perceived lack of spiritual or predictive outcomes Total liability shall be limited as set forth in the Terms of Service."
      },
      {
        "heading": "GOVERNING LAW",
        "content": "These Subscription Terms shall be governed by and construed in accordance with the laws of India. Any disputes shall fall under the jurisdiction of courts located in Delhi, subject to arbitration provisions where applicable."
      },
      {
        "heading": "CHANGES TO SUBSCRIPTION TERMS",
        "content": "The Company may update or revise these Subscription Terms from time to time to reflect: • Changes in subscription features or pricing • Legal or regulatory developments • Operational adjustments Users will be deemed to have accepted updated Terms by continuing to use subscription services after such updates take effect."
      },
      {
        "heading": "CONTACT",
        "content": "SkyHound Studios Email: prateekmalhotra.contentcreator@gmail.com"
      }
    ]
  },
  "refund-policy": {
    "type": "refund-policy",
    "title": "Refund & Cancellation Policy",
    "effective_date": "18th February 2026",
    "last_updated": "18th February 2026",
    "company": "SkyHound Studios",
    "sections": [
      {
        "heading": "REFUND & CANCELLATION POLICY",
        "content": "Effective Date: 18 February 2026 Last Updated: 18 February 2026 This Refund & Cancellation Policy (\"Policy\") governs all purchases made through: • Website: www.everydayhoroscope.in • Mobile Application: Celestial AI Operated by: SkyHound Studios (\"Company\", \"we\", \"us\", \"our\"). By purchasing any service, report, consultation, subscription, or product, you (\"User\", \"Member\", \"Customer\") acknowledge and agree to this Policy."
      },
      {
        "heading": "NATURE OF SERVICES",
        "content": "The Platform provides digital and physical offerings including: • AI-generated astrological insights • Spiritual guidance and consultations • Personalized reports and forecasts • Subscription-based spiritual content • Ritual or remedy-related services • Marketplace products Most Services involve: • Immediate or near-instant digital delivery • Personalized interpretive content • Belief-based spiritual frameworks Accordingly, refund eligibility is limited. GENERAL NO-REFUND PRINCIPLE Except where required by applicable law, purchases are final and non-refundable once: • Digital content is accessed or delivered • Reports are generated • Consultations are initiated • Subscription billing cycle begins • Spiritual or ritual services are fulfilled Dissatisfaction arising from: • Predictions • Interpretations • Spiritual outcomes • Emotional expectations does not qualify for refund."
      },
      {
        "heading": "LIMITED ELIGIBLE REFUND SCENARIOS",
        "content": "Refund requests may be considered only under the following conditions:"
      },
      {
        "heading": "3.1 Duplicate Payment",
        "content": "Where a User is charged more than once for the same transaction, one payment may be refunded after verification."
      },
      {
        "heading": "3.2 Technical Failure or Non-Delivery",
        "content": "If: • Payment has been successfully completed • Service was not delivered due to technical or system error User must notify the Company within 24 hours of the failed transaction. Refunds will be processed only after internal verification confirms non-delivery."
      },
      {
        "heading": "3.3 Consultation Wallet Deduction Error",
        "content": "Where wallet balance is deducted due to technical malfunction but the consultation does not occur at all: • User must notify the Company within 24 hours • Claims will be reviewed after system validation • Requests submitted after 24 hours may not be entertained Wallet balances are: • Non-transferable • Non-refundable • Intended solely for use within the Platform"
      },
      {
        "heading": "DIGITAL REPORTS & PERSONALIZED SERVICES",
        "content": "Personalized reports are generated based on User-provided data. Accordingly: • No refund shall be granted where incorrect or incomplete data is provided by the User • Once report generation begins, the service is deemed delivered • Reports cannot be \"returned\" due to dissatisfaction with outcomes Consultations are non-refundable once initiated, regardless of duration or perceived quality. TWO-HOUR CANCELLATION WINDOW (PRE-SERVICE) Refund requests may be considered if: • The User emails the Company within 2 hours of payment, AND • The Paid Service has not yet been accessed, initiated, or fulfilled No refund requests shall be entertained after the expiry of this 2-hour window. This provision applies only to services that have not commenced delivery."
      },
      {
        "heading": "SUBSCRIPTIONS",
        "content": "Users may cancel subscriptions at any time. However: • Cancellation prevents future billing only • Current billing cycle remains non-refundable Free trials convert automatically to paid subscriptions unless cancelled before expiry. MARKETPLACE PRODUCTS (PHYSICAL ITEMS) Physical products are eligible for replacement only under limited circumstances: • Product is damaged • Product is defective • Incorrect product delivered • Material portion of physical report missing Users must: • Notify within 2 working days of delivery • Provide photographic evidence • Return products in original condition with packaging Printable or customized spiritual products are non-returnable. Refunds or replacements will be processed after verification."
      },
      {
        "heading": "SPIRITUAL & REMEDY OUTCOME DISCLAIMER",
        "content": "Spiritual services and remedies are based on traditional belief systems. No refund shall be granted due to: • Lack of perceived spiritual effectiveness • Emotional dissatisfaction • Differences in belief systems • Unmet life outcome expectations"
      },
      {
        "heading": "REFUND PROCESSING",
        "content": "Approved refunds will: • Be processed within 7 business days • Be issued via original payment method However, actual credit timelines depend on: • Banking institutions • Payment gateway processing Transaction fees, gateway charges, customs duties, or service delivery costs may be deducted."
      },
      {
        "heading": "CHARGEBACK & FRAUD PREVENTION",
        "content": "If a User initiates a chargeback without first contacting support: • Account access may be suspended • Future transactions may be restricted Fraudulent refund claims may result in legal action."
      },
      {
        "heading": "POLICY ABUSE",
        "content": "We reserve the right to deny refund requests where: • Repeated refund claims are made • Pattern of misuse is detected • Terms of Service are violated"
      },
      {
        "heading": "POLICY UPDATES",
        "content": "We may update this Policy periodically to reflect: • Legal requirements • Service changes • Operational improvements Continued use of the Platform constitutes acceptance of the updated Policy."
      },
      {
        "heading": "CONTACT",
        "content": "SkyHound Studios Email: prateekmalhotra.contentcreator@gmail.com"
      }
    ]
  },
  "cookie-policy": {
    "type": "cookie-policy",
    "title": "Cookie Policy",
    "effective_date": "18th February 2026",
    "last_updated": "18th February 2026",
    "company": "SkyHound Studios",
    "sections": [
      {
        "heading": "COOKIE POLICY",
        "content": "Effective Date: 18 February 2026 Last Updated: 18 February 2026 This Cookie Policy explains how SkyHound Studios (\"Company\", \"we\", \"us\", \"our\") uses cookies and similar tracking technologies when you access or use: • Website: www.everydayhoroscope.in • Mobile Application: Celestial AI • Any related services, digital platforms, AI systems, or communication interfaces (collectively, the \"Services\") This Policy should be read together with our Privacy Policy and Terms of Service. By using the Services, you consent to the use of cookies as described herein, subject to your ability to manage or withdraw consent through available controls."
      },
      {
        "heading": "WHAT ARE COOKIES",
        "content": "Cookies are small text files stored on your device when you access digital services. They enable platforms to recognize devices, remember preferences, and support functionality. In addition to cookies, we may use similar technologies such as: • Local storage • Pixel tags or tracking pixels • Software development kit (SDK) tracking tools • Device identifiers • Server-side tracking mechanisms Cookies may be: • Session cookies, which expire when you close your session • Persistent cookies, which remain for a defined duration"
      },
      {
        "heading": "PURPOSES FOR USING COOKIES",
        "content": "We use cookies and related technologies to: • Enable core platform functionality and secure authentication • Deliver personalized astrological, spiritual, and behavioral insights • Remember user preferences and experience settings • Support AI-driven personalization and recommendation systems • Improve performance, reliability, and feature effectiveness • Detect and prevent fraud, misuse, or security threats • Measure effectiveness of marketing or referral campaigns • Support analytics, research, and product development • Optimize notification timing and engagement intelligence • Enhance behavioral modeling frameworks These activities are conducted in accordance with our Privacy Policy."
      },
      {
        "heading": "3.1 Strictly Necessary Cookies",
        "content": "These cookies are essential to provide core Services, including: • User authentication and account session management • Platform security and fraud prevention • Payment transaction integrity • System load balancing Without these cookies, certain Services may not function properly."
      },
      {
        "heading": "3.2 Performance and Analytics Cookies",
        "content": "These cookies help us understand how Users interact with the Services, including: • Feature usage patterns • Navigation behavior • Technical performance or errors • Aggregate traffic trends Analytics data is typically processed in aggregated or anonymized form."
      },
      {
        "heading": "3.3 Personalization Cookies",
        "content": "These cookies enable delivery of tailored experiences, including: • Customized astrological insights or spiritual content • Behavioral recommendations and feature personalization • User interface preferences and saved settings They help improve relevance and usability."
      },
      {
        "heading": "3.4 Marketing and Attribution Cookies",
        "content": "These cookies help measure and optimize outreach effectiveness by: • Tracking referral sources • Evaluating campaign performance • Supporting growth and user acquisition strategies Such cookies may be placed by advertising or attribution partners."
      },
      {
        "heading": "3.5 AI and Behavioral Optimization Signals",
        "content": "Certain tracking mechanisms may support: • Machine learning model refinement • Notification timing optimization • Feature recommendation systems • Platform engagement analytics These signals are processed in compliance with applicable data protection laws and internal AI governance standards. THIRD-PARTY COOKIES Trusted service providers may place cookies or tracking technologies for purposes including: • Analytics and performance monitoring • Payment processing • Cloud infrastructure management • Advertising attribution We do not control third-party cookie practices. Users should review the respective policies of such providers."
      },
      {
        "heading": "USER CONTROL AND COOKIE CHOICES",
        "content": "Users may manage cookie preferences through: • Browser configuration settings • Device privacy controls • In-app consent or preference management tools Disabling certain cookies may: • Affect platform functionality • Reduce personalization quality • Limit availability of certain features"
      },
      {
        "heading": "COOKIE RETENTION",
        "content": "Cookie retention periods vary depending on purpose. For example: • Session cookies are deleted at the end of a session • Preference or analytics cookies may persist longer We periodically review retention practices to ensure proportionality and compliance."
      },
      {
        "heading": "CONSENT MANAGEMENT",
        "content": "Where required by applicable law, we will: • Obtain consent before deploying non-essential cookies • Provide mechanisms to withdraw or modify consent Users may update preferences at any time through available controls."
      },
      {
        "heading": "INTERNATIONAL USERS",
        "content": "Users in certain jurisdictions (such as the European Union or United Kingdom) may have enhanced rights related to tracking technologies. We aim to comply with: • GDPR • ePrivacy Directive • Applicable global privacy regulation"
      },
      {
        "heading": "POLICY UPDATES",
        "content": "We may update this Cookie Policy periodically to reflect: • Changes in technology or Services • Legal or regulatory developments • Operational improvements Material changes may be communicated via platform notifications or other reasonable means."
      },
      {
        "heading": "CONTACT",
        "content": "SkyHound Studios Email: prateekmalhotra.contentcreator@gmail.com"
      }
    ]
  }
}
    
    seeded = []
    for policy_type, policy_content in policies_data.items():
        existing = await db.policies.find_one({"type": policy_type})
        if not existing:
            policy_content['created_at'] = datetime.now(timezone.utc).isoformat()
            policy_content['updated_at'] = datetime.now(timezone.utc).isoformat()
            await db.policies.insert_one(policy_content)
            seeded.append(policy_type)
    
    return {"success": True, "seeded": seeded, "message": f"Seeded {len(seeded)} policies"}


# ============== CONTACT FORM ==============

@api_router.post("/contact")
async def submit_contact_form(form: ContactFormRequest):
    """Handle contact form submission"""
    
    # Store in database
    contact_doc = {
        "id": str(uuid.uuid4()),
        "name": form.name,
        "email": form.email,
        "subject": form.subject or "Contact Form Submission",
        "message": form.message,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.contact_messages.insert_one(contact_doc)
    
    # Notify admin
    admin_email = os.environ.get('SMTP_USER', 'prateekmalhotra.contentcreator@gmail.com')
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
    
    # Auto-reply to user
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
    """Admin login endpoint"""
    
    if request.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_admin_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create admin session
    session_token = await create_admin_session(db)
    set_admin_session_cookie(response, session_token)
    
    return AdminLoginResponse(
        success=True,
        token=session_token,
        message="Login successful"
    )

@api_router.post("/admin/logout")
async def admin_logout(request: Request, response: Response):
    """Admin logout endpoint"""
    
    session_token = request.cookies.get("admin_session")
    
    if session_token:
        await db.admin_sessions.delete_one({"session_token": session_token})
    
    response.delete_cookie("admin_session", path="/")
    return {"message": "Logged out successfully"}

@api_router.post("/admin/change-password")
async def change_admin_password(request: Request, password_request: ChangePasswordRequest):
    """Change admin password"""
    
    await require_admin(request, db)
    
    # Verify current password
    if not verify_admin_password(password_request.current_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Validate new password
    if len(password_request.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
    
    # Update password in memory
    update_admin_password(password_request.new_password)
    
    # Store in database for persistence across restarts
    new_hash = hash_new_password(password_request.new_password)
    await db.admin_settings.update_one(
        {"key": "admin_password_hash"},
        {"$set": {"value": new_hash}},
        upsert=True
    )
    
    return {"success": True, "message": "Password changed successfully"}

@api_router.get("/admin/verify")
async def verify_admin(request: Request):
    """Verify admin session is valid"""
    
    is_admin = await require_admin(request, db)
    return {"authenticated": is_admin}

@api_router.get("/admin/dashboard")
async def get_dashboard_stats(request: Request):
    """Get dashboard statistics"""
    
    await require_admin(request, db)
    
    # Get today's date range
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_iso = today_start.isoformat()
    
    # Count totals
    total_users = await db.users.count_documents({})
    total_payments = await db.payments.count_documents({})
    total_birth_charts = await db.birth_chart_reports.count_documents({})
    total_kundali_milans = await db.kundali_milan_reports.count_documents({})
    active_subscriptions = await db.subscriptions.count_documents({"status": "active"})
    
    # Calculate total revenue from completed payments
    revenue_pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    revenue_result = await db.payments.aggregate(revenue_pipeline).to_list(1)
    total_revenue = revenue_result[0]['total'] if revenue_result else 0
    
    # Today's counts
    users_today = await db.users.count_documents({
        "created_at": {"$gte": today_iso}
    })
    payments_today = await db.payments.count_documents({
        "created_at": {"$gte": today_iso}
    })
    
    return DashboardStats(
        total_users=total_users,
        total_payments=total_payments,
        total_revenue=total_revenue,
        total_birth_charts=total_birth_charts,
        total_kundali_milans=total_kundali_milans,
        active_subscriptions=active_subscriptions,
        users_today=users_today,
        payments_today=payments_today
    )

@api_router.get("/admin/users")
async def get_all_users(request: Request, skip: int = 0, limit: int = 50):
    """Get all users with pagination"""
    
    await require_admin(request, db)
    
    users = await db.users.find(
        {},
        {"_id": 0, "password_hash": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.users.count_documents({})
    
    user_list = []
    for user in users:
        created_at = user.get('created_at', '')
        if hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        
        user_list.append(UserListItem(
            user_id=user.get('user_id', ''),
            email=user.get('email', ''),
            name=user.get('name', ''),
            picture=user.get('picture'),
            google_id=user.get('google_id'),
            created_at=str(created_at),
            has_password=bool(user.get('password_hash')),
            is_restricted=bool(user.get('is_restricted', False)),
            is_suspended=bool(user.get('is_suspended', False)),
            suspended_until=str(user['suspended_until']) if user.get('suspended_until') else None,
            locked_until=str(user['locked_until']) if user.get('locked_until') else None,
            failed_attempts=int(user.get('failed_attempts', 0))
        ))
    
    return {
        "users": user_list,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.get("/admin/payments")
async def get_all_payments(request: Request, skip: int = 0, limit: int = 50):
    """Get all payments with pagination"""
    
    await require_admin(request, db)
    
    payments = await db.payments.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.payments.count_documents({})
    
    payment_list = []
    for payment in payments:
        created_at = payment.get('created_at', '')
        if hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        
        payment_list.append(PaymentListItem(
            id=payment.get('id', ''),
            user_email=payment.get('user_email', ''),
            report_type=payment.get('report_type', ''),
            amount=payment.get('amount', 0),
            status=payment.get('status', ''),
            razorpay_order_id=payment.get('razorpay_order_id', ''),
            razorpay_payment_id=payment.get('razorpay_payment_id'),
            created_at=str(created_at)
        ))
    
    return {
        "payments": payment_list,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.get("/admin/reports")
async def get_all_reports(request: Request, skip: int = 0, limit: int = 50):
    """Get all generated reports"""
    
    await require_admin(request, db)
    
    # Get birth chart reports
    birth_charts = await db.birth_chart_reports.find(
        {},
        {"_id": 0}
    ).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    
    # Get kundali milan reports
    kundali_milans = await db.kundali_milan_reports.find(
        {},
        {"_id": 0}
    ).sort("generated_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total_birth_charts = await db.birth_chart_reports.count_documents({})
    total_kundali_milans = await db.kundali_milan_reports.count_documents({})
    
    return {
        "birth_charts": birth_charts,
        "kundali_milans": kundali_milans,
        "total_birth_charts": total_birth_charts,
        "total_kundali_milans": total_kundali_milans
    }

@api_router.delete("/admin/user/{user_id}")
async def delete_user(request: Request, user_id: str):
    """Delete a user (admin only)"""
    await require_admin(request, db)
    result = await db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    await db.user_sessions.delete_many({"user_id": user_id})
    return {"message": "User deleted successfully"}

class UserActionRequest(BaseModel):
    action: str  # restrict, unrestrict, suspend, unsuspend

@api_router.post("/admin/user/{user_id}/action")
async def user_action(request: Request, user_id: str, body: UserActionRequest):
    """Restrict, suspend, or unsuspend a user (admin only)"""
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
        # Notify user
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
    """Get all contact form messages (admin only)"""
    await require_admin(request, db)
    messages = await db.contact_messages.find(
        {}, {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.contact_messages.count_documents({})
    return {"messages": messages, "total": total}

# ============== BLOG ENDPOINTS ==============

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title"""
    import re
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    # Ensure no spaces remain (safety net)
    slug = slug.replace(' ', '-')
    return slug if slug else 'post'

# Admin Blog Management
@api_router.post("/admin/blog")
async def create_blog_post(request: Request, post: BlogPostCreate):
    """Create a new blog post (admin only)"""
    await require_admin(request, db)
    
    # Generate slug if not provided
    slug = post.slug if post.slug else generate_slug(post.title)
    
    # Check for duplicate slug
    existing = await db.blog_posts.find_one({"slug": slug})
    if existing:
        slug = f"{slug}-{str(uuid.uuid4())[:8]}"
    
    blog_post = BlogPost(
        title=post.title,
        slug=slug,
        excerpt=post.excerpt,
        content=post.content,
        author=post.author,
        category=post.category,
        tags=post.tags,
        featured_image=post.featured_image,
        video_url=post.video_url,
        published=post.published
    )
    
    doc = blog_post.model_dump(mode='json')
    
    await db.blog_posts.insert_one(doc)
    
    return {"success": True, "post": doc}

@api_router.get("/admin/blog")
async def get_all_blog_posts_admin(request: Request, skip: int = 0, limit: int = 50):
    """Get all blog posts for admin (including unpublished)"""
    await require_admin(request, db)
    
    posts = await db.blog_posts.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.blog_posts.count_documents({})
    
    return {
        "posts": posts,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.put("/admin/blog/{post_id}")
async def update_blog_post(request: Request, post_id: str, post: BlogPostUpdate):
    """Update a blog post (admin only)"""
    await require_admin(request, db)
    
    update_data = {k: v for k, v in post.model_dump(mode='json').items() if v is not None}
    
    # If title changed and no slug provided, regenerate slug
    if 'title' in update_data and 'slug' not in update_data:
        update_data['slug'] = generate_slug(update_data['title'])
    
    result = await db.blog_posts.update_one(
        {"id": post_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    return {"success": True, "message": "Post updated"}

@api_router.delete("/admin/blog/{post_id}")
async def delete_blog_post(request: Request, post_id: str):
    """Delete a blog post (admin only)"""
    await require_admin(request, db)
    
    result = await db.blog_posts.delete_one({"id": post_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    return {"success": True, "message": "Post deleted"}

# Public Blog Endpoints
@api_router.get("/blog")
async def get_published_blog_posts(skip: int = 0, limit: int = 10, category: str = None):
    """Get published blog posts (public)"""
    query = {"published": True}
    if category:
        query["category"] = category
    
    posts = await db.blog_posts.find(
        query,
        {"_id": 0, "content": 0}  # Exclude full content for listing
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.blog_posts.count_documents(query)
    
    return {
        "posts": posts,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.get("/blog/{slug}")
async def get_blog_post_by_slug(slug: str):
    """Get a single blog post by slug (public)"""
    post = await db.blog_posts.find_one(
        {"slug": slug, "published": True},
        {"_id": 0}
    )
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Increment view count
    await db.blog_posts.update_one(
        {"slug": slug},
        {"$inc": {"views": 1}}
    )
    
    return post

@api_router.get("/blog/categories/list")
async def get_blog_categories():
    """Get all unique blog categories"""
    categories = await db.blog_posts.distinct("category", {"published": True})
    return {"categories": categories}

# ============== END BLOG ENDPOINTS ==============

# ============== END ADMIN ENDPOINTS ==============

# ============== USER ACCOUNT ENDPOINTS ==============

class UpdateProfileRequest(BaseModel):
    name: str

class ChangeUserPasswordRequest(BaseModel):
    current_password: str
    new_password: str

@api_router.put("/auth/profile")
async def update_profile(request: Request, body: UpdateProfileRequest):
    """Update authenticated user's display name"""
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    name = body.name.strip()
    if not name or len(name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")

    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": {"name": name}}
    )
    return {"message": "Profile updated successfully", "name": name}


@api_router.put("/auth/change-password")
async def change_user_password(request: Request, body: ChangeUserPasswordRequest):
    """Change password for email/password users (not OAuth)"""
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
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": {"password_hash": new_hash}}
    )
    return {"message": "Password changed successfully"}


@api_router.get("/auth/my-payments")
async def get_my_payments(request: Request):
    """Get payment history for authenticated user"""
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payments = await db.payments.find(
        {"user_email": user.email},
        {"_id": 0}
    ).sort("created_at", -1).limit(50).to_list(50)

    result = []
    for p in payments:
        created_at = p.get("created_at", "")
        if hasattr(created_at, "isoformat"):
            created_at = created_at.isoformat()
        result.append({
            "id": p.get("id", ""),
            "report_type": p.get("report_type", ""),
            "amount": p.get("amount", 0),
            "status": p.get("status", ""),
            "created_at": str(created_at)
        })

    return {"payments": result}

# ============== END USER ACCOUNT ENDPOINTS ==============

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
                    "sign": sign,
                    "type": horoscope_type,
                    "prediction_date": prediction_date
                })
                if existing:
                    skipped += 1
                    continue
                
                content = await generate_horoscope_with_llm(sign, horoscope_type)
                horoscope = Horoscope(
                    sign=sign,
                    type=horoscope_type,
                    content=content,
                    prediction_date=prediction_date
                )
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
    # Run at midnight IST = 18:30 UTC daily
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(hour=18, minute=30, timezone="UTC"),
        id="daily_horoscope_prefetch",
        replace_existing=True
    )
    # Also run weekly prefetch on Sunday at 18:00 UTC
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(day_of_week="sun", hour=18, minute=0, timezone="UTC"),
        id="weekly_horoscope_prefetch",
        replace_existing=True
    )
    # Also run monthly prefetch on 1st of each month at 17:30 UTC
    scheduler.add_job(
        prefetch_all_horoscopes,
        CronTrigger(day=1, hour=17, minute=30, timezone="UTC"),
        id="monthly_horoscope_prefetch",
        replace_existing=True
    )
    scheduler.start()
    logging.info("Horoscope prefetch scheduler started")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown()
    client.close()
