#!/usr/bin/env python3
"""
Phase 1.5: Geometric Calculations

Comprehensive geometric calculation utilities:
- Spherical coordinate transformations
- Icosahedral coordinate transformations
- Distance and separation formulas
- Solid angle occlusion calculations
- Overlap and interference corrections

This provides the mathematical foundation for all nuclear geometry calculations.
"""

import numpy as np
from typing import Tuple, List, Optional
import math

# ============================================================================
# COORDINATE TRANSFORMATIONS
# ============================================================================

def cartesian_to_spherical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """
    Convert Cartesian to spherical coordinates.
    
    Spherical coordinates (r, theta, phi):
    - r: radial distance
    - theta: azimuthal angle (0 to 2*pi) - angle in xy-plane
    - phi: polar/zenith angle (0 to pi) - angle from z-axis
    
    Parameters:
    -----------
    x, y, z : float
        Cartesian coordinates
    
    Returns:
    --------
    (r, theta, phi) : Tuple[float, float, float]
        Spherical coordinates
    """
    r = math.sqrt(x*x + y*y + z*z)
    theta = math.atan2(y, x)  # Azimuthal (0 to 2*pi)
    phi = math.acos(z / r) if r > 0 else 0.0  # Polar (0 to pi)
    return (r, theta, phi)


def spherical_to_cartesian(r: float, theta: float, phi: float) -> Tuple[float, float, float]:
    """
    Convert spherical to Cartesian coordinates.
    
    Parameters:
    -----------
    r : float
        Radial distance
    theta : float
        Azimuthal angle (0 to 2*pi)
    phi : float
        Polar angle (0 to pi)
    
    Returns:
    --------
    (x, y, z) : Tuple[float, float, float]
        Cartesian coordinates
    """
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return (x, y, z)


def icosahedral_to_cartesian(vertex_index: int, r: float) -> Tuple[float, float, float]:
    """
    Convert icosahedral vertex index to Cartesian coordinates.
    
    Parameters:
    -----------
    vertex_index : int
        Vertex index (0-11)
    r : float
        Radial distance
    
    Returns:
    --------
    (x, y, z) : Tuple[float, float, float]
        Cartesian coordinates
    """
    # Icosahedral golden ratio
    phi_icosa = (1.0 + math.sqrt(5.0)) / 2.0
    
    # Standard icosahedron vertex coordinates (normalized)
    vertices_normalized = [
        (0, 1, phi_icosa),
        (0, -1, phi_icosa),
        (0, 1, -phi_icosa),
        (0, -1, -phi_icosa),
        (1, phi_icosa, 0),
        (-1, phi_icosa, 0),
        (1, -phi_icosa, 0),
        (-1, -phi_icosa, 0),
        (phi_icosa, 0, 1),
        (-phi_icosa, 0, 1),
        (phi_icosa, 0, -1),
        (-phi_icosa, 0, -1),
    ]
    
    if vertex_index < 0 or vertex_index >= len(vertices_normalized):
        raise ValueError(f"Vertex index {vertex_index} out of range [0, {len(vertices_normalized)-1}]")
    
    x_norm, y_norm, z_norm = vertices_normalized[vertex_index]
    
    # Normalize
    norm = math.sqrt(x_norm*x_norm + y_norm*y_norm + z_norm*z_norm)
    x = r * x_norm / norm
    y = r * y_norm / norm
    z = r * z_norm / norm
    
    return (x, y, z)


# ============================================================================
# DISTANCE CALCULATIONS
# ============================================================================

