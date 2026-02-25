#!/usr/bin/env python3
"""
Phase 1.3: Second Layer Structure

Establishes the second layer structure:
- 20 triangular interstices between first-shell spheres
- Building block stacking rules
- Alpha cluster arrangements (triangular, tetrahedral, octahedral)
- Inter-alpha spacing and bonding

This enables construction of heavier nuclei from alpha clusters.
"""

import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
import math

# ============================================================================
# CONSTANTS
# ============================================================================

R_NUCLEON_FM = 0.84  # fm
DIST_INTER_ALPHA_FM = 2.9  # fm (C-12/O-16 cluster spacing)

# ============================================================================
# TRIANGULAR INTERSTICES
# ============================================================================

@dataclass
class TriangularInterstice:
    """
    Represents a triangular interstice in the second layer.
    
    An icosahedron has 20 triangular faces.
    Each triangular face = 3 first-shell spheres forming a triangle.
    Each triangle has 1 triangular interstice (the gap in the middle).
    Total: 20 triangular interstices.
    """
    index: int  # 0-19
    face_vertices: Tuple[int, int, int]  # Indices of the 3 vertices forming the triangle
    center_position: Tuple[float, float, float]  # Center of the interstice
    radius: float  # Distance from center to interstice (fm)
    
    def distance_to_center(self) -> float:
        """Calculate distance from nuclear center"""
        x, y, z = self.center_position
        return math.sqrt(x*x + y*y + z*z)


class SecondLayer:
    """
    Second layer structure: 20 triangular interstices.
    
    Properties:
    - Total width: 10r (from center to outer edge)
    - Positions: Located in triangular interstices between first-shell spheres
    - Critical property: These positions do NOT touch each other - they are isolated
    - Each interstice is surrounded by 3 first-shell spheres (forming the triangle)
    """
    
    def __init__(self, first_shell_vertices: List[Tuple[float, float, float]], 
                 nucleon_radius: float = R_NUCLEON_FM):
        """
        Initialize second layer from first shell vertices.
        
        Parameters:
        -----------
        first_shell_vertices : List[Tuple[float, float, float]]
            Cartesian coordinates of first shell vertices
        nucleon_radius : float
            Nucleon radius (fm)
        """
        self.nucleon_radius = nucleon_radius
        self.first_shell_vertices = first_shell_vertices
        self.total_width = 10.0 * nucleon_radius  # 10r from center to outer edge
        
        # Generate triangular interstices
        self.interstices = self._generate_triangular_interstices()
    
    def _generate_triangular_interstices(self) -> List[TriangularInterstice]:
        """
        Generate 20 triangular interstices from icosahedral faces.
        
        An icosahedron has 20 triangular faces.
        Each face is defined by 3 vertices.
        The interstice is at the center of each triangle.
        
        Returns:
        --------
        List[TriangularInterstice]
            List of 20 interstices
        """
        interstices = []
        
        # Icosahedron has 20 faces
        # Each face is a triangle of 3 vertices
        # We need to identify all triangular faces
        
        # For an icosahedron, faces are defined by:
        # - 5 faces around each vertex (each vertex is part of 5 faces)
        # - Total: 12 vertices × 5 faces / 3 vertices per face = 20 faces
        
        # Generate faces by finding all triangles where all edges are equal
        # (all edges in icosahedron are equal length)
        faces = []
        n_vertices = len(self.first_shell_vertices)
        
        # Calculate all pairwise distances
        distances = {}
        for i in range(n_vertices):
            for j in range(i+1, n_vertices):
                v1 = np.array(self.first_shell_vertices[i])
                v2 = np.array(self.first_shell_vertices[j])
                dist = np.linalg.norm(v2 - v1)
                distances[(i, j)] = dist
        
        # Find triangles with equal edges (within tolerance)
        # Icosahedron: all edges equal, so all triangles with equal edges are faces
        mean_edge_length = np.mean(list(distances.values()))
        tolerance = 0.1 * mean_edge_length
        
        for i in range(n_vertices):
            for j in range(i+1, n_vertices):
                for k in range(j+1, n_vertices):
                    d_ij = distances.get((i, j), distances.get((j, i)))
                    d_jk = distances.get((j, k), distances.get((k, j)))
                    d_ki = distances.get((k, i), distances.get((i, k)))
                    
                    if (d_ij and d_jk and d_ki and
                        abs(d_ij - mean_edge_length) < tolerance and
                        abs(d_jk - mean_edge_length) < tolerance and
                        abs(d_ki - mean_edge_length) < tolerance):
                        faces.append((i, j, k))
        
        # Limit to 20 faces (icosahedron has exactly 20)
        faces = faces[:20]
        
        # Create interstices at centers of triangles
        for idx, (i, j, k) in enumerate(faces):
            v1 = np.array(self.first_shell_vertices[i])
            v2 = np.array(self.first_shell_vertices[j])
            v3 = np.array(self.first_shell_vertices[k])
            
            # Center of triangle
            center = (v1 + v2 + v3) / 3.0
            
            # Distance from origin
            radius = np.linalg.norm(center)
            
            interstice = TriangularInterstice(
                index=idx,
                face_vertices=(i, j, k),
                center_position=tuple(center),
                radius=radius
            )
            interstices.append(interstice)
        
        return interstices
    
    def get_interstice_positions(self) -> List[Tuple[float, float, float]]:
        """
        Get positions of all triangular interstices.
        
        Returns:
        --------
        List[Tuple[float, float, float]]
            List of (x, y, z) positions
        """
        return [inter.center_position for inter in self.interstices]
    
    def verify_isolation(self) -> dict:
        """
        Verify that interstices do not touch each other.
        
        Returns:
        --------
        dict
            Verification results
        """
        results = {
            'all_isolated': True,
            'min_separation': float('inf'),
            'violations': []
        }
        
        n = len(self.interstices)
        for i in range(n):
            for j in range(i+1, n):
                pos1 = np.array(self.interstices[i].center_position)
                pos2 = np.array(self.interstices[j].center_position)
                separation = np.linalg.norm(pos2 - pos1)
                
                results['min_separation'] = min(results['min_separation'], separation)
                
                # Check if they're too close (should be > 2r to not touch)
                if separation < 2.0 * self.nucleon_radius:
                    results['all_isolated'] = False
                    results['violations'].append(
                        f"Interstices {i} and {j}: separation {separation:.3f} fm < 2r = {2.0*self.nucleon_radius:.3f} fm"
                    )
        
        return results


