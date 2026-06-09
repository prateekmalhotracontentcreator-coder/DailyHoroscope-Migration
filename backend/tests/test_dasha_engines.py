"""
test_dasha_engines.py
Tests for Commission VC-1: Kalachakra & Chara Dasa Engines

Run:  python3 -m pytest backend/tests/test_dasha_engines.py -v
"""
from __future__ import annotations

import sys
import os

# Ensure backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vedic_calculator import (
    KALACHAKRA_PERIODS,
    KALACHAKRA_SAVYA_SIGNS,
    KALACHAKRA_APASAVYA_SIGNS,
    _KAL_TOTAL,
    CHARA_SIGN_LORDS,
    SIGN_MODALITY,
    SIGN_ORDER,
    calculate_kalachakra_dasha,
    build_kalachakra_timeline,
    get_current_kalachakra_dasha,
    chara_duration,
    calculate_chara_dasha,
    build_chara_timeline,
    get_current_chara_dasha,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _moon_lon_for_sign_pada(sign: str, pada: int = 0) -> float:
    """
    Return a Moon longitude that places the Moon in the given sign's
    first navamsa pada (or a specified pada, 0-indexed) of the
    108-point Kalachakra wheel.

    navamsa_size = 360/108 ≈ 3.333°
    Each Kalachakra Rasi = 9 padas × 3.333° = 30°
    sign start longitude = SIGN_ORDER.index(sign) × 30°
    pada start within sign = pada × 3.333°
    """
    navamsa_size = 360.0 / 108
    sign_idx     = SIGN_ORDER.index(sign)
    lon          = sign_idx * 30.0 + pada * navamsa_size + 0.5   # +0.5 to be mid-pada
    return lon


# ─────────────────────────────────────────────────────────────────────────────
# KALACHAKRA TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_kalachakra_moon_in_aries_savya_direction():
    """Moon at ~5° (Aries Navamsa 1) → first dasha = Aries, direction = forward."""
    # Aries is index 0; first pada (pada 0) within the 108 wheel ≈ longitude 0.5°
    moon_lon   = _moon_lon_for_sign_pada("Aries", pada=0)   # ~0.5°
    lagna_lon  = 0.0  # Aries lagna
    dashas     = calculate_kalachakra_dasha("1990-01-01", moon_lon, lagna_lon)

    assert dashas, "Dasha list must not be empty"
    assert dashas[0]["sign"] == "Aries", (
        f"First dasha sign must be Aries, got {dashas[0]['sign']}"
    )
    # In Savya (forward), second sign should be Taurus
    assert dashas[1]["sign"] == "Taurus", (
        f"Second dasha sign must be Taurus (forward direction), got {dashas[1]['sign']}"
    )
    assert "Aries" in KALACHAKRA_SAVYA_SIGNS


def test_kalachakra_moon_in_libra_apasavya_direction():
    """Moon at ~185° (Libra Navamsa 1) → direction = backward."""
    moon_lon  = _moon_lon_for_sign_pada("Libra", pada=0)    # ~180.5°
    lagna_lon = 0.0
    dashas    = calculate_kalachakra_dasha("1990-01-01", moon_lon, lagna_lon)

    assert dashas[0]["sign"] == "Libra", (
        f"First dasha sign must be Libra, got {dashas[0]['sign']}"
    )
    # In Apasavya (backward), second sign should be Virgo
    assert dashas[1]["sign"] == "Virgo", (
        f"Second dasha sign must be Virgo (backward direction), got {dashas[1]['sign']}"
    )
    assert "Libra" in KALACHAKRA_APASAVYA_SIGNS


def test_kalachakra_balance_correct():
    """Moon at mid-pada → years_remaining ≈ half the Aries period."""
    # Pada 4 of Aries (0-indexed) = 4/9 elapsed → 5/9 remaining
    # Aries period = 7 years → remaining ≈ 7 × 5/9 ≈ 3.889 years
    moon_lon  = _moon_lon_for_sign_pada("Aries", pada=4)
    lagna_lon = 0.0
    dashas    = calculate_kalachakra_dasha("1990-01-01", moon_lon, lagna_lon)

    first_years = dashas[0]["years"]
    expected    = KALACHAKRA_PERIODS["Aries"] * (1.0 - 4 / 9.0)
    assert abs(first_years - expected) < 0.01, (
        f"First dasha balance expected ~{expected:.3f}, got {first_years}"
    )


def test_kalachakra_timeline_has_antardashas():
    """build_kalachakra_timeline returns list where every entry has 'antardashas' key."""
    moon_lon  = _moon_lon_for_sign_pada("Aries", pada=0)
    lagna_lon = 0.0
    timeline  = build_kalachakra_timeline("1990-01-01", moon_lon, lagna_lon)

    assert timeline, "Timeline must not be empty"
    for entry in timeline:
        assert "antardashas" in entry, f"Entry {entry['sign']} missing 'antardashas'"
        assert len(entry["antardashas"]) == 12, (
            f"Expected 12 antardashas per maha, got {len(entry['antardashas'])}"
        )


