import numpy as np
import matplotlib.pyplot as plt

gamma = 1.4
mach_values = [1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.4, 3.6, 3.8, 4, 4.5, 5, 6, 8, 10, 20, 999999]

beta = np.linspace(0.01, np.radians(90), 500)  
theta_values = np.linspace(0, np.radians(50), 500)  

def theta_beta_mach(beta, M1, gamma):
    term1 = 2 * (1 / np.tan(beta)) #mero rato intentando sacar cotangente pero resulta que es 1/tan :| 
    term2 = ((M1**2 * np.sin(beta)**2 - 1) / (M1**2 * (gamma + np.cos(2 * beta)) + 2))
    return np.arctan(term1 * term2)

# Crear matrices para almacenar los valores de theta y beta
theta_matrix = []
beta_matrix = []

for M1 in mach_values:
    theta = theta_beta_mach(beta, M1, gamma)
    theta_deg = np.degrees(theta)
    beta_deg = np.degrees(beta)
    theta_matrix.append(theta_deg)
    beta_matrix.append(beta_deg)

plt.figure(figsize=(10, 8)) #Grafico esa vaina mach por mach ezzzzz
for i in range(len(mach_values)):
    plt.plot(theta_matrix[i], beta_matrix[i], label=f'M={mach_values[i]}')

#Gracias a chatgpt tenemos esta hermosa gráfica (:D)
plt.plot(np.max(theta_matrix, axis=1), beta_matrix[np.argmax(np.max(theta_matrix, axis=1))], 'k--', label='Máximo de θ')

# Configurar el gráfico
plt.xlim(0, 50)
plt.ylim(0, 90)
plt.xlabel(r'$\theta$ (Deflection Angle, degrees)')
plt.ylabel(r'$\beta$ (Wave Angle, degrees)')
plt.title(r'Relación $\theta$-$\beta$-M para ondas de choque oblicuas')
plt.legend(loc='upper right', fontsize='small')
plt.grid(True)
plt.show()
