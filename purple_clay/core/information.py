"""
Information theory tools for analyzing complex systems.

Provides functions to calculate entropy, mutual information,
and other information-theoretic quantities.
"""

import numpy as np
from typing import Optional, Tuple
from scipy.linalg import logm


class InformationTheory:
    """
    Information theory calculations for quantum and classical systems.
    """
    
    @staticmethod
    def shannon_entropy(probabilities: np.ndarray) -> float:
        """
        Calculate Shannon entropy: H = -Σ p_i log(p_i)
        
        Args:
            probabilities: Probability distribution (must sum to 1)
            
        Returns:
            Shannon entropy in bits
        """
        # Remove zero probabilities to avoid log(0)
        p = probabilities[probabilities > 0]
        return -np.sum(p * np.log2(p))
    
    @staticmethod
    def von_neumann_entropy(density_matrix: np.ndarray) -> float:
        """
        Calculate von Neumann entropy: S = -Tr(ρ log ρ)
        
        Args:
            density_matrix: Quantum density matrix
            
        Returns:
            von Neumann entropy
        """
        # Get eigenvalues of density matrix
        eigenvalues = np.linalg.eigvalsh(density_matrix)
        
        # Remove numerical zeros
        eigenvalues = eigenvalues[eigenvalues > 1e-12]
        
        # S = -Σ λ_i log(λ_i)
        return -np.sum(eigenvalues * np.log2(eigenvalues))
    
    @staticmethod
    def mutual_information(joint_prob: np.ndarray) -> float:
        """
        Calculate mutual information: I(X:Y) = H(X) + H(Y) - H(X,Y)
        
        Args:
            joint_prob: Joint probability distribution P(X,Y)
            
        Returns:
            Mutual information in bits
        """
        # Marginal distributions
        p_x = np.sum(joint_prob, axis=1)
        p_y = np.sum(joint_prob, axis=0)
        
        # Calculate entropies
        h_x = InformationTheory.shannon_entropy(p_x)
        h_y = InformationTheory.shannon_entropy(p_y)
        h_xy = InformationTheory.shannon_entropy(joint_prob.flatten())
        
        return h_x + h_y - h_xy
    
    @staticmethod
    def entanglement_entropy(state: np.ndarray, partition: int) -> float:
        """
        Calculate entanglement entropy for a bipartite quantum state.
        
        Args:
            state: Quantum state vector
            partition: Index where to partition the system
            
        Returns:
            Entanglement entropy
        """
        # Reshape state into bipartite form
        n = len(state)
        dim_a = partition
        dim_b = n // partition
        
        if dim_a * dim_b != n:
            raise ValueError("State dimension must be divisible by partition size")
        
        # Reshape state vector into matrix
        psi_matrix = state.reshape(dim_a, dim_b)
        
        # Calculate reduced density matrix for subsystem A
        # ρ_A = Tr_B(|ψ⟩⟨ψ|)
        rho_a = psi_matrix @ psi_matrix.conj().T
        
        # Calculate von Neumann entropy of reduced density matrix
        return InformationTheory.von_neumann_entropy(rho_a)
    
    @staticmethod
    def calculate_complexity(state: np.ndarray) -> float:
        """
        Calculate statistical complexity of a state.
        
        Uses a measure based on the balance between order and randomness.
        
        Args:
            state: Quantum or classical state
            
        Returns:
            Complexity measure (0 = ordered or random, >0 = complex)
        """
        # Convert to probability distribution
        probabilities = np.abs(state.flatten())**2
        probabilities /= np.sum(probabilities)
        
        # Entropy (disorder)
        entropy = InformationTheory.shannon_entropy(probabilities)
        
        # Disequilibrium (deviation from uniform)
        n = len(probabilities)
        uniform = np.ones(n) / n
        disequilibrium = np.sum((probabilities - uniform)**2)
        
        # Complexity is product of entropy and disequilibrium
        max_entropy = np.log2(n)
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return normalized_entropy * disequilibrium
    
    @staticmethod
    def local_information_density(lattice_state: np.ndarray) -> np.ndarray:
        """
        Calculate local information density on a lattice.
        
        Args:
            lattice_state: 2D lattice of quantum amplitudes
            
        Returns:
            2D array of local information densities
        """
        # Information density from probability density
        density = np.abs(lattice_state)**2
        
        # Add contribution from phase gradients (information in correlations)
        phase = np.angle(lattice_state)
        
        # Calculate gradient magnitude (how quickly phase changes)
        grad_y, grad_x = np.gradient(phase)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Total information density
        info_density = density * (1 + gradient_magnitude)
        
        return info_density
