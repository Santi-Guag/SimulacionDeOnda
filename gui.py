import sys
from PySide6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QGroupBox,
    QMessageBox
)

from simulation import run_simulation


class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulación ecuación de onda 1D")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        self.init_combo = QComboBox()
        self.init_combo.addItems(["triangular", "fundamental", "harmonic"])

        self.L_spin = QDoubleSpinBox()
        self.L_spin.setRange(1.0, 100.0)
        self.L_spin.setValue(1.0)

        self.c_spin = QDoubleSpinBox()
        self.c_spin.setRange(10.0, 5000.0)
        self.c_spin.setValue(100.0)

        self.alpha_spin = QDoubleSpinBox()
        self.alpha_spin.setRange(0.0, 50.0)
        self.alpha_spin.setValue(0.0)

        self.run_button = QPushButton("▶ Ejecutar simulación")
        self.run_button.clicked.connect(self.run_clicked)

        layout.addWidget(QLabel("Condición inicial"))
        layout.addWidget(self.init_combo)
        layout.addWidget(QLabel("Longitud L"))
        layout.addWidget(self.L_spin)
        layout.addWidget(QLabel("Velocidad c"))
        layout.addWidget(self.c_spin)
        layout.addWidget(QLabel("Amortiguamiento α"))
        layout.addWidget(self.alpha_spin)
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

        try:
            run_simulation(**params)
        except Exception as exc:  # Show the error so bundled EXE failures are visible
            QMessageBox.critical(self, "Error al simular", f"Ocurrió un error:\n{exc}")
        finally:
            self.run_button.setEnabled(True)


def launch_gui():
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec())
