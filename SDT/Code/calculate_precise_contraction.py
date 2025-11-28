import math

# Constants
c = 299792458.0
h = 6.62607015e-34
m_e = 9.10938356e-31
lambda_C = h / (m_e * c) # Compton Wavelength
alpha_inv = 137.035999084
alpha = 1.0 / alpha_inv

print(f"Compton Wavelength (Rest): {lambda_C:.20e} m")

print(f"| n | Beta (v/c) | Gamma | Length (m) | Delta (Rest - L) |")
print(f"|---|---|---|---|---|")

for n in range(1, 10):
    v_n = (c * alpha) / n
    beta = v_n / c
    # Precise Gamma: 1 / sqrt(1 - beta^2)
    # For small beta, gamma ~ 1 + 0.5*beta^2
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    
    L_n = lambda_C / gamma
    delta = lambda_C - L_n
    
    print(f"| {n} | {beta:.4e} | {gamma:.10f} | {L_n:.20e} | {delta:.4e} |")

# Check if Delta relates to anything
# Delta_1 ~ lambda_C * 0.5 * beta^2
# beta = alpha
# Delta_1 ~ lambda_C * 0.5 * alpha^2
val_check = lambda_C * 0.5 * alpha**2
print(f"\nCheck: lambda_C * 0.5 * alpha^2 = {val_check:.4e}")
