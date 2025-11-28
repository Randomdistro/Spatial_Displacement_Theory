"""
SDT P vs NP Investigation Harness
---------------------------------

This script maps a small 3-SAT instance onto the SDT-Navier field solver to
highlight the verification/discovery asymmetry described in the Millennium plan.

Workflow
~~~~~~~~
1. Build a 1-D SDT lattice where each literal in the 3-SAT formula is represented
   by a turbine site (curvature + circulation seed).
2. Encode a Boolean assignment by setting the local slip value η for each literal
   site (low slip = literal asserted, high slip = literal suppressed).
3. Run the SDT-Navier solver for a fixed number of steps and evaluate clause
   satisfaction using the evolved slip field.
4. Compare:
   - Verification: single run with a known satisfying assignment (local, fast).
   - Discovery: repeated random assignments until a satisfying configuration is
     found (global search, potentially exponential).

All physics parameters come directly from the SDT codebase (CMB pressure,
master-equation-derived energy density, SDT force functionals).
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Repository path setup
# ---------------------------------------------------------------------------

CURRENT_FILE = Path(__file__).resolve()
SDT_DIR = CURRENT_FILE.parents[4]  # .../SDT
CODE_DIR = SDT_DIR / "Code"
if str(CODE_DIR) not in sys.path:
    sys.path.append(str(CODE_DIR))

from sdt_navier.fields import (  # type: ignore  # noqa: E402
    FieldSystem,
    add_turbine_source,
    compute_diversion_density,
    initialize_fields,
)
from sdt_navier.equations import SDTNavierEquations  # type: ignore  # noqa: E402
from sdt_navier.solver import SDTNavierSolver  # type: ignore  # noqa: E402


# ---------------------------------------------------------------------------
# Problem definition (3-SAT instance) and helper dataclasses
# ---------------------------------------------------------------------------

FORMULA: List[Tuple[int, int, int]] = [
    (1, -2, 3),
    (-1, 2, 4),
    (2, -3, -4),
    (-1, -2, -5),
    (3, 4, 5),
]
NUM_VARS = 5
KNOWN_ASSIGNMENT: Dict[int, bool] = {
    1: True,
    2: True,
    3: True,
    4: False,
    5: False,
}

PCMB = 2.036e-2  # Pa, universal pressure from SDT Phase 0/1
TAU_CHAR = 8.4e-16 / 2.998e8  # s, proton response time for energy density


@dataclass
class LiteralSite:
    """Metadata for each literal location on the SDT lattice."""

    clause_id: int
    literal: int
    index: Tuple[int, int, int]


# ---------------------------------------------------------------------------
# Field construction and mapping utilities
# ---------------------------------------------------------------------------

def build_formula_environment(
    formula: Sequence[Sequence[int]],
    dx: float = 1.0,
) -> Tuple[FieldSystem, List[LiteralSite]]:
    """
    Initialize an SDT field system and embed turbine sites for each literal.
    """
    nx = len(formula) * 4 + 2  # leave spacer cells between clauses
    fields = initialize_fields(
        nx=nx,
        ny=1,
        nz=1,
        dx=dx,
        P_infinity=PCMB,
    )

    literal_sites: List[LiteralSite] = []
    for clause_id, clause in enumerate(formula):
        for literal_idx, literal in enumerate(clause):
            cell_i = 1 + clause_id * 4 + literal_idx
            add_turbine_source(
                fields,
                position=(cell_i, 0, 0),
                radius_cells=0.55,
                kappa_value=5.0e5,
                Gamma_value=0.08,
                eta_value=0.5,
                profile="gaussian",
            )
            literal_sites.append(
                LiteralSite(
                    clause_id=clause_id,
                    literal=literal,
                    index=(cell_i, 0, 0),
                )
            )

    recompute_energy_density(fields)
    return fields, literal_sites


def recompute_energy_density(fields: FieldSystem) -> None:
    """Update energy density using the master-equation relation."""
    sigma = compute_diversion_density(fields)
    fields.e = fields.P * sigma * TAU_CHAR


def literal_truth(literal: int, assignment: Dict[int, bool]) -> bool:
    """Evaluate whether a literal is True under the given assignment."""
    var = abs(literal)
    value = assignment[var]
    return value if literal > 0 else (not value)


def apply_assignment_to_fields(
    fields: FieldSystem,
    literal_sites: Sequence[LiteralSite],
    assignment: Dict[int, bool],
    satisfied_slip: float = 0.02,
    unsatisfied_slip: float = 0.82,
) -> None:
    """
    Encode a Boolean assignment into the slip field η.

    Low slip (near traction) represents a literal that is asserted; high slip
    represents a suppressed literal.
    """
    for site in literal_sites:
        target_eta = (
            satisfied_slip if literal_truth(site.literal, assignment) else unsatisfied_slip
        )
        fields.eta[site.index] = target_eta

    recompute_energy_density(fields)


def clause_slip_statistics(
    fields: FieldSystem,
    literal_sites: Sequence[LiteralSite],
) -> Dict[int, Dict[str, float]]:
    """Compute per-clause slip summaries."""
    slips: Dict[int, List[float]] = defaultdict(list)
    for site in literal_sites:
        slips[site.clause_id].append(float(fields.eta[site.index]))

    stats: Dict[int, Dict[str, float]] = {}
    for clause_id, values in slips.items():
        stats[clause_id] = {
            "min_eta": float(np.min(values)),
            "max_eta": float(np.max(values)),
            "mean_eta": float(np.mean(values)),
        }
    return stats


def clauses_satisfied(
    fields: FieldSystem,
    literal_sites: Sequence[LiteralSite],
    slip_threshold: float = 0.2,
) -> bool:
    """Check clause satisfaction using the evolved slip values."""
    per_clause = clause_slip_statistics(fields, literal_sites)
    return all(stats["min_eta"] < slip_threshold for stats in per_clause.values())


# ---------------------------------------------------------------------------
# Simulation routines
# ---------------------------------------------------------------------------

def simulate_assignment(
    assignment: Dict[int, bool],
    solver_steps: int = 25,
    method: str = "euler",
) -> Dict[str, object]:
    """Run the SDT-Navier solver for a specific Boolean assignment."""
    fields, literal_sites = build_formula_environment(FORMULA)
    apply_assignment_to_fields(fields, literal_sites, assignment)

    equations = SDTNavierEquations(
        rho_s=5.2e96,
        alpha_curv=5.0e-9,
        beta_slip=2.5e14,
        gamma_create=1.0e-25,
        delta_destroy=5.0e-10,
        epsilon_strain=1.0e-25,
        zeta_heal=5.0e-10,
    )
    solver = SDTNavierSolver(
        fields=fields,
        equations=equations,
        dt=None,
        cfl=0.8,
        method=method,
        enforce_incompressibility=True,
    )

    history = []
    for step in range(solver_steps):
        solver.step()
        history.append(
            {
                "step": step + 1,
                "divergence": float(solver.get_divergence_error()),
                "mean_eta": float(np.mean(fields.eta)),
                "mean_energy": float(np.mean(fields.e)),
            }
        )

    sat = clauses_satisfied(fields, literal_sites)
    stats = clause_slip_statistics(fields, literal_sites)
    return {
        "assignment": assignment,
        "clauses_satisfied": sat,
        "steps": solver_steps,
        "history": history,
        "final_divergence": history[-1]["divergence"],
        "final_mean_energy": history[-1]["mean_energy"],
        "clause_slip_stats": stats,
    }


def random_assignment(num_vars: int) -> Dict[int, bool]:
    """Generate a random Boolean assignment."""
    return {var: bool(random.getrandbits(1)) for var in range(1, num_vars + 1)}


def run_discovery(max_attempts: int = 128) -> Dict[str, object]:
    """Attempt to find a satisfying assignment by random search."""
    attempts: List[Dict[str, object]] = []
    t0 = time.perf_counter()
    for attempt in range(1, max_attempts + 1):
        guess = random_assignment(NUM_VARS)
        metrics = simulate_assignment(guess)
        metrics["attempt"] = attempt
        attempts.append(metrics)
        if metrics["clauses_satisfied"]:
            dt = time.perf_counter() - t0
            return {
                "success": True,
                "attempts": attempt,
                "elapsed_seconds": dt,
                "final_metrics": metrics,
                "attempt_history": attempts,
            }
    dt = time.perf_counter() - t0
    return {
        "success": False,
        "attempts": max_attempts,
        "elapsed_seconds": dt,
        "attempt_history": attempts,
    }


# ---------------------------------------------------------------------------
# Result logging
# ---------------------------------------------------------------------------

def write_results(output_dir: Path, data: Dict[str, object]) -> Path:
    """Persist experiment data to a timestamped JSON + Markdown summary."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"p_vs_np_experiment_{timestamp}.json"
    md_path = output_dir / f"p_vs_np_experiment_{timestamp}.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    verification = data["verification_results"]  # type: ignore[index]
    discovery = data["discovery_results"]  # type: ignore[index]

    def clause_table(stats: Dict[str, Dict[str, float]]) -> str:
        header = "| Clause | min η | mean η | max η |\n|---|---|---|---|"
        rows = []
        for cid, values in stats.items():
            rows.append(
                f"| {cid} | {values['min_eta']:.3f} | {values['mean_eta']:.3f} | {values['max_eta']:.3f} |"
            )
        return "\n".join([header] + rows)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# SDT P vs NP Experiment\n\n")
        f.write(f"- Timestamp (UTC): {timestamp}\n")
        f.write(f"- Formula (3-SAT): {FORMULA}\n\n")
        f.write("## Verification Run\n")
        f.write(f"- Clauses satisfied: {verification['clauses_satisfied']}\n")
        f.write(f"- Steps: {verification['steps']}\n")
        f.write(f"- Final divergence: {verification['final_divergence']:.3e}\n")
        f.write(f"- Final mean energy: {verification['final_mean_energy']:.3e} J/m³\n")
        f.write("### Clause Slip Statistics\n")
        f.write(clause_table({str(k): v for k, v in verification["clause_slip_stats"].items()}))
        f.write("\n\n")

        f.write("## Discovery Run\n")
        f.write(f"- Success: {discovery['success']}\n")
        f.write(f"- Attempts: {discovery['attempts']}\n")
        f.write(f"- Elapsed (s): {discovery['elapsed_seconds']:.3f}\n")
        if discovery["success"]:
            final = discovery["final_metrics"]
            f.write(f"- Final assignment: {final['assignment']}\n")
            f.write(f"- Final divergence: {final['final_divergence']:.3e}\n")
            f.write(f"- Final mean energy: {final['final_mean_energy']:.3e} J/m³\n")
            f.write("### Clause Slip Statistics (Final)\n")
            f.write(
                clause_table({str(k): v for k, v in final["clause_slip_stats"].items()})
            )
        f.write("\n")

    return md_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    verification_results = simulate_assignment(KNOWN_ASSIGNMENT)
    discovery_results = run_discovery()

    aggregate = {
        "verification_results": verification_results,
        "discovery_results": discovery_results,
        "formula": FORMULA,
        "known_assignment": KNOWN_ASSIGNMENT,
    }

    results_dir = CURRENT_FILE.parents[1] / "results"
    summary_path = write_results(results_dir, aggregate)
    print(f"SDT P vs NP experiment complete. Summary written to {summary_path}")


if __name__ == "__main__":
    main()



