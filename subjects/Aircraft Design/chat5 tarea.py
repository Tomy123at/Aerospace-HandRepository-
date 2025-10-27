# -*- coding: utf-8 -*-
"""
Roskam – sizing iterativo + F y sensibilidades (JET), con un único drop de peso
"""

import math
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ 1) FUNCION: calcular MFF dado WTO_guess ------------------
def calcular_mff_total(WTO_guess: float) -> float:
    """
    Misión (jet pesado):
      Start, Taxi, Takeoff, Climb,
      Cruise WITH Shuttle (R1, cj1, L/D1, V),
      DROP Shuttle (sin penalidad de combustible, pero corrige etapa siguiente),
      Cruise WITHOUT Shuttle (R2, cj2, L/D2, V)  <-- corregida por drop,
      Loiter (E, cj3, L/D3),
      Descent, Shutdown.
    """
    # Fases "fijas"
    mff_startup = 0.99
    mff_taxi    = 0.99
    mff_takeoff = 0.995
    #mff_climb   = 0.9676
    mff_climb   = 0.98


    # --- Cruise WITH Space Shuttle ---
    R_with   = 3239.74*0.43      # [nm]
    V_kts    = 520.0        # [kts]
    cj_with  = 0.7          # [lb/lb/hr]
    LD_with  = 13.0
    mff_with = math.exp(-R_with / ((V_kts / cj_with) * LD_with))

    # --- DROP Space Shuttle (solo masa, sin combustible) ---
    W_shuttle = 420000.0  # [lb]
    mff_drop  = 1.0

    # Para la corrección de la etapa posterior necesitamos el factor de peso
    mff_to_drop = mff_startup * mff_taxi * mff_takeoff * mff_climb * mff_with * mff_drop
    W_before = WTO_guess * mff_to_drop
    W_after  = W_before - W_shuttle
    weight_factor = W_after / W_before  # = W_{to,después}/W_{to,antes}

    # --- Cruise WITHOUT Shuttle (CORREGIDA por drop previo) ---
    R_wo     = 3239.74*0.57    # [nm]
    cj_wo    = 0.6
    LD_wo    = 14
    mff_wo_nom = math.exp(-R_wo / ((V_kts / cj_wo) * LD_wo))
    # Corrección por drop: mff_corr = 1 - (1 - mff_nom)*weight_factor
    mff_wo = 1.0 - (1.0 - mff_wo_nom) * weight_factor

    # --- Loiter ---
    E_loiter = 20.0/60.0   # [hr]
    cj_loit  = 0.45
    LD_loit  = 15.0
    mff_loit = math.exp(-E_loiter / ((1.0 / cj_loit) * LD_loit))

    # --- Descent & Shutdown ---
    mff_descent  = 0.990
    mff_shutdown = 0.992

    # Producto total (en orden)
    mff_total = (
        mff_startup * mff_taxi * mff_takeoff * mff_climb *
        mff_with * mff_drop * mff_wo * mff_loit *
        mff_descent * mff_shutdown
    )
    return mff_total


# --------------- 2) FUNCION: un paso para nuevo WTO_guess --------------------
def nuevo_WTO_guess(WTO_guess: float, Mff: float, *,
                    A: float, B: float,
                    WPayload: float, WCrew: float,
                    Mres: float, ftfo: float,
                    damping: float = 0.5) -> dict:
    """
    Un paso de Newton amortiguado sobre:
      f(W) = WE_allow(W) - WE_tent(W)
      WE_allow = 10**((log10 W - A)/B)
      WE_tent  = k*W - (WPL+WCrew), con k = 1 - (1-Mff)*(1+Mres) - ftfo
    """
    k = 1.0 - (1.0 - Mff) * (1.0 + Mres) - ftfo
    Wconst = WPayload + WCrew

    def WE_allow(W):
        return 10.0 ** ((math.log10(max(W, 1e-12)) - A) / B)

    W = max(WTO_guess, 1.0)
    WEa = WE_allow(W)
    WEt = k * W - Wconst
    f   = WEa - WEt
    fp  = (WEa / (B * W)) - k

    if fp == 0.0 or not math.isfinite(fp):
        W_new = max(W * 1.05, 1.0)
    else:
        W_new = W - damping * (f / fp)
        if not math.isfinite(W_new) or W_new <= 0.0:
            W_new = max(W * 1.05, 1.0)

    return {"WTO_new": W_new, "f": f, "k": k, "WE_allow": WEa, "WE_tent": WEt}


