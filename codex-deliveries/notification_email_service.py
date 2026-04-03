from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any, Callable
from urllib import error, request


RESEND_API_URL = "https://api.resend.com/emails"
DEFAULT_BASE_URL = "https://everydayhoroscope.in"


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _get_nested(context: dict[str, Any], dotted_key: str, default: Any = "") -> Any:
    current: Any = context
    for part in dotted_key.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(part)
        if current is None:
            return default
    return current


def _require_context_keys(context: dict[str, Any], keys: list[str]) -> None:
    missing = [key for key in keys if _get_nested(context, key, None) in (None, "")]
    if missing:
        raise ValueError(f"Missing template context values: {', '.join(missing)}")


def _render_text(template: str, context: dict[str, Any]) -> str:
    rendered = template
    for dotted_key in _all_context_keys(context):
        rendered = rendered.replace("{" + dotted_key + "}", _stringify(_get_nested(context, dotted_key, "")))
    return rendered


def _all_context_keys(context: dict[str, Any], prefix: str = "") -> list[str]:
    keys: list[str] = []
    for key, value in context.items():
        dotted = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.extend(_all_context_keys(value, dotted))
        else:
            keys.append(dotted)
    return keys


def _default_html(title: str, lines: list[str], action_label: str | None, action_url: str | None) -> str:
    paragraphs = "".join(f"<p>{line}</p>" for line in lines if line)
    cta = ""
    if action_label and action_url:
        cta = (
            f'<p><a href="{action_url}" '
            'style="display:inline-block;padding:12px 18px;background:#0f172a;color:#ffffff;'
            'text-decoration:none;border-radius:8px;">'
            f"{action_label}</a></p>"
        )
    return (
        "<html><body style=\"font-family:Arial,sans-serif;line-height:1.5;color:#111827;\">"
        f"<h2>{title}</h2>{paragraphs}{cta}</body></html>"
    )


@dataclass(frozen=True)
class EmailTemplate:
    template_id: str
    required_keys: list[str]
    subject_builder: Callable[[dict[str, Any]], str]
    preview_builder: Callable[[dict[str, Any]], str]
    body_builder: Callable[[dict[str, Any]], list[str]]
    action_label_builder: Callable[[dict[str, Any]], str | None]
    action_url_builder: Callable[[dict[str, Any]], str | None]
    marketing: bool = False


def _base_url(context: dict[str, Any]) -> str:
    return _stringify(_get_nested(context, "links.base_url", DEFAULT_BASE_URL)) or DEFAULT_BASE_URL


def _action_url(context: dict[str, Any], fallback_path: str) -> str:
    action_url = _stringify(_get_nested(context, "links.action_url", ""))
    if action_url:
        return action_url
    return f"{_base_url(context)}{fallback_path}"


EMAIL_TEMPLATES: dict[str, EmailTemplate] = {
    "report_ready": EmailTemplate(
        template_id="report_ready",
        required_keys=["event.report_name"],
        subject_builder=lambda context: f"Your {_get_nested(context, 'event.report_name')} is ready to view",
        preview_builder=lambda context: f"{_get_nested(context, 'event.report_name')} is now available.",
        body_builder=lambda context: [
            f"{_get_nested(context, 'event.report_name')} is ready.",
            "Open your report to see the latest guidance prepared for you.",
        ],
        action_label_builder=lambda context: "View Report",
        action_url_builder=lambda context: _action_url(context, "/reports"),
    ),
    "encounter_window_alert": EmailTemplate(
        template_id="encounter_window_alert",
        required_keys=["event.date"],
        subject_builder=lambda context: f"Your next encounter window opens {_get_nested(context, 'event.date')}",
        preview_builder=lambda context: "A meaningful timing window is now opening.",
        body_builder=lambda context: [
            f"Your next encounter window opens {_get_nested(context, 'event.date')}.",
            "Return to the app to review the guidance around this timing.",
        ],
        action_label_builder=lambda context: "Open Encounter Guidance",
        action_url_builder=lambda context: _action_url(context, "/love"),
    ),
    "love_weather_weekly": EmailTemplate(
        template_id="love_weather_weekly",
        required_keys=[],
        subject_builder=lambda context: "Your 90-day love forecast is in",
        preview_builder=lambda context: "See the emotional weather shaping the weeks ahead.",
        body_builder=lambda context: [
            "Your weekly Love Weather summary is ready.",
            _stringify(_get_nested(context, "content.summary", "See what the next 90 days may be emphasizing in love.")),
        ],
        action_label_builder=lambda context: "View Love Weather",
        action_url_builder=lambda context: _action_url(context, "/love"),
        marketing=True,
    ),
    "daily_panchang_digest": EmailTemplate(
        template_id="daily_panchang_digest",
        required_keys=["content.tithi", "content.nakshatra"],
        subject_builder=lambda context: f"{_get_nested(context, 'content.tithi')} | {_get_nested(context, 'content.nakshatra')}",
        preview_builder=lambda context: "Your daily Panchang digest is ready.",
        body_builder=lambda context: [
            f"Tithi: {_get_nested(context, 'content.tithi')}",
            f"Nakshatra: {_get_nested(context, 'content.nakshatra')}",
            f"Sunrise: {_get_nested(context, 'content.sunrise', 'N/A')}",
            _stringify(_get_nested(context, "content.special_yoga", "")),
        ],
        action_label_builder=lambda context: "Open Panchang",
        action_url_builder=lambda context: _action_url(context, "/panchang"),
    ),
    "date_night_score": EmailTemplate(
        template_id="date_night_score",
        required_keys=["content.score"],
        subject_builder=lambda context: f"Tonight's Love Battery: {_get_nested(context, 'content.score')}%",
        preview_builder=lambda context: "Your daily Date-Night score is ready.",
        body_builder=lambda context: [
            f"Tonight's Love Battery is {_get_nested(context, 'content.score')}%.",
            _stringify(_get_nested(context, "content.summary", "See how tonight's energy may support closeness and timing.")),
        ],
        action_label_builder=lambda context: "Open Love Battery",
        action_url_builder=lambda context: _action_url(context, "/love"),
    ),
    "welcome": EmailTemplate(
        template_id="welcome",
        required_keys=[],
        subject_builder=lambda context: "Welcome to Everyday Horoscope",
        preview_builder=lambda context: "Your account is ready to explore.",
        body_builder=lambda context: [
            "Welcome to Everyday Horoscope.",
            "Your spiritual guidance journey is ready whenever you are.",
        ],
        action_label_builder=lambda context: "Open App",
        action_url_builder=lambda context: _action_url(context, "/"),
    ),
}


