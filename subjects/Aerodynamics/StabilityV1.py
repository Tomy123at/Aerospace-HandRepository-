import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#Atmospheric Data
Humidity = 100 #%
P = 101727.12 #Pa
Visc = 1.823*10**(-5)
R = 287
Rho = 1.201 #Kg/m3

#Flight condition
AoA = 3 #Deg
V = 7 #m/s
q = (1/2)*Rho*V**2


#Wing initial Geometry 
Landa = 1
AR = 7.5

#Wing parameters
a0 = 0.099
a = a0/(1+(a0/math.pi*AR))
aL0 = -3.339 #Deg
aa = AoA-aL0
CL = a*(AoA-aL0)
CMacwb = -0.1023

#Wing final Geometry -------------------
S = (1*9.81)/(q*CL) #m2
#S = 0.657085281
b = math.sqrt(AR*S) #m
c = S/b #m

#Tail parameters
lt = 4*c
at = 0.0644047966379471
aL0t = 0
it = 2 #Deg


#General Parameters
VH = 0.7
epsilon0 = (2*CL)/math.pi*AR
deda = (2*math.degrees(a))/(math.pi*AR)
hacwb = 0.25
hn = 0.25+VH*(at/a)*(1-deda)
h = ((hn-hacwb)/2)+hacwb
SM = hn-h
dCMcgdaa = a*(h-hacwb-VH*(at/a)*(1-deda))
epsilon = epsilon0+deda*math.radians(aa)


#Tail Geometry 
Landat = 1
ARt = AR/2 
St = (VH*c*S)/lt
bt = math.sqrt(ARt*St)
ct = St/bt

#Wing Parameters Final --------------------------
CM0 = CMacwb+VH*at*(it+epsilon0)
aeq = -CM0/dCMcgdaa
ageo = aeq+aL0
CLageo = a*(ageo-aL0)
L = (q*S*CLageo)/9.81


#Tail Parameters Final
ai = aa-it-epsilon

#CMcg
CMcg = CMacwb+aa*a*(h-hacwb-VH*(at/a)*(1-deda))+VH*at*(it+epsilon0)


angles = np.arange(-2, 10.5, 0.5)
CMcgvalues = []

for i in range(len(angles)):
    CMcgvalues.append(dCMcgdaa * angles[i] + CM0)


plt.figure(figsize=(8, 6))
plt.plot(angles, CMcgvalues, label='CMcg vs AoA', marker='o', color='b')

plt.text(0, min(CMcgvalues), f'dCMcg/dAa = {dCMcgdaa:.4f}', fontsize=12, color='red')
plt.text(0, min(CMcgvalues) + 0.02, f'CM0 = {CM0:.4f}', fontsize=12, color='green')

plt.title('CMcg vs AoA')
plt.xlabel('AoA (degrees)')
plt.ylabel('CMcg')
plt.grid(True)
plt.legend()
plt.show()

