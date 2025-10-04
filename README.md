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
pip install numpy pandas matplotlib