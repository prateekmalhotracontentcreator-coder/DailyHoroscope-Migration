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

from ke_yoga_evaluator import evaluate_yoga_check
from knowledge_engine import ChartFacts, _condition_matches


def make_facts(
    placements: dict[str, tuple[int, str]],
    *,
    lagna_sign: str = "Aries",
    aspects: dict[str, set[int]] | None = None,
    aspected_by: dict[int, set[str]] | None = None,
    house_lords: dict[int, str] | None = None,
    varga_dignities: dict[str, dict] | None = None,
    yogas: set[str] | None = None,
    dignities: dict[str, str] | None = None,
    combusts: dict[str, bool] | None = None,
    retrogrades: dict[str, bool] | None = None,
) -> ChartFacts:
    planet_positions = {"Lagna": {"house": 1, "sign": lagna_sign, "dignity": "", "retrograde": False, "combust": False}}
    house_planets: dict[int, list[str]] = defaultdict(list)
    for planet, (house, sign) in placements.items():
        planet_positions[planet] = {
            "house": house,
            "sign": sign,
            "nakshatra": None,
            "dignity": (dignities or {}).get(planet, ""),
            "retrograde": (retrogrades or {}).get(planet, False),
            "combust": (combusts or {}).get(planet, False),
        }
        house_planets[house].append(planet)
    aspect_targets = defaultdict(set)
    for planet, houses in (aspects or {}).items():
        aspect_targets[planet].update(houses)
    reverse_aspects = defaultdict(set)
    for planet, houses in aspect_targets.items():
        for house in houses:
            reverse_aspects[house].add(planet)
    for house, planets in (aspected_by or {}).items():
        reverse_aspects[house].update(planets)
    return ChartFacts(
        planet_positions=planet_positions,
        house_planets=house_planets,
        house_lords=house_lords or {},
        yogas=yogas or set(),
        dasha_levels=defaultdict(set),
        aspect_targets=aspect_targets,
        aspected_by=reverse_aspects,
        varga_dignities=varga_dignities or {},
    )


