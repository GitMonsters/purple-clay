# Quick Start Guide

Get started with Purple Clay in 5 minutes!

## Installation

```bash
git clone https://github.com/GitMonsters/purple-clay.git
cd purple-clay
pip install -e .
```

## Your First Simulation

### 1. Emergent Spacetime

See how spacetime emerges from quantum information:

```python
from purple_clay import EmergentSpacetime

# Create a spacetime lattice
spacetime = EmergentSpacetime(lattice_size=(32, 32))

# Initialize with quantum fluctuations
spacetime.initialize_random(amplitude=0.5)

# Evolve the system
for step in range(100):
    spacetime.evolve(steps=1, nonlinear=True)
    
    # Print progress every 10 steps
    if step % 10 == 0:
        entropy = spacetime.calculate_entropy()
        print(f"Step {step}: Entropy = {entropy:.4f}")

# Analyze the emergent geometry
curvature = spacetime.get_curvature()
metric = spacetime.get_metric()

print(f"\nMax curvature: {curvature.max():.4f}")
print(f"Wormhole signature: {spacetime.measure_wormhole_signature():.6f}")
```

### 2. Quantum Information Flow

Explore quantum entanglement:

```python
from purple_clay import QuantumFlow

# Create quantum system with 8 qubits
qflow = QuantumFlow(num_qubits=8)

# Create entanglement with quantum circuit
qflow.apply_entangling_circuit(depth=5)

# Measure entanglement structure
entanglement = qflow.measure_entanglement()
network_info = qflow.plot_entanglement_network()

print(f"Average entanglement: {entanglement.mean():.4f}")
print(f"Network connectivity: {network_info['connectivity']}")
```

### 3. Neural Network Emergence

Watch patterns emerge from neural dynamics:

```python
from purple_clay.emergent.neural import NeuralEmergence
import numpy as np

# Create neural network
neural = NeuralEmergence(network_size=500, connectivity=0.1)

# Apply stimulus
stimulus = np.random.randn(50)
neural.apply_stimulus(stimulus)

# Evolve with learning
for step in range(100):
    neural.step(learning_rate=0.01)

# Detect emergent patterns
patterns = neural.detect_patterns()
print(f"Complexity: {patterns['complexity']:.4f}")
print(f"Synchrony: {patterns['synchrony']:.4f}")
```

### 4. Cosmic Structure Formation

Simulate the universe:

```python
from purple_clay.emergent.cosmic import CosmicStructure

# Create universe
cosmos = CosmicStructure(universe_size=128)

# Start with primordial fluctuations
cosmos.initialize_fluctuations(amplitude=0.01, scale=20)

# Let structures form
for t in range(50):
    cosmos.evolve(dt=0.1)

# Analyze structures
stats = cosmos.detect_structures()
print(f"Number of overdensities: {stats['num_overdensities']}")
print(f"Structure formation: {stats['structure_fraction']:.2%}")

# Get density fields
visible_matter = cosmos.get_density_field()
dark_matter = cosmos.get_dark_matter_field()
```

## Running Demos

Try the included demonstrations:

```bash
# Run all demos
python -m purple_clay.examples.demos

# Or run individually
python -c "from purple_clay.examples import emergent_spacetime_demo; emergent_spacetime_demo()"
python -c "from purple_clay.examples import quantum_flow_demo; quantum_flow_demo()"
python -c "from purple_clay.examples import neural_emergence_demo; neural_emergence_demo()"
python -c "from purple_clay.examples import cosmic_structure_demo; cosmic_structure_demo()"
```

## Understanding the Output

### Entropy
- Measures information/disorder
- Higher entropy = more information spread out
- Related to spacetime area in holography

### Complexity
- Balance between order and chaos
- 0 = fully ordered or random
- Maximum at "edge of chaos"

### Entanglement
- Quantum correlations
- Creates geometric connections
- Basis for emergent spacetime

### Curvature
- Emerges from information density gradients
- Positive curvature = information concentration
- Related to mass/energy in Einstein's equations

## Next Steps

1. **Read the Scientific Background**: See `SCIENTIFIC_BACKGROUND.md` for theory

2. **Explore Examples**: Check `purple_clay/examples/README.md`

3. **Customize Simulations**: Modify parameters and rules

4. **Contribute**: See `CONTRIBUTING.md` to add your ideas

5. **Visualize**: Add matplotlib/plotly visualizations

## Tips

- Start with small lattices (16x16 or 32x32) for fast iteration
- Use fewer qubits (4-8) for quantum simulations initially
- Increase time steps gradually to watch emergence
- Monitor entropy and complexity to understand dynamics

## Common Patterns

### Watching Emergence
```python
# Initialize
system.initialize_random()

# Evolve with monitoring
for i in range(1000):
    system.evolve(steps=1)
    if i % 100 == 0:
        # Measure interesting quantities
        print(f"Step {i}: ...")
```

### Parameter Exploration
```python
# Try different coupling strengths
for coupling in [0.05, 0.1, 0.2]:
    spacetime = EmergentSpacetime(
        lattice_size=(32, 32),
        coupling=coupling
    )
    # ... run and compare
```

### Information Analysis
```python
from purple_clay.core.information import InformationTheory

# Calculate various measures
shannon = InformationTheory.shannon_entropy(probs)
complexity = InformationTheory.calculate_complexity(state)
info_density = InformationTheory.local_information_density(lattice)
```

## Troubleshooting

**Import errors**: Make sure you installed with `pip install -e .`

**Slow simulations**: Reduce lattice size or number of qubits

**Memory issues**: Use smaller system sizes or batch processing

**Numerical instabilities**: Reduce time step or coupling strength

## Get Help

- Open an issue on GitHub
- Check the examples directory
- Read the scientific background
- Review the API documentation (docstrings)

---

**Have fun exploring emergence!** 🌌✨
