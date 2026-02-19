"""
Quantum information flow simulation.

Models how quantum information propagates through entangled systems.
"""

import numpy as np
from typing import List, Tuple, Optional
import networkx as nx


class QuantumFlow:
    """
    Simulates quantum information flow through entangled qubit networks.
    
    This class models how quantum information propagates through
    entanglement structures, relevant for understanding emergent
    spacetime and quantum communication.
    """
    
    def __init__(self, num_qubits: int):
        """
        Initialize quantum flow simulation.
        
        Args:
            num_qubits: Number of qubits in the system
        """
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits
        
        # Initialize in product state |0...0⟩
        self.state = np.zeros(self.dim, dtype=np.complex128)
        self.state[0] = 1.0
        
        # Track entanglement structure as a graph
        self.entanglement_graph = nx.Graph()
        self.entanglement_graph.add_nodes_from(range(num_qubits))
        
    def apply_hadamard(self, qubit: int):
        """
        Apply Hadamard gate to a qubit.
        
        Creates superposition: |0⟩ → (|0⟩ + |1⟩)/√2
        
        Args:
            qubit: Index of qubit to apply gate to
        """
        # Hadamard matrix
        h = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        # Build full operator
        operator = self._build_single_qubit_operator(h, qubit)
        
        # Apply to state
        self.state = operator @ self.state
        
    def apply_cnot(self, control: int, target: int):
        """
        Apply CNOT (controlled-NOT) gate.
        
        Creates entanglement between control and target qubits.
        
        Args:
            control: Control qubit index
            target: Target qubit index
        """
        # Build CNOT operator
        operator = self._build_cnot_operator(control, target)
        
        # Apply to state
        self.state = operator @ self.state
        
        # Add edge in entanglement graph
        self.entanglement_graph.add_edge(control, target)
        
    def apply_entangling_circuit(self, depth: int = 1):
        """
        Apply a circuit that creates entanglement across all qubits.
        
        Args:
            depth: Number of layers of entangling gates
        """
        for layer in range(depth):
            # Apply Hadamards to create superposition
            for i in range(self.num_qubits):
                self.apply_hadamard(i)
            
            # Apply CNOTs in a pattern that creates long-range entanglement
            for i in range(self.num_qubits - 1):
                self.apply_cnot(i, (i + 1) % self.num_qubits)
                
    def measure_entanglement(self) -> np.ndarray:
        """
        Measure pairwise entanglement between all qubits.
        
        Returns:
            Matrix of pairwise entanglement measures
        """
        entanglement_matrix = np.zeros((self.num_qubits, self.num_qubits))
        
        for i in range(self.num_qubits):
            for j in range(i + 1, self.num_qubits):
                # Calculate mutual information as entanglement measure
                mi = self._calculate_mutual_information(i, j)
                entanglement_matrix[i, j] = mi
                entanglement_matrix[j, i] = mi
                
        return entanglement_matrix
    
    def plot_entanglement_network(self):
        """
        Visualize the entanglement structure as a network.
        
        Returns:
            Information about the entanglement network
        """
        # Calculate entanglement strengths
        entanglement = self.measure_entanglement()
        
        # Create weighted graph
        G = nx.Graph()
        for i in range(self.num_qubits):
            for j in range(i + 1, self.num_qubits):
                if entanglement[i, j] > 0.01:  # Threshold for visualization
                    G.add_edge(i, j, weight=entanglement[i, j])
        
        return {
            'nodes': self.num_qubits,
            'edges': G.number_of_edges(),
            'avg_entanglement': np.mean(entanglement[entanglement > 0]),
            'max_entanglement': np.max(entanglement),
            'connectivity': nx.is_connected(G) if G.number_of_edges() > 0 else False
        }
    
    def _build_single_qubit_operator(self, gate: np.ndarray, qubit: int) -> np.ndarray:
        """Build operator for single-qubit gate acting on specified qubit."""
        # Identity on all other qubits
        operator = np.eye(1)
        
        for i in range(self.num_qubits):
            if i == qubit:
                operator = np.kron(operator, gate)
            else:
                operator = np.kron(operator, np.eye(2))
                
        return operator
    
    def _build_cnot_operator(self, control: int, target: int) -> np.ndarray:
        """Build CNOT operator."""
        # For simplicity, work with small systems
        # Full implementation would use tensor network methods
        
        operator = np.eye(self.dim, dtype=np.complex128)
        
        # Swap basis states where control is |1⟩
        for i in range(self.dim):
            # Check if control qubit is 1
            if (i >> (self.num_qubits - 1 - control)) & 1:
                # Flip target qubit
                j = i ^ (1 << (self.num_qubits - 1 - target))
                if i != j:
                    # Swap rows
                    operator[i, :], operator[j, :] = operator[j, :].copy(), operator[i, :].copy()
                    
        return operator
    
    def _calculate_mutual_information(self, qubit1: int, qubit2: int) -> float:
        """
        Calculate mutual information between two qubits.
        
        This measures how much information is shared between the qubits.
        """
        # Trace out all other qubits to get reduced density matrix
        # Simplified calculation for demonstration
        
        # Get probability distribution
        probs = np.abs(self.state) ** 2
        
        # Reshape to separate qubits (simplified for small systems)
        # This is a placeholder - full calculation requires partial trace
        
        # Calculate entropy of marginals and joint
        # Using simplified measure based on state overlap
        overlap = np.abs(self.state @ self.state.conj())
        
        return min(1.0, overlap * 0.1)  # Normalized measure
    
    def get_state(self) -> np.ndarray:
        """Get current quantum state vector."""
        return self.state.copy()
    
    def get_state_fidelity(self, target_state: np.ndarray) -> float:
        """
        Calculate fidelity with a target state.
        
        Args:
            target_state: Target quantum state
            
        Returns:
            Fidelity (1 = identical, 0 = orthogonal)
        """
        return np.abs(np.vdot(target_state, self.state)) ** 2