# ============================================================================
# ALPHA CLUSTER ARRANGEMENTS
# ============================================================================

class AlphaClusterArrangement:
    """
    Base class for alpha cluster arrangements in second layer.
    """
    
    def __init__(self, n_alphas: int, arrangement_type: str):
        """
        Initialize alpha cluster arrangement.
        
        Parameters:
        -----------
        n_alphas : int
            Number of alpha particles
        arrangement_type : str
            Type of arrangement ('triangle', 'tetrahedron', 'octahedron', etc.)
        """
        self.n_alphas = n_alphas
        self.arrangement_type = arrangement_type
        self.alpha_effective_radius = self._calculate_alpha_effective_radius()
    
    def _calculate_alpha_effective_radius(self) -> float:
        """
        Calculate effective radius of alpha particle.
        
        Alpha is tetrahedral with 4 nucleons.
        Effective radius = distance to center + nucleon radius
        
        Returns:
        --------
        float
            Effective radius (fm)
        """
        # Alpha internal separation (compressed)
        d_alpha = 1.45  # fm (vacuum lock compression)
        
        # Distance to geometric center of tetrahedron
        # For tetrahedron: r_center = d / sqrt(8/3) ≈ 0.6124 * d
        r_geometric_center = d_alpha * 0.6124
        
        # Effective radius = center distance + nucleon radius
        return r_geometric_center + R_NUCLEON_FM
    
    def calculate_inter_alpha_bonds(self) -> int:
        """
        Calculate number of inter-alpha bonds.
        
        Returns:
        --------
        int
            Number of bonds
        """
        if self.arrangement_type == 'triangle':
            return 3  # 3 alphas in triangle: 3 bonds
        elif self.arrangement_type == 'tetrahedron':
            return 6  # 4 alphas in tetrahedron: 6 bonds
        elif self.arrangement_type == 'octahedron':
            return 12  # 6 alphas in octahedron: 12 bonds
        else:
            # General: n(n-1)/2 for complete graph, but actual depends on geometry
            return self.n_alphas * (self.n_alphas - 1) // 2
    
    def calculate_inter_alpha_occlusion(self) -> float:
        """
        Calculate total inter-alpha occlusion.
        
        Returns:
        --------
        float
            Total occlusion from inter-alpha bonds (steradians)
        """
        n_bonds = self.calculate_inter_alpha_bonds()
        
        # Single bond occlusion
        R_eff = self.alpha_effective_radius
        d = DIST_INTER_ALPHA_FM
        
        if d <= R_eff:
            single_bond_occlusion = 2.0 * math.pi
        else:
            sin_theta = R_eff / d
            if sin_theta >= 1.0:
                single_bond_occlusion = 2.0 * math.pi
            else:
                cos_theta = math.sqrt(1.0 - sin_theta*sin_theta)
                single_bond_occlusion = 2.0 * math.pi * (1.0 - cos_theta)
        
        return n_bonds * single_bond_occlusion