BASE_PLACEMENTS = {
    "Sun": (1, "Aries"),
    "Moon": (2, "Taurus"),
    "Mars": (3, "Gemini"),
    "Mercury": (4, "Cancer"),
    "Jupiter": (5, "Leo"),
    "Venus": (6, "Virgo"),
    "Saturn": (7, "Libra"),
    "Rahu": (8, "Scorpio"),
    "Ketu": (9, "Sagittarius"),
}


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Venus": (5, "Virgo"), "Mars": (11, "Pisces")}, lagna_sign="Capricorn"),
            {"yoga_name": "Venus-Mars Wealth Axis - 5th/11th Own-Sign", "yoga_check": {"type": "planetary_combination", "checkable": True}},
            True,
        ),
        (
            make_facts({"Venus": (5, "Virgo"), "Mars": (10, "Aquarius")}, lagna_sign="Capricorn"),
            {"yoga_name": "Venus-Mars Wealth Axis - 5th/11th Own-Sign", "yoga_check": {"type": "planetary_combination", "checkable": True}},
            False,
        ),
    ],
    ids=["planetary_combination_positive", "planetary_combination_negative"],
)
def test_planetary_combination(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Jupiter": (7, "Libra"), "Mercury": (1, "Aries"), "Venus": (2, "Taurus")}, aspects={"Mercury": {7}, "Venus": {7}}),
            {"yoga_check": {"type": "planet_in_house", "checkable": True, "planet": "Jupiter", "houses": [2, 7], "aspected_by": ["Mercury", "Venus"]}},
            True,
        ),
        (
            make_facts({"Jupiter": (8, "Scorpio"), "Mercury": (1, "Aries"), "Venus": (2, "Taurus")}, aspects={"Mercury": {8}}),
            {"yoga_check": {"type": "planet_in_house", "checkable": True, "planet": "Jupiter", "houses": [2, 7], "aspected_by": ["Mercury", "Venus"]}},
            False,
        ),
    ],
    ids=["planet_in_house_positive", "planet_in_house_negative"],
)
def test_planet_in_house(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Venus": (2, "Taurus"), "Jupiter": (5, "Leo")}),
            {"yoga_check": {"type": "multi_house_requirements", "checkable": True, "requirements": [{"planet": "Venus", "house": 2}, {"planet": "Jupiter", "house": 5}]}},
            True,
        ),
        (
            make_facts({"Venus": (2, "Taurus"), "Jupiter": (6, "Virgo")}),
            {"yoga_check": {"type": "multi_house_requirements", "checkable": True, "requirements": [{"planet": "Venus", "house": 2}, {"planet": "Jupiter", "house": 5}]}},
            False,
        ),
    ],
    ids=["multi_house_requirements_positive", "multi_house_requirements_negative"],
)
def test_multi_house_requirements(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Moon": (1, "Aries"), "Mercury": (4, "Cancer"), "Venus": (7, "Libra"), "Jupiter": (10, "Capricorn")}),
            {"yoga_check": {"type": "benefics_in_houses", "checkable": True, "houses": [1, 4, 7, 10]}},
            True,
        ),
        (
            make_facts({"Moon": (1, "Aries"), "Mercury": (4, "Cancer"), "Venus": (7, "Libra"), "Jupiter": (11, "Aquarius")}),
            {"yoga_check": {"type": "benefics_in_houses", "checkable": True, "houses": [1, 4, 7, 10]}},
            False,
        ),
    ],
    ids=["benefics_in_houses_positive", "benefics_in_houses_negative"],
)
def test_benefics_in_houses(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Sun": (1, "Aries"), "Mars": (4, "Cancer"), "Saturn": (7, "Libra"), "Rahu": (10, "Capricorn"), "Ketu": (1, "Aries")}),
            {"yoga_check": {"type": "malefics_in_houses", "checkable": True, "houses": [1, 4, 7, 10]}},
            True,
        ),
        (
            make_facts({"Sun": (1, "Aries"), "Mars": (4, "Cancer"), "Saturn": (7, "Libra"), "Rahu": (11, "Aquarius"), "Ketu": (1, "Aries")}),
            {"yoga_check": {"type": "malefics_in_houses", "checkable": True, "houses": [1, 4, 7, 10]}},
            False,
        ),
    ],
    ids=["malefics_in_houses_positive", "malefics_in_houses_negative"],
)
def test_malefics_in_houses(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Jupiter": (10, "Capricorn")}),
            {"yoga_check": {"type": "benefic_only_in_house", "checkable": True, "house": 10}},
            True,
        ),
        (
            make_facts({"Jupiter": (10, "Capricorn"), "Mars": (10, "Capricorn")}),
            {"yoga_check": {"type": "benefic_only_in_house", "checkable": True, "house": 10}},
            False,
        ),
    ],
    ids=["benefic_only_in_house_positive", "benefic_only_in_house_negative"],
)
def test_benefic_only_in_house(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Moon": (1, "Aries"), "Jupiter": (4, "Cancer")}),
            {"yoga_check": {"type": "planet_in_kendra_from", "checkable": True, "planet": "Jupiter", "reference": "Moon", "positions": [1, 4, 7, 10]}},
            True,
        ),
        (
            make_facts({"Moon": (1, "Aries"), "Jupiter": (3, "Gemini")}),
            {"yoga_check": {"type": "planet_in_kendra_from", "checkable": True, "planet": "Jupiter", "reference": "Moon", "positions": [1, 4, 7, 10]}},
            False,
        ),
    ],
    ids=["planet_in_kendra_from_positive", "planet_in_kendra_from_negative"],
)
def test_planet_in_kendra_from(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Cancer"),
                "Mars": (3, "Libra"),
                "Mercury": (4, "Capricorn"),
                "Jupiter": (5, "Aries"),
                "Venus": (6, "Cancer"),
                "Saturn": (7, "Libra"),
            }),
            {"yoga_name": "Rajju Yoga", "yoga_check": {"type": "sign_quality_all", "checkable": True}},
            True,
        ),
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Cancer"),
                "Mars": (3, "Libra"),
                "Mercury": (4, "Capricorn"),
                "Jupiter": (5, "Taurus"),
                "Venus": (6, "Cancer"),
                "Saturn": (7, "Libra"),
            }),
            {"yoga_name": "Rajju Yoga", "yoga_check": {"type": "sign_quality_all", "checkable": True}},
            False,
        ),
    ],
    ids=["sign_quality_all_positive", "sign_quality_all_negative"],
)
def test_sign_quality_all(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Moon": (1, "Aries"), "Mercury": (4, "Cancer"), "Venus": (7, "Libra"), "Jupiter": (10, "Capricorn")}),
            {"yoga_check": {"type": "angles_by_planet_type", "checkable": True, "planet_type": "benefic", "required_houses": [1, 4, 7, 10], "requires_all": True}},
            True,
        ),
        (
            make_facts({"Moon": (1, "Aries"), "Mercury": (4, "Cancer"), "Venus": (7, "Libra"), "Jupiter": (11, "Aquarius")}),
            {"yoga_check": {"type": "angles_by_planet_type", "checkable": True, "planet_type": "benefic", "required_houses": [1, 4, 7, 10], "requires_all": True}},
            False,
        ),
    ],
    ids=["angles_by_planet_type_positive", "angles_by_planet_type_negative"],
)
def test_angles_by_planet_type(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (1, "Aries"),
                "Mars": (2, "Taurus"),
                "Mercury": (2, "Taurus"),
                "Jupiter": (3, "Gemini"),
                "Venus": (4, "Cancer"),
                "Saturn": (4, "Cancer"),
            }),
            {"yoga_check": {"type": "planets_in_n_signs", "checkable": True, "n": 4}},
            True,
        ),
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Taurus"),
                "Mars": (3, "Gemini"),
                "Mercury": (4, "Cancer"),
                "Jupiter": (5, "Leo"),
                "Venus": (1, "Aries"),
                "Saturn": (2, "Taurus"),
            }),
            {"yoga_check": {"type": "planets_in_n_signs", "checkable": True, "n": 4}},
            False,
        ),
    ],
    ids=["planets_in_n_signs_positive", "planets_in_n_signs_negative"],
)
def test_planets_in_n_signs(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Gemini"),
                "Mars": (3, "Leo"),
                "Mercury": (4, "Libra"),
                "Jupiter": (5, "Sagittarius"),
                "Venus": (6, "Aquarius"),
                "Saturn": (7, "Aries"),
            }),
            {"yoga_check": {"type": "all_planets_in_alt_signs", "checkable": True, "sign_parity": "odd"}},
            True,
        ),
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Gemini"),
                "Mars": (3, "Leo"),
                "Mercury": (4, "Libra"),
                "Jupiter": (5, "Sagittarius"),
                "Venus": (6, "Pisces"),
                "Saturn": (7, "Aries"),
            }),
            {"yoga_check": {"type": "all_planets_in_alt_signs", "checkable": True, "sign_parity": "odd"}},
            False,
        ),
    ],
    ids=["all_planets_in_alt_signs_positive", "all_planets_in_alt_signs_negative"],
)
def test_all_planets_in_alt_signs(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Taurus"),
                "Mars": (3, "Gemini"),
                "Mercury": (4, "Cancer"),
                "Jupiter": (5, "Leo"),
                "Venus": (6, "Virgo"),
                "Saturn": (1, "Aries"),
            }),
            {"yoga_check": {"type": "all_planets_in_houses", "checkable": True, "houses": [1, 2, 3, 4, 5, 6]}},
            True,
        ),
        (
            make_facts({
                "Sun": (1, "Aries"),
                "Moon": (2, "Taurus"),
                "Mars": (3, "Gemini"),
                "Mercury": (4, "Cancer"),
                "Jupiter": (5, "Leo"),
                "Venus": (7, "Libra"),
                "Saturn": (1, "Aries"),
            }),
            {"yoga_check": {"type": "all_planets_in_houses", "checkable": True, "houses": [1, 2, 3, 4, 5, 6]}},
            False,
        ),
    ],
    ids=["all_planets_in_houses_positive", "all_planets_in_houses_negative"],
)
def test_all_planets_in_houses(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Moon": (1, "Aries"), "Mars": (2, "Taurus")}),
            {"yoga_check": {"type": "planet_in_house_from_moon", "checkable": True, "planet": "any_except_sun", "distance_from_moon": 2}},
            True,
        ),
        (
            make_facts({"Moon": (1, "Aries"), "Mars": (3, "Gemini")}),
            {"yoga_check": {"type": "planet_in_house_from_moon", "checkable": True, "planet": "any_except_sun", "distance_from_moon": 2}},
            False,
        ),
    ],
    ids=["planet_in_house_from_moon_positive", "planet_in_house_from_moon_negative"],
)
def test_planet_in_house_from_moon(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Moon": (5, "Leo"), "Sun": (9, "Sagittarius")}),
            {"yoga_check": {"type": "kemadruma_check", "checkable": True, "strict": False}},
            True,
        ),
        (
            make_facts({"Moon": (5, "Leo"), "Jupiter": (6, "Virgo")}),
            {"yoga_check": {"type": "kemadruma_check", "checkable": True, "strict": False}},
            False,
        ),
    ],
    ids=["kemadruma_check_positive", "kemadruma_check_negative"],
)
def test_kemadruma_check(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Sun": (1, "Aries"), "Moon": (4, "Cancer")}),
            {"yoga_check": {"type": "moon_from_sun_position", "checkable": True, "houses_from_sun": [1, 4, 7, 10]}},
            True,
        ),
        (
            make_facts({"Sun": (1, "Aries"), "Moon": (3, "Gemini")}),
            {"yoga_check": {"type": "moon_from_sun_position", "checkable": True, "houses_from_sun": [1, 4, 7, 10]}},
            False,
        ),
    ],
    ids=["moon_from_sun_position_positive", "moon_from_sun_position_negative"],
)
def test_moon_from_sun_position(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            make_facts({"Saturn": (1, "Aries")}),
            {"yoga_check": {"type": "dosha", "checkable": True, "planet": "Saturn", "house": 1, "dosha_type": "negative_placement"}},
            True,
        ),
        (
            make_facts({"Saturn": (2, "Taurus")}),
            {"yoga_check": {"type": "dosha", "checkable": True, "planet": "Saturn", "house": 1, "dosha_type": "negative_placement"}},
            False,
        ),
    ],
    ids=["dosha_positive", "dosha_negative"],
)
def test_dosha(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


def test_guard_clause_for_uncheckable_rule() -> None:
    facts = make_facts(BASE_PLACEMENTS)
    result = evaluate_yoga_check({"yoga_check": {"type": "complex", "checkable": False}}, facts)
    assert result.checkable is False
    assert result.matched is False
    assert result.evidence == ["Rule not yet checkable"]


def test_condition_matches_dispatches_yoga_combination() -> None:
    facts = make_facts({"Venus": (5, "Virgo"), "Mars": (11, "Pisces")}, lagna_sign="Capricorn")
    condition = {
        "type": "yoga_combination",
        "yoga_name": "Venus-Mars Wealth Axis - 5th/11th Own-Sign",
        "yoga_check": {"type": "planetary_combination", "checkable": True},
    }
    assert _condition_matches(condition, facts) is True


# ---------------------------------------------------------------------------
# varga_dignity_tier (Brief D -- evaluator #17)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("facts", "condition", "expected"),
    [
        (
            # angular_lord is Jupiter (house 10), tier Iravatamsa ≥ required Devalokamsa → match
            make_facts(
                {"Jupiter": (10, "Capricorn")},
                house_lords={10: "Jupiter"},
                varga_dignities={"Jupiter": {"count": 9, "tier": "Iravatamsa"}},
            ),
            {
                "yoga_check": {
                    "type": "varga_dignity_tier",
                    "checkable": True,
                    "planet_role": "angular_lord",
                    "required_tier": "Devalokamsa",
                    "blockers": [],
                },
            },
            True,
        ),
        (
            # angular_lord is Saturn (house 10), tier Parijatamsa < required Gopuramsa → no match
            make_facts(
                {"Saturn": (10, "Capricorn")},
                house_lords={10: "Saturn"},
                varga_dignities={"Saturn": {"count": 2, "tier": "Parijatamsa"}},
            ),
            {
                "yoga_check": {
                    "type": "varga_dignity_tier",
                    "checkable": True,
                    "planet_role": "angular_lord",
                    "required_tier": "Gopuramsa",
                    "blockers": [],
                },
            },
            False,
        ),
        (
            # no house lords populated → evaluator returns False with explanation
            make_facts(
                {},
                house_lords={},
                varga_dignities={},
            ),
            {
                "yoga_check": {
                    "type": "varga_dignity_tier",
                    "checkable": True,
                    "planet_role": "angular_lord",
                    "required_tier": "Gopuramsa",
                    "blockers": [],
                },
            },
            False,
        ),
    ],
    ids=[
        "varga_dignity_tier_positive",
        "varga_dignity_tier_negative",
        "varga_dignity_tier_no_lords",
    ],
)
def test_varga_dignity_tier(facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert evaluate_yoga_check(condition, facts).matched is expected


# ── Dignity tests ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "facts, condition, expected",
    [
        (
            # Sun in Aries → exalted
            make_facts({"Sun": (1, "Aries")}, dignities={"Sun": "exalted"}),
            {"type": "planet_dignity", "planet": "Sun", "dignity": "exalted"},
            True,
        ),
        (
            # Saturn in Aries → debilitated
            make_facts({"Saturn": (1, "Aries")}, dignities={"Saturn": "debilitated"}),
            {"type": "planet_dignity", "planet": "Saturn", "dignity": "debilitated"},
            True,
        ),
        (
            # Jupiter in Cancer (exalted) does NOT match "own_sign"
            make_facts({"Jupiter": (4, "Cancer")}, dignities={"Jupiter": "exalted"}),
            {"type": "planet_dignity", "planet": "Jupiter", "dignity": "own_sign"},
            False,
        ),
        (
            # Mercury in Virgo → moolatrikona
            make_facts({"Mercury": (6, "Virgo")}, dignities={"Mercury": "moolatrikona"}),
            {"type": "planet_dignity", "planet": "Mercury", "dignity": "moolatrikona"},
            True,
        ),
    ],
    ids=["dignity_exalted", "dignity_debilitated", "dignity_mismatch", "dignity_moolatrikona"],
)
def test_planet_dignity(_condition_matches_import, facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert _condition_matches(condition, facts) is expected


# ── Combust tests ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "facts, condition, expected",
    [
        (
            # Mars combust → matches planet_combust condition
            make_facts({"Mars": (1, "Aries")}, combusts={"Mars": True}),
            {"type": "planet_combust", "planet": "Mars"},
            True,
        ),
        (
            # Jupiter not combust → does not match
            make_facts({"Jupiter": (5, "Leo")}, combusts={"Jupiter": False}),
            {"type": "planet_combust", "planet": "Jupiter"},
            False,
        ),
        (
            # combust flag absent → defaults to False → no match
            make_facts({"Venus": (7, "Libra")}),
            {"type": "planet_combust", "planet": "Venus"},
            False,
        ),
    ],
    ids=["combust_positive", "combust_negative", "combust_absent"],
)
def test_planet_combust(_condition_matches_import, facts: ChartFacts, condition: dict, expected: bool) -> None:
    assert _condition_matches(condition, facts) is expected


