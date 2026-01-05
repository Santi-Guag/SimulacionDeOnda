# modal.py
import numpy as np


def compute_modal_coefficients_from_samples(x_grid, f_samples, L, modes):
    B = np.zeros(modes + 1)
    for n in range(1, modes + 1):
        phi_n = np.sin(n * np.pi * x_grid / L)
        B[n] = (2 / L) * np.trapz(f_samples * phi_n, x_grid)
    return B


def generate_modal_sound(B, L, c, duration, fs, x0=None, alpha=0.0):
    t = np.linspace(0, duration, int(fs * duration))
    if x0 is None:
        x0 = L / 2

    signal = np.zeros_like(t)
    modes = len(B) - 1

    for n in range(1, modes + 1):
        omega = n * np.pi * c / L
        spatial = np.sin(n * np.pi * x0 / L)
        signal += B[n] * spatial * np.cos(omega * t)

    # Aplicar amortiguamiento exponencial
    if alpha > 0:
        damping = np.exp(-alpha * t)
        signal *= damping

    signal /= np.max(np.abs(signal)) + 1e-12
    return signal