class Carbon12Arrangement(AlphaClusterArrangement):
    """
    Carbon-12: 3 alphas in triangular arrangement.
    """
    
    def __init__(self):
        super().__init__(n_alphas=3, arrangement_type='triangle')
    
    def get_alpha_positions(self) -> List[Tuple[float, float, float]]:
        """
        Get positions of 3 alphas in triangle.
        
        Returns:
        --------
        List[Tuple[float, float, float]]
            Positions of 3 alpha particles
        """
        # Equilateral triangle in plane
        # Side length = DIST_INTER_ALPHA_FM
        d = DIST_INTER_ALPHA_FM
        
        # Triangle vertices
        pos1 = (0.0, 0.0, 0.0)  # Center of triangle at origin
        pos2 = (d, 0.0, 0.0)
        pos3 = (d/2.0, d*math.sqrt(3)/2.0, 0.0)
        
        return [pos1, pos2, pos3]


class Oxygen16Arrangement(AlphaClusterArrangement):
    """
    Oxygen-16: 4 alphas in tetrahedral arrangement.
    """
    
    def __init__(self):
        super().__init__(n_alphas=4, arrangement_type='tetrahedron')
    
    def get_alpha_positions(self) -> List[Tuple[float, float, float]]:
        """
        Get positions of 4 alphas in tetrahedron.
        
        Returns:
        --------
        List[Tuple[float, float, float]]
            Positions of 4 alpha particles
        """
        # Regular tetrahedron
        # All edges equal to DIST_INTER_ALPHA_FM
        d = DIST_INTER_ALPHA_FM
        
        # Tetrahedron vertices
        # One vertex at origin, others arranged around it
        pos1 = (0.0, 0.0, 0.0)
        pos2 = (d, 0.0, 0.0)
        pos3 = (d/2.0, d*math.sqrt(3)/2.0, 0.0)
        pos4 = (d/2.0, d*math.sqrt(3)/6.0, d*math.sqrt(2/3))
        
        return [pos1, pos2, pos3, pos4]


