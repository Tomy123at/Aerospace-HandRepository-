import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Colores predefinidos
predefined_colors = ['#0000FF', '#FF0000', '#FFFF00', '#00FF00', '#800080', '#FFA500', '#FFC0CB', '#000000', '#8B4513', '#ADD8E6']

def load_xfoil_csv(filepath):
    df = pd.read_csv(filepath, skiprows=0)
    return df

def select_files():
    Tk().withdraw()  # Para ocultar la ventana
    filepaths = askopenfilename(multiple=True, title="Selecciona archivos XFOIL (CSV)")
    return filepaths


def plot_data(dfs, labels, colors):
    for ax in axs.flat:
        ax.clear()

    for i, (df, label) in enumerate(zip(dfs, labels)):
        alpha = df['Alpha']
        Cl = df['Cl']
        Cd = df['Cd']
        Cm = df['Cm']

        color = colors[i % len(colors)] 

        axs[0, 0].plot(Cd, Cl, label=label, color=color)
        axs[0, 1].plot(alpha, Cl, label=label, color=color)
        axs[0, 2].plot(alpha, Cl/Cd, label=label, color=color)
        axs[1, 0].plot(alpha, Cd, label=label, color=color)
        axs[1, 1].plot(alpha, Cm, label=label, color=color)

    axs[0, 0].set_xlabel('Cd')
    axs[0, 0].set_ylabel('Cl')
    axs[0, 0].set_title('Cl vs Cd')
    axs[0, 0].legend()

    axs[0, 1].set_xlabel('Alpha (°)')
    axs[0, 1].set_ylabel('Cl')
    axs[0, 1].set_title('Cl vs Alpha')
    axs[0, 1].legend()

    axs[0, 2].set_xlabel('Alpha (°)')
    axs[0, 2].set_ylabel('Cl/Cd')
    axs[0, 2].set_title('Cl/Cd vs Alpha')
    axs[0, 2].legend()

    axs[1, 0].set_xlabel('Alpha (°)')
    axs[1, 0].set_ylabel('Cd')
    axs[1, 0].set_title('Cd vs Alpha')
    axs[1, 0].legend()

    axs[1, 1].set_xlabel('Alpha (°)')
    axs[1, 1].set_ylabel('Cm')
    axs[1, 1].set_title('Cm vs Alpha')
    axs[1, 1].legend()

    for ax in axs.flat[5:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.draw()

# Función para añadir nuevos archivos
def add_csv(event):
    new_filepaths = select_files()
    if not new_filepaths:
        return
    
    new_dfs = [load_xfoil_csv(filepath) for filepath in new_filepaths]
    new_labels = [f"Perfil {i+1+len(labels)} ({filepath.split('/')[-1]})" for i, filepath in enumerate(new_filepaths)]
    
    global colors
    new_colors = predefined_colors[len(colors):len(colors) + len(new_dfs)]  

    dfs.extend(new_dfs)
    labels.extend(new_labels)
    colors.extend(new_colors) 
    
    plot_data(dfs, labels, colors)

fig, axs = plt.subplots(2, 3, figsize=(14, 8))

dfs = []
labels = []
colors = []

filepaths = select_files()

dfs = [load_xfoil_csv(filepath) for filepath in filepaths]
labels = [f"Perfil {i+1} ({filepath.split('/')[-1]})" for i, filepath in enumerate(filepaths)]
colors = predefined_colors[:len(dfs)]  

# Grafica los datos
plot_data(dfs, labels, colors)

add_button_ax = plt.axes([0.75, 0.02, 0.2, 0.05])
add_button = plt.Button(add_button_ax, 'Añadir CSV')
add_button.on_clicked(add_csv)

plt.show()
