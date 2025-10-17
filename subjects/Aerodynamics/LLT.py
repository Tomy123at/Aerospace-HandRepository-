# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:42:42 2024

@author: garci
"""

# El siguiente codigo se realizó para el calculo de las caracteristicas aerodinámicas de un ala finita
# por el método LLT.
import numpy as np
import pandas as pd
import Tabla_ISA_module

# Parametros necesarios para los cálculos:
# Geometría del ala.5
bw = 3.37      # Embergadura del ala [m]
Croot = 0.958       # Cuerda de la raiz del ala [m]
Ctip = 0.958         # Cuerda de la punta del ala [m]
lambdaw = Ctip/Croot    # Taper ratio
Sw = (Croot + Ctip)*bw/2    # Área de la mitad del ala
AR = bw**2/Sw       # Acpect ratio
betaw = 0*np.pi/180      # Wing twist angle [deg]
htip = Ctip*np.sin(betaw)
AoA = np.radians(np.arange(-12, 12 + 1, 1))   # Vector  geometric Angle of attack [deg]
# Airfoil aerodynamics characteristics:
# Airfoil reference: Root: NACA 0015 Tip: NACA 0012
a0root = 6.54317802      # Root Lift slope [1/rad]
a0tip = 6.54317802       # Tip Lift slope [1/rad]
a0 =  6.54317802   # Lift slope [1/rad]
aL_0 = 0*np.pi/180   # Anfle of attack for L = 0 [deg]
aL_0_root = 0   # Root Anfle of attack for L = 0 [deg]
aL_0_tip = 0    # Tip Anfle of attack for L = 0 [deg]
#Cd_0 = np.arange()
# Flying (airflow) characteristics:
T,P,rho,avel = Tabla_ISA_module.Temp_Presion_Densidad(9000/3.281)
v = 125/1.944   # Air velocity [m/s]
# Procedure
N = 4 # Number of total stations for halft-wing
k = np.arange(1,N+1)
y_k = -(bw/2)*(1 - (2*k - 1)/(2*N))
c_k = Croot*(1 - ((2*(lambdaw - 1)/bw))*y_k)
beta_k = np.arcsin(-2 * y_k * htip / (bw * c_k))
a0_k = a0root - (2*y_k*( a0tip - a0root))/(bw)
aL_0_k = aL_0_root - (2*y_k*( aL_0_tip - aL_0_root))/(bw)
theta_k = np.arccos(-2*y_k/bw)
C = np.zeros((N,N))
for k_i in range(len(k)):
    for n in range(N):
        term1 = (4 * bw) / (a0_k[k_i] * c_k[k_i])
        term2 = (2 * (n + 1) - 1) / np.sin(theta_k[k_i])
        C[k_i, n] = (term1 + term2) * np.sin((2 * (n + 1) - 1) * theta_k[k_i])
        
C_inv = np.linalg.inv(C)

D_k = np.zeros((len(k), len(AoA)))
for ki in range(N):
    for AoAj in range(len(AoA)):
        D_k[ki,AoAj] = AoA[AoAj] - aL_0_k[ki] + beta_k[ki]
        
An = np.zeros((len(k), len(AoA)))
for AoAj in range(len(AoA)):
    An[:, AoAj] = np.dot(C_inv, D_k[:, AoAj])
CL_w = np.array([])
for AoAj in range(len(AoA)):
    CL_w = np.append(CL_w, An[0,AoAj] * np.pi * AR)
delta = np.array([])

print(CL_w)
        








