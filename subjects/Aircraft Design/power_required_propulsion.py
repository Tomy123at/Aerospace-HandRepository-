
from dataclasses import dataclass
import numpy as np

g = 9.80665
R = 287.058
T0 = 288.15
p0 = 101325.0
L  = -0.0065
gamma = 1.4

def isa_atmosphere(h_m: float):
    if h_m < 0:
        h_m = 0.0
    if h_m <= 11000.0:
        T = T0 + L*h_m
        p = p0 * (T/T0)**(-g/(L*R))
    else:
        T11 = T0 + L*11000.0
        p11 = p0 * (T11/T0)**(-g/(L*R))
        p = p11 * np.exp(-g*(h_m-11000.0)/(R*T11))
        T = T11
    rho = p/(R*T)
    a = np.sqrt(gamma*R*T)
    return T, p, rho, a

@dataclass
class Aircraft:
    mass_kg: float
    S_m2: float
    CD0: float
    AR: float
    e: float
    eta_prop: float = 0.85

def power_required(aircraft: Aircraft, V_ms: float, h_m: float):
    T, p, rho, a = isa_atmosphere(h_m)
    W = aircraft.mass_kg * g
    q = 0.5 * rho * V_ms**2
    CL = W / (q * aircraft.S_m2)
    CDi = CL**2 / (np.pi * aircraft.e * aircraft.AR)
    CD  = aircraft.CD0 + CDi
    D   = q * aircraft.S_m2 * CD
    P_aero = D * V_ms
    P_shaft = P_aero / aircraft.eta_prop
    return {
        "rho_kgm3": rho, "a_mps": a, "Mach": V_ms/a,
        "CL": CL, "CD0": aircraft.CD0, "CDi": CDi, "CD": CD,
        "q_Pa": q, "Drag_N": D, "Thrust_req_N": D,
        "P_aero_W": P_aero, "P_shaft_W": P_shaft, "P_shaft_hp": P_shaft/745.7
    }

if __name__ == "__main__":
    # Ejemplo rápido
    ac = Aircraft(2400.0, 18.0, 0.022, 11.0, 0.83, 0.85)
    V_ms = 160.0 * 0.514444
    h_m  = 15000.0 * 0.3048
    res = power_required(ac, V_ms, h_m)
    for k, v in res.items():
        if k.endswith("_hp"):
            print(f"{k}: {v:.2f}")
        elif k.endswith("_W"):
            print(f"{k}: {v/1000:.2f} kW")
        else:
            print(f"{k}: {v}")
