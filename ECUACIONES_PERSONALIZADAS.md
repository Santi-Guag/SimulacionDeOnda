# Ecuaciones Personalizadas - Guía de Uso

La funcionalidad de ecuaciones personalizadas permite escribir cualquier condición inicial para la simulación de la onda 1D.

## Cómo usar

1. En la interfaz gráfica, selecciona **"personalizado"** en el dropdown de "Condición inicial"
2. Aparecerá un campo de texto donde puedes escribir tu ecuación
3. La ecuación debe estar expresada en función de `x` (posición)
4. Presiona **"Ejecutar simulación"**

## Variables disponibles

- `x`: Posición (array de 0 a L)
- `L`: Longitud de la cuerda (parámetro que estableces)
- `d0`: Amplitud inicial (0.1 por defecto)

## Funciones matemáticas disponibles

- **Trigonométricas**: `sin()`, `cos()`, `tan()`, `sinh()`, `cosh()`, `tanh()`
- **Exponencial y logaritmo**: `exp()`, `log()`, `log10()`
- **Otras**: `sqrt()`, `abs()`
- **Constantes**: `pi`, `e`

## Ejemplos de ecuaciones

### 1. Onda triangular (equivalente a opción predefinida)
```
d0 * (1 - 2 * abs(x/L - 0.5))
```

### 2. Gaussiana (campana)
```
d0 * exp(-(x - L/2)**2 / (0.1*L)**2)
```

### 3. Cuadrada (step function)
```
d0 * (abs(x - L/2) < L/4)
```

### 4. Seno doble amplitud en el centro
```
d0 * sin(pi*x/L) * (1 + sin(4*pi*x/L))
```


### 6. Exponencial decreciente
```
d0 * exp(-2*x/L)
```

### 7. Arco parabólico
```
d0 * (1 - (2*x/L - 1)**2)
```

### 8. Rampa
```
d0 * x/L
```

### 9. Coseno modulado
```
d0 * cos(pi*x/L) * exp(-3*x/L)
```

### 10. Pulso en el centro
```
d0 * exp(-100*(x - L/2)**2 / L**2)
```

## Validaciones automáticas

El sistema automáticamente valida:

- ✅ **Sintaxis correcta**: Se detectan errores de escritura
- ✅ **Variables válidas**: Solo acepta x, L, d0 y funciones definidas
- ✅ **Resultados numéricos**: Rechaza NaN e infinito
- ✅ **Dimensiones correctas**: El array debe tener mismo tamaño que x
- ✅ **División por cero**: Se detectan divisiones imposibles

## Mensajes de error comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Error de sintaxis" | Falta paréntesis o símbolo incorrecto | Revisa la ecuación |
| "Variable no reconocida" | Usaste variable que no existe | Solo usa x, L, d0 |
| "División por cero" | Divides por 0 | Agrega condiciones (ej: `1/(x+0.01)`) |
| "Valores NaN o infinito" | Operación inválida (ej: sqrt de negativo) | Usa funciones que eviten valores inválidos |
| "Array de tamaño incorrecto" | La ecuación retorna un valor único | Asegúrate de que la ecuación sea vectorial |

## Consejos

1. **Prueba ecuaciones simples primero**: Empieza con `sin(pi*x/L)` antes de ecuaciones complejas
2. **Usa paréntesis**: Para evitar ambigüedades, ej: `d0 * (1 - x/L)` en lugar de `d0 * 1 - x/L`
3. **Evita división por x**: Si necesitas, usa `x + epsilon` para evitar división por cero
4. **Amplitudes razonables**: Mantén los valores entre -1 y 1 para una simulación estable
5. **Ecuaciones simétricas son bonitas**: Producen animaciones más interesantes

## Ejemplo completo de uso

Si quieres una onda que parece una campana descentrada hacia la derecha:

```
d0 * exp(-20 * (x - 0.7*L)**2 / L**2)
```

Entonces:
1. Selecciona "personalizado" en el dropdown
2. Escribe: `d0 * exp(-20 * (x - 0.7*L)**2 / L**2)`
3. Ajusta L, c, α según prefieras
4. ¡Ejecuta!
