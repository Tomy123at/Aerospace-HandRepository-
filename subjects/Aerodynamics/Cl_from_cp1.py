import numpy as np
from scipy.integrate import quad
import pandas as pd
import matplotlib.pyplot as plt

v_inf = 53.20 # m/s
rho_inf = 1.07376 # kg/m^3
alpha = 3.4 # grados
q_inf = (1/2) * rho_inf * (v_inf)**2
c = 0.18

file = r'C:\Users\tomya\OneDrive\Documentos\Universidad\2024-2\Aerodinámica\resultados_presion.txt'
data_file = pd.read_csv(file, delim_whitespace=True, header=None)

x = data_file[0].to_numpy().astype(float)
cp_u = data_file[1].to_numpy().astype(float)
cp_l = data_file[2].to_numpy().astype(float)

x = x / 1000
x = x / c


x_interpol = np.linspace(min(x), max(x), 1000)
cp_u_interp = np.interp(x_interpol, x, cp_u)
cp_l_interp = np.interp(x_interpol, x, cp_l)


def deltacp(x_integral):
    cp_u_val = np.interp(x_integral, x_interpol, cp_u_interp)
    cp_l_val = np.interp(x_integral, x_interpol, cp_l_interp)
    return cp_l_val - cp_u_val


Cn, error = quad(deltacp, 0, c)
print()
print("--------------------------------------------------------------------")
print("El coeficiente de sustentación es", round(Cn, 3))
print("--------------------------------------------------------------------")
print()


plt.scatter(x, cp_u, color='red', label='Datos Cp_u')
plt.scatter(x, cp_l, color='red', label='Datos Cp_l')
plt.plot(x_interpol, cp_u_interp, color='blue', label='Interpolación Cp_u')
plt.plot(x_interpol, cp_l_interp, color='green', label='Interpolación Cp_l')
plt.xlabel('x')
plt.ylabel('Cp')
plt.legend()
plt.title('Cp vs x')
plt.gca().invert_yaxis()
plt.show()
