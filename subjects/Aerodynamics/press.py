import numpy as np
import pandas as pd

# Datos de entrada
P_inf = 86438.42  # Pa
T = 280.49  # K
R = 287  # J/(kg·K)
densidad = 1.07376  # kg/m^3
pressure_leading_edge = 0.9804 * P_inf

# Velocidades locales medidas (x en cm)
x_cm = np.array([0, 4.0, 17.0, 22.0, 25.0, 27.0, 28.0, 35.0, 52.0, 71.0, 90.0, 99.0, 108.0, 117.0, 126.0, 135.0, 144.0, 153.0, 162.0, 171.0, 180.0])
v_l = np.array([0, 91.20, 90.92, 85.23, 81.87, 80.95, 80.55, 79.82, 78.12, 76.35, 74.52, 73.02, 71.82, 70.32, 68.35, 64.98, 62.32, 59.21, 57.25, 55.80, 53.20])
v_u = np.array([0, 45.32, 54.75, 55.82, 55.96, 56.02, 56.15, 56.53, 56.68, 56.76, 56.81, 56.91, 56.98, 56.06, 55.85, 55.76, 55.65, 55.54, 55.48, 55.34, 53.20])

# Convertir x a milímetros
x_mm = x_cm*100

# Velocidad de referencia (aproximación inicial como la media de las velocidades iniciales)
V_inf = v_l[0]

# Calcular las presiones usando la ecuación de Bernoulli
P_l = pressure_leading_edge + 0.5 * densidad * (V_inf**2 - v_l**2)
P_u = pressure_leading_edge + 0.5 * densidad * (V_inf**2 - v_u**2)

# Calcular las diferencias de presión
delta_P_u = P_u - P_inf
delta_P_l = P_l - P_inf

# Crear un DataFrame para mostrar los resultados
resultados = pd.DataFrame({
    'x (mm)': x_mm,
    'P_u - P_inf (Pa)': delta_P_u,
    'P_l - P_inf (Pa)': delta_P_l
})

# Imprimir el DataFrame en un archivo de texto
output_file = 'resultados_presion.txt'
resultados.to_csv(output_file, sep='\t', index=False, header=True)

print(f"Resultados guardados en {output_file}")
