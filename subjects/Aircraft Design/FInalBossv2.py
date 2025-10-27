# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 08:50:50 2025

@author: jlope
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Utilidad para poner rayitas diagonales ---
def draw_slash(ax, x0, y0, dx=3.5, dy=0.06, color=None):
    ax.plot([x0 - dx/2, x0 + dx/2], [y0 - dy/2, y0 + dy/2], color=color, zorder=6)

# Esta vaina es pa ver una tabla, no le mueva si no sabe (yo tampoco se)
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
    # Curvas T/W vs W/S (Taller 2 - Sea level std)
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

    # Modelo T/W (al nivel del mar, std) usado para las curvas base (Taller 2)
    "K": 0.009640,                # [-]
    "factor_sea_level": 1.17,     # [-]

    # Barrido de W/S para la gráfica
    "WS_max": 120.0,              # [psf]
    "WS_points": 120,             # [-]

    # Puntos para la TABLA de sizing (W/S) y CL para la columna de Take-Off
    "table_ws_points": [60, 80, 100, 120],  # [psf]
    "CLmax_TO_table": 2.0,                   # CL usado en (T/W)_TO de la tabla

    # Ajuste de (W/S) de aterrizaje (p.ej. W_L = 0.95 W_TO)
    "landing_weight_fraction": 0.95,  # [-]

    # ----------------------
    # NUESTROSDATOSEJERCICIO (Cruise @ 48,000 ft)
    # ----------------------
    "WTO_lb": 35300.0,            # [lb]
    "S_ref_ft2": 511.0,           # [ft^2]
    "c_swet": 0.2263,
    "d_swet": 0.6977,
    "a_log_f": -2.5229,
    "b_log_f": 1.0,
    # Aerodinámica inducida
    "AR": 12.0,
    "e": 0.85,
    # Condición de vuelo crucero
    "M_cruise": 0.87,
    "rho_cruise": 0.000398389,    # [slug/ft^3] (48,000 ft)
    "a_sound": 968.076,           # [ft/s]
    # Incremento de CD0 en counts
    "delta_CD0_counts": 18,       # 18 counts = 0.0018
    # Factor de ajuste motor (opcional). Pon 1.0 si no deseas esta variante
    "engine_adjust": 0.2,
    # Peso y performance de DirectClimb
    "W_lb": 35300.0,              # [lb] peso en condición de crucero/ascenso
    "RC_ft_s": 500.0 / 60,        # [ft/s] razón de ascenso deseada
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
print(f"K (T/O) [-]:                 {CONFIG['K']}")
print(f"factor_sea_level [-]:       {CONFIG['factor_sea_level']}")
print(f"WS_max [psf]:               {CONFIG['WS_max']}")
print(f"WS_points [-]:               {CONFIG['WS_points']}")
print(f"Tabla (W/S) puntos [psf]:   {CONFIG['table_ws_points']}")
print(f"CLmax_TO para tabla [-]:    {CONFIG['CLmax_TO_table']}")
print(f"landing_weight_fraction [-]: {CONFIG['landing_weight_fraction']}")
# NUESTROSDATOSEJERCICIO + DirectClimb
print(f"WTO [lb]:                   {CONFIG['WTO_lb']}")
print(f"W [lb]:                     {CONFIG['W_lb']}")
print(f"S_ref [ft^2]:               {CONFIG['S_ref_ft2']}")
print(f"AR [-]:                      {CONFIG['AR']}")
print(f"e [-]:                       {CONFIG['e']}")
print(f"M_cruise [-]:                {CONFIG['M_cruise']}")
print(f"rho_cruise [slug/ft^3]:     {CONFIG['rho_cruise']}")
print(f"a_sound [ft/s]:             {CONFIG['a_sound']}")
print(f"delta_CD0_counts [-]:       {CONFIG['delta_CD0_counts']}")
print(f"engine_adjust [-]:          {CONFIG['engine_adjust']}")
print(f"RC [ft/s]:                  {CONFIG['RC_ft_s']}\n")

# -----------------------------
# Derivados desde CONFIG
# -----------------------------
CLmax_TO_list = CONFIG["CLmax_TO_list"]
CLmax_L_list = CONFIG["CLmax_L_list"]
Vs = CONFIG["Vs_kts"] * CONFIG["kts_to_ftps"]  # [ft/s]
rho_SL = CONFIG["rho_SL"]
SIGMA_5000_HOT = CONFIG["DELTA_5000"] / CONFIG["THETA_5000"]
rho_5000_hot = SIGMA_5000_HOT * rho_SL
K_to = CONFIG["K"]               # K del modelo de T/W de despegue (NO confundir con K_ind)
factor_sea_level = CONFIG["factor_sea_level"]
WS_max = CONFIG["WS_max"]
WS = np.linspace(0.0, WS_max, CONFIG["WS_points"])  # [psf]
landing_weight_fraction = CONFIG["landing_weight_fraction"]

