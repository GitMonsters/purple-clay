"""
simulator/memory_module.py
--------------------------
Associative memory with hysteresis: path strengths grow through reinforcement,
decay exponentially over time, and can be weakened by conflict resolution.

Also exposes a discrete Shannon entropy utility for field arrays.
"""

import numpy as np


class MemoryHysteresisEngine:
    """Associative memory store with hysteresis dynamics.

    Paths are keyed by arbitrary hashable identifiers.  Each path has a
    *strength* in [0, 1].  Strengths increase on reinforcement (capped at 1),
    decay exponentially with time, and can be reduced when conflicting paths
    are resolved.  Paths below *threshold* are considered inactive and can be
    pruned.

    Parameters
    ----------
    decay_rate : float
        Per-unit-time exponential decay constant (λ in e^{-λ·dt}).
    conflict_factor : float
        Multiplicative penalty applied to each path in a conflict set.
    reinforce_delta : float
        Strength increment added when an existing path is reinforced.
    threshold : float
        Minimum strength for a path to be considered active.
    """

    def __init__(self, decay_rate=0.01, conflict_factor=0.5,
                 reinforce_delta=0.2, threshold=0.1):
        self.paths = {}
        self.decay_rate = decay_rate
        self.conflict_factor = conflict_factor
        self.reinforce_delta = reinforce_delta
        self.threshold = threshold

    def add_or_reinforce(self, key, data=None):
        """Add a new path at full strength, or reinforce an existing one.

        Parameters
        ----------
        key : hashable
            Path identifier.
        data : object, optional
            Arbitrary payload stored alongside the strength.
        """
        if key in self.paths:
            self.paths[key]['strength'] = min(
                1.0, self.paths[key]['strength'] + self.reinforce_delta
            )
        else:
            self.paths[key] = {'strength': 1.0, 'data': data}

    def apply_decay(self, dt=1.0):
        """Decay all path strengths by one time step *dt*.

        Parameters
        ----------
        dt : float
            Elapsed time (arbitrary units consistent with *decay_rate*).
        """
        for key in list(self.paths.keys()):
            self.paths[key]['strength'] *= np.exp(-self.decay_rate * dt)

    def resolve_conflict(self, keys):
        """Apply a conflict penalty to each path in *keys*.

        Parameters
        ----------
        keys : iterable
            Path identifiers that are in conflict.
        """
        for key in keys:
            if key in self.paths:
                self.paths[key]['strength'] *= (1 - self.conflict_factor)

    def prune(self):
        """Remove all paths whose strength is below *threshold*."""
        self.paths = {
            k: v for k, v in self.paths.items()
            if v['strength'] >= self.threshold
        }

    def active_memory(self):
        """Return only paths at or above *threshold*.

        Returns
        -------
        dict
        """
        return {
            k: v for k, v in self.paths.items()
            if v['strength'] >= self.threshold
        }

    def summary(self):
        """Return a {key: strength} mapping rounded to 4 decimal places.

        Returns
        -------
        dict
        """
        return {k: round(v['strength'], 4) for k, v in self.paths.items()}


def shannon_entropy(field):
    """Compute the discrete Shannon entropy of a non-negative field.

    Treats normalised field values as a probability distribution.

    Parameters
    ----------
    field : numpy.ndarray
        Array of non-negative values.

    Returns
    -------
    float
        Shannon entropy H = -Σ p_i log(p_i).  Returns 0.0 for a zero field.
    """
    flat = field.flatten()
    flat = flat[flat > 0]
    total = flat.sum()
    if total == 0:
        return 0.0
    p = flat / total
    return -np.sum(p * np.log(p + 1e-12))
