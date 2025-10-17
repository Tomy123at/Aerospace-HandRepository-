import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# Atmospheric Data
Humidity = 100  #%
P = 101727.12  #Pa
Visc = 1.823 * 10**(-5)
R = 287
Rho = 1.201  #Kg/m3

# Flight condition
AoA = 3  #Deg
V = 7  #m/s
q = (1/2) * Rho * V**2

# Wing initial Geometry
Landa = 1
AR = 7.5

# Wing parameters
a0 = 0.099
a = a0 / (1 + (a0 / math.pi * AR))
aL0 = -3.339  # Deg
aa = AoA - aL0
CL = a * (AoA - aL0)
CMacwb = -0.1023

# Wing final Geometry
S = (1 * 9.81) / (q * CL)  #m2
b = math.sqrt(AR * S)  #m
c = S / b  #m

# Tail parameters
lt = 4 * c
at = 0.0644047966379471
aL0t = 0

# General Parameters
epsilon0 = (2 * CL) / math.pi * AR
deda = (2 * math.degrees(a)) / (math.pi * AR)
hacwb = 0.25

angles = np.arange(-2, 10.5, 0.5)
St_values = np.arange(0.05, 0.45, 0.05)

it = 2

plt.figure(figsize=(10, 8))

annotations = []

for St in St_values:  
    bt = math.sqrt((AR / 2) * St)
    ct = St / bt
    VH = St * lt / (c * S)
    
    hn = 0.25 + VH * (at / a) * (1 - deda)
    h = ((hn - hacwb) / 2) + hacwb
    SM = hn - h

    dCMcgdaa = a * (h - hacwb - VH * (at / a) * (1 - deda))
    epsilon = epsilon0 + deda * math.radians(aa)

    CM0 = CMacwb + VH * at * (it + epsilon0)
    aeq = -CM0 / dCMcgdaa
    ageo = aeq + aL0
    CLageo = a * (ageo - aL0)
    L = (q * S * CLageo) / 9.81

    CMcgvalues = []
    for i in range(len(angles)):
        CMcgvalues.append(dCMcgdaa * angles[i] + CM0)

    plt.plot(angles, CMcgvalues, label=f'St = {St:.2f} m²', marker='o')

    annotations.append(f'St = {St:.2f} m²: dCMcg/dAa = {dCMcgdaa:.4f}, CM0 = {CM0:.4f}')

# Graph properties
plt.title('CMcg vs AoA for varying St values (it = 2°)')
plt.xlabel('AoA (degrees)')
plt.ylabel('CMcg')
plt.grid(True)

# Add legend and annotations
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.text(11, min(CMcgvalues), '\n'.join(annotations), fontsize=10, color='black', verticalalignment='bottom')

# Adjust layout to fit annotations
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()
