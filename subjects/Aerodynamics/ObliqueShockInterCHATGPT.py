import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.optimize import fsolve

# Función theta-beta-Mach
def theta_beta_mach(beta, M1, gamma):
    term1 = 2 * (1 / np.tan(beta))
    term2 = ((M1**2 * np.sin(beta)**2 - 1) / (M1**2 * (gamma + np.cos(2 * beta)) + 2))
    return np.arctan(term1 * term2)

# Función para calcular el valor faltante
def obtener_valor_faltante(valor1, valor2, variable_faltante, gamma=1.4):
    if variable_faltante == 'theta':
        beta, M1 = valor1, valor2
        return theta_beta_mach(beta, M1, gamma)
    elif variable_faltante == 'beta':
        theta, M1 = valor1, valor2
        func = lambda beta: theta_beta_mach(beta, M1, gamma) - theta
        beta_sol = fsolve(func, np.radians(10))  # Valor inicial en radianes
        return np.degrees(beta_sol[0])  # Convertir de radianes a grados
    elif variable_faltante == 'M1':
        theta, beta = valor1, np.radians(valor2)
        func = lambda M1: theta_beta_mach(beta, M1, gamma) - theta
        M1_sol = fsolve(func, 2)  # Valor inicial para M1
        return M1_sol[0]
    else:
        raise ValueError("Variable faltante debe ser 'theta', 'beta' o 'M1'.")

# Función para manejar el cálculo desde la interfaz
def calcular():
    try:
        valor1 = float(entry_valor1.get())
        valor2 = float(entry_valor2.get())
        variable_faltante = variable_var.get()

        if variable_faltante == 'theta':
            resultado = obtener_valor_faltante(np.radians(valor1), valor2, 'theta')
            resultado = f"{np.degrees(resultado):.4f} grados"
        elif variable_faltante == 'beta':
            resultado = obtener_valor_faltante(np.radians(valor1), valor2, 'beta')
            resultado = f"{resultado:.4f} grados"
        elif variable_faltante == 'M1':
            resultado = obtener_valor_faltante(np.radians(valor1), valor2, 'M1')
            resultado = f"{resultado:.4f}"
        else:
            raise ValueError("Selecciona una variable válida para calcular.")
        
        messagebox.showinfo("Resultado", f"El valor de {variable_faltante} es: {resultado}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Configuración de la interfaz de usuario
root = tk.Tk()
root.title("Cálculo de Theta-Beta-Mach")

# Variables
variable_var = tk.StringVar(value="theta")

# Widgets
tk.Label(root, text="Seleccione la variable que desea calcular: (theta, beta, MACH)").grid(row=0, column=0, columnspan=2)
tk.Radiobutton(root, text="Theta", variable=variable_var, value="theta").grid(row=1, column=0)
tk.Radiobutton(root, text="Beta", variable=variable_var, value="beta").grid(row=1, column=1)
tk.Radiobutton(root, text="Mach (M1)", variable=variable_var, value="M1").grid(row=1, column=2)

tk.Label(root, text="Valor 1:").grid(row=2, column=0)
entry_valor1 = tk.Entry(root)
entry_valor1.grid(row=2, column=1)

tk.Label(root, text="Valor 2:").grid(row=3, column=0)
entry_valor2 = tk.Entry(root)
entry_valor2.grid(row=3, column=1)

tk.Button(root, text="Calcular", command=calcular).grid(row=4, column=0, columnspan=2)

# Iniciar la interfaz
root.mainloop()
