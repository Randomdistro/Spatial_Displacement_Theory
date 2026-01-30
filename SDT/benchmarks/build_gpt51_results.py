"""
Generate a consolidated set of benchmark validation reports for the
"24 benchmarks_gpt5.1" package. This script:

1) Copies the freshest validation JSONs into the target folder
2) Computes a max error percentage heuristic for each benchmark
3) Flags whether the benchmark meets the <0.8% verification standard
4) Emits a summary JSON for quick inspection
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = REPO_ROOT / "SDT" / "benchmarks"
COMPOSER_DIR = BENCH_DIR / "Composer"
TARGET_DIR = BENCH_DIR / "24 benchmarks_gpt5.1"

# Prefer the hand-tuned validation scripts in SDT/tools for B01-B16/B20,
# and use the Composer auto-run outputs for B17-B24 (under investigation).
SOURCE_MAP = {
    "B01": BENCH_DIR / "B01_validation_report.json",
    "B02": BENCH_DIR / "B02_validation_report.json",
    "B03": BENCH_DIR / "B03_validation_report.json",
    "B04": BENCH_DIR / "B04_validation_report.json",
    "B05": BENCH_DIR / "B05_validation_report.json",
    "B06": BENCH_DIR / "B06_validation_report.json",
    "B07": BENCH_DIR / "B07_validation_report.json",
    "B08": BENCH_DIR / "B08_validation_report.json",
    "B09": BENCH_DIR / "B09_validation_report.json",
    "B10": BENCH_DIR / "B10_validation_report.json",
    "B11": BENCH_DIR / "B11_validation_report.json",
    "B12": BENCH_DIR / "B12_validation_report.json",
    "B13": BENCH_DIR / "B13_validation_report.json",
    "B14": BENCH_DIR / "B14_validation_report.json",
    "B15": BENCH_DIR / "B15_validation_report.json",
    "B16": BENCH_DIR / "B16_validation_report.json",
    "B17": COMPOSER_DIR / "B17_validation_report.json",
    "B18": COMPOSER_DIR / "B18_validation_report.json",
    "B19": COMPOSER_DIR / "B19_validation_report.json",
    "B20": BENCH_DIR / "B20_validation_report.json",
    "B21": COMPOSER_DIR / "B21_validation_report.json",
    "B22": COMPOSER_DIR / "B22_validation_report.json",
    "B23": COMPOSER_DIR / "B23_validation_report.json",
    "B24": COMPOSER_DIR / "B24_validation_report.json",
}


def collect_error_percentages(obj: Any, found: List[float]) -> None:
    """
    Recursively collect numeric error percentage fields.
    Only keys containing 'percent' or 'pct' are treated as percentages to
    avoid pulling raw error magnitudes (e.g., MHz, eV).
    """
    if isinstance(obj, dict):
        for key, val in obj.items():
            key_lower = key.lower()
            if isinstance(val, (int, float)):
                if "percent" in key_lower or "pct" in key_lower or "%" in key_lower:
                    found.append(float(val))
                elif "error" in key_lower and 0 <= float(val) <= 1:
                    # Treat small, unitless errors as percentages when labels are missing
                    found.append(float(val) * 100)
            else:
                collect_error_percentages(val, found)
    elif isinstance(obj, list):
        for item in obj:
            collect_error_percentages(item, found)


def compute_max_error_percent(data: Dict[str, Any]) -> Optional[float]:
    """Best-effort extraction of the max percentage error from a report."""
    candidates: List[float] = []
    collect_error_percentages(data, candidates)
    if not candidates:
        return None
    return max(candidates)


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    summary: List[Dict[str, Any]] = []

    for benchmark_id, source_path in SOURCE_MAP.items():
        entry: Dict[str, Any] = {"benchmark": benchmark_id, "source": str(source_path)}

        if not source_path.exists():
            entry.update(
                {
                    "status": "MISSING",
                    "max_error_percent": None,
                    "pass_lt_0.8": False,
                    "note": "Source validation report not found",
                }
            )
            summary.append(entry)
            continue

        with source_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        # Write a copy into the target folder
        target_file = TARGET_DIR / f"{benchmark_id}_validation_report.json"
        with target_file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

        max_error = compute_max_error_percent(data)
        status = data.get("overall_status") or data.get("status") or "UNKNOWN"
        pass_lt_0_8 = max_error is not None and max_error < 0.8

        entry.update(
            {
                "status": status,
                "max_error_percent": max_error,
                "pass_lt_0.8": pass_lt_0_8,
            }
        )
        summary.append(entry)

    summary_path = TARGET_DIR / "benchmark_summary_gpt51.json"
    with summary_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print(f"Saved {len(summary)} reports to {TARGET_DIR}")
    pass_count = sum(1 for s in summary if s.get("pass_lt_0_8"))
    print(f"Benchmarks passing <0.8% error: {pass_count}/24")


if __name__ == "__main__":
    main()
