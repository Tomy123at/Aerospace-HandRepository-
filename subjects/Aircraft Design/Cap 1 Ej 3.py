# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 11:05:56 2025

@author: jlope
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:52:09 2025

@author: jlope
"""

import math

# region Avance horizontal ascenso
#------------------------------------------------------------------------------
# Calcular avance horizontal tras ascenso

import math

def climb_profile(V_climb_kts, RC_fpm , h_ft):
    """
    Dado:
      - V_climb_kts: velocidad de ascenso [kts] (speed along flight path)
      - RC_fpm:       rate of climb [ft/min]
      - h_ft:         altura a subir [ft]
    Devuelve:
      - V_horizontal_kts: velocidad horizontal [kts]
      - time_min:         tiempo de ascenso [min]
      - distance_nm:      distancia horizontal recorrida [NM]
      - distance_ft:      distancia horizontal recorrida [ft]
    """
    # 1 kt = 6076.12 ft/h
    # Convertir RC (ft/min) → velocidad vertical en kts:
    V_vert_kts = (RC_fpm * 60) / 6076.12

    # Componente horizontal en kts por Pitágoras:
    V_horizontal_kts = math.sqrt(max(V_climb_kts**2 - V_vert_kts**2, 0))

    # Tiempo para subir h_ft (min)
    time_min = h_ft / RC_fpm

    # Distancia horizontal:
    #   en nmi: V_horizontal_kts [NM/h] * (time_min/60) [h]
    distance_nm = V_horizontal_kts * (time_min / 60.0)
    #   en ft: distance_nm * 6076.12
    distance_ft = distance_nm * 6076.12

    return V_horizontal_kts, time_min, distance_nm, distance_ft



#------------------------------------------------------------------------------




import math

# region Calcular Mff_1
def calcular_Mff_1():
    # Engine Start Warm Up
    W1_Wto = 0.990
    print(f"W1_Wto = {W1_Wto}")

    # Taxi
    W2_W1 = 0.990
    print(f"W2_W1 = {W2_W1}")

    # Take off
    W3_W2 = 0.990
    print(f"W3_W2 = {W3_W2}")

    # Climb
    W4_W3 = 0.971
    print(f"W4_W3 = {W4_W3}")

    # Cruise for jet aircraft, R is in nm
    V_climb_kts = 350
    RC_fpm = 5000
    h_ft = 40000
    print(f"V_climb_kts = {V_climb_kts} kts")
    print(f"RC_fpm = {RC_fpm} ft/min")
    print(f"h_ft = {h_ft} ft")

    _, _, distance_nm, _, = climb_profile(V_climb_kts, RC_fpm, h_ft)
    R_cr = 300 - distance_nm
    print(f"R_cr (cruise range) = {R_cr} nm")

    V_cr = 459
    cj_cr = 0.6
    L_over_D_cr = 7.0
    print(f"V_cr = {V_cr} kts")
    print(f"cj_cr = {cj_cr}")
    print(f"L_over_D_cr = {L_over_D_cr}")

    W5_W4 = math.exp(-R_cr / ((V_cr/cj_cr) * L_over_D_cr))
    print(f"W5_W4 = {W5_W4}")

    # Loiter for jet aircraft, E_ltr is in hours
    E_ltr = 0.5
    cj_ltr = 0.6
    L_over_D_ltr = 9.0
    print(f"E_ltr = {E_ltr} h")
    print(f"cj_ltr = {cj_ltr}")
    print(f"L_over_D_ltr = {L_over_D_ltr}")

    W6_W5 = math.exp(- E_ltr / ((1/cj_ltr) * L_over_D_ltr))
    print(f"W6_W5 = {W6_W5}")

    # Descent
    W7_W6 = 0.990
    print(f"W7_W6 = {W7_W6}")

    # Dash Out
    R_alt = 100
    V_cr_alt = 250.0
    cj_cr_alt = 0.9
    L_over_D_cr_alt = 4.5
    print(f"R_alt (to alternate) = {R_alt} nm")
    print(f"V_cr_alt = {V_cr_alt} kts")
    print(f"cj_cr_alt = {cj_cr_alt}")
    print(f"L_over_D_cr_alt = {L_over_D_cr_alt}")

    W8_W7 = math.exp(-R_alt / ((V_cr_alt/cj_cr_alt) * L_over_D_cr_alt))
    print(f"W8_W7 = {W8_W7}")
    

    # Mission fuel fraction
    Mff_1 = (W1_Wto * W2_W1 * W3_W2 * W4_W3 *
           W5_W4 * W6_W5 * W7_W6 * W8_W7 )
    print(f"Mff_1 = {Mff_1}")


    return Mff_1

# region Calcular Mff_2
def calcular_Mff_2(wto_anterior):
    
    # Strafe
    
    weight_drop_out = 10000 * 1
    w9 = wto_anterior - weight_drop_out
    
    E_ltr = 5/60
    cj_ltr = 0.9
    L_over_D_ltr = 4.5
    print(f"E_ltr = {E_ltr} h")
    print(f"cj_ltr = {cj_ltr}")
    print(f"L_over_D_ltr = {L_over_D_ltr}")

    W10_W9_Wrong = math.exp(- E_ltr / ((1/cj_ltr) * L_over_D_ltr))
    print(f"W10_W9_Wrong = {W10_W9_Wrong}")
    
    W10_W9_Right = 1 - (1 - W10_W9_Wrong) * ((wto_anterior - weight_drop_out)/(wto_anterior))
    

    # Mission fuel fraction
    Mff_2 = (W10_W9_Right)
    print(f"Mff_2 = {Mff_2}")

    return Mff_2
    
# region Calcular Mff_3
def calcular_Mff_3(wto_anterior):
    
    
    # Dash_In
    weight_drop_out = 2000 * 1
    w10 = wto_anterior - weight_drop_out

    
    # Dash Out
    R_alt = 100
    V_cr_alt = 450.0
    cj_cr_alt = 0.9
    L_over_D_cr_alt = 5.5
    print(f"R_alt (to alternate) = {R_alt} nm")
    print(f"V_cr_alt = {V_cr_alt} kts")
    print(f"cj_cr_alt = {cj_cr_alt}")
    print(f"L_over_D_cr_alt = {L_over_D_cr_alt}")

    W11_W10_Wrong = math.exp(-R_alt / ((V_cr_alt/cj_cr_alt) * L_over_D_cr_alt))
    print(f"W11_W10_Wrong = {W11_W10_Wrong}")
    
    W11_W10_Right =  1 - (1 - W11_W10_Wrong) * ((wto_anterior - weight_drop_out)/(wto_anterior))
    print(f"W11_W10_Right = {W11_W10_Right}")



    # Climb
    W12_W11 = 0.969
    print(f"W12_W11 = {W12_W11}")
    
    #Cruise
    
    V_climb_kts = 350
    RC_fpm = 5000
    h_ft = 40000
    print(f"V_climb_kts = {V_climb_kts} kts")
    print(f"RC_fpm = {RC_fpm} ft/min")
    print(f"h_ft = {h_ft} ft")

    _, _, distance_nm, _, = climb_profile(V_climb_kts, RC_fpm, h_ft)
    R_cr = 300 - distance_nm
    print(f"R_cr (cruise range) = {R_cr} nm")

    V_cr = 488
    cj_cr = 0.6
    L_over_D_cr = 7.5
    print(f"V_cr = {V_cr} kts")
    print(f"cj_cr = {cj_cr}")
    print(f"L_over_D_cr = {L_over_D_cr}")

    W13_W12 = math.exp(-R_cr / ((V_cr/cj_cr) * L_over_D_cr))
    print(f"W12_W11 = {W12_W11}")
    
    
    #Descent
    
    W14_W13 = 0.990
    print(f"W13_W12 = {W13_W12}")
    
    
    
    # Landing, Taxi, ShutDown
    W15_W14 = 0.995
    print(f"W15_W14 = {W15_W14}")
    

    # Mission fuel fraction
    Mff_3 = (W11_W10_Right * W12_W11 * W13_W12 * W14_W13 * W15_W14)
    print(f"Mff_3 = {Mff_3}")
    
    
    
    
    
    return Mff_3

#------------------------------------------------------------------------------

# region Loiter and Cruise 
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
W5_W4 = math.exp(-R_cr / ((V_cr/cj_cr) * L_over_D_cr))

# Loiter for jet aircraft, E_ltr is in hours

E_ltr        = 200.0     # energía de loiter [por ejemplo]
cj_ltr       = 0.05      # c_j en loiter
L_over_D_ltr = 11.0      # (L/D) en loiter

# Ratio W6/W5 en una sola línea
W6_W5 = math.exp(- E_ltr / ((1/cj_ltr) * L_over_D_ltr))






#------------------------------------------------------------------------------
# region Calcular WTO




import math
import matplotlib.pyplot as plt

def calcular_WTO_convergencia(A: float, B: float, c: float, D: float,
                              tol: float = 1e-8, max_iter: int = 100):
    """
    Resuelve log10(x) = A + B*log10(c*x - D) usando bisección,
    registrando la convergencia en cada iteración.
    Retorna el valor de WTO aproximado y la lista de x_mid por iteración.
    """
    # Dominio mínimo
    x_min = D / c
    if c <= 0:
        raise ValueError("c debe ser positivo")
    if D < 0:
        raise ValueError("D debe ser no negativo")
    
    def f(x):
        return math.log10(x) - A - B * math.log10(c*x - D)
    
    # Encuentra intervalo inicial
    x_low = x_min * (1 + 1e-6)
    f_low = f(x_low)
    x_high = x_low * 2
    
    for _ in range(100):
        f_high = f(x_high)
        if f_low * f_high < 0:
            break
        x_high *= 2
    else:
        raise RuntimeError("No se encontró intervalo con cambio de signo")
    
    # Bisección con registro de convergencia
    x_mid_list = []
    for i in range(max_iter):
        x_mid = 0.5 * (x_low + x_high)
        x_mid_list.append(x_mid)
        f_mid = f(x_mid)
        if abs(f_mid) < tol or (x_high - x_low) < tol:
            return x_mid, x_mid_list
        if f_low * f_mid < 0:
            x_high = x_mid
        else:
            x_low = x_mid
            f_low = f_mid
    
    raise RuntimeError(f"No convergió en {max_iter} iteraciones")

# Parámetros de ejemplo
A = 0.5091
B = 0.9505
# Asumimos Mff y c calculados como en tu script...
Mff_1 = calcular_Mff_1()   # ejemplo
Mres = 0.0
Mtfo = 0.005
c1 = 1 - (1 + Mres) * (1 - Mff_1) - Mtfo
WPL = 12000
Wcrew = 200
D = Wcrew + WPL

wto1, history = calcular_WTO_convergencia(A, B, c1, D)

# Graficar convergencia
plt.figure()
plt.plot(history, marker='o')
plt.title("Convergencia de WTO por iteración (bisección)")
plt.xlabel("Iteración")
plt.ylabel("Valor WTO aproximado")
plt.grid(True)
plt.tight_layout()
plt.show()

# Mostrar valor final



Mff_2 = calcular_Mff_2(wto1)
c2 = 1 - (1 + Mres) * (1 - (Mff_1 * Mff_2)) - Mtfo
wto2, history = calcular_WTO_convergencia(A, B, c2, D)


Mff_3 = calcular_Mff_3(wto2)
print()

cfinal = 1 - (1 + Mres) * (1 - (Mff_1 * Mff_2 * Mff_3)) - Mtfo
wto_final, history = calcular_WTO_convergencia(A, B, cfinal, D)


print(f"Mff final ≈ {Mff_1 * Mff_2 * Mff_3}")

print(f"WTO final ≈ {wto_final:.4f}")




