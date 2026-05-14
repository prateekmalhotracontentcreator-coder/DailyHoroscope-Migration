from __future__ import annotations

import asyncio
import io
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from google.oauth2.credentials import Credentials as GoogleCredentials
    from google.auth.transport.requests import Request as GoogleRequest
    from googleapiclient.discovery import build as google_build
    from googleapiclient.http import MediaIoBaseUpload

    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False


ROOT_DIR = Path(__file__).resolve().parent
LIVE_TV_ROOT = ROOT_DIR / "assets" / "live_tv"
SAI_BABA_ROOT = LIVE_TV_ROOT / "sai_baba"
OUTPUT_ROOT = LIVE_TV_ROOT / "output"
ACTIVE_MANIFEST_PATH = OUTPUT_ROOT / "active_live_tv.json"

DEFAULT_TITLE = "LIVE Sai Baba Arti | Om Sai Ram | EverydayHoroscope"
DEFAULT_DESCRIPTION = (
    "Watch Sai Baba Arti live on EverydayHoroscope. Experience continuous Om Sai Ram "
    "darshan at https://www.everydayhoroscope.in/live-sai-baba-arti"
)
DEFAULT_TAGS = ["Sai Baba", "Aarti", "Live", "Om Sai Ram", "EverydayHoroscope"]
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def ensure_live_tv_dirs() -> None:
    SAI_BABA_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in str(value or "").strip())
    collapsed = "-".join(part for part in cleaned.split("-") if part)
    return collapsed or "live-tv"


def resolve_public_base_url() -> str:
    frontend_url = os.environ.get("REACT_APP_FRONTEND_URL", "").strip()
    if frontend_url:
        return frontend_url.rstrip("/")
    return "https://www.everydayhoroscope.in"


def _safe_relpath(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT_DIR.resolve()))
    except ValueError:
        return str(resolved)


def _coerce_datetime(value: Any) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    return utc_now_iso()


def ffprobe_duration_seconds(video_path: Path) -> float:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return max(float(proc.stdout.strip() or "0"), 0.0)


async def extract_video_frame(video_path: Path, output_path: Path, timestamp_seconds: int = 1) -> None:
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-ss",
        str(max(timestamp_seconds, 0)),
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg thumbnail extraction failed: {stderr.decode()[-600:]}")


async def normalize_video_asset(source_path: Path, output_path: Path) -> dict[str, Any]:
    ensure_live_tv_dirs()
    source_duration = ffprobe_duration_seconds(source_path)
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-i",
        str(source_path),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-vf",
        "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        str(output_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg normalize failed: {stderr.decode()[-800:]}")

    duration_seconds = ffprobe_duration_seconds(output_path)
    return {
        "source_duration_seconds": round(source_duration, 2),
        "normalized_duration_seconds": round(duration_seconds, 2),
        "output_path": str(output_path),
    }


async def create_looped_video_asset(source_path: Path, output_path: Path, duration_seconds: int) -> dict[str, Any]:
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",
        "-i",
        str(source_path),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-t",
        str(int(duration_seconds)),
        str(output_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg looping failed: {stderr.decode()[-800:]}")

    rendered_duration = ffprobe_duration_seconds(output_path)
    return {
        "duration_seconds": round(rendered_duration, 2),
        "output_path": str(output_path),
    }


def _build_youtube_service(refresh_token: str, client_id: str, client_secret: str):
    creds = GoogleCredentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=YOUTUBE_SCOPES,
    )
    creds.refresh(GoogleRequest())
    return google_build("youtube", "v3", credentials=creds)


async def get_youtube_service(refresh_token: str):
    if not GOOGLE_LIBS_AVAILABLE:
        raise RuntimeError("Google API libraries are not installed.")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise RuntimeError("YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET must be configured.")
    if not refresh_token:
        raise RuntimeError("A YouTube refresh token is required.")

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: _build_youtube_service(refresh_token, client_id, client_secret),
    )


async def upload_video_to_youtube(
    video_path: Path,
    *,
    refresh_token: str,
    title: str,
    description: str,
    tags: list[str] | None = None,
    privacy_status: str = "public",
) -> dict[str, str]:
    service = await get_youtube_service(refresh_token)
    with video_path.open("rb") as fh:
        video_bytes = fh.read()

    body = {
        "snippet": {
            "title": (title or DEFAULT_TITLE)[:100],
            "description": description or DEFAULT_DESCRIPTION,
            "tags": tags or DEFAULT_TAGS,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
            "madeForKids": False,
        },
    }

    def _upload() -> dict[str, Any]:
        media = MediaIoBaseUpload(
            io.BytesIO(video_bytes),
            mimetype="video/mp4",
            resumable=True,
            chunksize=5 * 1024 * 1024,
        )
        request = service.videos().insert(part="snippet,status", body=body, media_body=media)
        response = None
        while response is None:
            _, response = request.next_chunk()
        return response

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, _upload)
    video_id = str(response.get("id") or "").strip()
    if not video_id:
        raise RuntimeError("YouTube upload completed without returning a video ID.")

    return {
        "youtube_video_id": video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
        "youtube_embed_url": f"https://www.youtube.com/embed/{video_id}",
    }


def write_active_manifest(payload: dict[str, Any]) -> Path:
    ensure_live_tv_dirs()
    ACTIVE_MANIFEST_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return ACTIVE_MANIFEST_PATH


def load_active_manifest() -> dict[str, Any] | None:
    if not ACTIVE_MANIFEST_PATH.exists():
        return None
    try:
        return json.loads(ACTIVE_MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def build_live_tv_payload(
    *,
    title: str,
    description: str,
    deity: str,
    arti_type: str,
    normalized_video_path: Path,
    thumbnail_path: Path,
    source_video_path: Path,
    tags: list[str] | None = None,
    duration_seconds: float | int | None = None,
    youtube_data: dict[str, str] | None = None,
    generated_at: str | None = None,
    uploaded_at: str | None = None,
    video_id: str | None = None,
) -> dict[str, Any]:
    timestamp = generated_at or utc_now_iso()
    payload = {
        "video_id": video_id or slugify(f"{title}-{timestamp}"),
        "title": title,
        "description": description,
        "deity": deity,
        "arti_type": arti_type,
        "is_active": True,
        "display_order": 1,
        "duration_seconds": round(float(duration_seconds or 0), 2),
        "tags": tags or DEFAULT_TAGS,
        "generated_at": timestamp,
        "uploaded_at": uploaded_at,
        "source_video_path": _safe_relpath(source_video_path),
        "website_video_path": _safe_relpath(normalized_video_path),
        "thumbnail_path": _safe_relpath(thumbnail_path),
        "youtube_video_id": None,
        "youtube_url": None,
        "youtube_embed_url": None,
    }
    if youtube_data:
        payload.update(
            {
                "youtube_video_id": youtube_data.get("youtube_video_id"),
                "youtube_url": youtube_data.get("youtube_url"),
                "youtube_embed_url": youtube_data.get("youtube_embed_url"),
            }
        )
    return payload


def build_live_tv_response(metadata: dict[str, Any], base_url: str | None = None) -> dict[str, Any]:
    public_base = (base_url or resolve_public_base_url()).rstrip("/")
    response = dict(metadata)
    response["generated_at"] = _coerce_datetime(response.get("generated_at"))
    if response.get("uploaded_at"):
        response["uploaded_at"] = _coerce_datetime(response.get("uploaded_at"))
    response["website_video_url"] = f"{public_base}/api/live-tv/video/active"
    response["thumbnail_url"] = f"{public_base}/api/live-tv/thumbnail/active"
    return response
