"""
Electricity / Ambient Energy Circuits (SDT) - Circuit Simulation
-----------------------------------------------------------------

This script simulates ambient energy harvesting circuits including:
- Simple rectifier circuits
- Charge pump voltage multipliers
- Multi-source combining circuits
- Power management (DC-DC converters)
- Efficiency vs load resistance analysis

Uses simplified circuit models for educational purposes.
"""

from __future__ import annotations

import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class CircuitComponent:
    """Base class for circuit components."""
    name: str
    value: float
    unit: str = ""


@dataclass
class VoltageSource:
    """Voltage source (ambient gradient)."""
    name: str
    internal_resistance: float  # Ω
    voltage: float  # V
    unit: str = ""


@dataclass
class Resistor:
    """Resistor."""
    name: str
    resistance: float  # Ω
    unit: str = ""


@dataclass
class Capacitor:
    """Capacitor."""
    name: str
    capacitance: float  # F
    unit: str = ""


@dataclass
class Diode:
    """Ideal diode with forward voltage drop."""
    name: str
    forward_voltage: float = 0.7  # V (silicon) or 0.3 V (Schottky)
    unit: str = ""


class SimpleRectifier:
    """Half-wave rectifier circuit simulation."""
    
    def __init__(
        self,
        source: VoltageSource,
        load_resistance: float,
        capacitor: Optional[Capacitor] = None
    ):
        self.source = source
        self.load_resistance = load_resistance
        self.capacitor = capacitor
        
    def calculate_output_voltage(self) -> float:
        """Calculate DC output voltage."""
        # For AC source, peak voltage
        V_peak = self.source.voltage
        
        # Diode forward voltage drop
        V_diode = 0.7  # Silicon diode
        
        # Output voltage (simplified - assumes large capacitor)
        if V_peak > V_diode:
            V_out = V_peak - V_diode
        else:
            V_out = 0.0  # Diode doesn't conduct
        
        return V_out
    
    def calculate_output_current(self) -> float:
        """Calculate DC output current."""
        V_out = self.calculate_output_voltage()
        I_out = V_out / self.load_resistance if self.load_resistance > 0 else 0.0
        return I_out
    
    def calculate_power(self) -> float:
        """Calculate output power."""
        V_out = self.calculate_output_voltage()
        I_out = self.calculate_output_current()
        return V_out * I_out
    
    def calculate_efficiency(self) -> float:
        """Calculate efficiency (output power / available power)."""
        # Available power (maximum power transfer)
        P_available = (self.source.voltage ** 2) / (4 * self.source.internal_resistance)
        P_out = self.calculate_power()
        
        if P_available > 0:
            return P_out / P_available
        return 0.0


class ChargePump:
    """Dickson charge pump (voltage multiplier)."""
    
    def __init__(
        self,
        source: VoltageSource,
        num_stages: int,
        capacitor_value: float = 1e-6,  # F
        load_resistance: float = 1e6  # Ω
    ):
        self.source = source
        self.num_stages = num_stages
        self.capacitor_value = capacitor_value
        self.load_resistance = load_resistance
        
    def calculate_output_voltage(self) -> float:
        """Calculate output voltage (ideal, no losses)."""
        V_diode = 0.3  # Schottky diode
        V_in = self.source.voltage
        
        # Ideal charge pump: V_out = N * V_in - N * V_diode
        V_out = self.num_stages * (V_in - V_diode)
        
        # Cannot exceed source voltage if V_in < V_diode
        if V_in < V_diode:
            V_out = 0.0
        
        return max(0.0, V_out)
    
    def calculate_output_current(self) -> float:
        """Calculate output current."""
        V_out = self.calculate_output_voltage()
        I_out = V_out / self.load_resistance if self.load_resistance > 0 else 0.0
        return I_out
    
    def calculate_power(self) -> float:
        """Calculate output power."""
        V_out = self.calculate_output_voltage()
        I_out = self.calculate_output_current()
        return V_out * I_out
    
    def calculate_efficiency(self) -> float:
        """Calculate efficiency."""
        P_available = (self.source.voltage ** 2) / (4 * self.source.internal_resistance)
        P_out = self.calculate_power()
        
        if P_available > 0:
            return P_out / P_available
        return 0.0


