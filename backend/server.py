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
