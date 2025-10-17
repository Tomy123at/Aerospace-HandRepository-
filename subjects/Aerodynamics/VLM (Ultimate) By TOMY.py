import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Tabla_ISA_module

#VLM by: TOMY 

#----------------------------------
#Parámetros
S = 15
AR = 7
Landa_w = 1
A_LE = 0 #deg

##########################
n = 8
##########################

b = math.sqrt(S*AR)
c_root = 2*S/(b*(1+Landa_w))
c_tip = c_root*Landa_w
A_c4 = A_LE #Deg
A_3c4 = A_LE #Deg

#----------------------------------

#Superficie del ala
X_wing_s = np.zeros(5)
Y_wing_s = np.zeros(5)

X_wing_s[0] = 0
X_wing_s[1] = (b/2)*math.tan(math.radians(A_LE))
X_wing_s[2] = X_wing_s[1] + c_tip
X_wing_s[3] = c_root
X_wing_s[4] = 0
Y_wing_s[0] = 0
Y_wing_s[1] = b/2
Y_wing_s[2] = Y_wing_s[1]
Y_wing_s[3] = 0
Y_wing_s[4] = 0

#---------------------------------------------------------
#C/4
X_c4 = np.zeros(2)
Y_c4 = np.zeros(2)

X_c4[0] = c_root*1/4
X_c4[1] = (c_tip*1/4)+(math.tan(math.radians(A_LE))*b/2)
Y_c4[0] = 0 
Y_c4[1] = b/2

#3C/4
X_3c4 = np.zeros(2)
Y_3c4 = np.zeros(2)

X_3c4[0] = c_root*3/4
X_3c4[1] = (c_tip*3/4)+(math.tan(math.radians(A_LE))*b/2)
Y_3c4[0] = 0
Y_3c4[1] = b/2

#-------------------------------------------------------------
#Pendiente
def pendiente(x1, y1, x2, y2):
    if x2 != x1:  #No tocar pls
        pendiente = (y2 - y1) / (x2 - x1)
    else:
        return None  
    return pendiente

def pendiente1(x1, y1, x2, y2):
    if x2 != x1:  #No tocar pls
        pendiente = ((x2-x1)*(y2-y1))/((x2-x1)**2)
    else:
        return None  
    return pendiente

#Divisiones Horseshoe
X_HorseshoeDiv = np.zeros((n+1)*2)
Y_HorseshoeDiv = np.zeros((n+1)*2)

iter = 1
for i in range((n+1)*2):
    if i == 0:
        X_HorseshoeDiv[0] = X_c4[0]
        Y_HorseshoeDiv[0] = Y_c4[0]
    elif i == 1:
        X_HorseshoeDiv[1] = 1
        Y_HorseshoeDiv[1] = Y_c4[0]
    elif i == len(X_HorseshoeDiv)-2:
        X_HorseshoeDiv[i] = X_c4[1]
        Y_HorseshoeDiv[i] = Y_c4[1]
    elif i == len(X_HorseshoeDiv)-1:
        X_HorseshoeDiv[i] = 1
        Y_HorseshoeDiv[i] = Y_c4[1]
    elif i%2 == 0 and i!=0:
        Y_HorseshoeDiv[i] = ((b/2)/n)*iter
        if X_c4[0] == X_c4[1]:
            X_HorseshoeDiv[i] = c_root*1/4
        else:
            X_HorseshoeDiv[i] = (c_root*1/4) + pendiente1(Y_c4[0],X_c4[0],Y_c4[1],X_c4[1])*Y_HorseshoeDiv[i]
        iter = iter+1
    elif i%2 == 1 and i!=1:
        X_HorseshoeDiv[i] = 1
        Y_HorseshoeDiv[i] = Y_HorseshoeDiv[i-1]


#Puntos de control
X_controlpoint = np.zeros(n)
Y_controlpoint = np.zeros(n)

