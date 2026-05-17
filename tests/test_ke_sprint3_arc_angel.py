from __future__ import annotations

import sys
import types
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

if "pymongo" not in sys.modules:
    pymongo_stub = types.ModuleType("pymongo")
    pymongo_stub.ASCENDING = 1
    pymongo_stub.DESCENDING = -1

    class _IndexModel:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    pymongo_stub.IndexModel = _IndexModel
    sys.modules["pymongo"] = pymongo_stub

import knowledge_engine
from knowledge_engine import (
    ARC_ANGEL_DOMAIN_LABELS,
    ARC_ANGEL_DOMAIN_SLUGS,
    arc_angel_profile_is_fresh,
    build_arc_angel_data_completeness,
    build_arc_angel_profile_doc,
    build_domain_rule_map,
    compute_arc_angel_windows,
    compute_dasha_timeline,
    compute_period_quality_now,
    _compute_confidence,
)
from vedic_calculator import build_dasha_timeline


def _active_timeline(antar_planet: str) -> list[dict]:
    today = date.today()
    return [
        {
            "planet": "Moon",
            "start": (today - timedelta(days=5)).isoformat(),
            "end": (today + timedelta(days=365)).isoformat(),
            "antardashas": [
                {
                    "planet": antar_planet,
                    "start": (today - timedelta(days=5)).isoformat(),
                    "end": (today + timedelta(days=365)).isoformat(),
                }
            ],
        }
    ]


def _profile_windows_and_quality() -> tuple[dict[str, dict], dict[str, str]]:
    timeline = build_dasha_timeline("1990-05-15", 123.45)
    domain_rule_map = build_domain_rule_map([])
    windows = compute_arc_angel_windows(timeline, domain_rule_map, horizon_years=10, as_of=date(2026, 5, 17))
    quality = compute_period_quality_now(timeline, domain_rule_map, as_of=date(2026, 5, 17))
    return windows, quality


def test_period_quality_now_returns_all_12_domains() -> None:
    result = compute_period_quality_now(_active_timeline("Jupiter"), build_domain_rule_map([]))
    assert set(result) == set(ARC_ANGEL_DOMAIN_SLUGS)
    assert set(result.values()) <= {"auspicious", "neutral", "inauspicious"}


def test_period_quality_falls_back_to_natural_quality_when_no_approved_rules() -> None:
    result = compute_period_quality_now(_active_timeline("Jupiter"), build_domain_rule_map([]))
    assert set(result.values()) == {"auspicious"}


def test_period_quality_inauspicious_for_saturn_antardasha() -> None:
    result = compute_period_quality_now(_active_timeline("Saturn"), build_domain_rule_map([]))
    assert set(result.values()) == {"inauspicious"}


def test_build_domain_rule_map_tolerates_sprint2_arbitration_fields() -> None:
    matched_rules = [
        {
            "categories": ["career"],
            "life_domain": "career",
            "representation_mode": "tension",
            "tension_blocks": [{"life_domain": "career"}],
            "c_score": 0.62,
        }
    ]
    result = build_domain_rule_map(matched_rules)
    assert "career" in result
    assert len(result["career"]) == 1


def test_arc_angel_windows_covers_all_12_domains() -> None:
    timeline = build_dasha_timeline("1990-05-15", 123.45)
    result = compute_arc_angel_windows(timeline, build_domain_rule_map([]), horizon_years=10, as_of=date(2026, 5, 17))
    assert set(result) == set(ARC_ANGEL_DOMAIN_SLUGS)


def test_arc_angel_windows_no_window_shorter_than_90_days() -> None:
    timeline = build_dasha_timeline("1990-05-15", 123.45)
    result = compute_arc_angel_windows(timeline, build_domain_rule_map([]), horizon_years=10, as_of=date(2026, 5, 17))
    for payload in result.values():
        for key in ("auspicious_periods", "inauspicious_periods"):
            for window in payload[key]:
                start = datetime.strptime(window["start"], "%Y-%m")
                end = datetime.strptime(window["end"], "%Y-%m")
                assert (end.year - start.year) * 12 + (end.month - start.month) >= 2


