from __future__ import annotations

import json
import os
from typing import Any


def _vapid_settings() -> tuple[str | None, str | None, str | None]:
    return os.getenv("VAPID_PUBLIC_KEY"), os.getenv("VAPID_PRIVATE_KEY"), os.getenv("VAPID_SUBJECT")


async def send_push(
    subscription_info: dict[str, Any],
    title: str,
    body: str,
    icon: str,
    url: str,
    *,
    db=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del db
    metadata = metadata or {}

    _, vapid_private_key, vapid_subject = _vapid_settings()
    if not vapid_private_key or not vapid_subject:
        return {"status": "skipped", "channel": "push", "error": "VAPID keys not configured"}

    try:
        from pywebpush import WebPushException, webpush
    except ImportError:
        return {"status": "failed", "channel": "push", "error": "pywebpush is not installed"}

    payload = {
        "title": title,
        "body": body,
        "icon": icon,
        "url": url,
        "tag": metadata.get("tag"),
        "data": metadata.get("data", {}),
    }
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=vapid_private_key,
            vapid_claims={"sub": vapid_subject},
        )
    except WebPushException as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        result = {"status": "failed", "channel": "push", "error": str(exc)}
        if status_code in {404, 410}:
            result["subscription_inactive"] = True
        return result
    except Exception as exc:
        return {"status": "failed", "channel": "push", "error": str(exc)}

    return {"status": "sent", "channel": "push", "error": None}


async def send_push_bulk(
    subscriptions: list[dict[str, Any]],
    title: str,
    body: str,
    icon: str,
    url: str,
    *,
    db=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sent = 0
    failed = 0
    skipped = 0
    inactive_endpoints: list[str] = []

    for subscription in subscriptions:
        result = await send_push(
            subscription,
            title,
            body,
            icon,
            url,
            db=db,
            metadata=metadata,
        )
        if result["status"] == "sent":
            sent += 1
        elif result["status"] == "skipped":
            skipped += 1
        else:
            failed += 1
        if result.get("subscription_inactive"):
            endpoint = subscription.get("endpoint")
            if endpoint:
                inactive_endpoints.append(str(endpoint))

    status = "sent" if sent and failed == 0 else "failed" if failed and sent == 0 else "sent"
    return {
        "status": status,
        "channel": "push",
        "error": None if failed == 0 else f"{failed} push sends failed",
        "sent_count": sent,
        "failed_count": failed,
        "skipped_count": skipped,
        "inactive_endpoints": inactive_endpoints,
    }
