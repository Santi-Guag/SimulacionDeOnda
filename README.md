# Simulación de onda 1D

Proyecto para el TFG **“Ecuaciones de onda y generación de sonido: implementación computacional de la cuerda vibrante”**. La aplicación permite simular la vibración de una cuerda ideal en 1D, visualizar su evolución en el tiempo y generar el sonido resultante mediante un modelo modal.

## Qué hace la aplicación
- Resuelve numéricamente la ecuación de onda en una cuerda fija en ambos extremos.
- Muestra una animación en tiempo real de la deformación de la cuerda.
- Genera audio sintético usando un modelo modal ajustado a la condición inicial.
- Ofrece condiciones iniciales predefinidas (triangular, fundamental, armónico) y admite ecuaciones personalizadas ingresadas por el usuario.

## Requisitos
- Python 3.10+ (probado con 3.10/3.11)
- Dependencias principales: PySide6, numpy, matplotlib, sounddevice, soundfile
- Instalar requisitos:
	```bash
	pip install -r requirements.txt
	```

## Cómo ejecutar
1. Abrir un terminal en la carpeta del proyecto.
2. Lanzar la interfaz gráfica:
	 ```bash
	 python main.py
	 ```

## Uso básico
1. **Condición inicial**: elegir entre las opciones predefinidas o seleccionar “personalizado”.
2. **Ecuación personalizada** (solo si se elige “personalizado”): escribir una expresión en función de `x` (ej.: `d0 * sin(pi*x/L)`).
3. Ajustar parámetros:
	 - Longitud `L`
	 - Amplitud inicial `d0`
	 - Velocidad de propagación `c`
	 - Amortiguamiento `alpha`
4. Pulsar **“Ejecutar simulación”**. Se abrirá la ventana de animación y se reproducirá el audio generado.

## Notas sobre ecuaciones personalizadas
- Variables disponibles: `x`, `L`, `d0`
- Funciones disponibles: `sin`, `cos`, `tan`, `exp`, `sqrt`, `abs`, `pi`, `e`, `log`, `log10`, `sinh`, `cosh`, `tanh`
- Validaciones automáticas: sintaxis, variables permitidas, tipos numéricos, tamaño del array, ausencia de NaN/Inf y división por cero.
- Ejemplos rápidos:
	- `d0 * sin(pi*x/L)`
	- `d0 * exp(-(x - L/2)**2 / (0.1*L)**2)`
	- `d0 * (1 - abs(2*x/L - 1))`

## Estructura principal
- `main.py`: punto de entrada; lanza la GUI.
- `gui.py`: interfaz PySide6, captura parámetros y lanza la simulación.
- `simulation.py`: arma la condición inicial, genera audio modal y animación matplotlib.
- `modelo.py`: implementación del modelo de cuerda discreta.
- `modal.py`: cálculo de coeficientes modales y síntesis de sonido.
- `ECUACIONES_PERSONALIZADAS.md`: guía ampliada con ejemplos y recomendaciones.

## Consejos de uso
- Si el audio se corta, cierra la ventana de animación y relanza; el stream se libera al cerrar la figura.
- Para ecuaciones personalizadas, empieza con amplitudes pequeñas (`d0` baja) para evitar saturar.
- Puedes aumentar `N` (en `run_simulation`) si necesitas más resolución espacial, teniendo en cuenta el costo computacional.

## Licencia
Uso académico para el TFG. Ajusta la licencia según las necesidades del proyecto.

