"""
SDT Hodge-Conjecture Investigation Harness
------------------------------------------

This script instantiates the mapping described in `hodge_mapping_notes.md`.
It builds a toroidal displacement surface (complex 2-torus analogue), seeds
algebraic cycles as turbine regions, and encodes Hodge classes via rational
weights on those cycles. Two scenarios are simulated:

1. A decomposable harmonic class (`[a] + [b]`)
2. A perturbed, non-harmonic configuration (adds slip noise outside the span)

Outputs are written to `hodge_conjecture/results/` as JSON plus a Markdown
summary capturing throughput coefficients, divergence norms, and slip residuals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

CURRENT_FILE = Path(__file__).resolve()
HODGE_DIR = CURRENT_FILE.parents[1]
LOG_PATH = HODGE_DIR / "experiments" / "hodge_run.log"
SDT_CODE_DIR = CURRENT_FILE.parents[5] / "SDT" / "Code"

import sys

if str(SDT_CODE_DIR) not in sys.path:
    sys.path.append(str(SDT_CODE_DIR))

from sdt_navier.fields import FieldSystem, compute_diversion_density, initialize_fields  # type: ignore  # noqa: E402
from sdt_navier.equations import SDTNavierEquations  # type: ignore  # noqa: E402
from sdt_navier.solver import SDTNavierSolver  # type: ignore  # noqa: E402


PCMB = 2.036e-2  # Pa
DX = 2.0e-15
DY = 2.0e-15
DZ = 1.0e-15
NX = 32
NY = 32
NZ = 8
TORUS_MAJOR = 6.0 * DX
TORUS_MINOR = 2.5 * DX
AMBIENT_ETA = 0.55
CYCLE_ETA = 0.08
CYCLE_ETA_OVERLAP = 0.04
CYCLE_GAMMA = 0.04
CYCLE_GAMMA_OVERLAP = 0.08
CYCLE_KAPPA = 2.0e3
KAPPA_MAX = 5.0e3
V_MAX = 1.0e3
VELOCITY_DAMPING = 0.05
CELL_VOLUME = DX * DY * DZ


@dataclass
class CycleRegion:
    name: str
    mask: np.ndarray  # boolean
    eta_base: float
    gamma: float


@dataclass
class Environment:
    fields: FieldSystem
    cycles: Dict[str, CycleRegion]
    torus_mask: np.ndarray


def coordinate_grids(fields: FieldSystem) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return physical-space coordinate grids centered in the domain."""
    ix = (np.arange(fields.nx) - fields.nx / 2 + 0.5) * fields.dx
    iy = (np.arange(fields.ny) - fields.ny / 2 + 0.5) * fields.dy
    iz = (np.arange(fields.nz) - fields.nz / 2 + 0.5) * fields.dz
    return np.meshgrid(ix, iy, iz, indexing="ij")


def build_hodge_environment() -> Environment:
    """Initialize SDT fields plus torus/cycle masks."""
    initial_eta = np.full((NX, NY, NZ), AMBIENT_ETA, dtype=np.float64)
    initial_kappa = np.zeros((NX, NY, NZ), dtype=np.float64)
    initial_gamma = np.full((NX, NY, NZ), 0.02, dtype=np.float64)

    fields = initialize_fields(
        nx=NX,
        ny=NY,
        nz=NZ,
        dx=DX,
        dy=DY,
        dz=DZ,
        P_infinity=PCMB,
        initial_eta=initial_eta,
        initial_kappa=initial_kappa,
        initial_Gamma=initial_gamma,
    )

    X, Y, Z = coordinate_grids(fields)
    r_xy = np.sqrt(X**2 + Y**2)
    torus_mask = ((r_xy - TORUS_MAJOR) ** 2 + Z**2) <= TORUS_MINOR**2
    occlusion = np.where(torus_mask, 0.35, 0.0)
    fields.P = PCMB * (1.0 - occlusion)

    cycle_a_mask = torus_mask & (np.abs(Z) < DZ * 1.5) & (np.abs(r_xy - TORUS_MAJOR) < DX * 1.2)
    rho_xz = np.sqrt(X**2 + Z**2)
    cycle_b_mask = torus_mask & (np.abs(Y) < DY * 1.5) & (np.abs(rho_xz - TORUS_MAJOR) < DX * 1.2)
    cycle_ab_mask = cycle_a_mask & cycle_b_mask

    def apply_cycle(mask: np.ndarray, eta_target: float, gamma_value: float) -> None:
        fields.kappa = np.where(mask, np.maximum(fields.kappa, CYCLE_KAPPA), fields.kappa)
        fields.Gamma = np.where(mask, np.maximum(fields.Gamma, gamma_value), fields.Gamma)
        fields.eta = np.where(mask, np.minimum(fields.eta, eta_target), fields.eta)

    apply_cycle(cycle_a_mask, CYCLE_ETA, CYCLE_GAMMA)
    apply_cycle(cycle_b_mask, CYCLE_ETA, CYCLE_GAMMA)
    apply_cycle(cycle_ab_mask, CYCLE_ETA_OVERLAP, CYCLE_GAMMA_OVERLAP)

    cycles = {
        "a": CycleRegion("a", cycle_a_mask, CYCLE_ETA, CYCLE_GAMMA),
        "b": CycleRegion("b", cycle_b_mask, CYCLE_ETA, CYCLE_GAMMA),
        "a+b": CycleRegion("a+b", cycle_ab_mask, CYCLE_ETA_OVERLAP, CYCLE_GAMMA_OVERLAP),
    }

    recompute_energy_density(fields)
    return Environment(fields=fields, cycles=cycles, torus_mask=torus_mask)


