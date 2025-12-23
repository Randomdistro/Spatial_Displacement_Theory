import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec

# SDT Investigation: Sound Wave Cancellation and Recovery Simulation
# Phase 3: Computational Simulation

class SDTWaveSimulation:
    def __init__(self, length=2.0, points=200, c=340.0, freq=340.0):
        """
        Initialize 1D SDT Wave Simulation
        length: Domain length (m)
        points: Number of spatial points
        c: Sound speed (m/s)
        freq: Frequency (Hz)
        """
        self.L = length
        self.N = points
        self.dx = self.L / (self.N - 1)
        self.x = np.linspace(0, self.L, self.N)
        self.c = c
        self.f = freq
        self.omega = 2 * np.pi * self.f
        self.k = self.omega / self.c
        self.wavelength = self.c / self.f
        
        # Time step (CFL condition)
        self.dt = 0.5 * self.dx / self.c
        self.t = 0.0
        
        # Fields
        self.P = np.zeros(self.N)      # Pressure Field (Spation Tension)
        self.P_old = np.zeros(self.N)  # Previous P
        self.P_new = np.zeros(self.N)  # Next P
        
        self.v = np.zeros(self.N)      # Velocity Field (Matter Flux)
        
        # Material Properties (Air approx)
        self.rho = 1.225 # kg/m^3
        self.K_bulk = self.rho * self.c**2
        
        # Simulation State
        self.running = True
        
    def initialize_standing_wave(self, amplitude=1.0):
        """Initialize with analytic standing wave solution to verify stability"""
        # P(x,0) = 2A sin(kx)
        # P_old(x) needs to be back-propagated
        self.P = 2 * amplitude * np.sin(self.k * self.x)
        
        # Backward time step for Verlet integration
        # P(x, -dt) = 2A sin(kx) cos(-omega*dt)
        self.P_old = 2 * amplitude * np.sin(self.k * self.x) * np.cos(-self.omega * self.dt)
        
    def initialize_counter_propagating_pulse(self):
        """Initialize two Gaussian pulses moving towards each other"""
        sigma = 0.1
        x0_left = self.L * 0.25
        x0_right = self.L * 0.75
        
        # Pulse 1 (Moving Right)
        # P = exp(-(x-x0-ct)^2 / 2sigma^2)
        
        def pulse_right(x, t):
            return np.exp(-(x - x0_left - self.c*t)**2 / (2*sigma**2))
            
        def pulse_left(x, t):
            return np.exp(-(x - x0_right + self.c*t)**2 / (2*sigma**2)) # Phase flipped for cancellation? 
            # If we want cancellation, they should be opposite sign? Or same sign?
            # Destructive interference of P requires opposite signs if they overlap.
            # Let's try same sign first, they add up. Opposite sign cancels P.
            # Prompt: "Two sound waves of equal amplitude but opposite phase"
            # So one positive, one negative.
            
        # P_total = Pulse_Right - Pulse_Left
        self.P = pulse_right(self.x, 0) - pulse_left(self.x, 0)
        self.P_old = pulse_right(self.x, -self.dt) - pulse_left(self.x, -self.dt)

    def step(self):
        """Execute one time step of FDTD"""
        # Wave Equation: d2P/dt2 = c^2 d2P/dx2
        # Finite Difference:
        # P_new = 2*P - P_old + (c*dt/dx)^2 * (P[i+1] - 2*P[i] + P[i-1])
        
        C2 = (self.c * self.dt / self.dx)**2
        
        # Vectorized update (interior points)
        self.P_new[1:-1] = 2*self.P[1:-1] - self.P_old[1:-1] + \
                           C2 * (self.P[2:] - 2*self.P[1:-1] + self.P[:-2])
                           
        # Boundary Conditions (Absorbing/Open or Reflective?)
        # Let's use reflective (Hard Wall) for standing wave: dP/dx = 0 -> P[0]=P[1]
        # Or Dirichlet P=0 (Open Pipe).
        # For Standing Wave sin(kx), P=0 at x=0 is good.
        self.P_new[0] = 0
        self.P_new[-1] = 0
        
        # Update Velocity Field (Derived from Pressure Gradient)
        # rho * dv/dt = -dP/dx
        # v_new = v_old - (dt/rho) * dP/dx
        # We calculate v at half-steps or centered?
        # Let's just approximate v from accumulated impulse
        # v[i] += - (dt/rho) * (P[i+1] - P[i-1]) / (2dx)
        
        grad_P = np.zeros_like(self.P)
        grad_P[1:-1] = (self.P[2:] - self.P[:-2]) / (2*self.dx)
        self.v[1:-1] += - (self.dt / self.rho) * grad_P[1:-1]
        
        # Shift buffers
        self.P_old[:] = self.P[:]
        self.P[:] = self.P_new[:]
        self.t += self.dt

    def get_energy_density(self):
        """Calculate Potential and Kinetic Energy Density"""
        # u_pot = P^2 / (2 * K_bulk)
        # u_kin = 0.5 * rho * v^2
        
        u_pot = self.P**2 / (2 * self.K_bulk)
        u_kin = 0.5 * self.rho * self.v**2
        return u_pot, u_kin

