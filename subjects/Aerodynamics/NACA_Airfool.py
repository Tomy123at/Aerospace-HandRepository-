import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def symetrical(zmax, xz_max, tt, t_max):
    dx = 0.005
    c = 1
    ran = int(c/dx)
    x = np.arange(0, 1, dx)
    yu = np.zeros_like(x)
    yl = np.zeros_like(x)
    for i in range(0, ran):
        yu[i] = (t_max/0.2)*(0.2969*(x[i]/c)**(1/2) - 0.126*(x[i]/c) - 0.3516*(x[i]/c)**2 + 0.2843*(x[i]/c)**3 - 0.1015*(x[i]/c)**4)
    yl = -yu
    return x, yu, yl

def assymetrical(zmax, xz_max, tt, t_max):
    dx = 0.005
    c = 1
    ran = int(c/dx)
    x = np.arange(0, 1, dx)
    yu = np.zeros_like(x)
    yl = np.zeros_like(x)
    z = np.zeros_like(x)
    zmax = zmax / 100
    xz_max = xz_max / 10
    tt = tt / 100
    range2 = int(ran * xz_max)
    
    # Primera parte de z(x)
    print(f"Primera parte de z(x) para 0 <= x < {xz_max}:")
    print(f"z(x) = {zmax:.4f} * (x / {xz_max**2:.4f}) * (2 * {xz_max:.4f} - x)\n")
    
    for i in range(0, range2):
        z[i] = zmax * (x[i] / (xz_max**2)) * (2 * xz_max - (x[i] / c))

    # Segunda parte de z(x)
    print(f"Segunda parte de z(x) para {xz_max} <= x <= 1:")
    print(f"z(x) = {zmax:.4f} * ((1 - x) / {(1 - xz_max)**2:.4f}) * (1 + x - 2 * {xz_max:.4f})\n")
    
    for i in range(range2, ran):
        z[i] = zmax * ((c - x[i]) / ((1 - xz_max)**2)) * (1 + (x[i] / c) - 2 * xz_max)
    
    # Cálculo de yu y yl (sin cambios)
    a = np.zeros_like(x)
    f = np.zeros_like(x)
    g = np.zeros_like(x)
    h = np.zeros_like(x)
    II = np.zeros_like(x)

    for i in range(0, ran):
        a[i] = 1.4845 * (x[i] / c)**(1/2)
        f[i] = 0.63 * (x[i] / c)
        g[i] = 1.758 * (x[i] / c)**2
        h[i] = 1.4215 * (x[i] / c)**3
        II[i] = 0.5075 * (x[i] / c)**4

    gamma_u = np.zeros_like(x)
    gamma_l = np.zeros_like(x)

    for i in range(0, ran):
        gamma_u[i] = t_max * (a[i] - f[i] - g[i] + h[i] - II[i])
        gamma_l[i] = -t_max * (a[i] - f[i] - g[i] + h[i] - II[i])

    for i in range(0, ran):
        yu[i] = z[i] + gamma_u[i]
        yl[i] = z[i] + gamma_l[i]

    return x, yu, yl, z

def plot_naca():
    code = int(entry_code.get())
    zmax = int(str(code)[0])
    xz_max = int(str(code)[1])
    tt = code % 100
    t_max = float(entry_thickness.get())

    if zmax == 0 and xz_max == 0:
        x, yu, yl = symetrical(zmax, xz_max, tt, t_max)
    else:
        x, yu, yl, z = assymetrical(zmax, xz_max, tt, t_max)

    fig, ax = plt.subplots()
    ax.plot(x, yu, 'b')
    ax.plot(x, yl, 'b')
    ax.plot(x, z, 'r')
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'NACA {code}')
    
    
    for widget in frame_plot.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("GRAFICADORA PERFILES NACA (4 DÍGITOS)")

frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_code = ttk.Label(frame_input, text="Ingrese el código NACA:")
label_code.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_code = ttk.Entry(frame_input)
entry_code.grid(row=0, column=1, pady=5)

label_thickness = ttk.Label(frame_input, text="Ingrese el máximo espesor:")
label_thickness.grid(row=1, column=0, sticky=tk.W, pady=5)

entry_thickness = ttk.Entry(frame_input)
entry_thickness.grid(row=1, column=1, pady=5)

button_plot = ttk.Button(frame_input, text="Graficar", command=plot_naca)
button_plot.grid(row=2, column=0, columnspan=2, pady=10)

frame_plot = ttk.Frame(root, padding="10")
frame_plot.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