def recompute_energy_density(fields: FieldSystem) -> None:
    sigma = compute_diversion_density(fields)
    tau_char = 8.4e-16 / 2.998e8
    fields.e = fields.P * sigma * tau_char


def stabilize_fields(fields: FieldSystem) -> None:
    fields.v = np.clip(fields.v, -V_MAX, V_MAX)
    fields.kappa = np.clip(fields.kappa, 0.0, KAPPA_MAX)
    fields.P = np.clip(fields.P, 0.0, PCMB)
    fields.eta = np.clip(fields.eta, 0.0, 1.0)
    recompute_energy_density(fields)


def damp_velocity(fields: FieldSystem) -> None:
    fields.v *= VELOCITY_DAMPING


def log_message(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now(timezone.utc).isoformat()}] {message}\n")


def encode_hodge_coefficients(env: Environment, coeffs: Dict[str, float]) -> None:
    """Map rational weights to slip/traction adjustments on each cycle."""
    for name, region in env.cycles.items():
        coeff = coeffs.get(name, 0.0)
        if coeff == 0.0:
            continue
        target_eta = AMBIENT_ETA - coeff * (AMBIENT_ETA - region.eta_base)
        fields_eta = env.fields.eta
        fields_eta = np.where(region.mask, np.clip(target_eta, 0.0, 1.0), fields_eta)
        env.fields.eta = fields_eta
    recompute_energy_density(env.fields)


