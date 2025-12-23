import numpy as np
import matplotlib.pyplot as plt
from sound_wave_simulation import SDTWaveSimulation

def generate_snapshot():
    print("Initializing Simulation for Snapshot...")
    sim = SDTWaveSimulation(length=2.0, points=200, freq=340.0)
    sim.initialize_standing_wave(amplitude=1.0)
    
    # Target time: T/4 (90 degrees phase)
    # At t=0, P is max (cos(0)=1).
    # At t=T/4, P should be 0 (cos(pi/2)=0).
    # Velocity should be max.
    
    period = 1.0 / sim.f
    target_time = period * 0.25
    
    print(f"Running to t = {target_time*1000:.2f} ms")
    
    while sim.t < target_time:
        sim.step()
        
    print(f"Time reached: {sim.t*1000:.2f} ms")
    print(f"Max Pressure: {np.max(np.abs(sim.P)):.4f} Pa")
    print(f"Max Velocity * Z: {np.max(np.abs(sim.v * sim.rho * sim.c)):.4f} Pa")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(sim.x, sim.P, 'b-', label='Pressure (P)', linewidth=2)
    Z = sim.rho * sim.c
    plt.plot(sim.x, sim.v * Z, 'r--', label='Velocity (v * Z)', linewidth=2)
    
    plt.title(f'SDT Sound Wave Snapshot at t=T/4\nGlobal Pressure Null (Cancellation) -> Velocity Max')
    plt.xlabel('Position (m)')
    plt.ylabel('Amplitude (Scaled)')
    plt.legend()
    plt.grid(True)
    
    output_path = 'SDT/investigations/sound_wave_snapshot_null.png'
    plt.savefig(output_path)
    print(f"Snapshot saved to {output_path}")

if __name__ == "__main__":
    generate_snapshot()

