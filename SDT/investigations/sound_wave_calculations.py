import math

# Constants
P_CMB = 2.036e-2  # Pa
P_ATM = 101325.0  # Pa (Standard Atmosphere)
RHO_AIR = 1.225   # kg/m^3
GAMMA_AIR = 1.4   # Adiabatic index
FREQ = 1000.0     # Hz
PRESSURE_AMPLITUDE = 1.0 # Pa (typical conversational sound)

# SDT Constants
K_BULK_SPATION = 4.6e113 # Pa
RHO_SPATION = 5.2e96     # kg/m^3

def calculate_sound_parameters():
    print("--- Sound Wave Parameters (Air, STP) ---")
    
    # 1. Sound Speed
    # Standard: c = sqrt(gamma * P / rho)
    c_standard = math.sqrt(GAMMA_AIR * P_ATM / RHO_AIR)
    print(f"Sound Speed (c): {c_standard:.2f} m/s")
    
    # 2. Wavelength
    wavelength = c_standard / FREQ
    print(f"Frequency (f): {FREQ:.1f} Hz")
    print(f"Wavelength (lambda): {wavelength:.4f} m")
    
    # 3. Wave Number
    k = 2 * math.pi / wavelength
    omega = 2 * math.pi * FREQ
    print(f"Wave Number (k): {k:.4f} rad/m")
    print(f"Angular Frequency (omega): {omega:.2f} rad/s")
    
    print("\n--- Suppression Zone Characteristics ---")
    # Suppression Zone Width (lambda/2)
    suppression_width = wavelength / 2
    print(f"Suppression Zone Width (lambda/2): {suppression_width:.4f} m")
    
    print("\n--- Atomic Level Dynamics ---")
    # Atomic Displacement Amplitude
    # delta_r = A_P / (rho * c * omega)  (derived from impedance Z = rho*c = P/v, v = omega*disp)
    # v = P / (rho * c)
    # disp = v / omega = P / (rho * c * omega)
    disp_amplitude = PRESSURE_AMPLITUDE / (RHO_AIR * c_standard * omega)
    velocity_amplitude = PRESSURE_AMPLITUDE / (RHO_AIR * c_standard)
    
    print(f"Pressure Amplitude (A_P): {PRESSURE_AMPLITUDE:.2f} Pa")
    print(f"Atomic Displacement Amp (delta_r): {disp_amplitude:.2e} m")
    print(f"Atomic Velocity Amp (v_atom): {velocity_amplitude:.2e} m/s")
    
    # Kinetic Energy per unit volume
    # E_k = 0.5 * rho * v^2
    energy_density = 0.5 * RHO_AIR * velocity_amplitude**2
    print(f"Peak Kinetic Energy Density: {energy_density:.2e} J/m^3")
    
    print("\n--- SDT Specific Calculations ---")
    # Occlusion Energy Storage
    # Formula from prompt: E_stored = P_CMB * A_eff * delta_eta
    # delta_eta = delta_P / P_CMB
    # A_eff = lambda^2 (Effective cross-section of the wave packet?)
    
    # Let's verify the prompt's derivation:
    # E_stored_total = P_CMB * A_eff * (delta_P / P_CMB) = A_eff * delta_P (Units: m^2 * Pa = N) -> This is Force, not Energy.
    # The prompt says E_stored = P_CMB * A_eff * delta_eta. 
    # Usually Energy = Force * Distance.
    # If A_eff is area, P is Force/Area. P*A = Force.
    # Maybe Energy Density?
    
    # Let's look at "Occlusion-Based Energy Storage" in prompt:
    # "Predict that energy is stored in occlusion reduction: E = P_CMB A_eff δη"
    # "Calculate energy storage: E_stored = P_CMB λ² (δη)"
    # If delta_eta is dimensionless, P * A is Force. This dimensionally doesn't match Energy (Joules).
    # Unless A_eff is Volume? Or there is a length scale missing?
    # Or maybe it's Energy Flux (Power)? The Master Equation is Power (E_dot).
    # "E_dot = P_CMB A_eff ..."
    # So E_stored might be Power Stored? No, "Energy is stored".
    
    # Let's assume the prompt meant Energy Density u ~ P * delta_eta?
    # Or maybe the formula is E = P * V * delta_eta.
    # Let's calculate the "Occlusion Factor Change":
    
    delta_eta = PRESSURE_AMPLITUDE / P_CMB
    print(f"Occlusion Change (delta_eta = dP/P_CMB): {delta_eta:.2f}")
    
    # This is huge! 1 Pa / 0.02 Pa = 50.
    # This implies sound waves modulate occlusion significantly relative to CMB background.
    # But wait, P_CMB is the background. If P_wave > P_CMB, does eta go negative?
    # eta = 1 - (P_wave/P_CMB). If P_wave = P_atm ~ 100kPa, eta is huge negative.
    # This suggests P_CMB in the master equation refers to the LOCAL ambient pressure for this context, 
    # OR the prompt implies something else about "P_wave" being the perturbation on top of P_CMB.
    
    # Re-reading prompt: "P_total = P_CMB + delta_P".
    # "Derive coupling strength: kappa_coupling = delta_P / P_CMB".
    # "Calculate coupling for typical sound: kappa ~ 10^-5".
    # If kappa ~ 10^-5, then delta_P must be small compared to P_CMB.
    # But P_CMB = 0.02 Pa. 
    # 1 Pa sound wave >> 0.02 Pa.
    # So kappa would be 50, not 10^-5.
    
    # CONTRADICTION CHECK:
    # Standard P_atm = 10^5 Pa.
    # P_CMB = 2e-2 Pa.
    # The prompt says "P_total = P_CMB + delta_P" and "kappa ~ 10^-5".
    # This implies P_CMB is the LARGE value (10^5) or delta_P is TINY (10^-7).
    # BUT the prompt explicitly defines P_CMB = 2.036e-2 Pa in other files.
    # AND typical sound is ~1 Pa.
    
    # HYPOTHESIS: The prompt might be assuming the sound wave is propagating in the "Spation" vacuum 
    # or the coupling is different.
    # OR, P_CMB in the context of gas sound waves acts differently.
    # Actually, in a GAS, the background pressure is P_ATM.
    # Maybe the "Coupling" is delta_P / P_ATM?
    # 1 Pa / 10^5 Pa = 10^-5. This matches the "10^-5" estimate.
    # So "P_CMB" in the prompt questions 305-308 likely refers to the AMBIENT pressure P_0 (P_ATM),
    # possibly mislabeled or implying P_ATM is the effective "CMB" for the gas environment.
    # Let's calculate with P_ATM as the baseline pressure for coupling.
    
    coupling_strength = PRESSURE_AMPLITUDE / P_ATM
    print(f"Coupling Strength (dP / P_ATM): {coupling_strength:.2e} (Matches ~10^-5 prediction)")

    # Energy in Occlusion (using P_ATM as baseline)
    # E_stored_occlusion = P_ATM * Volume * Coupling?
    # Classical Potential Energy Density = (dP)^2 / (2 * rho * c^2) = (dP)^2 / (2 * gamma * P_ATM)
    # = (dP/P_ATM)^2 * P_ATM / (2*gamma)
    # = Coupling^2 * P_ATM ...
    
    classical_PE_density = PRESSURE_AMPLITUDE**2 / (2 * RHO_AIR * c_standard**2)
    print(f"Classical Potential Energy Density: {classical_PE_density:.2e} J/m^3")
    
if __name__ == "__main__":
    calculate_sound_parameters()

