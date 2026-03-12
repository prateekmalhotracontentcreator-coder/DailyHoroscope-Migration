from fastapi import HTTPException, Request, Response, Cookie
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import httpx
import os
from typing import Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    user_id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:12]}")
    email: str
    name: str
    password_hash: Optional[str] = None  # None for OAuth users
    picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    session_token: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex}")
    user_id: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None

# Helper Functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)

async def create_session(db: AsyncIOMotorDatabase, user_id: str) -> str:
    """Create a new session for user"""
    session = UserSession(
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    
    doc = session.model_dump(mode='json')
    
    await db.user_sessions.insert_one(doc)
    return session.session_token

async def get_current_user(request: Request, db: AsyncIOMotorDatabase) -> Optional[UserResponse]:
    """Get current authenticated user from session token"""
    
    # Try to get token from cookie first, then Authorization header
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split("Bearer ")[1]
    
    if not session_token:
        return None
    
    # Find session
    session_doc = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session_doc:
        return None
    
    # Check expiry
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        # Session expired, delete it
        await db.user_sessions.delete_one({"session_token": session_token})
        return None
    
    # Get user
    user_doc = await db.users.find_one(
        {"user_id": session_doc["user_id"]},
        {"_id": 0, "password_hash": 0}  # Exclude sensitive data
    )
    
    if not user_doc:
        return None
    
    return UserResponse(**user_doc)

async def get_or_create_oauth_user(db: AsyncIOMotorDatabase, email: str, name: str, picture: str, google_id: str) -> User:
    """Get existing user by email or create new OAuth user"""
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if existing_user:
        # Update OAuth info if needed
        if not existing_user.get('google_id'):
            await db.users.update_one(
                {"email": email},
                {"$set": {"google_id": google_id, "picture": picture}}
            )
        
        if isinstance(existing_user['created_at'], str):
            existing_user['created_at'] = datetime.fromisoformat(existing_user['created_at'])
        
        return User(**existing_user)
    
    # Create new user
    new_user = User(
        email=email,
        name=name,
        picture=picture,
        google_id=google_id,
        password_hash=None  # OAuth user, no password
    )
    
    doc = new_user.model_dump(mode='json')
    
    await db.users.insert_one(doc)
    return new_user

def set_session_cookie(response: Response, session_token: str):
    """Set secure session cookie"""
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,  # 7 days
        path="/"
    )

async def exchange_session_id_for_token(session_id: str) -> dict:
    """Exchange Google OAuth code for user data"""
    import json, base64
    
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://daily-horoscope-migration.vercel.app')
    
    # Exchange authorization code for tokens
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": session_id,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{FRONTEND_URL}/auth/callback",
                "grant_type": "authorization_code",
            }
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to exchange OAuth code")
        
        tokens = token_response.json()
        
        # Get user info from Google
        userinfo_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        
        if userinfo_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to get user info")
        
        user_info = userinfo_response.json()
        return {
            "email": user_info["email"],
            "name": user_info.get("name", user_info["email"]),
            "picture": user_info.get("picture"),
            "id": user_info["id"]
        }