# ---- Derivados NUESTROSDATOSEJERCICIO (Cruise + DirectClimb)
WTO = CONFIG["WTO_lb"]
W = CONFIG["W_lb"]
S_ref = CONFIG["S_ref_ft2"]
AR = CONFIG["AR"]
e = CONFIG["e"]
M = CONFIG["M_cruise"]
rho = CONFIG["rho_cruise"]
a_sound = CONFIG["a_sound"]
RC = CONFIG["RC_ft_s"]
delta_CD0 = CONFIG["delta_CD0_counts"] * 1e-4

# Swet y f
log10_Swet = CONFIG["c_swet"] + CONFIG["d_swet"] * math.log10(WTO)
Swet = 10 ** log10_Swet
log10_f = CONFIG["a_log_f"] + CONFIG["b_log_f"] * math.log10(Swet)
f = 10 ** log10_f

# CD0 y aerodinámica (crucero)
CD0_base = f / S_ref
CD0_new = CD0_base + delta_CD0
V = M * a_sound
q = 0.5 * rho * V**2
K_ind = 1.0 / (math.pi * AR * e)   # Factor inducido (NO confundir con K_to)
A_cr = CD0_new * q
B_cr = K_ind / q

# Curva de crucero (parábola A/x + Bx)
def TW_cruise(ws):
    ws = np.asarray(ws, dtype=float)
    return (A_cr / ws) + (B_cr * ws)

TW_cr = TW_cruise(WS)
engine_adjust = CONFIG["engine_adjust"]
TW_cr_adj = TW_cr / engine_adjust if engine_adjust and engine_adjust != 0 else None

# DirectClimb (línea horizontal): T/W = (RC/V) + 1/(L/D)
CL_dc = W / (q * S_ref)
CD_dc = CD0_new + K_ind * CL_dc**2
L_over_D_dc = CL_dc / CD_dc
TW_direct = ((RC / V) + 1.0 / L_over_D_dc) / engine_adjust

print("=== Intermedios (Cruise 48kft + DirectClimb) ===")
print(f"Swet [ft^2]:               {Swet:.4f}")
print(f"f [-]:                     {f:.6f}")
print(f"CD0_base [-]:              {CD0_base:.6f}")
print(f"CD0_new [-]:               {CD0_new:.6f}")
print(f"V [ft/s]:                  {V:.3f}")
print(f"q [psf]:                   {q:.5f}")
print(f"K_ind [-]:                 {K_ind:.6f}")
print(f"CL (direct climb):         {CL_dc:.5f}")
print(f"CD (direct climb):         {CD_dc:.5f}")
print(f"L/D (direct climb):        {L_over_D_dc:.3f}")
print(f"T/W (direct climb):        {TW_direct:.5f}\n")

# -------------------------------------------------
# 2. Función para calcular T/W al nivel del mar (Taller 2)
# -------------------------------------------------
def TW_sea_level(ws, cl):
    """Calcula T/W al nivel del mar (ws en [lb/ft^2], cl adimensional) usando K_to."""
    return (K_to * ws / cl) * factor_sea_level

# -------------------------------------------------
# 1.b TABLA: Cruise Speed Sizing (según nuestros modelos)
#     Columnas: (W/S)_TO [psf], (T/W)_cruise (ajustado si aplica), (T/W)_TO (CL elegido)
# -------------------------------------------------
ws_tab = np.array(CONFIG["table_ws_points"], dtype=float)
cl_tab = float(CONFIG["CLmax_TO_table"])

# T/W en crucero para los puntos de la tabla, TOMADOS DE LA CURVA PUNTUADA ROJA (interpolación)
# Así garantizamos que los números de la tabla coinciden con lo dibujado.
if TW_cr_adj is not None:
    tw_cr_tbl = np.interp(ws_tab, WS, TW_cr_adj)
else:
    # Si no hay ajuste de motor, usa la curva cruda dibujada (TW_cr)
    tw_cr_tbl = np.interp(ws_tab, WS, TW_cr)

# T/W de take-off (modelo al nivel del mar) usando CL especificado para la tabla
tw_to_tbl = TW_sea_level(ws_tab, cl_tab)