def test_kalachakra_8th_sign_mortality_flag():
    """Lagna = Aries → 8th sign = Scorpio → Scorpio dasha entry has mortality_flag=True."""
    moon_lon  = _moon_lon_for_sign_pada("Aries", pada=0)
    lagna_lon = 0.0   # Aries lagna (index 0 → 8th sign = index 7 = Scorpio)
    dashas    = calculate_kalachakra_dasha("1990-01-01", moon_lon, lagna_lon)

    scorpio_dashas = [d for d in dashas if d["sign"] == "Scorpio"]
    assert scorpio_dashas, "Scorpio must appear in the dasha sequence"
    for sd in scorpio_dashas:
        assert sd.get("mortality_flag") is True, (
            f"Scorpio dasha (8th from Aries lagna) must have mortality_flag=True"
        )


def test_kalachakra_return_format():
    """Each entry must have keys: sign, planet, start, end, years."""
    moon_lon  = _moon_lon_for_sign_pada("Cancer", pada=2)
    lagna_lon = 60.0
    dashas    = calculate_kalachakra_dasha("1985-06-15", moon_lon, lagna_lon)

    required_keys = {"sign", "planet", "start", "end", "years"}
    for entry in dashas:
        missing = required_keys - entry.keys()
        assert not missing, f"Dasha entry missing keys: {missing}"
    # planet must be a string (sign lord)
    for entry in dashas:
        assert isinstance(entry["planet"], str), "planet field must be a string"
        assert isinstance(entry["sign"],   str), "sign field must be a string"


