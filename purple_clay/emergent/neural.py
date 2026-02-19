"""
Neural network emergence simulation.

Models how intelligent behavior emerges from simple neural dynamics.
"""

import numpy as np
import networkx as nx
from typing import Tuple, Optional


class NeuralEmergence:
    """
    Simulates emergence of intelligent patterns in neural networks.
    
    This models how complex computational capabilities can emerge
    from simple local rules in networks of neurons.
    """
    
    def __init__(self, network_size: int = 1000, connectivity: float = 0.1):
        """
        Initialize neural network.
        
        Args:
            network_size: Number of neurons
            connectivity: Probability of connection between neurons
        """
        self.size = network_size
        self.connectivity = connectivity
        
        # Create random network structure
        self.network = nx.erdos_renyi_graph(network_size, connectivity, directed=True)
        
        # Neural states (activations)
        self.activations = np.random.randn(network_size) * 0.1
        
        # Synaptic weights
        self.weights = {}
        for edge in self.network.edges():
            self.weights[edge] = np.random.randn() * 0.1
            
    def step(self, learning_rate: float = 0.01):
        """
        Perform one time step of neural dynamics.
        
        Args:
            learning_rate: Rate of synaptic plasticity
        """
        new_activations = np.zeros(self.size)
        
        # Update each neuron based on inputs
        for node in self.network.nodes():
            # Sum weighted inputs
            input_sum = 0
            for predecessor in self.network.predecessors(node):
                edge = (predecessor, node)
                input_sum += self.weights[edge] * self.activations[predecessor]
            
            # Apply nonlinear activation (tanh)
            new_activations[node] = np.tanh(input_sum)
        
        # Hebbian learning: strengthen active connections
        for edge in self.network.edges():
            i, j = edge
            # Δw = η * pre * post
            self.weights[edge] += learning_rate * self.activations[i] * new_activations[j]
            
            # Weight decay to prevent unbounded growth
            self.weights[edge] *= 0.999
        
        self.activations = new_activations
        
    def apply_stimulus(self, pattern: np.ndarray):
        """
        Apply external stimulus to the network.
        
        Args:
            pattern: Activation pattern to inject
        """
        self.activations[:len(pattern)] = pattern
        
    def measure_synchrony(self) -> float:
        """
        Measure degree of neural synchrony.
        
        High synchrony can indicate emergent collective behavior.
        """
        # Calculate correlation between neurons
        correlations = []
        for i in range(min(100, self.size)):
            for j in range(i+1, min(100, self.size)):
                if self.network.has_edge(i, j) or self.network.has_edge(j, i):
                    correlations.append(self.activations[i] * self.activations[j])
        
        return np.mean(np.abs(correlations)) if correlations else 0.0
    
    def measure_complexity(self) -> float:
        """
        Measure network complexity.
        
        Complex patterns are neither fully ordered nor fully random.
        """
        # Activity variance (0 = inactive, high = chaotic)
        variance = np.var(self.activations)
        
        # Distribution entropy
        bins = np.histogram(self.activations, bins=20)[0]
        probs = bins / np.sum(bins + 1e-10)
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        
        # Complexity balances variance and entropy
        return variance * entropy
    
    def detect_patterns(self) -> dict:
        """
        Detect emergent patterns in network activity.
        
        Returns:
            Dictionary of detected patterns
        """
        return {
            'mean_activation': np.mean(self.activations),
            'activity_variance': np.var(self.activations),
            'synchrony': self.measure_synchrony(),
            'complexity': self.measure_complexity(),
            'active_fraction': np.sum(np.abs(self.activations) > 0.5) / self.size,
            'network_modularity': nx.algorithms.community.modularity(
                self.network,
                nx.algorithms.community.greedy_modularity_communities(self.network.to_undirected())
            )
        }
