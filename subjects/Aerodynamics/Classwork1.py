import numpy as np
from scipy.integrate import quad
import pandas as pd
import matplotlib.pyplot as plt
import math 

file = r'C:\Users\tomya\OneDrive\Documentos\Universidad\2024-2\Aerodinámica\classwork1_Data.txt'

data_file = pd.read_csv(file, delim_whitespace=True, header=None)

x = np.zeros(21)
v_loc_l = np.zeros(21)
v_loc_u = np.zeros(21)

x = data_file[0].to_numpy().astype(float)
v_loc_l = data_file[1].to_numpy().astype(float)
v_loc_u = data_file[2].to_numpy().astype(float)

chord = 0.18
wing_span = 0.91

P_inf = 86438.42 #Pa
T = 280.49 #K
R = 287

Densidad = P_inf/(R*T)
print("La densidad es: ",Densidad)
P_l = np.zeros(21)
P_l[0]= 1

for i in range(1,21):
    P_l[i] = P_inf+(1/2)*Densidad*v_loc_l[i-1]-1


alpha_zero_cl = -3.31
lift_slope = 0.10737

b = -lift_slope * alpha_zero_cl
print("La intersección con el eje y (b) es:", b)

alpha = np.linspace(-4.02, 5.32, 100)

Cl = lift_slope * alpha + b

plt.figure(figsize=(10, 6))
plt.plot(alpha, Cl, label='Lift Curve')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.title('Coeficiente de Sustentación vs. Ángulo de Ataque')
plt.xlabel('Ángulo de Ataque (deg)')
plt.ylabel('Coeficiente de Sustentación (Cl)')
plt.legend()
plt.grid(True)
plt.show()

