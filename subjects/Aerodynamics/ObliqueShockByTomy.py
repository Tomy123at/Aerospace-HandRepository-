import numpy as np
import matplotlib.pyplot as plt


gamma = 1.4
mach_values = [1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.4, 3.6, 3.8, 4, 4.5, 5, 6, 8, 10, 20, 999999]
beta = np.linspace(0.01,np.radians(90),500)

# Funcion principal
#Hago las vainas por partes pa no equivocarme tan facil, el VLM ya me dejó traumado
def theta_beta_mach(beta,M1,gamma):
    term1 = 2 * (1/np.tan(beta)) 
    term2 = ((M1**2*np.sin(beta)**2-1)/(M1**2*(gamma + np.cos(2*beta))+2))
    return np.arctan(term1*term2)

#DOLOR DE CABEZA A LAS 12 AM DEL VIERNES ULTIMO DIA DE CLASEEEEE!!!!
def beta_separation_line(M1,gamma):
    term1 = M1**2*(gamma+1)+gamma-3
    term2 = 16*gamma
    term3 = 2*(M1**2-1)*(2+(gamma-1)*M1**2)
    
    tan2_beta_s = ((np.sqrt(term1**2+term2) + term1 + 4/(M1**2))/term3)*(M1**2)  #Ecuaciones sacadas del articulo salvador que encontré de apoyo
    beta_s = np.arctan(np.sqrt(tan2_beta_s))
    theta_s = theta_beta_mach(beta_s,M1,gamma)
    
    return np.degrees(theta_s), np.degrees(beta_s)


theta_s_values = []
beta_s_values = []
for M1 in mach_values: #Guardo los datos mijito
    theta_s, beta_s = beta_separation_line(M1,gamma)
    theta_s_values.append(theta_s)
    beta_s_values.append(beta_s)


# Valores maximos de theta
max_theta_values = []
beta_max_theta = []

# Esto es ezzzzzzz
plt.figure(figsize=(15, 8))
for M1 in mach_values:
    theta = theta_beta_mach(beta,M1,gamma)
    theta_deg = np.degrees(theta)
    beta_deg = np.degrees(beta)
    max_theta_index = np.argmax(theta_deg)

    # Gracias chatgpt
    plt.plot(theta_deg[:max_theta_index+1], beta_deg[:max_theta_index+1], label=f'M={M1}')
    plt.plot(theta_deg[max_theta_index:], beta_deg[max_theta_index:], 'k--', color=plt.gca().lines[-1].get_color())

    # Hay que guardar los datos parce
    max_theta = np.max(theta_deg)
    max_theta_values.append(max_theta)
    beta_max_theta.append(beta_deg[max_theta_index])

plt.plot(max_theta_values, beta_max_theta, 'k', linewidth=2, label='Máximo de θ')
plt.plot(theta_s_values, beta_s_values, 'k--', linewidth=2, label='Línea de separación $(\\theta_s, \\beta_s)$') #Linea de separacion = Linea del demonio

# Configurar el gráfico (Chatgpt otra vez)
plt.xlim(0, 50)
plt.ylim(0, 90)
plt.xlabel(r'$\theta$ (Deflection Angle, degrees)')
plt.ylabel(r'$\beta$ (Wave Angle, degrees)')
plt.title(r'Relación $\theta$-$\beta$-M para ondas de choque oblicuas')
plt.legend(loc='upper right', fontsize='small')
plt.grid(True)

plt.show()