# ── Dignity + combustion pure-logic unit tests ───────────────────────────────
# These replicate the logic from vedic_calculator.get_planet_dignity /
# is_planet_combust inline -- avoiding the flatlib + pyswisseph module-level
# imports that make vedic_calculator.py hard to import in a stub environment.

_SIGN_ORDER = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]
_EXALTATION = {
    'Sun': ('Aries', 10), 'Moon': ('Taurus', 3), 'Mars': ('Capricorn', 28),
    'Mercury': ('Virgo', 15), 'Jupiter': ('Cancer', 5),
    'Venus': ('Pisces', 27), 'Saturn': ('Libra', 20),
}
_DEBILITATION_SIGNS = {
    p: _SIGN_ORDER[(_SIGN_ORDER.index(s) + 6) % 12]
    for p, (s, _) in _EXALTATION.items()
}
_MOOLATRIKONA = {
    'Sun': ('Leo', 0, 20), 'Moon': ('Taurus', 3, 30), 'Mars': ('Aries', 0, 12),
    'Mercury': ('Virgo', 16, 20), 'Jupiter': ('Sagittarius', 0, 10),
    'Venus': ('Libra', 0, 15), 'Saturn': ('Aquarius', 0, 20),
}
_OWN_SIGNS = {
    'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mars': ['Aries', 'Scorpio'],
    'Mercury': ['Gemini', 'Virgo'], 'Jupiter': ['Sagittarius', 'Pisces'],
    'Venus': ['Taurus', 'Libra'], 'Saturn': ['Capricorn', 'Aquarius'],
}
_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'], 'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'], 'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'], 'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
}
_ENEMIES = {
    'Sun': ['Venus', 'Saturn'], 'Moon': [], 'Mars': ['Mercury'],
    'Mercury': ['Moon'], 'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'], 'Saturn': ['Sun', 'Moon', 'Mars'],
}
_SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter',
}
_COMBUSTION_ORBS = {
    'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15,
}


