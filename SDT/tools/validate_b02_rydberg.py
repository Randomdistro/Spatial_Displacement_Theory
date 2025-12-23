"""
B02: Rydberg Formula Validation

Validates SDT helical standing-wave prediction (Rydberg relationship) against
vacuum spectral line measurements for hydrogenic systems.
Tolerance: <0.01% for all tested transitions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (CODATA 2018)
# ---------------------------------------------------------------------------

R_INF = 10973731.56816021  # Rydberg constant for infinite nuclear mass (1/m)
M_E = 9.1093837015e-31  # Electron mass (kg)
M_P = 1.67262192369e-27  # Proton mass (kg)
M_HE4 = 6.6446573357e-27  # Helium-4 nucleus mass (kg)
M_LI7 = 1.164387e-26  # Lithium-7 nucleus mass (kg) (approximate, electrons removed)


@dataclass
class SpectralLine:
    """Container for an individual spectral transition."""

    name: str
    n_initial: int
    n_final: int
    wavelength_nm: float  # Experimental vacuum wavelength
    Z: int = 1
    nucleus_mass: float = M_P


class RydbergValidator:
    """Validates Rydberg relationship against spectral data."""

    def __init__(self, lines: List[SpectralLine]):
        self.lines = lines

    @staticmethod
    def reduced_mass_factor(nucleus_mass: float) -> float:
        """Return μ/m_e for a hydrogenic ion."""
        mu = (M_E * nucleus_mass) / (M_E + nucleus_mass)
        return mu / M_E

    def predict_wavelength(self, line: SpectralLine) -> float:
        """Predict wavelength from SDT Rydberg formulation."""
        if line.n_initial <= line.n_final:
            raise ValueError("Emission requires n_initial > n_final")

        delta = (1.0 / line.n_final**2) - (1.0 / line.n_initial**2)
        r_effective = R_INF * self.reduced_mass_factor(line.nucleus_mass)
        inv_lambda = r_effective * (line.Z**2) * delta
        return 1e9 / inv_lambda  # meters -> nm

    def extract_rydberg(self, line: SpectralLine) -> float:
        """Estimate effective R constant from the measured wavelength."""
        delta = (1.0 / line.n_final**2) - (1.0 / line.n_initial**2)
        lambda_m = line.wavelength_nm * 1e-9
        return (1.0 / lambda_m) / (line.Z**2 * delta)

    def validate(self) -> Dict[str, object]:
        """Validate all lines and produce a structured summary."""
        results = []
        max_error_pct = 0.0
        ridberg_diffs = []

        for line in self.lines:
            lambda_pred = self.predict_wavelength(line)
            err_nm = lambda_pred - line.wavelength_nm
            err_pct = abs(err_nm / line.wavelength_nm) * 100.0
            max_error_pct = max(max_error_pct, err_pct)

            r_measured = self.extract_rydberg(line)
            r_expected = R_INF * self.reduced_mass_factor(line.nucleus_mass)
            ridberg_diffs.append(r_measured - r_expected)

            results.append(
                {
                    "transition": line.name,
                    "n_initial": line.n_initial,
                    "n_final": line.n_final,
                    "Z": line.Z,
                    "lambda_exp_nm": line.wavelength_nm,
                    "lambda_sdt_nm": lambda_pred,
                    "error_nm": err_nm,
                    "error_pct": err_pct,
                    "R_measured": r_measured,
                    "R_expected": r_expected,
                }
            )

        r_stats = {
            "mean_diff": float(np.mean(ridberg_diffs)),
            "std_diff": float(np.std(ridberg_diffs)),
            "max_abs_diff": float(np.max(np.abs(ridberg_diffs))),
        }

        certified = max_error_pct < 0.01

        return {
            "benchmark": "B02",
            "name": "Rydberg Formula",
            "phase_document": "Phase_2_Rydberg_Spectrum_from_Helical_Standing_Waves",
            "tolerance": "<0.01%",
            "overall_status": "CERTIFIED" if certified else "FAILED",
            "max_error_pct": max_error_pct,
            "spectral_results": results,
            "rydberg_statistics": r_stats,
        }


def load_lines() -> List[SpectralLine]:
    """Return curated vacuum spectral lines for hydrogenic ions."""
    return [
        SpectralLine("H Lyman-α", 2, 1, 121.56701, Z=1, nucleus_mass=M_P),
        SpectralLine("H Lyman-β", 3, 1, 102.57220, Z=1, nucleus_mass=M_P),
        SpectralLine("H Lyman-γ", 4, 1, 97.25370, Z=1, nucleus_mass=M_P),
        SpectralLine("H Balmer-α", 3, 2, 656.46100, Z=1, nucleus_mass=M_P),
        SpectralLine("H Balmer-β", 4, 2, 486.27120, Z=1, nucleus_mass=M_P),
        SpectralLine("H Balmer-γ", 5, 2, 434.17360, Z=1, nucleus_mass=M_P),
        SpectralLine("H Paschen-α", 4, 3, 1875.62745, Z=1, nucleus_mass=M_P),
        SpectralLine("He II Lyman-α", 2, 1, 30.37822, Z=2, nucleus_mass=M_HE4),
        SpectralLine("Li III Lyman-α", 2, 1, 13.50010, Z=3, nucleus_mass=M_LI7),
    ]


def save_report(summary: Dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def main():
    lines = load_lines()
    validator = RydbergValidator(lines)
    summary = validator.validate()

    report_path = Path(__file__).parent.parent / "benchmarks" / "B02_validation_report.json"
    save_report(summary, report_path)

    print("=" * 60)
    print("B02: Rydberg Formula Validation")
    print("=" * 60)
    print(f"Overall status : {summary['overall_status']}")
    print(f"Max error (%)  : {summary['max_error_pct']:.6f}")
    print("Spectral lines : {}".format(len(summary["spectral_results"])))
    print("Rydberg mean Δ : {:.3e}".format(summary["rydberg_statistics"]["mean_diff"]))
    print("Report saved   :", report_path)
    print("=" * 60)


if __name__ == "__main__":
    main()


