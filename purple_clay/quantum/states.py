"""
Quantum state representation and manipulation.
"""

import numpy as np
from typing import Optional


class QuantumState:
    """
    Represents a quantum state (pure or mixed).
    """
    
    def __init__(self, num_qubits: int, pure: bool = True):
        """
        Initialize quantum state.
        
        Args:
            num_qubits: Number of qubits
            pure: If True, represent as state vector; if False, as density matrix
        """
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits
        self.pure = pure
        
        if pure:
            # Initialize to |0...0⟩
            self.state_vector = np.zeros(self.dim, dtype=np.complex128)
            self.state_vector[0] = 1.0
        else:
            # Initialize to maximally mixed state
            self.density_matrix = np.eye(self.dim, dtype=np.complex128) / self.dim
            
    def to_density_matrix(self) -> np.ndarray:
        """Convert to density matrix representation."""
        if self.pure:
            return np.outer(self.state_vector, self.state_vector.conj())
        else:
            return self.density_matrix.copy()
    
    def purity(self) -> float:
        """
        Calculate purity: Tr(ρ²)
        
        Returns:
            Purity (1 = pure state, 1/dim = maximally mixed)
        """
        rho = self.to_density_matrix()
        return np.real(np.trace(rho @ rho))
    
    def apply_unitary(self, unitary: np.ndarray):
        """
        Apply unitary operator.
        
        Args:
            unitary: Unitary matrix
        """
        if self.pure:
            self.state_vector = unitary @ self.state_vector
        else:
            self.density_matrix = unitary @ self.density_matrix @ unitary.conj().T
            
    def partial_trace(self, keep_qubits: list) -> np.ndarray:
        """
        Compute partial trace over qubits not in keep_qubits.
        
        Args:
            keep_qubits: List of qubit indices to keep
            
        Returns:
            Reduced density matrix
        """
        rho = self.to_density_matrix()
        
        # Simplified partial trace for small systems
        # Full implementation would use tensor network contractions
        
        trace_qubits = [i for i in range(self.num_qubits) if i not in keep_qubits]
        
        # For demonstration, return marginal for first kept qubit
        if len(keep_qubits) == 1:
            qubit = keep_qubits[0]
            dim_reduced = 2
            rho_reduced = np.zeros((dim_reduced, dim_reduced), dtype=np.complex128)
            
            # Trace out other qubits
            for i in range(self.dim):
                for j in range(self.dim):
                    # Check if qubits match on the kept qubit
                    i_bit = (i >> (self.num_qubits - 1 - qubit)) & 1
                    j_bit = (j >> (self.num_qubits - 1 - qubit)) & 1
                    
                    # Sum contributions
                    if (i ^ j) == (1 << (self.num_qubits - 1 - qubit)) or i == j:
                        rho_reduced[i_bit, j_bit] += rho[i, j]
                        
            return rho_reduced
            
        return rho  # Fallback
