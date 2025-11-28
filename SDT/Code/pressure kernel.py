import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sdt_core.constants import CELESTIAL_BODIES, C_LATTICE
from sdt_core.physics import compute_acceleration_particle

# Approximate Starting State (Mean Distance & Mean Velocity)
INITIAL_STATE = {
    'Sun':     {'r': [0, 0, 0], 'v': [0, 0, 0]},
    'Mercury': {'r': [5.79e10, 0, 0], 'v': [0, 47400, 0]},
    'Venus':   {'r': [1.082e11, 0, 0], 'v': [0, 35020, 0]},
    'Earth':   {'r': [1.496e11, 0, 0], 'v': [0, 29780, 0]},
    'Mars':    {'r': [2.279e11, 0, 0], 'v': [0, 24070, 0]},
    'Jupiter': {'r': [7.786e11, 0, 0], 'v': [0, 13070, 0]},
    'Saturn':  {'r': [1.433e12, 0, 0], 'v': [0, 9680, 0]},
    'Uranus':  {'r': [2.872e12, 0, 0], 'v': [0, 6800, 0]},
    'Neptune': {'r': [4.495e12, 0, 0], 'v': [0, 5430, 0]},
}

class DisplacementVortex:
    def __init__(self, name, r_eff, kappa, r_init, v_init, color):
        self.name = name
        self.r_eff = r_eff
        self.kappa = kappa
        self.r = np.array(r_init, dtype=float)
        self.v = np.array(v_init, dtype=float)
        self.a = np.zeros(3, dtype=float)
        self.color = color
        self.trajectory = [[], []]

    def update_trajectory(self):
        self.trajectory[0].append(self.r[0])
        self.trajectory[1].append(self.r[1])
        if len(self.trajectory[0]) > 200:
            self.trajectory[0].pop(0)
            self.trajectory[1].pop(0)

class SpationLattice:
    def __init__(self):
        self.bodies = []

    def add_vortex(self, body):
        self.bodies.append(body)

    def compute_pressure_gradients(self):
        # Reset accelerations
        for body in self.bodies:
            body.a = np.zeros(3)

        # N-Body Interaction Loop
        for i, body_i in enumerate(self.bodies):
            for j, body_j in enumerate(self.bodies):
                if i == j: continue

                r_vec = body_j.r - body_i.r
                distance = np.linalg.norm(r_vec)
                
                # Use Unified Physics Core (Phase 15 Gravity)
                acceleration = compute_acceleration_particle(
                    body_j.r_eff, body_j.kappa, r_vec, distance
                )
                
                body_i.a += acceleration

    def step_symplectic(self, dt):
        # 1. First Half-Kick
        for body in self.bodies:
            body.v += body.a * 0.5 * dt

        # 2. Drift
        for body in self.bodies:
            body.r += body.v * dt
            body.update_trajectory()

        # 3. Recalculate
        self.compute_pressure_gradients()

        # 4. Second Half-Kick
        for body in self.bodies:
            body.v += body.a * 0.5 * dt

def run_simulation():
    sim = SpationLattice()
    colors = ['yellow', 'gray', 'orange', 'blue', 'red', 'brown', 'gold', 'cyan', 'blue']
    names = list(CELESTIAL_BODIES.keys())

    for i, name in enumerate(names):
        if name in INITIAL_STATE:
            data = INITIAL_STATE[name]
            params = CELESTIAL_BODIES[name]
            vortex = DisplacementVortex(
                name, 
                params['R_eff'], 
                params['Kappa'], 
                data['r'], 
                data['v'], 
                colors[i] if i < len(colors) else 'white'
            )
            sim.add_vortex(vortex)

    # Time settings
    years_to_sim = 2.0
    dt = 86400 / 2  # 12 hour steps
    steps = int((years_to_sim * 365 * 86400) / dt)

    # Setup Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('black')
    ax.set_aspect('equal')
    limit = 3e11 
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    points = [ax.plot([], [], 'o', color=b.color, markersize=5 if b.name != 'Sun' else 10)[0] for b in sim.bodies]
    trails = [ax.plot([], [], '-', color=b.color, lw=0.5, alpha=0.7)[0] for b in sim.bodies]
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')

    def init():
        for p, t in zip(points, trails):
            p.set_data([], [])
            t.set_data([], [])
        return points + trails

    def animate(frame):
        speed_factor = 10 
        for _ in range(speed_factor):
            sim.step_symplectic(dt)

        for i, body in enumerate(sim.bodies):
            points[i].set_data([body.r[0]], [body.r[1]])
            trails[i].set_data(body.trajectory[0], body.trajectory[1])
        
        total_days = (frame * speed_factor * dt) / 86400
        time_text.set_text(f'SDT Void Engine: Day {int(total_days)}')
        
        return points + trails + [time_text]

    anim = FuncAnimation(fig, animate, init_func=init, frames=steps//10, interval=20, blit=True)

    print("Initializing Void Engine...")
    print("Spation Lattice Geometry Loaded.")
    print("Calculating Pressure Gradients (No G, No M, No Beta)...")
    plt.show()

if __name__ == "__main__":
    run_simulation()