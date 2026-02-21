"""
simulator/reaction_diffusion_gpu.py
------------------------------------
Full GPU-ready simulation harness for the Purple Clay dual-hemisphere
reaction-diffusion system.

Main entry points
-----------------
run_simulation(...)       – run a single simulation and return results dict
bifurcation_sweep(...)    – sweep coupling κ and record synchronisation measure
"""

import numpy as np
import torch

from .rk4_integrator import rk4_step
from .memory_module import shannon_entropy


def run_simulation(
    N=128,
    alpha=0.03, beta_L=0.6, beta_R=4.5,
    kappa=0.4, lam=0.5, gamma=0.02, eta=0.05, epsilon=0.2,
    dt=0.01, steps=2000,
    quantize=True, track_entropy=True, track_lyapunov=True,
    device=None,
):
    """Run the dual-hemisphere reaction-diffusion simulation.

    The simulation integrates a coupled PDE system on an N×N periodic grid
    using 4th-order Runge-Kutta.  A golden-angle modulated forcing term *G*
    drives the system at each step.

    Parameters
    ----------
    N : int
        Grid size (N×N spatial domain).
    alpha : float
        Diffusion coefficient.
    beta_L, beta_R : float
        Reaction strengths for left and right hemispheres.
    kappa : float
        Inter-hemisphere coupling.
    lam : float
        Memory restoring force.
    gamma : float
        Memory update rate.
    eta : float
        Cubic memory self-suppression.
    epsilon : float
        Geometric forcing amplitude.
    dt : float
        Time step.
    steps : int
        Number of integration steps.
    quantize : bool
        If True, fields are quantised to 6-bit precision after each step.
    track_entropy : bool
        If True, compute and record Shannon entropy each step.
    track_lyapunov : bool
        If True, evolve a perturbed copy and record the log-separation
        (leading Lyapunov estimate) each step.
    device : torch.device or None
        Compute device.  Defaults to CUDA if available, else CPU.

    Returns
    -------
    dict with keys:
        'Psi_L'      : numpy.ndarray, shape (N, N) – left hemisphere snapshot
        'Psi_R'      : numpy.ndarray, shape (N, N) – right hemisphere snapshot
        'M'          : numpy.ndarray, shape (N, N) – memory layer snapshot
        'entropy'    : list[float] (empty if *track_entropy* is False)
        'lyapunov'   : list[float] (empty if *track_lyapunov* is False)
        'bloch_traj' : numpy.ndarray, shape (steps, 3) – Bloch vector per step
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    phi_gr = (1 + 5 ** 0.5) / 2
    golden_angle = 2 * torch.pi * (1 - 1 / phi_gr)

    theta = torch.linspace(0, 2 * torch.pi, N, device=device)
    phi   = torch.linspace(0, 2 * torch.pi, N, device=device)
    Theta, Phi = torch.meshgrid(theta, phi, indexing='ij')

    # Initialise fields with small uniform noise
    Psi_L = torch.rand(N, N, device=device) * 0.1
    Psi_R = torch.rand(N, N, device=device) * 0.1
    M     = torch.zeros(N, N, device=device)

    # Perturbed copy for Lyapunov estimation
    Psi_L2 = Psi_L.clone() + 1e-6
    Psi_R2 = Psi_R.clone() + 1e-6

    entropy_log  = []
    lyapunov_log = []
    bloch_traj   = []

    for t in range(steps):
        # Geometric forcing: golden-angle modulated sinusoidal pattern
        G = torch.sin(Theta + t * dt) * torch.cos(Phi + golden_angle * t * dt)

        Psi_L, Psi_R, M = rk4_step(
            Psi_L, Psi_R, M, G, dt,
            alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon,
        )

        if track_lyapunov:
            Psi_L2, Psi_R2, _ = rk4_step(
                Psi_L2, Psi_R2, M, G, dt,
                alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon,
            )

        if quantize:
            Psi_L = torch.floor(63 * Psi_L.clamp(0, 1)) / 63
            Psi_R = torch.floor(63 * Psi_R.clamp(0, 1)) / 63

        if track_entropy:
            combined = ((Psi_L + Psi_R) / 2).cpu().numpy()
            entropy_log.append(shannon_entropy(combined))

        if track_lyapunov:
            delta = torch.norm(Psi_L - Psi_L2).item()
            lyapunov_log.append(np.log(delta + 1e-12))

        # Bloch projection: weighted average over angular grid
        Ptot = (Psi_L + Psi_R) / 2
        X = torch.sum(Ptot * torch.cos(Theta) * torch.sin(Phi)).item()
        Y = torch.sum(Ptot * torch.sin(Theta) * torch.sin(Phi)).item()
        Z = torch.sum(Ptot * torch.cos(Phi)).item()
        norm = (X ** 2 + Y ** 2 + Z ** 2) ** 0.5 + 1e-8
        bloch_traj.append([X / norm, Y / norm, Z / norm])

    return {
        'Psi_L':     Psi_L.cpu().numpy(),
        'Psi_R':     Psi_R.cpu().numpy(),
        'M':         M.cpu().numpy(),
        'entropy':   entropy_log,
        'lyapunov':  lyapunov_log,
        'bloch_traj': np.array(bloch_traj),
    }


def bifurcation_sweep(
    kappa_range=(0.0, 1.5), n_points=30, steps=1500, N=64, device=None
):
    """Sweep the coupling parameter κ and record a synchronisation measure.

    For each value of κ, a short simulation is run and the Frobenius norm
    ‖Psi_L − Psi_R‖ at the final step is recorded.  A small norm indicates
    near-synchronisation of the two hemispheres.

    Parameters
    ----------
    kappa_range : tuple (float, float)
        Start and end values for κ.
    n_points : int
        Number of κ values to sample.
    steps : int
        Integration steps per κ value.
    N : int
        Grid size.
    device : torch.device or None

    Returns
    -------
    kappas : numpy.ndarray, shape (n_points,)
    sync_measures : numpy.ndarray, shape (n_points,)
        ‖Psi_L − Psi_R‖ at the final step for each κ.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    kappas = np.linspace(*kappa_range, n_points)
    sync_measures = []
    for kappa in kappas:
        result = run_simulation(
            N=N, kappa=kappa, steps=steps,
            track_entropy=False, track_lyapunov=False, device=device,
        )
        diff = np.linalg.norm(result['Psi_L'] - result['Psi_R'])
        sync_measures.append(diff)
    return kappas, np.array(sync_measures)
