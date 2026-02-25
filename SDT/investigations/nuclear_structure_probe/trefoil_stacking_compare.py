#!/usr/bin/env python3
"""
Compare trefoil building blocks with nuclear stacking validation nuclei.

Loads trefoil_mappings.json (from SDT/data) and prints (Z,N), building_blocks,
and probe model name for each validation nucleus. Ensures alignment between
trefoil (generate_trefoil_mappings.py) and stacking (02_04, run_nuclear_stacking_validation).
"""

import json
from pathlib import Path

PROBE_ROOT = Path(__file__).resolve().parent
# SDT/data/trefoil_mappings.json from probe root
DATA_PATH = PROBE_ROOT.parent.parent / "data" / "trefoil_mappings.json"

VALIDATION_NUCLEI = [
    (1, 1, "2H", "DeuteronCalibration"),
    (2, 2, "4He", "AlphaParticleStructure"),
    (6, 6, "12C", "Carbon12Structure"),
    (7, 7, "14N", "nitrogen14_occlusion(C12+center)"),
    (8, 8, "16O", "Oxygen16Structure"),
    (4, 4, "8Be", "Beryllium8Structure"),
]


def main():
    if not DATA_PATH.exists():
        print(f"Not found: {DATA_PATH}")
        print("Run generate_trefoil_mappings.py from SDT/Code first.")
        return 1

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        structures = json.load(f)

    by_zn = {(s["Z"], s["N"]): s for s in structures}

    print("Trefoil vs stacking (validation nuclei)")
    print("=" * 70)
    print(f"{'Nucleus':<6} {'Z':>2} {'N':>2}  {'Trefoil building_blocks':<24}  Probe model")
    print("-" * 70)

    for Z, N, label, probe_model in VALIDATION_NUCLEI:
        s = by_zn.get((Z, N))
        blocks = s["building_blocks"] if s else "—"
        print(f"{label:<6} {Z:>2} {N:>2}  {blocks:<24}  {probe_model}")

    print("=" * 70)
    return 0


if __name__ == "__main__":
    exit(main())
