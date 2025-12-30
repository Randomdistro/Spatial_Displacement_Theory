#!/usr/bin/env python3
"""
Calculate octahedral defects in second layer of icosahedral/dodecahedral packing
"""

import math

# Icosahedral geometry constants
# Icosahedron: 12 vertices, 20 faces, 30 edges
# Dodecahedron (dual): 20 vertices, 12 faces, 30 edges

# For icosahedral close packing:
# First shell: 12 spheres around center
# Octahedral sites in first shell: 2 (the two octahedral spaces)

# Second layer: Next icosahedral arrangement
# Need to calculate octahedral interstitial sites

def calculate_octahedral_sites_second_layer():
    """
    Calculate number of octahedral defects in second layer
    
    In icosahedral close packing:
    - First shell: 12 vertices (icosahedron)
    - Octahedral sites require 6 neighbors
    
    For second layer:
    - The next icosahedral arrangement creates new positions
    - Octahedral sites appear where 6 spheres form octahedral coordination
    """
    
    # Icosahedron has 12 vertices
    # Each vertex can be part of multiple octahedral arrangements
    
    # In close packing, octahedral sites typically appear:
    # - Between layers (interstitial sites)
    # - At positions where 6 neighbors form octahedron
    
    # For icosahedral packing specifically:
    # The dodecahedron (20 vertices) interpenetrates the icosahedron
    # Each dodecahedral vertex sits at center of icosahedral face (20 faces)
    
    # However, octahedral coordination requires 6 neighbors, not 5 (pentagonal)
    # So not all dodecahedral positions are octahedral
    
    # Let's calculate from known geometry:
    # - Icosahedron: 12 vertices, 20 faces
    # - Dodecahedron: 20 vertices, 12 faces
    # - They are duals
    
    # For octahedral sites in second layer:
    # Need positions where 6 neighbors can form octahedron
    
    # In icosahedral close packing, the second layer positions
    # are determined by the next icosahedral arrangement
    
    # Actually calculating this requires:
    # 1. Position of first shell spheres
    # 2. Position of second shell spheres
    # 3. Finding positions where 6 neighbors form octahedron
    
    # From geometric principles:
    # If we have N spheres in first shell, and M spheres in second shell,
    # octahedral sites appear at specific geometric positions
    
    # For icosahedral packing:
    # First shell: 12 spheres
    # Second shell: Next icosahedral arrangement (also 12 positions, but offset)
    
    # Octahedral sites in second layer:
    # These are positions where a sphere can be placed with 6 neighbors
    # forming octahedral coordination
    
    # Without exact coordinates, we can estimate:
    # - Each icosahedral face (20 faces) could potentially host an octahedral site
    # - But octahedral requires 6 neighbors, not 5 (pentagonal face)
    
    # More precisely:
    # The second layer has positions where building blocks stack
    # The number of octahedral-like sites depends on the specific arrangement
    
    # For now, let's use the fact that:
    # - C-12 has 3 alphas in triangular arrangement
    # - O-16 has 4 alphas in tetrahedral arrangement  
    # - Mg-24 has 6 alphas in octahedral arrangement
    
    # This suggests the second layer can accommodate at least 6 positions
    # in octahedral arrangement
    
    # But we need the exact count of octahedral DEFECTS (empty sites)
    # not occupied positions
    
    print("Calculating octahedral defects in second layer...")
    print("\nFirst shell:")
    print("  - 12 icosahedral vertices")
    print("  - 2 octahedral spaces (filled by deuteron + helium deuteron)")
    print("  - Total: 14 positions")
    
    print("\nSecond layer geometry:")
    print("  - Icosahedron: 12 vertices, 20 triangular faces")
    print("  - Dodecahedron (dual): 20 vertices, 12 pentagonal faces")
    print("  - They interpenetrate")
    
    print("\nOctahedral sites require 6 neighbors")
    print("  - Icosahedral faces are triangular (3 neighbors)")
    print("  - Dodecahedral faces are pentagonal (5 neighbors)")
    print("  - Neither directly provides 6 neighbors")
    
    print("\nFor second layer octahedral defects:")
    print("  - Need positions where 6 neighbors can form octahedron")
    print("  - These appear at specific interstitial positions")
    print("  - Between the icosahedral and dodecahedral structures")
    
    # From the building block arrangements:
    # - 3 alphas (C-12): triangular
    # - 4 alphas (O-16): tetrahedral
    # - 6 alphas (Mg-24): octahedral
    
    # This suggests the second layer can accommodate multiple positions
    # The exact count of OCTAHEDRAL defects (empty octahedral sites)
    # depends on how many are occupied vs available
    
    # For a complete answer, we'd need:
    # 1. Exact coordinates of first shell
    # 2. Exact coordinates of second shell positions
    # 3. Identification of which positions have 6 neighbors (octahedral)
    
    print("\nAnswer: The second layer has interstitial positions where")
    print("octahedral coordination can occur. The exact count of octahedral")
    print("DEFECTS (empty sites) depends on how many building blocks occupy")
    print("the second layer positions.")
    
    print("\nFrom observed arrangements:")
    print("  - C-12: 3 alphas (triangular) - uses 3 second layer positions")
    print("  - O-16: 4 alphas (tetrahedral) - uses 4 second layer positions")
    print("  - Mg-24: 6 alphas (octahedral) - uses 6 second layer positions")
    
    print("\nThis suggests the second layer has at least 6 positions available")
    print("for octahedral arrangement. The number of OCTAHEDRAL DEFECTS")
    print("would be: (total octahedral sites) - (occupied positions)")

if __name__ == '__main__':
    calculate_octahedral_sites_second_layer()

