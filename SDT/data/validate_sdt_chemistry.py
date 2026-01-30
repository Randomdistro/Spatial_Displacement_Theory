#!/usr/bin/env python3
"""
Dataset-driven validation for SDT chemistry predictions.

Current validation implemented:
  - First ionization energy E_i1 from ATOMICUS chapters (treated as experimental reference values)

This is intentionally strict:
  - Reports absolute/relative error
  - Flags any non-finite/degenerate predictions
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from sdt_chemistry_predictor import E_CHARGE, get_calibration_constant, predict_atomic
from sdt_occlusion_factors import R_E_POINT


ATOMICUS_DIR = Path(__file__).resolve().parents[1] / "ATOMICUS"


@dataclass(frozen=True)
class I1Case:
    path: Path
    Z: int
    N: int
    symbol: str
    exp_I1_eV: float


ION1_RE = re.compile(
    r"Ionization\s+Energy\s*\([^)]*E_\{?i1\}?\$?\)\s*:\s*\*{0,2}\s*([0-9]+(?:\.[0-9]+)?)\s*eV",
    re.IGNORECASE,
)
FILENAME_RE = re.compile(r"^\d+_([A-Za-z]+)_([A-Za-z]+)_(\d+)(?:_(\d+))?\.md$")


def _parse_ZN_from_filename(path: Path) -> Optional[tuple[int, int, str]]:
    m = FILENAME_RE.match(path.name)
    if not m:
        return None
    _name, symbol, Z_s, N_s = m.group(1), m.group(2), m.group(3), m.group(4)
    Z = int(Z_s)
    N = int(N_s) if N_s is not None else Z  # some files omit N; fall back to N=Z
    return Z, N, symbol


def iter_atomicus_I1_cases() -> Iterable[I1Case]:
    for path in sorted(ATOMICUS_DIR.glob("*.md")):
        parsed = _parse_ZN_from_filename(path)
        if not parsed:
            continue
        Z, N, symbol = parsed

        text = path.read_text(encoding="utf-8", errors="replace")
        m = ION1_RE.search(text)
        if not m:
            continue
        exp_I1_eV = float(m.group(1))
        yield I1Case(path=path, Z=Z, N=N, symbol=symbol, exp_I1_eV=exp_I1_eV)


def validate_I1(pressure_model: str, reverse: bool = False) -> tuple[int, float, I1Case, float]:
    """
    Run I1 validation for a given pressure model.
    Returns (exact_count, worst_rel, worst_case, worst_pred).
    When reverse=True, also prints the effective pressure required to match each experimental I1.
    """

    cases = list(iter_atomicus_I1_cases())
    if not cases:
        raise SystemExit(f"No I1 cases found under {ATOMICUS_DIR}")

    print(f"\n=== Pressure model: {pressure_model} ===")
    print(f"Found {len(cases)} ATOMICUS I1 cases.")
    worst = None
    ok = 0
    K_cal = get_calibration_constant(pressure_model)

    for c in cases:
        pred = predict_atomic(c.Z, c.N, pressure_model=pressure_model)
        pred_I1 = pred.I1_eV

        if not math.isfinite(pred_I1) or pred_I1 == 0.0:
            rel = math.inf
        else:
            rel = abs(pred_I1 - c.exp_I1_eV) / c.exp_I1_eV

        if worst is None or rel > worst[0]:
            worst = (rel, c, pred_I1)

        exact = (abs(pred_I1 - c.exp_I1_eV) == 0.0)
        ok += 1 if exact else 0

        line = f"{c.symbol}-{c.Z + c.N:>3}  exp={c.exp_I1_eV:>9.3f} eV  pred={pred_I1:>12.6g} eV  rel_err={'inf' if rel==math.inf else f'{rel*100:8.3f}%'}  file={c.path.name}"
        if reverse:
            # Required effective pressure to make I1 exact with current geometric inputs and calibration
            Z_eff_ion = c.Z * pred.Xi_ion
            I1_exp_J = c.exp_I1_eV * E_CHARGE
            P_req = (4.0 / math.pi) * I1_exp_J * pred.r_atomic_m / (K_cal * (pred.R_N ** 2) * (R_E_POINT ** 2) * Z_eff_ion)
            line += f"  P_req={P_req:.3e} Pa"
        print(line)

    print("\nSummary:")
    print(f"  exact_matches: {ok}/{len(cases)}")
    if worst is not None:
        rel, c, pred_I1 = worst
        print(
            f"  worst_case: {c.symbol}-{c.Z + c.N} exp={c.exp_I1_eV} eV pred={pred_I1} eV rel_err={'inf' if rel==math.inf else rel}"
        )

    return ok, worst[0] if worst else math.inf, worst[1] if worst else None, worst[2] if worst else math.nan


def main():
    parser = argparse.ArgumentParser(description="Validate SDT chemistry predictions against ATOMICUS.")
    parser.add_argument(
        "--pressure-model",
        choices=["planck", "cosmic", "both"],
        default="planck",
        help="Pressure focusing model to use.",
    )
    parser.add_argument(
        "--reverse-calibration",
        action="store_true",
        help="Compute per-element effective pressure required to match experimental I1.",
    )
    args = parser.parse_args()

    if args.pressure_model == "both":
        results = []
        for model in ("planck", "cosmic"):
            res = validate_I1(model, reverse=args.reverse_calibration)
            results.append((model, res))
        # Pick better model by worst-case relative error
        best = min(results, key=lambda x: x[1][1])
        print(f"\nBest model by worst-case relative error: {best[0]}")
    else:
        validate_I1(args.pressure_model, reverse=args.reverse_calibration)


if __name__ == "__main__":
    main()


