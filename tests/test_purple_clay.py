"""
Basic tests for Purple Clay framework.
"""

import pytest
import numpy as np
from purple_clay import EmergentSpacetime, QuantumFlow
from purple_clay.core.lattice import Lattice
from purple_clay.core.evolution import EvolutionOperator
from purple_clay.core.information import InformationTheory
from purple_clay.emergent.neural import NeuralEmergence
from purple_clay.emergent.cosmic import CosmicStructure


class TestLattice:
    """Test lattice functionality."""
    
    def test_initialization(self):
        """Test lattice initialization."""
        lattice = Lattice(size=(10, 10))
        assert lattice.width == 10
        assert lattice.height == 10
        assert lattice.state.shape == (10, 10)
        
    def test_random_initialization(self):
        """Test random initialization."""
        lattice = Lattice(size=(10, 10))
        lattice.initialize_random(amplitude=1.0)
        
        # Should have non-zero states
        assert np.sum(np.abs(lattice.state)) > 0
        
    def test_neighbors(self):
        """Test neighbor calculation."""
        lattice = Lattice(size=(10, 10))
        neighbors = lattice.get_neighbors(5, 5)
        
        assert len(neighbors) == 4
        assert (6, 5) in neighbors
        assert (4, 5) in neighbors


class TestEvolution:
    """Test evolution operators."""
    
    def test_unitary_evolution(self):
        """Test unitary evolution preserves normalization."""
        evolver = EvolutionOperator()
        state = np.random.randn(10, 10) + 1j * np.random.randn(10, 10)
        
        # Normalize
        state /= np.sqrt(np.sum(np.abs(state)**2))
        
        # Evolve
        new_state = evolver.apply_unitary_evolution(state)
        
        # Check normalization preserved
        norm = np.sqrt(np.sum(np.abs(new_state)**2))
        assert np.abs(norm - 1.0) < 1e-10


class TestInformation:
    """Test information theory tools."""
    
    def test_shannon_entropy(self):
        """Test Shannon entropy calculation."""
        # Uniform distribution should have maximum entropy
        probs = np.ones(4) / 4
        entropy = InformationTheory.shannon_entropy(probs)
        assert np.abs(entropy - 2.0) < 1e-10
        
        # Delta distribution should have zero entropy
        probs = np.array([1, 0, 0, 0])
        entropy = InformationTheory.shannon_entropy(probs)
        assert np.abs(entropy) < 1e-10
        
    def test_von_neumann_entropy(self):
        """Test von Neumann entropy."""
        # Pure state should have zero entropy
        rho = np.array([[1, 0], [0, 0]], dtype=np.complex128)
        entropy = InformationTheory.von_neumann_entropy(rho)
        assert np.abs(entropy) < 1e-10


class TestEmergentSpacetime:
    """Test emergent spacetime simulation."""
    
    def test_initialization(self):
        """Test spacetime initialization."""
        spacetime = EmergentSpacetime(lattice_size=(16, 16))
        assert spacetime.lattice.width == 16
        assert spacetime.time_step == 0
        
    def test_evolution(self):
        """Test spacetime evolution."""
        spacetime = EmergentSpacetime(lattice_size=(16, 16))
        spacetime.initialize_random()
        
        initial_entropy = spacetime.calculate_entropy()
        spacetime.evolve(steps=10)
        
        assert spacetime.time_step == 10
        # State should have changed
        final_entropy = spacetime.calculate_entropy()
        assert initial_entropy != final_entropy


class TestQuantumFlow:
    """Test quantum information flow."""
    
    def test_initialization(self):
        """Test quantum flow initialization."""
        qflow = QuantumFlow(num_qubits=4)
        assert qflow.num_qubits == 4
        assert qflow.dim == 16
        
        # Should start in |0000⟩
        assert np.abs(qflow.state[0] - 1.0) < 1e-10
        
    def test_hadamard(self):
        """Test Hadamard gate."""
        qflow = QuantumFlow(num_qubits=1)
        qflow.apply_hadamard(0)
        
        # Should create equal superposition
        assert np.abs(np.abs(qflow.state[0]) - 1/np.sqrt(2)) < 1e-10
        assert np.abs(np.abs(qflow.state[1]) - 1/np.sqrt(2)) < 1e-10
        
    def test_entangling_circuit(self):
        """Test entangling circuit."""
        qflow = QuantumFlow(num_qubits=4)
        qflow.apply_entangling_circuit(depth=2)
        
        # Entanglement should be created
        entanglement = qflow.measure_entanglement()
        assert np.sum(entanglement) > 0


class TestNeuralEmergence:
    """Test neural network emergence."""
    
    def test_initialization(self):
        """Test neural network initialization."""
        neural = NeuralEmergence(network_size=100, connectivity=0.1)
        assert neural.size == 100
        assert len(neural.activations) == 100
        
    def test_evolution(self):
        """Test neural evolution."""
        neural = NeuralEmergence(network_size=100, connectivity=0.1)
        initial_activations = neural.activations.copy()
        
        neural.step()
        
        # State should change
        assert not np.array_equal(initial_activations, neural.activations)


class TestCosmicStructure:
    """Test cosmic structure formation."""
    
    def test_initialization(self):
        """Test cosmic simulation initialization."""
        cosmos = CosmicStructure(universe_size=64)
        assert cosmos.size == 64
        assert cosmos.density.shape == (64, 64)
        
    def test_evolution(self):
        """Test cosmic evolution."""
        cosmos = CosmicStructure(universe_size=64)
        cosmos.initialize_fluctuations(amplitude=0.01)
        
        initial_density = cosmos.density.copy()
        cosmos.evolve(dt=0.1)
        
        # Density should evolve
        assert not np.array_equal(initial_density, cosmos.density)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
