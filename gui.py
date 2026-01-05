# gui.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QGroupBox
)
from PySide6.QtCore import QTimer

from simulation import run_simulation


class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulación ecuación de onda 1D")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # -------- Condición inicial --------
        group_init = QGroupBox("Condición inicial")
        layout_init = QVBoxLayout()

        self.init_combo = QComboBox()
        self.init_combo.addItems([
            "triangular",
            "fundamental",
            "harmonic"
        ])

        layout_init.addWidget(QLabel("Tipo"))
        layout_init.addWidget(self.init_combo)
        group_init.setLayout(layout_init)

        # -------- Parámetros físicos --------
        group_params = QGroupBox("Parámetros físicos")
        layout_params = QVBoxLayout()

        self.L_spin = QDoubleSpinBox()
        self.L_spin.setRange(1.0, 100.0)
        self.L_spin.setValue(1.0)

        self.c_spin = QDoubleSpinBox()
        self.c_spin.setRange(10.0, 5000.0)
        self.c_spin.setValue(100.0)

        self.alpha_spin = QDoubleSpinBox()
        self.alpha_spin.setRange(0.0, 50.0)
        self.alpha_spin.setValue(0.0)

        layout_params.addWidget(QLabel("Longitud L"))
        layout_params.addWidget(self.L_spin)
        layout_params.addWidget(QLabel("Velocidad c"))
        layout_params.addWidget(self.c_spin)
        layout_params.addWidget(QLabel("Amortiguamiento α"))
        layout_params.addWidget(self.alpha_spin)

        group_params.setLayout(layout_params)

        # -------- Botón --------
        self.run_button = QPushButton("▶ Ejecutar simulación")
        self.run_button.clicked.connect(self.run_clicked)

        layout.addWidget(group_init)
        layout.addWidget(group_params)
        layout.addStretch()
        layout.addWidget(self.run_button)

    def run_clicked(self):
        self.run_button.setEnabled(False)

        params = {
            "L": self.L_spin.value(),
            "c": self.c_spin.value(),
            "alpha": self.alpha_spin.value(),
            "init_kind": self.init_combo.currentText()
        }

        # Ejecutar en el hilo principal con un pequeño delay
        QTimer.singleShot(100, lambda: self.start_simulation(params))

    def start_simulation(self, params):
        try:
            run_simulation(**params)
        finally:
            self.run_button.setEnabled(True)


def launch_gui():
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec())
