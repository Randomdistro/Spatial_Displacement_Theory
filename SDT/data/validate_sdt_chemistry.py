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

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from sdt_chemistry_predictor import predict_atomic


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


def main():
    cases = list(iter_atomicus_I1_cases())
    if not cases:
        raise SystemExit(f"No I1 cases found under {ATOMICUS_DIR}")

    print(f"Found {len(cases)} ATOMICUS I1 cases.")
    worst = None
    ok = 0

    for c in cases:
        pred = predict_atomic(c.Z, c.N)
        pred_I1 = pred.I1_eV

        if not math.isfinite(pred_I1) or pred_I1 == 0.0:
            rel = math.inf
        else:
            rel = abs(pred_I1 - c.exp_I1_eV) / c.exp_I1_eV

        if worst is None or rel > worst[0]:
            worst = (rel, c, pred_I1)

        exact = (abs(pred_I1 - c.exp_I1_eV) == 0.0)
        ok += 1 if exact else 0

        print(
            f"{c.symbol}-{c.Z + c.N:>3}  exp={c.exp_I1_eV:>9.3f} eV  pred={pred_I1:>12.6g} eV  rel_err={'inf' if rel==math.inf else f'{rel*100:8.3f}%'}  file={c.path.name}"
        )

    print("\nSummary:")
    print(f"  exact_matches: {ok}/{len(cases)}")
    if worst is not None:
        rel, c, pred_I1 = worst
        print(
            f"  worst_case: {c.symbol}-{c.Z + c.N} exp={c.exp_I1_eV} eV pred={pred_I1} eV rel_err={'inf' if rel==math.inf else rel}"
        )


if __name__ == "__main__":
    main()


