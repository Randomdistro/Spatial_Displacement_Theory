import math

# Constants
c = 299792458.0
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv
r_e = 2.8179403227e-15 # Classical Electron Radius
R_H = 5.29177210903e-11 # Bohr Radius

print(f"Classical Electron Radius (r_e): {r_e:.4e} m")
print(f"Bohr Radius (R_H): {R_H:.4e} m")

# 1. Verify the Scaling
# Hypothesis: R_H = r_e / alpha^2
R_H_calc = r_e / alpha**2
print(f"Calculated Bohr Radius (r_e / alpha^2): {R_H_calc:.4e} m")
print(f"Ratio R_H / R_H_calc: {R_H / R_H_calc:.6f}") # Should be 1.0

# 2. Orbital Velocity at r_e
# Hypothesis: v = c at r_e
# Check Keplerian scaling: v ~ 1/sqrt(r)
# v(r_e) = v(R_H) * sqrt(R_H / r_e)
v_H = c * alpha
v_re = v_H * math.sqrt(R_H / r_e)
print(f"Velocity at Bohr Radius: {v_H:.4e} m/s")
print(f"Velocity at r_e (Keplerian): {v_re:.4e} m/s")
print(f"Ratio v_re / c: {v_re / c:.6f}") # Should be 1.0

# 3. Rotation of Tidally Locked Electron at r_e
# Angular Velocity omega = v / r
omega = c / r_e
freq = omega / (2.0 * math.pi)
period = 1.0 / freq

print(f"Angular Velocity (omega): {omega:.4e} rad/s")
print(f"Frequency (Hz): {freq:.4e} Hz")
print(f"Period (s): {period:.4e} s")

# Compare to Zitterbewegung
# f_zitt = 2 m c^2 / h = c / lambda_C
lambda_C = 2.42631023867e-12
f_zitt = c / lambda_C
print(f"Zitterbewegung Frequency: {f_zitt:.4e} Hz")
print(f"Ratio freq / f_zitt: {freq / f_zitt:.4f}") # Expect 137?

# 4. Rotation at "Orbital Point c"
# User asks: "what would the rotation of the electron be at orbital point c?"
# Answer is omega.
