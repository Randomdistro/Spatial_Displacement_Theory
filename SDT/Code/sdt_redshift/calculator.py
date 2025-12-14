from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple

import numpy as np

# Speed of light expressed in km/s so that H0 provided in km/s/Mpc is consistent.
C_KM_PER_S = 299_792.458
# 1 megaparsec expressed in kilometres (exact enough for astrophysical work).
KM_PER_MPC = 3.085_677_581_491_367e19
# Seconds per giga-year for lookback time conversions.
SECONDS_PER_GYR = 3.155_76e16


@dataclass
class StrainModelParameters:
    """
    Parameterization of the strain-rate corrections described in sdt_redshift.md.

    The defaults reproduce the qualitative behaviour documented in Part 1:
    - δ_halo  : ~10% boost at z≈0 that decays over the local-universe range
    - δ_LSS   : ~5% oscillation capturing large-scale structure modulation
    - δ_CLS   : A Gaussian spike centred on the clearing boundary (z~1100)
    """

    halo_amplitude: float = 0.10
    halo_scale: float = 0.25
    lss_amplitude: float = 0.05
    lss_period: float = 0.45
    lss_decay: float = 3.0
    cls_amplitude: float = 0.35
    cls_center: float = 1_100.0
    cls_width: float = 120.0


class RedshiftCalculator:
    """
    Implements the SDT redshift compensator described in sdt_redshift.md.

    The core quantity is the strain rate σ(z) = σ₀[1 + δ_halo + δ_LSS + δ_CLS],
    where σ₀ = H₀/c. Integrating σ(z) yields the affine path length L(z) and the
    observable distances:
        D_L(z) = (1 + z)^3 L(z)
        D_A(z) = (1 + z)   L(z)
    """

    def __init__(
        self,
        H0: float = 70.0,
        *,
        params: StrainModelParameters | None = None,
        steps_per_unit: int = 512,
        min_steps: int = 256,
    ) -> None:
        if H0 <= 0:
            raise ValueError("H0 must be positive (km/s/Mpc).")
        if steps_per_unit <= 0 or min_steps <= 0:
            raise ValueError("Integration step settings must be positive.")

        self.H0 = float(H0)
        self.params = params or StrainModelParameters()
        self.sigma0 = self.H0 / C_KM_PER_S
        self.steps_per_unit = int(steps_per_unit)
        self.min_steps = int(min_steps)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sigma(self, z: np.ndarray | float) -> np.ndarray | float:
        """Return σ(z) in 1/Mpc for scalar or vector inputs."""
        z_arr, scalar = self._to_array(z)
        sigma = self.sigma0 * (1.0 + self._delta_total(z_arr))
        return float(sigma[0]) if scalar else sigma

    def comoving_affine_distance(self, z: np.ndarray | float) -> np.ndarray | float:
        """
        Compute L(z) = ∫₀ᶻ dz' / ((1 + z') σ(z'))  in megaparsecs.
        """
        return self._integrate(
            z,
            lambda zz: 1.0 / ((1.0 + zz) * self.sigma(zz)),
        )

    def luminosity_distance(self, z: np.ndarray | float) -> np.ndarray | float:
        """
        D_L(z) = (1 + z)^3 L(z)  in megaparsecs.
        """
        L = self.comoving_affine_distance(z)
        z_arr, scalar = self._to_array(z)
        D_L = (1.0 + z_arr) ** 3 * np.asarray(L if isinstance(L, np.ndarray) else np.array(L))
        return float(D_L[0]) if scalar else D_L

    def angular_diameter_distance(self, z: np.ndarray | float) -> np.ndarray | float:
        """
        D_A(z) = (1 + z) L(z)  in megaparsecs.
        """
        L = self.comoving_affine_distance(z)
        z_arr, scalar = self._to_array(z)
        D_A = (1.0 + z_arr) * np.asarray(L if isinstance(L, np.ndarray) else np.array(L))
        return float(D_A[0]) if scalar else D_A

    def lookback_time(self, z: np.ndarray | float) -> np.ndarray | float:
        """
        Lookback time in giga-years from the SDT strain model:
            t_L(z) = ∫₀ᶻ dz' / ((1 + z') H(z'))
        with H(z) = c σ(z) and unit conversions handled internally.
        """
        seconds = self._integrate(
            z,
            lambda zz: 1.0 / ((1.0 + zz) * self._H_of_z(zz)),
        )
        seconds_arr = np.asarray(seconds if isinstance(seconds, np.ndarray) else np.array(seconds))
        gyr = seconds_arr / SECONDS_PER_GYR
        scalar = np.isscalar(z)
        return float(gyr[0]) if scalar else gyr

    def distance_modulus(self, z: np.ndarray | float) -> np.ndarray | float:
        """
        Convenience helper: μ = 5 log10(D_L / 10 pc), with D_L returned in Mpc.
        """
        D_L_mpc = self.luminosity_distance(z)
        D_L_pc = np.asarray(D_L_mpc if isinstance(D_L_mpc, np.ndarray) else np.array(D_L_mpc)) * 1e6
        mu = 5.0 * np.log10(D_L_pc / 10.0)
        scalar = np.isscalar(z)
        return float(mu[0]) if scalar else mu

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _delta_total(self, z: np.ndarray) -> np.ndarray:
        return self._delta_halo(z) + self._delta_lss(z) + self._delta_cls(z)

    def _delta_halo(self, z: np.ndarray) -> np.ndarray:
        p = self.params
        if p.halo_amplitude == 0.0:
            return np.zeros_like(z)
        scale = max(p.halo_scale, 1e-6)
        return p.halo_amplitude * np.exp(-z / scale)

    def _delta_lss(self, z: np.ndarray) -> np.ndarray:
        p = self.params
        if p.lss_amplitude == 0.0:
            return np.zeros_like(z)
        period = max(p.lss_period, 1e-3)
        phase = (2.0 * np.pi / period) * z
        return p.lss_amplitude * np.sin(phase) * np.exp(-z / max(p.lss_decay, 1e-6))

    def _delta_cls(self, z: np.ndarray) -> np.ndarray:
        p = self.params
        if p.cls_amplitude == 0.0:
            return np.zeros_like(z)
        width = max(p.cls_width, 1e-6)
        arg = (z - p.cls_center) ** 2 / (2.0 * width ** 2)
        return p.cls_amplitude * np.exp(-arg)

    def _integrate(self, z: np.ndarray | float, integrand: Callable[[np.ndarray], np.ndarray]) -> np.ndarray | float:
        z_arr, scalar = self._to_array(z)
        results = np.zeros_like(z_arr)
        for idx, z_max in np.ndenumerate(z_arr):
            if z_max == 0.0:
                results[idx] = 0.0
                continue
            n_steps = max(self.min_steps, int(self.steps_per_unit * max(z_max, 1.0)))
            sample = np.linspace(0.0, float(z_max), n_steps, dtype=float)
            values = integrand(sample)
            results[idx] = np.trapz(values, sample)
        return float(results[0]) if scalar else results

    def _H_of_z(self, z: np.ndarray) -> np.ndarray:
        """
        Return H(z) in s^-1 for use in lookback-time integration.
        """
        Hz_km = C_KM_PER_S * self.sigma(z)
        return Hz_km / KM_PER_MPC

    def _to_array(self, z: np.ndarray | float) -> Tuple[np.ndarray, bool]:
        scalar = np.isscalar(z)
        arr = np.atleast_1d(np.asarray(z, dtype=float))
        if np.any(arr < 0):
            raise ValueError("Redshift must be non-negative.")
        return arr, scalar


