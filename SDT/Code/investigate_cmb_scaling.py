import math

# Constants
P_CMB = 2.036e-2 # Pa (Macro scale)
P_nuc = 1.65e31  # Pa (Micro scale)
Ratio = P_nuc / P_CMB
print(f"Pressure Ratio (P_nuc / P_CMB): {Ratio:.4e}")
print(f"Log10(Ratio): {math.log10(Ratio):.4f}")

# Scales
R_proton = 8.40e-16 # m
R_universe = 4.4e26 # m (Observable universe radius ~46 Gly)
Scale_Ratio = R_universe / R_proton
print(f"\nScale Ratio (R_univ / R_p): {Scale_Ratio:.4e}")
print(f"Log10(Scale Ratio): {math.log10(Scale_Ratio):.4f}")

# Hypothesis 1: Inverse Square Scaling
# P_micro = P_macro * (Scale_Ratio)^2 ?
P_pred_sq = P_CMB * (Scale_Ratio)**2
print(f"\nInverse Square Prediction: {P_pred_sq:.4e} Pa")
# Result: 2e-2 * (10^42)^2 = 2e82. Too big.

# Hypothesis 2: Linear Scaling?
P_pred_lin = P_CMB * Scale_Ratio
print(f"Linear Prediction: {P_pred_lin:.4e} Pa")
# Result: 2e-2 * 10^42 = 2e40. Still too big (Target 10^31).

# Hypothesis 3: "Halve and Double" (Powers of 2)
# How many "doublings" or "halvings" between the scales?
# Log2(Ratio)?
doublings = math.log2(Ratio)
print(f"\nDoublings (Log2(Pressure Ratio)): {doublings:.4f}")
# 10^33 is approx 2^110.

# Log2(Scale Ratio)?
scale_doublings = math.log2(Scale_Ratio)
print(f"Scale Doublings (Log2(Scale Ratio)): {scale_doublings:.4f}")
# 10^42 is approx 2^140.

# Is there a relation? 110 vs 140.
# Maybe related to 3/4? (110/140 = 0.78).

# Hypothesis 4: Energy Density Conservation with Volume/Area?
# Energy = P * V.
# If Energy is conserved?
# P_nuc * V_nuc = P_CMB * V_univ?
# P_nuc / P_CMB = V_univ / V_nuc = (R_univ / R_p)^3.
# This would be huge (10^126).

# Hypothesis 5: Force Conservation?
# P_nuc * A_nuc = P_CMB * A_univ?
# P_nuc / P_CMB = (R_univ / R_p)^2.
# Still 10^84.

# Hypothesis 6: "Halve and Double" - Geometric Progression
# User said "halve and double".
# Maybe it's related to the number of "steps" down the fractal?
# 128 steps? (2^128?)
# 2^128 = 3.4e38. Close to 10^33?
# 2^110 = 1.3e33.
# 2^109 = 6.5e32.
# 2^104 = 2e31.
# 104 doublings?

# Let's check 2^103.
print(f"\n2^103 * P_CMB = {2**103 * P_CMB:.4e}")
# 2.0e-2 * 1e31 = 2e29.
print(f"2^109 * P_CMB = {2**109 * P_CMB:.4e}")
# 1.3e31. Close!
print(f"2^110 * P_CMB = {2**110 * P_CMB:.4e}")
# 2.6e31.

# So P_nuc approx P_CMB * 2^109.5.
# Where does 109.5 come from?
# 1/alpha? 137?
# Proton/Electron mass ratio? 1836?

# Let's check the "Spation Matrix" Bulk Modulus.
# K_bulk = 4.6e113.
# P_nuc = 1.65e31.
# Ratio = 10^82.
# 10^82 is (10^41)^2.
# (Scale Ratio)^2 !
print(f"\nK_bulk / P_nuc = {4.6e113 / 1.65e31:.4e}")
print(f"(Scale Ratio)^2 = {Scale_Ratio**2:.4e}")
# 2.7e82 vs 2.7e83.
# This looks like a match!
# K_bulk / P_nuc approx (R_univ / R_p)^2.
# So P_nuc = K_bulk * (R_p / R_univ)^2.

# Let's verify this.
# If K_bulk is the "Stiffness at Planck Scale" or "Universe Scale"?
# User said "bulk modulus is the pressure that keeps everything together at the planck scale".
# So maybe K_bulk is the Planck Pressure?
# P_planck = c^7 / (hbar G^2) approx 4.6e113.
# Yes, K_bulk IS the Planck Pressure.

# So the relation is:
# P_nuc = P_planck * (R_planck / R_p)^?
# Let's check R_planck / R_p.
R_planck = 1.616e-35
ratio_p_pl = R_proton / R_planck
print(f"\nR_p / R_planck = {ratio_p_pl:.4e} (10^19)")
# P_nuc / P_planck = 10^31 / 10^113 = 10^-82.
# (10^19)^-4 = 10^-76.
# (10^19)^-4.something?

# Wait, look at the previous match:
# K_bulk / P_nuc approx (R_univ / R_p)^2.
# 10^113 / 10^31 = 10^82.
# (10^26 / 10^-15)^2 = (10^41)^2 = 10^82.
# So P_nuc = K_bulk * (R_p / R_univ)^2.
# This links the Macro (Universe) and Micro (Proton) to the Bulk Modulus.

# But user said "P_CMB is the energy injected".
# P_CMB = 2e-2.
# P_nuc = 1.65e31.
# Ratio = 10^33.
# Is there a relation between P_CMB and P_nuc?
# Maybe P_nuc = P_CMB * (R_univ / R_p)?
# 2e-2 * 10^41 = 2e39. Too big.

# Maybe P_nuc = P_CMB * (R_univ / R_p)^(3/4)?
