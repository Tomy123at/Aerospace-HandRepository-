import math
import numpy as np
import matplotlib.pyplot as plt

# ---------------------
# Datos de entrada
# ---------------------
M = 0.82
rho = 0.000736627        # slug/ft^3 (35,000 ft)
a_sound = 968.0          # ft/s
AR, e = 10.0, 0.85
CD0_base = 0.0184
CD0_new = CD0_base + 0.0005

parametro_de_ajuste_motor = 0.23

# ---------------------
# Dinámica y parámetros
# ---------------------
V = M * a_sound
q = 0.5 * rho * V**2
K = 1.0 / (math.pi * AR * e)

# Fórmula T/W
def T_over_W(ws):
    return (CD0_new * q) / ws + (K / q) * ws

# ---------------------
# Valores de W/S
# ---------------------
WS = np.linspace(40, 150, 300)
TW_no_ajustado = T_over_W(WS)
TW_ajustado = TW_no_ajustado / parametro_de_ajuste_motor

CD = CD0_new + (0.43**2)/(26.7)
print(f"CD (nuevo):          {CD:.5f}")
# ---------------------
# Imprimir resultados en consola
# ---------------------
print("=== Parámetros calculados ===")
print(f"Velocidad (V):        {V:.3f} ft/s")
print(f"q (presión dinámica): {q:.5f} psf")
print(f"K (inducido):         {K:.6f}")
print(f"CD0 (nuevo):          {CD0_new:.5f}")
print(f"A = CD0*q:            {CD0_new * q:.6f}")
print(f"B = K/q:              {K/q:.6e}\n")

print("=== Resultados T/W ===")
for ws in [60, 80, 100, 120]:
    tw = T_over_W(ws)
    print(f"W/S = {ws:>3} psf ->  T/W no ajustado = {tw:.5f},   T/W ajustado = {tw/parametro_de_ajuste_motor:.5f}")

# ---------------------
# Graficar resultados
# ---------------------
plt.figure(figsize=(8, 6))
plt.plot(WS, TW_no_ajustado, label=r'$T/W$ no ajustado', linewidth=2)
plt.plot(WS, TW_ajustado, '--', label=rf'$T/W$ ajustado ÷ {parametro_de_ajuste_motor}', linewidth=2)

plt.title(r'$\mathbf{T/W \ \ vs \ \ W/S}$', fontsize=14, weight='bold')
plt.xlabel(r'$(W/S) \ [\mathrm{psf}]$', fontsize=12)
plt.ylabel(r'$(T/W)$', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