def test_arc_angel_windows_periods_have_required_keys() -> None:
    timeline = build_dasha_timeline("1990-05-15", 123.45)
    result = compute_arc_angel_windows(timeline, build_domain_rule_map([]), horizon_years=10, as_of=date(2026, 5, 17))
    windows_found = 0
    for payload in result.values():
        for key in ("auspicious_periods", "inauspicious_periods"):
            for window in payload[key]:
                windows_found += 1
                assert set(window) == {"start", "end", "driver"}
                assert len(window["start"]) == 7 and len(window["end"]) == 7
                assert isinstance(window["driver"], str) and window["driver"].strip()
    assert windows_found > 0


def test_arc_angel_windows_sorted_chronologically() -> None:
    timeline = build_dasha_timeline("1990-05-15", 123.45)
    result = compute_arc_angel_windows(timeline, build_domain_rule_map([]), horizon_years=10, as_of=date(2026, 5, 17))
    populated_domains = 0
    for payload in result.values():
        for key in ("auspicious_periods", "inauspicious_periods"):
            starts = [window["start"] for window in payload[key]]
            assert starts == sorted(starts)
            if starts:
                populated_domains += 1
    assert populated_domains >= 4


def test_arc_angel_windows_preserve_ad_granularity_for_long_same_quality_periods() -> None:
    timeline = [
        {
            "planet": "Jupiter",
            "start": "2026-01-01",
            "end": "2027-12-31",
            "antardashas": [
                {"planet": "Moon", "start": "2026-01-01", "end": "2026-04-30"},
                {"planet": "Jupiter", "start": "2026-05-01", "end": "2026-08-31"},
                {"planet": "Venus", "start": "2026-09-01", "end": "2026-12-31"},
                {"planet": "Saturn", "start": "2027-01-01", "end": "2027-04-30"},
            ],
        }
    ]
    result = compute_arc_angel_windows(timeline, build_domain_rule_map([]), horizon_years=2, as_of=date(2026, 1, 1))
    career = result["career"]
    assert len(career["auspicious_periods"]) == 3
    assert [
        period["driver"] for period in career["auspicious_periods"]
    ] == [
        "Moon AD in Jupiter MD -- career auspicious period",
        "Jupiter AD in Jupiter MD -- career auspicious period",
        "Venus AD in Jupiter MD -- career auspicious period",
    ]


def test_build_dasha_timeline_returns_9_maha_periods() -> None:
    result = build_dasha_timeline("1990-05-15", 123.45)
    assert len(result) == 9


def test_build_dasha_timeline_each_maha_has_9_antardashas() -> None:
    result = build_dasha_timeline("1990-05-15", 123.45)
    for maha in result:
        assert len(maha["antardashas"]) == 9


def test_build_dasha_timeline_antardasha_end_aligns_with_maha_end() -> None:
    result = build_dasha_timeline("1990-05-15", 123.45)
    for maha in result:
        assert maha["antardashas"][-1]["end"] == maha["end"]


def test_compute_dasha_timeline_removed_or_shim(monkeypatch) -> None:
    assert not hasattr(knowledge_engine, "_build_sub_dashas")

    captured: dict[str, object] = {}

    def fake_build_dasha_timeline(birth_date: str, moon_longitude: float) -> list[dict]:
        captured["birth_date"] = birth_date
        captured["moon_longitude"] = moon_longitude
        return [{"planet": "Jupiter", "start": "1990-01-01", "end": "2006-01-01", "antardashas": []}]

    import vedic_calculator

    monkeypatch.setattr(vedic_calculator, "build_dasha_timeline", fake_build_dasha_timeline)
    chart = {"birth_details": {"date": "1990-05-15"}, "moon_longitude": 123.45}
    result = compute_dasha_timeline(chart)
    assert result[0]["planet"] == "Jupiter"
    assert captured == {"birth_date": "1990-05-15", "moon_longitude": 123.45}


