import numpy as np

def validate_safety_and_shear(freq_hz, amp_microns, thickness_mm=5):
    """
    Valida si la frecuencia cumple con los límites de seguridad ISO 2631 
    y genera cizallamiento (shear rate) suficiente.
    """
    omega = 2 * np.pi * freq_hz
    amp_m = amp_microns * 1e-6
    thick_m = thickness_mm * 1e-3
    
    # 1. Cálculo de Aceleración (Seguridad < 0.5 m/s2)
    acceleration = (omega**2) * amp_m
    
    # 2. Cálculo de Shear Rate
    shear_rate = (omega * amp_m) / thick_m
    
    return {
        "Frequency_Hz": freq_hz,
        "Acceleration_m_s2": round(acceleration, 4),
        "Shear_Rate_s1": round(shear_rate, 4),
        "Safe": acceleration < 0.5,
        "Effective_Shear": shear_rate > 1.0
    }

def find_optimal_amplitude(freq_hz, safety_limit=0.5):
    """
    Calcula la amplitud máxima permitida (A) para una frecuencia dada
    sin violar el límite de aceleración de la norma ISO 2631.
    """
    omega = 2 * np.pi * freq_hz
    # A = a / omega^2
    max_amp_m = safety_limit / (omega**2)
    return max_amp_m * 1e6  # Devolver en micrones

# Prueba de concepto para Cascada: 16Hz vs 90Hz
print(f"Test 16Hz: {validate_safety_and_shear(16, 100)}")
print(f"Test 90Hz: {validate_safety_and_shear(90, 10)}")
