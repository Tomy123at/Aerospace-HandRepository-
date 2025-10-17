import numpy as np
import matplotlib.pyplot as plt


Cp4deg_Up = [1.124, -0.647, -0.506, -0.445, -0.421, -0.343, -0.249, -0.079, 0.000, 0.149]
Cp4deg_Bottom = [1.12, 0.26, 0.23, 0.00, 0.23, 0.30, 0.27]

Cp0deg_Up = [1.114, -0.218, -0.248, -0.237, -0.253, -0.243, -0.165, -0.125, -0.015, 0.101]
Cp0deg_Bottom = [1.114, -0.199, -0.040, -0.204, 0.086, 0.200, 0.167]

CpNeg2deg_Up = [0.976, -0.035, -0.156, -0.188, -0.225, -0.230, -0.144, -0.091, 0.037, 0.097]
CpNeg2deg_Bottom = [0.976, -0.459, -0.178, -0.171, 0.073, 0.119, 0.190]

x = [0, 0.02, 0.035, 0.055, 0.07, 0.09, 0.105, 0.125, 0.14, 0.16, 0.18]
x2 = [0, 0.017, 0.045, 0.07, 0.097, 0.125, 0.150, 0.18]

# Función 
def project_new_value(data):
    diff = data[-1] - data[-2]
    return data[-1] + diff

new_Cp4deg_value = project_new_value(Cp4deg_Up)
new_Cp0deg_value = project_new_value(Cp0deg_Up)
new_CpNeg2deg_value = project_new_value(CpNeg2deg_Up)

Cp4deg_Up.append(new_Cp4deg_value)
Cp4deg_Bottom.append(new_Cp4deg_value)

Cp0deg_Up.append(new_Cp0deg_value)
Cp0deg_Bottom.append(new_Cp0deg_value)

CpNeg2deg_Up.append(new_CpNeg2deg_value)
CpNeg2deg_Bottom.append(new_CpNeg2deg_value)

print("Cp borde ataque: 4°:",Cp4deg_Up[10], "   0°:",Cp0deg_Up[10], "    -2°:",CpNeg2deg_Up[10])

plt.figure(figsize=(12, 8))
plt.plot(x, Cp4deg_Up, marker='o', linestyle='-', color='blue', label='Cp4deg_Up')
plt.plot(x2, Cp4deg_Bottom, marker='o', linestyle='-', color='red', label='Cp4deg_Bottom')
plt.xlabel('x/c')
plt.ylabel('Cp')
plt.title('Distribución de Cp a 4° de Ángulo de Ataque')
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 8))
plt.plot(x, Cp0deg_Up, marker='s', linestyle='--', color='green', label='Cp0deg_Up')
plt.plot(x2, Cp0deg_Bottom, marker='s', linestyle='--', color='orange', label='Cp0deg_Bottom')
plt.xlabel('x/c')
plt.ylabel('Cp')
plt.title('Distribución de Cp a 0° de Ángulo de Ataque')
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 8))
plt.plot(x, CpNeg2deg_Up, marker='^', linestyle=':', color='purple', label='CpNeg2deg_Up')
plt.plot(x2, CpNeg2deg_Bottom, marker='^', linestyle=':', color='pink', label='CpNeg2deg_Bottom')
plt.xlabel('x/c')
plt.ylabel('Cp')
plt.title('Distribución de Cp a -2° de Ángulo de Ataque')
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.show()
