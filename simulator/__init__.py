"""
simulator/__init__.py
---------------------
Public API for the Purple Clay UGI simulator.
"""

from .geometry_module import golden_spiral_torus, generate_spiral_path, torus_surface
from .bloch_projection import (
    to_bloch_vector,
    field_to_bloch,
    bloch_to_density_matrix,
    density_matrix_to_bloch,
    bloch_sphere_wireframe,
)
from .memory_module import MemoryHysteresisEngine, shannon_entropy
from .su2_lindblad import (
    su2_hamiltonian,
    su2_evolve,
    lindblad_dissipator,
    lindblad_step,
    bloch_from_density,
)
from .rk4_integrator import rk4_step
from .reaction_diffusion_gpu import run_simulation, bifurcation_sweep

__all__ = [
    # geometry
    "golden_spiral_torus",
    "generate_spiral_path",
    "torus_surface",
    # bloch
    "to_bloch_vector",
    "field_to_bloch",
    "bloch_to_density_matrix",
    "density_matrix_to_bloch",
    "bloch_sphere_wireframe",
    # memory
    "MemoryHysteresisEngine",
    "shannon_entropy",
    # su2 / lindblad
    "su2_hamiltonian",
    "su2_evolve",
    "lindblad_dissipator",
    "lindblad_step",
    "bloch_from_density",
    # integrator
    "rk4_step",
    # simulation harness
    "run_simulation",
    "bifurcation_sweep",
]
