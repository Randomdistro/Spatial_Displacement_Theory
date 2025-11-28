import math
from sdt_core.constants import C_LATTICE, ALPHA_CURV, CELESTIAL_BODIES

# Constants (CODATA 2018 / SDT)
c = 299792458
h = 6.62607015e-34
hbar = h / (2 * math.pi)
me = 9.10938356e-31
e = 1.602176634e-19
epsilon0 = 8.8541878128e-12
alpha = 7.2973525693e-3  # Fine structure constant

def test_lamb_shift():
    print("--- Testing Lamb Shift (Torus Threading Model) ---")
    
    # Formula: Delta E ~ me * c^2 * alpha^5 * ln(1/alpha)
    # This is the scaling derived from the hole pressure deficit model
    
    E_rest = me * c**2  # Joules
    E_rest_eV = E_rest / e
    
    factor = alpha**5 * math.log(1/alpha)
    
    delta_E_J = E_rest * factor
    delta_E_eV = delta_E_J / e
    
    # Convert to Frequency (Hz)
    # E = h * f  =>  f = E / h
    freq = delta_E_J / h
    freq_MHz = freq / 1e6
    
    print(f"Rest Energy (eV): {E_rest_eV:.6e}")
    print(f"Alpha: {alpha}")
    print(f"Scaling Factor (alpha^5 * ln(1/alpha)): {factor:.6e}")
    print(f"Calculated Shift (eV): {delta_E_eV:.6e}")
    print(f"Calculated Frequency (MHz): {freq_MHz:.2f}")
    print(f"Observed Lamb Shift (H, n=2): ~1057 MHz")
    
    error = abs(freq_MHz - 1057) / 1057 * 100
    print(f"Discrepancy: {error:.2f}%")
    
    # Check if it's within order of magnitude (the model claims scaling, not exact coeff yet)
    if error < 50: # The coefficient might be 1/pi or similar, checking scaling validity
        print("RESULT: PASS (Scaling confirmed)")
    else:
        print("RESULT: FAIL (Scaling incorrect)")

def test_hyperfine_scaling():
    print("\n--- Testing Hyperfine Scaling ---")
    # Hyperfine is order alpha^4 * (me/mp) roughly, or alpha^2 * magnetic moment ratio
    # The Torus model says it's geometric alignment.
    # Let's check the magnitude of the "flow alignment" energy if it's ~ alpha^2 * Rydberg
    
    Rydberg_J = 2.179872e-18 # 13.6 eV
    
    # HFS is ~ 5.9e-6 eV
    HFS_eV = 5.874e-6
    HFS_J = HFS_eV * e
    
    ratio = HFS_J / Rydberg_J
    print(f"Observed Hyperfine/Rydberg Ratio: {ratio:.6e}")
    
    # Check if this matches alpha^2 * (me/mp)
    mp = 1.6726219e-27
    mass_ratio = me / mp
    
    predicted_ratio = alpha**2 * mass_ratio
    print(f"Predicted Ratio (alpha^2 * me/mp): {predicted_ratio:.6e}")
    
    error = abs(ratio - predicted_ratio) / ratio * 100
    print(f"Difference: {error:.2f}%")
    
    if error < 50:
        print("RESULT: PASS (Geometric scaling consistent with mass ratio)")
    else:
        print("RESULT: FAIL")

if __name__ == "__main__":
    test_lamb_shift()
    test_hyperfine_scaling()
