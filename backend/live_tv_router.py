from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from live_tv_service import ROOT_DIR, build_live_tv_response, load_active_manifest


router = APIRouter(prefix="/api/live-tv", tags=["live-tv"])


def _resolve_doc_path(relative_path: str | None) -> Path | None:
    if not relative_path:
        return None
    return ROOT_DIR / relative_path


def _base_url(request: Request) -> str:
    frontend_url = (
        request.headers.get("x-forwarded-host")
        and f"{request.url.scheme}://{request.headers['x-forwarded-host']}"
    )
    return (frontend_url or str(request.base_url)).rstrip("/")


async def _load_active_record(request: Request) -> dict[str, Any]:
    db = getattr(getattr(request.app, "state", None), "db", None)
    if db is not None:
        record = await db.live_tv_videos.find_one({"is_active": True}, {"_id": 0})
        if record:
            return record

    manifest = load_active_manifest()
    if manifest:
        return manifest

    raise HTTPException(status_code=404, detail="No active Live TV video is configured.")


@router.get("/active")
async def get_active_live_tv(request: Request) -> dict[str, Any]:
    record = await _load_active_record(request)
    return build_live_tv_response(record, base_url=_base_url(request))


@router.get("/video/active")
async def stream_active_live_tv_video(request: Request) -> FileResponse:
    record = await _load_active_record(request)
    video_path = _resolve_doc_path(str(record.get("website_video_path") or ""))
    if video_path is None or not video_path.exists():
        raise HTTPException(status_code=404, detail="Active Live TV video file is missing.")
    return FileResponse(video_path, media_type="video/mp4", filename=video_path.name)


@router.get("/thumbnail/active")
async def get_active_live_tv_thumbnail(request: Request) -> FileResponse:
    record = await _load_active_record(request)
    thumbnail_path = _resolve_doc_path(str(record.get("thumbnail_path") or ""))
    if thumbnail_path is None or not thumbnail_path.exists():
        raise HTTPException(status_code=404, detail="Active Live TV thumbnail is missing.")
    return FileResponse(thumbnail_path, media_type="image/jpeg", filename=thumbnail_path.name)
