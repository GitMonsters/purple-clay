# 🏺 Purple Clay

**Unified Geometric Intelligence (UGI) Simulator**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/GitMonsters/purple-clay/pulls)

Purple Clay is a **computational research platform** that models symbolic information flow through
toroidal geometry, Bloch sphere state projection, and nonlinear reaction-diffusion dynamics.

> **Honest scope:** Purple Clay is a mathematical/computational simulator. It does not make claims
> about consciousness, artificial general intelligence, or sentience. It is a tool for exploring
> the rich behaviour of coupled nonlinear PDEs on geometrically non-trivial domains.

---

## Mathematical Foundations

| Component | Description |
|---|---|
| **Toroidal geometry** | Riemannian metric on a torus, Christoffel symbols, geodesic ODEs solved with `NDSolve` |
| **Golden spiral embedding** | Trajectory on the toroidal surface parameterised by the golden angle φ |
| **Bloch sphere projection** | Mapping from the field state ψ to SU(2) density matrices via the Bloch vector |
| **Reaction-diffusion PDEs** | Coupled nonlinear Turing-type system integrated with RK4 on a 2-D periodic grid |
| **Memory hysteresis** | Associative path strengths with exponential decay, conflict resolution, and pruning |
| **Lindblad decoherence** | Open-quantum-system evolution: unitary SU(2) rotation + dephasing / amplitude-decay |

---

## Repository Structure

```
purple-clay/
├── README.md
├── requirements.txt
├── .gitignore
├── mathematica/
│   └── toroidal_geodesics.nb      # Mathematica notebook: metric, Christoffel, geodesics
├── simulator/
│   ├── __init__.py                # Public API exports
│   ├── geometry_module.py         # Torus surface + golden spiral trajectory
│   ├── bloch_projection.py        # Torus field → Bloch vector mapping
│   ├── memory_module.py           # Memory hysteresis engine + Shannon entropy
│   ├── su2_lindblad.py            # SU(2) unitary evolution + Lindblad dissipator
│   ├── rk4_integrator.py          # RK4 step for dual-hemisphere reaction-diffusion
│   └── reaction_diffusion_gpu.py  # Full GPU-ready simulation harness (PyTorch)
├── app/
│   └── streamlit_main.py          # Interactive Streamlit UI
├── contracts/
│   └── SovereignNode.sol          # On-chain geometry hash registry (Solidity)
└── docs/
    └── manifesto.md               # Unified Geometric Intelligence manifesto
```

---

## Installation

```bash
# Clone
git clone https://github.com/GitMonsters/purple-clay.git
cd purple-clay

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### GPU support (optional)

If you have an NVIDIA GPU with CUDA, install the matching `torch` wheel from
[pytorch.org](https://pytorch.org/get-started/locally/). The simulator falls back to
CPU automatically when CUDA is unavailable.

---

## Running the Streamlit App

```bash
streamlit run app/streamlit_main.py
```

The app opens in your browser. Use the sidebar to:

- Tune all simulation parameters (grid size, diffusion, coupling, etc.)
- Run the simulation
- Explore interactive 3-D plots of the toroidal spiral, Bloch sphere trajectory, field
  heatmaps, entropy timeline, and Lyapunov estimate

---

## Module Descriptions

### `simulator/geometry_module.py`
Implements the golden-angle spiral embedded on a toroidal surface.
- `golden_spiral_torus(t, ...)` – returns a 3-D point on/near the torus at time *t*
- `generate_spiral_path(...)` – vectorised path array
- `torus_surface(...)` – mesh arrays for surface visualisation

### `simulator/bloch_projection.py`
Maps a 2-D field to a Bloch sphere vector and back.
- `field_to_bloch(psi, theta_grid, phi_grid)` – weighted projection to SU(2)
- `bloch_to_density_matrix(r)` / `density_matrix_to_bloch(rho)` – round-trip conversion
- `bloch_sphere_wireframe(n)` – wireframe mesh for plotting

### `simulator/su2_lindblad.py`
Open quantum system dynamics.
- `su2_hamiltonian(omega)` – Hermitian operator from Bloch vector
- `su2_evolve(rho, omega, dt)` – unitary step via matrix exponential
- `lindblad_step(rho, omega, dt, ...)` – unitary + dephasing + amplitude decay

### `simulator/rk4_integrator.py`
4th-order Runge-Kutta step for the dual-hemisphere PDE.
- `rk4_step(Psi_L, Psi_R, M, G, dt, ...)` – advances left/right fields and memory layer

### `simulator/reaction_diffusion_gpu.py`
Full simulation harness (PyTorch tensors, CUDA-ready).
- `run_simulation(...)` – main entry point; returns field snapshots, entropy log,
  Lyapunov estimates, and Bloch trajectory
- `bifurcation_sweep(...)` – sweeps coupling κ and records synchronisation measure

### `simulator/memory_module.py`
Associative memory with hysteresis.
- `MemoryHysteresisEngine` – add, reinforce, decay, conflict-resolve, prune paths
- `shannon_entropy(field)` – discrete Shannon entropy of a positive field

---

## Research Directions

| Topic | Description |
|---|---|
| **Adaptive timestep** | Apply the CFL condition to choose `dt` dynamically and avoid instability |
| **Full Lyapunov spectrum** | Use tangent-space linearisation to compute all exponents, not just the leading one |
| **Fractal boundary layer** | Measure the Hausdorff dimension of the L/R-field boundary at criticality |
| **Bifurcation diagrams** | Sweep κ, β, and ε to map the phase diagram; `bifurcation_sweep()` is a starting point |
| **Stochastic forcing** | Replace the deterministic G term with coloured noise and study noise-induced transitions |

---

## License

MIT — see [LICENSE](LICENSE).
