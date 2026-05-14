from __future__ import annotations

import asyncio
import json
import os
from typing import Any
from urllib import error, request


def _post_json(url: str, *, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    with request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8")
    if not raw:
        return {}
    return json.loads(raw)


def _credentials() -> tuple[str | None, str | None]:
    return os.getenv("WHATSAPP_PHONE_NUMBER_ID"), os.getenv("WHATSAPP_ACCESS_TOKEN")


async def send_whatsapp_template(
    to_phone: str,
    template_name: str,
    template_params: list[str] | tuple[str, ...],
    *,
    db=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del db
    del metadata

    phone_number_id, access_token = _credentials()
    if not phone_number_id or not access_token:
        return {"status": "skipped", "channel": "whatsapp", "error": "WhatsApp credentials not configured"}

    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": str(value)} for value in template_params],
                }
            ],
        },
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    try:
        response_payload = await asyncio.to_thread(_post_json, url, payload=payload, headers=headers)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return {"status": "failed", "channel": "whatsapp", "error": detail or str(exc)}
    except Exception as exc:
        return {"status": "failed", "channel": "whatsapp", "error": str(exc)}

    messages = response_payload.get("messages") or []
    message_id = messages[0].get("id") if messages else None
    return {
        "status": "sent",
        "channel": "whatsapp",
        "error": None,
        "provider": "meta_cloud_api",
        "provider_message_id": message_id,
        "template_name": template_name,
    }


async def send_whatsapp_text(
    to_phone: str,
    message: str,
    *,
    db=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del db
    del metadata

    phone_number_id, access_token = _credentials()
    if not phone_number_id or not access_token:
        return {"status": "skipped", "channel": "whatsapp", "error": "WhatsApp credentials not configured"}

    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,
        },
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    try:
        response_payload = await asyncio.to_thread(_post_json, url, payload=payload, headers=headers)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return {"status": "failed", "channel": "whatsapp", "error": detail or str(exc)}
    except Exception as exc:
        return {"status": "failed", "channel": "whatsapp", "error": str(exc)}

    messages = response_payload.get("messages") or []
    message_id = messages[0].get("id") if messages else None
    return {
        "status": "sent",
        "channel": "whatsapp",
        "error": None,
        "provider": "meta_cloud_api",
        "provider_message_id": message_id,
    }
