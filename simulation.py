import time
import numpy as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sounddevice as sd
import soundfile as sf  # obligatorio para PyInstaller

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
    audio_duration=60.0,
    fs=44100,
    fps=30,
    init_kind="triangular"
):
    x = np.linspace(0, L, N)
    y, x0_audio = create_initial_condition(init_kind, x, L, d0)

    string = String(x, y, c, alpha=alpha)

    dx = x[1] - x[0]
    dt = min(0.5 * dx / c, 0.99 * dx / c)

    # -------- AUDIO --------
    x_fine = np.linspace(0, L, 4000)
    y_fine = np.interp(x_fine, x, y)
    B = compute_modal_coefficients_from_samples(x_fine, y_fine, L, modes)

    signal = generate_modal_sound(
        B, L, c, audio_duration, fs, x0=x0_audio, alpha=alpha
    ).astype(np.float32)

    # Reproducir audio mediante un stream para evitar cortes (mantener referencia)
    sd.default.samplerate = fs
    sd.default.channels = 1

    play_idx = {"i": 0}

    # Callback que reproduce el buffer una sola vez
    def audio_callback(outdata, frames, time_info, status):
        if status:
            print(status)
        i = play_idx["i"]
        chunk = signal[i:i + frames]
        if len(chunk) < frames:
            outdata[:len(chunk), 0] = chunk
            outdata[len(chunk):, 0] = 0
            play_idx["i"] = len(signal)
            raise sd.CallbackStop
        outdata[:, 0] = chunk
        play_idx["i"] += frames

    audio_stream = sd.OutputStream(
        samplerate=fs,
        channels=1,
        dtype="float32",
        callback=audio_callback
    )
    audio_stream.start()

    # -------- ANIMACIÓN --------
    fig, ax = plt.subplots(figsize=(12, 4))
    line, = ax.plot(x, y)
    ax.axhline(0, color="black", alpha=0.3)
    ax.set_xlim([0, L])
    ax.set_ylim([-1.2 * d0, 1.2 * d0])

    t_prev = time.time()

    def update(_):
        nonlocal t_prev
        now = time.time()
        steps = int((now - t_prev) / dt)
        for _ in range(min(steps, 300)):
            string.increment(dt)
            t_prev += dt
        line.set_ydata(string.y[1:-1])
        return line,

    # Guardar la animación en una variable para evitar que el GC la destruya
    anim = FuncAnimation(
        fig,
        update,
        interval=1000 / fps,
        blit=False,
        cache_frame_data=False  # evitar warning de cache y uso de memoria
    )

    # Asociar la animación y el stream de audio a la figura para garantizar su ciclo de vida
    fig._anim = anim
    fig._audio_stream = audio_stream

    # Mostrar sin lanzar un nuevo bucle de eventos de Qt (ya está corriendo)
    plt.show(block=False)

    # Mantener la ventana y el audio hasta que se cierre la figura
    while plt.fignum_exists(fig.number):
        plt.pause(0.05)
        if not audio_stream.active:
            break

    # Si el stream sigue activo al cerrar la ventana, detenerlo
    if audio_stream.active:
        audio_stream.stop()
