from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from angel_numbers_data import (
    INTENT_ORDER,
    build_hub_payload,
    get_core_numbers,
    get_core_record,
    get_intent_record,
    get_sitemap_page,
    sitemap_page_count,
)


def test_core_number_scope_is_exactly_1000() -> None:
    numbers = get_core_numbers()
    assert len(numbers) == 1000
    assert len(set(numbers)) == 1000
    assert numbers[0] == "1"
    assert numbers[-1] == "10000"
    assert "7777" in numbers
    assert "8888" in numbers
    assert "9999" in numbers


def test_hub_counts_match_contract() -> None:
    counts = build_hub_payload()["counts"]
    assert counts == {"core_numbers": 1000, "intent_pages": 9000, "total_pages": 10001}


def test_core_record_contains_all_intent_summaries() -> None:
    record = get_core_record("111")
    assert len(record["intent_summaries"]) == len(INTENT_ORDER)
    assert record["numerology_base"] == "3"


def test_intent_record_contains_cross_navigation() -> None:
    record = get_intent_record("111", "love")
    assert record["intent"] == "love"
    assert len(record["all_intents"]) == len(INTENT_ORDER)
    assert len(record["related_numbers"]) == 3


def test_sitemap_pagination_matches_full_url_count() -> None:
    assert sitemap_page_count() == 11
    first_page = get_sitemap_page(1)
    last_page = get_sitemap_page(11)
    assert len(first_page["urls"]) == 1000
    assert len(last_page["urls"]) == 1