# ─────────────────────────────────────────────────────────────────────────────
# CHARA TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_chara_duration_movable_sign():
    """Aries, Mars in Scorpio → forward count Aries→Scorpio = 8 years."""
    pos = {
        "Sun": "Leo", "Moon": "Taurus", "Mars": "Scorpio",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Libra",
        "Saturn": "Capricorn", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    # Aries is movable; CHARA_SIGN_LORDS["Aries"] = "Mars" (standard lord)
    # Mars in Scorpio: forward count Aries(0) → Scorpio(7): (7-0)%12+1 = 8
    result = chara_duration("Aries", pos)
    assert result == 8, f"Aries with Mars in Scorpio must give 8 years, got {result}"


def test_chara_duration_fixed_sign():
    """Taurus, Venus in Libra → backward count Taurus→Libra = 8 years."""
    pos = {
        "Sun": "Leo", "Moon": "Cancer", "Mars": "Scorpio",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Libra",
        "Saturn": "Capricorn", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    # Taurus is fixed; CHARA_SIGN_LORDS["Taurus"] = "Venus"
    # Venus in Libra: backward count Taurus(1) → Libra(6): (1-6)%12+1 = 7+1 = 8
    result = chara_duration("Taurus", pos)
    assert result == 8, f"Taurus with Venus in Libra must give 8 years, got {result}"


def test_chara_duration_lord_in_own_sign():
    """Any sign where lord occupies the same sign → 12 years."""
    pos = {
        "Sun": "Leo", "Moon": "Cancer", "Mars": "Aries",
        "Mercury": "Gemini", "Jupiter": "Sagittarius", "Venus": "Taurus",
        "Saturn": "Capricorn", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    # Mars in Aries → Aries lord (Mars) in own sign → 12 years
    result = chara_duration("Aries", pos)
    assert result == 12, f"Lord in own sign must give 12 years, got {result}"

    # Venus in Taurus → Taurus lord (Venus) in own sign → 12 years
    result2 = chara_duration("Taurus", pos)
    assert result2 == 12, f"Venus in own sign (Taurus) must give 12 years, got {result2}"


def test_chara_antardasha_starts_from_lord_sign():
    """
    Chara Aries maha, Mars (CHARA lord of Aries) in Scorpio
    → antardasha sequence starts from Scorpio.
    """
    pos = {
        "Sun": "Leo", "Moon": "Taurus", "Mars": "Scorpio",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Libra",
        "Saturn": "Capricorn", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    # lagna = Aries so first maha = Aries
    timeline = build_chara_timeline("1990-01-01", pos, "Aries")

    aries_maha = next(e for e in timeline if e["sign"] == "Aries")
    first_antar = aries_maha["antardashas"][0]

    # CHARA_SIGN_LORDS["Aries"] = "Mars"; Mars is in Scorpio → first antar = Scorpio
    assert first_antar["sign"] == "Scorpio", (
        f"First antardasha of Aries maha must start from Scorpio "
        f"(Mars's sign), got {first_antar['sign']}"
    )


def test_chara_timeline_has_antardashas():
    """build_chara_timeline returns list where every entry has 'antardashas' key."""
    pos = {
        "Sun": "Leo", "Moon": "Taurus", "Mars": "Scorpio",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Libra",
        "Saturn": "Capricorn", "Rahu": "Gemini", "Ketu": "Sagittarius",
    }
    timeline = build_chara_timeline("1990-01-01", pos, "Aries")

    assert timeline, "Chara timeline must not be empty"
    for entry in timeline:
        assert "antardashas" in entry, f"Entry {entry['sign']} missing 'antardashas'"
        assert len(entry["antardashas"]) == 12, (
            f"Expected 12 Chara antardashas per maha, got {len(entry['antardashas'])}"
        )


def test_chara_return_format():
    """Each Chara maha entry must have keys: sign, planet, start, end, years."""
    pos = {
        "Sun": "Aries", "Moon": "Taurus", "Mars": "Gemini",
        "Mercury": "Cancer", "Jupiter": "Leo", "Venus": "Virgo",
        "Saturn": "Libra", "Rahu": "Scorpio", "Ketu": "Taurus",
    }
    dashas = calculate_chara_dasha("1975-03-21", pos, "Capricorn")

    required_keys = {"sign", "planet", "start", "end", "years"}
    for entry in dashas:
        missing = required_keys - entry.keys()
        assert not missing, f"Chara entry missing keys: {missing}"
    for entry in dashas:
        assert isinstance(entry["planet"], str), "planet must be a string"
        assert isinstance(entry["sign"],   str), "sign must be a string"


# ─────────────────────────────────────────────────────────────────────────────
# Cross-cutting: planet field must use SIGN_LORDS (standard), not Chara substitutes
# ─────────────────────────────────────────────────────────────────────────────

def test_chara_planet_field_uses_standard_sign_lords():
    """
    Acceptance gate: 'planet' field in each Chara entry must equal SIGN_LORDS[sign],
    NOT the Chara substitute lord.  (Scorpio's 'planet' = Mars, not Ketu.)
    """
    from vedic_calculator import SIGN_LORDS
    pos = {
        "Sun": "Leo", "Moon": "Taurus", "Mars": "Aries",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Libra",
        "Saturn": "Capricorn", "Rahu": "Aquarius", "Ketu": "Leo",
    }
    dashas = calculate_chara_dasha("1990-01-01", pos, "Scorpio")

    for entry in dashas:
        expected_planet = SIGN_LORDS[entry["sign"]]
        assert entry["planet"] == expected_planet, (
            f"sign={entry['sign']}: planet must be SIGN_LORDS value '{expected_planet}', "
            f"got '{entry['planet']}'"
        )


def test_kalachakra_planet_field_uses_standard_sign_lords():
    """
    Acceptance gate: 'planet' field in each Kalachakra entry must equal SIGN_LORDS[sign].
    """
    from vedic_calculator import SIGN_LORDS
    moon_lon  = _moon_lon_for_sign_pada("Libra", pada=0)
    lagna_lon = 0.0
    dashas    = calculate_kalachakra_dasha("1990-01-01", moon_lon, lagna_lon)

    for entry in dashas:
        expected_planet = SIGN_LORDS[entry["sign"]]
        assert entry["planet"] == expected_planet, (
            f"sign={entry['sign']}: planet must be '{expected_planet}', "
            f"got '{entry['planet']}'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Sanity: KALACHAKRA_PERIODS totals
# ─────────────────────────────────────────────────────────────────────────────

def test_kalachakra_period_totals():
    """Savya total = 52, Apasavya total = 39, Full = 91."""
    savya_total   = sum(KALACHAKRA_PERIODS[s] for s in KALACHAKRA_SAVYA_SIGNS)
    apasavya_total = sum(KALACHAKRA_PERIODS[s] for s in KALACHAKRA_APASAVYA_SIGNS)

    assert savya_total    == 52,  f"Savya total must be 52, got {savya_total}"
    assert apasavya_total == 39,  f"Apasavya total must be 39, got {apasavya_total}"
    assert _KAL_TOTAL     == 91,  f"Full cycle must be 91, got {_KAL_TOTAL}"


# ─────────────────────────────────────────────────────────────────────────────
# Chara: no knowledge_engine import anywhere in new code
# ─────────────────────────────────────────────────────────────────────────────

def test_no_knowledge_engine_import():
    """Acceptance gate: vedic_calculator must not import knowledge_engine."""
    import importlib, inspect
    vc_module = importlib.import_module("vedic_calculator")
    src = inspect.getsource(vc_module)
    assert "knowledge_engine" not in src, (
        "vedic_calculator.py must NOT import knowledge_engine"
    )
