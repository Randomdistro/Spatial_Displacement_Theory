#!/usr/bin/env python3
"""
Phase 1.1: Icosahedral Base Geometry

Establishes the fundamental icosahedral packing structure:
- Central sphere at origin
- 12 outer spheres in icosahedral arrangement
- Two octahedral interstitial spaces
- Complete coordinate system and distance calculations

This is the foundation for all nuclear packing geometry.
"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
import math

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

# Nucleon radii (from Phase 19, CODATA 2018)
R_P = 0.84e-15  # m (proton radius, 0.84 fm)
R_N = 0.87e-15  # m (neutron radius, 0.87 fm)
R_NUCLEON = 0.84e-15  # m (used for packing calculations, treat as equal)

# Convert to femtometers for convenience
R_P_FM = 0.84  # fm
R_N_FM = 0.87  # fm
R_NUCLEON_FM = 0.84  # fm

# ============================================================================
# ICOSAHEDRAL COORDINATE SYSTEM
# ============================================================================

@dataclass
class IcosahedralVertex:
    """Represents one vertex of the icosahedral arrangement"""
    index: int  # 0-11
    r: float  # Radial distance from center
    theta: float  # Azimuthal angle (0 to 2*pi)
    phi: float  # Polar angle (0 to pi)
    x: float  # Cartesian x
    y: float  # Cartesian y
    z: float  # Cartesian z
    
    def distance_to(self, other: 'IcosahedralVertex') -> float:
        """Calculate distance to another vertex"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)


