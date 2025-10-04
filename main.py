# Código usado para resolver los ítems 8, 9 y 10 del ejercicio.
# - Genera la tabla con t, v(t) y x(t) para μ = 1e-3 (paso 1e-4 s).
# - Compara τ y v∞ para μ = 1e-3 y μ = 0.1.
# - Resuelve numéricamente el modelo con memoria usando RK4 y lo compara con el modelo sin memoria.

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# Parámetros físicos
R = 1e-5                # m
rho_p = 1200.0          # kg/m^3
rho_f = 1000.0          # kg/m^3
g = 9.81                # m/s^2 (gravedad)
mu1 = 1e-3              # Pa·s (fluido 1: agua)
mu2 = 0.1               # Pa·s (fluido 2: aceite)

# Constantes memoria (ítem 10)
alpha = 1e-7            # kg/s^2
beta = 5.0              # s^-1

# Volumen y masa
V = 4.0/3.0 * math.pi * R**3
m = rho_p * V

# Funciones para tau y v_inf
def tau_from(mu, rho_p=rho_p, R=R):
    return (2.0/9.0) * rho_p * R**2 / mu

def v_inf_from(mu, rho_p=rho_p, rho_f=rho_f, R=R, g=g):
    return (2.0/9.0) * (rho_p - rho_f) * R**2 * g / mu

tau1 = tau_from(mu1)
v_inf1 = v_inf_from(mu1)

tau2 = tau_from(mu2)
v_inf2 = v_inf_from(mu2)

# Tiempo de muestreo pedido (0 a 0.001 en pasos de 0.0001)
t_sample = np.arange(0.0, 0.001 + 1e-12, 0.0001)

# Solución analítica (sin memoria)
v_analytic = v_inf1 * (1 - np.exp(-t_sample / tau1))
x_analytic = v_inf1 * (t_sample - tau1 * (1 - np.exp(-t_sample / tau1)))

# Crear tabla numérica (ítem 8)
df = pd.DataFrame({
    "t (s)": t_sample,
    "v(t) (m/s)": v_analytic,
    "x(t) (m)": x_analytic
})

# Mostrar tabla en consola
print("\nTabla: t, v(t), x(t) para μ=1e-3")
print(df.to_string(index=False))

# Gráfica v(t) y x(t) en el mismo plano (ítem 8)
plt.figure(figsize=(8,5))
plt.plot(t_sample, v_analytic, label='v(t) (m/s)')
plt.plot(t_sample, x_analytic, label='x(t) (m)')
plt.axhline(v_inf1, linestyle='--', label=f'v∞ = {v_inf1:.3e} m/s')
plt.axvline(tau1, linestyle=':', label=f'τ = {tau1:.3e} s')
plt.xlabel('t (s)')
plt.ylabel('v (m/s) / x (m)')
plt.title('v(t) y x(t) para μ = 1e-3 (0 ≤ t ≤ 0.001 s)')
plt.legend()
plt.grid(True)
plt.show()

# Comparación de parámetros entre μ=1e-3 y μ=0.1 (ítem 9)
comparison_df = pd.DataFrame({
    "μ (Pa·s)": [mu1, mu2],
    "τ (s)": [tau1, tau2],
    "v∞ (m/s)": [v_inf1, v_inf2]
})

print("\nComparación τ y v∞ para μ=1e-3 y μ=0.1")
print(comparison_df.to_string(index=False))

# --- Ítem 10: Modelo con memoria ---
# Sistema:
# dv/dt = ( (m - rho_f V)*g - 6πμ R v - α w ) / m
# dw/dt = v - β w

def integrate_memory(mu, alpha=alpha, beta=beta, dt_small=1e-6, t_max=0.001):
    n_steps = int(t_max / dt_small) + 1
    t_full = np.linspace(0, t_max, n_steps)
    v = np.zeros(n_steps)
    w = np.zeros(n_steps)
    v[0] = 0.0
    w[0] = 0.0
    Cgrav = (m - rho_f * V) * g
    k = 6.0 * math.pi * mu * R
    for i in range(n_steps - 1):
        ti = t_full[i]
        vi = v[i]
        wi = w[i]
        def rhs(vv, ww):
            dvdt = (Cgrav - k * vv - alpha * ww) / m
            dwdt = vv - beta * ww
            return dvdt, dwdt
        dv1, dw1 = rhs(vi, wi)
        dv2, dw2 = rhs(vi + 0.5*dt_small*dv1, wi + 0.5*dt_small*dw1)
        dv3, dw3 = rhs(vi + 0.5*dt_small*dv2, wi + 0.5*dt_small*dw2)
        dv4, dw4 = rhs(vi + dt_small*dv3, wi + dt_small*dw3)
        v[i+1] = vi + (dt_small/6.0)*(dv1 + 2*dv2 + 2*dv3 + dv4)
        w[i+1] = wi + (dt_small/6.0)*(dw1 + 2*dw2 + 2*dw3 + dw4)
    return t_full, v, w

# Integrar para μ = 1e-3 (agua)
t_full, v_mem_full, w_full = integrate_memory(mu1, dt_small=1e-6, t_max=0.001)

# Interpolar valores de v_mem en t_sample
v_mem_sample = np.interp(t_sample, t_full, v_mem_full)

# Crear tabla comparativa v sin memoria / con memoria
df_comp_mem = pd.DataFrame({
    "t (s)": t_sample,
    "v_no_memory (m/s)": v_analytic,
    "v_with_memory (m/s)": v_mem_sample
})

print("\nComparación v(t) sin memoria / con memoria (μ=1e-3)")
print(df_comp_mem.to_string(index=False))

# Gráfica comparación v(t) sin memoria vs con memoria
plt.figure(figsize=(8,5))
plt.plot(t_sample, v_analytic, label='v(t) sin memoria (analítico)')
plt.plot(t_sample, v_mem_sample, label='v(t) con memoria (numérico)')
plt.xlabel('t (s)')
plt.ylabel('v (m/s)')
plt.title('Comparación de velocidad: sin memoria vs con memoria (0 ≤ t ≤ 0.001 s)')
plt.legend()
plt.grid(True)
plt.show()

# Guardar resultados numéricos en variables para mostrar en el informe (resumen)
results = {
    "V": V,
    "m": m,
    "tau1": tau1,
    "v_inf1": v_inf1,
    "tau2": tau2,
    "v_inf2": v_inf2,
    "t_sample": t_sample,
    "v_analytic": v_analytic,
    "x_analytic": x_analytic,
    "v_mem_sample": v_mem_sample,
    "t_full": t_full,
    "v_mem_full": v_mem_full
}

# Mostrar resumen de resultados clave (opcional)
print("\nResumen de resultados clave:")
print(f"V = {V:.3e} m³")
print(f"m = {m:.3e} kg")
print(f"τ (mu=1e-3) = {tau1:.3e} s, v_inf = {v_inf1:.3e} m/s")
print(f"τ (mu=0.1)  = {tau2:.3e} s, v_inf = {v_inf2:.3e} m/s")
