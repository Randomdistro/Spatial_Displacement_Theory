import math

# Constants
alpha_inv = 137.035999084
factor_18_412 = 18.412
m_p_m_e_ratio = 1836.152673

print(f"Investigating Factor: {factor_18_412}")
print("-" * 30)

# 1. Alpha / 18.412
val_alpha_div = alpha_inv / factor_18_412
print(f"Alpha Inv / 18.412: {val_alpha_div:.8f}")

# 2. 18.412 vs Proton/Electron Ratio
print(f"Proton/Electron Ratio / 100: {m_p_m_e_ratio / 100.0:.8f}")
print(f"Difference: {factor_18_412 - (m_p_m_e_ratio / 100.0):.8f}")

# 3. Wavelengths?
# User asked: "is that the beginning of a set of wavelengths"
# Maybe the result (7.44) is a wavelength in some units?
# 7.44 meters? 7.44 nm?
# Or maybe a frequency factor?

# 4. Check 7.6 vs 7.44
print(f"Previous 7.6 Factor: 7.6")
print(f"New Factor (from Alpha/18.412): {val_alpha_div:.8f}")

# 5. Check 992.4 relation
# 992.4 / 18.412
print(f"992.4 / 18.412: {992.4 / factor_18_412:.8f}") # ~53.9

# 6. Check 18.412^2
print(f"18.412^2: {factor_18_412**2:.8f}") # ~339
