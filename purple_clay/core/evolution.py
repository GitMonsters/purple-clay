"""
Time evolution operators for lattice systems.

Implements various evolution schemes for quantum and classical lattice dynamics.
"""

import numpy as np
from typing import Callable, Optional


class EvolutionOperator:
    """
    Handles time evolution of lattice systems.
    
    Supports both unitary quantum evolution and dissipative classical dynamics.
    """
    
    def __init__(self, coupling_strength: float = 0.1, dt: float = 0.01):
        """
        Initialize evolution operator.
        
        Args:
            coupling_strength: Strength of nearest-neighbor interactions
            dt: Time step for evolution
        """
        self.coupling_strength = coupling_strength
        self.dt = dt
        
    def apply_unitary_evolution(self, state: np.ndarray) -> np.ndarray:
        """
        Apply unitary evolution operator (quantum dynamics).
        
        Uses a simple nearest-neighbor Hamiltonian:
        H = -J Σ(ψ_i† ψ_j + h.c.)
        
        Args:
            state: Current quantum state
            
        Returns:
            Evolved quantum state
        """
        height, width = state.shape
        new_state = state.copy()
        
        # Apply hopping term (nearest-neighbor coupling)
        for i in range(height):
            for j in range(width):
                # Sum over neighbors
                neighbor_sum = (
                    state[(i+1) % height, j] +
                    state[(i-1) % height, j] +
                    state[i, (j+1) % width] +
                    state[i, (j-1) % width]
                )
                
                # Evolve: ψ(t+dt) = ψ(t) - i*dt*H*ψ(t)
                new_state[i, j] = state[i, j] - 1j * self.dt * self.coupling_strength * neighbor_sum
                
        # Normalize to conserve probability
        norm = np.sqrt(np.sum(np.abs(new_state)**2))
        if norm > 0:
            new_state /= norm
            
        return new_state
    
    def apply_diffusion(self, state: np.ndarray, diffusion_rate: float = 0.1) -> np.ndarray:
        """
        Apply diffusion dynamics (classical information spread).
        
        Args:
            state: Current state (real or complex)
            diffusion_rate: Rate of diffusion
            
        Returns:
            Diffused state
        """
        height, width = state.shape
        new_state = np.zeros_like(state)
        
        for i in range(height):
            for j in range(width):
                # Central difference approximation to Laplacian
                laplacian = (
                    state[(i+1) % height, j] +
                    state[(i-1) % height, j] +
                    state[i, (j+1) % width] +
                    state[i, (j-1) % width] -
                    4 * state[i, j]
                )
                
                # Diffusion equation: ∂ψ/∂t = D∇²ψ
                new_state[i, j] = state[i, j] + self.dt * diffusion_rate * laplacian
                
        return new_state
    
    def apply_nonlinear_evolution(self, state: np.ndarray, nonlinearity: float = 0.01) -> np.ndarray:
        """
        Apply nonlinear evolution (self-interaction).
        
        Implements a Gross-Pitaevskii-like equation:
        i∂ψ/∂t = -∇²ψ + g|ψ|²ψ
        
        Args:
            state: Current quantum state
            nonlinearity: Strength of nonlinear term
            
        Returns:
            Evolved state with nonlinear interactions
        """
        # First apply linear evolution
        new_state = self.apply_unitary_evolution(state)
        
        # Add nonlinear term: -i*dt*g|ψ|²ψ
        density = np.abs(state)**2
        new_state -= 1j * self.dt * nonlinearity * density * state
        
        # Renormalize
        norm = np.sqrt(np.sum(np.abs(new_state)**2))
        if norm > 0:
            new_state /= norm
            
        return new_state
