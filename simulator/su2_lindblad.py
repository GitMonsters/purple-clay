"""
simulator/su2_lindblad.py
--------------------------
SU(2) unitary evolution of a qubit density matrix, followed by Lindblad
dissipation for dephasing and amplitude decay.
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
sigma_x = np.array([[0, 1],  [1,  0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0],  [0, -1]], dtype=complex)


def su2_hamiltonian(omega):
    """Construct the Hamiltonian H = ½(ωx σx + ωy σy + ωz σz).

    Parameters
    ----------
    omega : array_like, shape (3,)
        Bloch-vector components [ωx, ωy, ωz] (rad / time unit).

    Returns
    -------
    numpy.ndarray, shape (2, 2), dtype=complex
    """
    return 0.5 * (omega[0] * sigma_x + omega[1] * sigma_y + omega[2] * sigma_z)


def su2_evolve(rho, omega, dt):
    """Evolve density matrix *rho* under unitary SU(2) rotation for time *dt*.

    Uses the exact matrix exponential U = exp(-i H dt).

    Parameters
    ----------
    rho : numpy.ndarray, shape (2, 2), dtype=complex
        Input density matrix.
    omega : array_like, shape (3,)
        Hamiltonian frequency vector.
    dt : float
        Time step.

    Returns
    -------
    numpy.ndarray, shape (2, 2), dtype=complex
    """
    H = su2_hamiltonian(omega)
    U = expm(-1j * H * dt)
    return U @ rho @ U.conj().T


def lindblad_dissipator(rho, L, gamma):
    """Compute the Lindblad super-operator D[L](ρ) = γ(LρL† - ½{L†L, ρ}).

    Parameters
    ----------
    rho : numpy.ndarray, shape (2, 2), dtype=complex
    L : numpy.ndarray, shape (2, 2), dtype=complex
        Jump operator.
    gamma : float
        Dissipation rate.

    Returns
    -------
    numpy.ndarray, shape (2, 2), dtype=complex
    """
    return gamma * (
        L @ rho @ L.conj().T
        - 0.5 * (L.conj().T @ L @ rho + rho @ L.conj().T @ L)
    )


def lindblad_step(rho, omega, dt, gamma_dephasing=0.01, gamma_decay=0.005):
    """Advance *rho* by one time step: unitary rotation + Lindblad dissipation.

    The dissipation channels are:
    - Dephasing  : L = σz, rate *gamma_dephasing*
    - Amplitude decay : L = σ₋ = [[0,1],[0,0]], rate *gamma_decay*

    The density matrix is re-normalised (trace = 1) after each step to prevent
    numerical drift.

    Parameters
    ----------
    rho : numpy.ndarray, shape (2, 2), dtype=complex
    omega : array_like, shape (3,)
    dt : float
    gamma_dephasing : float
    gamma_decay : float

    Returns
    -------
    numpy.ndarray, shape (2, 2), dtype=complex
    """
    rho = su2_evolve(rho, omega, dt)
    rho = rho + dt * lindblad_dissipator(rho, sigma_z, gamma_dephasing)
    rho = rho + dt * lindblad_dissipator(
        rho, np.array([[0, 1], [0, 0]], dtype=complex), gamma_decay
    )
    # Re-normalise trace to prevent numerical drift
    rho = rho / np.trace(rho)
    return rho


def bloch_from_density(rho):
    """Extract the Bloch vector from a 2×2 density matrix.

    Parameters
    ----------
    rho : numpy.ndarray, shape (2, 2), dtype=complex

    Returns
    -------
    numpy.ndarray, shape (3,)
        Bloch vector [X, Y, Z].
    """
    X = 2 * rho[0, 1].real
    Y = 2 * rho[1, 0].imag
    Z = (rho[0, 0] - rho[1, 1]).real
    return np.array([X, Y, Z])
