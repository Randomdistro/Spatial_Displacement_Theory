#!/usr/bin/env python3
"""
SDT 3D Particle CMB Model — CLI Runner

Entry point for running simulations and batch tests.
"""

import argparse
import json
import sys
import numpy as np

from .simulation import Simulation, SimulationResult
from .batch_runner import (
    quick_sweep_toggles,
    pairing_comparison,
    nuclear_arrangements,
    run_batch,
    make_arrangement_grid,
    setup_single_proton,
    setup_deuteron,
    run_isotope_sweep,
    run_all_isotopes_element,
)
from .arrangements import ArrangementConfig


def _serialize_result(r: SimulationResult) -> dict:
    """Convert result to JSON-serializable dict."""
    return {
        "config_hash": r.config_hash,
        "pressure_centroid": float(r.pressure_centroid),
        "total_occlusion": float(r.total_occlusion),
        "energy_rate_proton": float(r.energy_rate_proton),
        "pairing_matrix_sum": float(r.pairing_matrix_sum),
        "metadata": r.metadata,
    }


def main():
    parser = argparse.ArgumentParser(
        description="SDT 3D Particle CMB Model — run simulations and batch tests"
    )
    sub = parser.add_subparsers(dest="cmd", help="Command")

    # Single run
    p_single = sub.add_parser("single", help="Single simulation")
    p_single.add_argument("--cmb", type=str, default="12")
    p_single.add_argument("--trefoil", action="store_true", default=True)
    p_single.add_argument("--no-trefoil", action="store_false", dest="trefoil")
    p_single.add_argument("--pairing", action="store_true", default=True)
    p_single.add_argument("--no-pairing", action="store_false", dest="pairing")
    p_single.add_argument("--setup", choices=["proton", "deuteron", "alpha"], default="proton")

    # Batch
    p_batch = sub.add_parser("batch", help="Batch run")
    p_batch.add_argument("--mode", choices=["toggles", "pairing", "nuclear", "isotopes"], default="toggles")
    p_batch.add_argument("--cmb", type=str, default="12")
    p_batch.add_argument("--json", action="store_true", help="Output JSON")
    p_batch.add_argument("--element", type=int, help="For isotopes mode: run all isotopes of element Z (1-50)")

    # Isotope single
    p_iso = sub.add_parser("isotope", help="Single isotope (Z, A)")
    p_iso.add_argument("Z", type=int, help="Atomic number")
    p_iso.add_argument("A", type=int, help="Mass number")
    p_iso.add_argument("--cmb", type=str, default="12")

    args = parser.parse_args()

    if args.cmd == "single":
        config = ArrangementConfig(
            trefoil_enabled=args.trefoil,
            pairing_enabled=args.pairing,
        )
        sim = Simulation(cmb_resolution=args.cmb)
        sim.arrangement = config
        if args.setup == "proton":
            sim.add_proton(np.zeros(3))
        elif args.setup == "deuteron":
            sim.add_proton(np.zeros(3), chirality="R")
            sim.add_neutron(np.array([1.942e-15, 0, 0]), chirality="L")
        elif args.setup == "alpha":
            d = 1.5e-15
            sim.add_proton(np.zeros(3), chirality="R")
            sim.add_proton(np.array([d, 0, 0]), chirality="L")
            sim.add_neutron(np.array([d/2, d * 0.866, 0]), chirality="L")
            sim.add_neutron(np.array([d/2, d * 0.289, d * 0.82]), chirality="R")
        res = sim.run()
        print(json.dumps(_serialize_result(res), indent=2))

    elif args.cmd == "isotope":
        sim = Simulation(cmb_resolution=args.cmb)
        sim.add_nucleus(args.Z, args.A)
        res = sim.run()
        res.metadata["Z"] = args.Z
        res.metadata["A"] = args.A
        print(json.dumps(_serialize_result(res), indent=2))

    elif args.cmd == "batch":
        if args.mode == "toggles":
            results = quick_sweep_toggles(args.cmb)
        elif args.mode == "pairing":
            results = pairing_comparison(args.cmb)
        elif args.mode == "nuclear":
            results = nuclear_arrangements(args.cmb)
        elif args.mode == "isotopes":
            if args.element is not None:
                results = run_all_isotopes_element(args.element, args.cmb)
            else:
                # Run all isotopes for C (6), Fe (26), Sn (50) as sample
                results = []
                for Z in [6, 26, 50]:
                    results.extend(run_all_isotopes_element(Z, args.cmb))

        if args.json:
            out = [_serialize_result(r) for r in results]
            print(json.dumps(out, indent=2))
        else:
            for i, r in enumerate(results):
                iso = f"Z={r.metadata.get('Z','?')} A={r.metadata.get('A','?')}" if "Z" in r.metadata else ""
                extra = f" | {iso}" if iso else ""
                print(f"[{i}] {r.config_hash} | P={r.pressure_centroid:.4e} | "
                      f"D_dot={r.energy_rate_proton:.4e} | pair={r.pairing_matrix_sum:.2f}{extra}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
