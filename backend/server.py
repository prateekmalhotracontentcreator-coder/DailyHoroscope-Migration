from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Optional
import uuid
from datetime import datetime, timezone, date, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
import stripe
from pdf_generator import generate_birth_chart_pdf, generate_kundali_milan_pdf
import secrets
from auth_utils import (
    User, UserSession, RegisterRequest, LoginRequest, UserResponse,
    hash_password, verify_password, create_session, get_current_user,
    get_or_create_oauth_user, set_session_cookie, exchange_session_id_for_token
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Stripe configuration
stripe.api_key = os.environ.get('STRIPE_API_KEY', 'sk_test_emergent')

# Pricing
PRICING = {
    "birth_chart": 9.99,
    "kundali_milan": 14.99,
    "premium_monthly": 19.99
}

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

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
    stripe_payment_id: str
    status: str  # "pending", "completed", "failed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ShareLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    report_type: str  # "birth_chart" or "kundali_milan"
    report_id: str
    views: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaymentIntentRequest(BaseModel):
    report_type: str  # "birth_chart", "kundali_milan", or "premium_monthly"
    report_id: Optional[str] = None
    user_email: str

# LLM Integration for horoscope generation
async def generate_horoscope_with_llm(sign: str, horoscope_type: str) -> str:
    """Generate horoscope using OpenAI GPT-5.2 via emergentintegrations"""
    
    # System prompts based on astrology principles
    system_prompts = {
        "daily": f"You are a professional astrologer with deep knowledge of Western astrology. Generate a detailed, authentic daily horoscope for {sign} based on astrological principles including planetary movements, house positions, and elemental influences. The horoscope should cover: love & relationships, career & finances, health & wellness, and a lucky element (number, color, or time). Make it personal, insightful, and actionable. Keep it around 120-150 words.",
        "weekly": f"You are a professional astrologer with deep knowledge of Western astrology. Generate a comprehensive weekly horoscope for {sign} based on astrological principles. Cover the major planetary transits this week and their impact on: relationships, career opportunities, personal growth, and challenges to watch for. Provide guidance and advice. Keep it around 180-220 words.",
        "monthly": f"You are a professional astrologer with deep knowledge of Western astrology. Generate an in-depth monthly horoscope for {sign} based on major astrological events. Discuss: key themes for the month, career and financial outlook, relationship dynamics, personal development opportunities, and important dates to remember. Make it comprehensive and empowering. Keep it around 250-300 words."
    }
    
    user_prompts = {
        "daily": f"Generate today's horoscope for {sign}. Make it unique, insightful, and based on real astrological principles.",
        "weekly": f"Generate this week's horoscope for {sign}. Include specific guidance and advice based on current planetary positions.",
        "monthly": f"Generate this month's horoscope for {sign}. Provide a comprehensive outlook covering all major life areas."
    }
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"horoscope_{sign}_{horoscope_type}_{datetime.now().isoformat()}",
            system_message=system_prompts[horoscope_type]
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(text=user_prompts[horoscope_type])
        response = await chat.send_message(user_message)
        return response
        
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
    
    doc = horoscope.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
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
    
    doc = horoscope.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.horoscopes.insert_one(doc)
    
    return horoscope

# Birth Profile Routes
@api_router.post("/profile/birth", response_model=BirthProfile)
async def create_birth_profile(profile: BirthProfileCreate):
    """Create a new birth profile"""
    birth_profile = BirthProfile(**profile.model_dump())
    
    doc = birth_profile.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
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
    """Generate comprehensive birth chart report using AI"""
    
    system_prompt = """You are an expert Vedic astrologer. Generate a birth chart analysis covering:

1. Ascendant & Rising Sign: Personality and life path
2. Sun & Moon Signs: Core identity and emotional nature
3. Key Planetary Positions: Major planets and their influence
4. Important Houses: 1st, 7th, 10th houses
5. Notable Yogas: Key planetary combinations
6. Career & Relationships: Strengths and guidance
7. Remedies: 2-3 practical suggestions

Be concise, insightful, and authentic. Target 600-700 words."""
    
    user_prompt = f"Birth chart for {profile.name}, born {profile.date_of_birth} at {profile.time_of_birth} in {profile.location}."
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"birthchart_{profile.id}_{datetime.now().isoformat()}",
            system_message=system_prompt,
            timeout=90  # Increase timeout to 90 seconds
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        return response
        
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
    
    doc = report.model_dump()
    doc['generated_at'] = doc['generated_at'].isoformat()
    await db.birth_chart_reports.insert_one(doc)
    
    return report

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

# Kundali Milan
async def generate_kundali_milan_with_llm(person1: BirthProfile, person2: BirthProfile) -> tuple:
    """Generate comprehensive Kundali Milan report using AI"""
    
    system_prompt = """You are an expert Vedic astrologer specializing in Kundali Milan (horoscope matching) for marriage compatibility.
Analyze the compatibility between two individuals based on their birth details using authentic Vedic astrology principles.

Provide a comprehensive analysis covering:

1. Overall Compatibility Score: Guna Milan score out of 36 points (Ashtakoot system)

2. Detailed Koota Analysis (All 8 Kootas):
   - Varna (1 point): Spiritual compatibility
   - Vashya (2 points): Mutual attraction and control
   - Tara (3 points): Birth star compatibility and health
   - Yoni (4 points): Sexual compatibility and nature
   - Graha Maitri (5 points): Mental compatibility
   - Gana (6 points): Temperament and behavior
   - Bhakoot (7 points): Love and emotional bonding
   - Nadi (8 points): Health and progeny

3. Manglik Dosha Analysis: Check for Mars affliction in both charts and its impact

4. Planetary Compatibility: How planets in both charts interact

5. Strengths of the Relationship: Positive aspects and natural harmony

6. Challenges & Areas of Growth: Potential conflicts and how to manage them

7. Long-term Prospects: Marriage success, family life, financial compatibility

8. Timing & Recommendations: Best timing for marriage, rituals, and remedies if needed

9. Remedies: If score is low, suggest gemstones, mantras, pujas for improvement

START your response with the compatibility score as a number (e.g., "Compatibility Score: 28/36"), then provide the detailed analysis.
Make it comprehensive, authentic, and helpful. Keep the report around 1000-1200 words."""
    
    user_prompt = f"Generate a detailed Kundali Milan compatibility analysis between {person1.name} (born {person1.date_of_birth} at {person1.time_of_birth} in {person1.location}) and {person2.name} (born {person2.date_of_birth} at {person2.time_of_birth} in {person2.location}) for marriage compatibility."
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"kundali_milan_{person1.id}_{person2.id}_{datetime.now().isoformat()}",
            system_message=system_prompt
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        import re
        score_match = re.search(r'(\d+)\s*/\s*36', response)
        compatibility_score = int(score_match.group(1)) if score_match else 24
        
        return compatibility_score, response
        
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
    
    doc = report.model_dump()
    doc['generated_at'] = doc['generated_at'].isoformat()
    await db.kundali_milan_reports.insert_one(doc)
    
    return report

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
        if subscription.get('expires_at'):
            expires_at = subscription['expires_at']
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            if expires_at > datetime.now(timezone.utc):
                return True
    
    # Check one-time payment for specific report
    payment = await db.payments.find_one({
        "user_email": user_email,
        "report_type": report_type,
        "report_id": report_id,
        "status": "completed"
    })
    
    return payment is not None

# Payment Endpoints
@api_router.post("/payment/create-intent")
async def create_payment_intent(request: PaymentIntentRequest):
    """Create Stripe payment intent for premium features"""
    
    try:
        amount_cents = int(PRICING[request.report_type] * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            metadata={
                "report_type": request.report_type,
                "report_id": request.report_id or "",
                "user_email": request.user_email
            }
        )
        
        return {
            "client_secret": intent.client_secret,
            "amount": PRICING[request.report_type]
        }
    except Exception as e:
        logging.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment processing error")

@api_router.post("/payment/confirm")
async def confirm_payment(payment_intent_id: str, user_email: str, report_type: str, report_id: str):
    """Confirm payment and grant access"""
    
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == "succeeded":
            # Record payment
            payment = Payment(
                user_email=user_email,
                report_type=report_type,
                report_id=report_id,
                amount=intent.amount / 100,
                stripe_payment_id=payment_intent_id,
                status="completed"
            )
            
            doc = payment.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            await db.payments.insert_one(doc)
            
            # If monthly subscription, create subscription record
            if report_type == "premium_monthly":
                subscription = UserSubscription(
                    user_email=user_email,
                    subscription_type="premium_monthly",
                    status="active",
                    stripe_subscription_id=payment_intent_id,
                    expires_at=datetime.now(timezone.utc) + timedelta(days=30)
                )
                
                sub_doc = subscription.model_dump()
                sub_doc['created_at'] = sub_doc['created_at'].isoformat()
                sub_doc['expires_at'] = sub_doc['expires_at'].isoformat()
                await db.subscriptions.insert_one(sub_doc)
            
            return {"status": "success", "message": "Payment confirmed"}
        else:
            return {"status": "pending", "message": "Payment pending"}
            
    except Exception as e:
        logging.error(f"Payment confirmation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment confirmation failed")

@api_router.get("/premium/check")
async def check_premium(user_email: str, report_type: str, report_id: str):
    """Check if user has premium access"""
    has_access = await check_premium_access(user_email, report_type, report_id)
    return {"has_premium_access": has_access}

# PDF Generation Endpoints
@api_router.get("/birthchart/{profile_id}/pdf")
async def download_birth_chart_pdf(profile_id: str, user_email: str):
    """Generate and download Birth Chart PDF (Premium)"""
    
    # Check premium access
    has_access = await check_premium_access(user_email, "birth_chart", profile_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="Premium access required")
    
    # Get profile and report
    profile = await db.birth_profiles.find_one({"id": profile_id}, {"_id": 0})
    report = await db.birth_chart_reports.find_one({"profile_id": profile_id}, {"_id": 0})
    
    if not profile or not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Generate PDF
    pdf_buffer = generate_birth_chart_pdf(profile, report['report_content'])
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=birth_chart_{profile['name'].replace(' ', '_')}.pdf"}
    )