def inject_non_harmonic_noise(env: Environment, magnitude: float = 0.15, seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    mask = (~env.torus_mask) & (rng.random(env.torus_mask.shape) < 0.05)
    perturbation = (rng.random(env.torus_mask.shape) - 0.5) * magnitude
    env.fields.eta = np.clip(env.fields.eta + mask * perturbation, 0.0, 1.0)
    recompute_energy_density(env.fields)


def simulate_environment(env: Environment, steps: int = 10) -> List[Dict[str, float]]:
    equations = SDTNavierEquations(
        rho_s=1.0e4,
        alpha_curv=1.0e-8,
        beta_slip=5.0e6,
        gamma_create=1.0e-22,
        delta_destroy=1.0e-6,
        epsilon_strain=1.0e-22,
        zeta_heal=1.0e-6,
    )
    solver = SDTNavierSolver(
        fields=env.fields,
        equations=equations,
        dt=None,
        cfl=0.8,
        method="euler",
        enforce_incompressibility=True,
    )
    history = []
    for step in range(steps):
        solver.step()
        stabilize_fields(env.fields)
        damp_velocity(env.fields)
        history.append(
            {
                "step": step + 1,
                "divergence": float(np.nan_to_num(solver.get_divergence_error())),
                "mean_eta": float(np.nan_to_num(np.mean(env.fields.eta))),
                "mean_energy": float(np.nan_to_num(np.mean(env.fields.e))),
            }
        )
    return history


def cycle_metrics(fields: FieldSystem, region: CycleRegion) -> Dict[str, float]:
    sigma = compute_diversion_density(fields)
    throughput_density = fields.P * sigma
    mask = region.mask
    throughput = float(np.sum(np.nan_to_num(throughput_density[mask])) * CELL_VOLUME)
    mean_eta = float(np.nanmean(fields.eta[mask])) if np.any(mask) else float("nan")
    mean_kappa = float(np.nanmean(fields.kappa[mask])) if np.any(mask) else float("nan")
    return {
        "throughput_J_per_s": throughput,
        "mean_eta": mean_eta,
        "mean_kappa": mean_kappa,
    }


def summarize_case(
    case_name: str,
    coeffs: Dict[str, float],
    non_harmonic: bool = False,
) -> Dict[str, object]:
    env = build_hodge_environment()
    encode_hodge_coefficients(env, coeffs)
    if non_harmonic:
        inject_non_harmonic_noise(env, magnitude=0.2, seed=7)
    history = simulate_environment(env, steps=35)
    per_cycle = {name: cycle_metrics(env.fields, region) for name, region in env.cycles.items()}
    total_throughput = float(
        np.sum(env.fields.P * compute_diversion_density(env.fields)) * CELL_VOLUME
    )
    ratios = {}
    if coeffs.get("b", 0.0) not in (0.0,):
        ratios["E_a_over_E_b"] = per_cycle["a"]["throughput_J_per_s"] / max(
            per_cycle["b"]["throughput_J_per_s"], 1e-30
        )
    return {
        "case": case_name,
        "coefficients": coeffs,
        "non_harmonic_noise": non_harmonic,
        "history": history,
        "per_cycle": per_cycle,
        "total_throughput_J_per_s": total_throughput,
        "divergence_final": history[-1]["divergence"],
        "ratio_checks": ratios,
    }


def write_results(verification: Dict[str, object], perturbation: Dict[str, object]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    results_dir = HODGE_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / f"hodge_pressure_basis_{timestamp}.json"
    md_path = results_dir / f"hodge_pressure_basis_{timestamp}.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump({"decomposable": verification, "perturbed": perturbation}, f, indent=2)

    def cycle_table(data: Dict[str, Dict[str, float]]) -> str:
        header = "| Cycle | Throughput (J/s) | mean η | mean κ |\n|---|---|---|---|"
        rows = []
        for name, values in data.items():
            rows.append(
                f"| {name} | {values['throughput_J_per_s']:.3e} | {values['mean_eta']:.3f} | {values['mean_kappa']:.3e} |"
            )
        return "\n".join([header] + rows)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# SDT Hodge Pressure Basis Experiment\n\n")
        f.write(f"- Timestamp (UTC): {timestamp}\n")
        f.write("## Decomposable Hodge Class (`a + b`)\n")
        f.write(f"- Divergence (final): {verification['divergence_final']:.3e}\n")
        f.write(f"- Total throughput: {verification['total_throughput_J_per_s']:.3e} J/s\n")
        f.write("### Cycle Metrics\n")
        f.write(cycle_table(verification["per_cycle"]))  # type: ignore[arg-type]
        f.write("\n\n")
        f.write("## Perturbed Configuration (`a + 1/2 b` + noise)\n")
        f.write(f"- Divergence (final): {perturbation['divergence_final']:.3e}\n")
        f.write(f"- Total throughput: {perturbation['total_throughput_J_per_s']:.3e} J/s\n")
        f.write("### Cycle Metrics\n")
        f.write(cycle_table(perturbation["per_cycle"]))  # type: ignore[arg-type]
        f.write("\n")

    return md_path


def main() -> None:
    log_message("Starting Hodge pressure-basis experiment run")
    try:
        decomposable = summarize_case(
            case_name="a+b harmonic",
            coeffs={"a": 1.0, "b": 1.0},
            non_harmonic=False,
        )
        perturbed = summarize_case(
            case_name="a + 0.5 b + noise",
            coeffs={"a": 1.0, "b": 0.5},
            non_harmonic=True,
        )
        summary = write_results(decomposable, perturbed)
        log_message(f"Experiment completed. Summary: {summary}")
        print(f"Hodge pressure-basis experiment complete. Summary written to {summary}")
    except Exception as exc:  # pragma: no cover - defensive logging
        log_message(f"Experiment failed: {exc}")
        raise


if __name__ == "__main__":
    main()


