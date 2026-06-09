from __future__ import annotations

import sys
import types
from collections import defaultdict
from pathlib import Path

import pytest


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

from ke_schema_constants import VALID_CLAIM_AXES
from knowledge_engine import ChartFacts, _condition_matches, extract_chart_facts, get_t05_enrichment
from knowledge_schema import InterpretationRuleDocument
from kp_engine import kp_chain
from kp_sublord_table import (
    T05_BY_CHAIN,
    T05_BY_NUMBER,
    get_profession_entry,
    get_sub_entries,
    get_sub_entry_for_sign,
)


def _first_non_shadow_linked_planet(chain: dict[str, str]) -> str:
    for planet in (chain["star_lord"], chain["sub_lord"], chain["sub_sub_lord"]):
        if planet not in {"Jupiter", "Rahu", "Ketu"}:
            return planet
    return "Mercury"


def build_kp_chart() -> tuple[dict, dict[str, str], str, float]:
    jupiter_longitude = 266.8
    jupiter_chain = kp_chain(jupiter_longitude)
    linked_planet = _first_non_shadow_linked_planet(jupiter_chain)
    cusp_longitude = 123.4
    cusp_chain = kp_chain(cusp_longitude)

    chart = {
        "planets": {
            "Jupiter": {
                "house": 5,
                "sign": "Sagittarius",
                "nakshatra": jupiter_chain["nakshatra"],
                "longitude": jupiter_longitude,
            },
            linked_planet: {
                "house": 8,
                "sign": "Scorpio",
                "nakshatra": kp_chain(45.0)["nakshatra"],
                "longitude": 45.0,
            },
        },
        "houses": {
            1: {"lord": "Mars"},
            5: {"lord": "Jupiter"},
            8: {"lord": linked_planet},
        },
        "cusps": [{"longitude": cusp_longitude + (index - 1) * 30.0} for index in range(1, 13)],
    }
    return chart, jupiter_chain, linked_planet, cusp_chain["sub_lord"]


def test_kp_lookup_tables_are_baked_in() -> None:
    assert len(T05_BY_NUMBER) == 249
    assert T05_BY_CHAIN[("Ketu", "Ketu")]
    assert get_sub_entries("Ketu", "Ketu")
    assert get_sub_entry_for_sign("Ketu", "Venus", "Aries") is not None
    assert get_profession_entry("Abrasives") is not None


def test_extract_chart_facts_populates_kp_fields() -> None:
    chart, jupiter_chain, linked_planet, cusp_sub_lord = build_kp_chart()
    facts = extract_chart_facts(chart)

    assert facts.kp_chains["Jupiter"] == {
        "star_lord": jupiter_chain["star_lord"],
        "sub_lord": jupiter_chain["sub_lord"],
        "sub_sub_lord": jupiter_chain["sub_sub_lord"],
    }
    assert facts.planet_positions["Jupiter"]["longitude"] == pytest.approx(266.8)
    assert facts.kp_significations["Jupiter"]
    assert 5 in facts.kp_significations["Jupiter"]
    assert linked_planet in facts.planet_positions
    assert facts.cuspal_sub_lords[1] == cusp_sub_lord


def test_kp_condition_handlers_and_composite_logic() -> None:
    chart, jupiter_chain, linked_planet, cusp_sub_lord = build_kp_chart()
    facts = extract_chart_facts(chart)

    assert linked_planet in facts.planet_positions
    assert _condition_matches(
        {"type": "kp_star_lord", "planet": "Jupiter", "star_lord": jupiter_chain["star_lord"]},
        facts,
    )
    assert _condition_matches(
        {"type": "kp_sublord", "planet": "Jupiter", "house": 5, "star_lord": jupiter_chain["star_lord"]},
        facts,
    )
    assert _condition_matches(
        {"type": "kp_planet_signification", "planet": "Jupiter", "house": 5},
        facts,
    )
    assert _condition_matches(
        {"type": "kp_signification_chain", "planet": "Jupiter", "houses": [5, 8]},
        facts,
    )
    assert _condition_matches(
        {"type": "kp_csl", "house": 1, "sub_lord": cusp_sub_lord},
        facts,
    )

    assert _condition_matches(
        {
            "type": "composite",
            "operator": "and",
            "sub_conditions": [
                {"type": "kp_star_lord", "planet": "Jupiter", "star_lord": jupiter_chain["star_lord"]},
                {"type": "kp_planet_signification", "planet": "Jupiter", "house": 5},
            ],
        },
        facts,
    )
    assert _condition_matches(
        {
            "type": "composite",
            "operator": "or",
            "sub_conditions": [
                {"type": "kp_star_lord", "planet": "Jupiter", "star_lord": "Saturn"},
                {"type": "kp_planet_signification", "planet": "Jupiter", "house": 5},
            ],
        },
        facts,
    )
    assert not _condition_matches(
        {
            "type": "composite",
            "operator": "xor",
            "sub_conditions": [
                {"type": "kp_star_lord", "planet": "Jupiter", "star_lord": jupiter_chain["star_lord"]},
            ],
        },
        facts,
    )


def test_secondary_axis_and_claim_axis_aliases_validate() -> None:
    doc = InterpretationRuleDocument(
        rule_id="KE-OP18-TEST-1",
        life_domain="career",
        claim_axis="career",
        secondary_axis="health",
        claim_scope="natal",
        claim_polarity="positive",
        timing_bias="none",
        strength_band="medium",
        subject_scope="self",
        condition={"type": "kp_star_lord", "planet": "Jupiter", "star_lord": "Mars"},
        interpretation={"summary": "x", "detailed": "y"},
        source={"primary": "test", "chapter": "1", "author_voice": "classical", "batch_id": "batch"},
    )

    assert doc.secondary_axis == "health"
    for axis in {"career", "health", "marriage", "timing", "death_timing", "death_mode", "spouse_longevity"}:
        assert axis in VALID_CLAIM_AXES


def test_get_t05_enrichment_uses_baked_lookup() -> None:
    chart, _, _, _ = build_kp_chart()
    facts = extract_chart_facts(chart)
    chain = facts.kp_chains["Jupiter"]
    table_match = get_sub_entries(chain["star_lord"], chain["sub_lord"])
    assert table_match
    facts.planet_positions["Jupiter"]["sign"] = table_match[0]["sign"]
    enrichment = get_t05_enrichment("Jupiter", facts)

    assert enrichment is not None
    assert enrichment["sign"] == table_match[0]["sign"]
