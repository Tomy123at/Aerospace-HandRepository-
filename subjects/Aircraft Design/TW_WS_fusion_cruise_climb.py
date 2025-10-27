# -*- coding: utf-8 -*-
"""
T/W vs W/S - Fusión de criterios de CRUCERO (48,000 ft, M=0.87) y ASCENSO DIRECTO

- Usa los mismos datos y correlaciones de:
  * Taller_2_criterio_crucero_NUESTROSDATOSEJERCICIO.py (curva de crucero)
  * DirectCLimb.py (requerimiento de ascenso)

- Todos los datos dados y supuestos están en el bloque CONFIG; modifícalos ahí si se requiere.
"""
import math
import numpy as np
import matplotlib.pyplot as plt

# ======================
# CONFIG: Datos dados y supuestos (modificables)
# ======================
CONFIG = {
    # Requerimientos (de la lámina / datos dados)
    "range_nmi": 3000.0,               # [nmi] (no se usa en estas curvas)
    "cruise_alt_ft": 48000.0,          # [ft]
    "cruise_Mach": 0.87,               # [-]
    "pressurization_cabin_ft": 5000.0, # [ft] (no usado aquí)
    "num_engines": 2,                  # turbofans (informativo)

    # Peso y geometría
    "WTO_lb": 35300.0,      # [lb]
    "S_ref_ft2": 511.0,     # [ft^2]
    "AR": 10.0,             # [-]
    "e": 0.85,              # [-]

    # Atmósfera a 48,000 ft (datos usados en los códigos)
    "rho_slug_ft3": 0.000398389,   # [slug/ft^3]
    "a_sound_ft_s": 968.076,       # [ft/s]

    # Correlaciones (Business Jets)
    # log10(Swet) = c + d*log10(WTO)
    "c_swet": 0.2263,
    "d_swet": 0.6977,
    # log10(f) = a_log + b_log*log10(Swet)
    "a_log_f": -2.5229,
    "b_log_f": 1.0,

    # Incremento de arrastre parasitario (counts)
    "delta_CD0_counts": 18,      # 18 counts => 0.0018

    # Ajuste motor (para graficar una segunda curva escalada)
    "engine_adjust": 0.23,       # dividir T/W por este factor para una curva "ajustada"

    # Ascenso directo - razón de ascenso deseada
    # Puedes especificar la unidad en 'RC_units': 'ft/s' o 'ft/min'
    "RC_value": 500.0,           # valor numérico
    "RC_units": "ft/s",         # 'ft/s' o 'ft/min'

    # Rango W/S para trazar
    "WS_min": 40.0,
    "WS_max": 200.0,
    "WS_points": 400,
}

# ======================
# Cálculos auxiliares
# ======================
WTO = CONFIG["WTO_lb"]
S = CONFIG["S_ref_ft2"]
AR = CONFIG["AR"]
e = CONFIG["e"]
rho = CONFIG["rho_slug_ft3"]
a_sound = CONFIG["a_sound_ft_s"]
M = CONFIG["cruise_Mach"]

# Swet y f (correlaciones en base 10)
log10_Swet = CONFIG["c_swet"] + CONFIG["d_swet"] * math.log10(WTO)
Swet = 10 ** log10_Swet
log10_f = CONFIG["a_log_f"] + CONFIG["b_log_f"] * math.log10(Swet)
f = 10 ** log10_f

# CD0 y delta por counts
CD0_base = f / S
CD0_new = CD0_base + CONFIG["delta_CD0_counts"] * 1e-4

# Dinámica y factor inducido
V = M * a_sound
q = 0.5 * rho * V**2                 # [psf]
K = 1.0 / (math.pi * AR * e)

# Conversión RC
RC_val = CONFIG["RC_value"]
if CONFIG["RC_units"].lower() in ("ft/min", "ftm", "fpm"):
    RC = RC_val / 60.0  # a [ft/s]
else:
    RC = RC_val         # ya en [ft/s]

# Coeficientes de parábola A/x + B*x (nivelado)
A = CD0_new * q
B = K / q

# Funciones T/W
# Nivelado (crucero): T/W = A/ws + B*ws
# Ascenso directo:    T/W = (RC/V) + A/ws + B*ws

def TW_cruise(ws):
    ws = np.asarray(ws, dtype=float)
    return (A / ws) + (B * ws)

