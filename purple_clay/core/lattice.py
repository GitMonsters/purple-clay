"""
Core lattice structures for spacetime simulations.

This module provides the fundamental lattice structures used in
emergent spacetime and quantum information simulations.
"""

import numpy as np
from typing import Tuple, Optional


class Lattice:
    """
    A discrete lattice structure representing spacetime.
    
    This class implements a 2D lattice with periodic boundary conditions,
    where each site can store quantum information (qubits) or classical data.
    """
    
    def __init__(self, size: Tuple[int, int], dimensions: int = 2):
        """
        Initialize a lattice.
        
        Args:
            size: Tuple of (width, height) for the lattice
            dimensions: Number of spatial dimensions (default: 2)
        """
        self.size = size
        self.dimensions = dimensions
        self.width, self.height = size
        
        # Initialize lattice with complex amplitudes (quantum states)
        self.state = np.zeros(size, dtype=np.complex128)
        
        # Track information density at each site
        self.info_density = np.zeros(size, dtype=np.float64)
        
    def initialize_random(self, amplitude: float = 1.0):
        """
        Initialize the lattice with random quantum states.
        
        Args:
            amplitude: Maximum amplitude for random states
        """
        # Random phases for quantum coherence
        phases = np.random.uniform(0, 2*np.pi, self.size)
        amplitudes = np.random.uniform(0, amplitude, self.size)
        
        self.state = amplitudes * np.exp(1j * phases)
        self._update_info_density()
        
    def initialize_vacuum(self):
        """Initialize to vacuum state (all zeros)."""
        self.state = np.zeros(self.size, dtype=np.complex128)
        self.info_density = np.zeros(self.size, dtype=np.float64)
        
    def _update_info_density(self):
        """Update information density based on quantum state."""
        # Information density proportional to |ψ|^2
        self.info_density = np.abs(self.state) ** 2
        
    def get_neighbors(self, x: int, y: int) -> list:
        """
        Get neighboring sites with periodic boundary conditions.
        
        Args:
            x, y: Coordinates of the site
            
        Returns:
            List of (x, y) tuples for neighboring sites
        """
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx = (x + dx) % self.width
            ny = (y + dy) % self.height
            neighbors.append((nx, ny))
        return neighbors
    
    def calculate_local_curvature(self, x: int, y: int) -> float:
        """
        Calculate local curvature from information gradient.
        
        This is a discrete approximation to how spacetime curves
        based on information density (analogous to Einstein equations).
        
        Args:
            x, y: Coordinates of the site
            
        Returns:
            Local curvature measure
        """
        neighbors = self.get_neighbors(x, y)
        center_density = self.info_density[x, y]
        
        # Laplacian of information density (discrete curvature)
        neighbor_sum = sum(self.info_density[nx, ny] for nx, ny in neighbors)
        curvature = neighbor_sum - 4 * center_density
        
        return curvature
    
    def get_state(self) -> np.ndarray:
        """Get the current quantum state of the lattice."""
        return self.state.copy()
    
    def get_info_density(self) -> np.ndarray:
        """Get the information density distribution."""
        return self.info_density.copy()