def _dignity(planet: str, sign: str, degree: float) -> str:
    if planet not in _EXALTATION:
        return 'neutral'
    if sign == _EXALTATION[planet][0]:
        return 'exalted'
    if sign == _DEBILITATION_SIGNS[planet]:
        return 'debilitated'
    mt_sign, mt_start, mt_end = _MOOLATRIKONA[planet]
    if sign == mt_sign and mt_start <= degree <= mt_end:
        return 'moolatrikona'
    if sign in _OWN_SIGNS.get(planet, []):
        return 'own_sign'
    lord = _SIGN_LORDS.get(sign, '')
    if lord in _FRIENDS.get(planet, []):
        return 'friendly'
    if lord in _ENEMIES.get(planet, []):
        return 'enemy'
    return 'neutral'


def _combust(planet: str, planet_lon: float, sun_lon: float) -> bool:
    if planet not in _COMBUSTION_ORBS:
        return False
    diff = abs(planet_lon - sun_lon) % 360
    if diff > 180:
        diff = 360 - diff
    return diff <= _COMBUSTION_ORBS[planet]


def test_dignity_computation_unit() -> None:
    assert _dignity("Sun",     "Aries",       10) == "exalted"
    assert _dignity("Moon",    "Taurus",       3) == "exalted"
    assert _dignity("Mars",    "Capricorn",   28) == "exalted"
    assert _dignity("Jupiter", "Capricorn",    5) == "debilitated"
    assert _dignity("Saturn",  "Aries",       20) == "debilitated"
    assert _dignity("Sun",     "Leo",         10) == "moolatrikona"
    assert _dignity("Saturn",  "Aquarius",    10) == "moolatrikona"
    assert _dignity("Mars",    "Scorpio",     20) == "own_sign"
    assert _dignity("Jupiter", "Pisces",      15) == "own_sign"
    assert _dignity("Sun",     "Sagittarius", 10) == "friendly"   # Jupiter's sign
    assert _dignity("Saturn",  "Gemini",      10) == "friendly"   # Mercury's sign
    assert _dignity("Sun",     "Libra",       15) == "debilitated"
    assert _dignity("Moon",    "Scorpio",      5) == "debilitated"
    assert _dignity("Rahu",    "Taurus",      10) == "neutral"    # nodes → neutral


