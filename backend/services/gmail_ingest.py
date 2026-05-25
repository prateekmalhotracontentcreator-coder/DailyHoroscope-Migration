import base64
import logging
import os
from typing import Any, Dict, List, Optional


try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest
    from googleapiclient.discovery import build
    GOOGLE_GMAIL_AVAILABLE = True
except ImportError:
    GOOGLE_GMAIL_AVAILABLE = False


GMAIL_TOKEN_URI = "https://oauth2.googleapis.com/token"


def _decode_sender_email(sender_header: str) -> str:
    if "<" in sender_header and ">" in sender_header:
        return sender_header.split("<", 1)[1].split(">", 1)[0].strip().lower()
    return sender_header.strip().lower()


def _header(headers: List[Dict[str, str]], name: str) -> str:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def _extract_parts(parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for part in parts or []:
        found.append(part)
        found.extend(_extract_parts(part.get("parts") or []))
    return found


def _build_credentials(refresh_token: str):
    client_id = os.environ.get("GMAIL_CLIENT_ID", "")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        raise RuntimeError("GMAIL_CLIENT_ID / GMAIL_CLIENT_SECRET not configured")
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri=GMAIL_TOKEN_URI,
        scopes=["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"],
    )
    creds.refresh(GoogleRequest())
    return creds


async def _get_refresh_token(db) -> Optional[str]:
    token_doc = await db.app_settings.find_one({"key": "gmail_refresh_token"})
    return (token_doc or {}).get("value") or os.environ.get("GMAIL_REFRESH_TOKEN", "")


async def _get_service(db):
    if not GOOGLE_GMAIL_AVAILABLE:
        logging.warning("Gmail ingest skipped: Google Gmail libraries not installed")
        return None

    refresh_token = await _get_refresh_token(db)
    if not refresh_token:
        logging.info("Gmail ingest skipped: no Gmail refresh token configured")
        return None

    try:
        creds = _build_credentials(refresh_token)
        return build("gmail", "v1", credentials=creds, cache_discovery=False)
    except Exception as exc:
        logging.warning("Gmail ingest auth failed: %s", exc)
        return None


async def fetch_vendor_emails(db) -> List[Dict[str, Any]]:
    service = await _get_service(db)
    if service is None:
        return []

    try:
        results = service.users().messages().list(
            userId="me",
            q="is:unread has:attachment filename:pdf",
        ).execute()
    except Exception as exc:
        logging.warning("Failed to list vendor emails: %s", exc)
        return []

    emails: List[Dict[str, Any]] = []
    for msg_meta in (results.get("messages") or [])[:20]:
        try:
            msg = service.users().messages().get(userId="me", id=msg_meta["id"]).execute()
            headers = (msg.get("payload") or {}).get("headers") or []
            parts = _extract_parts((msg.get("payload") or {}).get("parts") or [])
            for part in parts:
                filename = part.get("filename", "")
                attachment_id = ((part.get("body") or {}).get("attachmentId"))
                if not filename.lower().endswith(".pdf") or not attachment_id:
                    continue
                attachment = service.users().messages().attachments().get(
                    userId="me",
                    messageId=msg_meta["id"],
                    id=attachment_id,
                ).execute()
                pdf_bytes = base64.urlsafe_b64decode(attachment["data"])
                emails.append({
                    "message_id": msg_meta["id"],
                    "subject": _header(headers, "Subject"),
                    "sender": _header(headers, "From"),
                    "sender_email": _decode_sender_email(_header(headers, "From")),
                    "pdf_bytes": pdf_bytes,
                })
                break
        except Exception as exc:
            logging.warning("Failed to read vendor email %s: %s", msg_meta.get("id"), exc)
    return emails


async def fetch_support_emails(db) -> List[Dict[str, Any]]:
    service = await _get_service(db)
    if service is None:
        return []

    support_email = os.environ.get("SUPPORT_EMAIL", "").strip()
    if not support_email:
        logging.info("Support ticket triage skipped: SUPPORT_EMAIL not configured")
        return []
    query = f'to:{support_email} is:unread'

    try:
        results = service.users().messages().list(userId="me", q=query).execute()
    except Exception as exc:
        logging.warning("Failed to list support emails: %s", exc)
        return []

    emails: List[Dict[str, Any]] = []
    for msg_meta in (results.get("messages") or [])[:30]:
        try:
            msg = service.users().messages().get(userId="me", id=msg_meta["id"]).execute()
            headers = (msg.get("payload") or {}).get("headers") or []
            snippet = msg.get("snippet", "")
            emails.append({
                "message_id": msg_meta["id"],
                "subject": _header(headers, "Subject"),
                "sender": _header(headers, "From"),
                "sender_email": _decode_sender_email(_header(headers, "From")),
                "snippet": snippet,
            })
        except Exception as exc:
            logging.warning("Failed to read support email %s: %s", msg_meta.get("id"), exc)
    return emails
