import numpy as np
import matplotlib.pyplot as plt

# Datos proporcionados
x = [0, 0.02, 0.035, 0.055, 0.07, 0.09, 0.105, 0.125, 0.14, 0.16, 0.18]
x2 = [0, 0.017, 0.045, 0.07, 0.097, 0.125, 0.150, 0.18]
deltapu = [1.124, -0.647, -0.506, -0.445, -0.421, -0.343, -0.249, -0.079, 0.000, 0.149, 0.298]
deltapl = [1.124, 0.23, 0, 0.23, 0.3, 0.27, 0.261, 0.298]

# Ajuste polinómico de grados especificados
degree_pu = 7
degree_pl = 5
coeffs_pu = np.polyfit(x, deltapu, degree_pu)
coeffs_pl = np.polyfit(x2, deltapl, degree_pl)

# Crear funciones a partir de los coeficientes
poly_pu = np.poly1d(coeffs_pu)
poly_pl = np.poly1d(coeffs_pl)

# Integrar las funciones polinómicas
integral_pu = np.polyint(poly_pu)
integral_pl = np.polyint(poly_pl)

# Evaluar las integrales en los límites 0 y 0.18
integral_pu_0 = np.polyval(integral_pu, 0)
integral_pu_18 = np.polyval(integral_pu, 0.18)

integral_pl_0 = np.polyval(integral_pl, 0)
integral_pl_18 = np.polyval(integral_pl, 0.18)

# Calcular la diferencia de las integrales
difference_integral = (integral_pl_18 - integral_pl_0) - (integral_pu_18 - integral_pu_0)

# Multiplicar por el factor 1/0.18
result = (1 / 0.18) * difference_integral

print("Resultado de la integral:", result)

# Imprimir las ecuaciones de las funciones
def format_poly_coefficients(coeffs):
    terms = []
    degree = len(coeffs) - 1
    for i, coeff in enumerate(coeffs):
        power = degree - i
        if coeff != 0:
            term = f"{coeff:.6e}"
            if power > 0:
                term += f"*x^{power}"
            terms.append(term)
    equation = " + ".join(terms).replace("x^1 ", "x ").replace("1*x^", "x^")
    return equation

equation_pu = format_poly_coefficients(coeffs_pu)
equation_pl = format_poly_coefficients(coeffs_pl)

print("\nEcuación del polinomio para (p-p∞)u:")
print(equation_pu)
print("\nEcuación del polinomio para (p-p∞)l:")
print(equation_pl)

# Graficar resultados
x_fit = np.linspace(min(x), max(x), 100)
x_fit2 = np.linspace(min(x2), max(x2), 100)

y_fit_pu = poly_pu(x_fit)
y_fit_pl = poly_pl(x_fit2)

plt.figure(figsize=(12, 6))

# Graficar (p-p∞)u
plt.plot(x_fit, y_fit_pu, label='Ajuste polinómico (p-p∞)u', color='blue')
plt.scatter(x, deltapu, color='blue', marker='o', label='Datos (p-p∞)u')

# Graficar (p-p∞)l
plt.plot(x_fit2, y_fit_pl, label='Ajuste polinómico (p-p∞)l', color='red')
plt.scatter(x2, deltapl, color='red', marker='o', label='Datos (p-p∞)l')

# Configuración de gráficos
plt.xlabel('x [mm]')
plt.ylabel('Valores [Pa]')
plt.legend()
plt.title('Ajuste polinómico de (p-p∞)u y (p-p∞)l')
plt.gca().invert_yaxis()  # Invertir el eje y para que los valores negativos estén hacia arriba
plt.grid(True)
plt.tight_layout()

plt.show()
