"""
simulator/rk4_integrator.py
----------------------------
4th-order Runge-Kutta integrator for the dual-hemisphere reaction-diffusion
system on a 2-D periodic grid (PyTorch tensors, CUDA-compatible).

Left hemisphere  (Psi_L): linear-ish Fisher / logistic reaction.
Right hemisphere (Psi_R): nonlinear cubic (bistable) reaction.
Memory layer     (M)    : slow mean-field coupling between hemispheres.
"""

import torch


def laplacian(P):
    """Discrete periodic Laplacian (second-order finite differences).

    Parameters
    ----------
    P : torch.Tensor, shape (H, W)

    Returns
    -------
    torch.Tensor, shape (H, W)
    """
    return (
        torch.roll(P, 1, 0) + torch.roll(P, -1, 0) +
        torch.roll(P, 1, 1) + torch.roll(P, -1, 1) - 4 * P
    )


def F_L(P):
    """Linear-ish logistic reaction term (left hemisphere analogue).

    Parameters
    ----------
    P : torch.Tensor

    Returns
    -------
    torch.Tensor
    """
    return P * (1 - P)


def F_R(P):
    """Nonlinear cubic (bistable) reaction term (right hemisphere analogue).

    Parameters
    ----------
    P : torch.Tensor

    Returns
    -------
    torch.Tensor
    """
    return P * (1 - P) * (P - 0.5)


def rhs(Psi_L, Psi_R, M, G, alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon):
    """Evaluate the right-hand sides of the dual-hemisphere PDE.

    Parameters
    ----------
    Psi_L, Psi_R : torch.Tensor, shape (N, N)
        Left and right hemisphere field values.
    M : torch.Tensor, shape (N, N)
        Memory / mean-field layer.
    G : torch.Tensor, shape (N, N)
        External geometric forcing term.
    alpha : float
        Diffusion coefficient (shared).
    beta_L, beta_R : float
        Reaction strengths for left and right hemispheres.
    kappa : float
        Inter-hemisphere coupling strength.
    lam : float
        Memory restoring force.
    gamma : float
        Memory update rate.
    eta : float
        Cubic self-suppression of memory.
    epsilon : float
        Geometric forcing amplitude.

    Returns
    -------
    dL, dR, dM : torch.Tensor, shape (N, N)
    """
    dL = (
        alpha * laplacian(Psi_L)
        + beta_L * F_L(Psi_L)
        + kappa * (Psi_R - Psi_L)
        - lam * (Psi_L - M)
        + epsilon * G
    )
    dR = (
        alpha * laplacian(Psi_R)
        + beta_R * F_R(Psi_R)
        + kappa * (Psi_L - Psi_R)
        - lam * (Psi_R - M)
        + epsilon * G
    )
    dM = gamma * (Psi_L + Psi_R - 2 * M) - eta * M ** 3
    return dL, dR, dM


def rk4_step(Psi_L, Psi_R, M, G, dt,
             alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon):
    """Advance the dual-hemisphere system by one RK4 step.

    Parameters
    ----------
    Psi_L, Psi_R, M : torch.Tensor, shape (N, N)
    G : torch.Tensor, shape (N, N)
        Geometric forcing (held constant over the step).
    dt : float
        Time step size.
    alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon : float
        PDE parameters — see :func:`rhs`.

    Returns
    -------
    new_L, new_R, new_M : torch.Tensor, shape (N, N)
    """
    args = (G, alpha, beta_L, beta_R, kappa, lam, gamma, eta, epsilon)
    k1L, k1R, k1M = rhs(Psi_L, Psi_R, M, *args)
    k2L, k2R, k2M = rhs(
        Psi_L + 0.5 * dt * k1L,
        Psi_R + 0.5 * dt * k1R,
        M + 0.5 * dt * k1M,
        *args,
    )
    k3L, k3R, k3M = rhs(
        Psi_L + 0.5 * dt * k2L,
        Psi_R + 0.5 * dt * k2R,
        M + 0.5 * dt * k2M,
        *args,
    )
    k4L, k4R, k4M = rhs(
        Psi_L + dt * k3L,
        Psi_R + dt * k3R,
        M + dt * k3M,
        *args,
    )
    new_L = Psi_L + dt * (k1L + 2 * k2L + 2 * k3L + k4L) / 6
    new_R = Psi_R + dt * (k1R + 2 * k2R + 2 * k3R + k4R) / 6
    new_M = M     + dt * (k1M + 2 * k2M + 2 * k3M + k4M) / 6
    return new_L, new_R, new_M
