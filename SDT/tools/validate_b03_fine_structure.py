"""
B03: Fine Structure Validation

Recomputes hydrogenic 2P fine structure splittings (n=2, ℓ=1) for H, He⁺, and Li²⁺
and validates them against NIST vacuum spectroscopy data.
Tolerance: <0.1% across all cases.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

# Ensure local tools package (sdt_atomic) is importable
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))

from sdt_atomic.fine_structure import fine_structure_splitting  # type: ignore

EV_TO_GHZ = 241_798.9242  # GHz per eV


@dataclass
class FineStructureDatum:
    ion: str
    Z: int
    n: int
    l: int
    observed_GHz: float
    reference: str


FINE_STRUCTURE_DATA: List[FineStructureDatum] = [
    FineStructureDatum("H", 1, 2, 1, 10.950, "NIST ASD (2P1/2-2P3/2)"),
    FineStructureDatum("He⁺", 2, 2, 1, 175.30, "NIST ASD (He II 2P splitting)"),
    FineStructureDatum("Li²⁺", 3, 2, 1, 887.40, "NIST ASD (Li III 2P splitting)"),
]


def validate_fine_structure() -> Dict[str, object]:
    """Compute SDT predictions and compare to experimental splittings."""
    results: List[Dict[str, object]] = []
    max_error = 0.0

    for datum in FINE_STRUCTURE_DATA:
        delta_eV = fine_structure_splitting(datum.n, datum.l, datum.Z)
        predicted_GHz = delta_eV * EV_TO_GHZ
        predicted_THz = predicted_GHz / 1000.0
        observed_THz = datum.observed_GHz / 1000.0
        error_pct = abs(predicted_GHz - datum.observed_GHz) / datum.observed_GHz * 100.0
        max_error = max(max_error, error_pct)

        results.append(
            {
                "ion": datum.ion,
                "Z": datum.Z,
                "n": datum.n,
                "l": datum.l,
                "observed_GHz": datum.observed_GHz,
                "observed_THz": observed_THz,
                "predicted_GHz": predicted_GHz,
                "predicted_THz": predicted_THz,
                "delta_eV": delta_eV,
                "error_percent": error_pct,
                "reference": datum.reference,
            }
        )

    certified = max_error < 0.1

    return {
        "benchmark": "B03",
        "name": "Fine Structure",
        "phase_document": "Phase_3_Fine_structure.md",
        "tolerance": "<0.1%",
        "overall_status": "CERTIFIED" if certified else "FAILED",
        "max_error_percent": max_error,
        "splitting_results": results,
    }


def save_report(summary: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def main() -> None:
    summary = validate_fine_structure()
    report_path = SCRIPT_DIR.parent / "benchmarks" / "B03_validation_report.json"
    save_report(summary, report_path)

    print("=" * 60)
    print("B03: Fine Structure Validation")
    print("=" * 60)
    print(f"Overall status : {summary['overall_status']}")
    print(f"Max error (%)  : {summary['max_error_percent']:.4f}")
    print(f"Report saved   : {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()


