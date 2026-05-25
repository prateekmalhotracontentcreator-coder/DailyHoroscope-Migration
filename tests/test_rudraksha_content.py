from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from rudraksha_content import (  # noqa: E402
    PLANET_RUDRAKSHA_DATA,
    PROBLEM_RUDRAKSHA_DATA,
    SIGN_RUDRAKSHA_DATA,
)


def test_rudraksha_expansion_counts_match_brief() -> None:
    assert len(PLANET_RUDRAKSHA_DATA) == 9
    assert len(PROBLEM_RUDRAKSHA_DATA) == 20
    assert len(SIGN_RUDRAKSHA_DATA) == 12
    assert 2 + 21 + len(PLANET_RUDRAKSHA_DATA) + len(PROBLEM_RUDRAKSHA_DATA) + len(SIGN_RUDRAKSHA_DATA) == 64


def test_planet_primary_mukhi_mapping_matches_brief() -> None:
    expected = {
        "sun": 1,
        "moon": 2,
        "mars": 3,
        "mercury": 4,
        "jupiter": 5,
        "venus": 6,
        "saturn": 7,
        "rahu": 8,
        "ketu": 9,
    }

    observed = {
        slug: payload["primary_mukhi"]["mukhi"]
        for slug, payload in PLANET_RUDRAKSHA_DATA.items()
    }

    assert observed == expected


def test_problem_and_sign_pages_keep_expected_recommendation_links() -> None:
    business_success = PROBLEM_RUDRAKSHA_DATA["business-success"]
    support_numbers = {item["mukhi"] for item in business_success["supporting_mukhis"]}
    assert business_success["primary_mukhi"]["mukhi"] == 7
    assert {8, 11}.issubset(support_numbers)

    aries = SIGN_RUDRAKSHA_DATA["aries"]
    assert aries["primary_mukhi"]["mukhi"] == 3
    assert aries["secondary_mukhi"]["mukhi"] == 5
