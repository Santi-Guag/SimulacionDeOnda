# model.py
import numpy as np


class String:
    def __init__(self, x, y0, c, alpha=0.0):
        self.x = np.copy(x)
        self.y = self.pad_array(y0)
        self.y0 = self.pad_array(y0)
        self.c = c
        self.alpha = alpha
        self.y_prev = np.copy(self.y0)

    def pad_array(self, arr):
        return np.concatenate((arr[:1], arr, arr[-1:]))

    def increment(self, dt):
        r = (self.c * dt / np.gradient(self.x))**2
        temp = np.copy(self.y)

        if self.alpha == 0:
            # MODELO SIN AMORTIGUAR
            self.y[1:-1] = (
                2 * self.y[1:-1]
                - self.y_prev[1:-1]
                + r * (self.y[2:] - 2 * self.y[1:-1] + self.y[:-2])
            )
        else:
            # MODELO AMORTIGUADO
            self.y[1:-1] = (
                (2 - self.alpha * dt) * self.y[1:-1]
                - (1 - 0.5 * self.alpha * dt) * self.y_prev[1:-1]
                + r * (self.y[2:] - 2 * self.y[1:-1] + self.y[:-2])
            )

        self.y_prev = temp

        # Condiciones de contorno fijas
        self.y[[0, 1, -2, -1]] = self.y0[[0, 1, -2, -1]]