def test_compute_confidence_base_only() -> None:
    profile = {"pillar_1": {"areas_completed": []}, "pillar_2": {"reports_run": []}, "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 40


def test_compute_confidence_all_questionnaire_areas() -> None:
    all_areas = ["health", "career", "finances", "learning", "emotional", "spirituality", "relationships", "family", "social", "adventure", "environment", "creativity"]
    profile = {"pillar_1": {"areas_completed": all_areas}, "pillar_2": {"reports_run": []}, "pillar_3": {"pillar_3_score": 0}}
    assert _compute_confidence(profile) == 64


def test_compute_confidence_partial_questionnaire() -> None:
    profile = {
        "pillar_1": {"areas_completed": ["health", "career", "finances", "learning", "emotional", "spirituality"]},
        "pillar_2": {"reports_run": []},
        "pillar_3": {"pillar_3_score": 0},
    }
    assert _compute_confidence(profile) == 52


def test_compute_confidence_with_irs() -> None:
    profile = {
        "pillar_1": {"areas_completed": ["health", "career", "finances", "learning", "emotional", "spirituality"]},
        "pillar_2": {"reports_run": ["brihat_kundali", "numerology", "longevity", "kp_oracle", "tarot", "palmistry"]},
        "pillar_3": {"pillar_3_score": 0},
    }
    assert _compute_confidence(profile) == 58


def test_compute_confidence_cap_at_86() -> None:
    all_areas = ["health", "career", "finances", "learning", "emotional", "spirituality", "relationships", "family", "social", "adventure", "environment", "creativity"]
    all_irs = ["brihat_kundali", "numerology", "longevity", "kp_oracle", "tarot", "palmistry", "lk", "love", "ir1", "ir2", "ir3", "ir4"]
    profile = {"pillar_1": {"areas_completed": all_areas}, "pillar_2": {"reports_run": all_irs}, "pillar_3": {"pillar_3_score": 10}}
    assert _compute_confidence(profile) == 86


def test_build_arc_angel_profile_doc_has_engine_label_and_12_domains() -> None:
    raw_windows, quality = _profile_windows_and_quality()
    profile = build_arc_angel_profile_doc(
        user_id="test_user",
        birth_date="1990-05-15",
        birth_time="10:30",
        birth_place="New Delhi",
        domain_quality_now=quality,
        raw_windows=raw_windows,
        data_completeness=build_arc_angel_data_completeness(),
    )
    assert profile["engine_label"] == "Vedic Astrology Engine Activated"
    assert len(profile["domains"]) == 12
    assert profile["overall_confidence_pct"] == 40


def test_arc_angel_profile_schema_has_required_fields_and_cache_freshness() -> None:
    raw_windows, quality = _profile_windows_and_quality()
    computed_at = datetime.now(timezone.utc)
    completeness = build_arc_angel_data_completeness(
        questionnaire_areas=["health", "career"],
        modules_run=["brihat_kundali"],
    )
    profile = build_arc_angel_profile_doc(
        user_id="test_user",
        birth_date="1990-05-15",
        birth_time="10:30",
        birth_place="New Delhi",
        domain_quality_now=quality,
        raw_windows=raw_windows,
        data_completeness=completeness,
        computed_at=computed_at,
    )
    domain = profile["domains"][0]
    assert set(domain) >= {
        "domain_id",
        "domain_label",
        "period_quality",
        "confidence_pct",
        "period_indicator",
        "auspicious_periods",
        "inauspicious_periods",
        "last_updated",
    }
    assert set(profile["pillar_3"]) >= {
        "pillar_3_score",
        "last_ritual_date",
        "decay_started_at",
        "tarot_love_score",
        "strategist_score",
    }
    assert arc_angel_profile_is_fresh(profile, completeness, now=computed_at + timedelta(hours=1)) is True
    assert arc_angel_profile_is_fresh(profile, completeness, now=computed_at + timedelta(hours=7)) is False
    assert profile["domains"][0]["domain_label"] == ARC_ANGEL_DOMAIN_LABELS[profile["domains"][0]["domain_id"]]
