# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:15:46 2025

@author: jlope
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# ---------------------
# Datos base del problema
# ---------------------
# Para Swet y f (Business Jets)
WTO   = 35300.0           # lb
c, d  = 0.2263, 0.6977    # log10(Swet) = c + d*log10(WTO)
a_log, b_log = -2.5229, 1.0  # log10(f) = a_log + b_log*log10(Swet)

# Geometría
S_ref = 511            # ft^2 (área alar pedida) ------------------------------
# Aerodinámica (polar inducida)
AR, e = 10.0, 0.85 # --------------------------------------------------------------

# Condición de vuelo (48,000 ft)
M       = 0.87
rho     = 0.000398389     # slug/ft^3
a_sound = 968.076         # ft/s

# Delta de drag (counts)
delta_CD0_counts = 18
delta_CD0 = delta_CD0_counts * 1e-4  # 18 counts = 0.0018

# (Opcional) parámetro de ajuste "motor" para comparar una segunda curva
parametro_de_ajuste_motor = 0.23  # cámbialo o ponlo a 1.0 si no lo quieres usar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ---------------------
# 1) Swet a partir de WTO
# ---------------------
log10_Swet = c + d * math.log10(WTO)
Swet = 10 ** log10_Swet

# ---------------------
# 2) f a partir de Swet
# ---------------------
log10_f = a_log + b_log * math.log10(Swet)
f = 10 ** log10_f

# ---------------------
# 3) C_D0 base y ajustado por counts
# ---------------------
CD0_base = f / S_ref
CD0_new  = CD0_base + delta_CD0

# ---------------------
# 4) Dinámica (q) y factor inducido (K)
# ---------------------
V = M * a_sound
q = 0.5 * rho * V**2
K = 1.0 / (math.pi * AR * e)

# ---------------------
# 5) Función T/W en función de W/S
#     T/W = (CD0_new*q)/(W/S) + (K/q)*(W/S)
# ---------------------
def T_over_W(ws):
    ws = np.asarray(ws, dtype=float)
    return (CD0_new * q) / ws + (K / q) * ws

# Rango de W/S para trazar
WS = np.linspace(40, 200, 400)
TW_no_ajustado = T_over_W(WS)
TW_ajustado    = TW_no_ajustado / parametro_de_ajuste_motor


CL = WTO/(q*S_ref)
CD = CD0_new + K*CL**2


# ---------------------
# 6) Impresión en consola (parámetros y algunos puntos)
# ---------------------
print("=== Parámetros intermedios ===")
print(f"Swet [ft^2]:        {Swet:.4f}")
print(f"f [-]:              {f:.6f}")
print(f"CD0_base [-]:       {CD0_base:.6f}")
print(f"Delta CD0 (counts): {delta_CD0_counts} -> {delta_CD0:.4f}")
print(f"CD0_new [-]:        {CD0_new:.6f}")
print(f"V [ft/s]:           {V:.3f}")
print(f"q [psf]:            {q:.5f}")
print(f"K [-]:              {K:.6f}")
print(f"A = CD0_new*q:      {CD0_new*q:.6f}")
print(f"B = K/q:            {K/q:.6e}")
print(f"CL:                 {CL:.3f}")
print(f"CD:                 {CD:.3f}\n")

print("=== T/W para W/S típicos ===")
for ws in [60, 80, 100, 120, 140, 160, 180]:
    tw = T_over_W(ws)
    print(f"W/S = {ws:>3} psf ->  T/W = {tw:.5f}   |   T/W ajustado (÷{parametro_de_ajuste_motor}) = {tw/parametro_de_ajuste_motor:.5f}")

# (opcional) mínimo T/W teórico y W/S* asociado (parábola A/x + Bx)
A = CD0_new*q
B = K/q
ws_opt = math.sqrt(A/B)
tw_min = 2.0*math.sqrt(A*B)
print(f"\nMínimo teórico T/W en W/S* = {ws_opt:.3f} psf  ->  T/W_min = {tw_min:.5f}")

# ---------------------
# 7) Gráfico
# ---------------------
plt.figure(figsize=(8, 6))
plt.plot(WS, TW_no_ajustado, label=r'$T/W$ no ajustado', linewidth=2)
plt.plot(WS, TW_ajustado, '--', label=rf'$T/W$ ajustado ÷ {parametro_de_ajuste_motor}', linewidth=2)

# Marcar el mínimo
plt.scatter([ws_opt], [tw_min], s=40)
plt.annotate(fr"mín: W/S={ws_opt:.1f}, T/W={tw_min:.3f}",
             xy=(ws_opt, tw_min), xytext=(ws_opt+10, tw_min+0.01),
             arrowprops=dict(arrowstyle='->', lw=1))

plt.title(r'$\mathbf{T/W \ \ vs \ \ W/S}$', fontsize=14, weight='bold')
plt.xlabel(r'$(W/S)\ \mathrm{[psf]}$', fontsize=12)
plt.ylabel(r'$(T/W)$', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