for i in range(n):
    Y_controlpoint[i] = ((Y_HorseshoeDiv[2]-Y_HorseshoeDiv[0])/2)*(((i+1)*2)-1)
    X_controlpoint[i] = pendiente(Y_3c4[0],X_3c4[0],Y_3c4[1],X_3c4[1])*Y_controlpoint[i]+((c_root*3/4))


#----------------------------------------------------------
#TABLA 
Panel = np.zeros(n)
xms = np.zeros(n)
yms = np.zeros(n)
x1ns = np.zeros(n)
y1ns = np.zeros(n)
x2ns = np.zeros(n)
y2ns = np.zeros(n)

xmp = np.zeros(n)
ymp = np.zeros(n)
x1np = np.zeros(n)
y1np = np.zeros(n)
x2np = np.zeros(n)
y2np = np.zeros(n)

for i in range(n):
    Panel[i] = i+1
    xms[i] = X_controlpoint[i]
    yms[i] = Y_controlpoint[i]
    x1ns[i] = X_HorseshoeDiv[i*2]
    y1ns[i] = Y_HorseshoeDiv[i*2]
    x2ns[i] = X_HorseshoeDiv[(i+1)*2]
    y2ns[i] = Y_HorseshoeDiv[(i+1)*2]


    xmp[i] = X_controlpoint[i]
    ymp[i] = -Y_controlpoint[i] #MAN, I HATE THE NEGATIVE
    x1np[i] = X_HorseshoeDiv[(i+1)*2] #IDK WHAT'S GOING ON
    y1np[i] = Y_HorseshoeDiv[(i+1)*2] #EMPIRICAL SOLUTION :)
    x2np[i] = X_HorseshoeDiv[i*2]
    y2np[i] = Y_HorseshoeDiv[i*2]

#DataFrame
tabla_s = pd.DataFrame({
    'Panel': Panel,
    'xm': xms,
    'ym': yms,
    'x1n': x1ns,
    'y1n': y1ns,
    'x2n': x2ns,
    'y2n': y2ns
})

tabla_p = pd.DataFrame({
    'Panel': Panel,
    'xm': xmp,
    'ym': ymp,
    'x1n': x1np,
    'y1n': y1np,
    'x2n': x2np,
    'y2n': y2np
})#By:Tomy

print(tabla_s)
print("-----------------------------------")
print(tabla_p)

#---------------------------------------------------------------
#MATRIZ
Comp_s = np.zeros((n,n))
Comp_p = np.zeros((n,n))
Comp = np.zeros((n,n))

for m in range(n):
    for u in range(n):
        Comp_s[m,u] = (1/((xms[m]-x1ns[u])*(yms[m]-y2ns[u])-(xms[m]-x2ns[u])*(yms[m]-y1ns[u])))*((((x2ns[u]-x1ns[u])*(xms[m]-x1ns[u])+(y2ns[u]-y1ns[u])*(yms[m]-y1ns[u]))/(math.sqrt(((xms[m]-x1ns[u])**(2))+(yms[m]-y1ns[u])**(2))))-(((x2ns[u]-x1ns[u])*(xms[m]-x2ns[u])+(y2ns[u]-y1ns[u])*(yms[m]-y2ns[u]))/(math.sqrt(((xms[m]-x2ns[u])**(2))+(yms[m]-y2ns[u])**2))))+(1/(y1ns[u]-yms[m]))*(1+((xms[m]-x1ns[u])/(math.sqrt(((xms[m]-x1ns[u])**(2))+(yms[m]-y1ns[u])**(2)))))-(1/(y2ns[u]-yms[m]))*(1+((xms[m]-x2ns[u])/(math.sqrt(((xms[m]-x2ns[u])**(2))+(yms[m]-y2ns[u])**(2)))))