def build_email_message(template_id: str, context: dict[str, Any]) -> dict[str, Any]:
    template = EMAIL_TEMPLATES.get(template_id)
    if template is None:
        raise ValueError(f"Unknown email template: {template_id}")
    _require_context_keys(context, template.required_keys)
    subject = template.subject_builder(context)
    preview = template.preview_builder(context)
    body_lines = template.body_builder(context)
    action_label = template.action_label_builder(context)
    action_url = template.action_url_builder(context)
    html = _default_html(subject, [preview, *body_lines], action_label, action_url)
    text_lines = [preview, *body_lines]
    if action_label and action_url:
        text_lines.append(f"{action_label}: {action_url}")
    return {
        "template_id": template_id,
        "subject": subject,
        "preview_text": preview,
        "text": "\n\n".join(line for line in text_lines if line),
        "html": html,
        "action_url": action_url,
        "marketing": template.marketing,
    }


def _post_json(url: str, *, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    with request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8")
    if not raw:
        return {}
    return json.loads(raw)


async def send_transactional_email(
    to: str,
    template_id: str,
    context: dict[str, Any],
    *,
    db=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del db
    del metadata

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    if not api_key or not from_email:
        return {"status": "skipped", "channel": "email", "error": "Missing RESEND_API_KEY or FROM_EMAIL"}

    message = build_email_message(template_id, context)
    payload = {
        "from": from_email,
        "to": [to],
        "subject": message["subject"],
        "html": message["html"],
        "text": message["text"],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response_payload = await asyncio.to_thread(_post_json, RESEND_API_URL, payload=payload, headers=headers)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return {"status": "failed", "channel": "email", "error": detail or str(exc)}
    except Exception as exc:
        return {"status": "failed", "channel": "email", "error": str(exc)}

    return {
        "status": "sent",
        "channel": "email",
        "error": None,
        "provider": "resend",
        "provider_message_id": response_payload.get("id"),
        "template_id": template_id,
        "subject": message["subject"],
    }


async def send_bulk_email(
    audience_filter: list[str] | dict[str, Any],
    template_id: str,
    context: dict[str, Any],
    *,
    db,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del metadata

    if isinstance(audience_filter, list):
        recipients = audience_filter
    else:
        if db is None:
            raise ValueError("db is required when audience_filter is a query")
        collection = getattr(db, "subscribers", None)
        if collection is None:
            raise ValueError("subscribers collection unavailable")
        rows = await collection.find(audience_filter, {"email": 1}).to_list(length=10000)
        recipients = [str(row.get("email", "")).strip() for row in rows if row.get("email")]

    results: list[dict[str, Any]] = []
    for recipient in recipients:
        result = await send_transactional_email(recipient, template_id, context, db=db)
        results.append(result)

    sent = sum(1 for result in results if result["status"] == "sent")
    failed = sum(1 for result in results if result["status"] == "failed")
    skipped = sum(1 for result in results if result["status"] == "skipped")
    return {
        "status": "sent" if sent and not failed else "failed" if failed and not sent else "skipped" if skipped and not sent else "sent",
        "channel": "email",
        "error": None if failed == 0 else f"{failed} bulk email sends failed",
        "sent_count": sent,
        "failed_count": failed,
        "skipped_count": skipped,
    }
