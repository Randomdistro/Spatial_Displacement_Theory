import math

# Constants
c = 299792458.0
Planck_Length = 1.616255e-35
Planck_Time = 5.391247e-44
Proton_Radius = 8.41e-16

# User Values
val1 = 1.0 / c
val2 = val1 ** 2
val3 = val1 ** 3

# Geometric Value
# 1 m^2 sphere surface area -> radius
# 4 * pi * r^2 = 1
r_sphere = math.sqrt(1.0 / (4.0 * math.pi))

print(f"c = {c}")
print(f"Planck Length = {Planck_Length}")
print(f"Planck Time = {Planck_Time}")
print("-" * 30)
print(f"Value 1 (1/c): {val1:.8e}")
print(f"Value 2 (1/c^2): {val2:.8e}")
print(f"Value 3 (1/c^3): {val3:.8e}")
print(f"Radius (1m^2 sphere): {r_sphere:.8e}")
print("-" * 30)

# Scaling Down
# Hypothesis: The sequence continues 1/c^4, 1/c^5...
val4 = val1 ** 4
val5 = val1 ** 5
val6 = val1 ** 6

print(f"Value 4 (1/c^4): {val4:.8e}")
print(f"  Ratio to Planck Length: {val4 / Planck_Length:.4f}")

print(f"Value 5 (1/c^5): {val5:.8e}")
print(f"  Ratio to Planck Time: {val5 / Planck_Time:.4f}")

print("-" * 30)
# Scaling the Radius
# User said "scale these three values down".
# Maybe scale the Radius by 1/c?
r_scaled_1 = r_sphere * val1
r_scaled_2 = r_sphere * val2
r_scaled_3 = r_sphere * val3
r_scaled_4 = r_sphere * val4

print(f"Radius * (1/c): {r_scaled_1:.8e}")
print(f"Radius * (1/c^2): {r_scaled_2:.8e}")
print(f"Radius * (1/c^3): {r_scaled_3:.8e}")
print(f"Radius * (1/c^4): {r_scaled_4:.8e}")
print(f"  Ratio to Planck Length: {r_scaled_4 / Planck_Length:.4f}")

# Check if any hit Proton Radius
print(f"Ratio r_scaled_2 / Proton Radius: {r_scaled_2 / Proton_Radius:.4f}")
