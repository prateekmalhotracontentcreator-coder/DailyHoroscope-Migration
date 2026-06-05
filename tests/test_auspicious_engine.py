from __future__ import annotations

import sys
import types
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

_STUBBED_MODULE_NAMES = (
    "backend.panchang_router",
    "backend.vedic_shared_utils",
    "panchang_router",
    "swisseph",
    "vedic_shared_utils",
)
_ORIGINAL_MODULES = {name: sys.modules.get(name) for name in _STUBBED_MODULE_NAMES}

panchang_router_stub = types.ModuleType("panchang_router")
panchang_router_stub.DEFAULT_LOCATIONS = {}
panchang_router_stub.KARANA_NAMES = ["Bava"] * 11
panchang_router_stub.LOCATION_LIST = []
panchang_router_stub.NAKSHATRA_NAMES = ["Ashwini"] * 27
panchang_router_stub.TITHI_NAMES = ["Pratipada"] * 30
panchang_router_stub.YOGA_NAMES = ["Vishkambha"] * 27
panchang_router_stub._day_indexes = lambda *args, **kwargs: ({}, {"astro": None})
panchang_router_stub._day_quality_windows = lambda *args, **kwargs: []
panchang_router_stub._paksha_from_tithi = lambda *args, **kwargs: "Shukla"
sys.modules["panchang_router"] = panchang_router_stub
sys.modules["backend.panchang_router"] = panchang_router_stub

if "swisseph" not in sys.modules:
    sys.modules["swisseph"] = types.ModuleType("swisseph")

vedic_shared_utils_stub = types.ModuleType("vedic_shared_utils")
vedic_shared_utils_stub.build_transit_snapshot = lambda *args, **kwargs: {"planets": {"Mercury": {"retrograde": False}}}
sys.modules["vedic_shared_utils"] = vedic_shared_utils_stub
sys.modules["backend.vedic_shared_utils"] = vedic_shared_utils_stub

import auspicious_engine

for _module_name, _original_module in _ORIGINAL_MODULES.items():
    if _original_module is None:
        sys.modules.pop(_module_name, None)
    else:
        sys.modules[_module_name] = _original_module


def _vedic_result(*, score: int, blocked: bool, reasons: list[str], blockers: list[str]) -> dict:
    return {
        "score": score,
        "is_blocked": blocked,
        "reasons": reasons,
        "blockers": blockers,
        "details": {
            "tithi": 10,
            "tithi_name": "Shukla Dashami",
            "nakshatra": 12,
            "nakshatra_name": "Uttara Phalguni",
            "vara": 6,
            "vara_name": "Friday",
            "yoga": 5,
            "yoga_name": "Shobhana",
            "karana": 1,
            "karana_name": "Bava",
            "abhijit_muhurta": {"start": "12:00", "end": "12:48"},
            "rahu_kalam": {"start": "10:30", "end": "12:00"},
        },
    }


def _chinese_result(*, score: int, blocked: bool, reasons: list[str], blockers: list[str]) -> dict:
    return {
        "score": score,
        "is_blocked": blocked,
        "reasons": reasons,
        "blockers": blockers,
        "details": {
            "day_officer": "Success (Cheng)",
            "day_animal": "Horse",
            "user_animal": "Rat",
            "is_personal_clash": blocked,
            "lunar_mansion": "Room (Fang)",
        },
    }


def test_vedic_mode_ignores_chinese_blockers_and_reasons(monkeypatch) -> None:
    monkeypatch.setattr(
        auspicious_engine,
        "_vedic_score_for_day",
        lambda **kwargs: _vedic_result(
            score=88,
            blocked=False,
            reasons=["Dashami supports the action."],
            blockers=[],
        ),
    )
    monkeypatch.setattr(
        auspicious_engine,
        "_chinese_score_for_day",
        lambda **kwargs: _chinese_result(
            score=10,
            blocked=True,
            reasons=["Success officer supports the action."],
            blockers=["Personal zodiac clash shield blocked this date."],
        ),
    )

    result = auspicious_engine.score_day(
        target_date=date(2026, 6, 5),
        location=object(),
        activity_category="job_start",
        system="vedic",
    )

    assert result["vedic_score"] == 88
    assert result["chinese_score"] == 0
    assert result["unified_score"] == 88
    assert result["is_blocked"] is False
    assert result["blockers"] == []
    assert result["vedic_details"]["tithi_name"] == "Shukla Dashami"
    assert result["chinese_details"] is None
    assert "Dashami supports the action." in result["recommendation"]
    assert "zodiac clash" not in result["recommendation"]


def test_chinese_mode_ignores_vedic_blockers_and_reasons(monkeypatch) -> None:
    monkeypatch.setattr(
        auspicious_engine,
        "_vedic_score_for_day",
        lambda **kwargs: _vedic_result(
            score=15,
            blocked=True,
            reasons=["Dashami supports the action."],
            blockers=["Rikta Tithi is blocked for this category."],
        ),
    )
    monkeypatch.setattr(
        auspicious_engine,
        "_chinese_score_for_day",
        lambda **kwargs: _chinese_result(
            score=90,
            blocked=False,
            reasons=["Success officer supports the action."],
            blockers=[],
        ),
    )

    result = auspicious_engine.score_day(
        target_date=date(2026, 6, 5),
        location=object(),
        activity_category="job_start",
        system="chinese",
    )

    assert result["vedic_score"] == 0
    assert result["chinese_score"] == 90
    assert result["unified_score"] == 90
    assert result["is_blocked"] is False
    assert result["blockers"] == []
    assert result["vedic_details"] is None
    assert result["chinese_details"]["day_officer"] == "Success (Cheng)"
    assert "Success officer supports the action." in result["recommendation"]
    assert "Rikta Tithi" not in result["recommendation"]


def test_top_days_sorts_blocked_days_after_stronger_candidates() -> None:
    ranked = auspicious_engine.top_days(
        [
            {"date": "2026-06-03", "is_blocked": True, "unified_score": 95, "vedic_score": 95},
            {"date": "2026-06-01", "is_blocked": False, "unified_score": 80, "vedic_score": 70},
            {"date": "2026-06-02", "is_blocked": False, "unified_score": 80, "vedic_score": 75},
        ],
        limit=3,
    )

    assert [item["date"] for item in ranked] == ["2026-06-02", "2026-06-01", "2026-06-03"]
