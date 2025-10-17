import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

#Atmospheric Data
Humidity = 100  #%
P = 101727.12  #Pa
Visc = 1.823 * 10**(-5)
R = 287
Rho = 1.201  #Kg/m3

#Flight condition
AoA = 3  # Deg
V = 7  # m/s
q = (1 / 2) * Rho * V**2

#Wing initial Geometry
Landa = 1
AR = 7.5

#Wing parameters
a0 = 0.099
a = a0 / (1 + (a0 / math.pi * AR))
aL0 = -3.339  #Deg
aa = AoA - aL0
CL = a * (AoA - aL0)
CMacwb = -0.1023

#Tail parameters
lt = 4 * (S := (1 * 9.81) / (q * CL))  
at = 0.0644047966379471
aL0t = 0

#General Parameters
epsilon0 = (2 * CL) / math.pi * AR
deda = (2 * math.degrees(a)) / (math.pi * AR)
hacwb = 0.25

angles = np.arange(-2, 10.5, 0.5)
St_values = np.arange(0.05, 0.45, 0.05)

it = 2

fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.3)
line, = ax.plot([], [], label='Current Graph', marker='o')
ax.set_title('CMcg vs AoA')
ax.set_xlabel('AoA (degrees)')
ax.set_ylabel('CMcg')
ax.grid(True)
ax.set_xlim(-2, 10)
ax.set_ylim(-0.6, 0.6)

#Slider for it
ax_it = plt.axes([0.1, 0.2, 0.65, 0.03])
slider_it = Slider(ax_it, 'it (deg)', -5, 5, valinit=it)

#Slider for St
ax_st = plt.axes([0.1, 0.15, 0.65, 0.03])
slider_st = Slider(ax_st, 'St (m²)', 0.05, 0.4, valinit=0.115, valstep=0.01)

#Save
ax_save = plt.axes([0.8, 0.2, 0.1, 0.04])
btn_save = Button(ax_save, 'Save Graph')

#Update
def update(val):
    it = slider_it.val
    St = slider_st.val

    bt = math.sqrt((AR / 2) * St)
    ct = St / bt
    VH = St * lt / (bt * S)

    hn = 0.25 + VH * (at / a) * (1 - deda)
    h = ((hn - hacwb) / 2) + hacwb
    SM = hn - h

    dCMcgdaa = a * (h - hacwb - VH * (at / a) * (1 - deda))
    epsilon = epsilon0 + deda * math.radians(aa)

    CM0 = CMacwb + VH * at * (it + epsilon0)
    aeq = -CM0 / dCMcgdaa
    ageo = aeq + aL0
    CLageo = a * (ageo - aL0)

    CMcgvalues = dCMcgdaa * angles + CM0

    line.set_xdata(angles)
    line.set_ydata(CMcgvalues)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

def save_graph(event):
    plt.savefig('saved_graph.png')
    print("Graph saved as 'saved_graph.png'")

slider_it.on_changed(update)
slider_st.on_changed(update)
btn_save.on_clicked(save_graph)

update(None)

plt.show()