def distance_between_points(p1: Tuple[float, float, float], 
                            p2: Tuple[float, float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Parameters:
    -----------
    p1, p2 : Tuple[float, float, float]
        Cartesian coordinates of points
    
    Returns:
    --------
    float
        Distance
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def separation_in_octahedral_space(vertex1: Tuple[float, float, float],
                                  vertex2: Tuple[float, float, float]) -> float:
    """
    Calculate separation in octahedral space.
    
    Octahedral spaces are zones where vertices are slightly more than 2r apart.
    
    Parameters:
    -----------
    vertex1, vertex2 : Tuple[float, float, float]
        Positions of two vertices
    
    Returns:
    --------
    float
        Separation distance
    """
    return distance_between_points(vertex1, vertex2)


# ============================================================================
# SOLID ANGLE OCCLUSION
# ============================================================================

def spherical_occlusion(radius: float, distance: float) -> float:
    """
    Calculate solid angle occlusion of a sphere at a given distance.
    
    Formula: Omega = 2*pi*(1 - cos theta) where sin theta = R/d
    Geometric interpretation: observer at distance d from sphere center;
    sphere of radius R subtends solid angle Omega.
    
    Edge cases (physically correct):
    - d < R: observer inside sphere → full sky subtended → 4π sr
    - d = R: observer on sphere surface → hemisphere → 2π sr
    - d > R: standard formula
    
    Parameters:
    -----------
    radius : float
        Radius of occluding sphere (fm)
    distance : float
        Distance from observer to sphere center (fm)
    
    Returns:
    --------
    float
        Solid angle occlusion (steradians)
    """
    if distance <= 0.0:
        return 0.0
    if distance < radius:
        return 4.0 * math.pi  # Observer inside sphere: full sky
    if distance == radius:
        return 2.0 * math.pi  # Observer on surface: hemisphere
    
    sin_theta = radius / distance
    if sin_theta >= 1.0:
        return 2.0 * math.pi
    
    cos_theta = math.sqrt(1.0 - sin_theta * sin_theta)
    return 2.0 * math.pi * (1.0 - cos_theta)


def total_occlusion_from_spheres(observer_position: Tuple[float, float, float],
                                 sphere_positions: List[Tuple[float, float, float]],
                                 sphere_radius: float) -> float:
    """
    Calculate total solid angle occlusion from multiple spheres.
    
    Parameters:
    -----------
    observer_position : Tuple[float, float, float]
        Position of observer
    sphere_positions : List[Tuple[float, float, float]]
        Positions of occluding spheres
    sphere_radius : float
        Radius of each sphere
    
    Returns:
    --------
    float
        Total occlusion (steradians)
    """
    total = 0.0
    
    for sphere_pos in sphere_positions:
        distance = distance_between_points(observer_position, sphere_pos)
        occlusion = spherical_occlusion(sphere_radius, distance)
        total += occlusion
    
    # Cap at 4*pi (full sphere)
    return min(total, 4.0 * math.pi)


# ============================================================================
# OVERLAP AND INTERFERENCE CORRECTIONS
# ============================================================================

def calculate_overlap_correction(occlusion1: float, occlusion2: float,
                                 distance: float, radius: float) -> float:
    """
    Calculate overlap correction when two occlusions overlap.
    
    When spheres are close together, their occlusions overlap.
    This function estimates the overlap correction.
    
    Parameters:
    -----------
    occlusion1, occlusion2 : float
        Individual occlusions (steradians)
    distance : float
        Distance between sphere centers
    radius : float
        Sphere radius
    
    Returns:
    --------
    float
        Overlap correction (steradians to subtract)
    """
    if distance >= 2.0 * radius:
        return 0.0  # No overlap
    
    # Overlap is significant when distance < 2*radius
    # Simple model: overlap proportional to (2r - d) / (2r)
    overlap_fraction = (2.0 * radius - distance) / (2.0 * radius)
    overlap_fraction = max(0.0, min(1.0, overlap_fraction))
    
    # Overlap correction = average of two occlusions times overlap fraction
    avg_occlusion = (occlusion1 + occlusion2) / 2.0
    return avg_occlusion * overlap_fraction * 0.5  # Conservative estimate


def corrected_total_occlusion(observer_position: Tuple[float, float, float],
                              sphere_positions: List[Tuple[float, float, float]],
                              sphere_radius: float) -> float:
    """
    Calculate total occlusion with overlap corrections.
    
    Parameters:
    -----------
    observer_position : Tuple[float, float, float]
        Position of observer
    sphere_positions : List[Tuple[float, float, float]]
        Positions of occluding spheres
    sphere_radius : float
        Radius of each sphere
    
    Returns:
    --------
    float
        Corrected total occlusion (steradians)
    """
    # Calculate individual occlusions
    individual_occlusions = []
    for sphere_pos in sphere_positions:
        distance = distance_between_points(observer_position, sphere_pos)
        occlusion = spherical_occlusion(sphere_radius, distance)
        individual_occlusions.append(occlusion)
    
    # Sum individual occlusions
    total = sum(individual_occlusions)
    
    # Subtract overlaps
    n = len(sphere_positions)
    for i in range(n):
        for j in range(i+1, n):
            distance = distance_between_points(sphere_positions[i], sphere_positions[j])
            overlap = calculate_overlap_correction(
                individual_occlusions[i],
                individual_occlusions[j],
                distance,
                sphere_radius
            )
            total -= overlap
    
    # Cap at 4*pi
    return min(max(0.0, total), 4.0 * math.pi)


# ============================================================================
# TETRAHEDRAL GEOMETRY
# ============================================================================

def tetrahedral_center_to_vertex_distance(edge_length: float) -> float:
    """
    Calculate distance from center to vertex in regular tetrahedron.
    
    Parameters:
    -----------
    edge_length : float
        Length of tetrahedron edge
    
    Returns:
    --------
    float
        Distance from center to vertex
    """
    # For regular tetrahedron: r = d * sqrt(3/8)
    return edge_length * math.sqrt(3.0 / 8.0)


def tetrahedral_effective_radius(edge_length: float, nucleon_radius: float) -> float:
    """
    Calculate effective radius of tetrahedral cluster.
    
    Effective radius = distance to center + nucleon radius
    
    Parameters:
    -----------
    edge_length : float
        Length of tetrahedron edge
    nucleon_radius : float
        Radius of nucleon
    
    Returns:
    --------
    float
        Effective radius
    """
    center_distance = tetrahedral_center_to_vertex_distance(edge_length)
    return center_distance + nucleon_radius


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_geometric_calculations():
    """Test geometric calculations"""
    print("="*80)
    print("TEST: Geometric Calculations")
    print("="*80)
    
    # Coordinate transformations
    print("\nCoordinate Transformations:")
    x, y, z = 1.0, 2.0, 3.0
    r, theta, phi = cartesian_to_spherical(x, y, z)
    x2, y2, z2 = spherical_to_cartesian(r, theta, phi)
    print(f"  Cartesian: ({x:.3f}, {y:.3f}, {z:.3f})")
    print(f"  Spherical: r={r:.3f}, theta={math.degrees(theta):.1f} deg, phi={math.degrees(phi):.1f} deg")
    print(f"  Back to Cartesian: ({x2:.3f}, {y2:.3f}, {z2:.3f})")
    print(f"  Error: {distance_between_points((x,y,z), (x2,y2,z2)):.6f}")
    
    # Solid angle occlusion
    print("\nSolid Angle Occlusion:")
    R = 0.84  # fm
    d = 2.10  # fm (deuteron separation)
    occlusion = spherical_occlusion(R, d)
    print(f"  Sphere radius: {R:.3f} fm")
    print(f"  Distance: {d:.3f} fm")
    print(f"  Occlusion: {occlusion:.3f} sr")
    print(f"  Fraction of 4pi: {occlusion / (4.0 * math.pi):.3f}")
    
    # Multiple spheres
    print("\nMultiple Spheres:")
    observer = (10.0, 0.0, 0.0)
    spheres = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 2.0, 0.0)]
    total_occlusion = total_occlusion_from_spheres(observer, spheres, R)
    corrected_occlusion = corrected_total_occlusion(observer, spheres, R)
    print(f"  Observer position: {observer}")
    print(f"  Number of spheres: {len(spheres)}")
    print(f"  Total occlusion (no correction): {total_occlusion:.3f} sr")
    print(f"  Total occlusion (with correction): {corrected_occlusion:.3f} sr")
    
    # Tetrahedral geometry
    print("\nTetrahedral Geometry:")
    edge_length = 1.45  # fm (alpha internal separation)
    center_dist = tetrahedral_center_to_vertex_distance(edge_length)
    eff_radius = tetrahedral_effective_radius(edge_length, R)
    print(f"  Edge length: {edge_length:.3f} fm")
    print(f"  Center to vertex: {center_dist:.3f} fm")
    print(f"  Effective radius: {eff_radius:.3f} fm")


if __name__ == "__main__":
    test_geometric_calculations()
