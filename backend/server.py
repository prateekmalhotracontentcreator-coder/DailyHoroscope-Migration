from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Optional
import uuid
from datetime import datetime, timezone, date
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

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
        # Initialize LLM chat
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"horoscope_{sign}_{horoscope_type}_{datetime.now().isoformat()}",
            system_message=system_prompts[horoscope_type]
        ).with_model("openai", "gpt-5.2")
        
        # Create user message
        user_message = UserMessage(text=user_prompts[horoscope_type])
        
        # Get response
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
        # Convert ISO string timestamp back to datetime
        if isinstance(existing['created_at'], str):
            existing['created_at'] = datetime.fromisoformat(existing['created_at'])
        return Horoscope(**existing)
    
    # Generate new horoscope using LLM
    content = await generate_horoscope_with_llm(request.sign, request.type)
    
    # Create horoscope object
    horoscope = Horoscope(
        sign=request.sign,
        type=request.type,
        content=content,
        prediction_date=today
    )
    
    # Store in database
    doc = horoscope.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.horoscopes.insert_one(doc)
    
    return horoscope

@api_router.get("/horoscope/{sign}/{type}", response_model=Horoscope)
async def get_horoscope(sign: str, type: HoroscopeType):
    """Get horoscope for a specific sign and type (returns today's/current period's horoscope)"""
    
    # Validate sign
    valid_signs = [s["id"] for s in ZODIAC_SIGNS]
    if sign not in valid_signs:
        raise HTTPException(status_code=400, detail="Invalid zodiac sign")
    
    today = date.today().isoformat()
    
    # Try to get existing horoscope
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
    
    # If not found, generate new one
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
    
    system_prompt = f\"\"\"You are an expert Vedic astrologer with deep knowledge of Jyotish (Vedic Astrology). 
    Generate a comprehensive, authentic birth chart analysis based on the following birth details:
    
    Name: {profile.name}
    Date of Birth: {profile.date_of_birth}
    Time of Birth: {profile.time_of_birth}
    Place of Birth: {profile.location}
    
    Provide a detailed analysis covering:
    
    1. **Ascendant (Lagna) & Rising Sign**: Detailed interpretation of personality and life path
    2. **Sun Sign (Rashi)**: Core identity and soul purpose
    3. **Moon Sign (Chandra Rashi)**: Emotional nature and mind
    4. **Planetary Positions**: Analysis of all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) in their respective houses and signs
    5. **House Analysis**: Interpretation of key houses (1st, 4th, 7th, 10th, 5th, 9th) and their significance
    6. **Yogas**: Important planetary combinations and their effects
    7. **Dasha Periods**: Current and upcoming major planetary periods and their predictions
    8. **Career & Finance**: Strengths, suitable professions, wealth indicators
    9. **Relationships & Marriage**: Compatibility factors, timing, relationship patterns
    10. **Health**: Potential health concerns based on planetary positions
    11. **Remedies**: Gemstones, mantras, and spiritual practices for balance
    12. **Life Predictions**: Key life events and timing (next 1-2 years)
    
    Make it personal, insightful, and empowering. Use authentic Vedic astrology principles.
    Keep the report comprehensive but readable (800-1000 words).\"\"\"
    
    user_prompt = f\"\"\"Generate a detailed Vedic birth chart analysis for {profile.name} born on {profile.date_of_birth} at {profile.time_of_birth} in {profile.location}.\"\"\"
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f\"birthchart_{profile.id}_{datetime.now().isoformat()}\",
            system_message=system_prompt
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
    
    # Get birth profile
    profile = await db.birth_profiles.find_one({"id": request.profile_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    
    if isinstance(profile['created_at'], str):
        profile['created_at'] = datetime.fromisoformat(profile['created_at'])
    
    birth_profile = BirthProfile(**profile)
    
    # Check if report already exists
    existing = await db.birth_chart_reports.find_one(
        {"profile_id": request.profile_id},
        {"_id": 0}
    )
    
    if existing:
        if isinstance(existing['generated_at'], str):
            existing['generated_at'] = datetime.fromisoformat(existing['generated_at'])
        return BirthChartReport(**existing)
    
    # Generate new report
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

# Kundali Milan (Compatibility Matching)
async def generate_kundali_milan_with_llm(person1: BirthProfile, person2: BirthProfile) -> tuple[int, str]:
    """Generate comprehensive Kundali Milan report using AI"""
    
    system_prompt = f\"\"\"You are an expert Vedic astrologer specializing in Kundali Milan (horoscope matching) for marriage compatibility.
    Analyze the compatibility between two individuals based on their birth details using authentic Vedic astrology principles.
    
    Person 1: {person1.name}
    Date of Birth: {person1.date_of_birth}
    Time of Birth: {person1.time_of_birth}
    Place of Birth: {person1.location}
    
    Person 2: {person2.name}
    Date of Birth: {person2.date_of_birth}
    Time of Birth: {person2.time_of_birth}
    Place of Birth: {person2.location}
    
    Provide a comprehensive analysis covering:
    
    1. **Overall Compatibility Score**: Guna Milan score out of 36 points (Ashtakoot system)
    
    2. **Detailed Koota Analysis** (All 8 Kootas):
       - Varna (1 point): Spiritual compatibility
       - Vashya (2 points): Mutual attraction and control
       - Tara (3 points): Birth star compatibility and health
       - Yoni (4 points): Sexual compatibility and nature
       - Graha Maitri (5 points): Mental compatibility
       - Gana (6 points): Temperament and behavior
       - Bhakoot (7 points): Love and emotional bonding
       - Nadi (8 points): Health and progeny
    
    3. **Manglik Dosha Analysis**: Check for Mars affliction in both charts and its impact
    
    4. **Planetary Compatibility**: How planets in both charts interact
    
    5. **Strengths of the Relationship**: Positive aspects and natural harmony
    
    6. **Challenges & Areas of Growth**: Potential conflicts and how to manage them
    
    7. **Long-term Prospects**: Marriage success, family life, financial compatibility
    
    8. **Timing & Recommendations**: Best timing for marriage, rituals, and remedies if needed
    
    9. **Remedies**: If score is low, suggest gemstones, mantras, pujas for improvement
    
    START your response with the compatibility score as a number (e.g., "Compatibility Score: 28/36"), then provide the detailed analysis.
    Make it comprehensive, authentic, and helpful. Keep the report around 1000-1200 words.\"\"\"
    
    user_prompt = f\"\"\"Generate a detailed Kundali Milan compatibility analysis between {person1.name} and {person2.name} for marriage compatibility.\"\"\"
    
    try:
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f\"kundali_milan_{person1.id}_{person2.id}_{datetime.now().isoformat()}\",
            system_message=system_prompt
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        # Extract score from response (look for pattern like "28/36" or "Score: 28")
        import re
        score_match = re.search(r'(\d+)\s*/\s*36', response)
        compatibility_score = int(score_match.group(1)) if score_match else 24  # Default fallback
        
        return compatibility_score, response
        
    except Exception as e:
        logging.error(f"Error generating Kundali Milan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate Kundali Milan: {str(e)}")

@api_router.post("/kundali-milan/generate", response_model=KundaliMilanReport)
async def generate_kundali_milan(request: KundaliMilanRequest):
    """Generate comprehensive Kundali Milan compatibility report"""
    
    # Get both profiles
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
    
    # Check if report already exists
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
    
    # Generate new report
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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()