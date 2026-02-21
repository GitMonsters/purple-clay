"""
simulator/bloch_projection.py
------------------------------
Mapping between a 2-D field defined on angular coordinates (θ, φ) and the
Bloch sphere representation of a qubit state.
"""

import numpy as np


def to_bloch_vector(v):
    """Normalise *v* to the unit sphere; return north pole for zero vectors.

    Parameters
    ----------
    v : array_like, shape (3,)

    Returns
    -------
    numpy.ndarray, shape (3,)
    """
    norm = np.linalg.norm(v)
    if norm < 1e-10:
        return np.array([0.0, 0.0, 1.0])
    return v / norm


def field_to_bloch(psi, theta_grid, phi_grid):
    """Project a 2-D field *psi* to a Bloch sphere vector.

    Parameters
    ----------
    psi : numpy.ndarray, shape (M, N)
        Field values at grid points.
    theta_grid : numpy.ndarray, shape (M, N)
        Azimuthal angles (toroidal coordinate).
    phi_grid : numpy.ndarray, shape (M, N)
        Polar angles (poloidal coordinate).

    Returns
    -------
    numpy.ndarray, shape (3,)
        Unit Bloch vector [X, Y, Z].
    """
    X = np.sum(psi * np.cos(theta_grid) * np.sin(phi_grid))
    Y = np.sum(psi * np.sin(theta_grid) * np.sin(phi_grid))
    Z = np.sum(psi * np.cos(phi_grid))
    return to_bloch_vector(np.array([X, Y, Z]))


def bloch_to_density_matrix(r):
    """Convert a Bloch vector to a 2×2 density matrix.

    Parameters
    ----------
    r : array_like, shape (3,)
        Bloch vector [X, Y, Z]; must satisfy ‖r‖ ≤ 1 for a physical state.

    Returns
    -------
    numpy.ndarray, shape (2, 2), dtype=complex
    """
    X, Y, Z = r
    return 0.5 * np.array([
        [1 + Z,     X - 1j * Y],
        [X + 1j * Y, 1 - Z   ],
    ], dtype=complex)


def density_matrix_to_bloch(rho):
    """Extract the Bloch vector from a 2×2 density matrix.

    Parameters
    ----------
    rho : numpy.ndarray, shape (2, 2), dtype=complex

    Returns
    -------
    numpy.ndarray, shape (3,)
    """
    X = 2 * rho[0, 1].real
    Y = 2 * rho[1, 0].imag
    Z = (rho[0, 0] - rho[1, 1]).real
    return np.array([X, Y, Z])


def bloch_sphere_wireframe(n=60):
    """Return mesh arrays for a unit sphere wireframe.

    Parameters
    ----------
    n : int
        Number of azimuthal grid points (polar grid uses n//2 points).

    Returns
    -------
    xs, ys, zs : numpy.ndarray, shape (n, n//2)
    """
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n // 2)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(n), np.cos(v))
    return xs, ys, zs
