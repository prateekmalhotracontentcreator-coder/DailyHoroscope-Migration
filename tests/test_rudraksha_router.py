from __future__ import annotations

import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

_ORIGINAL_FASTAPI = sys.modules.get("fastapi")
_ORIGINAL_VEDIC = sys.modules.get("vedic_calculator")

fastapi_stub = types.ModuleType("fastapi")


class _HTTPException(Exception):
    def __init__(self, status_code: int, detail: str | None = None):
        super().__init__(detail or "")
        self.status_code = status_code
        self.detail = detail


class _Request:
    app = None


class _APIRouter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get(self, *args, **kwargs):
        return self._decorator

    def post(self, *args, **kwargs):
        return self._decorator

    def _decorator(self, func):
        return func


fastapi_stub.APIRouter = _APIRouter
fastapi_stub.HTTPException = _HTTPException
fastapi_stub.Request = _Request
sys.modules["fastapi"] = fastapi_stub

vedic_stub = types.ModuleType("vedic_calculator")
vedic_stub.SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
vedic_stub.calculate_graha_drishti = lambda positions: {}
vedic_stub.calculate_vedic_chart = lambda *args, **kwargs: {}
sys.modules["vedic_calculator"] = vedic_stub

from rudraksha_router import _build_recommendations  # noqa: E402

if _ORIGINAL_FASTAPI is None:
    sys.modules.pop("fastapi", None)
else:
    sys.modules["fastapi"] = _ORIGINAL_FASTAPI

if _ORIGINAL_VEDIC is None:
    sys.modules.pop("vedic_calculator", None)
else:
    sys.modules["vedic_calculator"] = _ORIGINAL_VEDIC


def _planet(sign: str, house: int, dignity: str = "friendly", degree: float = 10.0, total_rupas: float = 7.0) -> dict:
    return {
        "sign": sign,
        "sign_vedic": sign,
        "degree": degree,
        "house": house,
        "dignity": dignity,
        "shadbala": {
            "total_rupas": total_rupas,
            "is_strong": total_rupas >= 6.0,
        },
    }


def _base_chart() -> dict:
    return {
        "lagna": {"sign": "Aries", "sign_vedic": "Aries", "lord": "Mars"},
        "moon_sign": {"sign": "Taurus", "sign_vedic": "Taurus"},
        "current_dasha": {"planet": ""},
        "houses": {
            6: {"lord": "Mercury"},
            8: {"lord": "Mars"},
            12: {"lord": "Jupiter"},
        },
        "planets": {
            "Sun": _planet("Leo", 1),
            "Moon": _planet("Taurus", 2),
            "Mars": _planet("Aries", 1),
            "Mercury": _planet("Gemini", 3, total_rupas=6.2),
            "Jupiter": _planet("Sagittarius", 9, total_rupas=6.9),
            "Venus": _planet("Libra", 7),
            "Saturn": _planet("Capricorn", 10),
            "Rahu": _planet("Virgo", 6),
            "Ketu": _planet("Pisces", 12),
        },
    }


def test_sun_weakness_prefers_one_mukhi() -> None:
    chart = _base_chart()
    chart["planets"]["Sun"] = _planet("Libra", 6, dignity="debilitated")

    result = _build_recommendations(chart)

    assert result["primary"]["mukhi"] == 1
    assert result["secondary"][0]["mukhi"] == 12


def test_aquarius_lagna_can_surface_eight_mukhi() -> None:
    chart = _base_chart()
    chart["lagna"] = {"sign": "Aquarius", "sign_vedic": "Aquarius", "lord": "Saturn"}
    chart["planets"]["Mercury"] = _planet("Gemini", 3, total_rupas=8.0)
    chart["planets"]["Jupiter"] = _planet("Sagittarius", 9, total_rupas=7.2)
    chart["houses"] = {
        6: {"lord": "Moon"},
        8: {"lord": "Mercury"},
        12: {"lord": "Saturn"},
    }

    result = _build_recommendations(chart)

    assert result["primary"]["mukhi"] == 8


def test_neutral_chart_falls_back_to_five_mukhi() -> None:
    chart = _base_chart()
    chart["houses"] = {
        6: {"lord": "Moon"},
        8: {"lord": "Venus"},
        12: {"lord": "Saturn"},
    }

    result = _build_recommendations(chart)

    assert result["primary"]["mukhi"] == 5
    assert result["universal"]["mukhi"] == 5