df_tab = pd.DataFrame({
    "(W/S)_TO [psf]": ws_tab.astype(int),
    "(T/W)_cruise (dashed)": np.round(tw_cr_tbl, 3),
    f"(T/W)_TO (CL={cl_tab:g})": np.round(tw_to_tbl, 3),
})
show_table("Cruise Speed Sizing — valores tomados de la curva roja punteada", df_tab)

# -------------------------------------------------
# 3. Cálculo de W/S a partir de VsL (5000 ft hot day)
# -------------------------------------------------
Vs2 = Vs ** 2
const_WS = 0.5 * rho_5000_hot * Vs2
WS_from_Vs = const_WS * np.array(CLmax_L_list)                # [lb/ft^2]
WS_adjusted = WS_from_Vs / landing_weight_fraction           # [lb/ft^2]

# Tabla
df = pd.DataFrame({
    "CLmax_L [-]": CLmax_L_list,
    "(W/S)_L a 5000 ft hot day [psf]": np.round(WS_from_Vs, 1),
    f"(W/S) ajustado /( {landing_weight_fraction}) [psf]": np.round(WS_adjusted, 1),
})
show_table("W/S (5000 ft hot day) y ajuste", df)

# -------------------------------------------------
# 4. Gráfica final
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=140)

# ---- Curvas de T/W vs W/S para distintos CLmax_TO (Taller 2, sea level)
for cl in CLmax_TO_list:
    TW = TW_sea_level(WS, cl)
    ax.plot(WS, TW, label=fr"$C_{{L_{{\max TO}}}}={cl}$")
    # Rayitas inclinadas sobre el 20% final de cada curva
    x_start = WS_max * 0.80
    x_ticks = np.arange(x_start, WS_max + 1e-9, 6.0)
    for x0 in x_ticks:
        y0 = TW_sea_level(x0, cl) - 0.03
        draw_slash(ax, x0, y0)

# ---- Añadir SOLO la curva de Cruise AJUSTADA (48kft) con rayitas al inicio y más abajo
if TW_cr_adj is not None:
    ax.plot(WS, TW_cr_adj, "--", color="C3", linewidth=1.8, label=rf"Cruise adjusted ÷ {engine_adjust}")
    x_start = WS_max * 0.05
    x_end = WS_max * 0.25
    x_ticks = np.arange(x_start, x_end, 6.0)
    for x0 in x_ticks:
        y0 = np.interp(x0, WS, TW_cr_adj) - 0.075
        draw_slash(ax, x0, y0, color="C3")

# ---- Añadir DirectClimb: línea horizontal T/W = const  (rayitas a la izquierda y más abajo)
ax.axhline(
    TW_direct,
    color="C4",
    linestyle="-",
    linewidth=2,
    alpha=0.95,
    zorder=5,
    label=fr"Direct Climb: $T/W={TW_direct:.3f}$ (RC={RC:.0f} ft/s)"
)
x_ticks = np.arange(WS_max * 0.05, WS_max * 0.25, 6.0)
for x0 in x_ticks:
    draw_slash(ax, x0, TW_direct - 0.03, color="C4")

# ---- Líneas verticales para W/S calculados (5000 ft hot day)
for ws_val, CL in zip(WS_adjusted, CLmax_L_list):
    ax.plot([ws_val, ws_val],
            [0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 0.85],
            linewidth=1.6)
    ax.text(ws_val, 0.78, f"{CL}", rotation=0, ha="center", va="bottom")
    y_start = 0.70
    y_end = 0.84
    y_ticks = np.arange(y_start, y_end + 1e-9, 0.04)
    tick_dx = 4.0
    tick_dy = 0.06
    for y0 in y_ticks:
        ax.plot([ws_val + 0.0, ws_val + tick_dx],
                [y0 - tick_dy / 2, y0 + tick_dy / 2])

# ---- Línea horizontal extra: FAR 25.121 (OEI) – Balked landing (approach), 1.5·Vs_A
#     (T/W)_L = 2*(1/(L/D) + 0.021)  → TO eq.: *0.95 / 0.80
AR_app = 10.0
e_app  = 0.5*(0.825 + 0.775)        # ≈0.800
CD0_clean = 0.014722
dCD0_TO   = 0.010
dCD0_LDG  = 0.055
dCD0_gear = 0.015
CD0_app = CD0_clean + 0.5*(dCD0_TO + dCD0_LDG) + dCD0_gear
CLmax_A = 2.7
k_app  = 1.0/(math.pi*AR_app*e_app)
CL_A   = CLmax_A/(1.5**2)
CD_A   = CD0_app + k_app*(CL_A**2)
LD_A   = CL_A/CD_A
TW_balked_L  = 2.0*(1.0/LD_A + 0.021)
TW_balked_TO = TW_balked_L * landing_weight_fraction / 0.80

