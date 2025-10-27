# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:41:22 2025

@author: jlope
"""

import math

# -----------------------------
# Entradas (tuyas del caso actual)
# -----------------------------
# Condición de vuelo
M       = 0.87
rho     = 0.000398389      # slug/ft^3  (≈ 48,000 ft)
a_sound = 968.076          # ft/s
RC      = 500.0            # ft/s  (como indicaste)

# Geometría
S       = 511              # ft^2  (área alar)
AR, e   = 10.0, 0.85

# Peso
W       = 35300.0          # lb

# Para Swet y f (Business Jets)
WTO     = 35300.0          # lb (usamos el mismo valor como en tus pasos previos)
c, d    = 0.2263, 0.6977
a_log, b_log = -2.5229, 1.0

# Delta de drag en "counts"
delta_counts = 18          # 18 counts
delta_CD0    = delta_counts * 1e-4  # 0.0018

# -----------------------------
# 1) Swet -> f -> CD0
# -----------------------------
log10_Swet = c + d * math.log10(WTO)
Swet = 10 ** log10_Swet

log10_f = a_log + b_log * math.log10(Swet)
f = 10 ** log10_f

CD0_base = f / S           # ahora S = 1000 ft^2
CD0 = CD0_base + delta_CD0

# -----------------------------
# 2) q, CL
# -----------------------------
V = M * a_sound
q = 0.5 * rho * V**2       # psf

CL = W / (q * S)

# -----------------------------
# 3) Inducido y CD total
# -----------------------------
K = 1.0 / (math.pi * AR * e)
CD = CD0 + K * CL**2

# -----------------------------
# 4) L/D y T/W desde R/C
#     R/C = V * (T/W - 1/(L/D))  ->  T/W = (R/C)/V + 1/(L/D)
# -----------------------------
L_over_D = CL / CD
T_over_W = (RC / V) + 1.0 / L_over_D

# -----------------------------
# 5) Mostrar resultados
# -----------------------------
print("=== Intermedios de polar ===")
print(f"Swet [ft^2]     : {Swet:.4f}")
print(f"f [-]           : {f:.6f}")
print(f"CD0_base [-]    : {CD0_base:.6f}")
print(f"ΔCD0 (counts)   : {delta_counts} -> {delta_CD0:.4f}")
print(f"CD0 (final) [-] : {CD0:.6f}")

print("\n=== Condición de vuelo ===")
print(f"V [ft/s]        : {V:.3f}")
print(f"q [psf]         : {q:.5f}")
print(f"CL [-]          : {CL:.5f}")
print(f"K [-]           : {K:.6f}")
print(f"CD [-]          : {CD:.6f}")
print(f"L/D [-]         : {L_over_D:.3f}")

print("\n=== Requerimiento de empuje ===")
print(f"R/C [ft/s]      : {RC:.3f}")
print(f"T/W [-]         : {T_over_W:.5f}")
