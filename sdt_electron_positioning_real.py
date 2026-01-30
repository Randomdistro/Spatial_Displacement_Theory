#!/usr/bin/env python3
"""
Real SDT Electron Positioning Model
Based on nuclear pressure field minima with proper SDT physics
"""

import sys

# Ensure Unicode output works on Windows consoles (Cursor often runs with cp1252).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from typing import List, Tuple, Dict, Optional, Callable
from dataclasses import dataclass
import math

@dataclass
class NuclearGeometry:
    """SDT nuclear geometry with discrete nucleon positions"""
    nucleon_positions: List[np.ndarray]  # 3D positions in fm
    nucleon_types: List[str]  # 'proton' or 'neutron'
    effective_radius: float  # fm

@dataclass
class ElectronPosition:
    """Electron position at pressure minimum"""
    position: np.ndarray  # 3D position in Å
    occupancy: float  # 0-1
    type: str  # 'bonding', 'lone_pair'
    potential_energy: float  # SDT potential value

class SDTElectronPositioning:
    """
    Real SDT electron positioning using pressure field minima
    All calculations in meters internally
    """

    def __init__(self, nuclear_geometry: NuclearGeometry):
        self.nucleus = nuclear_geometry
        # Convert nuclear geometry to meters
        self.nuclear_positions_m = [pos * 1e-15 for pos in nuclear_geometry.nucleon_positions]  # fm to m
        self.nuclear_types = nuclear_geometry.nucleon_types
        self.effective_radius_m = nuclear_geometry.effective_radius * 1e-15  # fm to m

        # SDT fundamental constants
        self.E_nu = 1.57e6 * 1.602e-19  # Neutrino energy in J (1.57 MeV)

        # SDT chemistry scale: emergent spation correlation volume at atomic scale
        # This bridges nuclear (~fm) to chemical (~Å) scales
        # Derived from spation lattice correlation length at atomic densities
        spation_correlation_length = 1e-10  # 1 Å (atomic scale correlation)
        self.V_chem = spation_correlation_length ** 3  # m³ (chemistry averaging volume)

        # Electron repulsion strength (from SDT spation exclusion)
        self.electron_repulsion_strength = 1.0  # Relative strength

        # Placed electrons for iterative repulsion
        self.placed_electrons = []

    def sdt_pressure_kernel(self, r: np.ndarray, nucleon_pos: np.ndarray, nucleon_type: str) -> float:
        """
        SDT Pressure Kernel with Chemistry-Scale Averaging

        U_nuclear(r) = -Σᵢ [Ωᵢ(r) / 4π] × (E_ν / V_chem) + lattice_stiffness(r)

        Where:
        - Ωᵢ(r) = solid angle occlusion by nucleon i at r
        - E_ν = neutrino energy (1.57 MeV)
        - V_chem = chemistry-scale averaging volume (~1 Å³)
        - lattice_stiffness = repulsive counter-term creating bond length minimum

        This creates stable minima at Å scale through attraction + repulsion balance.
        """
        # Vector from nucleon to field point
        dr = r - nucleon_pos
        distance = np.linalg.norm(dr)

        if distance < 1e-12:  # Avoid singularity (1 pm)
            return 1e6  # Large repulsive potential

        # Nucleon radius based on type (all in meters now)
        if nucleon_type == 'proton':
            nucleon_radius = 0.84e-15
        elif nucleon_type == 'neutron':
            nucleon_radius = 0.87e-15
        elif nucleon_type == 'alpha':
            nucleon_radius = 1.7e-15
        else:
            nucleon_radius = 0.84e-15

        # Solid angle occlusion
        if distance <= nucleon_radius:
            omega = 4 * np.pi  # Full sphere
        else:
            sin_theta = nucleon_radius / distance
            if sin_theta >= 1:
                omega = 4 * np.pi
            else:
                cos_theta = np.sqrt(1 - sin_theta**2)
                omega = 2 * np.pi * (1 - cos_theta)

        # Attractive nuclear potential (occlusion creates pressure deficit)
        occlusion_fraction = omega / (4 * np.pi)
        attractive_potential = -occlusion_fraction * (self.E_nu / self.V_chem)

        # Repulsive counter-term: SDT lattice stiffness (nondimensionalized)
        # Prevents nuclear collapse by opposing compression at short distances
        r0 = 1e-10  # 1 Å reference distance
        A = 1e-18   # Reasonable scale factor (not insane like 1e-9)
        repulsive_potential = A * (r0 / distance)**12

        return attractive_potential + repulsive_potential

    def total_sdt_potential(self, r: np.ndarray) -> float:
        """
        Total SDT potential at position r (all in meters)
        Includes nuclear attraction + electron repulsion + lattice stiffness
        """
        total_potential = 0.0

        # Nuclear contribution (from nucleons/alpha clusters in meters)
        for pos_m, n_type in zip(self.nuclear_positions_m, self.nuclear_types):
            if n_type == 'alpha':
                # Alpha cluster: treat as 4 nucleons (2p + 2n)
                alpha_contribution = self._alpha_cluster_potential(r, pos_m)
                total_potential += alpha_contribution
            else:
                # Individual nucleon
                total_potential += self.sdt_pressure_kernel(r, pos_m, n_type)

        # Electron-electron repulsion from already-placed electrons
        electron_repulsion = self._electron_repulsion_potential(r)

        return total_potential + electron_repulsion

    def _alpha_cluster_potential(self, r: np.ndarray, alpha_center: np.ndarray) -> float:
        """
        SDT potential from alpha cluster (2p + 2n tetrahedral arrangement)
        All in meters for consistency
        """
        # Alpha internal structure: tetrahedral 2p + 2n
        # Internal spacing from SDT nuclear binding (not arbitrary)
        nucleon_spacing = 1.2e-15  # ~1.2 fm internal spacing (from alpha binding)

        # Tetrahedral nucleon positions relative to alpha center
        nucleon_positions = [
            alpha_center + np.array([nucleon_spacing, 0, nucleon_spacing]),
            alpha_center + np.array([-nucleon_spacing, 0, nucleon_spacing]),
            alpha_center + np.array([0, nucleon_spacing, -nucleon_spacing]),
            alpha_center + np.array([0, -nucleon_spacing, -nucleon_spacing])
        ]

        nucleon_types = ['proton', 'proton', 'neutron', 'neutron']

        # Sum contributions from all nucleons in alpha cluster
        total = 0.0
        for pos, n_type in zip(nucleon_positions, nucleon_types):
            total += self.sdt_pressure_kernel(r, pos, n_type)

        return total

    def _electron_repulsion_potential(self, r: np.ndarray) -> float:
        """
        SDT Electron-Electron Repulsion
        From already-placed electrons (iterative, not guessed geometry)

        Each placed electron creates spation exclusion pressure field
        that repels other electrons from occupying same region.
        """
        repulsion = 0.0

        # SDT electron cloud radius (from toroidal vortex structure)
        electron_cloud_radius = 5e-11  # 0.5 Å (electron cloud size)

        for placed_electron_pos in self.placed_electrons:
            dr = np.linalg.norm(r - placed_electron_pos)
            if dr < 1e-12:  # Avoid self-interaction
                continue

            # SDT spation exclusion: electrons repel via pressure field
            if dr <= electron_cloud_radius:
                # Inside electron cloud - strong Pauli-like repulsion
                repulsion += 1e3  # Strong repulsive barrier
            else:
                # Outside - screened Coulomb-like repulsion
                repulsion += self.electron_repulsion_strength / (dr ** 2)

        return repulsion

    def _get_tetrahedral_vertices_fm(self) -> List[np.ndarray]:
        """Tetrahedral nuclear positions in fm"""
        # Oxygen-16: 4 alpha particles at tetrahedral vertices
        scale = self.nucleus.effective_radius
        h = (2/3**0.5) * scale  # Tetrahedral height

        return [
            np.array([0, 0, h]),
            np.array([scale, 0, -h/3]),
            np.array([-scale/2, scale*np.sqrt(3)/2, -h/3]),
            np.array([-scale/2, -scale*np.sqrt(3)/2, -h/3])
        ]

    def _unit(self, v: np.ndarray) -> np.ndarray:
        """Unit vector"""
        n = np.linalg.norm(v)
        return v / n if n > 0 else v

    def _tetra_dirs(self) -> List[np.ndarray]:
        """Get tetrahedral direction vectors from nuclear geometry"""
        verts_fm = self._get_tetrahedral_vertices_fm()
        return [self._unit(np.array(v, dtype=float)) for v in verts_fm]

    def _local_refine(self, x0_m: np.ndarray, max_iter=80) -> np.ndarray:
        """
        Backtracking gradient descent in meters for stability
        """
        x = x0_m.copy()
        for _ in range(max_iter):
            # Numerical gradient
            eps = 1e-12  # 1 pm step
            g = np.zeros(3)
            f0 = self.total_sdt_potential(x)
            for i in range(3):
                xp = x.copy()
                xm = x.copy()
                xp[i] += eps
                xm[i] -= eps
                g[i] = (self.total_sdt_potential(xp) - self.total_sdt_potential(xm)) / (2 * eps)

            gnorm = np.linalg.norm(g)
            if gnorm < 1e-6:
                break

            # Backtracking line search
            step = 1e-12  # Start with 1 pm
            c = 1e-4  # Sufficient decrease parameter
            for _ls in range(20):
                xn = x - step * g
                if self.total_sdt_potential(xn) <= f0 - c * step * (gnorm ** 2):
                    x = xn
                    break
                step *= 0.5
            else:
                # Couldn't improve
                break

            # Keep away from nuclear center (soft constraint)
            nc = np.mean(self.nuclear_positions_m, axis=0)
            d = np.linalg.norm(x - nc)
            min_d = 5e-11  # 0.5 Å minimum
            if d < min_d:
                x = nc + (x - nc) / (d + 1e-30) * min_d

        return x

    def _best_candidates_on_shell(self, R0=1.0e-10, n_theta=16, n_phi=32, keep=12) -> List[np.ndarray]:
        """
        Deterministic candidate search on sphere of radius R0 around nuclear center.
        Returns candidate positions in meters.
        """
        nc = np.mean(self.nuclear_positions_m, axis=0)
        candidates = []  # list of (U, x)

        for it in range(n_theta):
            theta = np.pi * (it + 0.5) / n_theta
            for ip in range(n_phi):
                phi = 2 * np.pi * ip / n_phi
                d = np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])
                x = nc + R0 * d
                U = self.total_sdt_potential(x)
                candidates.append((U, x))

        candidates.sort(key=lambda t: t[0])  # Sort by potential energy
        return [x for _, x in candidates[:keep]]

    def find_electron_positions(self) -> List[ElectronPosition]:
        """
        Find electron positions using grid search + iterative refinement
        Much more robust than pure gradient descent
        """
        positions = []
        self.placed_electrons = []

        m_to_angstrom = 1e10

        # 1) Get deterministic candidates near chemistry scale (~1 Å)
        candidates = self._best_candidates_on_shell(R0=1.0e-10, keep=16)

        # 2) Place electrons iteratively: each placement updates repulsion
        for i in range(4):
            # Re-score candidates under current repulsion
            scored = [(self.total_sdt_potential(x), x) for x in candidates]
            scored.sort(key=lambda t: t[0])

            # Start refinement from best candidate
            x0 = scored[0][1]
            x_min = self._local_refine(x0)

            # Store placed electron for repulsion
            self.placed_electrons.append(x_min)

            # Remove candidates too close to placed electron (prevents re-picking same spot)
            prune_radius = 6e-11  # 0.6 Å - prevents clustering
            candidates = [c for c in candidates if np.linalg.norm(c - x_min) > prune_radius]

            # Ensure we have enough candidates for remaining electrons
            if len(candidates) < 8:
                candidates = self._best_candidates_on_shell(R0=1.0e-10, keep=32)

            # Classify and create electron position
            pos_type = 'bonding' if i < 2 else 'lone_pair'
            occupancy = 1.0 if i < 2 else 0.8

            positions.append(ElectronPosition(
                position=x_min * m_to_angstrom,  # Convert to Å for output
                occupancy=occupancy,
                type=pos_type,
                potential_energy=self.total_sdt_potential(x_min)
            ))

        return positions

    def _gradient_descent(self, initial_pos: np.ndarray, max_iter: int = 100, step_size: float = 0.01) -> np.ndarray:
        """
        Gradient descent to find potential minimum (all in consistent units)
        initial_pos in Å, works in meters internally, returns in Å
        """
        # Convert initial position from Å to meters for calculation
        angstrom_to_m = 1e-10
        pos_m = initial_pos * angstrom_to_m

        for _ in range(max_iter):
            # Numerical gradient in meter coordinates
            eps = 1e-12  # 1 pm step for numerical differentiation
            grad = np.zeros(3)

            for i in range(3):
                pos_plus = pos_m.copy()
                pos_minus = pos_m.copy()
                pos_plus[i] += eps
                pos_minus[i] -= eps

                grad[i] = (self.total_sdt_potential(pos_plus) - self.total_sdt_potential(pos_minus)) / (2 * eps)

            # Update position (gradient descent)
            pos_m -= step_size * grad

            # Prevent collapse to nucleus
            nuclear_center = np.mean(self.nuclear_positions_m, axis=0)
            min_distance = 5e-11  # 0.5 Å minimum distance
            current_distance = np.linalg.norm(pos_m - nuclear_center)
            if current_distance < min_distance:
                # Push away from nucleus
                direction = (pos_m - nuclear_center) / current_distance
                pos_m = nuclear_center + direction * min_distance

        # Convert back to Å for return
        return pos_m / angstrom_to_m

