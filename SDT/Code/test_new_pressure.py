import math

# Constants
P_old = 1.65e31
P_new = 1.76e31 # Derived Coulomb Energy Density
Ratio = P_new / P_old

print(f"Pressure Change: {P_old:.2e} -> {P_new:.2e} (Ratio: {Ratio:.4f})")

# 1. Proton Throughput
# Old: 2.373e16 W
E_dot_p_old = 2.373e16
E_dot_p_new = E_dot_p_old * Ratio
print(f"\n1. Proton Throughput:")
print(f"   Old: {E_dot_p_old:.3e} W")
print(f"   New: {E_dot_p_new:.3e} W")

# 2. Binding Energies
# Binding energy depends linearly on P_infinity in the Master Equation formulation:
# B = P * sum(A * Gamma * kappa * delta_eta) * tau
# So B scales linearly with P.

# Deuteron (2H)
B_2H_obs = 2.224 # MeV
B_2H_old_calc = 2.81 # From table 9.3 (Error 27%)
B_2H_new_calc = B_2H_old_calc * Ratio
print(f"\n2. Deuteron Binding Energy (Obs: {B_2H_obs} MeV):")
print(f"   Old Calc: {B_2H_old_calc:.2f} MeV (Error: {abs(B_2H_old_calc-B_2H_obs)/B_2H_obs*100:.1f}%)")
print(f"   New Calc: {B_2H_new_calc:.2f} MeV (Error: {abs(B_2H_new_calc-B_2H_obs)/B_2H_obs*100:.1f}%)")

# Alpha (4He)
B_4He_obs = 28.296 # MeV
B_4He_old_calc = 28.2 # From text (Error 0.3%)
B_4He_new_calc = B_4He_old_calc * Ratio
print(f"\n3. Alpha Binding Energy (Obs: {B_4He_obs} MeV):")
print(f"   Old Calc: {B_4He_old_calc:.2f} MeV (Error: {abs(B_4He_old_calc-B_4He_obs)/B_4He_obs*100:.1f}%)")
print(f"   New Calc: {B_4He_new_calc:.2f} MeV (Error: {abs(B_4He_new_calc-B_4He_obs)/B_4He_obs*100:.1f}%)")

# Iron-56 (56Fe)
B_56Fe_obs = 492.26 # MeV
B_56Fe_old_calc = 486.8 # From text (Error 1.1%)
B_56Fe_new_calc = B_56Fe_old_calc * Ratio
print(f"\n4. Iron-56 Binding Energy (Obs: {B_56Fe_obs} MeV):")
print(f"   Old Calc: {B_56Fe_old_calc:.1f} MeV (Error: {abs(B_56Fe_old_calc-B_56Fe_obs)/B_56Fe_obs*100:.1f}%)")
print(f"   New Calc: {B_56Fe_new_calc:.1f} MeV (Error: {abs(B_56Fe_new_calc-B_56Fe_obs)/B_56Fe_obs*100:.1f}%)")

print(f"\nConclusion:")
if abs(B_56Fe_new_calc - B_56Fe_obs) < abs(B_56Fe_old_calc - B_56Fe_obs):
    print("The new pressure IMPROVES accuracy for heavy nuclei.")
else:
    print("The new pressure WORSENS accuracy (overbinding).")
    print("However, (1-eta) was fitted to the OLD pressure.")
    print("We can simply retune (1-eta) by 6% to restore accuracy.")
