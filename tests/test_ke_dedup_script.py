from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "backend" / "ke_dedup_script.py"


def write_rules(path: Path, rules: list[dict]) -> None:
    path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rules(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_script(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=True,
    )


def test_dedup_script_detects_matches_and_is_idempotent(tmp_path: Path) -> None:
    folder_a = tmp_path / "BPHS_CC_Decode"
    folder_b = tmp_path / "Phaladeepika_CC_Decode"
    folder_a.mkdir()
    folder_b.mkdir()

    rules_a = [
        {
            "rule_id": "A.1",
            "condition": {"type": "house_lord_in_house", "lord_of_house": 8, "placed_in_house": 1},
            "claim_polarity": "positive",
            "full_text": "8th lord in Lagna confers long life.",
            "cross_text_matches": [
                {"rule_id": "outside.keep", "similarity_score": 0.33, "relationship": "partial_overlap"}
            ],
        },
        {
            "rule_id": "A.2",
            "condition": {"type": "planet_in_house", "planet": "mars", "house": 4},
            "claim_polarity": "neutral",
            "full_text": "Mars in the fourth house gives courage.",
            "cross_text_matches": [
                {"rule_id": "outside.keep.2", "similarity_score": 0.22, "relationship": "partial_overlap"}
            ],
        },
    ]
    rules_b = [
        {
            "rule_id": "B.1",
            "condition": {"type": "house_lord_in_house", "lord_of_house": 8, "placed_in_house": 1},
            "claim_polarity": "positive",
            "full_text": "8th lord in Lagna confers long life.",
        },
        {
            "rule_id": "B.2",
            "condition": {"type": "house_lord_in_house", "lord_of_house": 8, "placed_in_house": 1},
            "claim_polarity": "negative",
            "full_text": "8th lord in Lagna shortens life.",
        },
        {
            "rule_id": "B.3",
            "condition": {"type": "house_lord_in_house", "lord_of_house": 8, "placed_in_house": 1},
            "claim_polarity": "mixed",
            "full_text": "8th lord in Lagna can help or harm life.",
        },
        {
            "rule_id": "B.4",
            "condition": {"type": "planet_in_house", "planet": "venus", "house": 7},
            "claim_polarity": "positive",
            "full_text": "Venus in the seventh house supports partnerships.",
        },
    ]

    write_rules(folder_a / "BPHS_Rules_Part1.json", rules_a)
    write_rules(folder_b / "PD_Rules.json", rules_b)

    report_path = tmp_path / "report.json"

    dry_run = run_script(
        [
            "--folder-a",
            str(folder_a),
            "--folder-b",
            str(folder_b),
            "--output-report",
            str(report_path),
            "--dry-run",
        ]
    )
    assert report_path.exists()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["rules_in_a"] == 2
    assert report["rules_in_b"] == 4
    assert report["pairs_evaluated"] == 8
    assert report["duplicate_candidates"] == 1
    assert report["contradiction_pairs"] == 2
    assert report["matches"][0]["relationship"] == "identical_claim"
    assert {item["relationship"] for item in report["contradictions"]} == {"contradicts", "partial_contradiction"}
    assert "Dry run complete" in dry_run.stdout

    before_update_a = read_rules(folder_a / "BPHS_Rules_Part1.json")
    before_update_b = read_rules(folder_b / "PD_Rules.json")

    run_script(
        [
            "--folder-a",
            str(folder_a),
            "--folder-b",
            str(folder_b),
            "--output-report",
            str(report_path),
            "--update-files",
        ]
    )

    first_update_a = read_rules(folder_a / "BPHS_Rules_Part1.json")
    first_update_b = read_rules(folder_b / "PD_Rules.json")

    assert before_update_a[0]["cross_text_matches"] == [{"rule_id": "outside.keep", "similarity_score": 0.33, "relationship": "partial_overlap"}]
    assert before_update_b[0].get("cross_text_matches") is None
    assert {entry["rule_id"] for entry in first_update_a[0]["cross_text_matches"]} == {"B.1", "B.2", "B.3", "outside.keep"}
    assert {entry["rule_id"] for entry in first_update_a[1]["cross_text_matches"]} == {"outside.keep.2"}
    assert {entry["rule_id"] for entry in first_update_b[0]["cross_text_matches"]} == {"A.1"}
    assert {entry["rule_id"] for entry in first_update_b[1]["cross_text_matches"]} == {"A.1"}
    assert {entry["rule_id"] for entry in first_update_b[2]["cross_text_matches"]} == {"A.1"}
    assert first_update_b[3].get("cross_text_matches", []) == []

    run_script(
        [
            "--folder-a",
            str(folder_a),
            "--folder-b",
            str(folder_b),
            "--output-report",
            str(report_path),
            "--update-files",
        ]
    )

    second_update_a = read_rules(folder_a / "BPHS_Rules_Part1.json")
    second_update_b = read_rules(folder_b / "PD_Rules.json")
    assert second_update_a == first_update_a
    assert second_update_b == first_update_b
