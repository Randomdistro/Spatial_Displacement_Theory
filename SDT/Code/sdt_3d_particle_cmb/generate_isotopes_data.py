#!/usr/bin/env python3
"""
Generate isotopes_data.json from periodictable (AME2020 data).
Run: python generate_isotopes_data.py
Requires: pip install periodictable
"""

import json
from pathlib import Path

def main():
    try:
        import periodictable as pt
    except ImportError:
        print("periodictable not installed. Run: pip install periodictable")
        return 1

    out = []
    for Z in range(1, 51):
        el = pt.elements[Z]
        sym = el.symbol
        for A in el.isotopes:
            N = A - Z
            if N < 0:
                continue
            try:
                mass = pt.mass.mass(el[A])
            except Exception:
                mass = float(A)
            try:
                ab = pt.mass.abundance(el[A])
                stable = ab is not None and ab > 0
            except Exception:
                stable = False
            out.append({
                "Z": Z, "A": A, "N": N, "symbol": sym,
                "mass": float(mass), "stable": stable
            })

    out.sort(key=lambda x: (x["Z"], x["A"]))
    path = Path(__file__).parent / "isotopes_data.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=0)
    print(f"Written {len(out)} isotopes to {path}")
    return 0

if __name__ == "__main__":
    exit(main())