class MultiSourceCombiner:
    """Combines multiple ambient sources."""
    
    def __init__(self, sources: List[VoltageSource], load_resistance: float):
        self.sources = sources
        self.load_resistance = load_resistance
        
    def calculate_combined_voltage(self) -> float:
        """Calculate combined voltage (parallel connection)."""
        # For parallel connection, voltage is weighted average
        total_conductance = sum(1.0 / s.internal_resistance for s in self.sources)
        weighted_voltage = sum(
            s.voltage / s.internal_resistance for s in self.sources
        )
        
        if total_conductance > 0:
            V_combined = weighted_voltage / total_conductance
        else:
            V_combined = 0.0
        
        return V_combined
    
    def calculate_combined_resistance(self) -> float:
        """Calculate combined source resistance (parallel)."""
        total_conductance = sum(1.0 / s.internal_resistance for s in self.sources)
        
        if total_conductance > 0:
            R_combined = 1.0 / total_conductance
        else:
            R_combined = float('inf')
        
        return R_combined
    
    def calculate_output_power(self) -> float:
        """Calculate output power."""
        V_out = self.calculate_combined_voltage()
        R_source = self.calculate_combined_resistance()
        
        # Maximum power transfer
        if R_source < float('inf'):
            P_max = (V_out ** 2) / (4 * R_source)
        else:
            P_max = 0.0
        
        return P_max