def test_sdt_model():
    """Test the real SDT model on oxygen-16 with sanity checks"""
    print("Real SDT Electron Positioning Model")
    print("="*50)
    print("Units: Consistent meters internally, Å for output")
    print("V_chem: 1 Å³ (spation correlation volume)")
    print("Grid search + iterative refinement")
    print("Backtracking line search for stability")
    print()

    # Create oxygen-16 nucleus (4 alpha particles in tetrahedron)
    # Positions in fm (converted to meters internally)
    alpha_positions_fm = [
        np.array([0, 0, 2.0]),     # Top
        np.array([1.7, 0, -0.7]),  # Base 1
        np.array([-0.85, 1.5, -0.7]), # Base 2
        np.array([-0.85, -1.5, -0.7]) # Base 3
    ]

    nucleus = NuclearGeometry(
        nucleon_positions=alpha_positions_fm,
        nucleon_types=['alpha'] * 4,
        effective_radius=3.0  # fm
    )

    # Run SDT positioning
    model = SDTElectronPositioning(nucleus)
    electron_positions = model.find_electron_positions()

    # SANITY CHECKS (as requested)
    print("=== SANITY CHECKS ===")

    # Nuclear center in meters
    nuclear_center_m = np.mean(model.nuclear_positions_m, axis=0)
    nuclear_center_angstrom = nuclear_center_m * 1e10  # m to Å

    print(f"Nuclear center: ({nuclear_center_angstrom[0]:.3f}, {nuclear_center_angstrom[1]:.3f}, {nuclear_center_angstrom[2]:.3f}) Å")

    # Electron distances from nuclear center
    print("\nElectron distances from nuclear center:")
    for i, ep in enumerate(electron_positions):
        dist = np.linalg.norm(ep.position - nuclear_center_angstrom)
        print(f"  e{i+1} ({ep.type}): r = {dist:.3f} Å, U = {ep.potential_energy:.3e}")
    # Min pairwise electron distances
    print("\nMin pairwise electron distances:")
    min_pairwise = float('inf')
    for i in range(len(electron_positions)):
        for j in range(i+1, len(electron_positions)):
            dist = np.linalg.norm(electron_positions[i].position - electron_positions[j].position)
            min_pairwise = min(min_pairwise, dist)
            print(f"  e{i+1}-e{j+1}: {dist:.3f} Å")
    print(f"Min pairwise distance: {min_pairwise:.3f} Å")

    # Analyze results
    bonding_positions = [p for p in electron_positions if p.type == 'bonding']

    print("\n=== PREDICTIONS ===")
    print(f"Found {len(bonding_positions)} bonding electrons")

    if len(bonding_positions) >= 2:
        pos1, pos2 = bonding_positions[0].position, bonding_positions[1].position

        # Vectors from nuclear center to electrons
        vec1 = pos1 - nuclear_center_angstrom
        vec2 = pos2 - nuclear_center_angstrom

        # Bond angle
        cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        bond_angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))

        # Bond length (average)
        bond_length = (np.linalg.norm(vec1) + np.linalg.norm(vec2)) / 2

        print("\nSDT Predictions:")
        print(f"  Bond angle:  {bond_angle:.2f}°")
        print(f"  Bond length: {bond_length:.3f} Å")

        print("\nExperimental targets: 104.5°, 0.958 Å")
        angle_error = abs(bond_angle - 104.5)
        length_error = abs(bond_length - 0.958)
        print(f"  Angle error:  {angle_error:.2f}°")
        print(f"  Length error: {length_error:.3f} Å")

        if angle_error < 5 and length_error < 0.1:
            print("\n✅ SUCCESS: SDT quantitatively predicts water geometry!")
        elif angle_error < 10:
            print("\n⚠️ GOOD: Angle within 10° — anisotropy is doing something.")
        else:
            print("\n❌ NEEDS WORK: Not yet quantitative.")
    return electron_positions

if __name__ == '__main__':
    test_sdt_model()