# --------------- 3) FUNCION: iterar hasta convergencia -----------------------
def iterar_convergencia(WTO_guess0: float,
                        tol_rel: float = 1e-8,
                        max_iter: int = 100,
                        *,
                        A: float = -0.2009,
                        B: float = 1.1037,
                        WPayload: float = 420000.0,
                        WCrew: float = 1800.0,
                        Mres: float = 0.0,
                        ftfo: float = 0.005,
                        damping: float = 0.5,
                        hacer_grafica: bool = True):
    """
    Bucle: WTO -> MFF(WTO) -> nuevo WTO -> ... hasta converger.
    """
    history = []
    W = float(WTO_guess0)

    for it in range(1, max_iter + 1):
        Mff = calcular_mff_total(W)
        paso = nuevo_WTO_guess(W, Mff, A=A, B=B,
                               WPayload=WPayload, WCrew=WCrew,
                               Mres=Mres, ftfo=ftfo, damping=damping)

        W_new = paso["WTO_new"]
        rel_change = abs(W_new - W) / max(W_new, 1e-12)

        history.append({
            "iter": it, "WTO": W, "Mff": Mff,
            "WE_allow": paso["WE_allow"], "WE_tent": paso["WE_tent"],
            "f": paso["f"], "WTO_new": W_new, "rel_change": rel_change
        })

        W = W_new
        if rel_change <= tol_rel:
            break

    df = pd.DataFrame(history)

    if hacer_grafica and not df.empty:
        plt.figure()
        plt.plot(df["iter"], df["WTO_new"], marker="o")
        plt.xlabel("Iteración")
        plt.ylabel("WTO [lb]")
        plt.title("Convergencia de WTO (Newton amortiguado)")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.tight_layout()
        plt.show()

    return {
        "WTO": W,
        "history": df,
        "params": dict(A=A, B=B, WPayload=WPayload, WCrew=WCrew,
                       Mres=Mres, ftfo=ftfo, damping=damping,
                       tol_rel=tol_rel, max_iter=max_iter)
    }


# --------------- 4) F y sensibilidades (JET) --------------------------------
def calcular_F_y_sensibilidades_jet(
    WTO: float, Mff: float, Mres: float, Mtfo: float,
    WPL: float, Wcrew: float, A: float, B: float,
    legs: list
):
    """
    Calcula C, D, F y sensibilidades tipo JET por etapa.
    Fórmulas (Tabla 2.20, caso JET):

      Range (usa R y V):
        dW/dR   = F * (c_j / (V * (L/D)))
        dW/dc_j = F * (R   / (V * (L/D)))
        dW/dV   = F * ( - R c_j / (V^2 * (L/D)) )
        dW/d(L/D) = F * ( - R c_j / (V * (L/D)^2) )

      Endurance:
        dW/dE   = F * (c_j / (L/D))
        dW/dc_j = F * (E   / (L/D))
        dW/d(L/D) = F * ( - E c_j / (L/D)^2 )

    Además reporta:
      dWTO/dWPL  (payload)
      dWTO/dWE   (empty weight)
    """
    # C y D
    D = Wcrew + WPL
    C = 1.0 - (1.0 + Mres) * (1.0 - Mff) - Mtfo

    denom = C * WTO * (1.0 - B) - D
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Denominador de F ~ 0; revisa datos.")

    # F (tu fórmula)
    F = (-B * WTO**2 / denom) * (1.0 + Mres) * Mff

    # Sensibilidades que NO usan F
    dWTO_dWPL = (B * WTO) / (D - C * (1.0 - B) * WTO)
    WE_allow  = 10.0 ** ((math.log10(WTO) - A) / B)
    dWTO_dWE  = (B * WTO) / WE_allow

    rows = []
    for leg in legs:
        name = leg.get("name", "")
        t    = leg["type"].lower()
        cj   = float(leg["cj"])
        LD   = float(leg["L_D"])

        if t == "range":
            R = float(leg["R"]); V = float(leg["V"])
            dW_dR  = F * (cj / (V * LD))
            dW_dcj = F * (R  / (V * LD))
            dW_dV  = F * (-(R * cj) / (V**2 * LD))     # ojo: V^2
            dW_dLD = F * (-(R * cj) / (V * LD**2))
            rows.append({"leg": name, "type": "range",
                         "dWTO/dR": dW_dR, "dWTO/dE": None,
                         "dWTO/dcj": dW_dcj, "dWTO/dV": dW_dV,
                         "dWTO/d(L/D)": dW_dLD})

        elif t == "endurance":
            E = float(leg["E"])
            dW_dE  = F * (cj / LD)
            dW_dcj = F * (E  / LD)
            dW_dLD = F * (-(E * cj) / (LD**2))
            rows.append({"leg": name, "type": "endurance",
                         "dWTO/dR": None, "dWTO/dE": dW_dE,
                         "dWTO/dcj": dW_dcj, "dWTO/dV": None,
                         "dWTO/d(L/D)": dW_dLD})
        else:
            raise ValueError("leg['type'] debe ser 'range' o 'endurance'.")

    cols = ["leg","type","dWTO/dR","dWTO/dE","dWTO/dcj","dWTO/dV","dWTO/d(L/D)"]
    df = pd.DataFrame(rows, columns=cols)

    return {"C": C, "D": D, "F": F,
            "dWTO_dWPL": dWTO_dWPL, "dWTO_dWE": dWTO_dWE,
            "sensibilidades": df}