class IcosahedralBase:
    """
    Icosahedral base structure: 12 spheres arranged around central sphere.
    
    Structure:
    - Central sphere: radius r, at origin
    - 12 outer spheres: each radius r, centers at distance 2r from origin
    - Each outer sphere center is exactly 2r from every other outer sphere center
    - Total width: 6r (central + 2 layers of radius r spheres)
    """
    
    def __init__(self, r: float = R_NUCLEON_FM):
        """
        Initialize icosahedral base structure.
        
        Parameters:
        -----------
        r : float
            Sphere radius (default: 0.84 fm)
        """
        self.r = r
        self.central_sphere_radius = r
        self.outer_sphere_radius = r
        self.outer_sphere_distance = 2.0 * r  # Centers at 2r from origin
        self.total_width = 6.0 * r  # Central + 2 layers
        
        # Generate icosahedral vertices
        self.vertices = self._generate_icosahedral_vertices()
        
        # Calculate octahedral spaces
        self.octahedral_spaces = self._identify_octahedral_spaces()
    
    def _generate_icosahedral_vertices(self) -> List[IcosahedralVertex]:
        """
        Generate 12 vertices of icosahedron in spherical coordinates.
        
        Icosahedron has 12 vertices arranged such that:
        - All vertices are equidistant from center
        - All vertices are equidistant from each other
        - Arranged in alternating polar angles
        
        Returns:
        --------
        List[IcosahedralVertex]
            List of 12 vertices
        """
        vertices = []
        r = self.outer_sphere_distance
        
        # Icosahedral golden ratio
        phi_icosa = (1.0 + math.sqrt(5.0)) / 2.0  # ~1.618
        
        # Generate vertices using icosahedral symmetry
        # Standard icosahedron coordinates
        # 12 vertices: (0, ±1, ±φ), (±1, ±φ, 0), (±φ, 0, ±1) and permutations
        # Normalize to distance 2r from origin
        
        # First set: (0, +/-1, +/-phi_icosa)
        scale = r / math.sqrt(1.0 + phi_icosa*phi_icosa)
        for sign1 in [-1, 1]:
            for sign2 in [-1, 1]:
                x = 0.0
                y = sign1 * scale
                z = sign2 * scale * phi_icosa
                vertices.append(self._create_vertex(len(vertices), x, y, z))
        
        # Second set: (+/-1, +/-phi_icosa, 0)
        for sign1 in [-1, 1]:
            for sign2 in [-1, 1]:
                x = sign1 * scale
                y = sign2 * scale * phi_icosa
                z = 0.0
                vertices.append(self._create_vertex(len(vertices), x, y, z))
        
        # Third set: (+/-phi_icosa, 0, +/-1)
        for sign1 in [-1, 1]:
            for sign2 in [-1, 1]:
                x = sign1 * scale * phi_icosa
                y = 0.0
                z = sign2 * scale
                vertices.append(self._create_vertex(len(vertices), x, y, z))
        
        # Verify all vertices are at correct distance
        for v in vertices:
            dist = math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
            if abs(dist - r) > 1e-6:
                # Renormalize
                scale_factor = r / dist
                v.x *= scale_factor
                v.y *= scale_factor
                v.z *= scale_factor
                # Recalculate spherical coordinates
                v.r = r
                v.theta = math.atan2(v.y, v.x)
                v.phi = math.acos(v.z / r)
        
        return vertices[:12]  # Ensure exactly 12
    
    def _create_vertex(self, index: int, x: float, y: float, z: float) -> IcosahedralVertex:
        """Create vertex from Cartesian coordinates"""
        r = math.sqrt(x*x + y*y + z*z)
        theta = math.atan2(y, x)  # Azimuthal (0 to 2*pi)
        phi = math.acos(z / r) if r > 0 else 0.0  # Polar (0 to pi)
        
        return IcosahedralVertex(
            index=index,
            r=r,
            theta=theta,
            phi=phi,
            x=x,
            y=y,
            z=z
        )
    
    def _identify_octahedral_spaces(self) -> List[dict]:
        """
        Identify the two octahedral interstitial spaces.
        
        Octahedral spaces are zones where:
        - 5 surrounding positions (from 5 nearest outer spheres)
        - 1 reference position (the "fourth wall")
        - Total: 6 positions per octahedral space
        
        These are the zones on opposite sides where 2 dots are slightly
        more than 2r apart, creating space for additional nucleons.
        
        Returns:
        --------
        List[dict]
            List of two octahedral space descriptions
        """
        # Find pairs of vertices that are slightly more than 2r apart
        # These indicate octahedral spaces
        octahedral_spaces = []
        
        # Calculate all pairwise distances
        distances = []
        for i, v1 in enumerate(self.vertices):
            for j, v2 in enumerate(self.vertices[i+1:], start=i+1):
                dist = v1.distance_to(v2)
                distances.append({
                    'i': i,
                    'j': j,
                    'distance': dist,
                    'expected': 2.0 * self.r
                })
        
        # Find distances that are larger than expected (indicating octahedral spaces)
        # Sort by excess distance
        distances.sort(key=lambda d: d['distance'] - d['expected'], reverse=True)
        
        # The two largest excesses indicate the two octahedral spaces
        # Each space is associated with a pair of vertices that are further apart
        for idx in range(min(2, len(distances))):
            d = distances[idx]
            space = {
                'index': idx,
                'vertex_pair': (d['i'], d['j']),
                'separation': d['distance'],
                'expected_separation': d['expected'],
                'excess': d['distance'] - d['expected'],
                'description': f"Octahedral space {idx+1}: between vertices {d['i']} and {d['j']}"
            }
            octahedral_spaces.append(space)
        
        return octahedral_spaces
    
    def get_vertex_coordinates(self) -> List[Tuple[float, float, float]]:
        """
        Get Cartesian coordinates of all 12 vertices.
        
        Returns:
        --------
        List[Tuple[float, float, float]]
            List of (x, y, z) coordinates
        """
        return [(v.x, v.y, v.z) for v in self.vertices]
    
    def get_vertex_distances(self) -> np.ndarray:
        """
        Get distance matrix between all vertices.
        
        Returns:
        --------
        np.ndarray
            12x12 distance matrix (fm)
        """
        n = len(self.vertices)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    dist_matrix[i, j] = 0.0
                else:
                    dist_matrix[i, j] = self.vertices[i].distance_to(self.vertices[j])
        
        return dist_matrix
    
    def verify_icosahedral_structure(self) -> dict:
        """
        Verify that the structure matches icosahedral geometry.
        
        Checks:
        - All vertices at correct distance from center
        - All vertices equidistant from each other (within tolerance)
        - Two octahedral spaces identified
        
        Returns:
        --------
        dict
            Verification results
        """
        results = {
            'all_vertices_at_correct_distance': True,
            'vertices_equidistant': True,
            'octahedral_spaces_found': len(self.octahedral_spaces) == 2,
            'errors': []
        }
        
        # Check vertex distances from center
        for v in self.vertices:
            dist = math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
            if abs(dist - self.outer_sphere_distance) > 1e-3:
                results['all_vertices_at_correct_distance'] = False
                results['errors'].append(
                    f"Vertex {v.index}: distance {dist:.3f} fm, expected {self.outer_sphere_distance:.3f} fm"
                )
        
        # Check pairwise distances (should all be ~2r)
        dist_matrix = self.get_vertex_distances()
        pairwise_distances = []
        for i in range(len(self.vertices)):
            for j in range(i+1, len(self.vertices)):
                pairwise_distances.append(dist_matrix[i, j])
        
        if pairwise_distances:
            mean_dist = np.mean(pairwise_distances)
            std_dist = np.std(pairwise_distances)
            expected_dist = 2.0 * self.r
            
            if std_dist / mean_dist > 0.1:  # More than 10% variation
                results['vertices_equidistant'] = False
                results['errors'].append(
                    f"Pairwise distances: mean={mean_dist:.3f} fm, std={std_dist:.3f} fm, "
                    f"expected={expected_dist:.3f} fm"
                )
        
        return results
    
    def calculate_solid_angle_occlusion(self, observer_position: Tuple[float, float, float], 
                                       observer_distance: float) -> float:
        """
        Calculate total solid angle occlusion from icosahedral base.
        
        Parameters:
        -----------
        observer_position : Tuple[float, float, float]
            Position of observer in Cartesian coordinates (fm)
        observer_distance : float
            Distance from center to observer (fm)
        
        Returns:
        --------
        float
            Total solid angle occlusion (steradians)
        """
        total_occlusion = 0.0
        
        # Occlusion from central sphere
        if observer_distance > self.central_sphere_radius:
            sin_theta_center = self.central_sphere_radius / observer_distance
            if sin_theta_center < 1.0:
                cos_theta_center = math.sqrt(1.0 - sin_theta_center*sin_theta_center)
                omega_center = 2.0 * math.pi * (1.0 - cos_theta_center)
                total_occlusion += omega_center
        
        # Occlusion from 12 outer spheres
        for vertex in self.vertices:
            # Distance from observer to vertex center
            dx = vertex.x - observer_position[0]
            dy = vertex.y - observer_position[1]
            dz = vertex.z - observer_position[2]
            dist_to_vertex = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if dist_to_vertex > self.outer_sphere_radius:
                sin_theta = self.outer_sphere_radius / dist_to_vertex
                if sin_theta < 1.0:
                    cos_theta = math.sqrt(1.0 - sin_theta*sin_theta)
                    omega = 2.0 * math.pi * (1.0 - cos_theta)
                    total_occlusion += omega
        
        return total_occlusion


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_icosahedral_base():
    """Test icosahedral base structure"""
    print("="*80)
    print("TEST: Icosahedral Base Geometry")
    print("="*80)
    
    base = IcosahedralBase(r=R_NUCLEON_FM)
    
    print(f"\nStructure Parameters:")
    print(f"  Sphere radius: {base.r:.3f} fm")
    print(f"  Outer sphere distance: {base.outer_sphere_distance:.3f} fm")
    print(f"  Total width: {base.total_width:.3f} fm")
    
    print(f"\nVertices: {len(base.vertices)}")
    for v in base.vertices[:3]:  # Show first 3
        print(f"  Vertex {v.index}: r={v.r:.3f} fm, theta={math.degrees(v.theta):.1f} deg, "
              f"phi={math.degrees(v.phi):.1f} deg, pos=({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")
    
    print(f"\nOctahedral Spaces: {len(base.octahedral_spaces)}")
    for space in base.octahedral_spaces:
        print(f"  {space['description']}")
        print(f"    Separation: {space['separation']:.3f} fm (expected: {space['expected_separation']:.3f} fm)")
        print(f"    Excess: {space['excess']:.3f} fm")
    
    # Verification
    verification = base.verify_icosahedral_structure()
    print(f"\nVerification:")
    print(f"  All vertices at correct distance: {verification['all_vertices_at_correct_distance']}")
    print(f"  Vertices equidistant: {verification['vertices_equidistant']}")
    print(f"  Octahedral spaces found: {verification['octahedral_spaces_found']}")
    if verification['errors']:
        print(f"  Errors:")
        for error in verification['errors']:
            print(f"    - {error}")
    
    # Distance matrix
    dist_matrix = base.get_vertex_distances()
    print(f"\nDistance Matrix (first 3x3):")
    print(dist_matrix[:3, :3])
    print(f"  Mean pairwise distance: {np.mean(dist_matrix[dist_matrix > 0]):.3f} fm")
    print(f"  Expected: {2.0 * base.r:.3f} fm")
    
    # Solid angle occlusion test
    observer_pos = (10.0, 0.0, 0.0)  # 10 fm from center
    occlusion = base.calculate_solid_angle_occlusion(observer_pos, 10.0)
    print(f"\nSolid Angle Occlusion (at r=10 fm):")
    print(f"  Total occlusion: {occlusion:.3f} sr")
    print(f"  Fraction of 4pi: {occlusion / (4.0 * math.pi):.3f}")


if __name__ == "__main__":
    test_icosahedral_base()
