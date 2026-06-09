#!/usr/bin/env python3
from __future__ import annotations

"""Baked-in KP lookup tables for the KE runtime."""

import json
from typing import Any


_T05_RAW = {t05_raw}
_P27_RAW = {p27_raw}


def _normalize_title(value: str | None) -> str:
    return " ".join(part.capitalize() for part in str(value or "").strip().split())


def _normalize_vocation(value: str | None) -> str:
    return " ".join(part.strip() for part in str(value or "").split())


_T05_SOURCE = json.loads(_T05_RAW)
_T05_DATA = list(_T05_SOURCE.get("data") or [])
_P27_DATA = list(json.loads(_P27_RAW))

T05_BY_NUMBER: dict[int, dict[str, Any]] = {{
    int(entry["no"]): entry for entry in _T05_DATA if isinstance(entry, dict) and entry.get("no") is not None
}}

T05_BY_CHAIN: dict[tuple[str, str], list[dict[str, Any]]] = {{}}
for entry in _T05_DATA:
    if not isinstance(entry, dict):
        continue
    key = (_normalize_title(entry.get("nak_lord")), _normalize_title(entry.get("sub_lord")))
    T05_BY_CHAIN.setdefault(key, []).append(entry)

P27_BY_VOCATION: dict[str, dict[str, Any]] = {{
    _normalize_vocation(entry.get("profession")): entry
    for entry in _P27_DATA
    if isinstance(entry, dict) and entry.get("profession")
}}
_P27_BY_VOCATION_LOWER = {{key.lower(): value for key, value in P27_BY_VOCATION.items()}}


def get_sub_entries(star_lord: str, sub_lord: str) -> list[dict[str, Any]]:
    key = (_normalize_title(star_lord), _normalize_title(sub_lord))
    return list(T05_BY_CHAIN.get(key, []))


def get_sub_entry_for_sign(star_lord: str, sub_lord: str, sign: str) -> dict[str, Any] | None:
    normalized_sign = _normalize_title(sign)
    for entry in get_sub_entries(star_lord, sub_lord):
        if _normalize_title(entry.get("sign")) == normalized_sign:
            return entry
    return None


def get_profession_entry(vocation: str) -> dict[str, Any] | None:
    key = _normalize_vocation(vocation).lower()
    return _P27_BY_VOCATION_LOWER.get(key)


__all__ = [
    "T05_BY_NUMBER",
    "T05_BY_CHAIN",
    "P27_BY_VOCATION",
    "get_sub_entries",
    "get_sub_entry_for_sign",
    "get_profession_entry",
]