def TW_climb(ws):
    return (RC / V) + TW_cruise(ws)

# Rango de W/S
WS = np.linspace(CONFIG["WS_min"], CONFIG["WS_max"], CONFIG["WS_points"])
TW_cr = TW_cruise(WS)
TW_cl = TW_climb(WS)

# Variante ajustada por motor (si se desea)
adj = CONFIG["engine_adjust"]
TW_cr_adj = TW_cr / adj
TW_cl_adj = TW_cl / adj

# Punto de mínimo teórico para la parábola (mismo para crucero y ascenso)
ws_opt = math.sqrt(A / B)
tw_min_cr = 2.0 * math.sqrt(A * B)   # crucero
# En ascenso es el mismo + RC/V

tw_min_cl = (RC / V) + tw_min_cr

# ======================
# Salida de parámetros
# ======================
print("=== DATOS DADOS Y SUPUESTOS ===")
print(f"WTO [lb]:                {WTO:.1f}")
print(f"S_ref [ft^2]:            {S:.1f}")
print(f"AR [-]:                  {AR:.2f}")
print(f"e [-]:                   {e:.2f}")
print(f"Altitud de crucero [ft]: {CONFIG['cruise_alt_ft']:.0f}")
print(f"Mach crucero [-]:        {M:.2f}")
print(f"rho [slug/ft^3]:         {rho:.9f}")
print(f"a (sonido) [ft/s]:       {a_sound:.3f}")
print(f"RC [{CONFIG['RC_units']}]:            {CONFIG['RC_value']:.3f}")
print(f"Ajuste motor [-]:        {adj:.3f}")
print(f"delta_CD0 (counts):      {CONFIG['delta_CD0_counts']} -> {CONFIG['delta_CD0_counts']*1e-4:.4f}\n")

print("=== Intermedios aerodinámicos ===")
print(f"Swet [ft^2]:             {Swet:.4f}")
print(f"f [-]:                   {f:.6f}")
print(f"CD0_base [-]:            {CD0_base:.6f}")
print(f"CD0_new [-]:             {CD0_new:.6f}")
print(f"V [ft/s]:                {V:.3f}")
print(f"q [psf]:                 {q:.6f}")
print(f"K [-]:                   {K:.6f}")
print(f"A = CD0_new*q:           {A:.6f}")
print(f"B = K/q:                 {B:.6e}")
print(f"ws_opt [psf]:            {ws_opt:.3f}")
print(f"T/W_min (crucero):       {tw_min_cr:.5f}")
print(f"T/W_min (ascenso):       {tw_min_cl:.5f}\n")

# ======================
# Gráfico fusionado
# ======================
plt.figure(figsize=(8.6, 6.0))
plt.plot(WS, TW_cr, label=r"Cruise: $T/W = A/(W/S) + B\,(W/S)$", linewidth=2)
plt.plot(WS, TW_cl, label=rf"Direct climb: $T/W = (RC/V) + A/(W/S) + B\,(W/S)$  (RC={CONFIG['RC_value']} {CONFIG['RC_units']})", linewidth=2)
# Curvas ajustadas (opcional)
plt.plot(WS, TW_cr_adj, "--", label=rf"Cruise adjusted ÷ {adj}", linewidth=1.8)
plt.plot(WS, TW_cl_adj, "--", label=rf"Climb adjusted ÷ {adj}", linewidth=1.8)

# Marcar mínimos
plt.scatter([ws_opt], [tw_min_cr], s=35, color="C0")
plt.annotate(fr"min cruise: W/S={ws_opt:.1f}, T/W={tw_min_cr:.3f}",
             xy=(ws_opt, tw_min_cr), xytext=(ws_opt+10, tw_min_cr+0.01),
             arrowprops=dict(arrowstyle='->', lw=1), color="C0")
plt.scatter([ws_opt], [tw_min_cl], s=35, color="C1")
plt.annotate(fr"min climb: W/S={ws_opt:.1f}, T/W={tw_min_cl:.3f}",
             xy=(ws_opt, tw_min_cl), xytext=(ws_opt+10, tw_min_cl+0.02),
             arrowprops=dict(arrowstyle='->', lw=1), color="C1")

plt.title("Fusion: T/W vs W/S (Cruise & Direct Climb)")
plt.xlabel(r"$(W/S)\ \mathrm{[psf]}")
plt.ylabel(r"$T/W$")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