ax.axhline(
    TW_balked_TO,
    color="teal",
    linestyle="-",
    linewidth=2,
    alpha=0.95,
    zorder=6,
    label=fr"Balked landing OEI → TO eq.: $T/W={TW_balked_TO:.3f}$"
)
# Rayitas diagonales SOLO a la izquierda y más abajo
x_ticks = np.arange(WS_max * 0.05, WS_max * 0.25, 6.0)
for x0 in x_ticks:
    draw_slash(ax, x0, TW_balked_TO - 0.03, color="teal")

# -------------------------------------------------
# 5. Estética de la gráfica
# -------------------------------------------------
ax.set_xlabel(r"TAKE-OFF WING LOADING $(W/S)_{\mathrm{TO}}\ \mathrm{[psf]}$")
ax.set_ylabel(r"TAKE-OFF THRUST-TO-WEIGHT RATIO $(T/W)_{\mathrm{TO}}$")
ax.set_xlim(0, WS_max)
ax.set_ylim(0, 0.95)
ax.grid(True, which="both", linewidth=0.6, alpha=0.5)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.18),   # debajo del eje
    ncol=3,                        # varias columnas = más compacta
    frameon=True,
    borderaxespad=0.0,
    title="Sea level (T/O) + Cruise (48kft) + Direct Climb",
    prop={"size": 8},
    title_fontsize=9
)
fig.subplots_adjust(bottom=0.28)   # espacio para la leyenda
plt.show()

# -------------------------------------------------
# Segunda gráfica: textos más bajos (excepto Take-off distance)
# + puntos de aeronaves con colores y leyenda inferior
# -------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# Helper para etiquetas en curvas
def label_on_curve(ax, xs, ys, x_pref, text, offset_pts=(8, 8),
                   color="black", fontsize=9, clip=True, z=10):
    xs = np.asarray(xs); ys = np.asarray(ys)
    x0 = float(np.clip(x_pref, xs.min()+1e-6, xs.max()-1e-6))
    y0 = float(np.interp(x0, xs, ys))
    dydx = np.gradient(ys, xs)
    slope = float(np.interp(x0, xs, dydx))
    angle = np.degrees(np.arctan(slope))
    ax.annotate(
        text, xy=(x0, y0), xycoords="data",
        xytext=offset_pts, textcoords="offset points",
        color=color, fontsize=fontsize, rotation=angle,
        ha="left", va="bottom",
        bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.6),
        zorder=z, clip_on=clip
    )

fig2, ax2 = plt.subplots(figsize=(7.5, 5.2), dpi=140)

# === 1) Cruise speed ===
if TW_cr_adj is not None:
    ax2.plot(WS, TW_cr_adj, color="red", linewidth=2.8)
    for x0 in np.arange(WS_max*0.06, WS_max*0.26, 6.0):
        y0 = np.interp(x0, WS, TW_cr_adj) - 0.035
        draw_slash(ax2, x0, y0, color="red")
    label_on_curve(ax2, WS, TW_cr_adj, x_pref=WS_max*0.58,
                   text="Cruise speed", offset_pts=(10, -26))

# === 2) Take-off distance ===
CLmax_TO_max = max(CLmax_TO_list)
TW_takeoff = TW_sea_level(WS, CLmax_TO_max)
ax2.plot(WS, TW_takeoff, color="red", linewidth=2.8)
for x0 in np.arange(WS_max*0.80, WS_max+1e-9, 6.0):
    y0 = TW_sea_level(x0, CLmax_TO_max) - 0.035
    draw_slash(ax2, x0, y0, color="red")
label_on_curve(ax2, WS, TW_takeoff, x_pref=WS_max*0.78,
               text="Take-off distance", offset_pts=(-8, 12))

# === 3) Landing distance ===
CLmax_L_max = max(CLmax_L_list)
idx_Lmax = CLmax_L_list.index(CLmax_L_max)
ws_landing = WS_adjusted[idx_Lmax]
ax2.axvline(ws_landing, color="red", linewidth=2.8)
y_start, y_end = 0.06, 0.78
for y0 in np.arange(y_start, y_end + 1e-9, 0.06):
    ax2.plot([ws_landing, ws_landing + 4.0],
             [y0 - 0.06/2 - 0.035, y0 + 0.06/2 - 0.035],
             color="red", zorder=6)