def test_combustion_computation_unit() -> None:
    assert not _combust("Sun",   0.0,   0.0)    # Sun never combust
    assert not _combust("Rahu",  10.0,  10.0)   # nodes exempt
    assert _combust("Mars",     15.0,   0.0)    # within 17° orb
    assert _combust("Mars",     17.0,   0.0)    # exactly at orb (inclusive)
    assert not _combust("Mars", 18.0,   0.0)    # just outside orb
    assert _combust("Saturn",  355.0,   5.0)    # across 0°/360° boundary, diff=10°


def test_yoga_handler_supports_structured_debt_rules() -> None:
    facts = make_facts({"Sun": (10, "Capricorn"), "Moon": (11, "Aquarius"), "Saturn": (5, "Leo")})
    condition = {
        "type": "dosha",
        "sub_type": "debt",
        "trigger_planets": ["Sun", "Moon"],
        "trigger_houses": [10, 11],
        "trigger_operator": "and",
        "negative_condition": {"planet": "Saturn", "houses": [3, 4], "constraint": "absent"},
        "yoga_check": {"type": "yoga", "checkable": True},
    }
    result = evaluate_yoga_check(condition, facts)
    assert result.matched is True


def test_planet_affliction_detects_malefic_pressure() -> None:
    facts = make_facts({"Mars": (7, "Libra"), "Saturn": (7, "Libra")})
    condition = {"yoga_check": {"type": "planet_affliction", "checkable": True, "planet": "Mars Benefic"}}
    result = evaluate_yoga_check(condition, facts)
    assert result.matched is True
    assert any("conjunction" in note.lower() for note in result.evidence)


