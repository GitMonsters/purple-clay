"""
Entanglement measures for quantum systems.
"""

import numpy as np
from typing import Optional


class EntanglementMeasures:
    """
    Compute various measures of quantum entanglement.
    """
    
    @staticmethod
    def concurrence(density_matrix: np.ndarray) -> float:
        """
        Calculate concurrence for a two-qubit state.
        
        Concurrence is a measure of entanglement for two qubits.
        C = 0 means separable, C = 1 means maximally entangled.
        
        Args:
            density_matrix: 4x4 density matrix for two qubits
            
        Returns:
            Concurrence value
        """
        if density_matrix.shape != (4, 4):
            raise ValueError("Concurrence requires a two-qubit density matrix (4x4)")
        
        # Pauli Y matrix
        sigma_y = np.array([[0, -1j], [1j, 0]])
        
        # Construct spin-flipped density matrix
        sigma_y_2 = np.kron(sigma_y, sigma_y)
        rho_tilde = sigma_y_2 @ density_matrix.conj() @ sigma_y_2
        
        # Calculate R = ρ * ρ_tilde
        R = density_matrix @ rho_tilde
        
        # Get eigenvalues in decreasing order
        eigenvalues = np.linalg.eigvalsh(R)
        eigenvalues = np.sqrt(np.maximum(eigenvalues, 0))  # Remove numerical errors
        eigenvalues = np.sort(eigenvalues)[::-1]
        
        # Concurrence
        C = max(0, eigenvalues[0] - eigenvalues[1] - eigenvalues[2] - eigenvalues[3])
        
        return C
    
    @staticmethod
    def negativity(density_matrix: np.ndarray, partition: int) -> float:
        """
        Calculate negativity as an entanglement measure.
        
        Negativity measures how much a state violates the PPT criterion.
        
        Args:
            density_matrix: Density matrix of the full system
            partition: Dimension of first subsystem
            
        Returns:
            Negativity value
        """
        n = density_matrix.shape[0]
        m = n // partition
        
        # Partial transpose with respect to first subsystem
        rho_pt = np.zeros_like(density_matrix)
        
        for i in range(partition):
            for j in range(partition):
                for k in range(m):
                    for l in range(m):
                        # Transpose indices in first subsystem
                        rho_pt[i*m + k, j*m + l] = density_matrix[j*m + k, i*m + l]
        
        # Calculate eigenvalues
        eigenvalues = np.linalg.eigvalsh(rho_pt)
        
        # Negativity is sum of negative eigenvalues
        negativity = np.sum(np.abs(eigenvalues[eigenvalues < 0]))
        
        return negativity
    
    @staticmethod
    def entanglement_of_formation(density_matrix: np.ndarray) -> float:
        """
        Calculate entanglement of formation for two qubits.
        
        Args:
            density_matrix: 4x4 density matrix
            
        Returns:
            Entanglement of formation in ebits
        """
        # Calculate concurrence
        C = EntanglementMeasures.concurrence(density_matrix)
        
        # Entanglement of formation from concurrence
        if C == 0:
            return 0.0
        
        # Helper function h(x)
        def h(x):
            if x == 0 or x == 1:
                return 0
            return -x * np.log2(x) - (1-x) * np.log2(1-x)
        
        # E(ρ) = h((1 + √(1-C²))/2)
        sqrt_term = np.sqrt(1 - C**2)
        E = h((1 + sqrt_term) / 2)
        
        return E
