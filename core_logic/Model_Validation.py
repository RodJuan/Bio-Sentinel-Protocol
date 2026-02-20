import numpy as np
from scipy import optimize as opt  # Para optimización
import sympy as sp  # Para derivaciones simbólicas

def validate_safety_and_shear(frequency_hz, amp_microns, thickness_mm=5.0, viscosity_pa_s=100.0, density_kg_m3=1000.0):
    """
    Calcula aceleración mecánica y shear rate en un fluido viscóso bajo vibración oscilatoria.
    Incorpora boundary layer para precisión en regímenes oscilatorios.
    
    Args:
        frequency_hz: Frecuencia en Hz.
        amp_microns: Amplitud de vibración en micrones.
        thickness_mm: Espesor del gap en mm (default: 5.0).
        viscosity_pa_s: Viscosidad dinámica en Pa·s (default: 100.0, para fluidos densos).
        density_kg_m3: Densidad en kg/m³ (default: 1000.0).
    
    Returns:
        Dict con resultados físicos.
    """
    omega = 2 * np.pi * frequency_hz
    A = amp_microns * 1e-6  # micrones a metros
    h = thickness_mm * 1e-3  # mm a metros
    kinematic_viscosity = viscosity_pa_s / density_kg_m3  # ν = η / ρ
    delta = np.sqrt(2 * kinematic_viscosity / omega) if omega > 0 else h  # Espesor de boundary layer
    effective_thickness = min(h, delta)  # Usa el menor para shear concentration
    shear_rate = (omega * A) / effective_thickness if effective_thickness > 0 else 0.0
    acceleration = omega**2 * A  # Aceleración máxima
    safe = acceleration < 0.5  # Umbral aproximado ISO 2631 (max, no rms)
    effective_shear = shear_rate > 1.0  # Arbitrario para thinning significativo
    
    return {
        'Omega (rad/s)': omega,
        'Acceleration (m/s^2)': acceleration,
        'Boundary Layer Thickness (m)': delta,
        'Effective Thickness (m)': effective_thickness,
        'Shear Rate (1/s)': shear_rate,
        'Safe': safe,
        'Effective Shear': effective_shear
    }

# Ejemplo: Optimización para maximizar shear rate con a < 0.5 m/s²
def objective(amp_microns, frequency_hz, thickness_mm, viscosity_pa_s, density_kg_m3):
    """Función objetivo: Minimizar -shear_rate para maximizarlo."""
    return -validate_safety_and_shear(frequency_hz, amp
