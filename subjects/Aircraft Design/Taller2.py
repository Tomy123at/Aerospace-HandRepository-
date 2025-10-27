# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 08:50:50 2025

@author: jlope
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Esta vaina es pa ver los datos
def show_table(title: str, df: pd.DataFrame) -> None:
    print(f"\n{title}\n" + "-" * len(title))
    try:
        print(df.to_string(index=False))
    except Exception:
        print(df)

# ======================
# Datos y supuestos, me corrigen si algo ---------------------------------------------
# ======================
CONFIG = {
    # Curvas T/W vs W/S
    "CLmax_TO_list": [1.6, 2.0, 2.4],   # [-]

    # Aterrizaje (para columnas verticales de (W/S)_L a 5000 ft hot day)
    "CLmax_L_list": [1.8, 2.2, 2.6, 3.0],  # [-]

    # Velocidad de pérdida en aterrizaje VsL
    "Vs_kts": 99.3,               # [kt]
    "kts_to_ftps": 1.68781,       # [ft/s por kn]

    # Atmósfera a nivel del mar y 5000 ft hot day
    "rho_SL": 0.0023769,          # [slug/ft^3]
    "DELTA_5000": 0.8320,         # razón de presión δ
    "THETA_5000": 1.0694,         # razón de temperatura θ

    # Modelo T/W (al nivel del mar, std) usado para las curvas base
    "K": 0.009640,                # [-]
    "factor_sea_level": 1.17,     # [-]

    # Barrido de W/S para la gráfica
    "WS_max": 130.0,              # [psf]
    "WS_points": 400,             # [-]

    # Ajuste de (W/S) de aterrizaje (p.ej. W_L = 0.95 W_TO)
    "landing_weight_fraction": 0.95,  # [-]
}

# Imprimir todos los datos y supuestos
print("=== DATOS Y SUPUESTOS (editables) ===")
print(f"CLmax_TO_list [-]:          {CONFIG['CLmax_TO_list']}")
print(f"CLmax_L_list [-]:           {CONFIG['CLmax_L_list']}")
print(f"Vs [kt]:                    {CONFIG['Vs_kts']}")
print(f"kts->ft/s [-]:               {CONFIG['kts_to_ftps']}")
print(f"rho_SL [slug/ft^3]:         {CONFIG['rho_SL']}")
print(f"DELTA_5000 [-]:              {CONFIG['DELTA_5000']}")
print(f"THETA_5000 [-]:              {CONFIG['THETA_5000']}")
print(f"K [-]:                        {CONFIG['K']}")
print(f"factor_sea_level [-]:       {CONFIG['factor_sea_level']}")
print(f"WS_max [psf]:               {CONFIG['WS_max']}")
print(f"WS_points [-]:               {CONFIG['WS_points']}")
print(f"landing_weight_fraction [-]: {CONFIG['landing_weight_fraction']}\n")

# -----------------------------
# Derivados desde CONFIG
# -----------------------------
CLmax_TO_list = CONFIG["CLmax_TO_list"]
CLmax_L_list = CONFIG["CLmax_L_list"]
Vs = CONFIG["Vs_kts"] * CONFIG["kts_to_ftps"]  # [ft/s]
rho_SL = CONFIG["rho_SL"]
SIGMA_5000_HOT = CONFIG["DELTA_5000"] / CONFIG["THETA_5000"]
rho_5000_hot = SIGMA_5000_HOT * rho_SL
K = CONFIG["K"]
factor_sea_level = CONFIG["factor_sea_level"]
WS_max = CONFIG["WS_max"]
WS = np.linspace(0.0, WS_max, CONFIG["WS_points"])  # [psf]
landing_weight_fraction = CONFIG["landing_weight_fraction"]

# -------------------------------------------------
# 2. Función para calcular T/W al nivel del mar
# -------------------------------------------------
def TW_sea_level(ws, cl):
    """Calcula T/W al nivel del mar (ws en [lb/ft^2], cl adimensional)."""
    return (K * ws / cl) * factor_sea_level

# -------------------------------------------------
# 3. Cálculo de W/S a partir de VsL (5000 ft hot day)
#     Fórmula: (W/S)_L = 0.5 * rho * Vs^2 * CLmax  -> resultado en [lb/ft^2]
#     Con rho = σ * rho0, usando σ=δ/θ a 5000 ft y 95°F (según lámina).
# -------------------------------------------------
Vs2 = Vs ** 2                # [ft^2/s^2]
const_WS = 0.5 * rho_5000_hot * Vs2
WS_from_Vs = const_WS * np.array(CLmax_L_list)                # [lb/ft^2]

# Ajuste configurable del usuario (p. ej., W_L = frac * W_TO)
WS_adjusted = WS_from_Vs / landing_weight_fraction           # [lb/ft^2]

# Crear tabla de resultados
df = pd.DataFrame({
    "CLmax_L [-]": CLmax_L_list,
    "(W/S)_L a 5000 ft hot day [psf]": np.round(WS_from_Vs, 1),
    f"(W/S) ajustado /( {landing_weight_fraction}) [psf]": np.round(WS_adjusted, 1),
})

# Mostrar la tabla
show_table("W/S (5000 ft hot day) y ajuste", df)

# -------------------------------------------------
# 4. Gráfica final
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=140)

# ---- Curvas de T/W vs W/S para distintos CLmax_TO
for cl in CLmax_TO_list:
    TW = TW_sea_level(WS, cl)
    ax.plot(WS, TW, label=fr"$C_{{L_{{\max TO}}}}={cl}$")
    
    # Rayitas inclinadas sobre el 20% final de cada curva
    x_start = WS_max * 0.80
    x_ticks = np.arange(x_start, WS_max + 1e-9, 6.0)
    tick_len_x = 3.5
    tick_len_y = 0.06
    vertical_offset = 0.03
    for x0 in x_ticks:
        y0 = TW_sea_level(x0, cl) - vertical_offset
        ax.plot([x0 - tick_len_x / 2, x0 + tick_len_x / 2],
                [y0 - tick_len_y / 2, y0 + tick_len_y / 2])

# ---- Líneas verticales para W/S calculados (5000 ft hot day)
for ws_val, CL in zip(WS_adjusted, CLmax_L_list):
    # Línea vertical principal
    ax.plot([ws_val, ws_val],
            [0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 0.85],
            linewidth=1.6)
    
    # Etiquetas encima de las rayitas
    ax.text(ws_val, 0.78, f"{CL}", rotation=0, ha="center", va="bottom")
    
    # Rayitas pequeñas a la derecha de cada línea vertical
    y_start = 0.70
    y_end = 0.84
    y_ticks = np.arange(y_start, y_end + 1e-9, 0.04)
    tick_dx = 4.0
    tick_dy = 0.06
    for y0 in y_ticks:
        ax.plot([ws_val + 0.0, ws_val + tick_dx],
                [y0 - tick_dy / 2, y0 + tick_dy / 2])

# -------------------------------------------------
# 5. Estética de la gráfica
# -------------------------------------------------
ax.set_xlabel(r"TAKE-OFF WING LOADING $(W/S)_{\mathrm{TO}}\ \mathrm{[psf]}$")
ax.set_ylabel(r"TAKE-OFF THRUST-TO-WEIGHT RATIO $(T/W)_{\mathrm{TO}}$")
ax.set_xlim(0, WS_max)
ax.set_ylim(0, 0.95)
ax.grid(True, which="both", linewidth=0.6, alpha=0.5)
ax.legend(loc="upper left", title="Sea level, std")

plt.show()
