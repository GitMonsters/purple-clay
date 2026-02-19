# Purple Clay Examples

This directory contains example simulations demonstrating Purple Clay's capabilities.

## Running Examples

### All Demos
Run all demonstration simulations:
```bash
python -m purple_clay.examples.demos
```

### Individual Demos

#### 1. Emergent Spacetime
```python
from purple_clay.examples import emergent_spacetime_demo
emergent_spacetime_demo(lattice_size=64, steps=500)
```

#### 2. Quantum Information Flow
```python
from purple_clay.examples import quantum_flow_demo
quantum_flow_demo(num_qubits=16, circuit_depth=10)
```

#### 3. Neural Network Emergence
```python
from purple_clay.examples import neural_emergence_demo
neural_emergence_demo(network_size=1000, learning_steps=1000)
```

#### 4. Cosmic Structure Formation
```python
from purple_clay.examples import cosmic_structure_demo
cosmic_structure_demo(universe_size=256, time_steps=1000)
```

## Custom Simulations

You can create custom simulations by combining the core modules:

```python
from purple_clay import EmergentSpacetime, QuantumFlow
from purple_clay.core import InformationTheory

# Create custom emergent spacetime
spacetime = EmergentSpacetime(lattice_size=(128, 128))
spacetime.initialize_random()

# Evolve with custom parameters
for i in range(1000):
    spacetime.evolve(steps=1, nonlinear=True)
    
    if i % 100 == 0:
        entropy = spacetime.calculate_entropy()
        complexity = spacetime.calculate_complexity()
        print(f"Step {i}: Entropy={entropy:.4f}, Complexity={complexity:.4f}")
```
