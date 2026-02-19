"""
Cosmic structure formation simulation.

Models how galaxies and large-scale structures emerge from density fluctuations.
"""

import numpy as np
from typing import Tuple


class CosmicStructure:
    """
    Simulates formation of cosmic structures from primordial fluctuations.
    
    Models how galaxies, galaxy clusters, and cosmic web emerge from
    tiny quantum fluctuations in the early universe.
    """
    
    def __init__(self, universe_size: int = 256, hubble_constant: float = 0.1):
        """
        Initialize cosmic structure simulation.
        
        Args:
            universe_size: Size of simulation box (grid points)
            hubble_constant: Rate of universe expansion
        """
        self.size = universe_size
        self.H0 = hubble_constant
        
        # Matter density field
        self.density = np.ones((universe_size, universe_size))
        
        # Velocity field (for structure formation)
        self.velocity_x = np.zeros((universe_size, universe_size))
        self.velocity_y = np.zeros((universe_size, universe_size))
        
        # Dark matter distribution (invisible but gravitating)
        self.dark_matter = np.ones((universe_size, universe_size))
        
        self.time = 0
        
    def initialize_fluctuations(self, amplitude: float = 0.01, scale: int = 10):
        """
        Initialize with primordial density fluctuations.
        
        These represent quantum fluctuations from inflation.
        
        Args:
            amplitude: Amplitude of fluctuations
            scale: Characteristic scale of fluctuations
        """
        # Generate Gaussian random field
        for i in range(self.size):
            for j in range(self.size):
                # Sum multiple scales (power spectrum)
                fluctuation = 0
                for k in range(1, 5):
                    phase = np.random.uniform(0, 2*np.pi)
                    wavelength = scale * k
                    fluctuation += amplitude / k * np.cos(2*np.pi*(i+j)/wavelength + phase)
                
                self.density[i, j] += fluctuation
                self.dark_matter[i, j] += fluctuation * 5  # Dark matter dominates
        
    def evolve(self, dt: float = 0.1):
        """
        Evolve the universe forward in time.
        
        Uses simplified N-body dynamics with gravitational attraction.
        
        Args:
            dt: Time step
        """
        # Calculate gravitational potential from density
        potential = self._calculate_potential()
        
        # Update velocities (gravitational acceleration)
        grad_y, grad_x = np.gradient(potential)
        self.velocity_x -= dt * grad_x
        self.velocity_y -= dt * grad_y
        
        # Hubble drag (universe expansion)
        self.velocity_x *= (1 - self.H0 * dt)
        self.velocity_y *= (1 - self.H0 * dt)
        
        # Advect density
        self.density = self._advect_field(self.density, self.velocity_x, self.velocity_y, dt)
        self.dark_matter = self._advect_field(self.dark_matter, self.velocity_x, self.velocity_y, dt)
        
        self.time += dt
        
    def _calculate_potential(self) -> np.ndarray:
        """
        Calculate gravitational potential using Poisson equation.
        
        ∇²φ = 4πG(ρ - ρ_mean)
        """
        # Density perturbation
        delta_rho = self.density + self.dark_matter - np.mean(self.density + self.dark_matter)
        
        # Solve Poisson equation in Fourier space
        fft_delta = np.fft.fft2(delta_rho)
        
        # Fourier space coordinates
        kx = np.fft.fftfreq(self.size) * 2 * np.pi
        ky = np.fft.fftfreq(self.size) * 2 * np.pi
        KX, KY = np.meshgrid(kx, ky)
        K2 = KX**2 + KY**2
        K2[0, 0] = 1  # Avoid division by zero
        
        # φ(k) = -δρ(k) / k²
        fft_potential = -fft_delta / K2
        fft_potential[0, 0] = 0  # No monopole
        
        # Transform back
        potential = np.real(np.fft.ifft2(fft_potential))
        
        return potential
    
    def _advect_field(self, field: np.ndarray, vx: np.ndarray, vy: np.ndarray, dt: float) -> np.ndarray:
        """
        Advect a field along velocity field.
        """
        # Simple upwind scheme
        new_field = field.copy()
        
        for i in range(self.size):
            for j in range(self.size):
                # Trace back along velocity
                x_back = (i - vx[i, j] * dt) % self.size
                y_back = (j - vy[i, j] * dt) % self.size
                
                # Interpolate
                i0, j0 = int(x_back), int(y_back)
                i1, j1 = (i0 + 1) % self.size, (j0 + 1) % self.size
                
                wx, wy = x_back - i0, y_back - j0
                
                new_field[i, j] = (
                    (1-wx) * (1-wy) * field[i0, j0] +
                    wx * (1-wy) * field[i1, j0] +
                    (1-wx) * wy * field[i0, j1] +
                    wx * wy * field[i1, j1]
                )
        
        return new_field
    
    def detect_structures(self) -> dict:
        """
        Detect and characterize emergent structures.
        
        Returns:
            Dictionary of structure statistics
        """
        # Find overdense regions (galaxies/clusters)
        mean_density = np.mean(self.density)
        threshold = mean_density * 2
        
        structures = self.density > threshold
        num_structures = np.sum(structures)
        
        # Power spectrum (measures structure on different scales)
        fft_density = np.fft.fft2(self.density - mean_density)
        power_spectrum = np.abs(fft_density)**2
        
        # Radial average
        center = self.size // 2
        k_values = []
        power_values = []
        
        for i in range(self.size):
            for j in range(self.size):
                k = np.sqrt((i-center)**2 + (j-center)**2)
                if k > 0 and k < center:
                    k_values.append(k)
                    power_values.append(power_spectrum[i, j])
        
        return {
            'num_overdensities': num_structures,
            'mean_density': mean_density,
            'density_variance': np.var(self.density),
            'max_density': np.max(self.density),
            'time': self.time,
            'structure_fraction': num_structures / (self.size * self.size)
        }
    
    def get_density_field(self) -> np.ndarray:
        """Get the visible matter density field."""
        return self.density.copy()
    
    def get_dark_matter_field(self) -> np.ndarray:
        """Get the dark matter density field."""
        return self.dark_matter.copy()
