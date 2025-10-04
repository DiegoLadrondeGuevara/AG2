# Simulación de Movimiento con y sin Memoria

Este proyecto resuelve numéricamente el movimiento de una partícula esférica en un fluido viscoso bajo la influencia de la gravedad, comparando dos modelos:

- ✅ Modelo **sin memoria** (solución analítica)
- ✅ Modelo **con memoria** (usando el método de Runge-Kutta de orden 4)

Incluye:
- Tablas de resultados (velocidad y posición)
- Comparación de parámetros físicos (τ y v∞)
- Gráficas para visualizar ambos modelos

---

## ⚙️ Requisitos

Este proyecto requiere Python 3.x y las siguientes librerías:

- [`numpy`](https://numpy.org/) – Para cálculos numéricos
- [`pandas`](https://pandas.pydata.org/) – Para manipulación de tablas
- [`matplotlib`](https://matplotlib.org/) – Para graficar los resultados

---

## 💾 Instalación de dependencias

Puedes instalar todas las dependencias con:

```bash
pip install numpy pandas matplotlib scipy
```
---
### Pregunta 10 (Detalles de resultados sobre el código)

**Variables:**  
`v(t)` (velocidad) y `w(t)` (memoria/convolución)

**Parámetros memoria:**  
`α = 10⁻⁷ kg/s²`, `β = 5.0 s⁻¹`

**Integrador:**  
RK4 con paso `dt = 10⁻⁶` s (1000 pasos para 0.001 s)

**Resultado:**  
Vector `v(t)` numérico con memoria; comparación directa con la solución analítica sin memoria.

---

### Resultados numéricos y efectos observados

Comparando `v(t)` sin memoria (analítico) y con memoria (numérico) para `μ = 1·10⁻³`:

**Ejemplo numérico en `t = 0.001 s`:**

```text
v_sin_memoria(0.001) = 4.36000000 × 10⁻⁵ m/s
v_con_memoria(0.001) ≈ 4.35781601 × 10⁻⁵ m/s
```

- Diferencia absoluta: ≈ `2.18 × 10⁻⁸ m/s`  
- Diferencia relativa: ≈ `5 × 10⁻⁴` (≈ 0.05%)

---

La gráfica comparativa (se proporcionó) muestra que la memoria produce una ligera reducción de la velocidad en todo el intervalo:  
El término de memoria actúa como una **fuerza retardante adicional dependiente del historial de la velocidad**.  

Con los parámetros dados (`α` relativamente pequeño), el efecto es pequeño (fracción de 0.1% o menos en este caso), pero su dirección es clara:  
> **Mayor fricción efectiva → menor velocidad**

Con `α` mayor o `β` distinto, el efecto podría ser mucho más marcado.
