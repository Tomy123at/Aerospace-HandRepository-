import math


def calcular_Mff():
    
    # Engine Start Warm Up
    
    w1_wto = 0.992
    
    # Taxi
    
    w2_wt1 = 0.996
    
    # Take off
    
    w3_wt2 = 0.996
    
    # Climb
    
    w4_wt3 = 0.990
    
    
    # Cruise for propeller aircraft, R is in sm
    
    R_cr        = 1000.0
    eta_p       = 0.82
    cp_cr       = 0.50
    L_over_D_cr = 11.0

    W5_W4 = math.exp(-R_cr / (375 * (eta_p/cp_cr) * L_over_D_cr))
    
    # Descent
    
    w6_wt5 = 0.992
    
    #Landing, Taxi & Shut out
    
    w7_wt6 = 0.992
    
    Mff = w1_wto * w2_wt1 * w3_wt2 * w4_wt3 * W5_W4 * w6_wt5 * w7_wt6
    
    
    return Mff

#------------------------------------------------------------------------------


# Loiter for propeller aircraft, V_ltr is in mph & E_ltr is in hours

E_ltr        = 200.0    # energía de loitering [por ejemplo]
V_ltr        = 150.0    # velocidad de loitering en mph
eta_p        = 0.85     # eficiencia del propulsor en loitering
cp_ltr       = 0.50     # potencia específica en loitering
L_over_D_ltr = 11.0     # relación L/D en loitering

# Cálculo en una sola línea:
W6_W5 = math.exp(-E_ltr * V_ltr / (375 * (eta_p/cp_ltr) * L_over_D_ltr))



# Cruise for jet aircraft, R is in nm

R_cr        = 120.0    # valor de R_cr
V_cr        = 200.0    # velocidad V_cr
cj_cr       = 0.45     # c_j en condición crítica
L_over_D_cr = 12.0     # relación L/D en condición crítica

# Cálculo directo de W5/W4:
W5_over_W4 = math.exp(-R_cr / ((V_cr/cj_cr) * L_over_D_cr))

# Loiter for jet aircraft, E_ltr is in hours

E_ltr        = 200.0     # energía de loiter [por ejemplo]
cj_ltr       = 0.05      # c_j en loiter
L_over_D_ltr = 11.0      # (L/D) en loiter

# Ratio W6/W5 en una sola línea
W6_W5 = math.exp(- E_ltr / ((1/cj_ltr) * L_over_D_ltr))

#------------------------------------------------------------------------------
















def calcular_WTO(A: float, B: float, c: float, D: float,
                 tol: float = 1e-8, max_iter: int = 100) -> float:
    """
    Resuelve log10(x) = A + B*log10(c*x - D) para x > D/c
    usando el método de bisección.
    Parámetros:
      - A, B, c, D: constantes de la ecuación
      - tol: tolerancia en el valor de f(x_mid)
      - max_iter: iteraciones máximas de bisección
    Retorna:
      - x ≈ WTO que satisface la ecuación.
    """
    # Dominio mínimo: c*x - D > 0  =>  x > D/c
    x_min = D / c
    if c <= 0:
        raise ValueError("c debe ser positivo")
    if D < 0:
        raise ValueError("D debe ser no negativo")
    
    # Función f(x) = log10(x) - A - B*log10(c*x - D)
    def f(x: float) -> float:
        return math.log10(x) - A - B * math.log10(c*x - D)
    
    # Puntos que encierren la raíz
    x_low = x_min * (1 + 1e-6)
    f_low = f(x_low)
    x_high = x_low * 2.0

    # Ampliar hasta cambiar de signo
    for _ in range(100):
        f_high = f(x_high)
        if f_low * f_high < 0:
            break
        x_high *= 2.0
    else:
        raise RuntimeError("No se encontró intervalo con cambio de signo")

    # Bisección
    for _ in range(max_iter):
        x_mid = 0.5 * (x_low + x_high)
        f_mid = f(x_mid)
        if abs(f_mid) < tol or (x_high - x_low) < tol:
            return x_mid
        # Reducir intervalo
        if f_low * f_mid < 0:
            x_high = x_mid
        else:
            x_low = x_mid
            f_low = f_mid

    raise RuntimeError(f"No convergió en {max_iter} iteraciones")

if __name__ == "__main__":
    # Parámetros de ejemplo
    A   = 0.0966
    B   = 1.0298
#------------------------    
    Mff = calcular_Mff()
    Mres = 0.25
    Mtfo = 0.005
    c = 1 - (1 + Mres) * (1 - Mff) - Mtfo
#------------------------
    
    WPL = 1250
    Wcrew = 0
    D   = Wcrew + WPL

    try:
        wto = calcular_WTO(A, B, c, D)
        print(f"WTO ≈ {wto:.4f}")
    except Exception as e:
        print("Error al calcular WTO:", e)
