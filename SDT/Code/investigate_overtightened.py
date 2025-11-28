import math

# Constants
c = 299792458.0
m_e = 9.10938356e-31
m_p = 1.6726219e-27
e_charge = 1.60217663e-19

# User Values
v_tight = 1.8412 * c
v_stable = 1.81 * c

print(f"Overtightened Velocity: {v_tight:.4e} m/s")
print(f"Stabilized Velocity: {v_stable:.4e} m/s")

# Energy Difference Model
# Hypothesis: Energy is proportional to v^2 (Kinetic/Rotational Energy)
# Delta E = k * (v_tight^2 - v_stable^2)
# What is k? Maybe related to Electron Mass?
# Let's assume the "Rod" has mass m_e.
E_tight = 0.5 * m_e * v_tight**2
E_stable = 0.5 * m_e * v_stable**2
Delta_E = E_tight - E_stable

print(f"Energy Tight (eV): {E_tight / e_charge:.4e}")
print(f"Energy Stable (eV): {E_stable / e_charge:.4e}")
print(f"Delta E (eV): {Delta_E / e_charge:.4e}")

# Check if Delta E matches Neutron-Proton difference (1.29 MeV)
# or Antineutrino energy?
diff_MeV = (Delta_E / e_charge) / 1e6
print(f"Delta E (MeV): {diff_MeV:.4f} MeV")

# Check Ratio
ratio = v_tight / v_stable
print(f"Winding Ratio: {ratio:.4f}") # ~1.017

# Check if Delta E matches Neutrino Mass? (Unlikely, too huge)
# Check if Delta E matches Binding Energy?
