import math

# Constants
c = 299792458.0
r_e = 2.8179403227e-15 # Classical Electron Radius (c-boundary)
R_p = 0.841235667e-15 # Proton Radius (CODATA 2018 is 0.8414, user uses 0.84?)

print(f"c-Boundary (r_e): {r_e:.4e} m")
print(f"Proton Surface (R_p): {R_p:.4e} m")

# 1. Velocity Scaling
# Hypothesis: v ~ 1/sqrt(r) (Keplerian)
# v(R_p) = c * sqrt(r_e / R_p)
ratio_r = r_e / R_p
v_p_kepler = c * math.sqrt(ratio_r)

print(f"Radius Ratio (r_e / R_p): {ratio_r:.4f}")
print(f"Velocity at Proton Surface (Keplerian): {v_p_kepler:.4e} m/s")
print(f"  Ratio v / c: {v_p_kepler / c:.4f}") # Expect ~1.83

# 2. Rotation Frequency
# omega = v / r
omega_p = v_p_kepler / R_p
freq_p = omega_p / (2.0 * math.pi)

print(f"Angular Velocity (omega): {omega_p:.4e} rad/s")
print(f"Frequency (Hz): {freq_p:.4e} Hz")

# 3. Compare to c-Boundary Frequency
omega_e = c / r_e
freq_e = omega_e / (2.0 * math.pi)
print(f"Frequency at c-Boundary: {freq_e:.4e} Hz")
print(f"Ratio freq_p / freq_e: {freq_p / freq_e:.4f}")

# 4. Compare to Zitterbewegung
f_zitt = 1.23558996e20
print(f"Ratio freq_p / f_zitt: {freq_p / f_zitt:.4f}")

# 5. Check Vortex Scaling (1/r) just in case
v_p_vortex = c * ratio_r
print(f"Velocity (Vortex 1/r): {v_p_vortex / c:.4f} c") # Expect ~3.35
