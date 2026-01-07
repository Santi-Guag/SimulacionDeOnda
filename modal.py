# modal.py
import numpy as np


def safe_trapz(y, x):
    trapz_fn = getattr(np, "trapz", None)
    if trapz_fn is not None:
        return trapz_fn(y, x)
    dx = np.diff(x)
    return float(np.sum(dx * (y[1:] + y[:-1]) * 0.5))


def compute_modal_coefficients_from_samples(x_grid, f_samples, L, modes):
    B = np.zeros(modes + 1)
    for n in range(1, modes + 1):
        phi_n = np.sin(n * np.pi * x_grid / L)
        B[n] = (2 / L) * safe_trapz(f_samples * phi_n, x_grid)
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

    if alpha > 0:
        damping = np.exp(-alpha * t)
        signal *= damping

    signal /= np.max(np.abs(signal)) + 1e-12
    return signal