def run_simulation_and_plot():
    sim = SDTWaveSimulation(length=2.0, points=200, freq=340.0) # lambda = 1.0 m
    
    # Setup Standing Wave (Suppression Zones at nodes)
    sim.initialize_standing_wave(amplitude=1.0)
    
    # Run for a few cycles to stabilize velocity
    # (Velocity starts at 0 in init, needs to catch up to P)
    # Actually, analytic initialization of v would be better.
    # P = 2A sin(kx) cos(wt)
    # v = (2A/Z) cos(kx) sin(wt) -> At t=0, v=0. Correct.
    # So v starts at 0 is correct for Standing Wave starting at max P amplitude.
    
    # Setup Plot
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(3, 1, height_ratios=[2, 1, 1])
    
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])
    
    line_p, = ax1.plot([], [], 'b-', label='Pressure (P)', linewidth=2)
    line_v, = ax1.plot([], [], 'r--', label='Velocity (v)', linewidth=2, alpha=0.7)
    
    # Mark Nodes
    nodes = [0.0, 0.5, 1.0, 1.5, 2.0] # Lambda = 1m. Nodes at n*lambda/2?
    # sin(kx) = 0 -> kx = n*pi -> (2pi/L)*x = n*pi -> x = n*L/2 = n*0.5
    for node in nodes:
        ax1.axvline(x=node, color='k', linestyle=':', alpha=0.3)
        ax2.axvline(x=node, color='k', linestyle=':', alpha=0.3)
        ax3.axvline(x=node, color='k', linestyle=':', alpha=0.3)
        
    ax1.set_xlim(0, 2.0)
    ax1.set_ylim(-2.5, 2.5) # Amplitude 2.0
    ax1.set_ylabel('Amplitude')
    ax1.set_title('SDT Wave Mechanics: Pressure vs Velocity Exchange')
    ax1.legend(loc='upper right')
    
    line_ep, = ax2.plot([], [], 'b-', label='Potential Energy (Pressure)', alpha=0.6)
    line_ek, = ax2.plot([], [], 'r-', label='Kinetic Energy (Velocity)', alpha=0.6)
    line_et, = ax2.plot([], [], 'k-', label='Total Energy', linewidth=2)
    
    ax2.set_xlim(0, 2.0)
    ax2.set_ylim(0, 1e-5) # Adjust based on values
    ax2.set_ylabel('Energy Density (J/m³)')
    ax2.legend(loc='upper right')
    
    # Phase / SDT Metric
    # Plot "Occlusion" or "Information"
    # Information ~ P^2 + (Z*v)^2 (Envelope)
    line_info, = ax3.plot([], [], 'g-', label='Wave Information (Envelope)', linewidth=2)
    
    ax3.set_xlim(0, 2.0)
    ax3.set_ylim(0, 5.0)
    ax3.set_ylabel('Wave Envelope')
    ax3.set_xlabel('Position (m)')
    
    def init():
        return line_p, line_v, line_ep, line_ek, line_et, line_info
        
    def update(frame):
        for _ in range(5): # Speed up animation
            sim.step()
            
        u_pot, u_kin = sim.get_energy_density()
        u_total = u_pot + u_kin
        
        # Scale v for plotting alongside P
        # Z = rho*c approx 416. 
        # v ~ P/Z ~ 1/400. 
        # So plot v * Z to compare with P.
        Z = sim.rho * sim.c
        
        line_p.set_data(sim.x, sim.P)
        line_v.set_data(sim.x, sim.v * Z) # Scaled velocity (Impedance adjusted)
        
        line_ep.set_data(sim.x, u_pot)
        line_ek.set_data(sim.x, u_kin)
        line_et.set_data(sim.x, u_total)
        
        # Envelope recovery
        envelope = np.sqrt(sim.P**2 + (sim.v * Z)**2)
        line_info.set_data(sim.x, envelope)
        
        ax1.set_title(f'Time: {sim.t*1000:.1f} ms | Suppression Check: P(node)={sim.P[100]:.2f}, v(node)={sim.v[100]*Z:.2f}')
        
        return line_p, line_v, line_ep, line_ek, line_et, line_info

    ani = animation.FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=20)
    
    # Save animation
    try:
        ani.save('SDT/investigations/sound_wave_simulation.gif', writer='pillow', fps=30)
        print("Simulation saved to SDT/investigations/sound_wave_simulation.gif")
    except Exception as e:
        print(f"Could not save animation: {e}")
        
    # Also save a static snapshot at t ~ 1/4 cycle (max kinetic energy at some points)
    # Actually, we want a snapshot where P is minimal (zero crossing of standing wave in time)
    # Standing wave: P ~ cos(wt). Zero at t = T/4, 3T/4.
    # At these times, P is flat (zero everywhere), but v is MAX everywhere (in standing wave pattern).
    
    # Let's run until we hit a "Null Pressure" moment
    # Reset sim
    sim = SDTWaveSimulation(length=2.0, points=200, freq=340.0)
    sim.initialize_standing_wave(amplitude=1.0)
    
    target_time = sim.wavelength / sim.c * 0.25 # T/4
    while sim.t < target_time:
        sim.step()
        
    # Plot Snapshot
    plt.figure(figsize=(10, 6))
    plt.plot(sim.x, sim.P, 'b-', label='Pressure (P)')
    plt.plot(sim.x, sim.v * sim.rho * sim.c, 'r--', label='Velocity (v * Z)')
    plt.title(f'Snapshot at t=T/4 (Global Pressure Null)\nMax Velocity Field carries the Wave')
    plt.legend()
    plt.grid(True)
    plt.savefig('SDT/investigations/sound_wave_snapshot_null.png')
    print("Snapshot saved to SDT/investigations/sound_wave_snapshot_null.png")

if __name__ == "__main__":
    run_simulation_and_plot()

