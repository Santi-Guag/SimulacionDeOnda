# Ecuaciones Personalizadas – Guía de Uso

La funcionalidad de **ecuaciones personalizadas** permite al usuario definir libremente la **condición inicial de desplazamiento** de la cuerda para la simulación de la ecuación de onda 1D.

Esto posibilita experimentar con distintos perfiles iniciales y analizar su evolución temporal, así como su impacto en el sonido generado por la simulación.

---

## Cómo usar

1. En la interfaz gráfica, selecciona **"Personalizado"** en el desplegable de **Condición inicial**.
2. Aparecerá un campo de texto editable.
3. Escribe una ecuación en función de `x`.
4. Presiona **"Ejecutar simulación"**.

---

## Variables disponibles

- `x`: Posición espacial (array desde `0` hasta `L`)
- `L`: Longitud total de la cuerda
- `d0`: Amplitud inicial (valor por defecto: `0.1`)

---

## Funciones matemáticas disponibles

- **Trigonométricas**:  
  `sin()`, `cos()`, `tan()`, `sinh()`, `cosh()`, `tanh()`

- **Exponenciales y logarítmicas**:  
  `exp()`, `log()`, `log10()`

- **Otras**:  
  `sqrt()`, `abs()`

- **Constantes**:  
  `pi`, `e`

---

## Ejemplos de ecuaciones

### 🔹 Modos propios (soluciones analíticas)

#### 1. Modo fundamental (n = 1)
d0 * sin(pi * x / L)

#### 2. Segundo modo (n = 2)
d0 * sin(2 * pi * x / L)

#### 3. Tercer modo (n = 3)
d0 * sin(3 * pi * x / L)

#### 4. Superposición de modos
d0 * (sin(pix/L) + 0.5sin(2pix/L))

---

### 🔹 Excitaciones localizadas (pulsos)

#### 5. Pulso gaussiano centrado
d0 * exp(-(x - L/2)**2 / (0.1*L)**2)

#### 6. Pulso gaussiano desplazado
d0 * exp(-20 * (x - 0.7*L)2 / L2)

#### 7. Pulso estrecho (impacto tipo martillo)
d0 * exp(-100 * (x - L/2)2 / L2)

---

### 🔹 Formas geométricas simples

#### 8. Onda triangular (cuerda punteada)
d0 * (1 - 2 * abs(x/L - 0.5))

#### 9. Arco parabólico
d0 * (1 - (2*x/L - 1)**2)

#### 10. Rampa lineal
d0 * x / L

---

### 🔹 Excitaciones no suaves (experimentales)

#### 11. Función escalón
d0 * (abs(x - L/2) < L/4)

---

### 🔹 Ondas moduladas

#### 12. Seno modulado en amplitud
d0 * sin(pix/L) * (1 + sin(4pi*x/L))

#### 13. Coseno amortiguado (oscilatorio)
d0 * cos(4pix/L) * exp(-3*x/L)
#### 14. Onda localizada oscilante
d0 * sin(6pix/L) * exp(-10*(x - L/2)2 / L2)

---

## ✅ Validaciones automáticas

El sistema valida automáticamente:

- ✅ Sintaxis correcta
- ✅ Uso exclusivo de variables permitidas
- ✅ Resultados numéricos finitos
- ✅ Dimensión correcta del array
- ✅ Prevención de divisiones por cero

---

## Mensajes de error comunes

| Error | Causa | Solución |
|------|------|---------|
| Error de sintaxis | Paréntesis o símbolos incorrectos | Revisa la ecuación |
| Variable no reconocida | Variable inexistente | Usa solo `x`, `L`, `d0` |
| División por cero | Denominador nulo | Usa `x + ε` |
| Valores NaN o infinito | Operación inválida | Ajusta la función |
| Tamaño incorrecto | No es vectorial | Usa operaciones con `x` |

---

## Consejos de uso

1. Empieza con ecuaciones simples.
2. Usa paréntesis explícitos.
3. Evita divisiones directas por `x`.
4. Mantén amplitudes moderadas (`|y| < 1`).
5. Las funciones suaves producen animaciones y sonido más estables.
6. Los modos propios generan sonidos más puros.


