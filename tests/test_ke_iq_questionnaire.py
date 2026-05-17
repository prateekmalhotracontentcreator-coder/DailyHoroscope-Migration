from __future__ import annotations

import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

_STUBBED_MODULE_NAMES = (
    "pymongo",
    "fastapi",
    "motor",
    "motor.motor_asyncio",
    "auth_utils",
    "admin_utils",
    "knowledge_schema",
    "vedic_calculator",
    "knowledge_engine",
)
_ORIGINAL_MODULES = {name: sys.modules.get(name) for name in _STUBBED_MODULE_NAMES}

pymongo_stub = types.ModuleType("pymongo")
pymongo_stub.ASCENDING = 1
pymongo_stub.DESCENDING = -1


class _IndexModel:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class _MongoClient:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


pymongo_stub.IndexModel = _IndexModel
pymongo_stub.MongoClient = _MongoClient
sys.modules["pymongo"] = pymongo_stub

fastapi_stub = types.ModuleType("fastapi")


class _HTTPException(Exception):
    def __init__(self, status_code: int, detail: str | None = None):
        super().__init__(detail or "")
        self.status_code = status_code
        self.detail = detail


class _Request:
    app = None
    cookies: dict[str, str] = {}
    headers: dict[str, str] = {}


class _APIRouter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get(self, *args, **kwargs):
        return self._decorator

    def post(self, *args, **kwargs):
        return self._decorator

    def put(self, *args, **kwargs):
        return self._decorator

    def patch(self, *args, **kwargs):
        return self._decorator

    def _decorator(self, func):
        return func


def _query(default=None, **kwargs):
    return default


fastapi_stub.APIRouter = _APIRouter
fastapi_stub.HTTPException = _HTTPException
fastapi_stub.Query = _query
fastapi_stub.Request = _Request
sys.modules["fastapi"] = fastapi_stub

motor_stub = types.ModuleType("motor")
motor_asyncio_stub = types.ModuleType("motor.motor_asyncio")


class _AsyncIOMotorDatabase:
    pass


motor_asyncio_stub.AsyncIOMotorDatabase = _AsyncIOMotorDatabase
sys.modules["motor"] = motor_stub
sys.modules["motor.motor_asyncio"] = motor_asyncio_stub

auth_utils_stub = types.ModuleType("auth_utils")


async def _get_current_user(request, db):
    return None


auth_utils_stub.get_current_user = _get_current_user
sys.modules["auth_utils"] = auth_utils_stub

admin_utils_stub = types.ModuleType("admin_utils")


async def _require_admin(request, db):
    return True


admin_utils_stub.require_admin = _require_admin
sys.modules["admin_utils"] = admin_utils_stub

knowledge_schema_stub = types.ModuleType("knowledge_schema")
knowledge_schema_stub.COLLECTION_CASE_STUDIES = "case_studies"
knowledge_schema_stub.COLLECTION_IMPORT_BATCHES = "import_batches"
knowledge_schema_stub.COLLECTION_INTERPRETATION_RULES = "interpretation_rules"
knowledge_schema_stub.COLLECTION_USER_CONTEXT_PROFILE = "user_context_profile"
knowledge_schema_stub.ApprovalStatus = type("ApprovalStatus", (), {})
knowledge_schema_stub.CaseStudyDocument = type("CaseStudyDocument", (), {})
knowledge_schema_stub.EnginePrediction = type("EnginePrediction", (), {})


class _UserContextProfileDocument:
    def __init__(self, **payload):
        self.payload = payload

    def model_dump(self, mode="json", by_alias=True, exclude_none=False):
        return dict(self.payload)


knowledge_schema_stub.UserContextProfileDocument = _UserContextProfileDocument
sys.modules["knowledge_schema"] = knowledge_schema_stub

vedic_calculator_stub = types.ModuleType("vedic_calculator")


def _calculate_vedic_chart(*args, **kwargs):
    return {}


def _calculate_vimshottari_dasha(*args, **kwargs):
    return {}


vedic_calculator_stub.calculate_vedic_chart = _calculate_vedic_chart
vedic_calculator_stub.calculate_vimshottari_dasha = _calculate_vimshottari_dasha
sys.modules["vedic_calculator"] = vedic_calculator_stub

knowledge_engine_stub = types.ModuleType("knowledge_engine")


def _build_arc_angel_questionnaire_state(profile):
    areas_completed: list[str] = []
    if any(profile.get(field) not in (None, "") for field in ("salary_bracket", "family_wealth_tier", "siblings_count")):
        areas_completed.extend(["career", "finances"])
    if any(profile.get(field) not in (None, "") for field in ("current_city", "travel_frequency")):
        areas_completed.extend(["environment", "adventure"])
    if profile.get("relationship_status") not in (None, ""):
        areas_completed.extend(["relationships", "social"])
    parents = profile.get("parents_data") or {}
    father = parents.get("father") or {}
    mother = parents.get("mother") or {}
    if any(father.get(field) not in (None, "") for field in ("dob", "place")) or any(
        mother.get(field) not in (None, "") for field in ("dob", "place")
    ):
        areas_completed.extend(["family", "creativity"])
    return {"areas_completed": areas_completed}


async def _sync_arc_angel_questionnaire_state(db, user_id, context_profile):
    return None


knowledge_engine_stub.build_arc_angel_questionnaire_state = _build_arc_angel_questionnaire_state
knowledge_engine_stub.sync_arc_angel_questionnaire_state = _sync_arc_angel_questionnaire_state
sys.modules["knowledge_engine"] = knowledge_engine_stub

from knowledge_router import _derive_focus_domains, _questionnaire_completed, _recompute_context_profile_scores

for _module_name, _original_module in _ORIGINAL_MODULES.items():
    if _original_module is None:
        sys.modules.pop(_module_name, None)
    else:
        sys.modules[_module_name] = _original_module


def test_questionnaire_profile_completion_requires_core_sections() -> None:
    partial = {
        "salary_bracket": "mid",
        "family_wealth_tier": "mid",
        "siblings_count": 1,
        "current_city": "Delhi",
        "travel_frequency": "sometimes",
        "relationship_status": "",
        "parents_data": {"father": {"dob": "", "place": ""}, "mother": {"dob": "", "place": ""}},
    }
    assert _questionnaire_completed(partial) is False

    complete = {**partial, "relationship_status": "married"}
    assert _questionnaire_completed(complete) is True


def test_focus_domains_follow_completed_sections_priority() -> None:
    profile = {
        "salary_bracket": "high",
        "family_wealth_tier": "mid",
        "siblings_count": 2,
        "current_city": "Mumbai",
        "travel_frequency": "frequently",
        "relationship_status": "relationship",
        "parents_data": {"father": {"dob": "", "place": ""}, "mother": {"dob": "", "place": ""}},
    }
    assert _derive_focus_domains(profile) == ["career", "finances", "learning"]


def test_beta_gamma_scores_move_above_neutral_for_complete_profile() -> None:
    profile = {
        "salary_bracket": "high",
        "family_wealth_tier": "high",
        "siblings_count": 3,
        "current_city": "Bengaluru",
        "travel_frequency": "frequently",
        "relationship_status": "married",
        "parents_data": {
            "father": {"dob": "1960-01-01", "place": "Delhi"},
            "mother": {"dob": "1965-01-01", "place": "Mumbai"},
        },
    }
    beta, gamma = _recompute_context_profile_scores(profile)
    assert beta > 1.0
    assert gamma > 1.0
    assert beta <= 1.22
    assert gamma <= 1.22
