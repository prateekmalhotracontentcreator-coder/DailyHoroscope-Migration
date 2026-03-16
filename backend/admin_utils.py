from fastapi import HTTPException, Request, Response
from pydantic import BaseModel, Field, ConfigDict
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
from typing import Optional
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin credentials from environment (set these in .env)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = pwd_context.hash(os.environ.get('ADMIN_PASSWORD', 'CosmicAdmin2024!'))

# Store password hash in memory (can be updated at runtime)
_current_password_hash = ADMIN_PASSWORD_HASH

# Models
class AdminSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    session_token: str = Field(default_factory=lambda: f"admin_{uuid.uuid4().hex}")
    admin_id: str = "admin"
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    token: str
    message: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class DashboardStats(BaseModel):
    total_users: int
    total_payments: int
    total_revenue: float
    total_birth_charts: int
    total_kundali_milans: int
    active_subscriptions: int
    users_today: int
    payments_today: int

class UserListItem(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: str
    has_password: bool
    is_restricted: bool = False
    is_suspended: bool = False
    suspended_until: Optional[str] = None
    locked_until: Optional[str] = None
    failed_attempts: int = 0

class PaymentListItem(BaseModel):
    id: str
    user_email: str
    report_type: str
    amount: float
    status: str
    razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None
    created_at: str

# Helper Functions
def verify_admin_password(password: str) -> bool:
    """Verify admin password"""
    global _current_password_hash
    return pwd_context.verify(password, _current_password_hash)

def update_admin_password(new_password: str):
    """Update admin password hash in memory"""
    global _current_password_hash
    _current_password_hash = pwd_context.hash(new_password)

def hash_new_password(password: str) -> str:
    """Hash a new password"""
    return pwd_context.hash(password)

async def create_admin_session(db: AsyncIOMotorDatabase) -> str:
    """Create a new admin session"""
    session = AdminSession(
        expires_at=datetime.now(timezone.utc) + timedelta(hours=12)  # 12 hour session
    )
    
    doc = session.model_dump(mode='json')
    
    await db.admin_sessions.insert_one(doc)
    return session.session_token

async def get_admin_session(request: Request, db: AsyncIOMotorDatabase) -> bool:
    """Verify admin session is valid"""
    
    # Try to get token from cookie first, then Authorization header
    session_token = request.cookies.get("admin_session")
    
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split("Bearer ")[1]
    
    if not session_token:
        return False
    
    # Find session
    session_doc = await db.admin_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session_doc:
        return False
    
    # Check expiry
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        # Session expired, delete it
        await db.admin_sessions.delete_one({"session_token": session_token})
        return False
    
    return True

async def require_admin(request: Request, db: AsyncIOMotorDatabase):
    """Middleware to require admin authentication"""
    is_admin = await get_admin_session(request, db)
    if not is_admin:
        raise HTTPException(status_code=401, detail="Admin authentication required")
    return True

def set_admin_session_cookie(response: Response, session_token: str):
    """Set secure admin session cookie"""
    response.set_cookie(
        key="admin_session",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=12 * 60 * 60,  # 12 hours
        path="/"
    )