for m in range(n):
    for u in range(n):
        Comp_p[m,u] = (1/((xmp[m]-x1np[u])*(ymp[m]-y2np[u])-(xmp[m]-x2np[u])*(ymp[m]-y1np[u])))*((((x2np[u]-x1np[u])*(xmp[m]-x1np[u])+(y2np[u]-y1np[u])*(ymp[m]-y1np[u]))/(math.sqrt(((xmp[m]-x1np[u])**(2))+(ymp[m]-y1np[u])**(2))))-(((x2np[u]-x1np[u])*(xmp[m]-x2np[u])+(y2np[u]-y1np[u])*(ymp[m]-y2np[u]))/(math.sqrt(((xmp[m]-x2np[u])**(2))+(ymp[m]-y2np[u])**2))))+(1/(y1np[u]-ymp[m]))*(1+((xmp[m]-x1np[u])/(math.sqrt(((xmp[m]-x1np[u])**(2))+(ymp[m]-y1np[u])**(2)))))-(1/(y2np[u]-ymp[m]))*(1+((xmp[m]-x2np[u])/(math.sqrt(((xmp[m]-x2np[u])**(2))+(ymp[m]-y2np[u])**(2)))))
        Comp_p[m,u] = -Comp_p[m,u] #Another empirical correction, I'm sleepy

#SUMA DE STARBOARD Y PORT
for i in range(n):
    for j in range(n):
        Comp[i,j] = Comp_s[i,j]+Comp_p[i,j]

print("------------------------------------")
print(Comp_s)
print("------------------------------------")
print(Comp_p)
print("------------------------------------")
print(Comp)
print("------------------------------------")

#------------------------------------------------------------
#Solucion del sistema de ecuaciones


Coeficientes = np.zeros(n)
for i in range(n):
    Coeficientes[i] = -1

Sol = np.linalg.solve(Comp,Coeficientes)
print(Sol)

#-------------------------------------------------------------
#Valor test de Lift
#================================
alphatest = math.radians(0.94)     ############## ////////////// AoA
V = 125/1.944 #m/s
T,P,rho,avel = Tabla_ISA_module.Temp_Presion_Densidad(9000/3.281) 
q = (1/2)*rho*V**2
#================================

Sol_Sum = 0
for i in range(n):
    Sol_Sum = Sol_Sum + Sol[i]
ValueCond = 2*rho*(V**2)*4*math.pi*b*y2ns[0]
Ltest = ValueCond*Sol_Sum*alphatest

print(Sol_Sum)
print("------------------------------------")
print(Ltest, "N")
print("------------------------------------")

CLtest = Ltest/(q*S)
print(CLtest)

#-------------------------------------------------------------
#CL vs Angle (Here comes the good thing :D, I'm SOOOO SLEEEPY)
angles = 10 #Sin contar a=0 ##################################
alpha = np.zeros(angles+1)
Lift = np.zeros(angles+1)
CL = np.zeros(angles+1)

for i in range(angles+1):
    alpha[i] = i+0.94
    Lift[i] = ValueCond*Sol_Sum*math.radians(alpha[i])
    CL[i] = Lift[i]/(q*S)



# Exportar tabla_s a Excel
tabla_s.to_excel('tabla_superficie.xlsx', index=False)

# Exportar ángulos de ataque y CL a Excel
df_angles_cl = pd.DataFrame({
    'Alpha (degrees)': alpha,
    'CL': CL
})
df_angles_cl.to_excel('alpha_vs_cl.xlsx', index=False)

# Exportar matriz Comp a Excel
df_comp = pd.DataFrame(Comp)
df_comp.to_excel('matriz_comp.xlsx', index=False, header=False)

# Exportar resultados de circulación (Sol) a Excel
df_sol = pd.DataFrame({
    'Panel': Panel,
    'Circulación': Sol
})
df_sol.to_excel('resultados_circulacion.xlsx', index=False)













#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#Graficas (Gracias a CHATGPT :D)
# Parámetros del ala
X_wing_s = np.array([0, (b/2)*math.tan(math.radians(A_LE)), (b/2)*math.tan(math.radians(A_LE)) + c_tip, c_root, 0])
Y_wing_s = np.array([0, b/2, b/2, 0, 0])

# Gráfica del ala sin puntos
plt.figure()
plt.plot(X_wing_s, Y_wing_s, '-', color='black', label='Contorno del ala')  # Solo líneas

