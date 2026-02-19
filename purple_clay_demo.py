#!/usr/bin/env python3
"""
Purple Clay - Interactive Demonstration

This script provides an interactive demonstration of Purple Clay's capabilities.
Run it to see emergent phenomena in action!
"""

import sys


def main():
    """Run the interactive Purple Clay demonstration."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                        🌌 PURPLE CLAY 🌌                            ║
║                                                                      ║
║     A Scientific Framework for Emergent Systems & Quantum Info      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Purple Clay explores fundamental questions about reality through
computational models. Choose a simulation to explore:

1. 🌊 Emergent Spacetime - Watch geometry emerge from quantum information
2. 🔬 Quantum Information Flow - Visualize quantum entanglement networks
3. 🧠 Neural Emergence - See intelligence-like patterns form
4. 🌟 Cosmic Structure - Model galaxy formation from quantum fluctuations
5. 🎬 Run All Demos - Experience the complete suite
6. ❌ Exit

""")
    
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                run_spacetime_demo()
            elif choice == '2':
                run_quantum_demo()
            elif choice == '3':
                run_neural_demo()
            elif choice == '4':
                run_cosmic_demo()
            elif choice == '5':
                run_all_demos()
            elif choice == '6':
                print("\n✨ Thank you for exploring Purple Clay! Keep questioning the universe! ✨\n")
                break
            else:
                print("Invalid choice. Please enter 1-6.")
                continue
                
            input("\nPress Enter to continue...")
            print("\n" + "="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n✨ Thank you for exploring Purple Clay! ✨\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please report this issue on GitHub.\n")


def run_spacetime_demo():
    """Run the emergent spacetime demonstration."""
    from purple_clay.examples import emergent_spacetime_demo
    
    print("\n" + "="*70)
    print("🌊 EMERGENT SPACETIME SIMULATION")
    print("="*70)
    print("""
This simulation demonstrates how classical spacetime geometry can emerge
from underlying quantum information. Based on the ER=EPR conjecture and
holographic principle, watch as:

- Quantum information density creates emergent curvature
- Entanglement patterns form geometric structures
- Wormhole-like connections appear between distant regions

Key Concept: "Geometry is quantum information in disguise"
    """)
    
    size = input("Lattice size (default 32, larger=slower): ").strip() or "32"
    steps = input("Evolution steps (default 200): ").strip() or "200"
    
    emergent_spacetime_demo(
        lattice_size=int(size),
        steps=int(steps)
    )


def run_quantum_demo():
    """Run the quantum information flow demonstration."""
    from purple_clay.examples import quantum_flow_demo
    
    print("\n" + "="*70)
    print("🔬 QUANTUM INFORMATION FLOW SIMULATION")
    print("="*70)
    print("""
This simulation explores how quantum information propagates through
entangled qubit networks. Watch as:

- Quantum gates create entanglement between qubits
- Information becomes non-local
- Entanglement network structure emerges

Key Concept: "Quantum entanglement connects distant parts of the universe"
    """)
    
    qubits = input("Number of qubits (default 8, max ~12): ").strip() or "8"
    depth = input("Circuit depth (default 5): ").strip() or "5"
    
    quantum_flow_demo(
        num_qubits=int(qubits),
        circuit_depth=int(depth)
    )


def run_neural_demo():
    """Run the neural emergence demonstration."""
    from purple_clay.examples import neural_emergence_demo
    
    print("\n" + "="*70)
    print("🧠 NEURAL NETWORK EMERGENCE SIMULATION")
    print("="*70)
    print("""
This simulation models how intelligent-like patterns emerge from simple
neural dynamics. Watch as:

- Neurons self-organize through Hebbian learning
- Synchrony and complexity increase
- Patterns emerge from chaos

Key Concept: "Intelligence emerges from simple local rules"
    """)
    
    size = input("Network size (default 500): ").strip() or "500"
    steps = input("Learning steps (default 500): ").strip() or "500"
    
    neural_emergence_demo(
        network_size=int(size),
        learning_steps=int(steps)
    )


def run_cosmic_demo():
    """Run the cosmic structure demonstration."""
    from purple_clay.examples import cosmic_structure_demo
    
    print("\n" + "="*70)
    print("🌟 COSMIC STRUCTURE FORMATION SIMULATION")
    print("="*70)
    print("""
This simulation models how galaxies and large-scale structures form
from tiny quantum fluctuations in the early universe. Watch as:

- Primordial density fluctuations grow gravitationally
- Dark matter forms the cosmic web
- Galaxies emerge at density peaks

Key Concept: "Today's galaxies were once quantum fluctuations"
    """)
    
    size = input("Universe size (default 128, larger=slower): ").strip() or "128"
    steps = input("Time steps (default 50): ").strip() or "50"
    
    cosmic_structure_demo(
        universe_size=int(size),
        time_steps=int(steps)
    )


def run_all_demos():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("🎬 RUNNING COMPLETE DEMONSTRATION SUITE")
    print("="*70)
    print("\nThis will run all four simulations with default parameters.\n")
    
    from purple_clay.examples.demos import run_all_demos
    run_all_demos()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✨ Goodbye! ✨\n")
        sys.exit(0)