@api_router.get("/kundali-milan/{report_id}/pdf")
async def download_kundali_milan_pdf(report_id: str, user_email: str):
    """Generate and download Kundali Milan PDF (Premium)"""
    
    # Check premium access
    has_access = await check_premium_access(user_email, "kundali_milan", report_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="Premium access required")
    
    # Get report
    report = await db.kundali_milan_reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Get both profiles
    person1 = await db.birth_profiles.find_one({"id": report['person1_id']}, {"_id": 0})
    person2 = await db.birth_profiles.find_one({"id": report['person2_id']}, {"_id": 0})
    
    if not person1 or not person2:
        raise HTTPException(status_code=404, detail="Profiles not found")
    
    # Generate PDF
    pdf_buffer = generate_kundali_milan_pdf(
        person1, 
        person2, 
        report['compatibility_score'], 
        report['detailed_analysis']
    )
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=kundali_milan_{person1['name']}_{person2['name']}.pdf"}
    )

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
    
    doc = share_link.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
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
    
    doc = user.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.users.insert_one(doc)
    
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
    """Login with email/password"""
    
    user_doc = await db.users.find_one({"email": request.email}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user_doc.get('password_hash'):
        raise HTTPException(status_code=401, detail="Please login with Google")
    
    if not verify_password(request.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create session
    session_token = await create_session(db, user_doc['user_id'])
    set_session_cookie(response, session_token)
    
    return UserResponse(
        user_id=user_doc['user_id'],
        email=user_doc['email'],
        name=user_doc['name'],
        picture=user_doc.get('picture')
    )

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

@api_router.post("/auth/oauth/callback")
async def oauth_callback(session_id: str, response: Response):
    """Handle Emergent Google OAuth callback"""
    
    # REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    
    try:
        # Exchange session_id for user data
        user_data = await exchange_session_id_for_token(session_id)
        
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

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
