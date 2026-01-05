# simulation.py
import time
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # Usar backend compatible con Qt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd

from modelo import String
from modal import (
    compute_modal_coefficients_from_samples,
    generate_modal_sound
)


def create_initial_condition(kind, x, L, d0):
    if kind == "triangular":
        d0_loc = 0.8
        y = np.empty_like(x)
        left = x <= d0_loc * L
        y[left] = d0 / (d0_loc * L) * x[left]
        y[~left] = -d0 / ((1.0 - d0_loc) * L) * (x[~left] - L)
        x0_audio = 0.25 * L

    elif kind == "fundamental":
        y = d0 * np.sin(np.pi * x / L)
        x0_audio = 0.5 * L

    elif kind == "harmonic":
        y = d0 * np.sin(2 * np.pi * x / L)
        x0_audio = 0.25 * L

    else:
        raise ValueError("Condición inicial no válida")

    return y, x0_audio


def run_simulation(
    L=1.0,
    c=100.0,
    N=256,
    alpha=0.0,
    d0=0.1,
    modes=60,
    audio_duration=5.0,
    fs=44100,
    fps=30,
    init_kind="triangular"
):
    x = np.linspace(0, L, N)
    y, x0_audio = create_initial_condition(init_kind, x, L, d0)

    string = String(x, y, c, alpha=alpha)

    dx = x[1] - x[0]
    dt = min(0.5 * dx / c, 0.99 * dx / c)
    print(f"dt = {dt}, alpha = {alpha}")

    # ---------------- AUDIO ----------------
    x_fine = np.linspace(0, L, 4000)
    y_fine = np.interp(x_fine, x, y)
    B = compute_modal_coefficients_from_samples(x_fine, y_fine, L, modes)
    signal = generate_modal_sound(B, L, c, audio_duration, fs, x0=x0_audio, alpha=alpha)

    # Generar audio más largo para que no se corte antes de cerrar la ventana
    max_duration = 60.0  # Duración máxima de 60 segundos
    signal_long = generate_modal_sound(B, L, c, max_duration, fs, x0=x0_audio, alpha=alpha)
    
    sd.play(signal_long, fs)

    # ---------------- ANIMACIÓN ----------------
    plt.ion()  # Activar modo interactivo
    fig, ax = plt.subplots(figsize=(12, 4))
    line, = ax.plot(x, y)
    ax.axhline(0, color="black", alpha=0.3)
    ax.set_xlim([0, L])
    ax.set_ylim([-1.2*d0, 1.2*d0])
    ax.set_xlabel("x")
    ax.set_ylabel("desplazamiento")

    t_prev = time.time()

    def update(frame):
        nonlocal t_prev
        now = time.time()
        steps = int((now - t_prev) / dt)
        for _ in range(min(steps, 300)):
            string.increment(dt)
            t_prev += dt
        line.set_ydata(string.y[1:-1])
        return line,

    ani = FuncAnimation(
        fig,
        update,
        frames=100000,
        interval=1000 / fps,
        blit=False
    )

    plt.show(block=False)
    
    # Mantener la ventana abierta hasta que el usuario la cierre
    try:
        while plt.fignum_exists(fig.number):
            plt.pause(0.1)
    finally:
        sd.stop()  # Detener el audio cuando se cierre la ventana
