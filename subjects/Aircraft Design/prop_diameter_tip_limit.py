# Cálculo de diámetro de hélice y RPM con límite de velocidad de punta en crucero (250 m/s)
import math

# -----------------------------
# Parámetros de tu aeronave
# -----------------------------
P_hp   = 250.0                # [hp]
eta_p  = 0.85
AR_p   = 7.0
CL_p   = 0.4
V_c_kts = 160.0               # [kt]
h_ft    = 15000.0             # [ft]

# Hélice
blades    = 6
Knp_table = {2:1.00, 3:0.93, 4:0.86, 5:0.79, 6:0.72}
K_np      = Knp_table[blades]

V_tip_cruise = 250.0          # [m/s]

# -----------------------------
# ISA simple
# -----------------------------
g = 9.80665
R = 287.058
T0 = 288.15
p0 = 101325.0
L  = -0.0065
gamma = 1.4

def isa_atmosphere(h_m: float):
    if h_m < 0: h_m = 0.0
    if h_m <= 11000.0:
        T = T0 + L*h_m
        p = p0 * (T/T0)**(-g/(L*R))
    else:
        T11 = T0 + L*11000.0
        p11 = p0 * (T11/T0)**(-g/(L*R))
        p = p11 * math.exp(-g*(h_m-11000.0)/(R*T11))
        T = T11
    rho = p/(R*T)
    a = math.sqrt(gamma*R*T)
    return T, p, rho, a

# -----------------------------
# Conversión y estados
# -----------------------------
hp_to_W = 745.7
kt_to_ms = 0.514444
ft_to_m  = 0.3048

P_W = P_hp * hp_to_W
V_c = V_c_kts * kt_to_ms
h_m = h_ft * ft_to_m

_, _, rho, a = isa_atmosphere(h_m)
V_av = 0.7 * V_tip_cruise

# Ecuación (8.13)
numerator   = 2 * P_W * eta_p * AR_p
denominator = rho * (V_av**2) * CL_p * V_c
D_prop = K_np * math.sqrt(numerator / denominator)

# rpm necesarias para rozar V_tip en crucero
V_tip_static = math.sqrt(max(V_tip_cruise**2 - V_c**2, 0.0))
rpm = 60.0 * (2 * V_tip_static) / (math.pi * D_prop)

print("=== Entradas ===")
print(f"P = {P_hp} hp  (={P_W/1000:.1f} kW)")
print(f"rho(15000 ft) = {rho:.4f} kg/m^3,  a = {a:.1f} m/s")
print(f"V_cruise = {V_c_kts} kt ({V_c:.2f} m/s)")
print(f"blades = {blades}, K_np = {K_np}")
print(f"AR_p = {AR_p},  CL_p = {CL_p},  eta_p = {eta_p}")
print(f"V_tip_cruise = {V_tip_cruise} m/s  -> V_av = {V_av:.1f} m/s")

print("\n=== Resultados ===")
print(f"Diámetro D_p = {D_prop:.3f} m  ({D_prop*39.3701:.1f} in)")
print(f"RPM (para rozar V_tip) ≈ {rpm:.0f} rpm")
print(f"V_tip_static = {V_tip_static:.1f} m/s")