# Añadir líneas de C/4 y 3C/4
plt.plot(X_c4, Y_c4, '--', color='blue', label='C/4')  # Línea discontinua azul para C/4
plt.plot(X_3c4, Y_3c4, '--', color='red', label='3C/4')  # Línea discontinua roja para 3C/4

# Añadir divisiones Horseshoe
for i in range(0, len(X_HorseshoeDiv), 2):
    plt.plot([X_HorseshoeDiv[i], X_HorseshoeDiv[i+1]], 
             [Y_HorseshoeDiv[i], Y_HorseshoeDiv[i+1]], 
             '--', color='blue')  # Mismo color y estilo que C/4

# Añadir puntos de control
plt.scatter(X_controlpoint, Y_controlpoint, color='green', zorder=5, label='Puntos de control')  # Puntos verdes

# Ajustes de la gráfica
plt.fill(X_wing_s, Y_wing_s, 'lightblue', alpha=0.6)  # Sombreado azul claro
plt.title('Contorno del ala con C/4, 3C/4, divisiones Horseshoe y puntos de control')
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.grid(True)
plt.axis('equal')
plt.legend()

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

#-----------------------------------------------------------------
# Graficar Lift vs Alpha
axs[0].plot(alpha, Lift, 'b-', marker='o', label='Lift vs Alpha')
axs[0].set_title('Lift vs Alpha')
axs[0].set_xlabel('Alpha [°]')
axs[0].set_ylabel('Lift [N]')
axs[0].grid(True)
axs[0].legend()

# Graficar Cl vs Alpha
axs[1].plot(alpha, CL, 'r-', marker='o', label='Cl vs Alpha')
axs[1].set_title('Cl vs Alpha')
axs[1].set_xlabel('Alpha [°]')
axs[1].set_ylabel('Cl')
axs[1].grid(True)
axs[1].legend()
#By: Tomy
# Ajustar la presentación de las gráficas
plt.tight_layout()

#-------------------------------------------------------------------------------
# Definir las coordenadas en el espacio 3D (Z se mantiene en cero)
Z_wing_s = np.zeros(len(X_wing_s))  # El ala está en el plano Z=0
Z_c4 = np.zeros(len(X_c4))
Z_3c4 = np.zeros(len(X_3c4))
Z_HorseshoeDiv = np.zeros(len(X_HorseshoeDiv))
Z_controlpoint = np.zeros(len(X_controlpoint))

# Calcular el lift en cada punto de control
Lift_vectors = np.zeros(n)
for i in range(n):
    Lift_vectors[i] = (ValueCond/2) * Sol[i] * alphatest

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''#"#"###"#"#"#"#""
# Crear figura en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Ajustar las coordenadas Z para que el ala esté en Z=0
Z_wing_s = np.zeros(len(X_wing_s))
Z_c4 = np.zeros(len(X_c4))
Z_3c4 = np.zeros(len(X_3c4))
Z_HorseshoeDiv = np.zeros(len(X_HorseshoeDiv))
Z_controlpoint = np.zeros(len(X_controlpoint))

# Graficar contorno del ala derecha (en Z=0)
ax.plot(X_wing_s, Y_wing_s, Z_wing_s, '-', color='black', label='Contorno del ala derecha')

# Graficar línea de C/4 de la ala derecha (en Z=0)
ax.plot(X_c4, Y_c4, Z_c4, '--', color='blue', label='C/4 derecha')

# Graficar línea de 3C/4 de la ala derecha (en Z=0)
ax.plot(X_3c4, Y_3c4, Z_3c4, '--', color='red', label='3C/4 derecha')

# Graficar divisiones Horseshoe de la ala derecha (en Z=0)
for i in range(0, len(X_HorseshoeDiv), 2):
    ax.plot([X_HorseshoeDiv[i], X_HorseshoeDiv[i+1]], 
            [Y_HorseshoeDiv[i], Y_HorseshoeDiv[i+1]], 
            [Z_HorseshoeDiv[i], Z_HorseshoeDiv[i+1]], 
            '--', color='blue')

