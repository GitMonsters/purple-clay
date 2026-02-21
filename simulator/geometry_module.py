"""
simulator/geometry_module.py
----------------------------
Golden spiral trajectory embedded on a toroidal surface, plus mesh helpers
for visualisation.
"""

import numpy as np

# Golden ratio and derived golden angle
phi = (1 + np.sqrt(5)) / 2
golden_angle = 2 * np.pi * (1 - 1 / phi)

RT = 2.0   # major radius of the torus
rT = 0.75  # minor radius of the torus


def golden_spiral_torus(t, direction='forward', alpha=0.18, beta=0.2,
                        omega=2 * np.pi, r0=2.4, vIn=0.25):
    """Return a 3-D point on (or near) the torus surface at parameter *t*.

    The trajectory starts outside the torus and spirals inward, following
    the golden angle so that successive windings are maximally dispersed.

    Parameters
    ----------
    t : float
        Trajectory parameter (≥ 0).
    direction : {'forward', 'backward'}
        'backward' mirrors the point through the origin.
    alpha : float
        Exponential decay rate after the torus is reached.
    beta : float
        Vertical drift amplitude during the approach phase.
    omega : float
        Angular frequency of the toroidal winding.
    r0 : float
        Initial radial distance from the torus axis.
    vIn : float
        Inward radial velocity during the approach phase.

    Returns
    -------
    numpy.ndarray, shape (3,)
    """
    tHit = (r0 - RT) / vIn
    if t <= tHit:
        rho = max(RT, r0 - vIn * t)
    else:
        rho = RT * np.exp(-alpha * (t - tHit))
    theta = omega * t + golden_angle * t
    z_drift = beta * (t / tHit - 0.5) if t <= tHit else 0
    x = (RT + rho * np.cos(theta)) * np.cos(theta)
    y = (RT + rho * np.cos(theta)) * np.sin(theta)
    z = rho * np.sin(theta) + z_drift
    point = np.array([x, y, z])
    return -point if direction == 'backward' else point


def generate_spiral_path(t_max=40, t_step=0.05, direction='forward'):
    """Return an array of 3-D points along the golden spiral trajectory.

    Parameters
    ----------
    t_max : float
        Upper bound of the trajectory parameter.
    t_step : float
        Sampling interval.
    direction : {'forward', 'backward'}
        Passed through to :func:`golden_spiral_torus`.

    Returns
    -------
    numpy.ndarray, shape (N, 3)
    """
    return np.array([
        golden_spiral_torus(t, direction)
        for t in np.arange(0, t_max, t_step)
    ])


def torus_surface(RT=2.0, rT=0.75, n=40):
    """Return mesh arrays for the torus surface.

    Parameters
    ----------
    RT : float
        Major radius.
    rT : float
        Minor radius.
    n : int
        Number of grid points along each angular coordinate.

    Returns
    -------
    X, Y, Z : numpy.ndarray, shape (n, n)
    """
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, 2 * np.pi, n)
    U, V = np.meshgrid(u, v)
    X = (RT + rT * np.cos(V)) * np.cos(U)
    Y = (RT + rT * np.cos(V)) * np.sin(U)
    Z = rT * np.sin(V)
    return X, Y, Z
