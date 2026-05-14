from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from live_tv_service import (  # noqa: E402
    ACTIVE_MANIFEST_PATH,
    DEFAULT_DESCRIPTION,
    DEFAULT_TAGS,
    DEFAULT_TITLE,
    OUTPUT_ROOT,
    build_live_tv_payload,
    create_looped_video_asset,
    ensure_live_tv_dirs,
    extract_video_frame,
    normalize_video_asset,
    upload_video_to_youtube,
    utc_now_iso,
    write_active_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Temple Live TV video assets.")
    parser.add_argument("--video-path", required=True, help="Path to the Temple-provided source video.")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Video title.")
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION, help="Video description.")
    parser.add_argument(
        "--tags",
        default=",".join(DEFAULT_TAGS),
        help="Comma-separated YouTube tags.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=0,
        help="Optional target duration in seconds for a loop-extended YouTube asset.",
    )
    parser.add_argument("--deity", default="Sai Baba", help="Deity label stored in metadata.")
    parser.add_argument("--arti-type", default="general", help="Arti type stored in metadata.")
    parser.add_argument("--upload", action="store_true", help="Upload the generated asset to YouTube.")
    parser.add_argument("--dry-run", action="store_true", help="Generate assets without writing manifest or MongoDB metadata.")
    parser.add_argument("--privacy-status", default="public", choices=["private", "public", "unlisted"])
    parser.add_argument("--refresh-token", default="", help="Optional explicit YouTube refresh token override.")
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""), help="Optional MongoDB URL.")
    parser.add_argument("--db-name", default=os.environ.get("DB_NAME", ""), help="Optional MongoDB database name.")
    return parser.parse_args()


def parse_tags(raw_tags: str) -> list[str]:
    tags = [part.strip() for part in str(raw_tags or "").split(",") if part.strip()]
    return tags or list(DEFAULT_TAGS)


def pick_output_stem(video_path: Path) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"sai-baba-arti-{stamp}-{video_path.stem.lower().replace(' ', '-')}"


def get_refresh_token(client: MongoClient | None, db_name: str, explicit_token: str) -> str:
    if explicit_token.strip():
        return explicit_token.strip()
    if os.environ.get("YOUTUBE_REFRESH_TOKEN", "").strip():
        return os.environ["YOUTUBE_REFRESH_TOKEN"].strip()
    if client is not None and db_name:
        token_doc = client[db_name].app_settings.find_one({"key": "youtube_refresh_token"}, {"_id": 0, "value": 1})
        if token_doc and token_doc.get("value"):
            return str(token_doc["value"]).strip()
    return ""


def upsert_metadata(client: MongoClient | None, db_name: str, payload: dict, upload_success: bool) -> None:
    if client is None or not db_name:
        return
    db = client[db_name]
    db.live_tv_videos.update_many({"is_active": True}, {"$set": {"is_active": False}})
    db.live_tv_videos.update_one(
        {"video_id": payload["video_id"]},
        {"$set": payload},
        upsert=True,
    )
    if upload_success:
        db.social_post_logs.insert_one(
            {
                "channel": "youtube",
                "success": True,
                "post_id": payload.get("youtube_video_id"),
                "error": None,
                "message_preview": payload.get("title", "")[:100],
                "posted_at": utc_now_iso(),
            }
        )


async def main() -> None:
    args = parse_args()
    source_video_path = Path(args.video_path).expanduser().resolve()
    if not source_video_path.exists():
        raise SystemExit(f"Source video not found: {source_video_path}")

    ensure_live_tv_dirs()
    output_stem = pick_output_stem(source_video_path)
    normalized_path = OUTPUT_ROOT / f"{output_stem}.mp4"
    thumbnail_path = OUTPUT_ROOT / f"{output_stem}.jpg"
    looped_path = OUTPUT_ROOT / f"{output_stem}-looped-{args.duration}s.mp4"
    tags = parse_tags(args.tags)

    normalized = await normalize_video_asset(source_video_path, normalized_path)
    await extract_video_frame(normalized_path, thumbnail_path)

    youtube_upload_path = normalized_path
    looped_metadata = None
    if args.duration and args.duration > normalized["normalized_duration_seconds"]:
        looped_metadata = await create_looped_video_asset(normalized_path, looped_path, args.duration)
        youtube_upload_path = looped_path

    upload_payload = None
    mongo_client = MongoClient(args.mongo_url) if args.mongo_url and args.db_name else None
    try:
        if args.upload:
            refresh_token = get_refresh_token(mongo_client, args.db_name, args.refresh_token)
            if not refresh_token:
                raise SystemExit("YouTube upload requested, but no refresh token was found.")
            upload_payload = await upload_video_to_youtube(
                youtube_upload_path,
                refresh_token=refresh_token,
                title=args.title,
                description=args.description,
                tags=tags,
                privacy_status=args.privacy_status,
            )

        manifest_payload = build_live_tv_payload(
            title=args.title,
            description=args.description,
            deity=args.deity,
            arti_type=args.arti_type,
            normalized_video_path=normalized_path,
            thumbnail_path=thumbnail_path,
            source_video_path=source_video_path,
            tags=tags,
            duration_seconds=normalized["normalized_duration_seconds"],
            youtube_data=upload_payload,
            generated_at=utc_now_iso(),
            uploaded_at=utc_now_iso() if upload_payload else None,
        )

        if not args.dry_run:
            manifest_path = write_active_manifest(manifest_payload)
            upsert_metadata(mongo_client, args.db_name, manifest_payload, upload_success=bool(upload_payload))
        else:
            manifest_path = ACTIVE_MANIFEST_PATH

        result = {
            "source_video_path": str(source_video_path),
            "normalized_video_path": str(normalized_path),
            "thumbnail_path": str(thumbnail_path),
            "looped_video_path": str(youtube_upload_path) if looped_metadata else None,
            "manifest_path": str(manifest_path),
            "normalized_duration_seconds": normalized["normalized_duration_seconds"],
            "youtube_upload_requested": args.upload,
            "youtube_video_id": (upload_payload or {}).get("youtube_video_id"),
            "dry_run": bool(args.dry_run),
        }
        print(json.dumps(result, indent=2))
    finally:
        if mongo_client is not None:
            mongo_client.close()


if __name__ == "__main__":
    asyncio.run(main())
