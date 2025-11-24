# SDT-Navier C++ API Reference

## Core Classes

### FieldSystem

3D field storage container for SDT-Navier fields.

```cpp
FieldSystem fields(nx, ny, nz, dx, dy, dz, P_infinity);
```

**Methods:**
- `nx()`, `ny()`, `nz()`: Grid dimensions
- `size()`: Total number of grid points
- `dx()`, `dy()`, `dz()`: Grid spacing
- `t()`, `set_t(t)`: Current simulation time
- `dt()`, `set_dt(dt)`: Timestep
- `index(i, j, k)`: Convert 3D indices to linear index
- `coords(idx)`: Convert linear index to 3D coordinates
- `validate()`: Check field validity

**Field Access:**
- `P()`: Pressure field (Eigen::Map)
- `kappa()`: Curvature field
- `eta()`: Slip field
- `e()`: Energy density field
- `Gamma()`: Circulation factor field
- `v()`: Velocity field (vector of Vector3d)

### SDTNavierEquations

Field equations with configurable force functional parameters.

```cpp
SDTNavierEquations equations(
    rho_s, alpha_curv, beta_slip,
    gamma_create, delta_destroy,
    epsilon_strain, zeta_heal
);
```

**Force Functionals:**
- `compute_force_curvature()`: F_curv = -α ∇κ
- `compute_force_slip()`: F_slip = -β η v
- `compute_curvature_creation()`: C = γ κ |∇·v|
- `compute_curvature_destruction()`: D = δ κ η
- `compute_slip_strain()`: S_strain = ε κ |∇v|
- `compute_slip_healing()`: S_healing = ζ κ²

**RHS Computation:**
- `compute_flow_rhs()`: Right-hand side of flow equation
- `compute_curvature_rhs()`: Right-hand side of curvature equation
- `compute_slip_rhs()`: Right-hand side of slip equation
- `compute_energy_rhs()`: Right-hand side of energy equation

### SDTNavierSolver

Time-stepping solver for SDT-Navier equations.

```cpp
SDTNavierSolver solver(
    fields, equations, dt, cfl, method, enforce_incompressibility
);
```

**Methods:**
- `step()`: Perform one time step
- `run_until(t_end, callback)`: Run until specified time
- `get_divergence_error()`: Maximum divergence error
- `t()`, `dt()`: Current time and timestep

**Parameters:**
- `dt`: Fixed timestep (0 for adaptive)
- `cfl`: CFL number for adaptive timestep (default: 0.5)
- `method`: "euler" or "rk4" (default: "rk4")
- `enforce_incompressibility`: Whether to enforce ∇·v = 0 (default: true)

### Nuclear Systems

#### DeuteronSystem

```cpp
DeuteronSystem deuteron(fields, center, separation_cells);
```

**Methods:**
- `compute_binding_energy()`: Binding energy in J
- `compute_binding_energy_mev()`: Binding energy in MeV
- `proton()`, `neutron()`: Access turbine cells

#### TritonSystem, HelionSystem, AlphaSystem

Similar interface for other nuclear systems.

## Functions

### Field Initialization

```cpp
void initialize_fields(
    FieldSystem& fields,
    double P_infinity = sdt::P_INFINITY_NUCLEAR,
    double initial_kappa = 0.0,
    double initial_eta = 0.01,
    double initial_Gamma = sdt::GAMMA_P
);
```

### Turbine Sources

```cpp
void add_turbine_source(
    FieldSystem& fields,
    const std::array<std::size_t, 3>& position,
    double radius_cells,
    double kappa_value,
    double Gamma_value,
    double eta_value,
    const std::string& profile = "gaussian"
);
```

### Discrete Operators

```cpp
std::vector<std::array<double, 3>> compute_gradient(
    const std::vector<double>& field,
    const FieldSystem& fields,
    const std::string& boundary = "zero"
);

std::vector<double> compute_divergence(
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& boundary = "zero"
);

std::vector<double> compute_advection(
    const std::vector<double>& field,
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& method = "upwind"
);
```

### Analysis

```cpp
double compute_nuclear_magnetic_moment(
    const DeuteronSystem& system,
    const std::array<std::array<double, 3>, 2>& orientations = ...
);

ComparisonResult compare_magnetic_moment(
    double computed,
    double experimental,
    const std::string& name = "nucleus"
);
```

### I/O

```cpp
void save_fields_csv(const FieldSystem& fields, const std::string& filename);
void save_timeseries_csv(const std::vector<double>& times, ...);
void save_results_json(const std::string& filename, ...);
```

## Constants

All constants are in namespace `sdt_navier::sdt`:

- `P_INFINITY_NUCLEAR`: Nuclear scale pressure (1.65e31 Pa)
- `R_P`, `R_N`: Proton/neutron radii
- `KAPPA_P`, `KAPPA_N`: Curvature values
- `GAMMA_P`, `GAMMA_E_N`: Circulation factors
- `ETA_P_BOUND`, `ETA_N_BOUND`: Slip values
- `B_DEUTERON`, `B_TRITON`, etc.: Experimental binding energies
- `MU_P`, `MU_N`, `MU_D`, etc.: Experimental magnetic moments

## Python API

The Python bindings provide a similar interface:

```python
import sdt_navier_cpp

fields = sdt_navier_cpp.FieldSystem(50, 50, 50, 0.2e-15, 0.2e-15, 0.2e-15)
equations = sdt_navier_cpp.SDTNavierEquations()
solver = sdt_navier_cpp.SDTNavierSolver(fields, equations)
solver.run_until(1.0e-23)
```

