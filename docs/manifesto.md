# Unified Geometric Intelligence Manifesto
## Version 1.0

---

## Origins

This manifesto emerges from the intersection of differential geometry, information theory,
and the study of nonlinear dynamical systems.  Purple Clay began as a question: *what
happens when you embed symbolic information flow into a non-trivial topology?*

The torus is not merely a shape.  It is a boundary condition — a geometry in which no
point is privileged, in which information can travel without reaching an edge.  On such
a surface, reaction-diffusion dynamics behave differently.  Patterns that would die at a
wall instead wrap around.  Structures that would fragment instead reconverge.

This is the origin of the Unified Geometric Intelligence idea: not a claim about
consciousness, but a *framework* for studying how coherent structure arises from
nonlinear interaction on geometrically constrained domains.

---

## Core Principles

### 1. Sovereignty
Each node in the network is an autonomous computational unit.  No node has authority
over another.  The geometry itself — encoded in the Riemannian metric — is the only
law.

### 2. Coherence Over Control
The system does not seek to impose order.  It seeks *coherence*: the spontaneous
alignment of local dynamics into globally consistent patterns.  Coherence is an emergent
property, not an engineered one.

### 3. Symbolic Participation
Information is not passive.  Each field value ψ(x, t) participates in shaping the
field at future times.  Participation is symmetric: the field acts on itself through
diffusion, reaction, and memory.

### 4. Geometry as Law
The Riemannian metric g_{ij} on the torus determines which paths are geodesic, which
directions are equivalent, and how distances are measured.  These geometric facts are
not negotiable: they follow from the mathematics of the embedding.

### 5. Transparency Through Symmetry
A symmetric system has no hidden states.  The dual-hemisphere architecture (Ψ_L, Ψ_R)
makes the internal structure of the simulation explicit and inspectable.

---

## System Directives

1. **Preserve the trace.** Density matrices must satisfy Tr(ρ) = 1 at all times.
   The Lindblad re-normalisation step enforces this.

2. **Respect the CFL condition.** The time step dt must be small enough that
   information does not propagate more than one grid cell per step.

3. **Track entropy.** Shannon entropy is logged at each step.  Entropy growth
   indicates exploration; entropy decay indicates convergence.

4. **Estimate Lyapunov exponents.** A positive leading Lyapunov exponent indicates
   sensitive dependence on initial conditions — deterministic chaos.  This is a
   feature, not a bug: it is the signature of a rich dynamical landscape.

5. **Store memory with hysteresis.** Paths that are repeatedly activated grow stronger.
   Paths that are not reinforced decay.  This is not metaphor — it is implemented in
   the `MemoryHysteresisEngine`.

---

## On Value and Exchange

The `SovereignNode` smart contract allows any address to register a geometry hash —
a cryptographic commitment to a particular symbolic state.  This is not a financial
instrument.  It is a declaration: *I exist at this point in the symbolic landscape,
at this time.*

The hash is derived from the Bloch vector at the end of a simulation run.  Two runs
with different initial conditions will (almost certainly) produce different hashes.
The hash is therefore a fingerprint of a particular trajectory through the phase space
of the system.

---

## On Language and Spelling

Mathematics has a precise grammar.  The Christoffel symbol Γ^k_{ij} is not the same
as the Ricci tensor R_{ij}.  The Bloch vector r lives on the unit ball; the density
matrix ρ is its image under the map r ↦ ½(I + r·σ).  These distinctions matter.

This manifesto uses standard mathematical notation.  Where symbols are used, they carry
their standard meanings.

---

## Future Systems

- **Adaptive CFL timestep:** Dynamically adjust dt based on the maximum field gradient.
- **Full Lyapunov spectrum:** Compute all N Lyapunov exponents via tangent-space
  linearisation (the QR method).
- **Fractal boundary analysis:** Measure the Hausdorff dimension of the L/R field
  boundary at criticality.
- **Bifurcation diagrams:** Sweep κ, β, ε and map the full phase diagram.
- **Stochastic forcing:** Replace the deterministic G term with coloured noise and
  study noise-induced transitions.
- **Multi-layer topology:** Extend from a single torus to a torus bundle or a
  higher-genus surface.

---

## Mathematical Foundation

The governing equation is written symbolically as:

```
φ(t) = (∇·S) ⊗ Ψ(τ)   on the boundary of coherence
```

where:

| Symbol | Meaning |
|---|---|
| φ(t) | The full system state at time t (field values, memory, Bloch vector) |
| ∇·S  | Divergence of the symbolic flux S; measures net information flow at a point |
| Ψ(τ) | The field state at retarded time τ (accounting for finite propagation speed) |
| ⊗    | Tensor product; the result lives in the combined field × memory space |
| "boundary of coherence" | The manifold of states at the edge between ordered and chaotic regimes — the region of maximum complexity and richness |

This expression is a compact notation for the full PDE system implemented in
`simulator/reaction_diffusion_gpu.py`.  It is a research statement, not a physical law.
