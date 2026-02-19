"""
Demonstration scripts for Purple Clay simulations.

These demos showcase the various capabilities of the framework.
"""

import numpy as np
from purple_clay import EmergentSpacetime, QuantumFlow
from purple_clay.emergent.neural import NeuralEmergence
from purple_clay.emergent.cosmic import CosmicStructure


def emergent_spacetime_demo(lattice_size: int = 64, steps: int = 500):
    """
    Demonstrate emergent spacetime from quantum information.
    
    This simulation shows how geometric properties of spacetime
    can emerge from underlying quantum degrees of freedom.
    
    Args:
        lattice_size: Size of the spacetime lattice
        steps: Number of evolution steps
    """
    print("=" * 60)
    print("EMERGENT SPACETIME SIMULATION")
    print("=" * 60)
    print(f"Lattice size: {lattice_size}x{lattice_size}")
    print(f"Evolution steps: {steps}")
    print()
    
    # Create and initialize spacetime
    spacetime = EmergentSpacetime(lattice_size=(lattice_size, lattice_size))
    spacetime.initialize_random(amplitude=0.5)
    
    print("Initial state:")
    print(f"  Entropy: {spacetime.calculate_entropy():.4f}")
    print(f"  Complexity: {spacetime.calculate_complexity():.4f}")
    print()
    
    # Evolve the system
    print("Evolving spacetime...")
    for i in range(0, steps, steps//10):
        spacetime.evolve(steps=steps//10, nonlinear=True)
        
        entropy = spacetime.calculate_entropy()
        complexity = spacetime.calculate_complexity()
        wormhole = spacetime.measure_wormhole_signature()
        
        print(f"  Step {i+steps//10:4d}: " +
              f"Entropy={entropy:.4f}, " +
              f"Complexity={complexity:.4f}, " +
              f"Wormhole signature={wormhole:.6f}")
    
    print()
    print("Final state visualization data:")
    viz_data = spacetime.visualize(show_entropy=True)
    print(f"  Time step: {viz_data['time_step']}")
    print(f"  Total entropy: {viz_data['total_entropy']:.4f}")
    print(f"  Complexity: {viz_data['complexity']:.4f}")
    print(f"  Max curvature: {np.max(np.abs(viz_data['curvature'])):.4f}")
    print()
    
    return spacetime


def quantum_flow_demo(num_qubits: int = 16, circuit_depth: int = 10):
    """
    Demonstrate quantum information flow through entangled systems.
    
    Args:
        num_qubits: Number of qubits
        circuit_depth: Depth of entangling circuit
    """
    print("=" * 60)
    print("QUANTUM INFORMATION FLOW SIMULATION")
    print("=" * 60)
    print(f"Number of qubits: {num_qubits}")
    print(f"Circuit depth: {circuit_depth}")
    print()
    
    # Create quantum system
    qflow = QuantumFlow(num_qubits=num_qubits)
    
    print("Initial state: |00...0⟩")
    print()
    
    # Apply entangling circuit
    print("Applying entangling circuit...")
    qflow.apply_entangling_circuit(depth=circuit_depth)
    
    print("Circuit applied successfully")
    print()
    
    # Measure entanglement
    print("Measuring entanglement structure...")
    entanglement_matrix = qflow.measure_entanglement()
    
    print(f"  Average entanglement: {np.mean(entanglement_matrix):.4f}")
    print(f"  Max entanglement: {np.max(entanglement_matrix):.4f}")
    print()
    
    # Analyze entanglement network
    network_info = qflow.plot_entanglement_network()
    
    print("Entanglement network:")
    print(f"  Nodes: {network_info['nodes']}")
    print(f"  Edges: {network_info['edges']}")
    print(f"  Avg entanglement: {network_info['avg_entanglement']:.4f}")
    print(f"  Max entanglement: {network_info['max_entanglement']:.4f}")
    print(f"  Connected: {network_info['connectivity']}")
    print()
    
    return qflow


def neural_emergence_demo(network_size: int = 1000, learning_steps: int = 1000):
    """
    Demonstrate emergence of patterns in neural networks.
    
    Args:
        network_size: Number of neurons
        learning_steps: Number of learning iterations
    """
    print("=" * 60)
    print("NEURAL NETWORK EMERGENCE SIMULATION")
    print("=" * 60)
    print(f"Network size: {network_size} neurons")
    print(f"Learning steps: {learning_steps}")
    print()
    
    # Create neural network
    neural = NeuralEmergence(network_size=network_size, connectivity=0.1)
    
    print("Initial state:")
    patterns = neural.detect_patterns()
    for key, value in patterns.items():
        print(f"  {key}: {value:.4f}")
    print()
    
    # Apply random stimulus
    print("Applying stimulus and evolving...")
    stimulus = np.random.randn(50)
    neural.apply_stimulus(stimulus)
    
    # Evolve with learning
    for i in range(0, learning_steps, learning_steps//10):
        for _ in range(learning_steps//10):
            neural.step(learning_rate=0.01)
        
        patterns = neural.detect_patterns()
        print(f"  Step {i+learning_steps//10:4d}: " +
              f"Complexity={patterns['complexity']:.4f}, " +
              f"Synchrony={patterns['synchrony']:.4f}, " +
              f"Active={patterns['active_fraction']:.2%}")
    
    print()
    print("Final patterns:")
    patterns = neural.detect_patterns()
    for key, value in patterns.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value:.2%}")
    print()
    
    return neural


def cosmic_structure_demo(universe_size: int = 256, time_steps: int = 100):
    """
    Demonstrate cosmic structure formation from primordial fluctuations.
    
    Args:
        universe_size: Size of simulation box
        time_steps: Number of evolution steps
    """
    print("=" * 60)
    print("COSMIC STRUCTURE FORMATION SIMULATION")
    print("=" * 60)
    print(f"Universe size: {universe_size}x{universe_size}")
    print(f"Time steps: {time_steps}")
    print()
    
    # Create universe
    cosmos = CosmicStructure(universe_size=universe_size)
    
    # Initialize with quantum fluctuations
    print("Initializing with primordial fluctuations...")
    cosmos.initialize_fluctuations(amplitude=0.01, scale=20)
    
    print("Initial conditions:")
    stats = cosmos.detect_structures()
    print(f"  Mean density: {stats['mean_density']:.4f}")
    print(f"  Density variance: {stats['density_variance']:.6f}")
    print()
    
    # Evolve universe
    print("Evolving universe (structure formation)...")
    for i in range(0, time_steps, time_steps//10):
        for _ in range(time_steps//10):
            cosmos.evolve(dt=0.1)
        
        stats = cosmos.detect_structures()
        print(f"  Time {stats['time']:5.1f}: " +
              f"Structures={stats['num_overdensities']:5d}, " +
              f"Variance={stats['density_variance']:.4f}, " +
              f"Max density={stats['max_density']:.2f}")
    
    print()
    print("Final structure statistics:")
    stats = cosmos.detect_structures()
    for key, value in stats.items():
        if isinstance(value, (int, np.integer)):
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value:.4f}")
    print()
    
    return cosmos


def run_all_demos():
    """Run all demonstration simulations."""
    print("\n" + "=" * 60)
    print("PURPLE CLAY - COMPLETE DEMONSTRATION SUITE")
    print("=" * 60 + "\n")
    
    # Run each demo
    emergent_spacetime_demo(lattice_size=32, steps=200)
    print("\n")
    
    quantum_flow_demo(num_qubits=8, circuit_depth=5)
    print("\n")
    
    neural_emergence_demo(network_size=500, learning_steps=500)
    print("\n")
    
    cosmic_structure_demo(universe_size=128, time_steps=50)
    
    print("\n" + "=" * 60)
    print("ALL DEMONSTRATIONS COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_demos()