def simulate_power_vs_load(
    source: VoltageSource,
    load_resistances: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Simulate power vs load resistance."""
    powers = []
    
    for R_load in load_resistances:
        # Current divider
        I_total = source.voltage / (source.internal_resistance + R_load)
        V_load = I_total * R_load
        P_load = V_load * I_total
        powers.append(P_load)
    
    return np.array(powers)


def plot_efficiency_analysis():
    """Plot efficiency vs load resistance for different sources."""
    # Create sources
    sources = [
        VoltageSource("Atmospheric", 4.33e14, 1300.0, 4.33e14),
        VoltageSource("Telluric", 159.0, 0.0001, 159.0),
        VoltageSource("Geomagnetic", 100.0, 1e-6, 100.0),
    ]
    
    # Load resistance range (log scale)
    R_loads = np.logspace(0, 18, 100)  # 1 Ω to 1e18 Ω
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot 1: Power vs Load Resistance
    ax1 = axes[0]
    for source in sources:
        powers = simulate_power_vs_load(source, R_loads)
        ax1.loglog(R_loads, powers, label=source.name, linewidth=2)
    
    ax1.set_xlabel('Load Resistance (Ω)', fontsize=12)
    ax1.set_ylabel('Output Power (W)', fontsize=12)
    ax1.set_title('Power vs Load Resistance (Maximum Power Transfer)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Mark maximum power points
    for source in sources:
        R_opt = source.internal_resistance
        P_max = (source.voltage ** 2) / (4 * R_opt)
        ax1.plot(R_opt, P_max, 'ro', markersize=8)
        ax1.annotate(
            f'Max: {P_max:.2e} W',
            xy=(R_opt, P_max),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=9
        )
    
    # Plot 2: Efficiency vs Load Resistance
    ax2 = axes[1]
    for source in sources:
        efficiencies = []
        P_max = (source.voltage ** 2) / (4 * source.internal_resistance)
        
        for R_load in R_loads:
            I_total = source.voltage / (source.internal_resistance + R_load)
            V_load = I_total * R_load
            P_load = V_load * I_total
            eff = P_load / P_max if P_max > 0 else 0.0
            efficiencies.append(eff)
        
        ax2.semilogx(R_loads, efficiencies, label=source.name, linewidth=2)
    
    ax2.set_xlabel('Load Resistance (Ω)', fontsize=12)
    ax2.set_ylabel('Efficiency (P_out / P_max)', fontsize=12)
    ax2.set_title('Efficiency vs Load Resistance', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig('SDT/investigations/ambient_circuit_efficiency.png', dpi=150)
    print("Efficiency plot saved to SDT/investigations/ambient_circuit_efficiency.png")


def simulate_rectifier_circuits():
    """Simulate rectifier circuits for different sources."""
    print("\n" + "=" * 80)
    print("RECTIFIER CIRCUIT SIMULATION")
    print("=" * 80)
    
    # Create sources
    sources = [
        VoltageSource("Atmospheric", 4.33e14, 1300.0, 4.33e14),
        VoltageSource("Telluric", 159.0, 0.0001, 159.0),
        VoltageSource("Geomagnetic", 100.0, 1e-6, 100.0),
    ]
    
    # Load resistance (matched for maximum power)
    for source in sources:
        R_load = source.internal_resistance
        
        rectifier = SimpleRectifier(source, R_load)
        
        print(f"\n[{source.name}]")
        print(f"  Source voltage: {source.voltage:.3e} V")
        print(f"  Source resistance: {source.internal_resistance:.3e} Ω")
        print(f"  Load resistance: {R_load:.3e} Ω")
        print(f"  Output voltage: {rectifier.calculate_output_voltage():.3e} V")
        print(f"  Output current: {rectifier.calculate_output_current():.3e} A")
        print(f"  Output power: {rectifier.calculate_power():.3e} W")
        print(f"  Efficiency: {rectifier.calculate_efficiency()*100:.2f}%")
        
        # Check if diode drop is significant
        if source.voltage < 0.7:
            print(f"  WARNING: Diode forward voltage (0.7 V) exceeds source voltage!")
            print(f"  Rectifier will not work - need zero-threshold device")


def simulate_charge_pump():
    """Simulate charge pump for low-voltage sources."""
    print("\n" + "=" * 80)
    print("CHARGE PUMP SIMULATION")
    print("=" * 80)
    
    # Low-voltage source (telluric)
    source = VoltageSource("Telluric", 159.0, 0.0001, 159.0)
    
    print(f"\nSource: {source.name}")
    print(f"  Voltage: {source.voltage:.3e} V = {source.voltage*1e6:.2f} µV")
    print(f"  Resistance: {source.internal_resistance:.2f} Ω")
    
    # Try different numbers of stages
    for N in [1, 10, 100, 1000]:
        pump = ChargePump(source, N, capacitor_value=1e-6, load_resistance=1e6)
        
        V_out = pump.calculate_output_voltage()
        I_out = pump.calculate_output_current()
        P_out = pump.calculate_power()
        
        print(f"\n  Stages: {N}")
        print(f"    Output voltage: {V_out:.3e} V")
        print(f"    Output current: {I_out:.3e} A")
        print(f"    Output power: {P_out:.3e} W")
        
        if V_out == 0.0:
            print(f"    VERDICT: Charge pump cannot boost - input too small")


def simulate_multi_source():
    """Simulate multi-source combining."""
    print("\n" + "=" * 80)
    print("MULTI-SOURCE COMBINING SIMULATION")
    print("=" * 80)
    
    # Create multiple sources
    sources = [
        VoltageSource("Atmospheric", 4.33e14, 1300.0, 4.33e14),
        VoltageSource("Telluric", 159.0, 0.0001, 159.0),
        VoltageSource("Geomagnetic", 100.0, 1e-6, 100.0),
    ]
    
    # Combined circuit
    combiner = MultiSourceCombiner(sources, load_resistance=1e6)
    
    V_combined = combiner.calculate_combined_voltage()
    R_combined = combiner.calculate_combined_resistance()
    P_combined = combiner.calculate_output_power()
    
    print(f"\nCombined Circuit:")
    print(f"  Combined voltage: {V_combined:.3e} V")
    print(f"  Combined resistance: {R_combined:.3e} Ω")
    print(f"  Maximum power: {P_combined:.3e} W")
    
    # Individual powers
    print(f"\nIndividual Sources:")
    total_individual = 0.0
    for source in sources:
        P_ind = (source.voltage ** 2) / (4 * source.internal_resistance)
        total_individual += P_ind
        print(f"  {source.name}: {P_ind:.3e} W")
    
    print(f"\n  Total (sum): {total_individual:.3e} W")
    print(f"  Combined (parallel): {P_combined:.3e} W")
    print(f"  Difference: {abs(total_individual - P_combined):.3e} W")
    print(f"  NOTE: Parallel connection gives lower total resistance,")
    print(f"        but voltage is weighted average (not sum)")


def main():
    """Main simulation function."""
    print("=" * 80)
    print("SDT AMBIENT ENERGY CIRCUIT SIMULATION")
    print("=" * 80)
    
    # Run simulations
    simulate_rectifier_circuits()
    simulate_charge_pump()
    simulate_multi_source()
    
    # Generate plots
    print("\n" + "=" * 80)
    print("GENERATING EFFICIENCY PLOTS...")
    print("=" * 80)
    plot_efficiency_analysis()
    
    print("\nDone.")


if __name__ == "__main__":
    main()