class Nitrogen14Arrangement(AlphaClusterArrangement):
    """
    Nitrogen-14: 3 alphas + 1 proton (3α + p).
    
    Structure: same triangular alpha layout as Carbon-12, with one
    additional proton at the geometric center of the triangle
    (or in a nodal position). Nuclear field strength 14x.
    """
    
    def __init__(self):
        super().__init__(n_alphas=3, arrangement_type='triangle')
        self.n_protons_extra = 1
        # ¹⁴N = 7p + 7n. 3 alphas = 6p+6n; extra = 1p+1n (nodal proton + neutron).
        self.total_nucleons = 14
    
    def get_alpha_positions(self) -> List[Tuple[float, float, float]]:
        """Same triangle as Carbon-12."""
        d = DIST_INTER_ALPHA_FM
        pos1 = (0.0, 0.0, 0.0)
        pos2 = (d, 0.0, 0.0)
        pos3 = (d/2.0, d*math.sqrt(3)/2.0, 0.0)
        return [pos1, pos2, pos3]
    
    def get_proton_position(self) -> Tuple[float, float, float]:
        """Position of the extra proton: geometric center of the 3-alpha triangle."""
        d = DIST_INTER_ALPHA_FM
        cx = (0.0 + d + d/2.0) / 3.0
        cy = (0.0 + 0.0 + d*math.sqrt(3)/2.0) / 3.0
        cz = 0.0
        return (cx, cy, cz)
    
    def calculate_inter_alpha_bonds(self) -> int:
        return 3  # triangle
    
    def calculate_inter_alpha_occlusion(self) -> float:
        """Inter-alpha occlusion (same as C-12) plus contribution from extra proton if needed."""
        return super().calculate_inter_alpha_occlusion()


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_second_layer():
    """Test second layer structure"""
    print("="*80)
    print("TEST: Second Layer Structure")
    print("="*80)
    
    # Create dummy first shell vertices (simplified)
    # In real implementation, would come from FirstShell
    import importlib.util
    from pathlib import Path
    _base_path = Path(__file__).parent / "01_01_icosahedral_base_geometry.py"
    spec = importlib.util.spec_from_file_location("base", _base_path)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    IcosahedralBase = base.IcosahedralBase
    base = IcosahedralBase(r=R_NUCLEON_FM)
    vertices = base.get_vertex_coordinates()
    
    # Create second layer
    second_layer = SecondLayer(vertices, nucleon_radius=R_NUCLEON_FM)
    
    print(f"\nSecond Layer Parameters:")
    print(f"  Total width: {second_layer.total_width:.3f} fm (10r)")
    print(f"  Number of interstices: {len(second_layer.interstices)}")
    
    if second_layer.interstices:
        print(f"\nFirst 3 Interstices:")
        for inter in second_layer.interstices[:3]:
            print(f"  Interstice {inter.index}:")
            print(f"    Face vertices: {inter.face_vertices}")
            print(f"    Position: ({inter.center_position[0]:.3f}, "
                  f"{inter.center_position[1]:.3f}, {inter.center_position[2]:.3f})")
            print(f"    Radius: {inter.radius:.3f} fm")
    
    # Verify isolation
    isolation = second_layer.verify_isolation()
    print(f"\nIsolation Verification:")
    print(f"  All isolated: {isolation['all_isolated']}")
    print(f"  Minimum separation: {isolation['min_separation']:.3f} fm")
    if isolation['violations']:
        print(f"  Violations:")
        for violation in isolation['violations'][:3]:
            print(f"    - {violation}")
    
    # Test alpha cluster arrangements
    print(f"\nAlpha Cluster Arrangements:")
    
    c12 = Carbon12Arrangement()
    print(f"\nCarbon-12 (3-alpha triangle):")
    print(f"  Inter-alpha bonds: {c12.calculate_inter_alpha_bonds()}")
    print(f"  Inter-alpha occlusion: {c12.calculate_inter_alpha_occlusion():.3f} sr")
    
    o16 = Oxygen16Arrangement()
    print(f"\nOxygen-16 (4-alpha tetrahedron):")
    print(f"  Inter-alpha bonds: {o16.calculate_inter_alpha_bonds()}")
    print(f"  Inter-alpha occlusion: {o16.calculate_inter_alpha_occlusion():.3f} sr")
    
    n14 = Nitrogen14Arrangement()
    print(f"\nNitrogen-14 (3-alpha triangle + 1p):")
    print(f"  Inter-alpha bonds: {n14.calculate_inter_alpha_bonds()}")
    print(f"  Inter-alpha occlusion: {n14.calculate_inter_alpha_occlusion():.3f} sr")
    print(f"  Extra proton position: {n14.get_proton_position()}")


if __name__ == "__main__":
    test_second_layer()