# Graficar puntos de control de la ala derecha (en Z=0)
ax.scatter(X_controlpoint, Y_controlpoint, Z_controlpoint, color='green', label='Puntos de control derecha', zorder=5)

# Añadir vectores de lift de la ala derecha
for i in range(n):
    ax.quiver(X_controlpoint[i], Y_controlpoint[i], Z_controlpoint[i], 
              0, 0, Lift_vectors[i], color='orange', label='Lift vector derecha' if i == 0 else "", arrow_length_ratio=0.1)

# Graficar contorno del ala izquierda (espejado respecto al eje Y)
X_wing_s_left = X_wing_s
Y_wing_s_left = -Y_wing_s
X_c4_left = X_c4
Y_c4_left = -Y_c4
X_3c4_left = X_3c4
Y_3c4_left = -Y_3c4
X_HorseshoeDiv_left = X_HorseshoeDiv
Y_HorseshoeDiv_left = -Y_HorseshoeDiv
X_controlpoint_left = X_controlpoint
Y_controlpoint_left = -Y_controlpoint

# Graficar ala izquierda
ax.plot(X_wing_s_left, Y_wing_s_left, Z_wing_s, '-', color='black', linestyle='--', label='Contorno del ala izquierda')
ax.plot(X_c4_left, Y_c4_left, Z_c4, '--', color='blue', linestyle='--', label='C/4 izquierda')
ax.plot(X_3c4_left, Y_3c4_left, Z_3c4, '--', color='red', linestyle='--', label='3C/4 izquierda')

# Graficar divisiones Horseshoe de la ala izquierda
for i in range(0, len(X_HorseshoeDiv_left), 2):
    ax.plot([X_HorseshoeDiv_left[i], X_HorseshoeDiv_left[i+1]], 
            [Y_HorseshoeDiv_left[i], Y_HorseshoeDiv_left[i+1]], 
            [Z_HorseshoeDiv[i], Z_HorseshoeDiv[i+1]], 
            '--', color='blue')

# Graficar puntos de control de la ala izquierda
ax.scatter(X_controlpoint_left, Y_controlpoint_left, Z_controlpoint, color='green', marker='^', label='Puntos de control izquierda', zorder=5)

# Añadir vectores de lift de la ala izquierda
for i in range(n):
    ax.quiver(X_controlpoint_left[i], Y_controlpoint_left[i], Z_controlpoint[i], 
              0, 0, Lift_vectors[i], color='orange', linestyle='--', label='Lift vector izquierda' if i == 0 else "", arrow_length_ratio=0.1)

# Añadir sombreado para la ala derecha
ax.plot_trisurf(X_wing_s, Y_wing_s, Z_wing_s, color='lightblue', alpha=0.6, linewidth=0)

# Añadir sombreado para la ala izquierda
ax.plot_trisurf(X_wing_s, Y_wing_s_left, Z_wing_s, color='lightblue', alpha=0.6, linewidth=0)

# Calcular el mayor rango entre X e Y para establecer proporciones iguales
max_range = max(max(abs(X_wing_s)), max(abs(Y_wing_s)), b/2)

# Ajustar el rango de los ejes X y Y para que tengan el mismo tamaño
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])

# Ajustar el rango del eje Z para ser el doble del lift máximo
ax.set_zlim(0, 2 * max(Lift_vectors))

# Proporción de los ejes X e Y iguales, pero permitir que el eje Z tenga su propia escala
ax.set_box_aspect([1, 1, 0.5])  # Relación 1:1 para X:Y y 0.5 para el Z

# Etiquetas y título
ax.set_title(f'Alas en 3D con C/4, 3C/4, divisiones Horseshoe, puntos de control y vectores de Lift a {math.degrees(alphatest):.2f}°')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Lift [N]')  # Etiqueta del eje Z representando el lift

# Ajustes adicionales
ax.legend()
plt.grid(True)

plt.show()