ax2.annotate("Landing distance",
             xy=(ws_landing, 0.72), xycoords="data",
             xytext=(-12, -14), textcoords="offset points",
             color="black", fontsize=9, rotation=90,
             ha="right", va="center",
             bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.6),
             zorder=10, clip_on=True)

# === 4) Balked landing ===
ax2.axhline(TW_balked_TO, color="red", linewidth=2.8)
for x0 in np.arange(WS_max*0.06, WS_max*0.26, 6.0):
    draw_slash(ax2, x0, TW_balked_TO - 0.035, color="red")
ax2.annotate("Balked landing",
             xy=(WS_max*0.10, TW_balked_TO), xycoords="data",
             xytext=(0, -6), textcoords="offset points",
             color="black", fontsize=9,
             ha="left", va="top",
             bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.6),
             zorder=10, clip_on=True)

# === Intersección Landing ∩ Take-off ===
x_intersect = ws_landing
y_intersect = TW_sea_level(x_intersect, CLmax_TO_max)
ax2.plot(x_intersect, y_intersect, 'o', color="red", markersize=7, zorder=15)
ax2.plot(x_intersect, y_intersect, 'o', color="blue", markersize=8, zorder=16)

# === Estética general ===
ax2.set_xlabel(r"TAKE-OFF WING LOADING $(W/S)_{\mathrm{TO}}\ \mathrm{[psf]}$")
ax2.set_ylabel(r"TAKE-OFF THRUST-TO-WEIGHT RATIO $(T/W)_{\mathrm{TO}}$")
ax2.set_xlim(0, WS_max)
ax2.set_ylim(0, 0.8)
ax2.margins(x=0.02, y=0.03)
ax2.grid(True, which="both", linewidth=0.6, alpha=0.5)
plt.title("Highlighted Performance Limits")

# === Sombreados (burbuja superior) — solo si hay curva de crucero ajustada ===
if TW_cr_adj is not None:
    YTOP = ax2.get_ylim()[1]
    diff_top = TW_cr_adj - YTOP
    idx = np.where(np.sign(diff_top[:-1]) * np.sign(diff_top[1:]) <= 0)[0]
    if len(idx):
        i = idx[0]
        x0, x1 = WS[i], WS[i+1]
        y0, y1 = diff_top[i], diff_top[i+1]
        x_left = x0 - y0 * (x1 - x0) / (y1 - y0)
    else:
        x_left = WS[0]
    x_right = ws_landing
    if x_right > x_left:
        mask = (WS >= x_left) & (WS <= x_right)
        x_seg = WS[mask]
        y_cru = TW_cr_adj[mask]
        y_bkl = np.full_like(x_seg, TW_balked_TO)
        y_to  = TW_takeoff[mask]
        y_bot = np.maximum.reduce([y_cru, y_bkl, y_to])
        ax2.fill_between(x_seg, y_bot, YTOP,
                         where=(YTOP > y_bot),
                         interpolate=True,
                         color='red', alpha=0.22, zorder=2)

# === Aviones: círculos de colores + leyenda inferior ===
# === Aviones: círculos de colores + leyenda inferior ===
aircraft = [
    ("Citation X (750)",  69.4, 0.37, "C0",  0.0, 70),
    ("Challenger 350",    77.6, 0.36, "C1",  0.0, 70),
    ("Gulfstream G280",   80.0, 0.39, "#2ca02c", +0.5, 100),  # <- punto verde más grande
    ("Falcon 2000LXS",    81.1, 0.33, "C3",  0.0, 70),
    ("Legacy 500",        79.5, 0.37, "C4", -0.5, 70),
]

# Dibujar cada aeronave con tamaño personalizado
for name, ws_i, tw_i, col, offset, size in aircraft:
    ax2.scatter(ws_i + offset, tw_i,
                s=size, marker='o', color=col,
                edgecolor='white', linewidths=0.9,
                zorder=25, label=name)

# === Punto azul de Design Point ===
ax2.scatter(x_intersect, y_intersect,
            s=80, marker='o', color="blue",
            edgecolor="white", linewidths=0.9,
            zorder=26, label="Design Point")


# === Leyenda actualizada ===
legend = ax2.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.22),
    ncol=3,
    frameon=True,
    fontsize=9,
    title="Reference business jets"
)
fig2.subplots_adjust(bottom=0.32)


plt.show()

print(f"Coordenadas del Design Point: (W/S) = {x_intersect:.2f} psf, (T/W) = {y_intersect:.3f}")