# ------------------------------ Ejemplo de uso -------------------------------
if __name__ == "__main__":
    # Itera con el jet pesado
    res = iterar_convergencia(WTO_guess0=1_200_000.0, tol_rel=5e-8, max_iter=200,
                              A=-0.2009, B=1.1037,
                              WPayload=420000.0, WCrew=1800.0,
                              Mres=0.0, ftfo=0.005,
                              damping=0.5, hacer_grafica=True)

    WTO_conv = float(res["WTO"])
    print(f"\nWTO convergido: {WTO_conv:.3f} lb")

    # Mff en el WTO convergido (para F)
    Mff_final = calcular_mff_total(WTO_conv)

    # Legs para sensibilidad (coherentes con la misión)
    legs_jet = [
        {"name": "Cruise-with-SS",    "type": "range",     "cj": 0.7, "V": 520.0, "L_D": 14.0,  "R": 1393.09},
        {"name": "Cruise-withOUT-SS", "type": "range",     "cj": 0.5, "V": 520.0, "L_D": 15.5, "R": 1846.65},
        {"name": "Loiter",            "type": "endurance", "cj": 0.4,             "L_D": 16.0, "E": 20.0/60.0},
    ]

    out = calcular_F_y_sensibilidades_jet(
        WTO=WTO_conv, Mff=Mff_final, Mres=0.0, Mtfo=0.005,
        WPL=420000.0, Wcrew=1800.0, A=-0.2009, B=1.1037,
        legs=legs_jet
    )

    print(f"C={out['C']:.6f}  D={out['D']:.1f}  F={out['F']:.3f}")
    print(f"dWTO/dWPL = {out['dWTO_dWPL']:.3f}   dWTO/dWE = {out['dWTO_dWE']:.3f}")

    # ---- NUEVO: reportar WE y Mff ----
    A, B = -0.2009, 1.1037
    WE = 10.0 ** ((math.log10(WTO_conv) - A) / B)
    print(f"WE (empty weight) = {WE:.2f} lb")
    print(f"Mff (mass fraction final de misión) = {Mff_final:.6f}")

    df_hist = res["history"]
    df_sens = out["sensibilidades"]

    print("\nSensibilidades por etapa (JET):")
    print(df_sens.to_string(index=False))

    # Guardar CSVs
    df_hist.to_csv("iteracion_WTO_historial.csv", index=False)
    df_sens.to_csv("sensibilidades_jet.csv", index=False)
