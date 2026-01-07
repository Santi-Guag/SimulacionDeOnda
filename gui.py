import sys
from PySide6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QGroupBox,
    QMessageBox, QLineEdit
)

from simulation import run_simulation


class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulación ecuación de onda 1D")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        self.init_combo = QComboBox()
        self.init_combo.addItems(["triangular", "fundamental", "harmonic", "personalizado"])
        self.init_combo.currentTextChanged.connect(self.on_init_changed)
        
        self.custom_equation_label = QLabel("Ecuación (ej: sin(pi*x/L), d0*exp(-x**2))")
        self.custom_equation_label.setVisible(False)
        self.custom_equation_input = QLineEdit()
        self.custom_equation_input.setPlaceholderText("Ingrese la ecuación en función de x")
        self.custom_equation_input.setVisible(False)

        self.L_spin = QDoubleSpinBox()
        self.L_spin.setRange(1.0, 100.0)
        self.L_spin.setValue(1.0)

        self.c_spin = QDoubleSpinBox()
        self.c_spin.setRange(10.0, 5000.0)
        self.c_spin.setValue(100.0)

        self.alpha_spin = QDoubleSpinBox()
        self.alpha_spin.setRange(0.0, 50.0)
        self.alpha_spin.setValue(0.0)

        self.d0_spin = QDoubleSpinBox()
        self.d0_spin.setRange(0.01, 1.0)
        self.d0_spin.setValue(0.1)
        self.d0_spin.setSingleStep(0.01)

        self.run_button = QPushButton("▶ Ejecutar simulación")
        self.run_button.clicked.connect(self.run_clicked)

        layout.addWidget(QLabel("Condición inicial"))
        layout.addWidget(self.init_combo)
        layout.addWidget(self.custom_equation_label)
        layout.addWidget(self.custom_equation_input)
        layout.addWidget(QLabel("Longitud L"))
        layout.addWidget(self.L_spin)
        layout.addWidget(QLabel("Amplitud inicial d0"))
        layout.addWidget(self.d0_spin)
        layout.addWidget(QLabel("Velocidad c"))
        layout.addWidget(self.c_spin)
        layout.addWidget(QLabel("Amortiguamiento α"))
        layout.addWidget(self.alpha_spin)
        layout.addStretch()
        layout.addWidget(self.run_button)

    def on_init_changed(self, text):
        """Mostrar/ocultar campo de ecuación personalizada"""
        is_custom = (text == "personalizado")
        self.custom_equation_label.setVisible(is_custom)
        self.custom_equation_input.setVisible(is_custom)

    def run_clicked(self):
        self.run_button.setEnabled(False)

        init_kind = self.init_combo.currentText()
        
        params = {
            "L": self.L_spin.value(),
            "c": self.c_spin.value(),
            "alpha": self.alpha_spin.value(),
            "d0": self.d0_spin.value(),
            "init_kind": init_kind
        }
        
        # Si es personalizado, validar que haya ecuación
        if init_kind == "personalizado":
            equation = self.custom_equation_input.text().strip()
            if not equation:
                QMessageBox.warning(self, "Ecuación vacía", "Por favor ingrese una ecuación personalizada")
                self.run_button.setEnabled(True)
                return
            params["custom_equation"] = equation

        try:
            run_simulation(**params)
        except ValueError as exc:  
            QMessageBox.warning(self, "Ecuación inválida", f"Error en la ecuación:\n{exc}")
        except Exception as exc:  
            QMessageBox.critical(self, "Error al simular", f"Ocurrió un error:\n{exc}")
        finally:
            self.run_button.setEnabled(True)


def launch_gui():
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec())