def test_planet_conjunction_checks_shared_house() -> None:
    facts = make_facts({"Jupiter": (4, "Cancer"), "Sun": (4, "Cancer")})
    condition = {
        "planets_involved": ["Jupiter", "Sun"],
        "conjunction": ["Jupiter", "Sun"],
        "yoga_check": {"type": "planet_conjunction", "checkable": True},
    }
    assert evaluate_yoga_check(condition, facts).matched is True


def test_planet_in_house_from_sun_supports_compound_requirements() -> None:
    facts = make_facts({"Sun": (1, "Aries"), "Mars": (2, "Taurus"), "Jupiter": (12, "Pisces")})
    condition = {
        "yoga_check": {
            "type": "planet_in_house_from_sun",
            "checkable": True,
            "houses": [2, 12],
            "operator": "and",
            "exclude_planets": ["Moon"],
        }
    }
    assert evaluate_yoga_check(condition, facts).matched is True


def test_planet_combust_honors_exclusions() -> None:
    facts = make_facts({"Mercury": (2, "Taurus"), "Venus": (3, "Gemini")}, combusts={"Mercury": True, "Venus": True})
    condition = {
        "yoga_check": {
            "type": "planet_combust",
            "checkable": True,
            "excluded_planets": ["Venus"],
        }
    }
    result = evaluate_yoga_check(condition, facts)
    assert result.matched is True
    assert "Mercury" in result.evidence[0]


def test_house_position_supports_annual_house_shape() -> None:
    facts = make_facts({"Ketu": (8, "Scorpio")})
    condition = {
        "type": "journey_outcome",
        "planet": "Ketu",
        "ketu_annual_house": 8,
        "validation": {"yoga_check": {"type": "house_position", "checkable": True}},
    }
    assert evaluate_yoga_check(condition, facts).matched is True


# fixture alias so dignity/combust tests can import _condition_matches
@pytest.fixture
def _condition_matches_import():
    return None
